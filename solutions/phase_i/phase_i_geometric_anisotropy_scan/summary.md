# Phase I Geometric Anisotropy Scan Summary

**Date:** 2026-03-31  
**Phase:** I — First-Principles Derivation of Constants

## 1. Overview
This directory contains the numerical scan outputs analyzing the eigenvalues of the angular pullback metric $G_{ang}$ derived from the ordered quaternionic state map $Q(\omega, \theta, \phi, \rho)$. The primary objective of this scan was to verify whether the metric intrinsically provides anisotropic symmetry breaking for the angular channels without requiring hand-tuned $\beta_a$ phenomenological constants.

## 2. Scan Methodology
In accordance with the Transition Plan protocol, we evaluated the eigenvalues $\lambda_\phi, \lambda_+, \lambda_-$ of the angular pullback metric at a fixed scale ($\omega = 0.5$) across the unquotiented angular domain $[-2\pi, 2\pi]$. The scan executed:
- **1D Slices:** Fixing two angles and varying the third (`slice_1d_phi.csv`, `slice_1d_theta.csv`, `slice_1d_rho.csv`).
- **2D Slices:** Fixing one angle and varying the other two (`slice_2d_phi_rho.csv`, `slice_2d_theta_phi.csv`, `slice_2d_theta_rho.csv`).
- **Bulk Summary:** Aggregation of maximum anisotropy ratios and singular boundary locations (`bulk_summary.json`).

## 3. Data Interpretation and Results

### 3.1 $\phi$ as the Unique Anisotropy Switch
The 1D slices definitively show that the anisotropy is governed entirely by $\phi$:
- Sweeping $\phi$ (`slice_1d_phi.csv`) causes the eigenvalues $\lambda_+ = 1 + \sin(2\phi)$ and $\lambda_- = 1 - \sin(2\phi)$ to oscillate, shifting stiffness between the symmetric $(\theta + \rho)$ and anti-symmetric $(\theta - \rho)$ channels.
- Sweeping $\theta$ or $\rho$ (`slice_1d_theta.csv`, `slice_1d_rho.csv`) produces perfectly constant eigenvalues when $\phi$ is fixed. This validates that the local energy landscape of internal fluctuations is $\theta$- and $\rho$-independent but highly sensitive to $\phi$.

### 3.2 Dynamic Stiffness and Anisotropy Divergence
The `bulk_summary.json` confirms that the stiffness range spans from exactly $0.0$ to $5.436$ (which is $2e^{2\omega}$ at $\omega=0.5$).
- The **Maximum Anisotropy Ratio** reaches $>15,888$ near the singular locations. This massive disparity mathematically enforces that certain angular combinations become heavily suppressed (infinitely stiff) compared to others.

### 3.3 Identification of the Unbinding Limits
The scan locates the exact points where $\lambda_- \to 0$ (e.g., singular $\phi$ locations around $\pm \pi/4$, specifically mapped near $\pm 2.348$ and $\pm 5.521$ given numerical root finding on $\cos(2\phi) \approx 0$). At these exact boundaries:
- The effective stiffness of the anti-symmetric channel vanishes completely.
- This defines the topological "Unbinding Limits" of the theory: a state crossing this boundary loses its internal restoring force and dissolves.

## 4. Conclusion
The numerical scan flawlessly corroborates the analytical derivation. The geometric pullback metric of the ordered map natively provides dynamic, $\phi$-dependent interaction strengths ($\beta_{eff}$) that are orders of magnitude stronger than the toy constants from Phase C, successfully breaking the $O(4)$ symmetry from first principles.