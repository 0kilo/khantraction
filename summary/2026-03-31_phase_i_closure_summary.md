# Phase I Closure Summary — Direct Pullback Coefficient Replacement

**Date:** 2026-03-31  
**Phase:** I — First-Principles Derivation of Constants  
**Status:** Closed after direct runtime refresh

## 0. Project-level disposition

Phase I is no longer blocked at the level of coefficient replacement. The exact pullback metric, inverse metric, and Christoffel symbols are now the active coefficient source in the rebuilt direct runtime used by Phases J, E, and K. The remaining issue is empirical: that direct chain preserves universal objecthood but does not generate distinct species observables. The project-level synthesis is recorded in:

- `notes/2026-04-02_direct_data_closure_plan.md`
- `summary/2026-04-02_gap_closure_summary.md`
- `summary/2026-04-02_khantraction_model_conclusion.md`

## 1. Scope and motivation

`khantraction_paper.md` treats Khantraction as an exploratory structured-fold model built on the ordered quaternionic map

$$
Q(\omega,\theta,\phi,\rho)=e^\omega e^{\theta i} e^{\phi j} e^{\rho k}.
$$

`notes/real_physics_transition_plan.md` then asks a sharper question:

> can the active dynamical constants be replaced by geometry derived directly from that ordered map?

Before this refresh, Phase I only had a geometry-level answer. After the direct implementation pass, the burden of proof is broader:

1. show the exact pullback anisotropy on the full active domain,
2. wire that anisotropy into a live direct runtime,
3. check whether the rebuilt runtime supports regular branches without the exploratory `beta_a` path,
4. and see whether the resulting direct chain produces distinct species observables or only universal objecthood.

## 2. Support chain

This closure summary is supported by:

- `khantraction_paper.md`
- `notes/real_physics_transition_plan.md`
- `derivations/derivation_71_exponential_quaternion_parameter_mapping_clean.md`
- `derivations/derivation_75_ordered_pullback_and_exploratory_directional_phase_b_runtime.md`
- `derivations/derivation_90_geometric_origin_of_anisotropy.md`
- `analysis/direct_ordered_manifold.py`
- `analysis/phase_i/phase_i_geometric_anisotropy_scan.py`
- `notes/phase_i/phase_i_constants_derivation_assessment.md`
- `solutions/phase_i/phase_i_geometric_anisotropy_scan/summary.json`
- `solutions/phase_i/phase_i_geometric_anisotropy_scan/direct_profile_runs.csv`
- `solutions/phase_i/phase_i_geometric_anisotropy_scan/branch_stability_scan.csv`
- `solutions/phase_i/phase_i_geometric_anisotropy_scan/direct_runtime_coefficients.json`

## 3. Method

### 3.1 Exact pullback scan

The script evaluates the exact pullback eigenvalues

$$
\lambda_\phi=e^{2\omega}, \qquad
\lambda_\pm=e^{2\omega}(1\pm \sin 2\phi)
$$

across:

- full 1D `phi`, `theta`, and `rho` slices on `[-2pi, 2pi]`,
- full 2D `(phi, rho)`, `(theta, phi)`, and `(theta, rho)` slices on `[-2pi, 2pi]^2`,
- exact named reference points,
- and explicit alternating sheet-family tables.

This is the right method for Goal 1 because it directly tests whether anisotropy is already built into the ordered map rather than inserted by hand.

### 3.2 Direct runtime bridge

The refresh then implements the exact pullback metric, inverse metric, and Christoffel symbols in `analysis/direct_ordered_manifold.py` and records that downstream Phases J, E, and K import that shared module.

This is the right method for Goal 1 because it moves the project from “candidate geometry mechanism” to “active solver coefficient source.”

### 3.3 Branch-stability scan

The refresh adds a direct empirical scan over:

- `lambda_q in {0.005, 0.01, 0.02, 0.04}`
- `A0 in {0.01, 0.02, 0.03, 0.04}`

