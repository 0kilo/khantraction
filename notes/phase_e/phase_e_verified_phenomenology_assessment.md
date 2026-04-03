# Phase E Assessment — Direct External Phenomenology Refresh

**Date:** 2026-04-02
**Phase:** E — External particle-likeness
**Status:** Complete after direct runtime refresh

## Direct Implementation Update

The exploratory beta-driven external phenomenology path has now been replaced by a direct pullback-runtime study.

- `analysis/phase_e/phase_e_external_phenomenology.py` now uses direct pullback radial profiles plus direct 3D impulse-response runs.
- `solutions/phase_e/phase_e_phenomenology/summary.json` shows that scalar, rich, and off-sheet seeds have exactly the same:
  - final mass `0.032534129324309234`
  - compactness-90 `11.530999999999798`
  - RN-fit parameters
  - response-ratio range `[1.1197031965320845, 1.119987028419656]`
- `solutions/phase_e/phase_e_phenomenology/indistinguishability_map.json` places all three audited seeds in one class.
- `solutions/phase_e/phase_e_phenomenology/direct_response_ladder.csv` shows a clean family-level linear response law, but not any species-specific response splitting.

So the direct refresh closes the old “no direct response law” gap, but it closes it in a way that weakens the particle-zoo interpretation: the external phenomenology is universal across the audited seed family.

Where the older audit-only material below conflicts with this direct implementation update, the direct implementation update and the linked direct outputs take precedence.

## Purpose

This note records what the refreshed Phase E analysis actually proves after tracing the paper framing, the inherited Phase A to Phase D support trail, the active Phase E solver, and the regenerated solution package.

Relevant files:
- `derivations/derivation_76_full_einstein_equations_nonminimal_coupling.md`
- `derivations/derivation_78_maurer_cartan_tensor.md`
- `derivations/derivation_79_einstein_trace_with_mc_breaking.md`
- `analysis/phase_e/phase_e_external_phenomenology.py`
- `solutions/phase_e/phase_e_phenomenology/summary.json`
- `solutions/phase_e/phase_e_phenomenology/summary.md`
- `solutions/phase_e/phase_e_phenomenology/tail_run_results.csv`
- `solutions/phase_e/phase_e_phenomenology/rn_fit_results.csv`
- `solutions/phase_e/phase_e_phenomenology/scalar_tail.csv`
- `solutions/phase_e/phase_e_phenomenology/phi_dom_tail.csv`
- `solutions/phase_e/phase_e_phenomenology/fully_mixed_tail.csv`
- `solutions/phase_e/phase_e_phenomenology/phi_offsheet_tail.csv`
- `solutions/phase_e/phase_e_phenomenology/mixed_offsheet_tail.csv`
- `solutions/phase_e/phase_e_phenomenology/indistinguishability_pairs.csv`
- `solutions/phase_e/phase_e_phenomenology/indistinguishability_map.json`
- `solutions/phase_e/phase_e_phenomenology/gradient_response_ladder.csv`
- `solutions/phase_e/phase_e_phenomenology/dynamical_response.csv`
- `solutions/phase_e/phase_e_phenomenology/slice_1d_theta.csv`
- `solutions/phase_e/phase_e_phenomenology/slice_1d_phi.csv`
- `solutions/phase_e/phase_e_phenomenology/slice_1d_rho.csv`
- `solutions/phase_e/phase_e_phenomenology/slice_2d_theta_rho.csv`
- `solutions/phase_e/phase_e_phenomenology/slice_2d_phi_theta.csv`
- `solutions/phase_e/phase_e_phenomenology/slice_2d_phi_rho.csv`

---

## 1. What the active runtime actually is

Phase E reuses the same exploratory symmetry-broken Maurer-Cartan runtime family audited in Phases C and D.

Its mathematical base is inherited rather than newly derived in Phase E:
- `derivation_76` supplies the exact nonminimal Einstein trace closure,
- `derivation_78` introduces the anisotropic Maurer-Cartan kinetic term,
- `derivation_79` folds that anisotropy into the Ricci-trace source used by the radial runtime.

The regenerated `summary.json` records:
- anisotropic Maurer-Cartan weights `beta = [0.01, 0.02, 0.03]`,
- metric regularization `1e-4`,
- phi-localized angular potential coefficient `0.01`,
- horizon event threshold `2m/r = 0.48`,
- external-tail seed amplitude `A0 = 0.005`,
- default derivative seed `xp0 = [0.0, 0.01, 0.01, 0.0]`.

So the external claims must be interpreted inside that same exploratory runtime, not as closure-independent statements about the underlying theory.

---

## 2. What was tested

The refreshed Phase E package now checks four separate layers:

1. **Representative external tails**
   - `scalar`,
   - exact-sheet `phi_dom`,
   - exact-sheet `fully_mixed`,
   - off-sheet `phi_offsheet`,
   - off-sheet `mixed_offsheet`.
2. **RN-like outer-tail fits**
   - applied only when a run actually reaches the outer `r_max = 40` box.
3. **External indistinguishability**
   - pairwise tail and fit-parameter comparisons among the successful survivor fits.
