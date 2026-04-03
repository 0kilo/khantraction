# Phase A Assessment — Role Stability Stress Test

**Date:** 2026-03-28  
**Phase:** A — Parameter foundation  
**Status:** Complete supporting assessment

## Purpose

This note tests whether the emerging Phase A role picture is stable across a wider positive-$\omega$ range and a broader sample of the active angle box.

The hypothesis under test is:

- $\omega$ = scale only
- $\phi$ = separator / mixing controller
- $\theta,\rho$ = paired internal directions

## Method

Supporting analysis:

- `analysis/phase_a/phase_a_role_stability_stress_test.py`

Supporting solution artifacts:

- `stress_scan.csv`
- `stress_summary.json`
- `omega_scaling_check.csv`

The stress scan samples five positive $\omega$ values and a broad coarse grid of $(\theta,\phi,\rho)$ values on the active box.

## Results

### 1. Norm equality survives the full stress scan

The stress scan contains 26,325 rows and finds

$$
\text{max norm difference across channels} =
1.7763568394002505\times10^{-15}.
$$

So the angular channels remain equal in norm across the sampled positive-$\omega$ range to floating-point precision.

### 2. Phi stays orthogonal while theta-rho spans the full range

The same stress scan finds:

- `max abs cos(theta,phi) = 9.567545344253569e-32`
- `max abs cos(phi,rho) = 9.567545344253569e-32`
- `min cos(theta,rho) = -1.0000000000000004`
- `max cos(theta,rho) = 1.0000000000000004`

So the role hierarchy from the earlier Phase A steps is not local or accidental.
It survives the broader stress test.

### 3. Omega scaling remains exact across the sampled range

The dedicated `omega_scaling_check.csv` file verifies at one fixed angular point that

$$
\|\partial_\theta Q\|=\|\partial_\phi Q\|=\|\partial_\rho Q\|=e^\omega
$$

across

$$
\omega\in\{0.1,0.25,0.5,0.75,1.0,1.5,2.0,2.5\}.
$$

The recorded norm errors are zero or machine-noise-sized at every sampled value.

## Assessment

This note closes the adversarial check on the Phase A role picture:

1. $\omega$ continues to behave as a pure scale coordinate.
2. $\phi$ continues to behave as the orthogonal separator.
3. $\theta$ and $\rho$ continue to form the active paired subsystem.

So the Phase A role interpretation is stable across the sampled positive-$\omega$ range, not just at one favored point.

## Evidence

- `analysis/phase_a/phase_a_role_stability_stress_test.py`
- `solutions/phase_a/phase_a_role_stability_stress_test/stress_scan.csv`
- `solutions/phase_a/phase_a_role_stability_stress_test/stress_summary.json`
- `solutions/phase_a/phase_a_role_stability_stress_test/omega_scaling_check.csv`
- `solutions/phase_a/phase_a_role_stability_stress_test/summary.md`
