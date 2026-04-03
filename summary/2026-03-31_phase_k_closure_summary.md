# Phase K Closure Summary — Direct Same-Background Interaction Energy

**Date:** 2026-03-31  
**Phase:** K — Multi-Particle Interactions  
**Status:** Closed after direct runtime refresh

## 0. Project-level disposition

Phase K is no longer blocked by the absence of any direct interaction calculation. The rebuilt package now computes a real 3D interaction-energy density and force gradient for directly defined same-background pair initial data. The remaining blockers are:

- the force law is not inverse-square,
- the direct data are species-blind across scalar, rich, and off-sheet families,
- mixed-background multi-species composition is still not mathematically defined in a direct way.

The project-level synthesis is recorded in:

- `notes/2026-04-02_direct_data_closure_plan.md`
- `summary/2026-04-02_gap_closure_summary.md`
- `summary/2026-04-02_khantraction_model_conclusion.md`

## 1. Scope and motivation

Phase K asks whether two separated Khantraction objects interact in a structured way and whether any force law or polarity rule survives direct implementation.

After the direct refresh, the honest scope is narrower but stronger:

1. construct directly defined same-background pairs on a shared 3D grid,
2. integrate the real interaction-energy density,
3. extract `Delta M(D)` and `F(D)`,
4. test whether different internal seed families actually produce different interaction data.

## 2. Support chain

This closure summary is supported by:

- `khantraction_paper.md`
- `notes/real_physics_transition_plan.md`
- `derivations/derivation_92_multi_fold_interaction_energy.md`
- `analysis/direct_ordered_manifold.py`
- `analysis/phase_k/phase_k_multi_fold_force_law.py`
- `notes/phase_k/phase_k_multi_particle_interactions_assessment.md`
- `solutions/phase_k/phase_k_multi_fold_interaction/summary.json`
- `solutions/phase_k/phase_k_multi_fold_interaction/bulk_force_law.csv`
- `solutions/phase_k/phase_k_multi_fold_interaction/pair_comparisons.csv`
- `solutions/phase_k/phase_k_multi_fold_interaction/slices_1d_angle_interaction.csv`
- `solutions/phase_k/phase_k_multi_fold_interaction/slices_2d_theta_rho_interaction.csv`
- `solutions/phase_k/phase_k_multi_fold_interaction/slices_2d_theta_phi_interaction.csv`
- `solutions/phase_k/phase_k_multi_fold_interaction/slices_2d_phi_rho_interaction.csv`

## 3. Method

### 3.1 Direct same-background pair construction

The refresh builds pair initial data on a shared 3D grid for:

- `scalar_pair`
- `rich_pair`
- `phi_offsheet_pair`

with matched asymptotic background values for each pair family.

### 3.2 Direct interaction-energy density

For each distance `D`, the script computes

$$
\rho_{\mathrm{int}} = \rho_{\mathrm{tot}} - \rho_1 - \rho_2 + \rho_{\mathrm{bg}}
$$

and integrates

$$
\Delta M(D)=\int d^3x\,\rho_{\mathrm{int}}.
$$

This is the right method for Goals 1 and 2 because it is an actual 3D interaction-energy calculation, not the old one-dimensional overlap proxy.

### 3.3 Direct force-gradient extraction

The script differentiates `Delta M(D)` numerically to obtain `F(D)`.

### 3.4 Full same-background slice protocol

The phase also rebuilds 1D and 2D same-background angle scans at fixed separation to test whether common-seed family changes affect the direct interaction energy.

## 4. Results against the transition plan

### 4.1 Goal 1 — Simulate the spatial interaction of two distinct spacetime-folds separated by distance `D`

**Status:** Met for the directly defined same-background case.

**Result:** Phase K now contains a real 3D interaction-energy dataset on a shared domain.

### 4.2 Goal 2 — Calculate the effective force law

**Status:** Met for same-background direct data, inverse-square version not met.

**Result:** A direct force gradient is extracted from `Delta M(D)`, but the fitted behavior is not inverse-square.

### 4.3 Goal 3 — Determine whether different species attract/repel differently

**Status:** Not met.

**Result:** The direct same-background data are identical across scalar, rich, and off-sheet families.

### 4.4 Common slice protocol

**Status:** Met for the directly defined same-background case.

The rebuilt package includes 1D and 2D same-background angle scans over the full active domain.

## 5. Direct findings

The decisive numbers are:

- scalar `Delta M(D)` range: `[0.00031189491732663735, 0.0003726299482008006]`
- rich `Delta M(D)` range: `[0.00031189491732663735, 0.0003726299482008006]`
- off-sheet `Delta M(D)` range: `[0.00031189491732663735, 0.0003726299482008006]`
- scalar force power exponent: `0.8301296117826079`
- scalar force power-fit linear-space `R^2`: `0.9910489533515593`
- scalar force exponential-fit linear-space `R^2`: `0.9673762664064315`

The same-background 1D and 2D angle scans are also flat:

- `theta` 1D `Delta M` range is a single value
- `phi` 1D `Delta M` range is a single value
- `rho` 1D `Delta M` range is a single value
- all 2D same-background planes are likewise flat

## 6. Interpretation

Phase K now has a direct 3D interaction result, but it is not the result the old particle-zoo story needed.

What survives:

- same-background pairs have a real integrated interaction energy,
- and that energy yields a real direct force gradient.

What fails:

- the law is not inverse-square,
- scalar, rich, and off-sheet families are interaction-degenerate,
- and no species-dependent polarity rule appears.

So the direct refresh converts K from “no real interaction implementation” to “real but universal same-family interaction.”

## 7. Supporting outputs

Key files:

- `solutions/phase_k/phase_k_multi_fold_interaction/summary.json`
- `solutions/phase_k/phase_k_multi_fold_interaction/summary.md`
- `solutions/phase_k/phase_k_multi_fold_interaction/bulk_force_law.csv`
- `solutions/phase_k/phase_k_multi_fold_interaction/pair_comparisons.csv`
- `solutions/phase_k/phase_k_multi_fold_interaction/slices_1d_angle_interaction.csv`

## Bottom line

**Bottom line:** Phase K now closes on a direct 3D same-background interaction-energy implementation rather than a one-dimensional proxy. The rebuilt package shows that same-background pair data generate a real integrated `Delta M(D)` and a direct force gradient. But those results are identical across scalar, rich, and off-sheet families, they do not follow an inverse-square law, and they do not establish any mixed-background species polarity rule. So Phase K now supports universal same-family interaction structure, not particle-species interaction physics.
