# Phase 1 Solution Summary

Phase 1 analyzed the quaternion map
`q(omega, theta, phi, rho) = exp(a(omega) + b(theta)i + c(phi)j + d(rho)k)`
as a pure kinematic object on the required angle domain `[-2pi, 2pi]^4`.

## What was tested
- exact redundancy structure of the quaternion exponential,
- anchor-lattice coverage on the full 11 x 11 x 11 x 11 grid,
- every hold/vary family extracted from that lattice,
- canonical high-resolution 1D scans,
- canonical convergence summaries for 1D, 2D, 3D, and 4D families,
- Jacobian ranks at every anchor point,
- Hessian diagnostics at the named regression anchors,
- sensitivity to two periodic admissible families and one lifted-chart diagnostic family.

## Main result
- The first complete pointwise invariant is the quaternion value `q` itself.
- The raw input labels `(omega, theta, phi, rho)` are not identity invariants.
- The norm is always
  - `|q| = exp(a(omega))`.
- Therefore any norm-only theory is blind to `theta`, `phi`, and `rho`.

## What the data shows
- The periodic families show large redundancy on the required anchor lattice.
- Vacuum-equivalent points recur across many angle tuples.
- Sign-flip and orientation-loss sheets appear whenever the imaginary radius reaches `R = k pi`.
- The lifted non-periodic diagnostic family retains more unique anchor classes, which shows that part of the collapse comes from the angular periodic admissibility, but not all of it. The exponential map itself remains non-injective.

## Interpretation
- The ansatz does not produce discrete particle species pointwise.
- If Khantraction is going to survive, the surviving identity must come from non-norm structure, topology, geometry, or a later spacetime lift.
- Phase 2 must reject any action that claims angular species structure while depending only on `|q|`.

## Primary artifacts
- `anchor_lattice_samples.csv`
- `subset_slice_summary.csv`
- `redundancy_class_summary.csv`
- `redundancy_pair_samples.csv`
- `vacuum_equivalent_anchor_points.csv`
- `sign_flip_anchor_points.csv`
- `named_anchor_table.csv`
- `hessian_anchor_diagnostics.csv`
- `canonical_dense_1d_scans.csv`
- `canonical_convergence_summary.csv`
- `summary.json`