using the direct ordered-variable radial solver.

This is the right method for Goal 2 because it checks whether regular branch behavior survives in the new non-`beta_a` runtime.

## 4. Results against the transition plan

### 4.1 Goal 1 — Replace arbitrary anisotropic coefficients with derived dynamical values

**Status:** Met for the new direct solver chain.

**Result:** The exact pullback chain is now active in:

- `analysis/direct_ordered_manifold.py`
- `analysis/phase_j/phase_j_dynamic_stability_solver.py`
- `analysis/phase_e/phase_e_external_phenomenology.py`
- `analysis/phase_k/phase_k_multi_fold_force_law.py`

The old exploratory `beta_a` coefficients are not used in that new chain.

**Why this proves the claim:** coefficient replacement is no longer only an intention or a note-level recommendation; it is an implemented runtime fact.

### 4.2 Goal 2 — Calculate self-coupling limits for branch stability

**Status:** Partially met.

**Result:** The branch scan records `16` regular branch candidates across the tested `(lambda_q, A0)` grid, with candidate ranges:

- `lambda_q in [0.005, 0.04]`
- `A0 in [0.01, 0.04]`

**Why this only partially proves the claim:** the result is empirical rather than analytical. It demonstrates branch regularity in the direct chain, but it is not yet a closed-form self-coupling bound.

### 4.3 Goal 3 — Map the derived constants to physical observables

**Status:** Partially met.

**Result:** The direct refresh now extracts regenerated profile observables such as final mass and compactness and uses the same coefficient chain downstream in Phases J, E, and K.

**Why this only partially proves the claim:** no fine-structure analog, mass-gap law, or other sharp observable constant has yet been derived from first principles.

### 4.4 Common slice protocol

**Status:** Met.

The Phase I package now contains all required bulk, 1D, and 2D studies on the full active domain.

## 5. Direct findings

The most important direct numbers are:

- maximum regular sampled anisotropy ratio: `101320.51697625456`
- `lambda_phi` constant at fixed `omega = 0.5`
- direct representative profile success count: `3/3`
- direct profile mass spread across scalar / rich / off-sheet seeds: `0.0`
- direct profile compactness-90 spread across scalar / rich / off-sheet seeds: `0.0`

So the direct runtime preserves the anisotropy mechanism geometrically, but that anisotropy does not show up as species-level mass or compactness splitting on the representative seed set.

## 6. Interpretation

Phase I now answers two different questions cleanly:

1. **Can the exploratory `beta_a` path be replaced?**  
   Yes. The direct runtime replacement is implemented.

2. **Does that replacement recover distinct species?**  
   No. The rebuilt direct chain yields degenerate representative profiles.

That changes the project-level problem materially. The old blocker was “there is no direct coefficient replacement.” The new blocker is “the direct coefficient replacement appears to universalize the object family.”

## 7. Supporting outputs

Key files:

- `solutions/phase_i/phase_i_geometric_anisotropy_scan/summary.json`
- `solutions/phase_i/phase_i_geometric_anisotropy_scan/summary.md`
- `solutions/phase_i/phase_i_geometric_anisotropy_scan/coefficient_map.csv`
- `solutions/phase_i/phase_i_geometric_anisotropy_scan/direct_profile_runs.csv`
- `solutions/phase_i/phase_i_geometric_anisotropy_scan/branch_stability_scan.csv`
- `solutions/phase_i/phase_i_geometric_anisotropy_scan/direct_runtime_coefficients.json`

## Bottom line

**Bottom line:** Phase I now closes at a stronger level than the audit-only version. The exact pullback anisotropy is no longer only a geometry observation; it is the active coefficient source for the rebuilt direct runtime. But the resulting direct profiles are degenerate across the representative seed family, so Phase I now supports universal objecthood rather than distinct particle-like species. Analytical self-coupling limits and sharp observable constants remain open.
