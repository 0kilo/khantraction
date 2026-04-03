# Phase K Assessment - Direct Same-Background Interaction Refresh

**Date:** 2026-04-02  
**Phase:** K - Multi-Particle Interactions  
**Status:** Complete after direct runtime refresh

## Direct Implementation Update

The old one-dimensional overlap proxy has now been replaced for the directly defined same-background case.

- `analysis/phase_k/phase_k_multi_fold_force_law.py` now computes a real 3D interaction-energy density on a shared grid.
- `solutions/phase_k/phase_k_multi_fold_interaction/bulk_force_law.csv` now contains direct `Delta M(D)` data for scalar, rich, and off-sheet same-background pairs.
- `solutions/phase_k/phase_k_multi_fold_interaction/pair_comparisons.csv` shows that those three families are again exactly degenerate in the direct chain.
- The extracted force gradient is real for the same-background case, but the fitted power exponent is `0.8301296117826079`, so the direct refresh does not recover an inverse-square law.

So Phase K now has direct interaction data rather than an overlap proxy, but the direct same-background interaction is universal across the audited seed family and does not support a species-dependent force law.

Where the older audit-only material below conflicts with this direct implementation update, the direct implementation update and the linked direct outputs take precedence.

## Purpose

This note records what the refreshed Phase K package actually proves after tracing:

- `khantraction_paper.md`
- `notes/real_physics_transition_plan.md`
- `summary/2026-03-31_phase_j_closure_summary.md`
- `notes/phase_j/phase_j_dynamic_stability_assessment.md`
- `summary/2026-03-31_phase_i_closure_summary.md`
- `notes/phase_i/phase_i_constants_derivation_assessment.md`
- `summary/2026-03-29_phase_h_closure_summary.md`
- `notes/phase_h/phase_h_verified_quantum_assessment.md`
- `derivations/derivation_92_multi_fold_interaction_energy.md`
- `analysis/phase_k/phase_k_multi_fold_force_law.py`
- `scripts/run_phase_k_interaction_sim.sh`
- `solutions/phase_k/phase_k_multi_fold_interaction/summary.json`
- `solutions/phase_k/phase_k_multi_fold_interaction/summary.md`
- `solutions/phase_k/phase_k_multi_fold_interaction/bulk_force_law.csv`
- `solutions/phase_k/phase_k_multi_fold_interaction/pair_comparisons.csv`
- `solutions/phase_k/phase_k_multi_fold_interaction/slices_1d_angle_interaction.csv`
- `solutions/phase_k/phase_k_multi_fold_interaction/slices_2d_theta_rho_interaction.csv`
- `solutions/phase_k/phase_k_multi_fold_interaction/slices_2d_theta_phi_interaction.csv`
- `solutions/phase_k/phase_k_multi_fold_interaction/slices_2d_phi_rho_interaction.csv`

---

## 1. What the active Phase K runtime actually is

The refreshed Phase K runtime is not the 3D nonlinear overlap construction sketched in `derivations/derivation_92_multi_fold_interaction_energy.md`.

It is a narrower interaction proxy:

- two separated ordered-state anchors,
- exponentially decaying parameter envelopes,
- a one-dimensional line integral along the separation axis,
- and a signed dot-product kernel on the raw parameter amplitudes.

The regenerated `summary.json` states this explicitly:

- `type = one_dimensional_signed_overlap_proxy`
- "Not a full 3D nonlinear metric-overlap solve."

So every Phase K claim must be read as a statement about this proxy runtime, not as proof that the non-commutative multi-fold interaction density from Derivation 92 has already been implemented.

This matters even more after the refreshed Phase J audit:

- Phase J did not establish solver-backed stable 3D Khantraction particles in the intended nonlinear dynamics.

So Phase K cannot inherit a stronger "real interacting particles" status from the previous handoff.

---

## 2. Main audit corrections

### 2.1 The old scope claim was too strong

The previous summary described the active code as if it had already:

- simulated two interacting 3D folds,
- measured asymptotic metric overlap,
- and extracted a force law from nonlinear geometry.

That was not what the code did. The active runtime only integrated a one-dimensional proxy overlap of exponentially decaying anchor amplitudes.

### 2.2 The old 2D slice package violated the transition-plan domain

The earlier 2D slices only sampled `[-pi, pi]`.

The refreshed solver now scans:

- `theta, phi, rho in [-2pi, 2pi]`

for all 1D and 2D interaction tables, restoring compliance with `notes/real_physics_transition_plan.md`.

### 2.3 The old chirality-based attraction story did not survive the audited operator check

The earlier writeup claimed:

