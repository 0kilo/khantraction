# Phase I Direct Pullback Runtime Summary

**Date:** 2026-04-02
**Phase:** I — First-Principles Derivation of Constants
**Data Source:** `analysis/phase_i/phase_i_geometric_anisotropy_scan.py`

## Overview
This package now does more than scan the pullback geometry.
It keeps the exact pullback eigenvalue study, adds a direct ordered-variable radial runtime, and uses that runtime as the coefficient bridge for downstream Phases J, E, and K.

## Geometry results
- `lambda_phi` stays constant at `e^(2omega) = 2.718281828459045` for fixed `omega = 0.5`.
- maximum regular sampled anisotropy ratio on the dense phi sweep: 101320.51697625456
- active-scale paired-mode gap at `phi = pi/8`: 3.844231028159116

## Direct runtime bridge
- direct profile success count on the representative seed set: 3
- direct profile mass spread across scalar/rich/off-sheet seeds: 0.0
- direct profile compactness-90 spread across scalar/rich/off-sheet seeds: 0.0
- downstream direct-runtime phases now import the exact pullback metric and Christoffel symbols from `analysis/direct_ordered_manifold.py`.
- the old exploratory `beta_a` coefficients are not used in that new chain.

## Branch-stability scan
- regular branch candidate count on the `(lambda_q, A0)` scan: 16
- regular candidate lambda range: [0.005, 0.04]
- regular candidate central-amplitude range: [0.01, 0.04]

Interpretation: Phase I now supports a real coefficient replacement claim for the new direct runtime. The exact pullback geometry is no longer only an interpretation layer; it is the active kinetic structure used downstream. But the direct representative seed set is degenerate in mass and compactness, so coefficient replacement alone does not reproduce the exploratory trait splitting. The self-coupling scan is still empirical and does not yet amount to a full analytical stability bound.

## Bottom line
Phase I now closes at a stronger level than the audit-only version. The exact pullback anisotropy remains the controlling geometric mechanism, and the new direct runtime uses that mechanism in place of the exploratory beta-coefficient path. But the resulting direct representative profiles remain degenerate, so the new chain supports universal objecthood rather than distinct particle-like species. What remains open is a full analytical self-coupling derivation and a sharper mapping from those direct coefficients to physical observables.
