# Highlighted publication thumbnails — install

Adds an optional figure beside each paper on /publications/ (the "graphical abstract" look).
Entries without an image just render as text, so you can add them one at a time.

## 1. Drop the files in
    cp -rT mm-pub-images "$SITE"     # $SITE = your main-site folder
This updates tools/bib2yml.py and _pages/publications.html, and creates
assets/images/publications/ for the images. (The new bib2yml.py also folds in the
Python-3.11 year fix, so it replaces your patched copy cleanly.)

## 2. Add an image + a bib field per paper you want to highlight
- Put the image at:  assets/images/publications/<name>.png   (or .jpg)
- In _bibliography/papers.bib, add a `preview` field to that entry, e.g.:

    @article{sen2025grain,
      author  = {...},
      title   = {...},
      journal = ami,
      year    = {2025},
      doi     = {10.1002/admi.202500567},
      selected= {true},
      preview = {sen2025.png}      <-- just the filename
    }

## 3. Regenerate the data file and refresh
    cd "$SITE"
    python3 tools/bib2yml.py _bibliography/papers.bib _data/publications.yml
    # refresh the browser (publications.yml is in _data/, which the server watches)

## Image tips
- A journal TOC/graphical-abstract image or one striking figure works best.
- Landscape or square; ~400-800 px wide source is plenty. Keep each under ~300 KB.
- The thumbnail renders at 150 px wide (full-width on mobile); aspect ratio is preserved.
- The border uses a translucent gray, so it looks right in both Latte and Mocha.
