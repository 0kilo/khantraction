# Phase B Assessment — Closure and Boundary Stress Test

**Date:** 2026-03-28  
**Phase:** B — Structured-object picture  
**Status:** Stress test implemented and run; findings remain closure-provisional

## Purpose

This note records a genuine stress test of the fresh-tree Phase B full radial runtime in
`analysis/phase_b/phase_b_full_radial_solver.py`.

The goal was not to invent new physically justified Einstein closures out of thin air.
It was to perturb the current provisional runtime in clearly labeled **numerical stress variants** and test which parts of the current family-coherence / compactness story survive.

Generated outputs are in:
- `solutions/phase_b/phase_b_closure_stress_test/stress_results.csv`
- `solutions/phase_b/phase_b_closure_stress_test/scenario_summaries.json`
- `solutions/phase_b/phase_b_closure_stress_test/cross_scenario_summary.json`
- `solutions/phase_b/phase_b_closure_stress_test/summary.md`

---

## 1. What was tested

The stress harness lives in:
- `analysis/phase_b/phase_b_closure_stress_test.py`
- `scripts/run_phase_b_closure_stress_test.sh`

It ran **12 scenarios** on a focused seed set of **39 seeds**:
- 9 scalar-to-rich continuation seeds
- 27 rich-anchor neighborhood seeds
- 3 coarse scalar-like reference seeds at `omega = 0.1, 0.35, 0.75`

### 1.1 Closure-side numerical stress variants

These are solver-side comparison variants only, not validated physics.

1. `minimal_trace` (baseline)
2. `numerical_ricci_off`
   - turns Ricci feedback off in the matter operator
3. `numerical_trace_half`
   - halves the baseline Ricci feedback
4. `numerical_trace_potential_only`
   - uses only the potential part in the Ricci feedback estimate

### 1.2 Setup / boundary sensitivity variants

1. Central amplitude base:
   - baseline `0.02`
   - half `0.01`
   - double `0.04`
2. Outer radius:
   - `r_max = 15`
   - `r_max = 20`
   - `r_max = 30`
3. Decay target:
   - `0.03`
   - `0.05`
   - `0.08`
4. Combined stress:
   - `amp_double_rmax_30`
   - `ricci_off_amp_double`

---

## 2. What ran successfully

Across all 12 scenarios and all 39 tested seeds per scenario:
- success count: **39 / 39** in every scenario
- regularity-ok count: **39 / 39** in every scenario
- horizon hits: **0** in every scenario
- field/mass blowups: **0** in every scenario

So the current runtime is numerically stable on this tested neighborhood, even under the closure/setup perturbations above.

---

## 3. What robustly survived

## 3.1 Scalar-to-rich continuation stayed coherent

For every tested scenario,
- continuation final mass remained monotone along the 9-point scalar-to-rich ordered path
- the integration stayed regular without horizons or blowups

This is the strongest solver-side robustness result from the stress test.

Baseline example (`minimal_trace`, `A0 = 0.02`, `r_max = 20`):
- scalar anchor final mass: `0.059437562855148535`
- rich anchor final mass: `0.1082188762469576`
- continuation mass range: `0.048781313391809064`

This monotone ordering also survived all tested closure-side perturbations.

### Closure dependence of the continuation mass was small

Relative to the baseline rich anchor mass `0.1082188762469576`:
- `numerical_ricci_off`: shift `-6.702250354304051e-06`
- `numerical_trace_half`: shift `-3.3513099246401667e-06`
- `numerical_trace_potential_only`: shift `+9.342368327558415e-08`

So for this tested seed set, the coarse continuation ordering is **much less sensitive to these Ricci-feedback perturbations than to setup choices like central amplitude or box size**.

## 3.2 Rich-neighborhood regularity survived

The 27-seed neighborhood around the rich anchor remained regular in every scenario.
No neighborhood point triggered horizon formation or blowup.

So the rich sector is not a numerically isolated special point in the current runtime.

---

## 4. What turned out to be fragile or misleading

## 4.1 The current solver almost completely collapses angular-sector distinctions

This is the most important stress-test finding.

In the baseline scenario, for the 27 rich-neighborhood seeds at fixed `omega = 0.5`:
- rich-neighborhood final-mass range: `7.494005416219807e-16`
- rich-neighborhood integrated-`|R|` range: `3.2959746043559335e-17`

Across **all** 12 scenarios, the largest rich-neighborhood final-mass range was only:
- `9.43689570931383e-15`

That is essentially numerical degeneracy.

