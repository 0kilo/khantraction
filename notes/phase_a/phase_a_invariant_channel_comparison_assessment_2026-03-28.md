# Phase A Assessment — Less Chart-Bound Channel Comparison

**Date:** 2026-03-28  
**Phase:** A — Parameter foundation  
**Status:** In progress

## Purpose

This note starts the next Phase A task:

> compare $\theta,\phi,\rho$ using quantities that are less tied to raw determinant-zero language and more tied to the geometry of the angular tangent bundle itself.

## Why this is needed

So far Phase A has shown:
- local angular independence away from singular slices,
- singular sheets controlled by $\phi$,
- and very clean 1D/2D slice behavior.

But determinant language alone can over-focus attention on singularity structure.
We also want to know:
- do the three angular channels differ in tangent norms?
- do they differ in pairwise overlap structure?
- does one channel collapse while others remain robust?
- how does the full angular tangent condition number behave as different channels vary?

## Active implementation

The current analysis file is:
- `analysis/phase_a/phase_a_invariant_channel_comparison.py`

Outputs are stored under:
- `solutions/phase_a/phase_a_invariant_channel_comparison/`

## Diagnostics used

For the angular Jacobian columns $(\partial_\theta Q, \partial_\phi Q, \partial_\rho Q)$, compute:
- individual tangent norms,
- pairwise cosine overlaps,
- the angular Gram matrix,
- its singular values,
- and the resulting condition number.

These are still chart-derived quantities, but they are more geometric than using only $\det J$.

## What to look for

The key interpretive tests are:
1. Does $\phi$ only control singularity, or does it also distort the full angular tangent spectrum more strongly than $\theta$ and $\rho$?
2. Away from singular sheets, do $\theta$ and $\rho$ remain nearly symmetric while $\phi$ acts differently?
3. At regular points, are all three channels still equally strong in norm, with differences showing up mainly in overlap/coupling structure?

## Interpretation target

The target is not yet to claim physical meaning.
The target is narrower:

> determine whether the chart geometry gives evidence for a robust structural asymmetry between the three angular channels that survives beyond simply saying where the determinant vanishes.
