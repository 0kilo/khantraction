# Phase H Closure Summary — Quantum-Facing Restart Audit

**Date:** 2026-03-30  
**Phase:** H — Return to Stronger Quantum-Facing Work  
**Status:** Closed after audit refresh

## 0. Project-level disposition

Phase H is outside the current classical particle-level verdict. Its current result remains a corrected semiclassical proxy, so it is explicitly excluded from the project-level decision on whether Khantraction works as a classical particle model. The governing synthesis is recorded in `summary/2026-04-02_gap_closure_summary.md`, `notes/2026-04-02_direct_data_closure_plan.md`, and `summary/2026-04-02_khantraction_model_conclusion.md`.

## 1. Scope and motivation

`khantraction_paper.md` presents Khantraction as an exploratory toy model for structured spacetime folds, not as a finished particle theory.

That matters even more in Phase H than in the earlier classical phases. The Phase H section of `notes/classical_exploration_plan.md` does not say that a full quantum theory has already been earned. It says that only after the classical object picture is rebuilt can the project return to stronger quantum-facing questions such as:

- whether excitation channels exist,
- whether mode ladders form,
- whether chirality or loading affect them,
- and whether quasi-discrete structure survives improved operators.

So the burden of proof for the audited Phase H package is narrower than the old closure summary claimed. The phase has to show what the current semiclassical ansatz actually supports, while staying honest about the gaps left by the refreshed Phase F and Phase G audits.

The active Phase H convention remained:

- `omega > 0`
- `theta, phi, rho in [-2pi, 2pi]`
- no redundancy quotienting

The support chain for the refreshed audit is:

- `khantraction_paper.md`
- `notes/classical_exploration_plan.md`
- `derivations/derivation_84_quantum_excitation_ansatz.md`
- `derivations/derivation_85_discrete_spectrum_conditions.md`
- `derivations/derivation_82_classical_chirality_operators.md`
- `summary/2026-03-29_phase_f_closure_summary.md`
- `notes/phase_f/phase_f_verified_hosting_assessment.md`
- `summary/2026-03-29_phase_g_closure_summary.md`
- `notes/phase_g/phase_g_verified_chirality_assessment.md`

---

## 2. Audit against `notes/classical_exploration_plan.md`

The plan does not prescribe a finished QFT in Phase H. It reopens the program to stronger quantum-facing work by asking four concrete questions. After tracing the derivations, code, notes, and regenerated solution package, the audited status is:

### 2.1 Question 1 — Does a quantum-facing excitation ansatz exist?

**Status:** Met at the proxy level.

**How it was tested:** Derivations 84 and 85 define a draft wave-equation and quantization framework. The refreshed script implements the reduced Bohr-Sommerfeld proxy explicitly and records its assumptions in `summary.json`.

**Why this proves the point:** The project now has a concrete semiclassical excitation ansatz that can be inspected, rerun, and audited. It is not just narrative speculation.

### 2.2 Question 2 — Do mode ladders form?

**Status:** Partially met.

**How it was tested:** The refreshed script searches for proxy roots with `n = 0, 1, 2` on representative states within the fixed bracket `[0.01, 2.0]`.

**Why this only partially proves the point:** The current package finds a sampled `n = 0` root, but not a robust multi-level ladder. So the present evidence supports a ground-state proxy, not a fully established native mode ladder.

### 2.3 Question 3 — Do chirality or loading affect the proxy spectrum?

**Status:** Met within the current proxy model.

**How it was tested:** The refreshed package compares:

- a right-handed base state,
- its parity partner,
- its true `phi -> phi + pi/2` chiral-flip partner,
- and a loading sweep on the right-handed base state.

**Why this proves the point:** These tests isolate the two control channels the plan highlighted: handedness and external content.

### 2.4 Question 4 — Does the quasi-discrete structure survive improved operators?

**Status:** Not met.

**How it was tested:** It was not. The current Phase H package still uses the same draft proxy ansatz rather than a stronger operator built from the regenerated classical backgrounds.

**Why this matters:** The classical plan explicitly says stronger quantum-facing work should restart on stronger footing. That stronger footing has not yet been realized at the operator level.

### 2.5 Common slice protocol

**Status:** Met after audit refresh.

The refreshed Phase H package now includes:

- 1D `theta`, `phi`, `rho` slices on `[-2pi, 2pi]`
- 2D `(phi, theta)`, `(theta, rho)`, `(phi, rho)` slices on `[-2pi, 2pi]^2`

The old 2D `[-pi, pi]` truncation has been removed.

---

## 3. Final Phase H conclusions

### 3.1 The current Phase H runtime is a semiclassical proxy, not a native solver-backed quantum operator on the refreshed background

**Claim:** The audited Phase H package implements a hand-built resonator proxy rather than a wave operator extracted from the refreshed Phase F hosting backgrounds.

**Method and rationale:** This claim is established by tracing the actual code and regenerated metadata, not by inferring from the old prose. The refreshed script records its runtime scope directly in `summary.json`.

