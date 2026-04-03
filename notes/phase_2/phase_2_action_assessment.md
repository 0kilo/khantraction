# Phase 2 Assessment

## Verdict
Phase 2 is complete.

## What Phase 2 established

### 1. Norm-only action families are retired as particle-species routes
This is now settled both derivationally and numerically.

Derivationally:

```text
|q| = exp(a(omega))
```

so any action depending only on `|q|` can only see the `omega` channel.

Numerically:
- every tested family classifies `A0_norm_only` as `retired_for_species`,
- every tested family classifies `A4_curvature_scale_only` as `retired_for_species`.

### 2. The full quaternion and split routes survive
The direct surviving routes are:
- `A1_full_quaternion_sigma`,
- `A2_split_sigma`,
- `A3_split_sigma_skyrme`.

These survive because they retain non-norm derivative structure.

### 3. The strongest current route is the split sigma plus Skyrme route
This route survives for the strongest reason:
- non-norm angular sensitivity,
- nontrivial kinetic rank,
- nonzero quartic Maurer-Cartan density,
- and nonzero candidate topological density on the sampled domain.

For the tested families:
- `periodic_simple`
  - `max_trace_u = 14.520000000000003`
  - `max_skyrme_density = 70.27680000000002`
  - `max_abs_topological_density = 10.648000000000005`
- `periodic_harmonic`
  - `max_trace_u = 32.690000000000005`
  - `max_skyrme_density = 355.77640000000014`
  - `max_abs_topological_density = 35.90400000000002`
- `lifted_chart_linear`
  - `max_trace_u = 0.7550000000000001`
  - `max_skyrme_density = 0.18750625000000007`
  - `max_abs_topological_density = 0.12375000000000001`

### 4. The curvature-split and frame/connection routes remain open, but not solved
- `A5_curvature_split` survives as `viable_but_unresolved`.
- `A6_frame_connection` survives as `structurally_incomplete`.

That is the correct status. There is enough nontrivial structure to keep them alive, but not enough direct specification yet to solve them.

## Important Phase 2 restraint
The nonzero angle-space topological density is **not yet** a physical conserved charge.

Phase 2 only proves that the unit-quaternion route has a live topological avenue. Phase 3 still has to derive:
- the correct physical-space map,
- the admissible boundary conditions,
- and the actual conserved charge.

## Next action
Proceed to Phase 3.

Phase 3 should now focus on the `u` sector:
1. derive the real topological candidate,
2. determine whether it survives the spacetime lift,
3. and test whether distinct sectors are dynamically protected rather than just kinematically nontrivial.
