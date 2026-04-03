# Phase 0 Note: Exhaustive Scan Protocol

## Purpose
This note defines the mandatory scan protocol for the restart program. "Exhaustive" means every free-variable subset is covered directly on the required angle domain, with documented refinement where features appear.

## 1. Active Angle Domain

The mandatory exploration interval for every angle is

```text
[-2pi, 2pi].
```

This applies to:
- `omega`,
- `theta`,
- `phi`,
- `rho`.

## 2. Mandatory Variable-Family Matrix

Every phase that probes dependence on `(omega, theta, phi, rho)` must include:

### 4 free variables
- vary `(omega, theta, phi, rho)`

### 3 free variables
- vary `(theta, phi, rho)` holding `omega`
- vary `(omega, phi, rho)` holding `theta`
- vary `(omega, theta, rho)` holding `phi`
- vary `(omega, theta, phi)` holding `rho`

### 2 free variables
- vary `(omega, theta)` holding `(phi, rho)`
- vary `(omega, phi)` holding `(theta, rho)`
- vary `(omega, rho)` holding `(theta, phi)`
- vary `(theta, phi)` holding `(omega, rho)`
- vary `(theta, rho)` holding `(omega, phi)`
- vary `(phi, rho)` holding `(omega, theta)`

### 1 free variable
- vary `omega` holding `(theta, phi, rho)`
- vary `theta` holding `(omega, phi, rho)`
- vary `phi` holding `(omega, theta, rho)`
- vary `rho` holding `(omega, theta, phi)`

### 0 free variables
- evaluate named anchors

No phase is complete without all applicable families.

## 3. Mandatory Anchor Set

The base anchor set for each angle is

```text
{-2pi, -3pi/2, -pi, -pi/2, -pi/4, 0, pi/4, pi/2, pi, 3pi/2, 2pi}.
```

This 11-point set is the minimum discovery lattice for each free dimension in every phase, including solver phases.

## 4. Resolution Schedule

There are two protocol tiers.

### Tier A: algebraic / kinematic phases
Use direct full tensor grids.

- coarse:
  - 1D: 65 points
  - 2D: 33 x 33
  - 3D: 17 x 17 x 17
  - 4D: 11 x 11 x 11 x 11

- refinement:
  - 1D: 257 points
  - 2D: 129 x 129
  - 3D: 33 x 33 x 33
  - 4D: 17 x 17 x 17 x 17

- convergence:
  - 1D: 1025 points
  - 2D: 257 x 257
  - 3D: 65 x 65 x 65
  - 4D: 33 x 33 x 33 x 33

### Tier B: direct solver phases
Use the full 11-anchor lattice as the mandatory discovery pass for each free dimension, then refine locally around detected features.

- discovery:
  - 11 anchors per free dimension

- refinement trigger:
  - any sign change,
  - any branch change,
  - any singularity indicator,
  - any stability transition,
  - any sharp change in slope or curvature between adjacent anchors

- refinement rule:
  - insert midpoints between every flagged adjacent anchor pair,
  - repeat until the feature location and the key reported observables stabilize to tolerance

- convergence rule:
  - double the outer-domain resolution and tighten step sizes until the reported phase observables change by less than the declared tolerance.

## 5. Reported Tolerances

Every phase summary must state:
- the numerical tolerance used for solver convergence,
- the observable tolerance used for declaring a feature stable,
- and the resolution at which the headline claims stopped changing materially.

If a phase does not report tolerances, it is not closed.

## 6. Named Regression Anchors

The following anchors are mandatory in every phase unless proven irrelevant:
- `(0, 0, 0, 0)`
- `(0, pi/4, 0, 0)`
- `(0, 0, pi/4, 0)`
- `(0, 0, 0, pi/4)`
- `(pi/4, 0, 0, 0)`
- `(pi/4, pi/4, pi/4, pi/4)`
- `(-pi/4, -pi/4, -pi/4, -pi/4)`
- `(pi, 0, 0, 0)`
- `(0, pi, 0, 0)`
- `(0, 0, pi, 0)`
- `(0, 0, 0, pi)`

These anchors are the base regression checks for cross-phase consistency.

## 7. Contradiction Pass

Before any phase closes, it must explicitly test whether the reported structure can be explained by:
- periodic aliasing,
- coordinate redundancy,
- branch-cut choice,
- resolution artifacts,
- box-size artifacts,
- or solver tolerances.

If one of those explanations survives, the claim is not closed.

## Phase 0 Decision
- The scan protocol is fixed.
- The 11-anchor lattice is the minimum direct discovery coverage for every free dimension.
- Later phases may add points, but they may not use fewer without an explicit proof of irrelevance.
