# Phase 3 Assessment

## Verdict
Phase 3 is complete.

## What Phase 3 established

### 1. The globally regular scalar-angle lift is topologically dead
This is now an exact result, not just a numerical suspicion.

If

```text
u(x) = exp(X(x)),
X : S^3 -> R^3
```

with `X` globally continuous, then

```text
u_t(x) = exp(t X(x))
```

is an explicit homotopy from `u` to the constant map `1`.

Therefore:

```text
deg(u) = 0
```

for the globally regular scalar-angle lift.

### 2. The angle-space topological density is real but insufficient
The exact angle-space density is

```text
J_ang = (sin(R)/R)^2 b'(theta) c'(phi) d'(rho).
```

The direct samples show that this density is genuinely nonzero in the live families:
- `periodic_simple`
  - `max_abs_J_ang = 10.648000000000005`
- `periodic_harmonic`
  - `max_abs_J_ang = 35.90400000000002`
- `periodic_topology_ready`
  - `max_abs_J_ang = 42.87500000000001`

So the local topological avenue is real. It is the scalar-angle global factorization that kills the total charge.

### 3. Current tested families do not all have full single-chart `S^3` reach
Chart-coverage results:
- `periodic_simple`
  - `ball_pi_contained = false`
- `periodic_harmonic`
  - `ball_pi_contained = false`
- `lifted_chart_linear`
  - `ball_pi_contained = false`
- `periodic_topology_ready`
  - `ball_pi_contained = true`

This matters because:
- the first three families cannot even cover the full logarithm ball in one chart,
- while the topology-ready periodic family shows that the admissible periodic class itself does not forbid full single-chart reach.

### 4. Even with full single-chart reach, Route S1 still cannot carry nonzero degree
The `periodic_topology_ready` family satisfies the chart-coverage prerequisite:
- `single_chart_surjective_to_S3 = true`

But its Route S1 topological status is still:
- `route_S1_nonzero_degree_possible = false`

That is the key distinction:
- chart reach is only a prerequisite,
- the null-homotopy obstruction is the decisive killer for global scalar-angle topology.

### 5. The unit-quaternion route survives
The direct S2 benchmark uses a standard degree-one hedgehog-like unit-quaternion field. Its numerical degree converges toward `-1` as the grid is refined:
- `33^3`: `-0.8544390798849802`
- `49^3`: `-0.9289226204920789`
- `65^3`: `-0.9572477795220055`

So the `u` sector itself is fully capable of carrying nontrivial topology when treated as fundamental.

### 6. The attempted global logarithm is singular
The principal-log benchmark around the direct degree-one `u` field shows large shell spread near the core:
- at `n = 65`, shell radius `0.15`
  - `log_vector_spread = 2.7708967535984037`
- at `n = 65`, shell radius `0.30`
  - `log_vector_spread = 2.7708967535984037`

That is the expected failure of a global regular scalar-angle representation near a nontrivial topological core.

### 7. Direct S1 smooth scalar-angle benchmarks integrate to near zero degree
Examples:
- `cartesian_decay`
  - `-0.0007261940343658896` at `33^3`
  - `-0.0003294868465552811` at `49^3`
- `mixed_polynomial`
  - `1.0005576689441423e-19` at `33^3`
  - `-2.0095856673608276e-19` at `49^3`
- `trig_swirl`
  - `-0.01217691033183402` at `33^3`
  - `-0.005753342850588188` at `49^3`

This is numerically consistent with the exact null-homotopy theorem.

## Phase 3 decision
The strong "knotted spacetime through globally regular scalar angles" claim is retired.

The topological survival path is now:
1. treat `u` as the fundamental field,
2. or explicitly use a multi-chart / singular-angle construction and track it honestly.

If the program insists on globally regular scalar-angle fields as the physical variables, topology is finished.
