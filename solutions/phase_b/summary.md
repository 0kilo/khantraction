# Phase B Solution Index

This directory is the refreshed audited Phase B solution package.

## Subdirectories

- `phase_b_radial_equation_structure/`
  - Structural report for the reconstructed four-component matter equations and the active Phase B slice anchors.
- `phase_b_full_radial_solver/`
  - Provisional full solver outputs for the 117-seed branch-family/objecthood scan, including representative profiles and explicit 1D/2D slice exports.
- `phase_b_closure_stress_test/`
  - Twelve-scenario closure/setup sensitivity study on the focused 39-seed comparison set, plus representative slice comparisons across selected scenarios.
- `phase_b_improved_dynamics/`
  - Ordered-runtime comparison package. `baseline_pullback/` tests pure pullback geometry; `exploratory_directional/` adds explicitly labeled directional terms.
- `phase_b_exact_radial_solver/`
  - Exact-trace anchor and slice check for the linear component basis, including anchor profile exports.

## Interpretation

Use this directory as the entry point for the audited Phase B claims:
- broad objecthood and family coherence come primarily from `phase_b_full_radial_solver/` and `phase_b_closure_stress_test/`,
- exploratory ordered-variable differentiation comes from `phase_b_improved_dynamics/`,
- exact linear-basis angular degeneracy comes from `phase_b_exact_radial_solver/`.
