# Phase K Data Assessment - Refreshed Solution Interpretation

**Date:** 2026-04-02  
**Phase:** K - Multi-Particle Interactions  
**Status:** Complete after audit refresh

## Purpose

This note interprets the regenerated Phase K solution artifacts directly so the closure summary can cite data rather than only raw files.

The active data source is the refreshed proxy runtime:

- `analysis/phase_k/phase_k_multi_fold_force_law.py`
- `solutions/phase_k/phase_k_multi_fold_interaction/summary.json`
- `solutions/phase_k/phase_k_multi_fold_interaction/bulk_force_law.csv`
- `solutions/phase_k/phase_k_multi_fold_interaction/pair_comparisons.csv`
- `solutions/phase_k/phase_k_multi_fold_interaction/slices_1d_angle_interaction.csv`
- `solutions/phase_k/phase_k_multi_fold_interaction/slices_2d_theta_rho_interaction.csv`
- `solutions/phase_k/phase_k_multi_fold_interaction/slices_2d_theta_phi_interaction.csv`
- `solutions/phase_k/phase_k_multi_fold_interaction/slices_2d_phi_rho_interaction.csv`

---

## 1. Bulk distance sweep

The regenerated bulk table tracks three representative pairings:

- `base_vs_base`
- `base_vs_sign_flipped`
- `base_vs_chiral_flip`

At the representative near-`D = 3` row, the derived force signs are:

- `base_vs_base`: positive
- `base_vs_sign_flipped`: negative
- `base_vs_chiral_flip`: positive

Interpretation:

- the present proxy does distinguish pair types by interaction sign,
- but that sign change alone does not prove anything about true geometric force laws or topological charge.

---

## 2. Pair comparison table

The regenerated pair comparison file is the most important audit artifact because it combines:

- chirality values,
- force signs,
- and fit diagnostics.

Its decisive results are:

- `base_vs_sign_flipped`:
  - left chi `= -1.0`
  - right chi `= -1.0`
  - same chirality `= True`
  - force sign at fixed distance `= -2.3471508503031377`

- `base_vs_chiral_flip`:
  - left chi `= -1.0`
  - right chi `= 1.0`
  - same chirality `= False`
  - force sign at fixed distance `= 2.029873252405542`

Interpretation:

- the attractive pair in this proxy is same-chirality,
- the opposite-chirality pair is still repulsive,
- so the present sign structure does not implement the advertised charge rule.

---

## 3. Force-law fit diagnostics

For the base pair, the regenerated table reports:

- force log-log slope `= -2.972105002447939`
- force power-fit linear-space `R^2 = -11.51889900698413`
- force exponential-fit linear-space `R^2 = 0.5272042280673697`

Interpretation:

- the old inverse-square-style reading was an overinterpretation of the log-log slope,
- the power-law reconstruction is actually very poor in linear space,
- and the present proxy is better understood as finite-range decay from exponential envelopes.

So the distance sweep does support a force-gradient proxy, but not a robust macroscopic `1/D^2` law.

---

## 4. Angular slice interpretation

The refreshed package now satisfies the full-domain protocol:

- 1D slices on `[-2pi, 2pi]`
- 2D slices on `[-2pi, 2pi]^2`

The regenerated 1D ranges are:

- `theta`: `[-2.8966008388979945, 4.960347278678194]`
- `phi`: `[0.5408139625415908, 4.469288021329676]`
- `rho`: `[0.5408139625415906, 4.469288021329676]`

Interpretation:

- the current proxy is sensitive to all three angular coordinates,
- because the kernel is a raw signed dot product of parameter amplitudes,
- and not because the active runtime has derived a non-commutative scattering geometry.

That is why the old "phi remains the primary switch for interaction polarity" claim did not survive the audit.

---

## 5. Summary of what the data actually supports

The regenerated Phase K data supports four narrow conclusions:

1. A separated-envelope interaction proxy exists and produces signed overlap energies.
2. A derived force-gradient proxy exists as a function of distance.
3. The current sign rule does not follow the audited chirality operator.
4. The present bulk scaling does not support the old inverse-square claim.

That is the interpretation carried forward into the refreshed closure summary.
