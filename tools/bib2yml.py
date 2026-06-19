#!/usr/bin/env python3
"""
bib2yml.py — convert a BibTeX file into _data/publications.yml for the
Minimal Mistakes publications page. Keeps the .bib as the single source of truth.

Usage:
    python3 tools/bib2yml.py _bibliography/papers.bib _data/publications.yml

No third-party dependencies. Handles the common @article/@inproceedings/etc.
entries with brace-delimited values. Bolds your name in the author list and
honours a `selected = {true}` field.
"""
import re
import sys
import html

# Surname tokens that should be rendered <strong> in author lists.
ME = ("Gaona Carranza", "Gaona Carranza", "Gaona")


# ---------------------------------------------------------------------------
# Minimal brace-aware BibTeX parser
# ---------------------------------------------------------------------------
def parse_bib(text):
    # First pass: collect @string{key = {value}} macro definitions.
    strings = {}
    for m in re.finditer(r"@string\s*\{\s*([\w-]+)\s*=\s*", text, re.I):
        j = m.end()
        if j < len(text) and text[j] in "{\"":
            close = "}" if text[j] == "{" else "\""
            k = text.find(close, j + 1)
            strings[m.group(1).lower()] = clean(text[j + 1:k])

    entries = []
    i, n = 0, len(text)
    while i < n:
        at = text.find("@", i)
        if at == -1:
            break
        m = re.match(r"@(\w+)\s*\{", text[at:])
        if not m:
            i = at + 1
            continue
        etype = m.group(1).lower()
        if etype == "string":           # skip @string{...}
            i = at + text[at:].find("}") + 1
            continue
        # find matching closing brace for the entry body
        start = at + m.end()            # char after the opening '{'
        depth, j = 1, start
        while j < n and depth:
            if text[j] == "{":
                depth += 1
            elif text[j] == "}":
                depth -= 1
            j += 1
        body = text[start:j - 1]
        # citekey is up to the first comma
        key, _, rest = body.partition(",")
        fields = parse_fields(rest, strings)
        fields["__type__"] = etype
        fields["__key__"] = key.strip()
        fields["__raw__"] = text[at:j].strip()
        entries.append(fields)
        i = j
    return entries


def parse_fields(s, strings=None):
    """Parse `name = {value}` / `"value"` / bare-macro pairs, brace-aware."""
    strings = strings or {}
    fields, i, n = {}, 0, len(s)
    while i < n:
        m = re.match(r"\s*([\w-]+)\s*=\s*", s[i:])
        if not m:
            break
        name = m.group(1).lower()
        i += m.end()
        if i >= n:
            break
        if s[i] == "{":
            depth, j = 1, i + 1
            while j < n and depth:
                if s[j] == "{":
                    depth += 1
                elif s[j] == "}":
                    depth -= 1
                j += 1
            val = s[i + 1:j - 1]
            i = j
        elif s[i] == '"':
            j = i + 1
            while j < n and s[j] != '"':
                j += 1
            val = s[i + 1:j]
            i = j + 1
        else:  # bare value (number / macro)
            j = i
            while j < n and s[j] not in ",\n":
                j += 1
            raw = s[i:j].strip()
            val = strings.get(raw.lower(), raw)   # expand @string macro if known
            i = j
        # consume trailing comma/whitespace
        m2 = re.match(r"\s*,\s*", s[i:])
        if m2:
            i += m2.end()
        fields[name] = clean(val)
    return fields


# LaTeX accent command -> Unicode combining map, e.g. ("'", "a") -> "á"
_ACC = {
    "'": "\u0301", "`": "\u0300", '"': "\u0308", "^": "\u0302",
    "~": "\u0303", "=": "\u0304", ".": "\u0307", "u": "\u0306",
    "v": "\u030C", "H": "\u030B", "c": "\u0327", "k": "\u0328",
}
# Standalone special-letter commands
_SPECIAL = {
    r"\i": "i", r"\j": "j", r"\l": "\u0142", r"\L": "\u0141",
    r"\o": "\u00F8", r"\O": "\u00D8", r"\aa": "\u00E5", r"\AA": "\u00C5",
    r"\ss": "\u00DF", r"\ae": "\u00E6", r"\AE": "\u00C6",
    r"\oe": "\u0153", r"\OE": "\u0152",
}
import unicodedata


