# Phase C Closure Summary — Distinct Angular Traits Audit

**Date:** 2026-03-29  
**Phase:** C — Distinct angular traits  
**Status:** Closed after audit refresh

## 1. Scope and motivation

`khantraction_paper.md` frames Khantraction as a speculative toy model for localized structured spacetime-fold objects, not as a finished particle theory.

That framing matters here. Phase C was never supposed to jump straight to final particle labels. Its job was narrower and more foundational:

- start from the Phase A result that the ordered map contains genuinely different angular directions,
- face the Phase B result that the exact linear-basis classical runtime is effectively angularly blind at fixed `omega`,
- and test whether an explicit symmetry-broken runtime can make those angular directions show up as different classical traits.

The active Phase C convention remained:

- `omega > 0`
- `theta, phi, rho in [-2pi, 2pi]`
- no redundancy quotienting

That framing is consistent with:

- `khantraction_paper.md`
- `notes/classical_exploration_plan.md`

---

## 2. Audit against `notes/classical_exploration_plan.md`

### 2.1 Goal 1 — Vary `theta`, `phi`, and `rho` separately and systematically

**Status:** Met after audit refresh.

**How it was tested:** The refreshed Phase C package includes:

- representative seeded anchors,
- angle-only anchor checks,
- all three 1D slices,
- and all three 2D angle-pair slices.

All slice studies now use the active unquotiented domain `[-2pi, 2pi]`.

**Why this proves the goal:** The plan required the full channel comparison, not a single favored angular scan. The refreshed package now covers the full 1D and 2D angular comparison set.

### 2.2 Goal 2 — Compare shape, concentration, compactness, external profile, and core/bulk balance

**Status:** Met within the active exploratory runtime, with an important survival caveat.

**How it was tested:** The representative and angle-only anchor outputs report:

- final mass,
- mass half-radius,
- mass 90% radius,
- core mass fraction,
- skewness proxy,
- final compactness proxy `2m/r`,
- and explicit radial profile exports.

The slice studies then map how mass response changes across the angular domain.

**Why this proves the goal:** The anchor diagnostics are enough to compare concentration, compactness, and core/bulk balance directly. The slices then show which angular directions drive those changes.

### 2.3 Goal 3 — Avoid prematurely collapsing all angular behavior into one channel

**Status:** Met.

**How it was tested:** The refreshed package compares the channels separately and jointly before drawing any role conclusion.

**Why this proves the goal:** The final interpretation does not collapse everything into one label. It distinguishes:

- `phi` as the dominant driver,
- `rho` as a secondary standalone driver,
- `theta` as weak on the audited standalone 1D slice but still part of the paired angular structure.

### 2.4 Common slice protocol

**Status:** Met after audit refresh.

The audited Phase C slice set is:

- 1D `theta` slice: fix `omega = 0.5`, `phi = pi/8`, `rho = 0`
- 1D `phi` slice: fix `omega = 0.5`, `theta = 0`, `rho = 0`
- 1D `rho` slice: fix `omega = 0.5`, `theta = 0`, `phi = pi/8`
- 2D `(theta, rho)` slice: fix `omega = 0.5`, `phi = pi/8`
- 2D `(phi, theta)` slice: fix `omega = 0.5`, `rho = 0`
- 2D `(phi, rho)` slice: fix `omega = 0.5`, `theta = 0`

All use the active `[-2pi, 2pi]` angular box.

### 2.5 Phase C key question

The plan asks:

> Do the angular variables encode genuinely different object traits?

After the audit, the answer is:

- **within the native linear-basis classical runtime:** no, they remain effectively degenerate at fixed `omega`,
- **within the active exploratory symmetry-broken Phase C runtime:** yes, they produce different trait diagnostics,
- **for final stable species claims:** not yet established.

That is the actual Phase C result.

---

## 3. Final Phase C conclusions

### 3.1 The native linear-basis classical runtime is effectively angularly blind at fixed scale

**Claim:** Before the Phase C symmetry-breaking upgrade, the exact classical runtime is effectively blind to angular orientation at fixed `omega`.

**Method and rationale:** This was already the decisive outcome of the refreshed Phase B exact solver. That solver compared:

- multiple anchors,
- a full 1D `phi` slice,
- and a full 2D `(theta, rho)` slice

at fixed `omega`.

That is the right baseline test because Phase C only matters if the earlier exact runtime really failed to distinguish the angles dynamically.

**Results:** The refreshed Phase B exact solver found:

- anchor final-mass range = `8.049116928532385e-16`
- 1D exact `phi`-slice final-mass range = `8.049116928532385e-16`
- 2D exact `(theta, rho)`-slice final-mass range = `0.0`

with equally tiny curvature-observable spreads.

**Why this proves the claim:** Those spreads are effectively zero. So at fixed scale, the native linear-basis classical runtime does not turn the angular coordinates into distinct macroscopic traits.

**Supporting documents:**

