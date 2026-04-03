# Phase F Closure Summary — Classical Hosting Audit

**Date:** 2026-03-29  
**Phase:** F — Classical hosting properties  
**Status:** Closed after audit refresh

## 0. Project-level disposition

Phase F is deferred in the project-level closure plan. Its signed probe-response asymmetry survives, but strong classical hosting is not established and the phase is not treated as a blocker for the final classical particle-level verdict. The governing synthesis is recorded in `summary/2026-04-02_gap_closure_summary.md`, `notes/2026-04-02_direct_data_closure_plan.md`, and `summary/2026-04-02_khantraction_model_conclusion.md`.

## 1. Scope and motivation

`khantraction_paper.md` treats Khantraction as a toy model of structured spacetime folds, not as a finished theory of matter or charge.

That means Phase F is not supposed to prove that the model already hosts real particle content in a final physical sense. Its narrower burden is:

- define a mathematically explicit probe-coupling ansatz,
- test whether the structured object measurably changes the probe response,
- compare opposite signed loadings,
- and map where that response sensitivity lives across the angular domain.

This is the classical precursor to later charge-hosting work, as stated in `notes/classical_exploration_plan.md`.

The active Phase F solver does not introduce a brand-new background model. It inherits:

- the exact nonminimal Einstein trace closure from `derivations/derivation_76_full_einstein_equations_nonminimal_coupling.md`,
- the exploratory anisotropic Maurer-Cartan breaking from `derivations/derivation_78_maurer_cartan_tensor.md`,
- the Ricci-trace update from `derivations/derivation_79_einstein_trace_with_mc_breaking.md`,
- and the probe-field coupling ansatz from `derivations/derivation_80_external_field_coupling.md`.

The active Phase F convention remained:

- `omega > 0`
- `theta, phi, rho in [-2pi, 2pi]`
- no redundancy quotienting

That framing is consistent with:
- `khantraction_paper.md`
- `notes/classical_exploration_plan.md`
- `derivations/derivation_76_full_einstein_equations_nonminimal_coupling.md`
- `derivations/derivation_78_maurer_cartan_tensor.md`
- `derivations/derivation_79_einstein_trace_with_mc_breaking.md`
- `derivations/derivation_80_external_field_coupling.md`

---

## 2. Audit against `notes/classical_exploration_plan.md`

### 2.1 Goal 1 — Study whether the structured object can host externally induced content

**Status:** Partially met.

**How it was tested:** The refreshed package integrates the explicit probe-field ansatz on representative active-runtime backgrounds and records:

- solver status,
- final mass,
- final probe amplitude,
- core-vs-outer probe averages,
- and localization ratios.

It also compares `gamma_host = 0` against `gamma_host = 0.1` to test whether the explicit Maurer-Cartan coupling itself materially changes the probe response.

**Why this proves the goal:** This directly tests whether the probe merely responds to the background or actually becomes more localized because of the hosting term.

### 2.2 Goal 2 — Compare opposite signed induced loadings

**Status:** Met as an exploratory load-response asymmetry result.

**How it was tested:** The refreshed package runs a signed loading ladder

- `J_ext in {-0.01, -0.001, 0.0, 0.001, 0.01}`

across representative anchors and records:

- final mass,
- final probe response,
- solver status,
- and final integration radius.

**Why this proves the goal:** This is the right direct test of whether opposite induced loading signs produce materially different outcomes.

### 2.3 Goal 3 — Locate where hosting sensitivity lives

**Status:** Partially met.

**How it was tested:** The refreshed package runs the full 1D / 2D slice protocol on the full `[-2pi, 2pi]` domain using:

- `probe_response_ratio = psi_final / psi_initial`
- `localization_ratio = <|psi|>_core / <|psi|>_outer`

with status-aware outputs.

**Why this proves the goal:** These slices identify where the probe response changes across the angular domain, even when the evidence for strong trapping remains incomplete.

### 2.4 Goal 4 — Test whether different angular sectors host content differently

**Status:** Partially met.

**How it was tested:** Representative anchor comparisons and full-domain slice widths test whether scalar-like, theta-like, rho-like, and phi-rich sectors produce measurably different probe-response profiles.

**Why this proves the goal:** This checks sector dependence directly instead of assuming it from earlier internal labels alone.

### 2.5 Common slice protocol

**Status:** Met after audit refresh.

The refreshed Phase F slice set now includes:

