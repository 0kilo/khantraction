# Phase M Data Assessment - Refreshed Pair-Lifecycle Outputs

**Date:** 2026-04-02  
**Status:** Complete after audit refresh

## 1. Output package

The refreshed Phase M solution directory now contains the active audited evidence files:

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
- `summary.md`

These are the files that should be used to interpret the current runtime.

## 2. What the regenerated data shows

### 2.1 Bulk creation gate

The bulk table contains `50` energy samples. It shows a clean switch from:

- `Sub-threshold fluctuation`

to:

- `L+R Pair Created`

once the scan crosses the fixed gate.

The important reading is:

- imposed threshold: `2.55`
- first sampled created row: `2.5510204081632653`

So the table documents the behavior of the gate, not a discovered onset from dynamics.

### 2.2 Pair-reference checks

The pair-reference table is the most important annihilation evidence:

- exact enantiomer:
  - `Vacuum`
  - `pair_score ~ 1.249e-16`
- parity partner:
  - `Residual Dipole`
  - `pair_score ~ 0.19635`
- same-handed copy:
  - `Residual Dipole`
  - `pair_score ~ 1.80691`

This confirms that the current model now distinguishes the true chiral-flip partner from a parity partner.

### 2.3 One-dimensional annihilation slices

The refreshed annihilation slices show localized vacuum-return windows:

- `theta`: `10 / 100`
- `phi`: `1 / 100`
- `rho`: `12 / 100`

These are not generic annihilation regions. They are narrow compatibility windows around the exact periodic partner conditions allowed by the simplified score.

### 2.4 Two-dimensional creation slices

The refreshed 2D creation slices now satisfy the full `[-2pi, 2pi]` protocol and show:

- strong variation on phi-involving slices,
- flat baseline on the `theta-rho` slice at fixed `phi = 0`.

The named phi reference table makes the localization clearer:

- `phi = 0`: `0.9090909090909091`
- `phi = +pi/4`: `9.999999999999995`
- `phi = -pi/4`: `9.999999999999995`
- `phi = pi/2`: `0.9090909090909091`

So the current creation rule is explicitly singular-sheet localized.

## 3. Correct reading of the data

The regenerated data supports three narrow statements:

1. the active Phase M model can represent exact-partner annihilation differently from parity or same-handed overlap,
2. it can represent a phi-localized creation tendency near the singular sheets,
3. it can represent a fixed energy-threshold gate for pair creation.

The data does not support:

1. a field-theory collision solve,
2. dynamical Maurer-Cartan cancellation in spacetime,
3. an emergent vacuum-tearing threshold derived from the equations of motion,
4. or the claim that the full Real Physics Transition Plan is already complete.
