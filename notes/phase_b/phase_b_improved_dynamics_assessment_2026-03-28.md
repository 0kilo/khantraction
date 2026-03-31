# Phase B Assessment — Improved Dynamics Runtime

**Date:** 2026-03-28  
**Phase:** B — Structured-object picture  
**Status:** Improved runtime implemented and compared against current baseline

## Purpose

This note records the first serious attempt to reduce the Phase B runtime’s angular degeneracy without pretending to have derived a final new theory.

The current component solver is real, but the stress test showed that it is almost completely degenerate across rich angular neighborhoods at fixed `omega`.
So the goal here was:

1. keep a clean baseline,
2. add the most honest next geometry-motivated upgrade the existing materials support,
3. run actual comparisons on the stressed seed sets,
4. check whether angular-sector differentiation improves while continuation-family regularity survives.

Outputs are in:
- `solutions/phase_b/phase_b_improved_dynamics/baseline_pullback/`
- `solutions/phase_b/phase_b_improved_dynamics/exploratory_directional/`
- `solutions/phase_b/phase_b_improved_dynamics/comparison_summary.json`
- `solutions/phase_b/phase_b_improved_dynamics/summary.md`

---

## 1. What was implemented

## 1.1 Conservative ordered baseline: `baseline_pullback`

A new solver was written in ordered variables
\[
(w,\theta,\phi,\rho),
\qquad w = \log(0.02)+\omega,
\]
using the exact pullback metric induced by the ordered quaternion map.

That means the runtime now uses the project’s own ordered-state geometry rather than collapsing everything back into purely component-norm evolution.

This mode is deliberately conservative:
- same norm potential,
- same provisional Einstein trace closure,
- same seeded families,
- but kinetic evolution and stress bookkeeping are done in ordered coordinates.

## 1.2 Exploratory directional upgrade: `exploratory_directional`

A second mode adds a small explicitly labeled angular potential built from the project’s own ordered-map invariants:
- `sin^2(2 phi)` / `cos(2 phi)` from the Jacobian-singularity structure,
- `theta-rho` pairing from the pullback angular metric.

Tested exploratory parameters:
- `angular_eta = 0.02`
- `angular_zeta = 0.015`

This is **not** claimed as final derived physics.
It is an exploratory closure meant to test whether the project’s own anisotropic ordered geometry can begin to produce nontrivial angular-sector differentiation.

## 1.3 Necessary coordinate regularization

Because the ordered pullback metric is singular on the known `phi` slices
\[
\cos(2\phi)=0,
\]
the ordered inverse metric was regularized with a small numerical floor
- `phi_regularization = 1e-3`

This is not a physical claim.
It is a coordinate-side numerical regularization so the continuation path can pass through the known midpoint singular slice without fake runtime collapse.

---

## 2. What ran successfully

The improved solver lives in:
- `analysis/phase_b/phase_b_improved_dynamics_solver.py`

It ran on the same focused 39-seed comparison set used by the earlier stress test:
- 9 continuation seeds,
- 27 rich-neighborhood seeds,
- 3 coarse scalar-like references.

### 2.1 Baseline component reference

From the pre-existing component solver / stress-test baseline:
- rich-neighborhood mass spread: `7.494005416219807e-16`
- rich-neighborhood integrated-`|R|` spread: `3.2959746043559335e-17`

That is effectively total angular degeneracy.

### 2.2 Baseline ordered pullback mode

From `solutions/phase_b/phase_b_improved_dynamics/baseline_pullback/run_summary.json`:
- seed count: `39`
- success count: `39`
- regularity-ok count: `39`
- horizon hits: `0`
- continuation final mass monotone: `true`
- rich-neighborhood mass spread: `0.0`
- rich-neighborhood integrated-`|R|` spread: `0.0`
- rich-neighborhood max angle shifts: all `0.0`

So simply rewriting the runtime in ordered variables did **not** by itself produce angular differentiation.
That is an important negative result.

### 2.3 Exploratory directional mode

From `solutions/phase_b/phase_b_improved_dynamics/exploratory_directional/run_summary.json`:
- seed count: `39`
- success count: `39`
- regularity-ok count: `39`
- horizon hits: `0`
- continuation final mass monotone: `true`
- rich-neighborhood mass spread: `0.0018439538403206834`
- rich-neighborhood integrated-`|R|` spread: `0.0016244217122699453`
- rich-neighborhood max `theta` shift: `0.017140994059472447`
- rich-neighborhood max `phi` shift: `0.23760581262518055`
- rich-neighborhood max `rho` shift: `0.017140994059465786`

So the exploratory mode does produce genuine angle-sensitive runtime differences while preserving clean completion and monotone continuation mass ordering on the tested family.

---

## 3. Main comparison result

