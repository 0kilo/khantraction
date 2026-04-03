# Phase 2 Closure Summary

## Status
Closed.

## Phase Goal
Phase 2 was the direct action-family phase. After Phases 0 and 1, its goals had to be updated to reflect what was already known:
1. build mathematically explicit direct theories starting from the ansatz,
2. reject norm-only species claims immediately,
3. identify which action families still preserve a plausible path to nontrivial identity,
4. classify each avenue as retired, viable core, viable but unresolved, or structurally incomplete.

The updated Phase 2 goals are now recorded in [2026-04-03_khantraction_restart_plan.md](/home/mcesel/.openclaw/workspace/projects/physics/notes/2026-04-03_khantraction_restart_plan.md).

## Method
Phase 2 used two linked methods.

### 1. Direct derivation of candidate action families
The phase derived the action-building structures that survive the Phase 0 and Phase 1 restrictions:
- norm-only channel `N = |q|`,
- full quaternion derivative structure,
- split `q = e^alpha u` structure,
- Maurer-Cartan current `L_mu = u^-1 partial_mu u`,
- quartic Skyrme-type density,
- and a candidate angle-space topological density.

Primary derivation:
- [phase_02_direct_action_families.md](/home/mcesel/.openclaw/workspace/projects/physics/derivations/phase_02_direct_action_families.md)

### 2. Direct numerical classification on the required angle domain
The phase then evaluated the candidate structures on the required `[-2pi, 2pi]^4` domain using:
- the full 11-anchor lattice,
- the full hold/vary subset-family protocol,
- named-anchor action tables,
- and convergence summaries for the action-building observables.

Primary analysis:
- [phase_2_action_family_analysis.py](/home/mcesel/.openclaw/workspace/projects/physics/analysis/phase_2/phase_2_action_family_analysis.py)
- [run_phase_2_action_family_analysis.sh](/home/mcesel/.openclaw/workspace/projects/physics/scripts/run_phase_2_action_family_analysis.sh)

## Main Derivational Results

### 1. Norm-only actions are angle-blind
The norm channel is

```text
N = |q| = exp(a(omega)).
```

So an action depending only on `N` or its derivatives can only see the `omega` channel. That immediately retires:
- the minimal norm-only species route,
- and any curvature-coupled route that still only sees the norm channel.

### 2. The split `q = e^alpha u` route is the correct decomposition
Phase 2 derived

```text
q = e^alpha u,
|u| = 1,
```

and

```text
|partial_mu q|^2 = e^(2 alpha) [ (partial_mu alpha)^2 + |partial_mu u|^2 ].
```

This means the direct surviving action families are the ones that retain the `u` sector explicitly.

### 3. The quartic Maurer-Cartan term is the first live stabilizing/topological route
With

```text
L_mu = u^-1 partial_mu u,
```

the quartic density

```text
S_4 = sum_{mu < nu} |[L_mu, L_nu]|^2
```

is the first direct stabilizing/topological building block that survives the current program.

Support:
- [phase_02_direct_action_families.md](/home/mcesel/.openclaw/workspace/projects/physics/derivations/phase_02_direct_action_families.md)

Goal status: met.

## Main Numerical Results

### 1. Norm-only and scale-only curvature routes are retired
The direct classification table marks the following as retired for all tested family classes:
- `A0_norm_only`
- `A4_curvature_scale_only`

Support:
- [action_family_classification.csv](/home/mcesel/.openclaw/workspace/projects/physics/solutions/phase_2/phase_2_action_families/action_family_classification.csv)
- [action_family_catalog.json](/home/mcesel/.openclaw/workspace/projects/physics/solutions/phase_2/phase_2_action_families/action_family_catalog.json)

Goal status: met.

### 2. The non-norm direct routes survive
The direct classification table marks the following as viable core routes for every tested function family:
- `A1_full_quaternion_sigma`
- `A2_split_sigma`
- `A3_split_sigma_skyrme`

This is backed by direct nonzero sampled diagnostics such as:
- nonzero full kinetic trace,
- nonzero split kinetic trace,
- nonzero Maurer-Cartan quartic density.

For example:
- `periodic_simple`
  - `max_trace_full = 29.23968931247132`
  - `max_trace_split = 14.642500000000002`
  - `max_skyrme_density = 70.27680000000002`
