# Phase K Direct Interaction Summary

**Date:** 2026-04-02
**Phase:** K — Multi-Particle Interactions
**Data Source:** `analysis/phase_k/phase_k_multi_fold_force_law.py`

## Overview
This package replaces the old one-dimensional overlap proxy with a direct 3D interaction-energy computation for same-background pair initial data.

## Direct interaction-energy ranges
- scalar pair `Delta M(D)` range: [0.00031189491732663735, 0.0003726299482008006]
- rich pair `Delta M(D)` range: [0.00031189491732663735, 0.0003726299482008006]
- phi-offsheet pair `Delta M(D)` range: [0.00031189491732663735, 0.0003726299482008006]

## Distance scaling
- scalar force log-log slope: 0.8301296117826079
- scalar power-fit linear-space R^2: 0.9910489533515593
- scalar exponential-fit linear-space R^2: 0.9673762664064315

Interpretation: Phase K now has a real 3D interaction-energy dataset for the directly defined same-background case. But the refreshed direct data are species-blind across scalar, rich, and off-sheet same-background pairs. The remaining open gaps are both a mathematically clean mixed-background multi-species composition law and any direct evidence that different internal species interact differently.

## Bottom line
Phase K now supports a narrower but substantially stronger claim than the old proxy version: same-background pair initial data have a direct 3D interaction-energy density and an extractable force gradient. But the current direct runtime produces the same interaction data for scalar, rich, and off-sheet families, so it does not support particle-species interaction structure. What remains open is whether mixed-background species comparisons and Standard-Model-like polarity rules can be defined without additional many-object composition machinery.
