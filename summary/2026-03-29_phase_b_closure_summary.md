# Phase B Closure Summary — Structured Objecthood Audit

**Date:** 2026-03-29  
**Phase:** B — Structured-object picture  
**Status:** Closed after audit refresh

## 0. Project-level disposition

Phase B remains an important precursor result because static structured objecthood survives audit. Its old raw size-invariance claim is retired at the project level because the current observables remain setup-dependent. The governing synthesis is recorded in `summary/2026-04-02_gap_closure_summary.md`, `notes/2026-04-02_direct_data_closure_plan.md`, and `summary/2026-04-02_khantraction_model_conclusion.md`.

## 1. Scope and motivation

`khantraction_paper.md` does **not** present Khantraction as a finished particle theory. It presents it as a speculative toy model for localized, compact, structured spacetime-fold objects with a continuous scalar-to-quaternion branch family.

That framing determines the correct burden of proof for Phase B.

Phase B was not supposed to prove known particles. It was supposed to answer whether the full-quaternion branch can honestly be treated as a coherent structured object family with:
- a compact external profile,
- an organized interior,
- measurable concentration/size observables,
- and enough persistence to justify classical object language.

The active Phase B convention remained:
- $\omega > 0$
- $\theta,\phi,\rho \in [-2\pi,2\pi]$
- no redundancy quotienting

That framing is consistent with:
- `khantraction_paper.md`
- `notes/classical_exploration_plan.md`

---

## 2. Audit against `notes/classical_exploration_plan.md`

### 2.1 Goal 1 — Reconfirm the strongest full-quaternion branch family

**Status:** Met.

**How it was tested:** The provisional full solver runs a 117-seed scan with continuation, rich-neighborhood, and coarse-domain seeds. The closure stress test then reruns the focused 39-seed comparison set across 12 closure/setup scenarios.

**Why this proves the goal:** A branch family counts as reconfirmed only if it survives beyond one rich seed. Here the scalar-to-rich continuation remains monotone and regular, and the rich anchor sits inside a broad regular neighborhood.

### 2.2 Goal 2 — Re-express the rich branch as a structured object with compact external profile, folded/organized interior, and core/bulk structure

**Status:** Met qualitatively, but not with closure-independent dimensions.

**How it was tested:** The full solver extracts the Phase B objecthood observables directly:
- mass half-radius,
- mass 90% radius,
- curvature half-radius,
- curvature 90% radius,
- settling radius,
- core radius,
- soft-region width.

**Why this proves the goal:** Those observables are sufficient to describe a structured object picture. They show that the rich branch is not just a naked mass number. It has a measurable concentration profile and an internal core/bulk description.

### 2.3 Goal 3 — Re-evaluate concentration and size observables

**Status:** Met.

**How it was tested:** The closure stress test compares the observables across Ricci-feedback variants, amplitude changes, and outer-box changes. The exact solver then checks whether the exact trace closure changes the angular-identity story at fixed `omega`.

**Why this proves the goal:** The observables were not merely extracted once. They were tested for sensitivity and reinterpreted in light of both the stress variants and the exact closure.

### 2.4 Common slice protocol

**Status:** Met after audit refresh.

The refreshed Phase B package now includes explicit 1D and 2D slices in:
- `solutions/phase_b/phase_b_full_radial_solver/`
- `solutions/phase_b/phase_b_closure_stress_test/`
- `solutions/phase_b/phase_b_improved_dynamics/`
- `solutions/phase_b/phase_b_exact_radial_solver/`

The audited reference slices are:
- 1D: fix $\omega=0.5$, $\theta=\pi$, $\rho=\pi/2$, vary $\phi$
- 2D: fix $\omega=0.5$, $\phi=-\pi/2$, vary $(\theta,\rho)$

### 2.5 Phase B key question

The plan asks:

> Does Khantraction produce coherent compact structured objects with stable classical identity?

After the audit, the answer is:

- **coherent compact structured objects:** yes, in the broad family/objecthood sense,
- **stable classical identity in the linear angular channels:** no,
- **closure-independent size scales:** no.

That is the actual Phase B result.

---

## 3. Final Phase B conclusions

### 3.1 Khantraction supports a broad regular family of compact object-like profiles

**Claim:** The scalar-to-rich branch family is numerically real and broad enough to justify structured-object language at the family level.

**Method and rationale:** The right test for family coherence is not one rich seed. It is:
- continuation from scalar-like to rich behavior,
- local neighborhood checks around the rich anchor,
- and survival under explicit closure/setup perturbations.

That is exactly what the provisional full solver and the closure stress test do.

**Results:**
- provisional full solver: `117 / 117` successful runs, `117 / 117` regularity-ok, `0` horizons
- closure stress test: `39 / 39` successful runs in every one of `12` scenarios
- continuation mass ordering monotone in every stress-test scenario

**Why this proves the claim:** Those results show that the rich branch is not an isolated numerical accident. It sits inside a broad, regular branch family.

