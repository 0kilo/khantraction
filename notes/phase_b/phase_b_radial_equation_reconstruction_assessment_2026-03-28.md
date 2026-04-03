# Phase B Assessment — Radial Equation Reconstruction

**Date:** 2026-03-28  
**Phase:** B — Structured-object picture  
**Status:** Complete after audit refresh

## Purpose

This note records what the fresh-tree Phase B reconstruction actually established at the equation level, and what it did not.

The relevant files are:
- `derivations/derivation_73_full_four_component_radial_system_fresh_start.md`
- `analysis/phase_b/phase_b_radial_equation_structure.py`
- `solutions/phase_b/phase_b_radial_equation_structure/report.json`
- `solutions/phase_b/phase_b_radial_equation_structure/summary.md`

---

## 1. What is genuinely reconstructed

The fresh tree now has an explicit four-component matter-side radial system for

$$
q(r)=a(r)+b(r)i+c(r)j+d(r)k,
\qquad
|q|^2=a^2+b^2+c^2+d^2.
$$

Each component obeys the same radial operator,

$$
q_A''+\left(\frac{2}{r}+\Phi'-\Lambda'\right)q_A'
+ e^{2\Lambda}\Big(m_{\mathrm{glue}}^2+\lambda_q|q|^2-2\xi R\Big)q_A=0,
$$

so the matter system is component-symmetric and coupled only through the shared norm, the curvature scalar, and the metric functions.

That is the key Phase B reconstruction fact:

> the bare matter equations do not privilege one component or one ordered angle over another.

---

## 2. What the reconstruction note now contributes to the audited Phase B package

The refreshed structure report now does two things:

1. records the active unquotiented domain used throughout the audited Phase B work,
   - $\omega > 0$
   - $\theta,\phi,\rho \in [-2\pi,2\pi]$
   - no redundancy quotienting
2. records the slice-protocol anchors used by the refreshed runtime studies,
   - 1D slice: fix $\omega=0.5$, $\theta=\pi$, $\rho=\pi/2$, vary $\phi$
   - 2D slice: fix $\omega=0.5$, $\phi=-\pi/2$, vary $\theta,\rho$

So this note is no longer just a scaffold. It now supplies the structural and protocol reference point for the later Phase B runtime evidence.

---

## 3. What remained missing at this stage

This reconstruction alone did **not** supply:
- the Einstein-sector closure,
- the explicit decoupled Ricci formula,
- the regular-origin and asymptotic runtime choices,
- or the observable extraction formulas used in the later objecthood studies.

Those were added later through:
- `derivations/derivation_74_provisional_phase_b_einstein_closure_and_boundary_data.md`
- `analysis/phase_b/phase_b_full_radial_solver.py`
- `derivations/derivation_76_full_einstein_equations_nonminimal_coupling.md`
- `analysis/phase_b/phase_b_exact_radial_solver.py`

---

## 4. Why this matters for interpretation

Because the matter equations are component-symmetric, any later structured-object asymmetry cannot be attributed to unequal component equations.

It must come from some combination of:
- ordered-state seeding,
- boundary/continuation structure,
- the Einstein closure,
- and, in the exploratory ordered-runtime work, explicitly added directional terms.

That is the correct guardrail for the audited Phase B claims.

---

## 5. Bottom line

**Bottom line:** the Phase B radial-equation reconstruction is complete at the matter-system level. It establishes a clean four-component norm-coupled radial operator and the active domain/slice protocol used by the refreshed Phase B evidence package. It does **not** by itself prove structured-object objecthood or exact Einstein closure, but it gives the correct equation-level foundation for every later Phase B runtime claim.
