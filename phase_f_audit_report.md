# Phase F Audit Report

**Date:** 2026-04-02
**Scope:** Re-audit `summary/2026-03-29_phase_f_closure_summary.md` against `khantraction_paper.md`, `notes/classical_exploration_plan.md`, the inherited derivation chain, inherited Phase C to Phase E evidence, the active Phase F analysis code, and the full Phase F solution package.

## Files reviewed

Primary framing:
- `khantraction_paper.md`
- `notes/classical_exploration_plan.md`

Inherited derivation chain:
- `derivations/derivation_76_full_einstein_equations_nonminimal_coupling.md`
- `derivations/derivation_78_maurer_cartan_tensor.md`
- `derivations/derivation_79_einstein_trace_with_mc_breaking.md`
- `derivations/derivation_80_external_field_coupling.md`

Inherited prerequisite evidence:
- `summary/2026-03-29_phase_e_closure_summary.md`
- `notes/phase_e/phase_e_verified_phenomenology_assessment.md`
- `notes/phase_e/phase_e_synthesis_2026-04-02.md`

Phase F analysis code:
- `analysis/phase_f/phase_f_hosting_analysis.py`
- `scripts/run_phase_f_hosting_analysis.sh`

Phase F notes and summaries:
- `notes/phase_f/phase_f_verified_hosting_assessment.md`
- `summary/2026-03-29_phase_f_closure_summary.md`

Phase F solution package:
- `solutions/phase_f/phase_f_hosting/summary.json`
- `solutions/phase_f/phase_f_hosting/summary.md`
- `solutions/phase_f/phase_f_hosting/representative_runs.csv`
- `solutions/phase_f/phase_f_hosting/coupling_comparison.csv`
- `solutions/phase_f/phase_f_hosting/signed_loading_ladder.csv`
- `solutions/phase_f/phase_f_hosting/signed_loading_test.csv`
- `solutions/phase_f/phase_f_hosting/scalar_profile.csv`
- `solutions/phase_f/phase_f_hosting/theta_seed_profile.csv`
- `solutions/phase_f/phase_f_hosting/rho_seed_profile.csv`
- `solutions/phase_f/phase_f_hosting/phi_sheet_profile.csv`
- `solutions/phase_f/phase_f_hosting/phi_offsheet_profile.csv`
- `solutions/phase_f/phase_f_hosting/mixed_offsheet_profile.csv`
- `solutions/phase_f/phase_f_hosting/slice_1d_theta.csv`
- `solutions/phase_f/phase_f_hosting/slice_1d_phi.csv`
- `solutions/phase_f/phase_f_hosting/slice_1d_rho.csv`
- `solutions/phase_f/phase_f_hosting/slice_2d_theta_rho.csv`
- `solutions/phase_f/phase_f_hosting/slice_2d_phi_theta.csv`
- `solutions/phase_f/phase_f_hosting/slice_2d_phi_rho.csv`
- `solutions/phase_f/phase_f_hosting/angular_hosting_map.csv`

## Corrections made

1. Rewrote the Phase F analysis script so it now:
   - uses the active runtime instead of the old frozen-background seed,
   - records status, termination flags, event radii, final radius, probe-response ratios, and localization ratios,
   - compares gamma-on versus gamma-off runs,
   - runs a signed loading ladder across representative anchors,
   - reruns the full 1D / 2D slice protocol on the full `[-2pi, 2pi]` domain,
   - writes profile CSVs and a machine-readable `summary.json`.

2. Replaced the old “verified hosting” interpretation. The refreshed evidence shows:
   - unloaded localization ratios remain below `1`,
   - so the current package does not prove strong trapping.

3. Replaced the old trap-validation claim. The refreshed evidence supports:
   - angular response sensitivity,
   - but not physical validation of the Phase E external proxy as a robust trap.

4. Added the missing top-level solution summary for `solutions/phase_f/`.

## Validation

Python was run inside the virtual environment as requested.

Executed:
- `source venv/bin/activate && python -m py_compile analysis/phase_f/phase_f_hosting_analysis.py`
- `source venv/bin/activate && python analysis/phase_f/phase_f_hosting_analysis.py`

Verified:
- every directory under `solutions/phase_f/` contains a `summary.md`,
- regenerated Phase F outputs now include representative profiles, localization metrics, gamma comparisons, signed loading diagnostics, and full-domain slices,
- the closure summary now matches the actual data rather than the older overclaims.

## Audit judgment

Phase F is supportable as closed only with the following audited meaning:

- it establishes sign-sensitive probe response on structured backgrounds,
- it does not establish robust classical hosting in a strong trapping sense.

The defensible Phase F result is:

- the probe-coupling ansatz exists,
- the explicit hosting term is subleading in the current implementation,
- signed loading asymmetry is real,
- the response map is phi-dominated,
- and strong classical hosting remains open.
