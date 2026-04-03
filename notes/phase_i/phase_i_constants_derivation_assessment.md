# Phase I Assessment — Direct Pullback Runtime Refresh

**Date:** 2026-04-02  
**Phase:** I — First-Principles Derivation of Constants  
**Status:** Complete after direct runtime refresh

## Direct Implementation Update

The old audit-only Phase I result has now been superseded by a direct implementation result:

- `analysis/direct_ordered_manifold.py` now carries the exact pullback metric, inverse metric, and Christoffel symbols.
- `analysis/phase_i/phase_i_geometric_anisotropy_scan.py` now writes both the geometry scans and a direct ordered-variable radial runtime bridge.
- `solutions/phase_i/phase_i_geometric_anisotropy_scan/direct_profile_runs.csv` shows that the representative scalar, rich, and off-sheet seeds are all regular under the new direct chain.
- `solutions/phase_i/phase_i_geometric_anisotropy_scan/direct_runtime_coefficients.json` records that downstream Phases J, E, and K now use this exact pullback chain instead of exploratory `beta_a`.
- `solutions/phase_i/phase_i_geometric_anisotropy_scan/summary.json` also shows that the direct profile mass and compactness spreads are exactly `0.0` on the representative seed set.

So Phase I no longer fails at “coefficient replacement.” It now fails at a different and more decisive place: the direct coefficient chain preserves universal objecthood but does not generate distinct species observables.

Where the older audit-only material below conflicts with this direct implementation update, the direct implementation update and the linked direct outputs take precedence.

## Purpose

This note records what the refreshed Phase I package actually proves after tracing:

- `khantraction_paper.md`
- `notes/real_physics_transition_plan.md`
- `summary/2026-03-29_phase_h_closure_summary.md`
- `notes/phase_h/phase_h_verified_quantum_assessment.md`
- `derivations/derivation_71_exponential_quaternion_parameter_mapping_clean.md`
- `derivations/derivation_75_ordered_pullback_and_exploratory_directional_phase_b_runtime.md`
- `derivations/derivation_90_geometric_origin_of_anisotropy.md`
- `analysis/phase_i/phase_i_geometric_anisotropy_scan.py`
- `solutions/phase_i/phase_i_geometric_anisotropy_scan/summary.json`
- `solutions/phase_i/phase_i_geometric_anisotropy_scan/summary.md`
- `solutions/phase_i/phase_i_geometric_anisotropy_scan/bulk_summary.json`
- `solutions/phase_i/phase_i_geometric_anisotropy_scan/named_phi_reference.csv`
- `solutions/phase_i/phase_i_geometric_anisotropy_scan/sheet_families.json`

---

## 1. What the active Phase I runtime actually is

The refreshed Phase I package is a **geometry-level pullback scan**. It computes the angular pullback metric of the ordered quaternion map and scans its eigenvalues on the active domain.

It does **not**:

- evolve the active Phase C to H solver with dynamically replaced `beta_a`,
- derive a spontaneous-symmetry-breaking potential,
- or compute observables from a full dynamical runtime.

The regenerated `summary.json` states this scope explicitly:

- `type = geometry_level_pullback_scan`
- "does not yet replace the exploratory beta coefficients in the active dynamical solver chain."

So every Phase I claim must be read as a result about the ordered-map pullback geometry, not as proof that the whole solver stack has already been upgraded.

---

## 2. Main audit corrections

### 2.1 The old derivation overstated the result

The earlier derivation and summary treated the pullback scan as if it had already eliminated the phenomenological constants from the active runtime.

That is not what the code does. The scan identifies a native geometric anisotropy mechanism, but it does not implement those state-dependent weights into the active dynamics.

### 2.2 The old soft-sheet description was incomplete

The earlier material effectively described only the `lambda_- = 0` family.

The refreshed derivation and outputs now distinguish the two alternating singular-sheet families:

- `lambda_+ = 0` on `phi = -pi/4 + n*pi`
- `lambda_- = 0` on `phi = pi/4 + n*pi`