- `periodic_harmonic`
  - `max_trace_full = 49.92508361061742`
  - `max_trace_split = 32.805600000000005`
  - `max_skyrme_density = 355.77640000000014`

Support:
- [summary.json](/home/mcesel/.openclaw/workspace/projects/physics/solutions/phase_2/phase_2_action_families/summary.json)
- [action_anchor_samples.csv](/home/mcesel/.openclaw/workspace/projects/physics/solutions/phase_2/phase_2_action_families/action_anchor_samples.csv)
- [named_anchor_action_table.csv](/home/mcesel/.openclaw/workspace/projects/physics/solutions/phase_2/phase_2_action_families/named_anchor_action_table.csv)

Goal status: met.

### 3. The split sigma plus Skyrme route is the strongest current avenue
The split sigma plus Skyrme route survives because it is the first route that combines:
- non-norm angular sensitivity,
- nontrivial kinetic rank,
- and a direct topological avenue.

For the periodic families, the sampled topological density is not only nonzero in magnitude; it also changes sign across the sampled domain:
- `periodic_simple`
  - `max_abs_topological_density = 10.648000000000005`
  - sign change detected: `true`
- `periodic_harmonic`
  - `max_abs_topological_density = 35.90400000000002`
  - sign change detected: `true`

The lifted diagnostic family also has a nonzero candidate topological density:
- `max_abs_topological_density = 0.12375000000000001`

Support:
- [summary.json](/home/mcesel/.openclaw/workspace/projects/physics/solutions/phase_2/phase_2_action_families/summary.json)
- [subset_action_sensitivity.csv](/home/mcesel/.openclaw/workspace/projects/physics/solutions/phase_2/phase_2_action_families/subset_action_sensitivity.csv)

Goal status: met.

### 4. The curvature-split and frame/connection routes remain alive but unresolved
The classification table marks:
- `A5_curvature_split` as `viable_but_unresolved`
- `A6_frame_connection` as `structurally_incomplete`

That is the correct status:
- both routes inherit nontrivial `u`-sector structure,
- but neither route has a fully fixed direct action principle yet.

Support:
- [action_family_classification.csv](/home/mcesel/.openclaw/workspace/projects/physics/solutions/phase_2/phase_2_action_families/action_family_classification.csv)
- [action_family_catalog.json](/home/mcesel/.openclaw/workspace/projects/physics/solutions/phase_2/phase_2_action_families/action_family_catalog.json)

Goal status: met.

## Contradiction Check
Phase 2 was checked against the main risks:
- accidentally reviving norm-only angular claims,
- confusing angle-space topological density with a physical conserved charge,
- and treating unresolved curvature or connection routes as solved.

Those risks are resolved as follows:
- norm-only angular routes are explicitly retired,
- the topological density is described only as a surviving avenue, not yet a conserved physical charge,
- and the curvature/frame routes are explicitly marked unresolved or incomplete.

## Overall Assessment
Phase 2 narrows the program correctly.

Retired:
- norm-only scalar route,
- scale-only curvature route.

Surviving core:
- full quaternion sigma,
- split sigma,
- split sigma plus Skyrme stabilization.

Still open but unresolved:
- curvature-coupled split route,
- frame/connection route.

The strongest current path is now clear:
- carry the `u` sector into Phase 3,
- derive the actual topological content of that sector,
- and determine whether the nonzero angle-space topological density becomes a real conserved physical charge after the spacetime lift.

## Supporting Files
- [phase_02_direct_action_families.md](/home/mcesel/.openclaw/workspace/projects/physics/derivations/phase_02_direct_action_families.md)
- [phase_2_action_family_analysis.py](/home/mcesel/.openclaw/workspace/projects/physics/analysis/phase_2/phase_2_action_family_analysis.py)
- [phase_2_action_assessment.md](/home/mcesel/.openclaw/workspace/projects/physics/notes/phase_2/phase_2_action_assessment.md)
- [summary.json](/home/mcesel/.openclaw/workspace/projects/physics/solutions/phase_2/phase_2_action_families/summary.json)
- [summary.md](/home/mcesel/.openclaw/workspace/projects/physics/solutions/phase_2/phase_2_action_families/summary.md)
