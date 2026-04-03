# Phase 0 Derivation: Formal Specification for the Exponential-Quaternion Restart

## Purpose
This note fixes the starting mathematical object for the restart program and records the constraints that follow immediately from the quaternion exponential itself. The purpose is not to prove viability. The purpose is to prevent later phases from smuggling in unstated assumptions.

## Starting Object

The restart program begins with the angle-space map

```text
q(omega, theta, phi, rho) = exp(a(omega) + b(theta) i + c(phi) j + d(rho) k)
```

with:
- `omega, theta, phi, rho` angle variables,
- `a, b, c, d` real-valued scalar functions,
- `i, j, k` the standard quaternion basis with
  - `i^2 = j^2 = k^2 = -1`,
  - `ij = k`, `jk = i`, `ki = j`,
  - `ji = -k`, `kj = -i`, `ik = -j`.

The default scan domain is

```text
A = [-2pi, 2pi]^4.
```

## Derived Coordinates

Define

```text
alpha = a(omega)
beta  = b(theta)
gamma = c(phi)
delta = d(rho)
V = beta i + gamma j + delta k
R = sqrt(beta^2 + gamma^2 + delta^2).
```

Since `V` is purely imaginary, the quaternion exponential takes the exact form

```text
q = e^alpha [cos(R) + (V/R) sin(R)]
```

for `R != 0`, and

```text
q = e^alpha
```

for `R = 0`.

## Immediate Algebraic Consequences

### 1. Norm collapse
The quaternion norm satisfies

```text
|q| = e^alpha = exp(a(omega)).
```

So the pointwise norm depends only on `omega` through `a(omega)`. It is completely blind to `theta`, `phi`, and `rho`.

This is a hard constraint on all later theory-building:
- any model built only from `|q|` or a potential `U(|q|)` cannot distinguish `theta`, `phi`, and `rho` algebraically,
- any angular distinction must therefore come from:
  - non-norm observables,
  - derivative structure,
  - topology,
  - boundary conditions,
  - coupling to geometry,
  - or some other explicit non-norm mechanism.

### 2. Scalar and vector parts
The real part of `q` is

```text
Re(q) = e^alpha cos(R),
```

and the imaginary magnitude is

```text
|Im(q)| = e^alpha |sin(R)|.
```

So:
- `a(omega)` sets the overall amplitude,
- `R` sets the scalar/vector mixing,
- the unit direction `V / R` sets the orientation inside the imaginary quaternion space.

### 3. Inverse
Because `exp` of a quaternion is never zero,

```text
q^-1 = exp(-(a + b i + c j + d k))
     = e^-alpha [cos(R) - (V/R) sin(R)].
```

This gives a globally defined inverse on the full scan domain.

## Canonical Normalization

The restart program adopts the baseline normalization

```text
a(0) = b(0) = c(0) = d(0) = 0.
```

Then

```text
q(0, 0, 0, 0) = 1.
```

This point is the canonical reference anchor used in early phases unless a later derivation proves that a different anchor is more natural.

## Admissible Function Classes

The program uses two admissible classes.

### Class P: periodic angle-respecting class
This is the mainline class for the physical-angle interpretation.

Requirements:
- `a, b, c, d : R -> R`,
- each is at least `C^3`,
- each is `2pi`-periodic,
- values and first three derivatives remain finite on `[-2pi, 2pi]`.

This class is the default whenever a phase claims to respect the statement that `omega, theta, phi, rho` are angles.

### Class L: lifted-chart diagnostic class
This class is allowed only for diagnostic sensitivity studies.

Requirements:
- `a, b, c, d` are at least `C^3` on `[-2pi, 2pi]`,
- values and first three derivatives remain finite on `[-2pi, 2pi]`,
- periodic identification is not assumed.

This class may be used to test whether observed structures are real or merely artifacts of a chosen angular chart, but results obtained only in Class L cannot be presented as evidence for a physical angle model unless the loss of periodicity is justified.

### Excluded classes
The following are not admissible:
- discontinuous functions,
- singular functions on the scan domain,
- functions with unbounded first derivative on the scan domain,
- functions that require branch cuts crossing the active scan region without explicit bookkeeping.

## Promotion to Spacetime

At Phase 0, `q` is only an angle-space map. No spacetime field interpretation is assumed.

The program allows three possible promotion routes, to be tested explicitly in later phases.

### Route S1: scalar-angle pullback
Introduce four spacetime scalar fields

```text
Omega(x), Theta(x), Phi(x), Rho(x)
```

and define

```text
q(x) = q(Omega(x), Theta(x), Phi(x), Rho(x)).
```

This is the simplest route and is the default first route for direct PDE work if no stronger geometric construction is derived first.

### Route S2: unit-quaternion bundle section
Rewrite

```text
q = e^alpha u,
```

with

```text
u = cos(R) + (V/R) sin(R),
```

and interpret `u` as a unit-quaternion-valued field or bundle section. This route is the natural entry point for topology.

### Route S3: frame or connection variable
Interpret the quaternion object as part of a local frame, orientation field, or connection-like structure. This route is allowed, but it must be derived explicitly rather than inserted rhetorically.

## Phase 0 Definitions

### Energy
For any later spacetime theory, "energy" means a direct functional derived from the declared action or geometric law. It is not allowed to introduce an ad hoc diagnostic and call it energy unless it is explicitly labeled as diagnostic only.

### Regularity
A candidate state is regular if:
- all declared dynamical fields remain finite in the domain of interest,
- all invariants used in the phase remain finite,
- no untracked singular sheets or coordinate branch jumps occur in the active region.

### Localization
A candidate state is localized if its direct energy density or direct mass density has finite concentration radii, and the density decays sufficiently that a finite-radius containment measure can be defined.

### Identity
A candidate object has identity only if it carries invariant data that:
- survives allowed coordinate changes,
- survives small perturbations,
- and distinguishes it from other candidate objects.

Seed labels do not count as identity.

### Stability
Stability requires both:
- no decisive linear instability in the direct linearized problem,
- no decisive nonlinear dissolution or universalization in the direct evolution problem.

### Viability
The model is viable only if the later direct program produces regular localized states with invariant identity, direct stability, transportability, and nontrivial direct interactions.

## Consequences for Later Phases

1. Phase 1 must treat norm-only observables as `omega`-only observables unless a different norm is explicitly derived.
2. Phase 2 must reject any proposed action that claims angular species structure while depending only on `|q|`.
3. Phase 3 must test whether topology can live in `u` or in a spacetime lift of `u`, because it will not come from `|q|`.
4. Phase 4 and later must declare explicitly whether they use Route S1, S2, or S3.

## Phase 0 Result
Phase 0 fixes the starting mathematical contract and exposes the first major structural constraint:

```text
|q(omega, theta, phi, rho)| = exp(a(omega)).
```

So a purely norm-based Khantraction theory cannot support angle-defined species.
