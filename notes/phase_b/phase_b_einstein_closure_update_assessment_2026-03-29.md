# Phase B Assessment — Einstein Closure Update

**Date:** 2026-03-29  
**Phase:** B — Structured-object picture  
**Status:** Exact decoupling implemented and audited

## Purpose

This note records the audited status of the nonminimal Einstein-sector closure for the Phase B model.

The relevant support chain is:
- `derivations/derivation_76_full_einstein_equations_nonminimal_coupling.md`
- `analysis/phase_b/phase_b_exact_radial_solver.py`
- `solutions/phase_b/phase_b_exact_radial_solver/run_summary.json`
- `solutions/phase_b/phase_b_exact_radial_solver/summary.md`

---

## 1. What Derivation 76 established

Derivation 76 correctly identified the exact implicit trace equation,

$$
R=\frac{-\kappa T^{(q)}+6\kappa\xi \square |q|^2}{1+2\kappa\xi |q|^2},
$$

and also made the main conceptual correction to the earlier provisional closure:

> the $\xi R|q|^2$ model does not reduce exactly to the naive `R = -\kappa T` trace closure.

That derivation was the necessary starting point.

---

## 2. The audited algebraic completion used by the exact solver

The exact solver completes the remaining explicit decoupling step by substituting

$$
\square |q|^2 = S + 4\xi R |q|^2
$$

back into the trace equation, where

$$
S = 2 e^{-2\Lambda}\sum_A q_A'^2 - 2(m_{\mathrm{glue}}^2 + \lambda_q |q|^2)|q|^2.
$$

That yields the explicit denominator

$$
1 + 2\kappa\xi(1-12\xi)|q|^2,
$$

which is the form implemented in
`analysis/phase_b/phase_b_exact_radial_solver.py`.

So the support chain is now:
- implicit exact trace formula from Derivation 76,
- explicit decoupling step recorded in the exact-solver implementation,
- numerical confirmation from the regenerated exact-solver outputs.

---

## 3. What the exact closure check actually validated

The refreshed exact solver integrates successfully for:
- 3 anchor seeds,
- a 17-point 1D $\phi$ slice,
- and an 81-point 2D $(\theta,\rho)$ slice,

all at fixed `omega = 0.5`.

From `solutions/phase_b/phase_b_exact_radial_solver/run_summary.json`:
- anchor final-mass range: `8.049116928532385e-16`
- anchor mass-half-radius range: `0.0`
- anchor integrated-`|R|` range: `3.209238430557093e-17`
- 1D exact $\phi$-slice final-mass range: `8.049116928532385e-16`
- 2D exact $(\theta,\rho)$-slice final-mass range: `0.0`

So the exact solver does validate the explicit decoupled trace formula on the tested sample set.

---

## 4. What this did *not* establish

This update did **not** prove:
- a full asymptotic boundary-value solution theory,
- a closure-independent compactness scale,
- or dynamically distinct angular identities in the linear basis.

In fact, the exact closure check made the opposite identity result much sharper:

> once the exact trace is used in the linear component basis, the runtime remains effectively O(4)-degenerate at fixed scale.

So the exact closure update tightened the Einstein-sector story, but it also removed any hope that the linear basis itself was hiding a rich angular identity structure.

---

## 5. Bottom line

**Bottom line:** the Phase B exact-closure update is now complete in the narrow audited sense that matters for the closure summary. Derivation 76 supplied the exact implicit trace equation, the exact solver completed the remaining algebraic decoupling step, and the regenerated anchor and slice outputs confirm that the explicit solver integrates stably on the tested sample set. The result strengthens the gravity-sector bookkeeping while simultaneously confirming that exact linear-basis dynamics remain angularly degenerate.
