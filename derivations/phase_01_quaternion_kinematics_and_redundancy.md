# Phase 1 Derivation: Quaternion Kinematics, Redundancy, and First Invariants

## Purpose
Phase 1 studies the angle-space map

```text
q(omega, theta, phi, rho) = exp(a(omega) + b(theta) i + c(phi) j + d(rho) k)
```

purely as a kinematic object. The goal is to determine:
- how much of the input angle space survives as genuine quaternion data,
- where the map loses rank,
- how large the vacuum-equivalent and sign-flip sets can be,
- and what the first honest invariant candidates are before any spacetime lift is introduced.

Throughout this derivation,

```text
alpha = a(omega)
beta  = b(theta)
gamma = c(phi)
delta = d(rho)
x = (beta, gamma, delta)^T
R = |x| = sqrt(beta^2 + gamma^2 + delta^2).
```

Define also

```text
f(R) = sin(R)/R
```

with removable continuation `f(0) = 1`.

Then

```text
q = e^alpha [cos(R) + f(R)(beta i + gamma j + delta k)].
```

In component form,

```text
q = (q0, q1, q2, q3)
```

with

```text
q0 = e^alpha cos(R)
qv = (q1, q2, q3)^T = e^alpha f(R) x.
```

## 1. Complete Pointwise Data

The pointwise quaternion value is completely determined by:
- `alpha`,
- `cos(R)`,
- and the vector `x f(R)`.

Equivalently, away from `R = 0`, it is determined by:
- `alpha`,
- `R`,
- and the unit direction
  - `n = x / R`.

So the map factors as

```text
(omega, theta, phi, rho)
  -> (alpha, x)
  -> (alpha, R, n)
  -> q.
```

This factorization is the basic redundancy mechanism.

## 2. Equality Classification

Consider two points with data `(alpha1, R1, n1)` and `(alpha2, R2, n2)`. Their quaternions are equal if and only if

```text
e^alpha1 [cos(R1) + n1 sin(R1)] = e^alpha2 [cos(R2) + n2 sin(R2)].
```

Since quaternion norm is multiplicative and positive,

```text
|q1| = |q2|  =>  alpha1 = alpha2.
```

So equality reduces to equality of the unit-quaternion factors:

```text
cos(R1) + n1 sin(R1) = cos(R2) + n2 sin(R2).
```

This yields the exact cases below.

### Case A: nonsingular angular points
If `sin(R1) != 0` and `sin(R2) != 0`, then equality holds if and only if:

1. `cos(R1) = cos(R2)`, and
2. `n1 sin(R1) = n2 sin(R2)`.

Therefore:
- either `R2 = R1 + 2pi m` and `n2 = n1`,
- or `R2 = 2pi m - R1` and `n2 = -n1`,

for some integer `m`, subject to `R2 >= 0`.

So the quaternion exponential is non-injective in the imaginary magnitude and direction together.

### Case B: singular angular points
If `sin(R1) = sin(R2) = 0`, then `R1, R2 in pi Z`, the direction data `n1, n2` drops out completely, and equality reduces to parity:

```text
cos(R1) = cos(R2) = (-1)^k.
```

So on the sheets `R = k pi` the quaternion value is

```text
q = (-1)^k e^alpha,
```

independent of the imaginary direction.

These are the fundamental orientation-loss sheets of the ansatz.

## 3. Vacuum-Equivalent and Sign-Flip Sets

### Vacuum-equivalent set
The set where `q = 1` is given by

```text
alpha = 0,
R = 2pi m,
```

for integers `m >= 0`.

In terms of the original functions:

```text
a(omega) = 0,
b(theta)^2 + c(phi)^2 + d(rho)^2 = (2pi m)^2.
```

### Sign-flip set
The set where `q = -1` is given by

```text
alpha = 0,
R = (2m + 1) pi.
```

So the sign-flip set is

```text
a(omega) = 0,
b(theta)^2 + c(phi)^2 + d(rho)^2 = ((2m + 1)pi)^2.
```

These formulas show immediately that:
- a large zero set of `a` enlarges both the vacuum-equivalent and sign-flip families,
- and large amplitudes in `b, c, d` can create orientation-blind sign sheets even when `q != ±1`.

## 4. First Derivatives

The derivatives with respect to the transformed variables `(alpha, beta, gamma, delta)` are cleanest.

Let

```text
h(R) = (R cos(R) - sin(R)) / R^3
```

with removable continuation `h(0) = -1/3`.

Then

```text
partial_alpha q0 = q0
partial_alpha qv = qv
```

and, for `x_i in {beta, gamma, delta}`,

```text
partial_xi q0 = -e^alpha f(R) x_i
partial_xi qv = e^alpha [f(R) e_i + h(R) x_i x],
```

