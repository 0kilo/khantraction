# Phase A Assessment — Explicit 1D and 2D Slice Studies

**Date:** 2026-03-28  
**Phase:** A — Parameter foundation  
**Status:** Complete supporting assessment

## Purpose

This note records the slice-study results required by the Phase A analysis protocol.

The governing question is:

> when the ordered map is viewed through explicit 1D and 2D slices, which variable drives singular collapse and which variables remain regular when $\phi$ is held away from its singular values?

## Method

Supporting analysis:

- `analysis/phase_a/phase_a_slice_studies.py`

The solution set includes:

- six 1D slices,
- four 2D slices,
- and JSON summaries that count singular points on each slice.

This is the direct implementation of the plan requirement that Phase A use both 1D and 2D slice studies rather than only bulk scans.

## Results

### 1. Phi sweeps expose repeated singular crossings directly

For both `vary_phi_theta0_rho0` and `vary_phi_theta1.1_rho-0.9`:

- `singular_count = 8`
- `min_abs_detJ = 0.0`

So sweeping $\phi$ across the active interval crosses the repeated singular sheets exactly as expected.

### 2. Theta and rho sweeps remain regular at regular phi

For both `vary_theta_phi0_rho0` and `vary_rho_theta0_phi0`:

- `singular_count = 0`
- `min_abs_detJ = 20.085536923187664`

That means varying $\theta$ or $\rho$ alone does not force singular collapse when $\phi$ is fixed at a regular value.

### 3. The theta-rho plane collapses completely at $\phi=\pi/4$

The clearest 2D comparison is:

- `theta_rho_phi0`: `0 / 1089` singular points
- `theta_rho_phi_pi4`: `1089 / 1089` singular points

Likewise, the 1D slices `vary_theta_phi_pi4_rho0` and `vary_rho_theta0_phi_pi4` are singular at all 65 sampled points.

So the paired $(\theta,\rho)$ subsystem is fully regular at $\phi=0` and fully collapsed at $\phi=\pi/4`.

## Assessment

The slice studies make the Phase A role picture concrete:

1. $\phi$ is the variable that decides whether the $\theta$-$\rho$ subsystem remains locally distinct.
2. $\theta$ and $\rho$ vary regularly when $\phi$ is regular.
3. The repeated singular sheets are visible directly in 1D and 2D views, not only in bulk determinant scans.

That is exactly the kind of transparent geometric evidence Phase A needed.

## Evidence

- `analysis/phase_a/phase_a_slice_studies.py`
- `solutions/phase_a/phase_a_slice_studies/one_d_summary.json`
- `solutions/phase_a/phase_a_slice_studies/two_d_summary.json`
- `solutions/phase_a/phase_a_slice_studies/vary_theta_phi0_rho0.csv`
- `solutions/phase_a/phase_a_slice_studies/vary_phi_theta0_rho0.csv`
- `solutions/phase_a/phase_a_slice_studies/vary_rho_theta0_phi0.csv`
- `solutions/phase_a/phase_a_slice_studies/vary_theta_phi_pi4_rho0.csv`
- `solutions/phase_a/phase_a_slice_studies/vary_rho_theta0_phi_pi4.csv`
- `solutions/phase_a/phase_a_slice_studies/vary_phi_theta1.1_rho-0.9.csv`
- `solutions/phase_a/phase_a_slice_studies/theta_phi_rho0.csv`
- `solutions/phase_a/phase_a_slice_studies/theta_rho_phi0.csv`
- `solutions/phase_a/phase_a_slice_studies/phi_rho_theta0.csv`
- `solutions/phase_a/phase_a_slice_studies/theta_rho_phi_pi4.csv`
- `solutions/phase_a/phase_a_slice_studies/summary.md`
