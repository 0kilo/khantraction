# Phase G Closure Summary — Classical Handedness Audit

**Date:** 2026-03-29  
**Phase:** G — Classical rotational / handedness properties  
**Status:** Closed after audit refresh

## 0. Project-level disposition

Phase G remains a valid static handedness result, but the direct runtime refresh now clarifies its scope further: chirality survives as a kinematic sign structure, while the rebuilt direct Phases J, E, and K do not show species-level dynamical or interaction splitting from that handedness. So Phase G supports geometric handedness language, not particle-species physics. The governing synthesis is recorded in `summary/2026-04-02_gap_closure_summary.md`, `notes/2026-04-02_direct_data_closure_plan.md`, and `summary/2026-04-02_khantraction_model_conclusion.md`.

## 1. Scope and motivation

`khantraction_paper.md` presents Khantraction as a toy model of structured spacetime folds, not as a finished theory of spin, charge, or particle identity.

That means Phase G is not supposed to prove quantum spin or full rotational dynamics. Its narrower burden is:

- define the chirality operators on the ordered quaternion map,
- test whether opposite angular sectors are equivalent, mirrored, or genuinely distinct,
- determine whether handedness belongs to the object’s classical identity,
- and clarify how much of the “rotational” language is actually solver-backed.

This is the correct classical precursor to later spin-like work, as stated in `notes/classical_exploration_plan.md`.

The active Phase G solver inherits the same exploratory Maurer-Cartan runtime used in the refreshed Phase C to Phase F audits:

- the exact nonminimal Einstein trace closure from `derivations/derivation_76_full_einstein_equations_nonminimal_coupling.md`,
- the anisotropic Maurer-Cartan construction from `derivations/derivation_78_maurer_cartan_tensor.md`,
- the Ricci-trace update from `derivations/derivation_79_einstein_trace_with_mc_breaking.md`,
- the chirality operators from `derivations/derivation_82_classical_chirality_operators.md`.

`derivations/derivation_83_rotational_energy_momentum.md` supplies a rotational ansatz, but the old numerical “stability scan” was only a mass-rescaling proxy, not a solved rotational dynamics test.

The active Phase G convention remained:

- `omega > 0`
- `theta, phi, rho in [-2pi, 2pi]`
- no redundancy quotienting

That framing is consistent with:
- `khantraction_paper.md`
- `notes/classical_exploration_plan.md`
- `derivations/derivation_76_full_einstein_equations_nonminimal_coupling.md`
- `derivations/derivation_78_maurer_cartan_tensor.md`
- `derivations/derivation_79_einstein_trace_with_mc_breaking.md`
- `derivations/derivation_82_classical_chirality_operators.md`
- `derivations/derivation_83_rotational_energy_momentum.md`

---

## 2. Audit against `notes/classical_exploration_plan.md`

### 2.1 Goal 1 — Study whether angular sectors define classical chirality classes

**Status:** Met.

**How it was tested:** The refreshed package now records:

- direct operator checks for parity and chiral-flip actions,
- exact chirality-density values on representative points,
- a reference table for the a-chiral sheets,
- and full-domain 1D / 2D slice maps of `chi`.

**Why this proves the goal:** This tests chirality at the level the derivation actually defines it: as the determinant of the angular Maurer-Cartan frame.

### 2.2 Goal 2 — Compare whether opposite angular sectors are equivalent, mirrored, or distinct

**Status:** Met.

**How it was tested:** The refreshed package compares:

- a parity pair,
- a base mirror pair,
- and a sheetlike mirror pair,

using solver-backed mass profiles and chirality signs.

**Why this proves the goal:** This directly distinguishes “same chirality under parity” from “sign-reversed chirality under the topological chiral flip.”

### 2.3 Goal 3 — Identify whether handedness belongs to the object’s classical identity

**Status:** Met.

**How it was tested:** The refreshed package combines:

- exact operator checks,
- near-degenerate mirror-pair runs,
- and full-domain slice maps showing chirality sign changes only across `phi`.

**Why this proves the goal:** If handedness were just a coordinate artifact, parity would reverse it. It does not. Instead, only the `phi -> phi + pi/2` chiral flip reverses `chi`, while the object remains nearly the same macroscopically.

### 2.4 Common slice protocol

**Status:** Met after audit refresh.

The refreshed Phase G slice set now includes:

- 1D `theta`, `phi`, `rho` on `[-2pi, 2pi]`
- 2D `(theta, rho)`, `(phi, theta)`, `(phi, rho)` on `[-2pi, 2pi]^2`

with status-aware outputs written to the active solution package.

### 2.5 Phase G key question

The plan asks:

> Does the structured object have a classical handedness architecture?

After the audit, the answer is:

- **classical handedness architecture:** yes,
- **phi-controlled chirality classes:** yes,
- **true enantiomeric mirror pairs:** yes, at the mapping/object level,
- **solver-backed rotational stability architecture:** not yet established.

