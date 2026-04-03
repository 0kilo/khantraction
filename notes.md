# Notes: Khantraction Direct-Data Implementation

## Source Map

### Primary framing
- `khantraction_paper.md`
- `notes/2026-04-02_direct_data_closure_plan.md`
- `notes/real_physics_transition_plan.md`

### Critical derivations
- `derivations/derivation_75_ordered_pullback_and_exploratory_directional_phase_b_runtime.md`
- `derivations/derivation_90_geometric_origin_of_anisotropy.md`
- `derivations/derivation_91_3d_ordered_wave_operator.md`
- `derivations/derivation_92_multi_fold_interaction_energy.md`

### Active implementation targets
- `analysis/phase_i/phase_i_geometric_anisotropy_scan.py`
- `analysis/phase_j/phase_j_dynamic_stability_solver.py`
- `analysis/phase_e/phase_e_external_phenomenology.py`
- `analysis/phase_k/phase_k_multi_fold_force_law.py`
- `analysis/phase_b/phase_b_improved_dynamics_solver.py`

### Affected phase documents
- `summary/2026-03-31_phase_i_closure_summary.md`
- `summary/2026-03-31_phase_j_closure_summary.md`
- `summary/2026-03-29_phase_e_closure_summary.md`
- `summary/2026-03-31_phase_k_closure_summary.md`

## Findings

### Reusable direct machinery already present
- `analysis/phase_b/phase_b_improved_dynamics_solver.py` already contains:
  - exact pullback metric `G(w, phi)`,
  - inverse metric,
  - metric derivatives,
  - Christoffel symbols,
  - a direct ordered-variable radial solver.
- That code is the best starting point for replacing the exploratory `beta_a` path.

### Implemented direct chain
- `analysis/direct_ordered_manifold.py` now provides the exact pullback metric, inverse metric, Christoffels, direct radial solver, 3D wave solver, and direct interaction-energy bookkeeping.
- Phase I now uses that module as the coefficient bridge and no longer stops at geometry-only scans.
- Phase J now uses direct ordered-manifold 3D evolution instead of the anchored proxy.
- Phase E now uses direct pullback profiles and a direct impulse-response ladder.
- Phase K now uses direct 3D same-background interaction-energy calculations instead of the old one-dimensional overlap proxy.

### Resulting empirical pattern
- The direct chain supports stable localized objecthood.
- The direct chain supports a clean family-level motion-response law.
- The direct chain supports direct same-background interaction energy and force gradients.
- The direct chain is degenerate across scalar, rich, and off-sheet representative seeds in:
  - mass,
  - compactness,
  - transport response,
  - external tails,
  - same-background interaction data.

### Final synthesis
- The implementation gap is no longer the reason Khantraction fails as a particle-level model.
- The direct implementation itself now provides the decisive negative result: the exact pullback chain universalizes the audited seed family instead of preserving particle-like species structure.
