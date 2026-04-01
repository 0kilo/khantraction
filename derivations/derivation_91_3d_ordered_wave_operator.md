# Derivation 91: 3D Wave Operator in Ordered Quaternionic Coordinates

**Date:** 2026-03-31  
**Phase:** J — Full 3D Dynamic Stability

## 1. Background
To evolve the Khantraction field $Q(t, x, y, z)$ in a 3D+1 spacetime, we must generalize the radial equations used in Phase B. The goal is to define the action of the Laplacian $\square$ on the target manifold coordinates $\alpha^i = (\omega, \theta, \phi, \rho)$.

## 2. Target Manifold Metric (Pullback)
From Phase I (Derivation 90), the pullback metric $G_{ij}$ in ordered coordinates is:

$$
G = e^{2\omega} \begin{pmatrix} 
1 & 0 & 0 & 0 \\ 
0 & 1 & 0 & \sin(2\phi) \\ 
0 & 0 & 1 & 0 \\ 
0 & \sin(2\phi) & 0 & 1 
\end{pmatrix}
$$

The kinetic energy density for the field is:

$$
\mathcal{K} = \frac{1}{2} G_{ij}(\alpha) \partial_\mu \alpha^i \partial^\mu \alpha^j
$$

## 3. General 3D Wave Equation
The field equations for the Non-Linear Sigma Model (NLSM) are given by:

$$
\square \alpha^i + \Gamma^i_{jk}(\alpha) \partial_\mu \alpha^j \partial^\mu \alpha^k + \frac{1}{A} G^{ij} \frac{\partial V}{\partial \alpha^j} = 0
$$

Where:
- $\square = \eta^{\mu\nu} \partial_\mu \partial_\nu = -\partial_t^2 + \nabla^2$ is the flat-space wave operator (assuming weak-gravity limit for stability testing).
- $\Gamma^i_{jk}$ are the Christoffel symbols of the target manifold metric $G$.
- $V$ is the potential including the norm coupling and non-minimal curvature terms.

## 4. Christoffel Symbols and Nonlinearity
Because $G_{ij}$ depends on $\phi$, the connection $\Gamma^i_{jk}$ introduces coupling between the angular channels. For example, the interaction between $\theta$ and $\rho$ is mediated by:

$$
\Gamma^\phi_{\theta\rho} = -\cos(2\phi)
$$

(Note: Exact coefficients to be computed in the solver). This term ensures that fluctuations in the $\theta$-channel can transfer energy into the $\rho$-channel and vice versa, but the "gate" is controlled by the $\phi$ state.

## 5. Potential Gradient
The potential $V(\alpha)$ includes the effective mass and the self-coupling terms. The force term $G^{ij} \partial_j V$ requires the inverse pullback metric $G^{ij}$:

$$
G^{-1} = e^{-2\omega} \begin{pmatrix} 
1 & 0 & 0 & 0 \\ 
0 & \sec^2(2\phi) & 0 & -\tan(2\phi)\sec(2\phi) \\ 
0 & 0 & 1 & 0 \\ 
0 & -\tan(2*phi)\sec(2\phi) & 0 & \sec^2(2\phi)
\end{pmatrix}
$$

Near the singular points $\phi = \pm \pi/4$, the inverse metric components blow up, representing the geometric "walls" that trap the species.

## 6. Implementation for Phase J
The 3D stability solver will use a semi-implicit integration scheme:
1. **Advection:** Evolve $\alpha^i$ using the standard wave operator.
2. **Geometric Correction:** Apply the $\Gamma^i_{jk}$ nonlinear term to ensure the path remains on the $S^3 \times \mathbb{R}^+$ manifold.
3. **Restoring Force:** Apply the potential gradient to maintain the species anchor.

---
**Conclusion:** The 3D wave operator in ordered coordinates is intrinsically nonlinear and self-coupling. This geometry is what provides the dynamical identity of the Khantraction species.