The same pattern appears in the omega-bucket summary:
- at `omega = 0.5`, 28 seeds with different `(theta, phi, rho)` gave baseline final-mass spread only `~7.5e-16`
- baseline integrated-`|R|` spread in that same bucket was only `~3.3e-17`

So under the present norm-symmetric closure/runtime,
**family coherence survives — but mostly because the solver is nearly blind to angular distinctions in these observables.**

That is a robustness result and a limitation at the same time.

It means the current Phase B solver does support a broad coherent family, but it does **not** currently provide strong evidence that different rich angular sectors are dynamically distinct structured objects.

## 4.2 Peak imaginary/real ratio is not a robust richness discriminator by itself

The rich-neighborhood peak imaginary-to-real ratio had huge spreads, for example in baseline:
- min: `3.2807277833778428`
- max: `32974425414.002563`

But the mass and curvature observables were simultaneously almost exactly degenerate.
So the enormous ratio spikes are largely produced by the real component crossing near zero, not by a correspondingly large change in the whole object profile.

Therefore this ratio should not be used alone as a decisive structured-object discriminator.

## 4.3 Compactness-style numbers are much more sensitive to setup than to closure toggles

Rich-anchor final mass shifts versus baseline:
- `amp_half`: `-0.08112954497619859`
- `amp_double`: `+0.322395146603596`
- `rmax_15`: `-0.05107237489513319`
- `rmax_30`: `+0.09499960482892357`
- `amp_double_rmax_30`: `+0.6890033337254071`

Compare those with the closure-side shifts:
- `numerical_ricci_off`: `-6.702250354304051e-06`
- `numerical_trace_half`: `-3.3513099246401667e-06`
- `numerical_trace_potential_only`: `+9.342368327558415e-08`

So in the current runtime,
**central amplitude scaling and finite box size dominate the measured mass/compactness shifts far more than the tested closure perturbations do.**

That means the present compactness/objecthood story is still strongly tied to solver setup conventions.

---

## 5. Boundary and decay sensitivity

All tested scenarios passed the finite-radius decay check on this seed set, including:
- `decay_target = 0.03`
- `decay_target = 0.05`
- `decay_target = 0.08`

This happened because the actual outer-boundary residuals were already comfortably below even the tighter threshold in the tested runs.
For example, baseline continuation boundary `|q|` residuals ranged only from:
- `0.011066977174830628` to `0.01489634712144958`

Extending `r_max` from `20` to `30` reduced the rich-anchor boundary residual from:
- `0.01489634712144958` to `0.0014034112032649615`

So the finite-radius decay bookkeeping is stable on this test set, but the resulting mass/curvature integrals still move with `r_max`, meaning true compactness claims remain box-sensitive.

One subtle warning sign did appear in the combined `amp_double_rmax_30` scenario:
- continuation mass remained monotone
- but continuation boundary `|q|` monotonicity no longer held exactly

That is not a failure of regularity, but it is a hint that setup-driven ordering statements are weaker than the mass ordering statement.

---

## 6. Overall interpretation

The current stress test supports the following restrained statement.

### 6.1 What looks genuinely robust in the present solver

- A regular scalar-to-rich continuation family exists in the tested Phase B runtime.
- That family remains regular under the tested Ricci-feedback stress variants.
- The rich anchor sits inside a broad regular neighborhood rather than a fragile isolated point.
- The continuation mass ordering is robust on the tested seed set.

### 6.2 What does **not** look robustly established yet

- Distinct angular-sector structured-object identity is **not** strongly supported by the present solver observables.
- The current solver’s family coherence is driven largely by norm symmetry, which collapses many angle differences at fixed `omega`.
- Compactness-style observables depend much more strongly on central amplitude and outer box size than on the tested closure perturbations.
- Therefore current objecthood/compactness conclusions are still provisional to setup conventions as well as closure choice.

---

## 7. Bottom line

**Bottom line:** the Phase B full radial solver survives a real closure/setup stress test without numerical breakdown, and the scalar-to-rich continuation family remains coherent and monotone across all tested scenarios. But the same stress test shows that the current runtime is almost completely degenerate across rich angular neighborhoods at fixed `omega`, so the present family-coherence story is robust mainly at the level of a broad norm-controlled family, not at the level of sharply resolved angular-sector structured-object differentiation. Closure-side Ricci perturbations changed the tested mass observables only weakly, while central amplitude base and outer-radius choices changed them substantially. So the current structured-object picture survives as a provisional broad-family statement, but its finer identity/compactness interpretation remains strongly setup-dependent and still provisional.
