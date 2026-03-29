# Phase B Assessment — Radial Equation Reconstruction

**Date:** 2026-03-28  
**Phase:** B — Structured-object picture  
**Status:** In progress

## Purpose

This note starts the next true Phase B bottleneck task:

> reconstruct the full four-component radial equations in the fresh tree so Phase B can advance from ordered-state viability toward actual physical branch continuation.

## What has now been established

The fresh tree now has an explicit derivation for the full four-component **matter-side** radial equations of the norm-based quaternion glue field.

That is a real step forward, because the project no longer has to say only “the equations are missing.”
At least the component field equations have now been written explicitly from the stated toy-model Lagrangian.

## What this derivation gives

The new derivation establishes that each component \(q_A \in \{a,b,c,d\}\) obeys the same radial operator:
\[
q_A''+\left(\frac{2}{r}+\Phi'-\Lambda'\right)q_A' + e^{2\Lambda}\Big(m_{\mathrm{glue}}^2+\lambda_q|q|^2-2\xi R\Big)q_A=0,
\]
with shared coupling through
\[
|q|^2=a^2+b^2+c^2+d^2.
\]

So the full norm-based toy model is matter-symmetric at the component-equation level.

## What is still missing

This still does **not** complete a trustworthy physical solver.
The following remain to be reconstructed explicitly in the fresh tree:
- Einstein-sector closure,
- an eliminable or explicit formula for \(R\),
- boundary conditions,
- continuation setup,
- observable extraction formulas.

## Why this matters conceptually

The derivation also clarifies something important for interpretation:

> any later asymmetry among ordered variables is not built into unequal bare component equations here.

It must instead arise from:
- the ordered parameter embedding into \((a,b,c,d)\),
- nonlinear norm coupling,
- geometry closure,
- boundary conditions,
- and solution-family selection.

That is an important guardrail for later Phase B and Phase C claims.

## Active files

New files for this reconstruction step:
- `derivations/derivation_73_full_four_component_radial_system_fresh_start.md`
- `analysis/phase_b_radial_equation_structure.py`
- `solutions/phase_b_radial_equation_structure/`

## Immediate next step

A first real solver/runtime now exists in:
- `analysis/phase_b_full_radial_solver.py`
- `scripts/run_phase_b_full_radial_solver.sh`
- `solutions/phase_b_full_radial_solver/`
- `notes/phase_b_full_radial_solver_assessment_2026-03-28.md`

But that runtime still uses an explicit provisional Einstein closure rather than a uniquely derived fresh-tree nonminimal-coupling closure.
So the next required derivation step remains: reconstruct the full Einstein-sector closure and sharpen the regular/asymptotic boundary conditions, then test whether the current runtime survives that tighter derivation or needs structural correction.
