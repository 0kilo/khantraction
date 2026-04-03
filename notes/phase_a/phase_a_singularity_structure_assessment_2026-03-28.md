# Phase A Assessment — Singularity Structure of the Ordered Map

**Date:** 2026-03-28  
**Phase:** A — Parameter foundation  
**Status:** Complete supporting assessment

## Purpose

This note isolates the singularity architecture of the ordered quaternion chart on the active Phase A domain.

The exact question is:

> which variable controls the loss of local angular-coordinate independence, and does that structure survive on the full unquotiented box $\theta,\phi,\rho\in[-2\pi,2\pi]$?

## Method

The supporting derivation and analysis are:

- `derivations/derivation_72_phase_a_jacobian_singularity_structure.md`
- `analysis/phase_a/phase_a_singularity_structure.py`

The regenerated solution set performs three checks:

1. a full active-domain determinant scan over 55,539 sampled points,
2. a fixed-$(\theta,\rho)$ phi slice,
3. and a unit-scale candidate-factor check comparing `detJ` directly to `cos(2phi)`.

## Results

### 1. The determinant law is numerically stable on the active domain

Across the active-domain scan, the determinant matches

$$
\det J = e^{4\omega}\cos(2\phi)
$$

with maximum absolute discrepancy

$$
3.979039320256561\times10^{-13}.
$$

The supplementary unit-scale factor check contains 71,825 rows and finds a maximum absolute error of

$$
9.992007221626409\times10^{-16}
$$

between `detJ` and `cos(2phi)` at $\omega=0$.

### 2. The singular condition depends on $\phi$ alone

The singular slices occur when

$$
\cos(2\phi)=0
\quad\Longleftrightarrow\quad
\phi=\frac{\pi}{4}+\frac{n\pi}{2}.
$$

Inside the active working box, that gives the repeated slices

- $\phi=\pm\pi/4$
- $\phi=\pm 3\pi/4$
- $\phi=\pm 5\pi/4$
- $\phi=\pm 7\pi/4$

The `phi_reference_table.json` file shows the expected alternation `detJ = +1, 0, -1, 0, ...` at the canonical reference values.

### 3. Widening the box reveals repetition, not a new singular law

The larger unquotiented domain does not alter the determinant rule.
It only exposes repeated copies of the same singular-sheet architecture across multiple periods.

## Assessment

This is the precise Phase A statement supported by the evidence:

1. $\omega$ rescales determinant magnitude through $e^{4\omega}$.
2. $\phi$ controls where the ordered chart loses local angular rank.
3. The repeated singular sheets belong to the chart geometry itself, not to a newly discovered object-class hierarchy.

That is the strongest disciplined reading of the singular data.

## Limits

This note does **not** show that $\phi$ is a dynamically dominant field variable.

It shows only:

> in the ordered coordinate chart, $\phi$ is the variable that governs singularity placement and the local collapse of angular-coordinate independence.

## Evidence

- `derivations/derivation_72_phase_a_jacobian_singularity_structure.md`
- `analysis/phase_a/phase_a_singularity_structure.py`
- `solutions/phase_a/phase_a_singularity_structure/candidate_factor_check.csv`
- `solutions/phase_a/phase_a_singularity_structure/domain_singular_points.json`
- `solutions/phase_a/phase_a_singularity_structure/phi_reference_table.json`
- `solutions/phase_a/phase_a_singularity_structure/phi_slice_table.csv`
- `solutions/phase_a/phase_a_singularity_structure/summary.md`