- `summary/2026-03-29_phase_b_closure_summary.md`
- `notes/phase_b/phase_b_exact_radial_assessment_2026-03-29.md`
- `analysis/phase_b/phase_b_exact_radial_solver.py`
- `solutions/phase_b/phase_b_exact_radial_solver/run_summary.json`
- `solutions/phase_b/phase_b_exact_radial_solver/slice_1d_phi.csv`
- `solutions/phase_b/phase_b_exact_radial_solver/slice_2d_theta_rho.csv`
- `solutions/phase_b/phase_b_exact_radial_solver/summary.md`

---

### 3.2 Derivations 78 and 79 justify anisotropic Maurer-Cartan symmetry breaking, but the active runtime is broader than the derivation-only core

**Claim:** The Maurer-Cartan derivations provide the formal symmetry-breaking route for Phase C, but the active audited solver is an exploratory runtime that adds extra numerical and phenomenological devices beyond the minimal derivation-only term.

**Method and rationale:** Derivation 78 shows why the standard Skyrme-style commutator route fails under the strict 1D radial ansatz and introduces the anisotropic Maurer-Cartan coupling as the alternative. Derivation 79 shows how that extra term enters the Einstein trace.

The active analysis code and regenerated `summary.json` then show what was actually implemented.

**Results:** The derivation layer establishes:

- `[\omega_r, \omega_r] = 0` in the strict 1D radial setting,
- anisotropic Maurer-Cartan coupling

$$
\mathcal{L}_{MC} = g^{rr}\left(\beta_1(\omega_r^1)^2 + \beta_2(\omega_r^2)^2 + \beta_3(\omega_r^3)^2\right)
$$

as the symmetry-breaking mechanism,

- and the Einstein-trace update with the explicit extra trace contribution.

The active solver configuration then records:

- `beta = [0.01, 0.02, 0.03]`
- `metric_regularization = 1e-4`
- `angular_phi_potential = 0.01`

**Why this proves the claim:** The derivations justify the Maurer-Cartan route. The solver inspection shows that the current runtime is exploratory rather than a pure derivation-only implementation. That distinction is necessary for an accurate closure statement.

**Supporting documents:**

- `derivations/derivation_78_maurer_cartan_tensor.md`
- `derivations/derivation_79_einstein_trace_with_mc_breaking.md`
- `analysis/phase_c/phase_c_mc_radial_solver.py`
- `solutions/phase_c/phase_c_angular_traits/summary.json`
- `solutions/phase_c/phase_c_angular_traits/summary.md`
- `notes/phase_c/phase_c_corrected_mc_radial_assessment.md`

---

### 3.3 The active exploratory symmetry-broken runtime does produce distinct angular trait diagnostics

**Claim:** Within the active Phase C runtime, `theta`, `phi`, and `rho` no longer behave as equivalent channels.

**Method and rationale:** The correct test is not one favored rich seed. It is the combination of:

- representative seeded anchors,
- angle-only anchors,
- full 1D channel scans,
- and full 2D pair scans.

That separates seed-choice artifacts from persistent angular-response patterns.

**Results:** The audited outputs show a clear channel hierarchy.

Representative and angle-only anchor checks:

- `scalar` and `theta`-dominant sectors both reach the full `r_max = 20` interval with
  - final mass about `0.108039`,
  - mass half-radius `14.6501`,
  - mass 90% radius `18.9801`,
  - core mass fraction about `2.04e-4`.
- `phi`-dominant and fully mixed sectors both terminate early with
  - final mass about `1.465564`,
  - mass half-radius `2.6001`,
  - mass 90% radius `3.1601`,
  - core mass fraction about `2.78e-2`.

1D slice widths:

- `theta`: `6.069374447470466e-10`
- `rho`: `0.20494570186855265`
- `phi`: `1.9239803098587736`

2D slice widths:

- `(theta, rho)`: `0.1059810327281174`
- `(phi, theta)`: `1.0914284604307958`
- `(phi, rho)`: `1.0914284604307958`

**Why this proves the claim:** The channels now produce measurably different macroscopic diagnostics in the active runtime. The evidence is especially clear in the mass-response landscape:

- `phi` is the dominant driver,
- `rho` is a moderate standalone driver,
- `theta` is nearly flat on the audited standalone 1D slice,
- but the paired `theta-rho` sector still has nontrivial structure.

**Supporting documents:**

- `analysis/phase_c/phase_c_mc_radial_solver.py`
- `solutions/phase_c/phase_c_angular_traits/representative_seed_results.csv`
- `solutions/phase_c/phase_c_angular_traits/angle_only_anchor_results.csv`
- `solutions/phase_c/phase_c_angular_traits/slice_1d_theta.csv`
- `solutions/phase_c/phase_c_angular_traits/slice_1d_phi.csv`
- `solutions/phase_c/phase_c_angular_traits/slice_1d_rho.csv`
- `solutions/phase_c/phase_c_angular_traits/slice_2d_theta_rho.csv`
- `solutions/phase_c/phase_c_angular_traits/slice_2d_phi_theta.csv`
- `solutions/phase_c/phase_c_angular_traits/slice_2d_phi_rho.csv`
- `solutions/phase_c/phase_c_angular_traits/profiles/scalar.csv`
- `solutions/phase_c/phase_c_angular_traits/profiles/phi_dom.csv`
- `solutions/phase_c/phase_c_angular_traits/summary.json`
- `solutions/phase_c/phase_c_angular_traits/summary.md`
- `notes/phase_c/phase_c_corrected_mc_radial_assessment.md`
- `notes/phase_c/phase_c_synthesis_2026-04-02.md`

