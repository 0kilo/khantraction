# Phase D Exploration Plan — Identity, Persistence, and Species Fingerprinting

**Date:** 2026-03-29
**Phase:** D — Identity and persistence
**Status:** Active Pathway Selected

## Purpose
This note establishes the roadmap for Phase D. Following the successful breaking of the \(O(4)\) degeneracy in Phase C, we have proven that the internal angles (\(\theta, \phi, \rho\)) generate distinctly different classical objects. Phase D must now determine how to mathematically classify these objects. We must define what constitutes a stable "family" or "species," separate structural identity from pure scale, and test the persistence of these traits under perturbation.

---

## 1. The Core Questions
1. **Neighborhood Stability:** If we take a stable anchor (e.g., `rich_anchor_fully_mixed`) and slightly perturb its internal angles, does the object experience a catastrophic shape transition, or does it smoothly deform while maintaining its core identity?
2. **Species Clustering:** In the observable phase space (e.g., Final Mass vs. Mass Half-Radius), do the objects form discrete clusters (distinct particle species) or a continuous, unorganized smear?
3. **Scale vs. Structure:** How do we prove two objects are the "same kind" if they have different sizes? We must define scale-invariant fingerprints that factor out the \(\omega\) parameter.

---

## 2. The Implementation Roadmap

### Step 1: Scale-Invariant Fingerprinting (`analysis/phase_d_invariant_observables.py`)
Because \(\omega\) controls the overall scale (amplitude) of the object, varying \(\omega\) will trivially change the total mass and radius. To establish an object's *structural identity*, we must define observables that cancel out \(\omega\). 
- **Target Observables:** - The compactness ratio: \(\mathcal{C} = \frac{m_{\text{final}}}{r_{\text{half}}}\)
  - The core-to-bulk ratio.
  - The ratio of MC energy penalty to base geometric energy.
- **Goal:** Prove that if we hold \(\theta, \phi, \rho\) constant but sweep \(\omega\), the invariant fingerprint \(\mathcal{C}\) remains stable.

### Step 2: Dense Neighborhood Sweeps (`analysis/phase_d_neighborhood_stability.py`)
Phase C tested 4 isolated anchors. Phase D requires dense local sampling.
- We will generate a grid of \(N=100\) micro-perturbed seeds around each of the 4 Phase C anchors (Scalar, \(\theta\)-dom, \(\phi\)-dom, Fully-mixed).
- We will execute the exact Maurer-Cartan radial solver over these 400 seeds.
- **Goal:** Determine the gradient of trait changes. Do the traits shift linearly with the angle, or are there "cliffs" where the chart singularity (\(\det J \propto \cos(2\phi)\)) forces a sudden phase transition?

### Step 3: Observable Clustering and Identity Mapping (`analysis/phase_d_species_clustering.py`)
- We will map the outputs of the 400 seeds into a 2D feature space (e.g., Invariant Compactness vs. Integrated Curvature).
- **Goal:** Visually and mathematically identify "basins" or "clusters." If the seeds clump tightly into distinct islands separated by empty voids, Khantraction classically supports distinct, quantized particle-like families.

### Step 4: Phase Assessment (`notes/phase_d_identity_assessment.md`)
- Interpret the clustering data. 
- Formally define the "Indistinguishability Classes" of Khantraction structured objects.
- Close Phase D and prepare for Phase E (External Particle-Likeness).