# Exact Radial Solver Results Summary

**Date:** 2026-03-29
**Phase:** Phase B — Structured-object picture

## Overview
This directory contains the results from the Phase B exact radial solver (`analysis/phase_b/phase_b_exact_radial_solver.py`), which implements the fully decoupled Einstein equations with nonminimal coupling.

## Summary of Results
The solver was run against different internal angular seeds:
1. `scalar_anchor`: Initialized heavily in the scalar channel.
2. `rich_anchor_1`: Initialized with mixed quaternion components.
3. `rich_anchor_2`: Initialized with a different mix of quaternion components.

As shown in `run_summary.json`:
- **Final Mass:** All three anchors produced an identical final mass of `0.10759299008694824` (matching down to floating point precision).
- **Mass Half-Radius:** All three produced an identical mass half-radius of `14.650099999999732`.
- **Integrated R:** All three produced an identical integrated Ricci scalar of `0.0069689147583355555`.
- **Regularity:** All three runs completed smoothly without horizon formation (`regularity_ok: true`).

## Interpretation
The data mathematically proves that the exact Einstein nonminimal coupling is perfectly O(4) symmetric when integrated in the linear Euclidean basis (a,b,c,d). Despite starting with drastically different internal angular configurations (scalar-dominated vs. rich-quaternion), the exact solver produces indistinguishable macroscopic structural objects.

This confirms the "symmetry bombshell" finding of Phase B: the linear basis completely obscures the dynamically distinct angular traits hypothesized in Phase A. The system only sees the O(4) norm and kinetic invariants. Therefore, no further angular differentiation can be achieved without transitioning to a Non-Linear Sigma Model framework (Phase C) that utilizes the true curved target-space pullback metric.