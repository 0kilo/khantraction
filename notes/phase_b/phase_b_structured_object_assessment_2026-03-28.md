# Phase B Assessment — Structured Objecthood

**Date:** 2026-03-28  
**Phase:** B — Structured-object picture  
**Status:** Complete after audit refresh

## Purpose

This note records the audited answer to the core Phase B question from `notes/classical_exploration_plan.md`:

> Does Khantraction produce coherent compact structured objects with stable classical identity?

The answer is now specific:

- **broad objecthood:** yes, at the level of a regular scalar-to-rich family of compact profiles,
- **closure-independent size claims:** no,
- **stable angular identity in the linear basis:** no.

---

## 1. Goal-by-goal audit against the Phase B plan

### 1.1 Goal 1 — Reconfirm the strongest full-quaternion branch family

**Status:** Met.

The full provisional solver (`analysis/phase_b/phase_b_full_radial_solver.py`) completed:
- 117 / 117 seeded runs successfully,
- 117 / 117 regularity checks,
- 0 horizons,
- a monotone 9-point scalar-to-rich continuation track.

The closure stress test (`analysis/phase_b/phase_b_closure_stress_test.py`) then showed that this continuation ordering survives all 12 tested closure/setup scenarios on the focused 39-seed comparison set.

So the rich branch is not an isolated numerical seed. It sits inside a broad regular family.

### 1.2 Goal 2 — Re-express the rich branch as a structured object with compact external profile and organized interior

**Status:** Met qualitatively, but not with closure-independent dimensions.

The full solver now extracts exactly the Phase B objecthood observables listed in the plan:
- mass half-radius,
- mass 90% radius,
- curvature half-radius,
- curvature 90% radius,
- settling radius,
- core radius,
- soft-region width.

For the audited rich anchor (`continuation_08` / `rich_nbhd_13`) in the provisional baseline runtime:
- final mass = `0.1082188762469576`
- mass half-radius = `14.670999999999731`
- mass 90% radius = `19.00100000000017`
- Ricci half-radius = `14.28099999999974`
- Ricci 90% radius = `18.86100000000015`
- core radius = `7.8509999999998765`
- soft-region width = `20.000000000000327`

That is enough to describe a compact external profile plus an internal core/bulk picture.

What failed is stronger uniqueness: these dimensions move substantially when the setup changes.

### 1.3 Goal 3 — Re-evaluate concentration and size observables

**Status:** Met.

The closure stress test showed that the concentration observables are numerically real but strongly setup-dependent:
- rich-anchor mass shift under `amp_double`: `+0.322395146603596`
- rich-anchor mass shift under `rmax_30`: `+0.09499960482892357`
- rich-anchor mass shift under `amp_double_rmax_30`: `+0.6890033337254071`

By contrast, the tested closure-side perturbations changed the same rich-anchor mass only by:
- `numerical_ricci_off`: `-6.702250354304051e-06`
- `numerical_trace_half`: `-3.3513099246401667e-06`
- `numerical_trace_potential_only`: `+9.342368327558415e-08`

So the observables were re-evaluated successfully, and the result is that their quantitative values depend much more on setup conventions than on the tested Ricci-feedback toggles.

---

## 2. What the refreshed slice protocol adds

The audited Phase B solution package now includes explicit 1D and 2D slices in the active domain:
- provisional full solver slices,
- representative stress-test scenario slices,
- improved-runtime mode slices,
- exact-solver slices.

These slice outputs sharpen the interpretation:

1. In the baseline full solver, both the 1D $\phi$ slice and the 2D $(\theta,\rho)$ slice are effectively degenerate at fixed $\omega$.
2. In the exact linear-basis solver, that degeneracy survives unchanged to floating-point precision.
3. In the exploratory ordered-runtime solver, the visible splitting appears in the 1D $\phi$ slice, while the audited 2D $(\theta,\rho)$ slice at fixed $\phi=-\pi/2$ remains degenerate.

So the only audited sign of angle-sensitive splitting in Phase B is exploratory and strongly $\phi$-localized.

---

## 3. Stable classical identity: what Phase B did and did not establish

Phase B **did** establish:
- a regular family of compact object-like profiles,
- a scalar-to-rich continuation family,
- and a reproducible set of objecthood observables.

Phase B did **not** establish:
- closure-independent object radii,
- angularly distinct stable classical identities in the linear $(a,b,c,d)$ basis,
- or a unique boundary-value selection principle.

The exact solver makes the main identity limitation explicit:
- anchor final-mass spread = `8.049116928532385e-16`
- anchor integrated-`|R|` spread = `3.209238430557093e-17`
- 1D exact $\phi$-slice final-mass spread = `8.049116928532385e-16`
- 2D exact $(\theta,\rho)$-slice final-mass spread = `0.0`

That is effectively exact angular degeneracy in the linear basis.

---

## 4. Best audited interpretation

The strongest defensible Phase B statement is:

> Khantraction supports a broad regular family of compact structured-object profiles, and the rich/full-quaternion branch is a real member of that family. But the physically interesting quantitative sizes remain setup-dependent in the present runtime package, and the exact linear-basis equations collapse angular identity into an O(4)-symmetric norm sector.

That is more restrained than the older summary language, but it is fully supported.

---

## 5. Bottom line

**Bottom line:** Phase B succeeds as an objecthood phase, not as an angular-identity phase. It confirms that the scalar-to-rich branch family produces coherent compact structured-object profiles with measurable core/bulk observables. It also shows that those sizes are still setup-dependent and that exact linear-basis dynamics erase angular identity at fixed scale. That is enough to close Phase B honestly and to justify the later pivot away from the linear basis for distinct-trait work.
