# Phase 2 Derivation: Direct Action Families After the Phase 0 and Phase 1 Constraints

## Purpose
Phase 2 builds the first mathematically explicit direct action families that can still survive after the Phase 0 and Phase 1 results.

Those earlier phases already established:

```text
|q(omega, theta, phi, rho)| = exp(a(omega)),
```

and showed directly that raw angle labels are not pointwise identity invariants.

Therefore Phase 2 must not start from a blank slate. It must enforce the following constraint immediately:

> Any action family that depends only on `|q|` cannot support angle-defined particle species.

Such a family may still describe a classical lump theory, but it cannot be treated as a surviving particle-species route.

## 1. Spacetime Lift Used in Phase 2

Phase 2 uses the default promotion route from Phase 0:

```text
q(x) = q(Omega(x), Theta(x), Phi(x), Rho(x)),
```

where

```text
Omega, Theta, Phi, Rho
```

are spacetime scalar fields.

Define

```text
alpha(x) = a(Omega(x))
beta(x)  = b(Theta(x))
gamma(x) = c(Phi(x))
delta(x) = d(Rho(x))
x = (beta, gamma, delta)^T
R = |x|.
```

Then

```text
q = e^alpha u,
u = cos(R) + (x/R) sin(R),
|u| = 1.
```

Crucially:
- `alpha` depends only on `Omega`,
- `u` depends only on `Theta, Phi, Rho`.

So the ansatz already splits into:
- one scale channel,
- and one unit-quaternion orientation channel.

## 2. Kinematic Building Blocks

Phase 2 uses the following direct building blocks.

### 2.1 Norm channel

```text
N = |q| = e^alpha.
```

Its derivative is

```text
partial_mu N = e^alpha partial_mu alpha.
```

Since `alpha = a(Omega)`,

```text
partial_mu alpha = a'(Omega) partial_mu Omega.
```

So the norm channel depends only on `Omega`.

### 2.2 Full quaternion derivative

From

```text
q = e^alpha u,
```

we get

```text
partial_mu q = e^alpha (partial_mu alpha) u + e^alpha partial_mu u.
```

Because `u` is unit:

```text
u · partial_mu u = 0.
```

Hence

```text
|partial_mu q|^2 = e^(2 alpha) [ (partial_mu alpha)^2 + |partial_mu u|^2 ].
```

This is the key decomposition of the full quaternion sigma-model kinetic term.

### 2.3 Unit-quaternion Maurer-Cartan form

Define

```text
L_mu = u^-1 partial_mu u.
```

For unit quaternions, `L_mu` is purely imaginary. So it can be identified with a 3-vector `ell_mu`.

This gives two important direct invariants:

1. sigma-model kinetic density

```text
K_u = sum_mu |ell_mu|^2 = sum_mu |partial_mu u|^2,
```

2. quartic Skyrme-type density

```text
S_4 = sum_{mu < nu} |[L_mu, L_nu]|^2
    = 4 sum_{mu < nu} |ell_mu x ell_nu|^2.
```

The quartic density is the first direct stabilizing/topological building block available from the unit-quaternion route.

### 2.4 Candidate topological density

Before physical-space topology is introduced in Phase 3, the relevant angle-space diagnostic is

```text
B_ang = det[u, partial_theta u, partial_phi u, partial_rho u],
```

interpreting the four vectors as columns in `R^4`.

This is not yet a physical topological charge. But if it is identically zero, the unit-quaternion route has little chance of carrying nontrivial degree structure later. If it is generically nonzero, the topological route survives to Phase 3.

## 3. Candidate Action Families

## Avenue A0: norm-only scalar action

Take

```text
S_norm = ∫ d^4x sqrt(-g)
  [ 1/2 kappa_N g^{mu nu} partial_mu N partial_nu N - U(N) ].
```

Since

```text
N = exp(a(Omega)),
```

this theory depends only on `Omega`.

### Consequence
`Theta, Phi, Rho` are completely invisible to the direct action. Therefore:
- this avenue may still be a classical one-channel lump model,
- but it is already retired as a candidate source of angle-defined particle species.

## Avenue A1: full quaternion sigma model

Take

```text
S_q = ∫ d^4x sqrt(-g)
  [ 1/2 kappa_q g^{mu nu} <partial_mu q, partial_nu q> - U_q(q) ].
```

Using the split,

```text
<partial_mu q, partial_nu q>
  = e^(2 alpha)
    [ (partial_mu alpha)(partial_nu alpha)
      + <partial_mu u, partial_nu u> ].
```

This route is nontrivial because the derivative term sees the unit-quaternion sector. So unlike Avenue A0, it can respond to `Theta, Phi, Rho`.

