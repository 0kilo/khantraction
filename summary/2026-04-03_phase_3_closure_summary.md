# Phase 3 Closure Summary

## Status
Closed.

## Phase Goal
Phase 3 was the topological-machinery phase. After Phases 0, 1, and 2, its scope had narrowed sharply. The goals were now to:
1. derive the actual physical topological charge carried by the `u` sector,
2. determine whether that charge survives the spacetime lift,
3. test whether the default scalar-angle lift kills topology,
4. and decide whether the "knotted spacetime" path remains alive or has to be reformulated.

The updated Phase 3 scope is recorded in [2026-04-03_khantraction_restart_plan.md](/home/mcesel/.openclaw/workspace/projects/physics/notes/2026-04-03_khantraction_restart_plan.md).

## Method
Phase 3 used three linked methods.

### 1. Exact topological derivation
The phase derived:
- the physical degree density of a unit-quaternion field,
- the angle-space density `J_ang`,
- the scalar-angle pullback formula for the physical density,
- and the null-homotopy theorem for the globally regular scalar-angle lift.

Primary derivation:
- [phase_03_topological_machinery.md](/home/mcesel/.openclaw/workspace/projects/physics/derivations/phase_03_topological_machinery.md)

### 2. Direct angle-space scans
The phase directly sampled the angle-space density and chart-coverage criteria for:
- the two existing periodic families,
- the lifted diagnostic family,
- and a new admissible periodic topology-ready family with enough component amplitude to cover the logarithm ball.

### 3. Direct physical-space benchmarks
The phase then compared:
- direct S1 smooth scalar-angle benchmark maps,
- against a direct S2 degree-one unit-quaternion benchmark.

That is the correct method because the topological question is no longer just local. It depends on the actual physical-space lift.

## Main Derivational Results

### 1. Physical degree density
For a unit-quaternion field `u : S^3 -> S^3`, the natural topological charge is the degree

```text
deg(u) = ∫ (1 / 2 pi^2) det[u, partial_x u, partial_y u, partial_z u] d^3x.
```

This is the physically relevant topological quantity for the `u` sector.

### 2. Exact angle-space density
For the angle-space map,

```text
J_ang = det[u, partial_theta u, partial_phi u, partial_rho u]
      = (sin(R)/R)^2 b'(theta) c'(phi) d'(rho).
```

So the angle-space topological avenue is locally real whenever this density is nonzero.

### 3. Exact null-homotopy obstruction for the scalar-angle lift
If

```text
u(x) = exp(X(x)),
X : S^3 -> R^3
```

with `X` globally continuous, then

```text
u_t(x) = exp(t X(x))
```

is an explicit homotopy to the constant map. Therefore:

```text
deg(u) = 0
```

for the globally regular scalar-angle lift.

This is the decisive Phase 3 result.

Support:
- [phase_03_topological_machinery.md](/home/mcesel/.openclaw/workspace/projects/physics/derivations/phase_03_topological_machinery.md)

Goal status: met.

## Main Numerical Results

### 1. The angle-space density is genuinely nonzero
The directly sampled angle-space density is nonzero for the live families:
- `periodic_simple`
  - `max_abs_J_ang = 10.648000000000005`
- `periodic_harmonic`
  - `max_abs_J_ang = 35.90400000000002`
- `periodic_topology_ready`
  - `max_abs_J_ang = 42.87500000000001`

The direct determinant formula and the sampled determinant agree to numerical precision:
- `formula_abs_error_max` is at most `1.4210854715202004e-14` for the tested families.

So Phase 2 was right to keep the topological avenue alive locally.

Support:
- [angle_space_topology_anchor_samples.csv](/home/mcesel/.openclaw/workspace/projects/physics/solutions/phase_3/phase_3_topology/angle_space_topology_anchor_samples.csv)
- [topology_convergence_summary.csv](/home/mcesel/.openclaw/workspace/projects/physics/solutions/phase_3/phase_3_topology/topology_convergence_summary.csv)
- [named_anchor_topology_table.csv](/home/mcesel/.openclaw/workspace/projects/physics/solutions/phase_3/phase_3_topology/named_anchor_topology_table.csv)

Goal status: met.

### 2. Most tested families do not have full single-chart `S^3` coverage
The single-chart coverage table shows:
- `periodic_simple`
  - `ball_pi_contained = false`
- `periodic_harmonic`
  - `ball_pi_contained = false`
- `lifted_chart_linear`
  - `ball_pi_contained = false`

