---
permalink: /research/
title: "Research"
excerpt: "Electronic structure, lattice dynamics, and beyond-DFT methods for quantum materials."
author_profile: true
toc: true
toc_label: "Threads"
toc_sticky: true
---

My work sits where **electronic-structure theory**, **lattice dynamics**, and **beyond-DFT
corrections** meet. The unifying question is methodological: I look for systems where standard
functionals break — flat bands, strong correlation — and build the machinery
(hybrids, SOC, MLIPs, spin-wave theory) needed to recover the right physics. Below are the
active threads.

## 2D materials & heterostructures

First-principles defects and phonons in transition-metal dichalcogenides and their
heterostructures, with a focus on **1T-SnSe₂ / 2H-WSe₂**. Recent work: substitutional W defects in
1T-SnSe₂ (CRYSTAL23, hybrid functionals), diagnosing and curing a spurious imaginary out-of-plane
phonon mode that was a basis-set artifact rather than a true dynamical instability, and full phonopy
force-constant workflows on 100+ atom supercells.

*Methods:* CRYSTAL23 (hybrids, SOC), phonopy/VASP/Quantum ESPRESSO, broken-symmetry DFT.

## Chiral materials & spintronics

Chirality and spin transport in low-dimensional tellurium: spin-resolved band structures,
Brillouin-zone spin textures, the spin Hall tensor via pseudo-atomic orbitals (PAOFLOW), and
chirality analysis of finite Te–H oligomers (L/R enantiomers, Kabsch-RMSD validation) in the
context of the **chiral-induced spin selectivity (CISS)** effect.

*Methods:* VASP, Quantum ESPRESSO, PAOFLOW, Wannier90, VMD-based analysis pipelines.

## Magnetic materials & spin dynamics

Magnetic ground states and excitations in 2D and bulk magnets (**CrI₃, CrSBr, Mn₅Si₃**). The
central project: extracting exchange tensors from **CRYSTAL23 hybrid + SOC** broken-symmetry
calculations and feeding them into a **linear spin-wave theory** engine to find magnetic ground
states where semilocal DFT and DFT+U disagree — plus skyrmion-scale physics (DMI, micromagnetics)
via the QE → Wannier90 → TB2J → UppASD chain.

*Methods:* Quantum ESPRESSO, TB2J, UppASD, LSWT.

## Methods: Machine-learned interatomic potentials

Cross-cutting methods work on extending Machine-learned interatomic potentials to the dynamical 
matrix (phonons), and machine-learned interatomic potentials for accelerated screening.

*Methods:* Machine-learned interatomic potentials, high-throughput screening.

---

For the formal write-ups behind some of this — spin-wave theory, the acoustic sum rule,
density-driven error — see the **[THE GRID](https://nanotheochem.github.io/the-grid/)** ↗.
A full list of publications is on the **[publications page](/publications/)**.