def _accents(v):
    # \'{a} | \'a | \'\i | \c{c} | \v{s} ...  -> base + combining mark, NFC-composed
    pat = re.compile(r"\\([\'`\"^~=.uvHck])\s*(?:\{\s*(\\?[A-Za-z]+)\s*\}|(\\[ij])|([A-Za-z]))")

    def repl(m):
        mark = _ACC.get(m.group(1))
        base = m.group(2) or m.group(3) or m.group(4) or ""
        base = _SPECIAL.get(base, base)          # \i -> i, etc.
        if mark is None:
            return base
        return unicodedata.normalize("NFC", base + mark)

    v = pat.sub(repl, v)
    for k, val in _SPECIAL.items():              # bare \i \o \ss ... outside accents
        v = v.replace(k, val)
    return v


def clean(v):
    v = _accents(v)
    v = v.replace("\\&", "&").replace("\\%", "%").replace("\\$", "$")
    v = v.replace("{", "").replace("}", "")
    v = re.sub(r"\\[a-zA-Z]+", "", v)            # drop any leftover \commands
    v = v.replace("\\", "")
    v = v.replace("--", "\u2013")
    v = re.sub(r"\s+", " ", v).strip()
    return v


# ---------------------------------------------------------------------------
# Author formatting:  "Last, First Middle"  ->  "F. M. Last"  (+ bold me)
# ---------------------------------------------------------------------------
def fmt_authors(raw):
    out = []
    for a in re.split(r"\s+and\s+", raw):
        a = a.strip()
        if not a:
            continue
        if "," in a:
            last, first = [p.strip() for p in a.split(",", 1)]
        else:
            parts = a.split()
            last, first = parts[-1], " ".join(parts[:-1])
        initials = " ".join(f"{p[0]}." for p in first.split() if p)
        name = f"{initials} {last}".strip()
        if any(tok in last for tok in ME):
            name = f"<strong>{name}</strong>"
        out.append(name)
    if len(out) > 1:
        return ", ".join(out[:-1]) + ", and " + out[-1]
    return out[0] if out else ""


# ---------------------------------------------------------------------------
def yq(s):
    """YAML-quote a scalar safely (double-quoted, escape backslash + quote)."""
    s = s.replace("\\", "\\\\").replace('"', '\\"')
    return f'"{s}"'


def main(src, dst):
    text = open(src, encoding="utf-8").read()
    entries = parse_bib(text)
    # newest first
    entries.sort(key=lambda e: int(re.sub(r"\D", "", e.get("year", "0")) or 0),
                 reverse=True)
    lines = ["# Auto-generated by tools/bib2yml.py — edit papers.bib, not this file.\n"]
    for e in entries:
        venue = e.get("journal") or e.get("booktitle") or ""
        url = e.get("url") or (f"https://doi.org/{e['doi']}" if e.get("doi") else "")
        lines.append(f"- key: {yq(e['__key__'])}")
        lines.append(f"  title: {yq(e.get('title',''))}")
        lines.append(f"  authors: {yq(fmt_authors(e.get('author','')))}")
        lines.append(f"  venue: {yq(venue)}")
        lines.append(f"  year: {int(''.join(filter(str.isdigit, e.get('year','0'))) or 0)}")
        if e.get("doi"):
            lines.append(f"  doi: {yq(e['doi'])}")
        if url:
            lines.append(f"  url: {yq(url)}")
        if e.get("preview"):
            lines.append(f"  preview: {yq(e['preview'])}")
        if str(e.get("selected", "")).lower() == "true":
            lines.append("  selected: true")
        # preserve the raw BibTeX for the <details> toggle (block scalar)
        raw = e["__raw__"]
        lines.append("  bibtex: |-")
        for rl in raw.splitlines():
            lines.append("    " + rl)
        lines.append("")
    open(dst, "w", encoding="utf-8").write("\n".join(lines))
    print(f"Wrote {dst} with {len(entries)} entries.")


if __name__ == "__main__":
    if len(sys.argv) != 3:
        print(__doc__)
        sys.exit(1)
    main(sys.argv[1], sys.argv[2])
