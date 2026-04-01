# Phase I Assessment: First-Principles Derivation of Constants

**Date:** 2026-03-31  
**Status:** Planning / In-Progress

## 1. Research Plan & Methodology

### 1.1 Objective
The primary goal of Phase I is to eliminate the phenomenological $\beta_a$ constants introduced in Phase C and replace them with a geometric derivation anchored in the **Ordered Quaternionic State Map**:

$$
Q(\omega, \theta, \phi, \rho) = e^{\omega} e^{\theta i} e^{\phi j} e^{\rho k}
$$

### 1.2 Theoretical Hypothesis
We hypothesize that the anisotropic symmetry breaking required to distinguish species is already present in the **pullback metric** $G_{ij}$ and the **Jacobian determinant**. Specifically, the term $2\sin(2\phi)\theta'\rho'$ in the kinetic density $|Q'|^2$ implies that the energy cost of angular fluctuations depends on the state variable $\phi$. 

We propose that the "real" $\beta_a$ values are not constants but are proportional to the local curvature of the target manifold or the inverse of the Jacobian determinant:

$$
\beta_{eff} \propto \frac{1}{|\det J|} = \frac{e^{-4\omega}}{|\cos(2\phi)|}
$$

This would mean that near chart singularities, the "glue" becomes infinitely stiff, forcing the fold into specific stable angular basins.

### 1.3 Analysis Protocol
To ensure a complete investigation, we will execute the following scans across the mandatory domains:
- **Domains:** $\omega > 0$; $\theta, \phi, \rho \in [-2\pi, 2\pi]$.
- **1D Slices:** All 3 combinations (varying $\theta, \phi, \rho$ separately).
- **2D Slices:** All 3 combinations (varying pairs).
- **Bulk:** Full 3D angular volume.

## 2. Implementation Steps (Workflow Alignment)

1. **Derivation:** Formalize the geometric weight function $\beta_a(\phi)$ in `derivations/derivation_90_geometric_origin_of_anisotropy.md`.
2. **Analysis Code:** Develop `analysis/phase_i/phase_i_geometric_anisotropy_scan.py` to compute the effective "stiffness" of the angular channels.
3. **Execution:** Run the scan using `scripts/run_phase_i_anisotropy_scan.sh`.
4. **Validation:** Compare the derived weights against the Phase C proxies ($\beta_1=0.01, \beta_2=0.02, \beta_3=0.03$) to see if the "real" physics reproduces the "toy" success.

---
**Key Question:** Can the anisotropic $O(4)$ symmetry breaking arise spontaneously from the geometry of the ordered quaternionic state map rather than being inserted by hand?