Within `[-2pi, 2pi]`, each family appears four times.

### 2.3 The old physical-analog language was too strong

The earlier note treated:

- `alpha_K = xi`,
- and `Delta M_g = 2|sin(2phi)|`

as if they had already been mapped to observables.

The scan does not do that. Those are at best heuristic proposed analogs, not derived physical measurements.

---

## 3. Main findings

### 3.1 The ordered-map pullback metric carries a native phi-controlled anisotropy

At fixed `omega = 0.5`, the pullback eigenvalues are:

- `lambda_phi = e^(2omega) = 2.718281828459045`
- `lambda_plus = e^(2omega) * (1 + sin(2phi))`
- `lambda_minus = e^(2omega) * (1 - sin(2phi))`

The scan confirms:

- `theta` slice `lambda_minus` width: `0.0`
- `phi` slice `lambda_minus` width: `5.43656365691809`
- `rho` slice `lambda_minus` width: `0.0`

So phi alone controls the stiffness split of the paired `theta-rho` subsystem.

### 3.2 The paired subsystem has alternating exact soft-sheet families

The refreshed `sheet_families.json` gives:

- `lambda_plus_zero_sheets`:
  - `-5pi/4`
  - `-pi/4`
  - `3pi/4`
  - `7pi/4`
- `lambda_minus_zero_sheets`:
  - `-7pi/4`
  - `-3pi/4`
  - `pi/4`
  - `5pi/4`

At these sheets, one paired mode softens to zero while the other reaches the maximum active-scale stiffness `2e^(2omega) = 5.43656365691809`.

### 3.3 Strong near-sheet anisotropy is real

The dense phi scan records a maximum regular sampled anisotropy ratio of:

- `101320.51697625456`

The exact sheet rows in `named_phi_reference.csv` show the formal limit directly:

- `anisotropy_ratio = inf`

because one paired eigenvalue vanishes exactly there.

### 3.4 The old observable-mapping goal is still open

The scan does provide two useful geometric diagnostics:

- unit-scale gap at `phi = pi/8`: `1.414213562373095`
- active-scale gap at `phi = pi/8`, `omega = 0.5`: `3.844231028159116`

But these are still geometric stiffness gaps. They are not yet mapped to measured observables such as a physical mass gap or a fine-structure analog extracted from dynamics.

---

## 4. Goal status against `notes/real_physics_transition_plan.md`

### Goal 1 — Replace arbitrary `beta_a` with dynamical values derived from an underlying principle

**Status:** Partially met.

What is met:

- the ordered pullback metric provides a native phi-controlled anisotropy mechanism,
- the scan proves that the paired angular stiffnesses are state dependent.

What is not met:

- the active solver chain still uses exploratory `beta_a` coefficients,
- no regenerated runtime yet replaces them with the pullback-derived values.

### Goal 2 — Calculate exact self-coupling limits required for stability without hand-tuned proxies

**Status:** Partially met at the geometry level only.

What is met:

- exact soft-sheet families where one paired mode loses stiffness are identified.

What is not met:

- no full self-coupling limits for branch stability have been derived in the actual dynamics,
- no stability solver demonstrates these limits without exploratory proxies.

### Goal 3 — Map the derived constants to physical observables

**Status:** Not met.

What exists:

- heuristic proposals for a unit-scale gap and an `alpha_K`-style ratio.

What is missing:

- an observable extraction pipeline,
- a demonstrated mass-gap calculation from dynamics,
- and a defensible fine-structure-like analog derived from measured response.

---

## 5. Bottom line

**Bottom line:** Phase I now supports a narrower but solid claim. The ordered quaternion pullback metric carries a native phi-controlled anisotropy, and the paired theta-rho subsystem has exact alternating soft-sheet families where one mode loses stiffness. But Phase I has not yet completed the stronger transition-plan task of replacing the exploratory `beta_a` coefficients in the active solver or mapping those geometric quantities to physical observables.
