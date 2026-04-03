# Phase 0 Solution Summary

Phase 0 does not contain numerical solution data. It fixes the mathematical and workflow contract that all later phases must obey.

## What was established
- The restart object is the angle-space map
  - `q(omega, theta, phi, rho) = exp(a(omega) + b(theta)i + c(phi)j + d(rho)k)`.
- `omega, theta, phi, rho` are angles.
- `a, b, c, d` are scalar functions.
- The canonical reference anchor is `(0, 0, 0, 0)` with `q = 1`.
- The mandatory scan domain is `[-2pi, 2pi]` in each angle.
- Every later phase must cover the full family matrix of variable subsets.

## Most important structural result
- The quaternion exponential norm collapses to
  - `|q| = exp(a(omega))`.
- Therefore any future theory built only from `|q|` is automatically blind to `theta`, `phi`, and `rho`.

## Why this matters
- It narrows the viable direct-theory space immediately.
- If Khantraction is going to support genuine particle-like distinctions, they must come from:
  - non-norm structure,
  - derivative couplings,
  - topology,
  - geometry,
  - or boundary-condition structure.

## Artifacts in this phase
- `scan_anchor_sets.json`
- `scan_family_matrix.csv`
- `specification_snapshot.json`

## Phase 0 disposition
- Goal status: met
- Next phase: Phase 1, quaternion kinematics and redundancy analysis
