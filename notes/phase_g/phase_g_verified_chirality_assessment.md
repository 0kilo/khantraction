# Phase G Assessment — Handedness Audit Refresh

**Date:** 2026-04-02
**Phase:** G — Classical rotational / handedness properties
**Status:** Complete after audit refresh

## Purpose

This note records what the refreshed Phase G analysis actually proves after tracing the paper framing, the exploration plan, the inherited Phase C to Phase F runtime chain, the chirality and rotational derivations, the active Phase G solver, and the regenerated solution package.

Relevant files:
- `derivations/derivation_76_full_einstein_equations_nonminimal_coupling.md`
- `derivations/derivation_78_maurer_cartan_tensor.md`
- `derivations/derivation_79_einstein_trace_with_mc_breaking.md`
- `derivations/derivation_82_classical_chirality_operators.md`
- `derivations/derivation_83_rotational_energy_momentum.md`
- `analysis/phase_g/phase_g_chirality_analysis.py`
- `solutions/phase_g/phase_g_chirality/summary.json`
- `solutions/phase_g/phase_g_chirality/summary.md`
- `solutions/phase_g/phase_g_chirality/operator_checks.csv`
- `solutions/phase_g/phase_g_chirality/a_chiral_reference.csv`
- `solutions/phase_g/phase_g_chirality/representative_runs.csv`
- `solutions/phase_g/phase_g_chirality/pair_comparisons.csv`
- `solutions/phase_g/phase_g_chirality/mirror_pair_results.csv`
- `solutions/phase_g/phase_g_chirality/right_handed_base_profile.csv`
- `solutions/phase_g/phase_g_chirality/parity_partner_profile.csv`
- `solutions/phase_g/phase_g_chirality/left_handed_flip_profile.csv`
- `solutions/phase_g/phase_g_chirality/right_handed_sheet_profile.csv`
- `solutions/phase_g/phase_g_chirality/left_handed_sheet_profile.csv`
- `solutions/phase_g/phase_g_chirality/slice_1d_theta_chi.csv`
- `solutions/phase_g/phase_g_chirality/slice_1d_phi_chi.csv`
- `solutions/phase_g/phase_g_chirality/slice_1d_rho_chi.csv`
- `solutions/phase_g/phase_g_chirality/slice_2d_theta_rho_chi.csv`
- `solutions/phase_g/phase_g_chirality/slice_2d_phi_theta_chi.csv`
- `solutions/phase_g/phase_g_chirality/slice_2d_phi_rho_chi.csv`
- `solutions/phase_g/phase_g_chirality/rotational_stability.csv`

---

## 1. What the active runtime actually is

Phase G does not stand on a separate background. It reuses the same exploratory symmetry-broken Maurer-Cartan runtime audited in Phases C to F:

- `derivation_76` supplies the exact nonminimal Einstein trace closure,
- `derivation_78` introduces the anisotropic Maurer-Cartan kinetic term,
- `derivation_79` folds that anisotropy into the Ricci-trace source,
- `derivation_82` defines the chirality operators,
- `derivation_83` adds a rotational ansatz but not a solved rotational dynamics model.

The regenerated `summary.json` records:

- anisotropic Maurer-Cartan weights `beta = [0.01, 0.02, 0.03]`,
- metric regularization `1e-4`,
- phi-localized angular potential coefficient `0.01`,
- horizon event threshold `2m/r = 0.48`,
- field seed amplitude `A0 = 0.005`,
- derivative seed `xp0 = [0.0, 0.01, 0.01, 0.0]`,
- audited outer box `r_max = 20`.

So every Phase G claim must be interpreted inside that same exploratory runtime, not as a closure-independent statement about the underlying theory.

---

## 2. What was tested

The refreshed Phase G package checks four separate layers:

1. **Exact operator checks**
   - parity preservation of `chi`,
   - chiral-flip reversal of `chi`.
2. **Representative solver-backed runs**
   - right-handed base,
   - parity partner,
   - left-handed chiral-flip partner,
   - right-handed and left-handed sheetlike partners.
3. **Full 1D / 2D slice protocol**
   - all 1D and 2D angle combinations,
   - all on the active `[-2pi, 2pi]` domain.
4. **Rotational file audit**
   - traced whether the old rotational scan was solver-backed or only proxy-backed.

The refreshed package also records:

- solver status,
- termination flags,
- event radii,
- final integration radius,
- final mass,
- chirality density,
- pairwise mass differences.

That was missing from the old Phase G evidence trail and is why the old rotational language had to be narrowed.

---

## 3. Main findings

### 3.1 Chirality is phi-controlled and operator-exact

The operator checks confirm:

- parity preserves chirality on all audit samples,
- the topological chiral flip reverses chirality on all audit samples.

The a-chiral reference table also places the zero-chirality sheets at

- `phi = -3pi/4`
- `phi = -pi/4`
- `phi = pi/4`
- `phi = 3pi/4`

which is exactly the structure predicted by `chi = cos(2phi)`.

### 3.2 Mirror-pair objecthood is solver-backed

The refreshed mirror-pair comparisons show near-degenerate masses with opposite chirality signs:

- base mirror pair mass abs diff: `1.0765515557897842e-06`
- sheet mirror pair mass abs diff: `1.1114040713300355e-06`

The parity pair preserves the chirality sign instead:

- parity pair mass abs diff: `8.221556238474648e-06`
- chirality sign preserved

So the numerical runtime supports a real enantiomer picture at the mapping/object level.

### 3.3 Theta and rho are spectators for chirality sign

The slice ranges show:

- theta and rho slices keep `chi` fixed at about `0.7071067811865476`,
- only phi-involving slices traverse positive and negative chirality sectors.

So handedness is a phi-separator effect, not a balanced three-angle effect.

### 3.4 The old rotational claim was not solver-backed

The old rotational file came from a proxy rescaling of one baseline mass rather than a modified solver.

So `derivation_83` remains useful as an ansatz, but the numerical claim that Khantraction already behaves as a stable spin-like host for angular momentum was too strong.

---

## 4. Correct interpretation

The refreshed Phase G result is mixed:

- stronger than before, because the handedness story is now explicitly backed by operator checks, mirror-pair runs, and full-domain slices,
- narrower than before, because the rotational add-on was not solver-backed.

The phase therefore supports the following audited statement:

> In the current exploratory runtime, Khantraction has a genuine classical handedness architecture controlled by `phi`. But the present package does not yet establish solved rotational stability or hosted angular momentum dynamics.

---

## 5. Bottom line

**Bottom line:** Phase G now supports a classical handedness claim. Parity preserves chirality, the topological chiral flip reverses it, phi partitions the angular domain into right-handed and left-handed sectors, and mirror pairs remain nearly mass-degenerate on solved runs. But the rotational part remains analytical and provisional rather than solver-backed.