- like chirality repels,
- opposite chirality attracts.

The refreshed pair diagnostics show that this is not what the active proxy does.

In the regenerated comparison table:

- `base_vs_sign_flipped` is attractive,
- but both anchors have `chi = -1`,
- while `base_vs_chiral_flip` is opposite-chirality and remains repulsive.

So the sign rule in the current proxy follows the raw signed anchor vectors, not the audited chirality operator.

### 2.4 The old inverse-square claim was not supportable

The earlier summary promoted the log-log slope `-2.97` as an inverse-square-like force law.

The refreshed fit diagnostics show:

- `base_vs_base` force power-fit linear-space `R^2 = -11.51889900698413`
- `base_vs_base` force exponential-fit linear-space `R^2 = 0.5272042280673697`

So the finite-range log-log exponent is not a stable force-law proof. In the current proxy, the envelopes are exponential by construction.

---

## 3. Main findings

### 3.1 The current package supports a signed separated-envelope interaction proxy

The bulk sweep shows that separated anchors do produce a nonzero interaction mass and a derived force sign.

At the representative fixed distance near `D = 3`:

- `base_vs_base` has `dm = 3.2405806643877946`, force `= 2.4277845344699696`
- `base_vs_sign_flipped` has `dm = -3.1329516906879604`, force `= -2.3471508503031377`
- `base_vs_chiral_flip` has `dm = 2.709452968131478`, force `= 2.029873252405542`

This is a real proxy interaction result. It shows that the sign of the overlap can change across pair choices.

### 3.2 The interaction sign does not follow audited chirality

The regenerated pair table reports:

- `base` chirality: `-1.0`
- `sign_flipped` chirality: `-1.0`
- `chiral_flip` chirality: `1.0`

Yet:

- `base_vs_sign_flipped` is attractive with force sign `-1.0`
- `base_vs_chiral_flip` is repulsive with force sign `+1.0`

So the current proxy does not support the target claim that opposite topological charge attracts while like charge repels.

### 3.3 The old inverse-square reading was a fit artifact

For the base pair:

- force log-log slope = `-2.972105002447939`
- power-fit linear-space `R^2 = -11.51889900698413`
- exponential-fit linear-space `R^2 = 0.5272042280673697`

That means the old "inverse-square-like scaling" sentence was not defensible. The proxy decay is better described as finite-range behavior of an exponential-envelope overlap than as an extracted macroscopic `1/D^2` law.

### 3.4 The angular maps are raw-amplitude-sensitive, not a clean phi-polarity architecture

The refreshed 1D interaction ranges are:

- `theta`: `[-2.8966008388979945, 4.960347278678194]`
- `phi`: `[0.5408139625415908, 4.469288021329676]`
- `rho`: `[0.5408139625415906, 4.469288021329676]`

The current proxy therefore responds to all three angular coordinates because they enter as raw signed amplitudes in the dot-product kernel.

This is not the same thing as a solver-backed phi-controlled polarity switch derived from non-commutative geometry.

---

## 4. Goal status against `notes/real_physics_transition_plan.md`

### Goal 1 - Simulate the spatial interaction of two distinct spacetime-folds separated by a distance `D`

**Status:** Met in proxy form only.

What is met:

- the package evaluates separated anchor overlaps as a function of distance,
- and it produces a signed interaction-mass table with derived force gradients.

What is not met:

- the runtime is not a full 3D two-fold field solve,
- and it does not evolve two regenerated Phase J objects in the intended nonlinear dynamics.

### Goal 2 - Calculate the effective force law by measuring deformation of the asymptotic metric overlaps

**Status:** Partially met in proxy form.

What is met:

- a force-gradient proxy is extracted from the distance-dependent interaction mass.

What is not met:

- no asymptotic metric-overlap deformation is measured,
- and the current fit diagnostics do not support the old inverse-square claim.

### Goal 3 - Determine if identical topological charge repels and opposite charge attracts

**Status:** Not met.

What was tested:

- same-anchor,
- sign-flipped same-chirality,
- and opposite-chirality chiral-flip partner comparisons.

Result:

- attraction / repulsion in the current proxy does not track the audited chirality operator `chi = cos(2phi)`.

---

## 5. Bottom line

**Bottom line:** The refreshed Phase K package supports a narrower interaction-proxy result. Separated ordered-state anchors produce a signed overlap energy and a derived force gradient in a one-dimensional exponential-envelope proxy. But the runtime does not yet implement the 3D nonlinear interaction density from Derivation 92, it does not support an inverse-square force-law claim, and it does not establish attraction/repulsion from audited chirality or topological charge.
