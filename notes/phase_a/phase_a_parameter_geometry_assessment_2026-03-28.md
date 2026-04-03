# Phase A Assessment — Ordered Quaternion Parameter Geometry

**Date:** 2026-03-28  
**Phase:** A — Parameter foundation  
**Status:** Complete supporting assessment

## Purpose

This note records the final assessment of the base ordered-map geometry for

$$
Q(\omega,\theta,\phi,\rho)=e^{\omega}e^{\theta i}e^{\phi j}e^{\rho k}.
$$

The question for this step is narrower than later structured-object work:

> does the ordered map already justify treating $\omega$ separately from the angular variables, and do $\theta,\phi,\rho$ behave as genuinely distinct local angular directions away from chart singularities?

## Method

The supporting work for this assessment is:

- `derivations/derivation_71_exponential_quaternion_parameter_mapping_clean.md`
- `analysis/phase_a/phase_a_parameter_geometry.py`

The regenerated solution set now uses the active Phase A domain convention:

- $\omega>0$
- $\theta,\phi,\rho\in[-2\pi,2\pi]$
- no redundancy quotienting

The analysis evaluates the exact Jacobian of the ordered map on a coarse active-domain grid at fixed $\omega=0$, then inspects named benchmark points such as the origin, quarter turns, and the current quaternion-rich sector guess.

## Results

### 1. Scale separates cleanly from angular geometry

The component formulas from Derivation 71 all carry the same multiplicative factor $e^\omega$.

That means:

- $\omega$ changes overall magnitude,
- the normalized angular geometry lives entirely in $(\theta,\phi,\rho)$,
- and any angular-role comparison should be done after factoring out scale.

### 2. The coarse active-domain scan remains generically full rank

The updated regenerated coarse scan

- samples 35,937 grid points on the active domain,
- finds a minimum sampled $|\det J|$ of `0.0`,
- and records 8,712 coarse special/singular points where rank drops or the determinant vanishes.

Those special points are not generic. They are the repeated singular sheets later isolated precisely in the singularity-structure assessment.

Away from those sheets, the map behaves as a regular local chart with one scale direction and three distinct local angular directions.

### 3. Named benchmark points do not privilege one angular channel by norm

At the origin, the quarter-turn points, the all-quarter-turn point, and the rich-sector guess:

- `rankJ = 4`,
- `||∂θQ|| = ||∂φQ|| = ||∂ρQ|| = 1` at $\omega=0$,
- and the pairwise angular cosines vanish to numerical precision.

So the base map does not support a claim that one angle is generically larger or stronger than the others at regular points.

## Assessment

This step establishes the correct starting point for Phase A:

1. $\omega$ is already separated from the internal angular geometry at the mapping level.
2. $\theta,\phi,\rho$ are not fake duplicates of one local angle; they define three genuine local tangent directions wherever the chart is regular.
3. Any stronger asymmetry claim must come from the overlap structure and singular architecture, not from a raw norm hierarchy.

That is enough to justify the plan requirement that the angular channels be compared symmetrically before assigning stronger role language.

## Limits

This note does **not** prove a dynamical or physical hierarchy among the angles.

It only proves the mapping-level statement:

> the ordered quaternion parameter map is a coherent local foundation with one scale direction and three locally distinct angular directions, except on a repeated singular-sheet set.

## Evidence

- `derivations/derivation_71_exponential_quaternion_parameter_mapping_clean.md`
- `analysis/phase_a/phase_a_parameter_geometry.py`
- `solutions/phase_a/phase_a_parameter_geometry/coarse_scan.csv`
- `solutions/phase_a/phase_a_parameter_geometry/named_points.json`
- `solutions/phase_a/phase_a_parameter_geometry/special_points.json`
- `solutions/phase_a/phase_a_parameter_geometry/summary.md`
