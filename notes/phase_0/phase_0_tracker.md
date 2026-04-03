# Phase 0 Tracker

## Status
- Phase 0 specification packet: closed
- Boundary-condition framework: closed
- Exhaustive scan protocol: closed
- Machine-readable artifacts: closed
- Phase 0 closure summary: closed

## Locked Decisions
- Starting object: `q(omega, theta, phi, rho) = exp(a(omega) + b(theta) i + c(phi) j + d(rho) k)`
- `omega, theta, phi, rho` are angles
- `a, b, c, d` are scalar functions
- canonical anchor: `(0, 0, 0, 0)` with `q = 1`
- default angle domain: `[-2pi, 2pi]` in each coordinate
- no proxy dynamics allowed anywhere in the restart program

## Immediate Structural Warning
- `|q| = exp(a(omega))`
- therefore norm-only models are blind to `theta`, `phi`, and `rho`

## Open Questions for Phase 1
1. How large is the vacuum-equivalent set beyond the canonical anchor?
2. Under what conditions do distinct angle tuples map to the same `q`?
3. Can periodic admissible function classes preserve any nontrivial invariant classes?
4. Does the unit quaternion part `u` support real topological separation before spacetime is introduced?