That is the actual Phase G result.

---

## 3. Final Phase G conclusions

### 3.1 Parity preserves chirality, while the topological chiral flip reverses it

**Claim:** Pure parity does not reverse the internal handedness of the Khantraction state; only the `phi -> phi + pi/2` topological chiral flip does.

**Method and rationale:** The refreshed package checks the exact chirality density

`chi = det(J_angular)`

on representative points under:

- parity: `(theta, phi, rho) -> (-theta, -phi, -rho)`
- chiral flip: `(theta, phi, rho) -> (theta, phi + pi/2, rho)`

**Results:** The operator checks give:

- parity preserves chirality on all audit samples: `True`
- topological chiral flip reverses chirality on all audit samples: `True`

For example, at the base sample:

- `chi = 0.7071067811865475`
- `parity_chi = 0.7071067811865475`
- `flip_chi = -0.7071067811865476`

**Why this proves the claim:** This is the exact operator-level distinction Phase G needed. Handedness is not a superficial coordinate label; it is preserved under parity and reversed only by crossing the `phi` separator through the chiral flip.

**Supporting documents:**

- `derivations/derivation_82_classical_chirality_operators.md`
- `analysis/phase_g/phase_g_chirality_analysis.py`
- `solutions/phase_g/phase_g_chirality/operator_checks.csv`
- `solutions/phase_g/phase_g_chirality/a_chiral_reference.csv`
- `solutions/phase_g/phase_g_chirality/summary.json`
- `solutions/phase_g/phase_g_chirality/summary.md`
- `notes/phase_g/phase_g_verified_chirality_assessment.md`

---

### 3.2 Handedness is controlled by `phi`; `theta` and `rho` are spectator coordinates for chirality sign

**Claim:** The chirality sign is controlled by `phi` alone in the audited runtime.

**Method and rationale:** The correct test is the full 1D / 2D slice protocol on the active domain, recording `chi` directly and checking whether any sign reversal occurs away from `phi`.

**Results:** The refreshed slice widths are:

- 1D `theta` chi range = `[0.7071067811865476, 0.7071067811865476]`
- 1D `phi` chi range = `[-0.9009688679024191, 1.0]`
- 1D `rho` chi range = `[0.7071067811865475, 0.7071067811865476]`
- 2D `(theta, rho)` chi range = `[0.7071067811865475, 0.7071067811865476]`
- 2D `(phi, theta)` chi range = `[-0.9009688679024189, 1.0]`
- 2D `(phi, rho)` chi range = `[-0.9009688679024189, 1.0]`

The a-chiral reference table gives:

- `phi = -3pi/4`
- `phi = -pi/4`
- `phi = pi/4`
- `phi = 3pi/4`

with `chi` numerically zero at those sheets up to floating-point roundoff.

**Why this proves the claim:** Theta and rho sweeps never change the chirality sign, while phi sweeps pass through the a-chiral boundaries and reverse the sign. That is exactly the phi-controlled handedness architecture the derivation predicts.

**Supporting documents:**

- `derivations/derivation_82_classical_chirality_operators.md`
- `analysis/phase_g/phase_g_chirality_analysis.py`
- `solutions/phase_g/phase_g_chirality/a_chiral_reference.csv`
- `solutions/phase_g/phase_g_chirality/slice_1d_theta_chi.csv`
- `solutions/phase_g/phase_g_chirality/slice_1d_phi_chi.csv`
- `solutions/phase_g/phase_g_chirality/slice_1d_rho_chi.csv`
- `solutions/phase_g/phase_g_chirality/slice_2d_theta_rho_chi.csv`
- `solutions/phase_g/phase_g_chirality/slice_2d_phi_theta_chi.csv`
- `solutions/phase_g/phase_g_chirality/slice_2d_phi_rho_chi.csv`
- `solutions/phase_g/phase_g_chirality/summary.md`
- `notes/phase_g/phase_g_verified_chirality_assessment.md`

---

### 3.3 Mirror pairs remain nearly mass-degenerate while the chirality sign reverses

**Claim:** Right-handed and left-handed mirror pairs exist as nearly mass-degenerate structured objects with opposite chirality signs.

**Method and rationale:** The refreshed package compares solver-backed mirror pairs on the active runtime instead of relying only on the analytic chirality formula.

**Results:** The representative audited pairs are:

- base mirror pair:
  - `right_handed_base` mass = `0.6961232297626876`
  - `left_handed_flip` mass = `0.6961221532111318`
  - mass absolute difference = `1.0765515557897842e-06`
  - chirality signs = `+0.7071067811865475` and `-0.7071067811865476`

- sheet mirror pair:
  - `right_handed_sheet` mass = `0.8928812067096225`
  - `left_handed_sheet` mass = `0.8928800953055511`
  - mass absolute difference = `1.1114040713300355e-06`
  - chirality signs = `+0.7071067811865476` and `-0.7071067811865477`

The parity pair differs only by coordinate inversion:

- `right_handed_base` versus `parity_partner`
  - mass absolute difference = `8.221556238474648e-06`
  - chirality signs both positive

**Why this proves the claim:** The chiral-flip pairs preserve objecthood to high numerical accuracy while reversing the handedness sign, whereas the parity pair preserves the sign. That is the classical enantiomer structure Phase G needed to show.

**Supporting documents:**

- `analysis/phase_g/phase_g_chirality_analysis.py`
- `solutions/phase_g/phase_g_chirality/representative_runs.csv`
- `solutions/phase_g/phase_g_chirality/pair_comparisons.csv`
- `solutions/phase_g/phase_g_chirality/mirror_pair_results.csv`
- `solutions/phase_g/phase_g_chirality/right_handed_base_profile.csv`
- `solutions/phase_g/phase_g_chirality/left_handed_flip_profile.csv`
- `solutions/phase_g/phase_g_chirality/right_handed_sheet_profile.csv`
- `solutions/phase_g/phase_g_chirality/left_handed_sheet_profile.csv`
- `solutions/phase_g/phase_g_chirality/summary.md`
- `notes/phase_g/phase_g_verified_chirality_assessment.md`

---

### 3.4 The old rotational-stability claim is not solver-backed

**Claim:** The previous “stable spin-like host for angular momentum” wording is not supported by a solved rotational dynamics test.

**Method and rationale:** The refreshed audit traced the numerical evidence used for the old rotational claim.

**Results:** The old `rotational_stability.csv` was produced from the proxy formula

`m_rot = m_base * (1 + 5 * omega_rot^2)`

rather than from a modified solver that actually integrates rotational dynamics.

The refreshed package retains `rotational_stability.csv`, but now labels it as:

- `is_solver_backed = False`
- `interpretation = analytic_proxy_only`

**Why this proves the claim:** A hand-applied mass rescaling is not evidence of solved rotational stability. `derivation_83` remains useful as an ansatz, but the numerical rotational claim had to be downgraded.

**Supporting documents:**

- `derivations/derivation_83_rotational_energy_momentum.md`
- `analysis/phase_g/phase_g_chirality_analysis.py`
- `solutions/phase_g/phase_g_chirality/rotational_stability.csv`
- `solutions/phase_g/phase_g_chirality/summary.md`
- `notes/phase_g/phase_g_verified_chirality_assessment.md`
- `notes/phase_g/phase_g_synthesis_2026-04-02.md`

---

### 3.5 Phase G closes as a handedness-architecture phase, not as a full rotational dynamics phase

**Claim:** Phase G is complete, but the supported closure is specifically about classical handedness architecture.

**Method and rationale:** A phase can close with a narrower answer as long as the proven part and the unproven part are both explicit.

**Results:** The refreshed package now supports the following final statement:

- the object has a classical handedness architecture,
- `phi` controls the handedness sign,
- parity preserves chirality,
- the topological chiral flip reverses chirality,
- mirror-pair objecthood is solver-backed,
- but rotational stability and hosted angular momentum are not yet solved numerically.

**Why this proves the claim:** That fully answers the plan’s actual handedness goals while removing the unsupported rotational overreach.

**Supporting documents:**

- `khantraction_paper.md`
- `notes/classical_exploration_plan.md`
- `derivations/derivation_82_classical_chirality_operators.md`
- `derivations/derivation_83_rotational_energy_momentum.md`
- `analysis/phase_g/phase_g_chirality_analysis.py`
- `solutions/phase_g/summary.md`
- `solutions/phase_g/phase_g_chirality/summary.md`
- `notes/phase_g/phase_g_verified_chirality_assessment.md`
- `notes/phase_g/phase_g_synthesis_2026-04-02.md`
- `phase_g_audit_report.md`

---

## 4. What Phase G has not established

Phase G has **not** established:

- a solved rotational stability threshold,
- frame-dragging or centrifugal leakage,
- hosted angular momentum dynamics,
- helicity alignment under real rotation,
- quantum spin states.

Those belong to later work.

---

## 5. Why the phase is considered closed

Phase G is considered closed because its actual burden of proof has now been answered in audited form:

- the chirality operators were traced to their derivation,
- the mirror-pair objecthood claim was checked on solver-backed runs,
- the full slice protocol was rerun on the correct domain,
- the old rotational overclaim was separated from the solver-backed handedness result,
- and the key question has a disciplined answer.

That answer is not “full rotational dynamics is solved.” The answer is:

> Khantraction has a real classical handedness architecture, while the rotational part remains analytical and provisional.

---

## 6. Bottom line

**Bottom line:** Phase G now supports a real classical handedness result. Chirality is phi-controlled, parity preserves it, the topological chiral flip reverses it, and right-handed and left-handed mirror pairs remain nearly mass-degenerate on the audited active-runtime runs. But the old rotational stability claim was only proxy-backed, not solver-backed. That is the real Phase G result, and it is the one this closure summary now records.