So these families cannot even cover the full logarithm ball in one global chart.

However:
- `periodic_topology_ready`
  - `ball_pi_contained = true`
  - `single_chart_surjective_to_S3 = true`

This matters because it shows the admissible periodic class itself does not forbid full single-chart reach. The actual decisive killer is not coverage. It is the scalar-angle null-homotopy obstruction.

Support:
- [topology_chart_coverage.csv](/home/mcesel/.openclaw/workspace/projects/physics/solutions/phase_3/phase_3_topology/topology_chart_coverage.csv)

Goal status: met.

### 3. Route S1 smooth scalar-angle benchmarks integrate to near zero degree
The direct S1 scalar-angle benchmark maps all produce near-zero integrated degree:
- `cartesian_decay`
  - `-0.0007261940343658896` at `33^3`
  - `-0.0003294868465552811` at `49^3`
- `mixed_polynomial`
  - `1.0005576689441423e-19` at `33^3`
  - `-2.0095856673608276e-19` at `49^3`
- `trig_swirl`
  - `-0.01217691033183402` at `33^3`
  - `-0.005753342850588188` at `49^3`

This is exactly what the null-homotopy theorem predicts.

Support:
- [physical_topology_benchmarks.csv](/home/mcesel/.openclaw/workspace/projects/physics/solutions/phase_3/phase_3_topology/physical_topology_benchmarks.csv)

Goal status: met.

### 4. A direct unit-quaternion benchmark carries nonzero degree
The direct S2 hedgehog benchmark gives integrated degree values that converge toward `-1`:
- `33^3`: `-0.8544390798849802`
- `49^3`: `-0.9289226204920789`
- `65^3`: `-0.9572477795220055`

So the `u` sector is topologically capable when treated as fundamental.

Support:
- [physical_topology_benchmarks.csv](/home/mcesel/.openclaw/workspace/projects/physics/solutions/phase_3/phase_3_topology/physical_topology_benchmarks.csv)

Goal status: met.

### 5. The global logarithm is singular near a nontrivial topological core
For the direct S2 degree-one benchmark, the principal-log shell spread remains large near the core:
- at resolution `65`, shell radius `0.15`
  - `log_vector_spread = 2.7708967535984037`
- at resolution `65`, shell radius `0.30`
  - `log_vector_spread = 2.7708967535984037`

So the direct benchmark confirms what the derivation predicts:
- a nontrivial topological `u` field does not admit a globally regular scalar-angle logarithm.

Support:
- [principal_log_singularity_shells.csv](/home/mcesel/.openclaw/workspace/projects/physics/solutions/phase_3/phase_3_topology/principal_log_singularity_shells.csv)

Goal status: met.

## What Phase 3 Proves
Phase 3 proves the following.

1. The `u` sector is the correct location of any real Khantraction topology.
2. The angle-space topological density is genuinely nonzero, so the local topological avenue is real.
3. The globally regular scalar-angle lift kills nonzero topology exactly.
4. Nontrivial topology survives only if:
   - `u` is treated as a fundamental field,
   - or the angle representation becomes multi-chart or singular.

## What Phase 3 Retires
Phase 3 retires the strong version of the claim:

> globally regular scalar angles directly realize knotted spacetime sectors.

That route is dead.

## Overall Assessment
Phase 3 changes the program materially.

Alive:
- topology through the fundamental unit-quaternion route,
- and possibly through a carefully tracked multi-chart or singular-angle construction.

Dead:
- topology through the default globally regular scalar-angle lift.

So the next phase cannot proceed as if the scalar-angle fields are enough. If Khantraction is going to retain a knotted interpretation at all, the program now has to elevate `u` itself to fundamental status.

## Supporting Files
- [phase_03_topological_machinery.md](/home/mcesel/.openclaw/workspace/projects/physics/derivations/phase_03_topological_machinery.md)
- [phase_3_topological_machinery.py](/home/mcesel/.openclaw/workspace/projects/physics/analysis/phase_3/phase_3_topological_machinery.py)
- [phase_3_topology_assessment.md](/home/mcesel/.openclaw/workspace/projects/physics/notes/phase_3/phase_3_topology_assessment.md)
- [summary.json](/home/mcesel/.openclaw/workspace/projects/physics/solutions/phase_3/phase_3_topology/summary.json)
- [summary.md](/home/mcesel/.openclaw/workspace/projects/physics/solutions/phase_3/phase_3_topology/summary.md)
