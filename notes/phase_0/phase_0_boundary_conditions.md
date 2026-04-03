# Phase 0 Note: Boundary Conditions and Reference Anchors

## Purpose
This note fixes the boundary-condition language used by the restart program. It separates:
- angle-space boundaries for scans,
- and physical-space boundaries for later spacetime lifts.

## 1. Angle-Space Domain

The base scan domain is

```text
A = [-2pi, 2pi]^4
```

with coordinates

```text
(omega, theta, phi, rho).
```

This is a closed exploration domain, not yet a quotient space. No periodic identification is assumed silently. If a later phase wants to identify opposite faces of this box or reduce the domain, it must prove the relevant symmetry first.

## 2. Canonical Reference Anchor

Phase 0 adopts the normalization

```text
a(0) = b(0) = c(0) = d(0) = 0,
```

so the canonical anchor is

```text
(omega, theta, phi, rho) = (0, 0, 0, 0),
q = 1.
```

This is the default vacuum-like reference state for early phases.

## 3. Vacuum Set for the Angle-Space Object

Because

```text
q = e^a [cos(R) + (V/R) sin(R)],
```

the condition `q = 1` is satisfied when:
- `a(omega) = 0`,
- `R(theta, phi, rho) = 2pi n`,
- and the unit direction is irrelevant when `sin(R) = 0`.

So the vacuum set can be non-unique unless `a, b, c, d` are constrained further.

This means later phases must distinguish:
- the **canonical vacuum anchor** `q = 1` at `(0, 0, 0, 0)`,
- from the broader **vacuum-equivalent set** where the same quaternion value may reappear.

If the vacuum-equivalent set is large, that itself may become an identity-collapse mechanism.

## 4. Physical-Space Boundary Conditions for Route S1

If later phases adopt the scalar-angle pullback route

```text
q(x) = q(Omega(x), Theta(x), Phi(x), Rho(x)),
```

the default finite-energy boundary conditions are:
- `Omega(x) -> 0`,
- `Theta(x) -> 0`,
- `Phi(x) -> 0`,
- `Rho(x) -> 0`,
- spatial gradients go to zero at infinity.

This sends the fields to the canonical vacuum anchor.

## 5. Radial-Origin Regularity

For any later radial reduction, regularity at `r = 0` requires:
- all scalar angle fields remain finite,
- odd radial singularities are excluded,
- derivative conditions are chosen so the reconstructed spacetime or field observables remain finite.

The exact origin conditions depend on the chosen action in Phase 2, but any radial ansatz violating finiteness at the origin is inadmissible.

## 6. Topological Boundary Conditions

If Phase 3 or later derives a real topological sector, the admissible asymptotic condition may broaden from "approach the canonical anchor" to "approach the vacuum set." That is allowed only if:
- the charge is explicitly defined,
- the asymptotic class is explicit,
- and the finite-energy condition still holds.

No topological boundary condition is allowed before the relevant topological invariant exists on paper.

## 7. Solver-Domain Boundaries

For future finite-box numerical solves:
- the outer boundary must approximate one of the admissible asymptotic conditions above,
- the box size must be increased until the key observables stop changing beyond tolerance,
- and no closure summary may confuse finite-box regularity with genuine asymptotic regularity.

## Phase 0 Decision
- The canonical reference anchor is fixed at `(0, 0, 0, 0)`.
- The broad vacuum-equivalent set is acknowledged and must be tracked in Phase 1.
- All later boundary conditions must be tied either to the canonical anchor or to an explicitly derived vacuum set.
