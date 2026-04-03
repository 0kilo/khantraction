# Phase A Assessment — Less Chart-Bound Channel Comparison

**Date:** 2026-03-28  
**Phase:** A — Parameter foundation  
**Status:** Complete supporting assessment

## Purpose

This note checks whether the angular asymmetry survives in diagnostics that are less tied to raw determinant-zero language.

The specific question is:

> do the three angular channels remain equal in norm while differing in angular conditioning and overlap structure?

## Method

Supporting analysis:

- `analysis/phase_a/phase_a_invariant_channel_comparison.py`

The analysis constructs the angular Gram matrix from the Jacobian columns $(\partial_\theta Q,\partial_\phi Q,\partial_\rho Q)$ and records:

- channel norms,
- pairwise cosines,
- Gram-matrix singular values,
- and the resulting condition number.

Three scans are compared:

1. a `phi_scan`,
2. a `theta_scan_phi0`,
3. a `rho_scan_phi0`.

## Results

### 1. Norm equality survives all scans

Across the named points and scan data, the three angular channels keep equal norm.

At the representative scaled regular points, all three norms are

$$
2.117000016612675
$$

to numerical precision.

So the asymmetry is not a norm hierarchy.

### 2. Phi is the channel that changes conditioning

The `phi_scan.csv` results show:

- `min sigma_min = 0.0`
- `max condition = 100458282.95159373`

By contrast, both `theta_scan_phi0.csv` and `rho_scan_phi0.csv` show:

- `min sigma_min = 2.117000016612675`
- `max condition = 1.0`

That means varying $\phi$ can collapse the smallest singular value, while varying $\theta$ or $\rho$ at regular $\phi$ leaves the angular tangent spectrum perfectly isotropic.

### 3. Named points confirm the same pattern

At the regular generic point:

- `cos(theta,rho) = 0.5646424733950354`
- `sigma_min = 1.3968310809381657`
- `condition = 1.8957651228540087`

At the singular $\phi=\pi/4$ and $\phi=3\pi/4$ points:

- `cos(theta,rho) = ±1`
- `sigma_min ≈ 2.98e-08`
- `condition ≈ 1.00e8`

So the singular-value picture and the overlap picture tell the same story.

## Assessment

This note supports the stronger mapping-level interpretation:

1. the channels are equal in norm,
2. the asymmetry lives in overlap and conditioning,
3. and $\phi$ is the channel that controls when the angular tangent bundle becomes badly conditioned or singular.

That is more robust than relying on determinant language alone.

## Limits

These diagnostics are still chart-derived.
They are more geometric than raw determinant zeros, but they are not yet field-equation or observable-level evidence.

## Evidence

- `analysis/phase_a/phase_a_invariant_channel_comparison.py`
- `solutions/phase_a/phase_a_invariant_channel_comparison/phi_scan.csv`
- `solutions/phase_a/phase_a_invariant_channel_comparison/theta_scan_phi0.csv`
- `solutions/phase_a/phase_a_invariant_channel_comparison/rho_scan_phi0.csv`
- `solutions/phase_a/phase_a_invariant_channel_comparison/named_points.json`
- `solutions/phase_a/phase_a_invariant_channel_comparison/summary.md`