4. **Gradient-response ladder**
   - three survivor anchors,
   - gradient strengths `1e-12`, `1e-10`, `1e-8`, `1e-6`.
5. **Full 1D / 2D slice protocol**
   - all 1D and 2D angle combinations,
   - all on the active `[-2pi, 2pi]` domain.

The refreshed package also records:
- solver status,
- termination flags,
- event radii,
- final integration radius,
- final `2m/r`,
- and explicit fit diagnostics.

That was missing from the old Phase E evidence trail and is why the old ADM-charge and dynamical-response wording had to be corrected.

---

## 3. Main findings

### 3.1 Some survivor configurations do admit RN-like outer tails

The refreshed representative runs split into two classes:

- `scalar`, `phi_offsheet`, and `mixed_offsheet` reach the full `r_max = 40` interval,
- exact-sheet `phi_dom` and `fully_mixed` terminate early near `r = 3.38508`.

For the full-domain survivors, the RN-like fits are:

- `scalar`
  - `M_ADM_fit = 0.02265470583763311`
  - `Q_eff_fit = 0.8010416987423646`
  - fit RMSE `1.524256230884276e-04`
- `phi_offsheet`
  - `M_ADM_fit = 7.978766568341449`
  - `Q_eff_fit = 15.10032183300207`
  - fit RMSE `0.016264816180621033`
- `mixed_offsheet`
  - `M_ADM_fit = 7.979354683429322`
  - `Q_eff_fit = 15.101684014867716`
  - fit RMSE `0.016262888640353454`

So some extended structured folds do admit smooth outer tails that can be approximated by an RN-like mass function on the audited outer region.

### 3.2 The old exact-sheet ADM-charge claim was overstated

The old Phase E wording treated exact-sheet `phi_dom` and `fully_mixed` as deep-tail asymptotic successes. The refreshed tail diagnostics show that both:

- terminate early,
- stop at `r_final ≈ 3.38508`,
- never reach the outer `r = 40` box,
- and therefore do **not** support a genuine deep asymptotic fit.

So the old “phi-dominant charged point-particle” claim, as written, was not supported by the actual saved tail data.

### 3.3 External indistinguishability does occur

The strongest audited indistinguishability class is:

- `phi_offsheet`
- `mixed_offsheet`

Their pairwise diagnostics are:
- tail max absolute difference on `r in [30, 40]`: `1.4057479065243683e-06`
- tail mean absolute difference: `4.1461433580192165e-07`
- `M_ADM_fit` difference: `0.0005881150878730423`
- `Q_eff_fit` difference: `0.0013621818656464058`

That is strong evidence that internally different configurations can become externally almost indistinguishable in the current runtime.

### 3.4 The external footprint remains phi-dominated

The refreshed slice widths are:

- 1D theta width: `1.8688606218120185e-11`
- 1D phi width: `3.0880666871106057`
- 1D rho width: `0.3859091722317475`
- 2D `(theta, rho)` width: `0.20254158052953192`
- 2D `(phi, theta)` width: `1.8804457800616183`
- 2D `(phi, rho)` width: `1.880445780076083`

So the outer mass footprint remains organized mainly by phi. Theta is nearly flat on the audited 1D slice, while rho has a secondary standalone effect.

### 3.5 The current background-gradient probe does not support a clean effective-mass law

This is the strongest correction to the old dynamical-response claim.

In the perturbative regime (`1e-12`, `1e-10`), the shifts are small:
- `scalar`: `8.04182584423184e-06` to `8.041825843219282e-04`
- `phi_offsheet`: `7.534725646074492e-06` to `7.534727048899015e-04`
- `mixed_offsheet`: `-7.534725608770998e-06` to `-7.534724216649025e-04`

But outside that window:
- `scalar` becomes strongly non-perturbative,
- `phi_offsheet` becomes strongly non-perturbative,
- `mixed_offsheet` eventually develops a negative final mass under the same simple probe ansatz.

So the present background-gradient loading is not yet a clean basis for claiming an effective inertial-vs-gravitational mass law or a reliable equation-of-motion model.

---

## 4. Correct interpretation

The refreshed Phase E result is mixed:

- stronger than before, because the successful external-tail fits and the indistinguishability class are now explicitly documented and checked,
- narrower than before, because the old exact-sheet asymptotic and inertial-response claims do not survive the audit.

The phase therefore supports the following audited statement:

> In the current exploratory runtime, some survivor Khantraction configurations do behave particle-like externally in the limited sense of admitting smooth RN-like outer tails, and at least one externally indistinguishable class exists. But the present gradient-response probe does not yet establish a clean effective equation of motion.

---

## 5. Bottom line

**Bottom line:** Phase E now supports a partial external particle-likeness claim. Some survivor anchors have smooth RN-like tails, and `phi_offsheet` / `mixed_offsheet` provide a strong external indistinguishability class. But exact-sheet anchors do not reach the asymptotic zone, and the current background-gradient probe does not support a clean inertial-mass interpretation. The honest audited reading is therefore “external particle-likeness for a subset of survivor configurations, with dynamical response still unresolved.”
