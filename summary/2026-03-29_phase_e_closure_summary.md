# Phase E Closure Summary — Direct External Phenomenology

**Date:** 2026-03-29  
**Phase:** E — External particle-likeness  
**Status:** Closed after direct runtime refresh

## 0. Project-level disposition

Phase E is no longer blocked by the absence of a direct motion-response measurement. The phase has been rebuilt on direct pullback-runtime profiles and direct 3D impulse-response data. The remaining issue is that the rebuilt direct chain makes scalar, rich, and off-sheet seeds externally and dynamically indistinguishable. The project-level synthesis is recorded in:

- `notes/2026-04-02_direct_data_closure_plan.md`
- `summary/2026-04-02_gap_closure_summary.md`
- `summary/2026-04-02_khantraction_model_conclusion.md`

## 1. Scope and motivation

Phase E asks whether a structured Khantraction object can look particle-like from the outside without becoming point-like internally.

After the direct implementation pass, that question has three parts:

1. do the rebuilt direct profiles have simple outer tails,
2. do different internal seeds remain externally distinguishable,
3. does a direct motion-response law emerge on solved backgrounds.

## 2. Support chain

This closure summary is supported by:

- `khantraction_paper.md`
- `notes/classical_exploration_plan.md`
- `analysis/direct_ordered_manifold.py`
- `analysis/phase_e/phase_e_external_phenomenology.py`
- `notes/phase_e/phase_e_verified_phenomenology_assessment.md`
- `solutions/phase_e/phase_e_phenomenology/summary.json`
- `solutions/phase_e/phase_e_phenomenology/tail_run_results.csv`
- `solutions/phase_e/phase_e_phenomenology/rn_fit_results.csv`
- `solutions/phase_e/phase_e_phenomenology/indistinguishability_pairs.csv`
- `solutions/phase_e/phase_e_phenomenology/indistinguishability_map.json`
- `solutions/phase_e/phase_e_phenomenology/direct_response_ladder.csv`
- `solutions/phase_e/phase_e_phenomenology/slice_1d_theta.csv`
- `solutions/phase_e/phase_e_phenomenology/slice_1d_phi.csv`
- `solutions/phase_e/phase_e_phenomenology/slice_1d_rho.csv`

## 3. Method

### 3.1 Direct radial profiles and tail fits

The refresh solves direct pullback-runtime radial profiles for:

- `scalar`
- `rich`
- `phi_offsheet`

and then fits the tail mass function to an RN-like form.

This is the right method for Goals 1 and 2 because it tests the actual external profile of the direct chain rather than the old exploratory beta-driven runtime.

### 3.2 Direct impulse-response ladder

The refresh then applies direct 3D impulses with strengths:

- `0.02`
- `0.04`
- `0.08`

to the solved profiles and measures:

- centroid shift,
- compactness shift,
- energy drift,
- response ratio.

This is the right method for Goal 4 because it replaces the old tiny-gradient radial probe with actual direct 3D response data on solved objects.

### 3.3 Full slice protocol

The phase also rebuilds all 1D and 2D slices on the direct chain to test whether external mass or compactness depend on `theta`, `phi`, or `rho`.

## 4. Results against the classical plan

### 4.1 Goal 1 — Determine how the object looks from the outside

**Status:** Met.

**Result:** All three representative direct profiles have smooth outer tails and successful RN-like fits.

### 4.2 Goal 2 — Compare whether internally different objects become externally similar

**Status:** Met, but only as a universal class.

**Result:** `scalar`, `rich`, and `phi_offsheet` all fall into the same external indistinguishability class.

### 4.3 Goal 3 — Define external particle-likeness without requiring pointlikeness

**Status:** Met for a universal family, not for distinct species.

**Result:** The direct chain supports smooth compact external behavior, but not seed-specific external identities.

### 4.4 Goal 4 — Assess dynamical response to external forcing

**Status:** Met for the tested family.

**Result:** The response ratios remain nearly constant across the impulse ladder.

### 4.5 Common slice protocol

**Status:** Met.

The full 1D and 2D slice set is present on the rebuilt direct chain.

## 5. Direct findings

The decisive numbers are:

- final mass for `scalar`, `rich`, and `phi_offsheet`: `0.032534129324309234`
- compactness-90 for all three: `11.530999999999798`
- RN-fit `M_ADM_fit` for all three: `0.08396759860443653`
- RN-fit `Q_eff_fit` for all three: `1.1267522196207713`
- response-ratio range for all three: `[1.1197031965320845, 1.119987028419656]`

The direct 1D and 2D slices are also completely flat in both mass and compactness across `theta`, `phi`, and `rho`.

## 6. Interpretation

Phase E now gives a much cleaner answer than the audit-only version:

- the direct chain does support external particle-like behavior,
- it also supports a clean family-level linear motion-response law,
- but all audited seeds collapse into one universal external family.

So the direct refresh closes the old “missing response law” gap, but it closes it in a way that weakens the particle-species interpretation rather than strengthening it.

## 7. Supporting outputs

Key files:

- `solutions/phase_e/phase_e_phenomenology/summary.json`
- `solutions/phase_e/phase_e_phenomenology/summary.md`
- `solutions/phase_e/phase_e_phenomenology/tail_run_results.csv`
- `solutions/phase_e/phase_e_phenomenology/rn_fit_results.csv`
- `solutions/phase_e/phase_e_phenomenology/indistinguishability_pairs.csv`
- `solutions/phase_e/phase_e_phenomenology/direct_response_ladder.csv`

## Bottom line

**Bottom line:** Phase E now has a direct pullback-runtime rebuild. It supports smooth external tails, a clean family-level linear impulse-response law, and complete external indistinguishability across scalar, rich, and off-sheet seeds. That closes the old “no direct response law” gap, but in a way that weakens the particle-zoo claim: the direct runtime produces universal external behavior rather than distinct particle-like species.