**Supporting documents:**
- `derivations/derivation_73_full_four_component_radial_system_fresh_start.md`
- `derivations/derivation_74_provisional_phase_b_einstein_closure_and_boundary_data.md`
- `analysis/phase_b/phase_b_full_radial_solver.py`
- `analysis/phase_b/phase_b_closure_stress_test.py`
- `solutions/phase_b/phase_b_full_radial_solver/run_summary.json`
- `solutions/phase_b/phase_b_closure_stress_test/cross_scenario_summary.json`
- `solutions/phase_b/phase_b_full_radial_solver/summary.md`
- `solutions/phase_b/phase_b_closure_stress_test/summary.md`
- `notes/phase_b/phase_b_full_radial_solver_assessment_2026-03-28.md`
- `notes/phase_b/phase_b_closure_stress_test_assessment_2026-03-28.md`
- `notes/phase_b/phase_b_structured_object_assessment_2026-03-28.md`

---

### 3.2 The rich branch supports a structured-object picture, but the measured sizes are setup-dependent

**Claim:** Phase B does justify objecthood language for the rich branch, but not closure-independent or setup-independent object radii.

**Method and rationale:** The correct way to test this claim is:
- extract the planned objecthood observables from the rich branch,
- then stress those observables under solver-side perturbations.

That separates qualitative object structure from quantitative size claims.

**Results:**

For the audited rich anchor in the baseline provisional solver:
- final mass = `0.1082188762469576`
- mass half-radius = `14.670999999999731`
- mass 90% radius = `19.00100000000017`
- Ricci half-radius = `14.28099999999974`
- Ricci 90% radius = `18.86100000000015`
- core radius = `7.8509999999998765`
- soft-region width = `20.000000000000327`

But the stress test shows strong setup sensitivity:
- rich-anchor mass shift under `amp_double` = `+0.322395146603596`
- rich-anchor mass shift under `rmax_30` = `+0.09499960482892357`
- rich-anchor mass shift under `amp_double_rmax_30` = `+0.6890033337254071`

while the tested closure-side shifts are much smaller:
- `numerical_ricci_off` = `-6.702250354304051e-06`
- `numerical_trace_half` = `-3.3513099246401667e-06`
- `numerical_trace_potential_only` = `+9.342368327558415e-08`

**Why this proves the claim:** The observables do describe a structured object, but their absolute sizes are not yet invariant physical properties. They remain strongly tied to the present finite-radius setup conventions.

**Supporting documents:**
- `analysis/phase_b/phase_b_full_radial_solver.py`
- `analysis/phase_b/phase_b_closure_stress_test.py`
- `solutions/phase_b/phase_b_full_radial_solver/run_results.csv`
- `solutions/phase_b/phase_b_full_radial_solver/slice_1d_phi.csv`
- `solutions/phase_b/phase_b_full_radial_solver/slice_2d_theta_rho.csv`
- `solutions/phase_b/phase_b_closure_stress_test/cross_scenario_summary.json`
- `solutions/phase_b/phase_b_closure_stress_test/stress_results.csv`
- `solutions/phase_b/phase_b_full_radial_solver/summary.md`
- `notes/phase_b/phase_b_structured_object_assessment_2026-03-28.md`
- `notes/phase_b/phase_b_closure_stress_test_assessment_2026-03-28.md`

---

### 3.3 The exact nonminimal trace can be decoupled explicitly and integrated on the audited anchor/slice set

**Claim:** The exact nonminimal trace closure is usable as an explicit runtime, but the support trail is narrower than the old wording implied.

**Method and rationale:** The mathematically correct route is:
1. derive the exact implicit trace equation,
2. substitute `□|q|^2 = S + 4 xi R |q|^2`,
3. solve explicitly for `R`,
4. run an exact solver on representative anchors and slices.

That is the right way to verify the Einstein-sector update without pretending that a broader exact family scan already exists.

**Results:**
- exact anchor runs: `3`
- exact 1D $\phi$ slice: `17` samples
- exact 2D $(\theta,\rho)$ slice: `81` samples
- all audited exact runs regular on this sample set

The exact solver uses the explicit denominator

$$
1 + 2\kappa\xi(1-12\xi)|q|^2.
$$

**Why this proves the claim:** The explicit decoupling is not just a symbolic suggestion anymore. It is implemented and numerically exercised on an audited anchor-and-slice set. But that is still a narrower claim than “the full exact family has been exhaustively solved.”

**Supporting documents:**
- `derivations/derivation_76_full_einstein_equations_nonminimal_coupling.md`
- `analysis/phase_b/phase_b_exact_radial_solver.py`
- `solutions/phase_b/phase_b_exact_radial_solver/run_summary.json`
- `solutions/phase_b/phase_b_exact_radial_solver/summary.md`
- `notes/phase_b/phase_b_einstein_closure_update_assessment_2026-03-29.md`
- `notes/phase_b/phase_b_exact_radial_assessment_2026-03-29.md`

---

### 3.4 Exact linear-basis dynamics are angularly degenerate at fixed scale

