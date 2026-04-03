# Phase 3 Derivation: Topological Machinery After the Phase 2 Narrowing

## Purpose
Phase 3 determines whether Khantraction can carry genuine topological sectors after the spacetime lift.

After Phase 2, only the `u` sector remains a live topological candidate. The norm channel is already retired for topology and for particle-species structure.

So the central Phase 3 question is:

> Can the spacetime lift of the unit-quaternion sector support a nonzero conserved topological charge, or does the scalar-angle factorization force the topology to collapse?

## 1. The Unit-Quaternion Field

From earlier phases,

```text
q = e^alpha u,
|u| = 1,
u = exp(beta i + gamma j + delta k),
```

with

```text
beta = b(theta),
gamma = c(phi),
delta = d(rho).
```

So topological information, if any, must live in the map

```text
u : physical space -> S^3.
```

## 2. Physical Topological Degree for a Unit Quaternion Field

If the physical-space boundary condition sends the field to a fixed vacuum value at spatial infinity, then compactified physical space is `S^3`, and the natural topological charge of a unit-quaternion field is its degree:

```text
deg(u) in Z.
```

The standard degree density is

```text
B_phys(x)
  = (1 / 2 pi^2) det[u, partial_x u, partial_y u, partial_z u].
```

Equivalently,

```text
deg(u) = ∫ B_phys(x) d^3x.
```

This is the physically relevant candidate topological charge for the `u` sector.

## 3. Angle-Space Density

Before applying the spacetime lift, define the angle-space density

```text
J_ang(omega, theta, phi, rho)
  = det[u, partial_theta u, partial_phi u, partial_rho u].
```

Because `u` depends only on `(theta, phi, rho)`, `omega` is a spectator in this object.

From the Phase 1 determinant structure, the exact formula is

```text
J_ang = (sin(R) / R)^2 b'(theta) c'(phi) d'(rho).
```

This quantity can be nonzero. Phase 2 already showed that it is nonzero on the sampled domain for the live families.

However, a nonzero angle-space density does **not** by itself imply a nonzero physical topological charge. The spacetime lift matters.

## 4. Route S1 Scalar-Angle Pullback

The default scalar-angle lift from Phase 0 is

```text
u(x) = exp(v(x)),
v(x) = beta(x) i + gamma(x) j + delta(x) k,
```

with

```text
beta(x) = b(Theta(x)),
gamma(x) = c(Phi(x)),
delta(x) = d(Rho(x)).
```

If `Theta, Phi, Rho` are globally regular scalar fields, then the coefficient vector

```text
X(x) = (beta(x), gamma(x), delta(x))
```

is a continuous map

```text
X : S^3 -> R^3.
```

Then

```text
u = Exp(X),
```

where `Exp : R^3 -> S^3` is the pure-imaginary quaternion exponential map.

## 5. Null-Homotopy Theorem for the Scalar-Angle Lift

Because `R^3` is contractible, the map `X` is homotopic to the constant map `0` through

```text
X_t = t X,
0 <= t <= 1.
```

Applying the exponential map pointwise gives the explicit homotopy

```text
u_t(x) = Exp(t X(x)).
```

At `t = 1` this is the original field `u`, and at `t = 0` it is the constant field

```text
u_0(x) = 1.
```

Therefore:

```text
u is null-homotopic whenever it is globally of the form Exp(X) with continuous X : S^3 -> R^3.
```

So for the scalar-angle lift with globally regular scalar fields,

```text
deg(u) = 0.
```

This is the decisive Phase 3 obstruction.

## 6. Consequence

The scalar-angle lift Route S1 cannot support nonzero topological sectors if the angle fields are required to be globally regular.

That means:
- the strong "knotted spacetime" claim fails under the globally regular scalar-angle lift,
- and any nontrivial topology must come from one of the following instead:
  1. `u` treated as the fundamental field rather than as `Exp(X)` of global scalar-angle data,
  2. a multi-chart angular description,
  3. or an explicitly singular scalar-angle construction whose singularities are physically justified and tracked.

## 7. Pullback Density Under Route S1

Locally, Route S1 still has a density formula.

By chain rule,

```text
partial_i u
  = u_theta partial_i Theta
  + u_phi partial_i Phi
  + u_rho partial_i Rho.
```

So

```text
B_phys
  = (1 / 2 pi^2)
    J_ang(Theta, Phi, Rho)
    det(grad Theta, grad Phi, grad Rho).
```

Using the exact angle-space density,

```text
B_phys
  = (1 / 2 pi^2)
    (sin(R)/R)^2
    b'(Theta) c'(Phi) d'(Rho)
    det(grad Theta, grad Phi, grad Rho).
```

This density can be locally nonzero even though the total degree must vanish under the global scalar-angle theorem.

So Phase 2's nonzero sampled angle-space density was not wrong. It was only incomplete.

## 8. Single-Chart Coverage Criterion

Even before the null-homotopy obstruction, a single global chart must have enough range to cover the logarithm ball needed for full `S^3` reach.

Let

```text
I_b = range(b), I_c = range(c), I_d = range(d),
B_box = I_b x I_c x I_d subset R^3.
```

Every point of `S^3` has a logarithm representative `X` with `|X| <= pi`.

Therefore a sufficient and practically necessary single-chart coverage condition is:

```text
closed ball B_pi = { X in R^3 : |X| <= pi } subset B_box.
```

If the box fails to contain the ball `B_pi`, then the chart image misses some points of `S^3`. Any physical map constrained to that chart image misses those points as well, and therefore cannot have nonzero degree.

So even as a chart-level prerequisite:
- many admissible families can fail topology simply because their component ranges are too small.

## 9. What Survives

### Route S1 with global scalar angles
Topologically dead.

### Route S2 with `u` fundamental
Topologically alive in principle. The degree formula is valid and nonzero sectors are allowed.

### Route S3 frame/connection route
Still unresolved, but not killed by the scalar-angle null-homotopy theorem because it need not factor through a global `R^3` chart.

## Phase 3 Working Decision
Phase 3 changes the survival picture sharply:

1. The `u` sector remains the only live topological route.
2. The globally regular scalar-angle lift kills nonzero topology exactly.
3. Any serious topological continuation of Khantraction must elevate `u` to a fundamental field or use a multi-chart / singular-angle description.