where `e_i` is the standard basis vector in `R^3`.

So the Jacobian with respect to `(alpha, beta, gamma, delta)` is

```text
J_y = e^alpha
      [ cos(R)        -f(R) x^T ]
      [ f(R) x   f(R) I3 + h(R) x x^T ].
```

By chain rule, the Jacobian with respect to `(omega, theta, phi, rho)` is

```text
J = J_y diag(a'(omega), b'(theta), c'(phi), d'(rho)).
```

## 5. Exact Jacobian Determinant

This determinant is the key Phase 1 structural result.

Using the block matrix formula and the determinant lemma for

```text
B = f I3 + h x x^T,
```

one finds

```text
det(B) = f(R)^2 cos(R),
```

and the Schur complement contributes exactly `1 / cos(R)` when `cos(R) != 0`, with the final result extending by continuity through those points.

Therefore

```text
det(J_y) = e^(4 alpha) f(R)^2
         = e^(4 alpha) (sin(R)/R)^2.
```

Hence

```text
det(J)
  = e^(4 a(omega))
    (sin(R)/R)^2
    a'(omega) b'(theta) c'(phi) d'(rho).
```

This formula implies:

### Full-rank region
The map is locally full rank whenever all of the following hold:
- `a'(omega) != 0`,
- `b'(theta) != 0`,
- `c'(phi) != 0`,
- `d'(rho) != 0`,
- and either `R = 0` or `sin(R) != 0`.

### Rank-loss sets
Rank loss occurs on:
1. derivative-zero sheets:
   - `a' = 0`, `b' = 0`, `c' = 0`, `d' = 0`,
2. orientation-loss sheets:
   - `R = k pi` for nonzero integer `k`.

At `R = 0`, the Jacobian is regular provided the four one-variable derivatives are nonzero.

## 6. Rank on the Orientation-Loss Sheets

At `R = k pi` with `k != 0`, we have

```text
f(R) = 0,
h(R) = cos(R) / R^2 = (-1)^k / R^2.
```

So

```text
J_y = e^alpha
      [ (-1)^k   0 ]
      [   0    h x x^T ].
```

The lower block is rank `1` whenever `x != 0`, which it must be because `R = |x| = k pi != 0`.

Therefore, on a generic orientation-loss sheet:

```text
rank(J_y) = 2.
```

So the map loses two local degrees of freedom there:
- one because the unit direction becomes irrelevant,
- one because the remaining angular dependence is only through the radial change of `R`.

After the chain rule scaling, the rank of `J` can drop below `2` if one or more of `b'`, `c'`, `d'` also vanishes.

## 7. Hessian Existence and Regularity

Because the admissible classes require `a, b, c, d` to be at least `C^3`, and because both

```text
f(R) = sin(R)/R
```

and

```text
h(R) = (R cos(R) - sin(R)) / R^3
```

have removable continuations at `R = 0`, the component Hessians of `q` exist and remain finite on the full scan domain for the admissible classes.

So the important issue in Phase 1 is not Hessian blow-up. It is rank loss and identity collapse.

## 8. First Honest Invariants

Before any spacetime lift, the first honest pointwise invariants are:

1. the full quaternion value `q`,
2. the norm `|q| = exp(a(omega))`,
3. the normalized unit quaternion

```text
u = q / |q| = cos(R) + n sin(R),
```

4. the scalar/vector pair

```text
Re(q) = e^alpha cos(R),
|Im(q)| = e^alpha |sin(R)|.
```

What is **not** an invariant is the raw label tuple `(omega, theta, phi, rho)` by itself. Many different angle tuples can map to the same quaternion value.

## 9. Immediate Consequences for Viability

Phase 1 already narrows the program sharply:

1. Any species claim based only on input-angle labels is invalid unless those labels survive the redundancy map.
2. Any norm-only action is already too weak to distinguish `theta`, `phi`, and `rho`.
3. The orientation-loss sheets `R = k pi` are unavoidable kinematic degeneracy surfaces whenever the functions `b, c, d` can reach those radii.
4. The first meaningful identity question is not "which angle labels were chosen?" but rather "what invariant quaternion data and what preimage structure survive?"

## Phase 1 Working Hypothesis
The exponential-quaternion ansatz does not create pointwise particle species by itself. It creates:
- a norm channel controlled by `a(omega)`,
- a scalar/vector mixing channel controlled by `R`,
- and an orientation channel controlled by the unit direction `n`,
with substantial redundancy.

Phase 1 numerical work must now measure how severe that redundancy becomes on the required `[-2pi, 2pi]^4` scan domain for admissible families of `a, b, c, d`.
