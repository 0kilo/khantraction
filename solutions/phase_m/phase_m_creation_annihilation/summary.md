# Phase M Analysis Summary: Pair Creation and Annihilation

**Date:** 2026-04-02  
**Phase:** M - Pair Creation / Annihilation

This directory contains the refreshed outputs for the audited Phase M runtime in `analysis/phase_m/phase_m_creation_annihilation_sim.py`.

## 1. Active audited outputs

The current script regenerates these evidence files:

- `bulk_creation_sweep.csv`
- `pair_reference_checks.csv`
- `creation_phi_reference.csv`
- `slices_1d_annihilation_theta.csv`
- `slices_1d_annihilation_phi.csv`
- `slices_1d_annihilation_rho.csv`
- `slices_1d_annihilation.csv`
- `slices_2d_creation_theta_phi.csv`
- `slices_2d_creation_theta_rho.csv`
- `slices_2d_creation_phi_rho.csv`
- `slices_2d_creation_probability.csv`
- `summary.json`

## 2. What the active runtime is

The active runtime is a simplified pair-lifecycle model:

- chirality `chi = cos(2phi)`
- an exact-partner annihilation score
- a fixed creation threshold
- a hand-built singular-sheet susceptibility

So this package is not a solved collision or vacuum-tearing model.

## 3. Interpretation of the data

### 3.1 Annihilation references

`pair_reference_checks.csv` is the key file for interpreting the annihilation side:

- the exact chiral-flip partner returns `Vacuum`,
- the parity partner does not,
- the same-handed copy does not.

That is the main usable annihilation result of the current package.

### 3.2 Creation gate

`bulk_creation_sweep.csv` documents a fixed threshold gate:

- imposed threshold `2.55`
- first sampled created row `2.5510204081632653`

This is not a discovered dynamical threshold.

### 3.3 Phi-localized creation tendency

`creation_phi_reference.csv` and the 2D creation slices show that the current creation rule is strongest near the singular sheets and flat on the `theta-rho` slice at fixed `phi = 0`.

## 4. Conclusions

This solution package is appropriate evidence for a narrowed Phase M claim:

1. the active runtime contains a corrected pair-lifecycle model consistent with audited chirality,
2. it distinguishes exact chiral-flip annihilation from parity or same-handed overlap,
3. it maps a singular-sheet-localized creation tendency under a fixed threshold gate.

It is not evidence that Phase M has already proven dynamical annihilation, genuine vacuum tearing, or completion of the Real Physics Transition Plan.