**Results:** The active proxy consists of:

- a quartic resonator well with `hosting_depth_proxy = 0.999`,
- a chirality shift `lambda_chi * chi` with `lambda_chi = 0.05`,
- a Gaussian loading term,
- a fixed proxy box size `r_h = 3.0`,
- and a fixed search bracket `[0.01, 2.0]`.

The summary explicitly states:

- `type = semiclassical_proxy`
- "not a solved wave equation on an audited Phase F trapping background."

**Why this proves the claim:** The current Phase H evidence is controlled by explicit proxy choices, not by an operator solved on regenerated classical profiles. So the right interpretation is semiclassical-proxy evidence, not native-spectrum proof.

**Supporting documents:**

- `derivations/derivation_84_quantum_excitation_ansatz.md`
- `derivations/derivation_85_discrete_spectrum_conditions.md`
- `analysis/phase_h/phase_h_quantum_analysis.py`
- `solutions/phase_h/phase_h_quantum/summary.json`
- `solutions/phase_h/phase_h_quantum/summary.md`
- `notes/phase_h/phase_h_verified_quantum_assessment.md`
- `notes/phase_h/phase_h_synthesis_2026-04-02.md`

---

### 3.2 A sampled ground-state proxy root exists, but a full ladder is not established

**Claim:** The refreshed package supports a sampled ground-state proxy mode, not a robust multi-level ladder claim.

**Method and rationale:** The correct test is to search for modes `n = 0, 1, 2` on representative states and count what actually converges.

**Results:** The representative spectra are:

- `Scalar Anchor`: `chi = 1.0`, `mode_count = 1`, `E0 = 0.9173867490363242`
- `Right-Handed Base`: `chi = 0.7071067811865476`, `mode_count = 1`, `E0 = 0.9093699942084978`
- `Parity Partner`: `chi = 0.7071067811865476`, `mode_count = 1`, `E0 = 0.9093699942084978`
- `Left-Handed Flip`: `chi = -0.7071067811865477`, `mode_count = 1`, `E0 = 0.869622394058611`

Only `n = 0` appears in the representative tables within the audited bracket.

**Why this proves the claim:** A single stable proxy root is enough to show that the ansatz can produce a discrete-like sampled state. It is not enough to justify the stronger old language of established mode ladders or multiple levels.

**Supporting documents:**

- `analysis/phase_h/phase_h_quantum_analysis.py`
- `solutions/phase_h/phase_h_quantum/excitation_spectrum.json`
- `solutions/phase_h/phase_h_quantum/representative_spectra.csv`
- `solutions/phase_h/phase_h_quantum/summary.json`
- `solutions/phase_h/phase_h_quantum/summary.md`
- `notes/phase_h/phase_h_verified_quantum_assessment.md`

---

### 3.3 Parity leaves the proxy spectrum unchanged, while the true chiral flip splits it

**Claim:** The refreshed Phase H proxy respects the audited Phase G handedness architecture: parity is spectrally degenerate, while the true chiral flip changes the ground-state energy.

**Method and rationale:** The old Phase H claim was rechecked against audited Phase G chirality. The refreshed script now uses

`chi = det(J) = cos(2phi)`

and compares:

- a parity pair: `phi = pi/8` versus `phi = -pi/8`
- a true chiral-flip pair: `phi = pi/8` versus `phi = 5pi/8`

**Results:** The pair comparison table gives:

- parity pair:
  - same chirality sign,
  - `E0` difference = `0.0`
- chiral-flip pair:
  - opposite chirality signs,
  - `E0` difference = `0.039747600149886875`

**Why this proves the claim:** The refreshed result is now consistent with Phase G. Parity preserves chirality and therefore leaves the proxy spectrum unchanged. Only the true topological chiral flip produces the spectral split.

**Supporting documents:**

- `derivations/derivation_82_classical_chirality_operators.md`
- `summary/2026-03-29_phase_g_closure_summary.md`
- `analysis/phase_h/phase_h_quantum_analysis.py`
- `solutions/phase_h/phase_h_quantum/excitation_spectrum.json`
- `solutions/phase_h/phase_h_quantum/pair_comparisons.csv`
- `solutions/phase_h/phase_h_quantum/summary.md`
- `notes/phase_h/phase_h_verified_quantum_assessment.md`

---

### 3.4 External loading shifts the proxy ground state monotonically

**Claim:** Within the present proxy model, external loading changes the ground-state energy in a smooth monotone way.

**Method and rationale:** The right test is a direct loading sweep on a fixed representative state, keeping chirality fixed while varying the added loading term.

**Results:** For the right-handed base state:

- `loading = -0.1`: `E0 = 0.8755308759378563`
- `loading = -0.05`: `E0 = 0.8926080440711557`
- `loading = 0.0`: `E0 = 0.9093699942084978`
- `loading = 0.05`: `E0 = 0.9258350572772599`
- `loading = 0.1`: `E0 = 0.9420200171751509`

The total span is

- `0.06648914123729466`

and the refreshed package records this as monotone increasing.

