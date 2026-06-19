---
title: "Reading imaginary phonons near Γ: artifact or instability?"
date: 2026-01-15
categories: [notes]
tags: [phonons, dft, methods]
excerpt: "Why a soft mode at the zone center is not automatically a structural instability — the sum-rule, rotational-invariance, and basis-set checks, worked through on a monolayer SnSe₂ dispersion."
toc: true
toc_label: "Contents"
toc_sticky: true
---

A negative (imaginary) frequency in a phonon dispersion is read as a dynamical instability —
the crystal can lower its energy by freezing in that displacement pattern. But before believing
any soft mode, especially one at or near $$\Gamma$$, it pays to separate genuine physics from
numerical artifacts.

## Case in point: monolayer 1T-SnSe₂

Here is the kind of result that motivates all of this — a phonon calculation for a 1T-SnSe₂
monolayer, one of the systems I actually work on:

{% include figure image_path="/assets/images/2026-01-15-snse2-za-artifact.png" alt="Phonon dispersion and projected DOS of monolayer 1T-SnSe2 along Gamma–M–K–Gamma, with the flexural ZA branch dipping just below zero near Gamma" caption="**Monolayer 1T-SnSe₂**, phonon dispersion along Γ–M–K–Γ with atom-projected DOS (Se, Sn). Look at the lowest branch on either side of Γ: the flexural (ZA) mode dips just below zero — there is a matching sliver of negative DOS at the bottom of the right panel. SnSe₂ is a known, stable 2D semiconductor, so this is a *suspect*, not a verdict. The dip is small (≈0.1 THz on an 8 THz axis); a zoom-in on Γ makes it obvious." %}

Look near $$\Gamma$$. The lowest branch — the out-of-plane flexural (ZA) mode — does not sit
cleanly at zero; it dips a hair *below* it on both sides of the zone center. Taken at face value,
that imaginary frequency says the freestanding monolayer is dynamically unstable: it would rather
buckle than stay flat.

I do not believe it for a second, and neither should you. 1T-SnSe₂ is a real, experimentally known
layered semiconductor; a freestanding monolayer that genuinely wanted to corrugate would be a
remarkable claim, not a blemish on a band-structure plot. Everywhere else in the BZ the branches are
clean and positive. The only defect is a small imaginary ZA pocket sitting *exactly* at $$\Gamma$$ —
which is the single most artifact-prone place a soft mode can appear. The rest of this post is the
machinery for being sure, and at the end I come back to what is actually going on in this figure.

## The dynamical matrix

The harmonic phonon frequencies $$\omega_{\mathbf{q}\nu}$$ are eigenvalues of the dynamical
matrix built from the interatomic force constants $$\Phi$$:

$$
D_{\alpha\beta}^{\kappa\kappa'}(\mathbf{q})
= \frac{1}{\sqrt{M_\kappa M_{\kappa'}}}
\sum_{l'} \Phi_{\alpha\beta}^{0\kappa,\,l'\kappa'}\,
e^{\,i\mathbf{q}\cdot\left(\mathbf{R}_{l'} - \mathbf{R}_{0}\right)},
\qquad
\det\!\left[ D(\mathbf{q}) - \omega_{\mathbf{q}\nu}^2\, \mathbf{1} \right] = 0 ,
$$

where $$\kappa$$ indexes basis atoms, $$\alpha,\beta$$ Cartesian directions, and $$l'$$ runs over
lattice vectors.

## Why Γ is special

Translational invariance forces the **acoustic sum rule (ASR)**: a rigid shift of the whole
crystal costs no energy, so

$$
\sum_{l'\kappa'} \Phi_{\alpha\beta}^{0\kappa,\,l'\kappa'} = 0
\quad\Longrightarrow\quad
\omega_{\Gamma,\nu}^{\text{acoustic}} = 0 .
$$

In practice the ASR is only satisfied to within the numerical accuracy of your force constants.
Residual drift shows up precisely as small spurious frequencies at $$\Gamma$$ — sometimes a few
cm⁻¹, sometimes a deceptively large few THz if the basis or grid is poor.[^1]

## Beyond translation: rotational invariance and the Huang conditions

The translational ASR is the sum rule everyone enforces — it is what phonopy's `FC_SYMMETRY`
and the standard acoustic-sum-rule correction impose. But it is only *one* of the invariance
conditions the harmonic lattice potential must satisfy at equilibrium, and for low-dimensional
systems it is emphatically not the binding one.

The complete set, the **Born–Huang invariance conditions**, follows from the conservation of
total linear and angular momentum — Noether's theorem applied to the lattice potential.[^2]
At equilibrium the first-order IFCs vanish, and the constraints on the second-order IFCs
collapse to three. Writing $$\Phi_{\kappa\alpha,\kappa'\beta}$$ for the force constant between
atom $$\kappa$$ in the reference cell and atom $$\kappa'$$ anywhere in the Born–von Kármán
supercell (so $$\kappa'$$ now subsumes the cell index $$l'$$), and $$\tau_{\kappa\alpha}$$ for
equilibrium positions, they read:

**Translational invariance** — the ASR above, rewritten as a sum over supercell atoms:

$$
\sum_{\kappa'} \Phi_{\kappa\alpha,\kappa'\beta} = 0 .
$$

**Rotational invariance** (Born–Huang) — the IFCs weighted by equilibrium positions are
constrained pairwise:

$$
\sum_{\kappa'} \Phi_{\kappa\alpha,\kappa'\beta}\,\tau_{\kappa'\gamma}
= \sum_{\kappa'} \Phi_{\kappa\alpha,\kappa'\gamma}\,\tau_{\kappa'\beta} .
$$

**The Huang (equilibrium) conditions** — *not* a rotational constraint but the statement that
the stress tensor vanishes:

$$
\sum_{\kappa\kappa'} \Phi_{\kappa\alpha,\kappa'\beta}\,\tau_{\kappa\kappa'\gamma}\,\tau_{\kappa\kappa'\delta}
= \sum_{\kappa\kappa'} \Phi_{\kappa\gamma,\kappa'\delta}\,\tau_{\kappa\kappa'\alpha}\,\tau_{\kappa\kappa'\beta} ,
$$

with $$\tau_{\kappa\kappa'\gamma} = \tau_{\kappa'\gamma} - \tau_{\kappa\gamma}$$ the interatomic
separation along $$\gamma$$. These three, together with space-group and permutation symmetry,
are the *complete* description of the invariance conditions at equilibrium.[^3]

Two things are worth internalizing. First, the rotational and Huang conditions are violated by
exactly the same numerical pathologies as the translational ASR — incomplete basis sets, sparse
Brillouin-zone sampling, finite-displacement noise — so the basis-set discipline from the
checklist below is doing double duty. Second, and far less obvious: **phonopy's `FC_SYMMETRY`
imposes neither the rotational invariance nor the Huang condition.** It symmetrizes the IFCs under
permutation and enforces the translational sum rule, and it stops there. If you converge your force
constants, switch on `FC_SYMMETRY`, and *still* see a misbehaving acoustic branch near $$\Gamma$$,
you have not ruled out an artifact — you have only ruled out the *translational* one.

## The 2D trap: the flexural (ZA) branch

This is where it bites, and it bites precisely in the systems I work on — monolayers and few-layer
heterostructures. In a 2D crystal the out-of-plane flexural acoustic (ZA) branch should disperse
*quadratically*, $$\omega_{\mathrm{ZA}}(\mathbf{q}) \sim q^2$$, in the long-wavelength limit, with a
polarization that is purely out-of-plane (along the vacuum direction). That $$q^2$$ law is the
lattice-dynamical fingerprint of a membrane's bending rigidity, and it is universal across
low-dimensional crystals.[^4]

What a finite-displacement or DFPT calculation actually hands you, more often than not, is a ZA
branch that is *linear* near $$\Gamma$$ — or worse, one that dips to small imaginary frequencies
just off the zone center (the SnSe₂ figure at the top is precisely this). For years a linear or
slightly soft ZA was read as borderline dynamical instability.[^4] It usually is not. Lin, Poncé,
and Marzari showed cleanly that the linear (or imaginary) ZA branch is the signature of two
*violated* conditions: broken rotational invariance and residual stress.[^3] Restore both — enforce
the Born–Huang rotational invariance *and* the Huang vanishing-stress condition — and the leading
linear term cancels identically, leaving the physical $$q^2$$ branch with purely out-of-plane
polarization.

The roles split in an instructive way. For a high-symmetry, centrosymmetric monolayer like graphene
the rotational invariance is automatically satisfied by symmetry, so the Born–Huang correction does
nothing; it is the *Huang* (vanishing-stress) condition that straightens the ZA branch into a
parabola.[^3] Drop the inversion center — MoS₂ is the canonical case — and the vanishing-stress
condition alone is no longer sufficient: you need the rotational invariance as well.[^3]

And here is the practical trap that catches careful people. There is residual stress in the
**vacuum direction** even after a high-quality relaxation with a 2D Coulomb cutoff, because the
periodic images still interact weakly across the vacuum gap.[^4] Any nonzero stress feeds a linear
term into the bending dispersion and suppresses the quadratic one. So "I relaxed until the forces
and the in-plane stress were small" does *not* protect you — the offending component is the stress
along $$\hat{z}$$, which you may not even be printing.

For infrared-active 2D semiconductors — which is most of them, with nonzero Born charges; SnSe₂ and
WSe₂ included — there is one more wrinkle. The long-range dipole–dipole interaction contributes to
*both* the stress tensor and the rotational invariance, so imposing the conditions on the
short-range IFCs alone still leaves residual imaginary ZA frequencies near $$\Gamma$$.[^3] The fix
is to impose the *polar* Born–Huang and *polar* Huang conditions: correct the short-range IFCs in
the presence of the analytic long-range part, then add the non-analytic LO–TO contribution back. If
you are doing NAC / Born-charge phonons in a polar monolayer and chasing a soft ZA branch, this is
the subtlety to know about.

### Back to the SnSe₂ dip

The opening figure has every hallmark of the artifact: small, imaginary, in the ZA branch, parked at
$$\Gamma$$, in a material no one expects to spontaneously buckle, with a clean dispersion everywhere
else in the BZ. The symmetry even tells you *which* correction should do the work. 1T-SnSe₂ is
**centrosymmetric** — space group $$P\bar{3}m1$$, with an inversion center at the Sn site — so it
sits in graphene's camp rather than MoS₂'s: the rotational-invariance correction is, by the same
logic, likely a near no-op, and the operative fix is the Huang vanishing-stress condition,
specifically the residual stress along $$\hat{z}$$ that survives even a tight relaxation with a 2D
Coulomb cutoff. And because SnSe₂ is infrared-active — it has $$A_{2u}$$ and $$E_u$$ modes and
nonzero Born charges — the conditions must be imposed in their *polar* form; correcting the
short-range IFCs alone would leave exactly this kind of residual imaginary ZA near $$\Gamma$$.[^3]
My money is on the dip collapsing into a clean $$q^2$$ parabola once the $$z$$-stress is genuinely
zeroed and the polar Huang condition is applied — but the honest move is to run that check, not to
assert it. (And if the imaginary pocket had instead been sitting away from $$\Gamma$$, none of this
would apply — see the next section.)

## How often is it real? One number, and one diagnostic

The paper gives an unusually direct answer to the question that actually matters. Of 245 candidate
2D materials from the Mounet et al. high-throughput exfoliation database,[^6] 187 showed soft modes
or an incorrect linear ZA branch when only a naive sum rule was applied. After the full invariance
and equilibrium conditions were enforced, **158 of them became dynamically stable with a clean
quadratic ZA branch.**[^3] That is the majority of the flagged set turning out to be
sum-rule/stress artifacts rather than new physics.

The remaining 87 are the interesting ones for our purposes: 54 are *genuinely* dynamically unstable,
and 33 need tighter numerical convergence.[^3] And the genuinely unstable ones carry a tell worth
committing to memory: their **imaginary frequencies are not located around $$\Gamma$$.**[^3] This is
the single most useful discriminator I know. A small imaginary or linear ZA branch *at* the zone
center, in a 2D system, is overwhelmingly likely to be an invariance/stress artifact — that is the
SnSe₂ case above. A robust imaginary pocket *away* from $$\Gamma$$ — at a zone-boundary point, along
a particular line, at some incommensurate $$\mathbf{q}$$ — is the kind of soft mode that corresponds
to a real structural distortion you can freeze in and relax into. The location of the instability in
the BZ tells you, before any further work, which regime you are in.

A caveat on the 33 stragglers: even with the conditions imposed, they did not parabolize. Some need
only tighter relaxation and DFPT grids, but a few point at genuinely missing physics in the
harmonic-plus-dipole model — strain–electric-field coupling and dynamical *quadrupoles*
(flexoelectric/piezoelectric effects) that the standard dipole–dipole treatment omits.[^3] Black
phosphorus and arsenene, with nonvanishing $$yz$$ components of the Born-charge tensor, are the
worked examples. So the conditions are a powerful filter, not a panacea.

For bulk 3D crystals none of this drama applies: Lin et al. confirm that the rotational and Huang
corrections are negligible for bulk silicon and even for low-symmetry triclinic CaP₃ — a bulk
crystal is periodic in all three directions and has no rigid-rotation degree of freedom to
protect.[^3] The only residual fingerprint in bulk is a slightly asymmetric elastic tensor,
$$c_{ij} \neq c_{ji}$$, from the broken conditions. The flexural problem is intrinsically a
low-dimensional one.

## My checklist

When a mode goes soft, in order:

1. **Enforce the translational ASR / `FC_SYMMETRY`** and re-diagonalize. If the mode at $$\Gamma$$ vanishes, it was drift, not physics.
2. **Ask *where* in the BZ the imaginary frequency lives.** At or near $$\Gamma$$ — especially the ZA branch of a 2D system — suspect an artifact and keep going. Robust and *away* from $$\Gamma$$, surviving refinement, is far more likely to be a real instability; skip to step 6.
3. **Inspect the on-site block** $$\Phi_{zz}^{\kappa\kappa}$$ for the offending atom/direction. A wrong sign (e.g. I once measured $$\Phi_{zz}(\mathrm{W}) = -3.20~\text{eV/Å}^2$$) points at an incomplete basis.
4. **Converge the basis**, not just the k-mesh — minimal/pseudopotential bases lacking semicore or polarization (f) shells routinely fabricate out-of-plane instabilities in heavy-element systems. The same incompleteness breaks rotational invariance, so this step pays off twice.
5. **For a 2D/1D system, enforce rotational invariance and the Huang (vanishing-stress) condition**, not just the translational ASR — `FC_SYMMETRY` does not do this. Check the residual stress *in the vacuum direction* specifically; for a polar monolayer, use the polar versions of the conditions so the long-range part is handled consistently. If the ZA branch straightens into a $$q^2$$ parabola, it was an invariance/stress artifact.[^5]
6. **Only then** consider it real, displace along the eigenvector, and relax into the lower-symmetry structure.

The takeaway: a soft mode at $$\Gamma$$ is a hypothesis, not a result. Most of mine have turned
out to be sum-rule or basis-set artifacts — and now I add a third class, the low-dimensional ZA
modes that need rotational invariance and a genuinely stress-free cell, of which the SnSe₂ dip at
the top is a textbook specimen. In every case the fix changed the science.

[^1]: This is the failure mode behind a lot of "exotic instability" claims in the 2D literature; the imaginary branch disappears once the force constants are converged and the ASR is imposed — and, in low-dimensional systems, once rotational invariance and the vanishing-stress (Huang) condition are imposed as well (see below).
[^2]: The conditions trace to M. Born and K. Huang, *Dynamical Theory of Crystal Lattices* (Oxford University Press, 1954), with the second-order acoustic sum rules in the form used here laid out by G. Leibfried and W. Ludwig, "Theory of anharmonic effects in crystals," *Solid State Physics* **12**, 275 (1961). The link to total-momentum and angular-momentum conservation is Noether's theorem.
[^3]: C. Lin, S. Poncé, and N. Marzari, "General invariance and equilibrium conditions for lattice dynamics in 1D, 2D, and 3D materials," *npj Comput. Mater.* **8**, 236 (2022). DOI: [10.1038/s41524-022-00920-6](https://doi.org/10.1038/s41524-022-00920-6). The graphene-vs-MoS₂ split, the polar (infrared-active) treatment, the bulk-vs-LD comparison, and the database statistics quoted here are all from this work.
[^4]: For the linear-ZA-as-instability history and the founding diagnosis, see J. Carrete *et al.*, "Physically founded phonon dispersions of few-layer materials and the case of borophene," *Mater. Res. Lett.* **4**, 204 (2016); the universality of the $$q^2$$ bending law is A. Croy, "Bending rigidities and universality of flexural modes in 2D crystals," *J. Phys.: Mater.* **3**, 02LT03 (2020). The residual vacuum-direction stress and the 2D Coulomb-cutoff / LO-TO machinery are from T. Sohier, M. Gibertini, M. Calandra, F. Mauri, and N. Marzari, "Breakdown of optical phonons' splitting in two-dimensional materials," *Nano Lett.* **17**, 3758 (2017).
[^5]: Codes that impose rotational invariance and the Huang conditions on the IFCs (via ridge-regression / null-space constraints) include hiPhive — F. Eriksson, E. Fransson, and P. Erhart, *Adv. Theor. Simul.* **2**, 1800184 (2019) — and ALAMODE (the `ICONST` constraints). Lin *et al.* integrated the corrections into Quantum ESPRESSO's `q2r.x`/`matdyn.x`.[^3] Plain phonopy `FC_SYMMETRY` does not.
[^6]: N. Mounet *et al.*, "Two-dimensional materials from high-throughput computational exfoliation of experimentally known compounds," *Nat. Nanotechnol.* **13**, 246 (2018); the original phonon screening (with the simpler sum rule) is on Materials Cloud. The 187 / 158 / 54 / 33 split is from the re-analysis in Ref. [^3].