### Limitation
If `U_q` is chosen to depend only on `|q|`, then the potential remains angle-blind. The angular structure then lives only in the kinetic term.

## Avenue A2: split sigma action

Take

```text
S_split = ∫ d^4x sqrt(-g)
  [ 1/2 kappa_alpha g^{mu nu} partial_mu alpha partial_nu alpha
    + 1/2 kappa_u e^(2 alpha) g^{mu nu} <partial_mu u, partial_nu u>
    - U_alpha(alpha) ].
```

This route makes the scale/orientation split explicit.

### Advantages
1. It respects the structure revealed by Phase 1.
2. It does not pretend that the norm channel carries angular species information.
3. It isolates the unit-quaternion channel where topology and orientation may survive.

### Immediate consequence
Because `u` depends only on `Theta, Phi, Rho`, the scale and orientation sectors are already block-separated at the kinematic level.

## Avenue A3: split sigma plus Skyrme stabilizer

Take

```text
S_split+4 = ∫ d^4x sqrt(-g)
  [ 1/2 kappa_alpha g^{mu nu} partial_mu alpha partial_nu alpha
    + 1/2 kappa_u e^(2 alpha) g^{mu nu} <partial_mu u, partial_nu u>
    - lambda_4 e^(4 alpha) S_4
    - U_alpha(alpha) ].
```

This is the first avenue that has a direct route to:
- nontrivial unit-quaternion geometry,
- quartic stabilization,
- and later topological protection.

So this avenue survives Phase 2 as the strongest current candidate.

## Avenue A4: curvature-coupled scale-only route

Take

```text
S_curv,scale = ∫ d^4x sqrt(-g)
  [ 1/2 kappa_N g^{mu nu} partial_mu N partial_nu N
    + xi N^2 R_g
    - U(N) ].
```

This route still couples only the norm channel to curvature.

### Consequence
It remains blind to `Theta, Phi, Rho` as a species mechanism. So it is retired as a particle-species route for the same reason as Avenue A0.

## Avenue A5: curvature-coupled split route

Take

```text
S_curv,split = ∫ d^4x sqrt(-g)
  [ 1/2 kappa_alpha g^{mu nu} partial_mu alpha partial_nu alpha
    + 1/2 kappa_u e^(2 alpha) g^{mu nu} <partial_mu u, partial_nu u>
    - lambda_4 e^(4 alpha) S_4
    + xi e^(2 alpha) R_g
    + eta T(u, g, partial u, curvature)
    - U_alpha(alpha) ].
```

This avenue is structurally viable, but only if the curvature coupling actually sees more than the scale channel. The exact tensor `T` is not fixed yet, so this avenue survives as viable but unresolved.

## Avenue A6: frame/connection reinterpretation

Instead of treating `u` as a sigma-model field, one may treat

```text
L_mu = u^-1 partial_mu u
```

as a connection-like or frame-like object and build dynamics from it directly.

This avenue is not rejected. But it is still structurally incomplete in Phase 2 because the geometric interpretation and the direct action are not yet uniquely fixed.

## 4. Direct Phase 2 Classifications

The Phase 2 direct classifications are:

### Retired as particle-species routes
- Avenue A0: norm-only scalar action
- Avenue A4: curvature-coupled scale-only route

Reason:
- both are blind to `Theta, Phi, Rho` except through structures they do not contain.

### Viable core routes
- Avenue A1: full quaternion sigma model
- Avenue A2: split sigma action
- Avenue A3: split sigma plus Skyrme stabilizer

Reason:
- they contain explicit non-norm derivative structure,
- and A3 also contains a direct stabilizing/topological route.

### Viable but unresolved
- Avenue A5: curvature-coupled split route

Reason:
- it can still carry nontrivial structure,
- but the exact curvature tensor couplings are not fixed yet.

### Structurally incomplete
- Avenue A6: frame/connection reinterpretation

Reason:
- the direct field content and action principle are not yet specified enough to solve.

## 5. Consequences for Later Phases

1. Phase 3 should prioritize the `u`-based topological route.
2. Phase 4 should prioritize direct static solves for A2 and A3.
3. Norm-only or scale-only curvature models may still be used as baselines, but they should no longer be presented as live particle-species candidates.

## Phase 2 Working Decision
After Phases 0 and 1, the only serious routes left are the non-norm routes:
- full quaternion sigma,
- split sigma,
- split sigma plus Skyrme stabilization,
- and curvature/frame extensions built on the `u` sector.

Phase 2 numerical work must now confirm that these routes really carry nontrivial angular sensitivity, nontrivial kinetic rank, and a nonzero topological avenue on the required angle domain.
