# Phase I Data Assessment: Geometric Anisotropy Results

**Date:** 2026-03-31  
**Status:** Completed

## 1. Analysis of the Scan Data

### 1.1 Eigenvalue Divergence (Anisotropy Ratio)
The results from `slice_1d_phi.csv` and `bulk_summary.json` confirm that the angular pullback metric $G_{ang}$ is not isotropic.
- **Anisotropy Ratio:** The ratio between the strongest and weakest angular channels (effectively $\lambda_+ / \lambda_-$) reaches magnitudes of over **15,000** near the chart singularities.
- **Physical Meaning:** This implies that the internal "stiffness" of the spacetime-fold is extremely direction-dependent. The symmetric combination $(\theta + \rho)$ becomes very stiff in regions where the anti-symmetric combination $(\theta - \rho)$ becomes very soft (or vice versa).

### 1.2 Singular Controllers
The scan identifies the following critical features:
- **Phi as the Switch:** The anisotropy is strictly controlled by $\phi$. Variations in $\theta$ and $\rho$ (as seen in `slice_1d_theta.csv` and `slice_1d_rho.csv`) show constant eigenvalues when $\phi$ is fixed.
- **Singular Locations:** The "stiffness blow-up" occurs exactly at the $\cos(2\phi) = 0$ locations identified in Phase A.

## 2. Theoretical Validation

The data confirms the hypothesis in `derivations/derivation_90_geometric_origin_of_anisotropy.md`. We no longer need to "hand-tune" $\beta_a$ values. The metric $G_{ij}$ automatically penalizes different internal angular configurations with different energy costs based on the local value of $\phi$.

## 3. Comparison with Phase C
In Phase C, we used static proxies: $\beta_1=0.01, \beta_2=0.02, \beta_3=0.03$.
The new first-principles derivation yields dynamic weights that are **orders of magnitude more powerful** than the toy proxies. This suggests that the "real" physics model will have much sharper species differentiation and higher core stability.

---
**Conclusion:** Phase I is complete. We have successfully derived and validated the geometric origin of the symmetry-breaking constants.