**Claim:** In the exact linear component basis `(a,b,c,d)`, the macroscopic observables are effectively O(4)-degenerate at fixed `omega`.

**Method and rationale:** If the linear basis really preserved distinct angular identity, then anchor comparisons and explicit 1D/2D angular slices at fixed `omega` should change final mass, concentration radii, or curvature observables.

So the exact anchor and slice checks are the right test.

**Results:**
- exact anchor final-mass range = `8.049116928532385e-16`
- exact anchor mass-half-radius range = `0.0`
- exact anchor integrated-`|R|` range = `3.209238430557093e-17`
- exact 1D $\phi$-slice final-mass range = `8.049116928532385e-16`
- exact 2D $(\theta,\rho)$-slice final-mass range = `0.0`

**Why this proves the claim:** Those spreads are at or below floating-point noise. On the audited exact sample set, the linear-basis observables do not resolve angular orientation at fixed scale.

**Supporting documents:**
- `analysis/phase_b/phase_b_exact_radial_solver.py`
- `solutions/phase_b/phase_b_exact_radial_solver/run_summary.json`
- `solutions/phase_b/phase_b_exact_radial_solver/slice_1d_phi.csv`
- `solutions/phase_b/phase_b_exact_radial_solver/slice_2d_theta_rho.csv`
- `solutions/phase_b/phase_b_exact_radial_solver/profiles/scalar_anchor.csv`
- `solutions/phase_b/phase_b_exact_radial_solver/profiles/rich_anchor_1.csv`
- `solutions/phase_b/phase_b_exact_radial_solver/profiles/rich_anchor_2.csv`
- `solutions/phase_b/phase_b_exact_radial_solver/summary.md`
- `notes/phase_b/phase_b_exact_radial_assessment_2026-03-29.md`

---

### 3.5 The exploratory ordered-runtime differentiation is real, but it is not the core proof of Phase B

**Claim:** The improved ordered-runtime study is useful evidence about where angular differentiation may enter, but it is exploratory and cannot carry the main closure claim by itself.

**Method and rationale:** The right comparison is:
- component baseline,
- pure pullback ordered baseline,
- exploratory directional runtime,

run on the same seed set and now also checked against explicit slices.

**Results:**
- component baseline rich-neighborhood mass spread = `7.494005416219807e-16`
- baseline pullback rich-neighborhood mass spread = `0.0`
- exploratory directional rich-neighborhood mass spread = `0.0018439538403206834`
- exploratory 1D $\phi$-slice mass range = `[0.1082188762467994, 0.12553663276310717]`
- exploratory 2D $(\theta,\rho)$-slice mass range = `[0.1082188762467994, 0.1082188762467994]`

**Why this matters:** The improvement is real, but it is $\phi$-localized on the audited slice protocol and still depends on explicitly exploratory directional terms. So it is a useful handoff clue, not a replacement for the exact closure result.

**Supporting documents:**
- `derivations/derivation_75_ordered_pullback_and_exploratory_directional_phase_b_runtime.md`
- `analysis/phase_b/phase_b_improved_dynamics_solver.py`
- `solutions/phase_b/phase_b_improved_dynamics/comparison_summary.json`
- `solutions/phase_b/phase_b_improved_dynamics/summary.md`
- `solutions/phase_b/phase_b_improved_dynamics/exploratory_directional/run_summary.json`
- `solutions/phase_b/phase_b_improved_dynamics/exploratory_directional/slice_1d_phi.csv`
- `solutions/phase_b/phase_b_improved_dynamics/exploratory_directional/slice_2d_theta_rho.csv`
- `notes/phase_b/phase_b_improved_dynamics_assessment_2026-03-28.md`

---

## 4. What Phase B has *not* established

Phase B has **not** established:
- a unique asymptotically matched boundary-value family,
- closure-independent physical radii,
- stable angularly distinct classical identities in the linear basis,
- or particle/species claims beyond structured-object language.

It has also **not** proved that the exploratory ordered-runtime directional terms are the final correct theory. They remain exploratory.

---

## 5. Why the phase is considered closed

Phase B is considered closed because its central question has been answered at the right level:

1. **Objecthood:** yes, Khantraction supports a broad family of regular compact structured-object profiles.
2. **Quantitative size invariance:** no, the present sizes remain setup-dependent.
3. **Stable angular identity in the linear basis:** no, the exact solver shows effective O(4) degeneracy at fixed scale.

That means further Phase B work inside the same linear-basis objecthood framework would mostly repeat the same conclusions:
- broad family coherence,
- setup-sensitive sizes,
- angular degeneracy.

The next real theoretical leverage lies beyond that.

---

## 6. Bottom line

**Bottom line:** Phase B successfully rebuilt the structured-object picture at the broad family level. The refreshed evidence chain shows that Khantraction supports regular compact profiles with measurable core/bulk observables and a continuous scalar-to-rich family. It also shows that those sizes are still setup-dependent and that exact linear-basis dynamics erase angular identity at fixed scale. So the honest Phase B closure is: objecthood survives, quantitative size invariance does not yet survive, and linear-basis angular identity fails.