The comparison summary reports:

- component baseline rich-neighborhood mass spread:
  `7.494005416219807e-16`
- exploratory directional rich-neighborhood mass spread:
  `0.0018439538403206834`

- component baseline rich-neighborhood integrated-`|R|` spread:
  `3.2959746043559335e-17`
- exploratory directional rich-neighborhood integrated-`|R|` spread:
  `0.0016244217122699453`

So on the tested seed set, the exploratory mode increased the rich-neighborhood spread by many orders of magnitude relative to the component baseline.

Just as importantly:
- the baseline pullback mode stayed exactly degenerate,
- so the differentiation is not coming from mere coordinate relabeling,
- it is coming from the explicitly identified exploratory directional couplings.

That makes the comparison honest.

---

## 4. Did angular differentiation improve?

Yes — **in the exploratory directional mode, clearly**.

But the right statement is careful:

> the improved runtime begins to resolve angular-sector differences in Phase B observables, and it does so while preserving regular completion and monotone continuation ordering on the tested seeds.

What this does **not** yet justify saying is:
- that the angular sectors are already physically validated distinct species,
- that the directional potential is uniquely derived,
- or that the resulting differentiation is closure-independent.

The improvement is real, but still exploratory.

---

## 5. What survived and what did not

## 5.1 Survived

- all 39 seeds completed successfully in both ordered modes after adding the explicit `phi`-slice regularization,
- no horizons were triggered,
- continuation mass ordering stayed monotone,
- the exploratory directional mode produced visible internal angle evolution along continuation seeds,
- rich-neighborhood seeds stopped being numerically collapsed in the main observables.

## 5.2 Did not survive / important negative finding

- the pure ordered pullback baseline did **not** reduce degeneracy at all,
- so the ordered kinetic metric alone is too weak to resolve sectors in this current setup,
- the new differentiation therefore depends on the exploratory directional potential rather than on the baseline pullback geometry by itself.

That distinction matters and should be preserved.

---

## 6. Current best interpretation

The best restrained statement is:

> The current component-norm Phase B runtime is too symmetric to resolve rich angular sectors. Moving to ordered variables alone still leaves the runtime degenerate on the tested seeds. But adding a small explicitly labeled directional potential built from the project’s own ordered-map invariants produces nontrivial angular-sector differentiation while preserving family regularity and monotone continuation behavior on the tested seed set.

That is a meaningful runtime improvement.
It is also still provisional.

---

## 7. Remaining limitations

1. **Directional potential is exploratory.**  
   It is motivated by the project’s own geometry, but not yet derived from a settled action principle.

2. **Einstein closure is still provisional.**  
   The improved runtime reuses the same trace-style closure logic as the existing Phase B solver.

3. **Coordinate singularity handling is numerical, not physical.**  
   The `phi_regularization` floor is necessary for runtime continuity across known Jacobian-singular slices, but it is a solver device.

4. **Angular differentiation is demonstrated only on the tested seed families.**  
   It still needs broader scans and sensitivity checks in the improved runtime itself.

5. **No claim of particle/species recovery yet.**  
   The result is only that the solver can now begin to distinguish sectors honestly in its observables.

---

## 8. Exact files created / updated in this step

Created:
- `derivations/derivation_75_ordered_pullback_and_exploratory_directional_phase_b_runtime.md`
- `analysis/phase_b/phase_b_improved_dynamics_solver.py`
- `notes/phase_b/phase_b_improved_dynamics_assessment_2026-03-28.md`
- `solutions/phase_b/phase_b_improved_dynamics/comparison_summary.json`
- `solutions/phase_b/phase_b_improved_dynamics/summary.md`
- `solutions/phase_b/phase_b_improved_dynamics/baseline_pullback/run_summary.json`
- `solutions/phase_b/phase_b_improved_dynamics/baseline_pullback/run_results.csv`
- `solutions/phase_b/phase_b_improved_dynamics/exploratory_directional/run_summary.json`
- `solutions/phase_b/phase_b_improved_dynamics/exploratory_directional/run_results.csv`
- profile CSV outputs under both improved-runtime subdirectories

Still unchanged intentionally:
- `analysis/phase_b/phase_b_full_radial_solver.py`
- prior baseline/stress-test notes and outputs

---

## 9. Bottom line

**Bottom line:** a real improved Phase B runtime now exists. The conservative ordered-pullback baseline showed that coordinate rewriting alone does not fix the degeneracy. The exploratory directional upgrade, however, produced clear rich-neighborhood mass/curvature splitting while keeping all tested seeds regular and preserving monotone continuation ordering. So the project now has an honest next runtime that begins to resolve angular-sector differences — but it does so through explicitly labeled exploratory directional couplings, not through a fully derived final closure.
