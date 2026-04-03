# Phase B Assessment — Exact Radial Solver and Linear-Basis Degeneracy

**Date:** 2026-03-29  
**Phase:** B — Structured-object picture  
**Status:** Complete after audit refresh

## Purpose

This note evaluates what the refreshed exact radial solver actually proves.

Relevant files:
- `analysis/phase_b/phase_b_exact_radial_solver.py`
- `solutions/phase_b/phase_b_exact_radial_solver/run_summary.json`
- `solutions/phase_b/phase_b_exact_radial_solver/summary.md`
- `solutions/phase_b/phase_b_exact_radial_solver/slice_1d_phi.csv`
- `solutions/phase_b/phase_b_exact_radial_solver/slice_2d_theta_rho.csv`

---

## 1. What was tested

The refreshed exact solver now checks three separate things:

1. **Anchor comparison**
   - scalar-like anchor,
   - rich angular anchor 1,
   - rich angular anchor 2.
2. **1D slice protocol**
   - fix $\omega=0.5$, $\theta=\pi$, $\rho=\pi/2$,
   - vary $\phi$ on `[-2pi, 2pi]`.
3. **2D slice protocol**
   - fix $\omega=0.5$, $\phi=-pi/2$,
   - vary $(\theta,\rho)$ on `[-2pi, 2pi]^2`.

This is materially stronger than the earlier three-anchor-only check.

---

## 2. Exact-closure runtime result

All tested exact-solver runs completed regularly on the audited sample set.

Anchor values:
- final mass: `0.1081724783796303`, `0.1081724783796303`, `0.1081724783796295`
- mass half-radius: `14.670099999999731` for all three anchors
- mass 90% radius: `19.000100000000174` for all three anchors
- integrated `|R|`: `0.006919589880281697`, `0.006919589880281697`, `0.006919589880281665`

So the exact solver reproduces the same broad objecthood picture as the provisional solver: regular compact profiles exist.

---

## 3. What the exact solver proves about angular identity

The anchor spreads are already tiny:
- final-mass range = `8.049116928532385e-16`
- integrated-`|R|` range = `3.209238430557093e-17`

The explicit slices then confirm that this is not an accident of anchor choice:
- 1D exact $\phi$-slice final-mass range = `8.049116928532385e-16`
- 1D exact $\phi$-slice integrated-`|R|` range = `3.2959746043559335e-17`
- 2D exact $(\theta,\rho)$-slice final-mass range = `0.0`
- 2D exact $(\theta,\rho)$-slice integrated-`|R|` range = `0.0`

That means the exact linear-basis runtime is, for practical purposes, perfectly blind to angular orientation at fixed scale.

---

## 4. Correct interpretation

The right conclusion is narrower than the older wording:

> the exact solver does not prove that all future angular formulations must be degenerate; it proves that the *current linear component basis* keeps the exact classical observables O(4)-symmetric on the tested Phase B sample set.

That distinction matters.

The exact solver therefore supports two statements simultaneously:
- the exact trace decoupling is numerically workable,
- the linear $(a,b,c,d)$ basis is not the right place to look for stable angular identity.

---

## 5. Bottom line

**Bottom line:** the refreshed exact radial solver confirms that regular exact-closure objects exist, but it also shows that the linear-basis observables are angularly degenerate across both anchors and explicit 1D/2D slices at fixed `omega`. So the exact solver strengthens the Einstein-sector bookkeeping and weakens any remaining claim that Phase B could recover distinct angular identities without leaving the linear basis.