- 1D `theta`, `phi`, `rho` on `[-2pi, 2pi]`
- 2D `(theta, rho)`, `(phi, theta)`, `(phi, rho)` on `[-2pi, 2pi]^2`

with status-aware outputs written to the active solution package.

### 2.6 Phase F key question

The plan asks:

> Can the structured object classically act as a host for externally supplied content?

After the audit, the answer is:

- **explicit probe coupling:** yes,
- **sign-sensitive probe response:** yes,
- **angular response sensitivity:** yes,
- **robust classical hosting in a strong trapping sense:** not yet established.

That is the actual audited Phase F result.

---

## 3. Final Phase F conclusions

### 3.1 The probe-field coupling ansatz exists, but the explicit Maurer-Cartan hosting term is subleading in the current implementation

**Claim:** Derivation 80 supplies a valid probe-coupling ansatz, but the explicit `gamma_host` term is not yet the dominant source of the observed probe response.

**Method and rationale:** The right test is a gamma-on versus gamma-off comparison on the same backgrounds. If the explicit hosting term is carrying the effect, turning it off should materially change the probe response.

**Results:** The refreshed coupling comparison gives:

- `scalar`: `probe_response_ratio` delta = `4.218847493575595e-15`
- `phi_sheet`: delta = `8.371681126106978e-11`
- `phi_offsheet`: delta = `0.004316488908030491`
- `mixed_offsheet`: delta = `0.004316488906694005`

Those deltas are tiny compared with the total response levels:

- `scalar`: `1.1783929446946346`
- `phi_offsheet`: `1.273311616144233`
- `mixed_offsheet`: `1.2733116161332019`

**Why this proves the claim:** The explicit coupling changes the output only at the fourth decimal place for the most responsive survivor anchors and effectively not at all for scalar-like anchors. So the current probe behavior is driven mainly by the inherited background geometry, not by a strong standalone hosting term.

**Supporting documents:**

- `derivations/derivation_80_external_field_coupling.md`
- `analysis/phase_f/phase_f_hosting_analysis.py`
- `solutions/phase_f/phase_f_hosting/coupling_comparison.csv`
- `solutions/phase_f/phase_f_hosting/summary.json`
- `solutions/phase_f/phase_f_hosting/summary.md`
- `notes/phase_f/phase_f_verified_hosting_assessment.md`

---

### 3.2 The unloaded active-runtime runs do not establish strong trapping or core localization

**Claim:** The current Phase F package does not prove robust classical hosting in the strong sense of a probe becoming more concentrated in the core than in the outer region.

**Method and rationale:** A true hosting claim requires more than a coupled integration. The probe should show some kind of core-favoring localization signature. The refreshed representative runs therefore measure

- `probe_response_ratio = psi_final / psi_initial`
- `localization_ratio = <|psi|>_core / <|psi|>_outer`

on the active runtime.

**Results:** The unloaded representative anchors are:

- `scalar`:
  - `status = 0`
  - `psi_final = 0.11783929446946348`
  - `probe_response_ratio = 1.1783929446946346`
  - `localization_ratio = 0.8720466979005634`
- `theta_seed`:
  - `probe_response_ratio = 1.1783929446945591`
  - `localization_ratio = 0.8717732154160472`
- `rho_seed`:
  - `probe_response_ratio = 1.1783929446945223`
  - `localization_ratio = 0.87185894017199`
- `phi_sheet`:
  - `status = 1`
  - `r_final = 3.382921053355878`
  - `probe_response_ratio = 1.0160266653077443`
  - `localization_ratio = 0.9888319340899799`
- `phi_offsheet`:
  - `probe_response_ratio = 1.273311616144233`
  - `localization_ratio = 0.8182228010863636`
- `mixed_offsheet`:
  - `probe_response_ratio = 1.2733116161332019`
  - `localization_ratio = 0.8181990228063704`

Every unloaded survivor anchor has `localization_ratio < 1`, and the exact-sheet anchor terminates early before any deep hosting interpretation is justified.

**Why this proves the claim:** The probe is not becoming more concentrated in the core than in the outer region on the audited unloaded runs. So the current evidence supports probe response, not a strong trapping proof.

**Supporting documents:**

