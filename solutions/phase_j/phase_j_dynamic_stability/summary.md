# Phase J Direct Ordered-Manifold Summary

**Date:** 2026-04-02
**Phase:** J — Full 3D Dynamic Stability
**Data Source:** `analysis/phase_j/phase_j_dynamic_stability_solver.py`

## Overview
This package replaces the old anchored Gaussian proxy with a direct ordered-manifold 3D wave solver in the weak-gravity limit.
The runtime uses the exact pullback metric, Christoffel couplings, and norm-potential force term from `analysis/direct_ordered_manifold.py`.

## Bulk direct evolution
- scalar energy drift: 8.364579092918004e-07
- rich energy drift: 8.364579092918004e-07
- scalar compactness-90 shift: 0.0
- rich compactness-90 shift: 0.0

Interpretation: these drifts measure whether a direct solved object remains structurally intact without an artificial anchor. In the audited window they are very small, so localized objecthood survives the direct upgrade.

## Boosted transport
- scalar centroid-x shift under direct boost: 0.0014607158466764868
- rich centroid-x shift under direct boost: 0.0014607158466764868
- scalar compactness-90 shift under boost: 0.0010330192029899266
- rich compactness-90 shift under boost: 0.0010330192029899266

Interpretation: the direct runtime now tests transport by boosting the actual field profile instead of dragging a hand-built anchor through the box. The centroid shift is small but clean, and compactness changes only weakly.

## Slice diagnostics
- theta 1D compactness-shift range: [0.030725649662316723, 0.030725649662316723]
- phi 1D compactness-shift range: [0.030725649662316723, 0.030725649662316723]
- rho 1D compactness-shift range: [0.030725649662316723, 0.030725649662316723]
- max abs compactness shift on theta/rho 2D slice: 0.02863357459338678
- max abs compactness shift on theta/phi 2D slice: 0.02863357459338678
- max abs compactness shift on phi/rho 2D slice: 0.02863357459338678

## Bottom line
Phase J now has a direct 3D ordered-manifold implementation. The direct runtime does preserve localized objecthood on the audited window, but it does not distinguish scalar and rich seeds at the level needed for discrete species identity. So J now supports direct object persistence more strongly than before, while still failing to rescue the particle-zoo claim.