---

### 3.4 The strongest phi-rich representative states are near-horizon exploratory diagnostics, not full-domain survivors

**Claim:** The dramatic high-mass `phi`-rich representative states should not be described as full-domain settled survivors.

**Method and rationale:** The representative and angle-only anchor outputs now record:

- solver status,
- termination flag,
- final integration radius,
- horizon event radius,
- and final `2m/r`.

Those are the right diagnostics for checking whether a high-mass state actually persists across the full interval.

**Results:** Both `phi_dom` and `fully_mixed` show:

- `status = 1`
- `terminated_early = True`
- `r_final = 3.2701`
- horizon event radius about `3.27676554`
- final `2m/r` about `0.896342`

By contrast, the scalar and theta-dominant anchors reach `r_final = 19.9901` without triggering the event.

**Why this proves the claim:** The strongest phi-rich representative states are real outputs of the exploratory runtime, but they do not survive to the full outer box. So they should be interpreted as near-horizon exploratory states rather than already-established long-range stable objects.

**Supporting documents:**

- `analysis/phase_c/phase_c_mc_radial_solver.py`
- `solutions/phase_c/phase_c_angular_traits/representative_seed_results.csv`
- `solutions/phase_c/phase_c_angular_traits/angle_only_anchor_results.csv`
- `solutions/phase_c/phase_c_angular_traits/summary.json`
- `solutions/phase_c/phase_c_angular_traits/summary.md`
- `notes/phase_c/phase_c_corrected_mc_radial_assessment.md`
- `notes/phase_c/phase_c_synthesis_2026-04-02.md`

---

### 3.5 Phase C closes as an exploratory proof-of-principle trait-differentiation phase

**Claim:** Phase C is complete, but the closed claim is narrower than the earlier wording.

**Method and rationale:** A phase is closed when its roadmap question is answered at the level it was meant to answer it. Here that means:

- establishing whether angular channels can become dynamically distinct,
- and identifying the broad role pattern without pretending that the strongest high-mass sectors are already final stable species.

**Results:** The audited package now supports the following final statement:

- the native linear-basis runtime is angularly blind,
- the active exploratory Maurer-Cartan-based runtime does produce distinct angular trait diagnostics,
- `phi` is the dominant driver,
- `rho` is secondary,
- `theta` is weak on the audited standalone 1D slice,
- the strongest phi-rich representative states terminate early rather than surviving to the full outer interval.

**Why this proves the claim:** That is enough to answer the Phase C key question in the exploratory symmetry-broken setting. It is not enough to skip later persistence or identity testing, but it is enough to close Phase C honestly.

**Supporting documents:**

- `khantraction_paper.md`
- `notes/classical_exploration_plan.md`
- `summary/2026-03-29_phase_b_closure_summary.md`
- `analysis/phase_c/phase_c_mc_radial_solver.py`
- `solutions/phase_c/summary.md`
- `solutions/phase_c/phase_c_mc_equations/summary.md`
- `solutions/phase_c/phase_c_angular_traits/summary.md`
- `notes/phase_c/phase_c_corrected_mc_radial_assessment.md`
- `notes/phase_c/phase_c_synthesis_2026-04-02.md`
- `phase_c_audit_report.md`

---

## 4. What Phase C has not established

Phase C has **not** established:

- that the active runtime is the final minimal physical symmetry-broken theory,
- that the chosen `beta` weights, regularization, or phi-localized potential are physical constants,
- that the strongest phi-rich states are full-domain stable objects,
- a completed map of stable angular species,
- chirality, hosting, or persistence claims.

Those belong to later phases.

---

## 5. Why the phase is considered closed

Phase C is considered closed because its actual burden of proof has now been met in an audited form:

- the full angular comparison protocol is present,
- the active solver and outputs are traceable,
- each solution directory has interpretive summaries,
- the closure summary now states the actual method and actual caveats,
- and the key question has been answered honestly.

The answer is not "the final particle picture is complete." The answer is:

> the angular variables can produce genuinely different classical trait diagnostics once explicit symmetry-breaking machinery is introduced, with phi as the dominant driver in the audited exploratory runtime.

---

## 6. Bottom line

**Bottom line:** Phase C does not overthrow the audited Phase B result that the native linear-basis runtime is angularly blind. Instead, it shows that an exploratory Maurer-Cartan-based symmetry-broken runtime can make the angular variables dynamically visible. In that runtime, phi drives the strongest trait splitting, rho contributes a secondary standalone effect, theta is weak on the audited standalone slice, and the strongest phi-rich representative states are high-mass near-horizon terminations rather than full-domain survivors. That is a real Phase C result, and it is the one this closure summary now records.
