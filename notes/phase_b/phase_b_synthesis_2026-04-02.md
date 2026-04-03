# Phase B Synthesis — Audit Refresh

**Date:** 2026-04-02  
**Phase:** B — Structured-object picture  
**Status:** Closed after audit refresh

## Purpose

This note synthesizes the refreshed Phase B evidence chain after re-reading:
- `khantraction_paper.md`
- `notes/classical_exploration_plan.md`
- Phase B derivations 73 through 76
- all Phase B analysis scripts
- all Phase B notes
- all Phase B solution directories and nested summaries

---

## 1. Paper-level motivation

`khantraction_paper.md` frames Khantraction as a speculative toy model for compact, structured spacetime-fold objects, not as a finished particle theory.

That framing matters for Phase B:

> the phase is supposed to establish objecthood and structured-family behavior, not a completed particle interpretation.

Any closure summary that overstates Phase B as if it had already produced robust particle-like species would therefore be out of bounds.

---

## 2. Audited answer to the Phase B key question

The plan asks:

> Does Khantraction produce coherent compact structured objects with stable classical identity?

The audited answer is:

- **coherent compact structured objects:** yes, in the broad family/objecthood sense,
- **stable classical identity in the linear angular channels:** no,
- **closure-independent object sizes:** no.

That is the Phase B result in one line.

---

## 3. Strongest supported claims

### 3.1 Broad family coherence is real

Supported by:
- `analysis/phase_b/phase_b_full_radial_solver.py`
- `analysis/phase_b/phase_b_closure_stress_test.py`
- `solutions/phase_b/phase_b_full_radial_solver/run_summary.json`
- `solutions/phase_b/phase_b_closure_stress_test/cross_scenario_summary.json`

Key facts:
- 117 / 117 provisional full-solver runs succeeded,
- 39 / 39 runs succeeded in every stress-test scenario,
- continuation mass ordering stayed monotone in all 12 tested stress scenarios.

### 3.2 Structured-object observables exist but their sizes are setup-dependent

Supported by:
- `solutions/phase_b/phase_b_full_radial_solver/run_results.csv`
- `solutions/phase_b/phase_b_closure_stress_test/cross_scenario_summary.json`

Key facts:
- the solver extracts the planned objecthood observables,
- the rich anchor has a clear core/bulk profile,
- but amplitude and outer-box choices change those sizes much more than the tested closure toggles do.

### 3.3 Exact linear-basis dynamics are angularly degenerate

Supported by:
- `analysis/phase_b/phase_b_exact_radial_solver.py`
- `solutions/phase_b/phase_b_exact_radial_solver/run_summary.json`
- `solutions/phase_b/phase_b_exact_radial_solver/slice_1d_phi.csv`
- `solutions/phase_b/phase_b_exact_radial_solver/slice_2d_theta_rho.csv`

Key facts:
- exact anchor and slice observables match to floating-point precision at fixed `omega`,
- so the exact linear-basis runtime depends only on the norm-symmetric sector.

### 3.4 Exploratory ordered-runtime differentiation is real but limited

Supported by:
- `analysis/phase_b/phase_b_improved_dynamics_solver.py`
- `solutions/phase_b/phase_b_improved_dynamics/comparison_summary.json`
- `solutions/phase_b/phase_b_improved_dynamics/exploratory_directional/slice_1d_phi.csv`
- `solutions/phase_b/phase_b_improved_dynamics/exploratory_directional/slice_2d_theta_rho.csv`

Key facts:
- pure pullback rewriting remains degenerate,
- the exploratory directional mode splits the rich neighborhood and the 1D $\phi$ slice,
- but the audited 2D $(\theta,\rho)$ slice at fixed `phi = -pi/2` remains degenerate.

So the exploratory signal is not a generic angular-identity result. It is narrower and strongly $\phi$-localized.

---

## 4. Audit corrections applied

The audit refresh corrected four concrete problems:

1. Phase B scripts with incorrect output roots were fixed so they now regenerate into `solutions/phase_b/...`.
2. The Phase B package now includes explicit 1D and 2D slice outputs rather than only bulk scans.
3. Missing nested `summary.md` files were added for the profile and sub-runtime solution directories.
4. Stale notes and the closure summary are being rewritten to match the evidence actually present in the regenerated outputs.

---

## 5. Bottom line

**Bottom line:** Phase B closes as a disciplined objecthood phase. It supports a broad regular family of compact structured-object profiles, but not closure-independent object sizes and not stable angular identity in the linear basis. That narrower conclusion is fully supported by the refreshed derivations, notes, scripts, and regenerated solution outputs.