- `analysis/phase_f/phase_f_hosting_analysis.py`
- `solutions/phase_f/phase_f_hosting/representative_runs.csv`
- `solutions/phase_f/phase_f_hosting/scalar_profile.csv`
- `solutions/phase_f/phase_f_hosting/theta_seed_profile.csv`
- `solutions/phase_f/phase_f_hosting/rho_seed_profile.csv`
- `solutions/phase_f/phase_f_hosting/phi_sheet_profile.csv`
- `solutions/phase_f/phase_f_hosting/phi_offsheet_profile.csv`
- `solutions/phase_f/phase_f_hosting/mixed_offsheet_profile.csv`
- `solutions/phase_f/phase_f_hosting/summary.json`
- `solutions/phase_f/phase_f_hosting/summary.md`
- `notes/phase_f/phase_f_verified_hosting_assessment.md`

---

### 3.3 Signed loading asymmetry is real, but it is a load-response asymmetry rather than proof of stable hosted matter

**Claim:** Opposite loading signs materially change both the mass response and the probe response.

**Method and rationale:** The refreshed signed loading ladder is the correct direct test of whether the object reacts asymmetrically to opposite external loadings.

**Results:** The effect is strong on the main survivor anchors.

For `scalar`:

- `J_ext = -0.01`:
  - `final_mass = 2.167485190562235`
  - `probe_response_ratio = 0.930769698007601`
- `J_ext = +0.01`:
  - `final_mass = -1.1991859381621084`
  - `probe_response_ratio = 1.3993697457290926`

For `phi_offsheet`:

- `J_ext = -0.01`:
  - `final_mass = 5.6027902759390065`
  - `probe_response_ratio = 0.6952276171106406`
- `J_ext = +0.01`:
  - `final_mass = 1.411472698310113`
  - `probe_response_ratio = 1.750916228510713`

For `mixed_offsheet`, the same pattern appears to numerical precision.

For `phi_sheet`, the effect is milder but still monotone in the same direction, with all runs terminating early near the same horizon sheet.

**Why this proves the claim:** Negative loading increases the final mass and suppresses the probe response, while positive loading decreases the mass and amplifies the probe response. That is a real sign-sensitive asymmetry. But because one side can drive scalar mass negative and the unloaded runs do not prove trapping, the honest interpretation is load-response asymmetry, not proof of stable hosted matter.

**Supporting documents:**

- `analysis/phase_f/phase_f_hosting_analysis.py`
- `solutions/phase_f/phase_f_hosting/signed_loading_ladder.csv`
- `solutions/phase_f/phase_f_hosting/signed_loading_test.csv`
- `solutions/phase_f/phase_f_hosting/summary.json`
- `solutions/phase_f/phase_f_hosting/summary.md`
- `notes/phase_f/phase_f_verified_hosting_assessment.md`
- `notes/phase_f/phase_f_synthesis_2026-04-02.md`

---

### 3.4 Angular probe response is phi-dominated, while theta-only and rho-only seeds remain close to scalar

**Claim:** Different angular sectors do affect the probe response, but the effect is narrower and more phi-driven than the old “species hosting hierarchy” wording implied.

**Method and rationale:** The correct test is:

- representative anchor comparison,
- plus the full 1D / 2D slice protocol on the active domain.

**Results:** The representative anchors already show the pattern:

- `scalar`, `theta_seed`, and `rho_seed` all sit at `probe_response_ratio ≈ 1.178392944694...`
- `phi_offsheet` and `mixed_offsheet` both sit at `probe_response_ratio ≈ 1.27331161614...`
- `phi_sheet` is distinct mainly because it terminates early at `r_final = 3.382921053355878`

The refreshed slice widths confirm that phi is the main controller:

- 1D `theta` width = `9.294787219640933e-13`
- 1D `phi` width = `0.08804633536947054`
- 1D `rho` width = `0.007467723133360876`
- 2D `(theta, rho)` width = `0.007467723134008808`
- 2D `(phi, theta)` width = `0.08804633205702057`
- 2D `(phi, rho)` width = `0.08804633207320292`

**Why this proves the claim:** Theta-only and rho-only variations remain close to scalar, while phi-rich off-sheet sectors materially increase the probe response. So sector dependence exists, but it is primarily phi-driven rather than a broad balanced hierarchy across all angular channels.

**Supporting documents:**