**Why this proves the claim:** The loading scan shows a consistent one-parameter spectral response inside the proxy ansatz. That supports loading sensitivity as a real proxy effect.

**Supporting documents:**

- `analysis/phase_h/phase_h_quantum_analysis.py`
- `solutions/phase_h/phase_h_quantum/loading_sensitivity.csv`
- `solutions/phase_h/phase_h_quantum/summary.json`
- `solutions/phase_h/phase_h_quantum/summary.md`
- `notes/phase_h/phase_h_verified_quantum_assessment.md`

---

### 3.5 The present proxy is phi-controlled; theta and rho are exact spectators

**Claim:** In the refreshed Phase H runtime, spectral variation is controlled by `phi` alone.

**Method and rationale:** The slice protocol is the direct check. If `theta` or `rho` matter, their 1D and 2D sweeps should produce nonzero spectral width.

**Results:** The refreshed slice widths are:

- 1D `theta`: `0.0`
- 1D `phi`: `0.05622564488235715`
- 1D `rho`: `0.0`
- 2D `(phi, theta)`: `0.05622564488235715`
- 2D `(theta, rho)`: `0.0`
- 2D `(phi, rho)`: `0.05622564488235715`

All `theta` and `rho` slice entries remain at the same `E0` value when `phi` is held fixed.

**Why this proves the claim:** The current proxy potential depends on `chi = cos(2phi)` and the loading term only. So the phi-only response is real for this runtime, but it is a consequence of the proxy construction rather than a solved emergent discovery about the full theory.

**Supporting documents:**

- `analysis/phase_h/phase_h_quantum_analysis.py`
- `solutions/phase_h/phase_h_quantum/slice_1d_theta_energy.csv`
- `solutions/phase_h/phase_h_quantum/slice_1d_phi_energy.csv`
- `solutions/phase_h/phase_h_quantum/slice_1d_rho_energy.csv`
- `solutions/phase_h/phase_h_quantum/slice_2d_phi_theta_energy.csv`
- `solutions/phase_h/phase_h_quantum/slice_2d_theta_rho_energy.csv`
- `solutions/phase_h/phase_h_quantum/slice_2d_phi_rho_energy.csv`
- `solutions/phase_h/phase_h_quantum/summary.json`
- `solutions/phase_h/phase_h_quantum/summary.md`
- `notes/phase_h/phase_h_verified_quantum_assessment.md`

---

### 3.6 Improved-operator robustness is still open

**Claim:** The present Phase H package does not prove that quasi-discrete structure survives stronger operators.

**Method and rationale:** This is an audit-by-absence claim. The support chain was checked for any stronger operator build or regenerated wave-equation solve on audited backgrounds.

**Results:** No such implementation is present in the active Phase H package. The derivations remain draft-level, and the script still evaluates the same proxy ansatz.

**Why this proves the claim:** The classical plan explicitly reserved this question for later stronger quantum-facing work. The present package does not close it.

**Supporting documents:**

- `notes/classical_exploration_plan.md`
- `derivations/derivation_84_quantum_excitation_ansatz.md`
- `derivations/derivation_85_discrete_spectrum_conditions.md`
- `analysis/phase_h/phase_h_quantum_analysis.py`
- `notes/phase_h/phase_h_verified_quantum_assessment.md`
- `phase_h_audit_report.md`

---

## 4. Final Phase H reading

The defensible audited Phase H result is:

- **semiclassical excitation ansatz:** yes
- **sampled ground-state proxy root:** yes
- **parity-based splitting:** no
- **true chiral-flip splitting:** yes, in the current proxy
- **loading sensitivity:** yes, in the current proxy
- **full-domain slice protocol:** yes, after refresh
- **native solver-backed Khantraction spectrum:** no
- **robustness under improved operators:** not yet established

---

## 5. What Phase H has not established

Phase H has **not** established:

- a full quantum field theory,
- a wave operator solved on the refreshed Phase F hosting backgrounds,
- a robust multi-level mode ladder,
- robustness under stronger operators,
- or a direct mapping from these proxy levels to Standard Model particles.

---

## 6. Why the phase is considered closed

Phase H is considered closed after audit refresh because the current package now has a clear, accurate interpretation:

- the code, notes, and summary agree on what model was actually run,
- the slice protocol has been restored to the active domain,
- the chirality logic now matches audited Phase G,
- and the surviving claims are sharply separated from the unsupported historical overclaims.

So the phase closes as a **corrected semiclassical restart**, not as a final proof of native Khantraction quantum physics.

---

## 7. Bottom line

**Bottom line:** Phase H now supports a corrected semiclassical proxy result. The current Bohr-Sommerfeld ansatz admits a sampled `n = 0` root, parity leaves that proxy spectrum unchanged, the true `phi -> phi + pi/2` chiral flip splits it, loading shifts it monotonically, and the full-domain slice protocol has been restored. But the runtime is still a hand-built resonator model rather than a solver-backed quantum operator extracted from the refreshed classical background, so strong native mode-ladder claims remain open.
