# Notes: Khantraction Restart Plan

## Starting Thesis Under Test
- Empty spacetime can be driven into a localized contracted or knotted configuration by energy injection.
- The internal shape of that contracted region is encoded by an exponential quaternion field,
  `q(omega, theta, phi, rho) = exp(a(omega) + b(theta) i + c(phi) j + d(rho) k)`.
- The research task is to determine whether this can become a direct classical particle-level model, not just a geometric metaphor.

## Key Mathematical Observations

### Exponential-quaternion split
- `omega, theta, phi, rho` are angle variables.
- `a, b, c, d` are scalar functions of those angle variables.
- At the restart stage, the ansatz is a map on angle space, not yet a spacetime field.
- Any later move from `q(omega, theta, phi, rho)` to a spacetime-dependent object must be derived explicitly rather than assumed.
- Let
  - `alpha = a(omega)`
  - `beta = b(theta)`
  - `gamma = c(phi)`
  - `delta = d(rho)`
- Then
  - `V = beta i + gamma j + delta k`
  - `R = sqrt(beta^2 + gamma^2 + delta^2)`
  - `q = e^alpha [cos(R) + (V/R) sin(R)]` for `R != 0`
- This immediately suggests that the ansatz may collapse many nominal angle labels into:
  - one overall scale `e^alpha`
  - one rotation size `R`
  - one unit internal direction `V / R`
- That possible collapse is a core risk and must be tested before making species claims.

### Practical scan consequence
- All four inputs `omega, theta, phi, rho` are angular variables for the purpose of the restart program.
- The default exploration domain is `[-2pi, 2pi]` for each angle, matching the user-required exhaustive scan range.
- Any later reduction of that angular domain must be derived and documented; it cannot be assumed.

## Planning Outcomes

### Non-negotiable method rules
- Direct derivation only.
- Direct numerical solves only.
- No proxy or surrogate dynamics.
- Every solution package must contain a `summary.md`.
- Every phase must end with an explicit gate: advance, revise, or retire the claim.

### Phase structure chosen
- Foundation and specification
- Quaternion kinematics
- Direct action families
- Topological machinery
- Static direct solutions
- Self-gravitating direct solutions
- Linear and nonlinear stability
- Transport and two-body interaction
- Vacuum injection / creation / emission only after core viability
- Final viability decision

## Phase 0 Findings
- The formal specification packet is now on disk.
- The canonical anchor is fixed at `(0, 0, 0, 0)` with `q = 1`.
- The exhaustive scan contract is fixed for all subset families.
- The first hard restriction is now explicit:
  - `|q| = exp(a(omega))`
  - therefore norm-only models cannot distinguish `theta`, `phi`, and `rho`.
- This means Phase 1 and Phase 2 must focus on non-norm structure if the model is going to retain any particle-species ambition.

## Phase 1 Findings
- The Phase 1 derivation and direct scan packet are now on disk.
- The exact Jacobian determinant is fixed:
  - `det(J) = exp(4 a(omega)) (sin(R)/R)^2 a'(omega) b'(theta) c'(phi) d'(rho)`
- Periodic admissible families collapse heavily on the required 11-anchor lattice:
  - `14641` total points
  - `1080` unique quaternion classes
  - redundancy ratio `0.9262345468205724`
  - `625` vacuum-equivalent anchor points
- The lifted non-periodic diagnostic family removes the large periodic preimage collapse but still shows the intrinsic exponential singular-sheet structure:
  - `22` rank-2 anchor points
  - `22` singular-sheet hits
  - `2` sign-flip anchor points
- Pointwise raw angle labels are not identity invariants.
- The viable survival path is now narrower:
  - non-norm direct action structure,
  - topology,
  - geometry,
  - or the spacetime lift.

## Phase 2 Findings
- The restart plan Phase 2 goals were updated to match the Phase 0 and Phase 1 constraints.
- Norm-only and scale-only curvature routes are now explicitly retired as particle-species routes.
- The direct surviving core routes are:
  - full quaternion sigma,
  - split sigma,
  - split sigma plus Skyrme stabilization.
- The strongest current route is the split sigma plus Skyrme family.
- Direct sampled maxima:
  - `periodic_simple`
    - `max_trace_u = 14.520000000000003`
    - `max_skyrme_density = 70.27680000000002`
    - `max_abs_topological_density = 10.648000000000005`
  - `periodic_harmonic`
    - `max_trace_u = 32.690000000000005`
    - `max_skyrme_density = 355.77640000000014`
    - `max_abs_topological_density = 35.90400000000002`
- The nonzero angle-space topological density keeps the topological route alive, but it is not yet a physical conserved charge. That remains the job of Phase 3.

## Phase 3 Findings
- The restart plan Phase 3 scope was updated before implementation.
- Exact obstruction:
  - a globally regular scalar-angle lift `u(x) = exp(X(x))` with continuous `X : S^3 -> R^3` is null-homotopic
  - therefore the physical topological degree is exactly zero on that route
- The angle-space density remains nonzero:
  - `periodic_simple`: `max_abs_J_ang = 10.648000000000005`
  - `periodic_harmonic`: `max_abs_J_ang = 35.90400000000002`
  - `periodic_topology_ready`: `max_abs_J_ang = 42.87500000000001`
- Direct S2 benchmark degree values converge toward `-1`:
  - `-0.8544390798849802`
  - `-0.9289226204920789`
  - `-0.9572477795220055`
- Direct S1 smooth scalar-angle benchmark degrees stay near zero.
- The scalar-angle topological path is dead.
- The topological survival path now requires:
  - `u` as a fundamental field,
  - or a tracked multi-chart / singular-angle construction.

## Deliverable Saved
- `notes/2026-04-03_khantraction_restart_plan.md`
- `summary/2026-04-03_phase_0_closure_summary.md`
- `summary/2026-04-03_phase_1_closure_summary.md`
- `summary/2026-04-03_phase_2_closure_summary.md`
- `summary/2026-04-03_phase_3_closure_summary.md`