- `analysis/phase_f/phase_f_hosting_analysis.py`
- `solutions/phase_f/phase_f_hosting/representative_runs.csv`
- `solutions/phase_f/phase_f_hosting/slice_1d_theta.csv`
- `solutions/phase_f/phase_f_hosting/slice_1d_phi.csv`
- `solutions/phase_f/phase_f_hosting/slice_1d_rho.csv`
- `solutions/phase_f/phase_f_hosting/slice_2d_theta_rho.csv`
- `solutions/phase_f/phase_f_hosting/slice_2d_phi_theta.csv`
- `solutions/phase_f/phase_f_hosting/slice_2d_phi_rho.csv`
- `solutions/phase_f/phase_f_hosting/angular_hosting_map.csv`
- `solutions/phase_f/phase_f_hosting/summary.json`
- `solutions/phase_f/phase_f_hosting/summary.md`
- `notes/phase_f/phase_f_verified_hosting_assessment.md`

---

### 3.5 The old “Phase E effective charge physically validated as a trap” claim is not supported by the refreshed evidence

**Claim:** The current Phase F evidence does not justify saying that the Phase E external proxy has already been physically validated as a localized trap.

**Method and rationale:** The right check is to compare the phi-rich sectors that were externally distinctive in Phase E against the refreshed Phase F localization and gamma-on/gamma-off diagnostics.

**Results:** The most responsive survivor anchors are `phi_offsheet` and `mixed_offsheet`, but:

- both have `localization_ratio ≈ 0.818`, not a core-favoring signature,
- both have only `~0.0043` gamma-on versus gamma-off probe-response deltas,
- and the exact-sheet `phi_sheet` anchor terminates early before supporting a strong trapping interpretation.

**Why this proves the claim:** The refreshed data shows that phi-rich sectors are responsive, not that they already constitute a robust physical trapping well for external content.

**Supporting documents:**

- `summary/2026-03-29_phase_e_closure_summary.md`
- `analysis/phase_f/phase_f_hosting_analysis.py`
- `solutions/phase_f/phase_f_hosting/coupling_comparison.csv`
- `solutions/phase_f/phase_f_hosting/representative_runs.csv`
- `solutions/phase_f/phase_f_hosting/summary.md`
- `notes/phase_f/phase_f_verified_hosting_assessment.md`

---

### 3.6 Phase F closes as a partial probe-response phase, not as proof of robust classical hosting

**Claim:** Phase F is complete, but the closed claim is narrower than the old wording.

**Method and rationale:** A phase can close with a partial answer as long as the answer is explicit and the unresolved burden is carried forward honestly.

**Results:** The refreshed package now supports the following final statement:

- an explicit probe-coupling ansatz exists,
- sign-sensitive load response is real,
- angular probe sensitivity is real and phi-dominated,
- but robust classical hosting in a strong trapping sense is not yet established.

**Why this proves the claim:** That answers the plan’s key question honestly while keeping the unresolved hosting burden visible for later repair.

**Supporting documents:**

- `khantraction_paper.md`
- `notes/classical_exploration_plan.md`
- `derivations/derivation_80_external_field_coupling.md`
- `summary/2026-03-29_phase_e_closure_summary.md`
- `analysis/phase_f/phase_f_hosting_analysis.py`
- `solutions/phase_f/summary.md`
- `solutions/phase_f/phase_f_hosting/summary.md`
- `notes/phase_f/phase_f_verified_hosting_assessment.md`
- `notes/phase_f/phase_f_synthesis_2026-04-02.md`
- `phase_f_audit_report.md`

---

## 4. What Phase F has not established

Phase F has **not** established:

- strong trapping of externally supplied content,
- a clean core-localization proof,
- physical validation of the Phase E effective-charge proxy as a trap,
- a mature loading Hamiltonian or equation of motion for hosted matter,
- loaded chirality or loaded quantum response.

Those belong to later work.

---

## 5. Why the phase is considered closed

Phase F is considered closed because its actual burden of proof has now been answered in audited form:

- the coupling ansatz was traced to its derivation,
- the active-runtime solver was refreshed and rerun,
- the full slice protocol is present on the correct domain,
- signed loading asymmetry was tested directly,
- the old overclaims about robust hosting and trap validation are now corrected,
- and the key question has a disciplined partial answer.

That answer is not “Khantraction already hosts content robustly.” The answer is:

> the current runtime supports sign-sensitive probe response on structured backgrounds, but strong classical hosting is still unresolved.

---

## 6. Bottom line

**Bottom line:** Phase F now supports a real but partial probe-response result. The model has an explicit probe-coupling ansatz, the response to external loading is strongly sign-sensitive, and the angular dependence is clearly phi-dominated. But the explicit Maurer-Cartan hosting term is subleading, unloaded localization ratios remain below 1, and the present package does not yet prove robust classical hosting of externally supplied content. That is the real Phase F result, and it is the one this closure summary now records.
