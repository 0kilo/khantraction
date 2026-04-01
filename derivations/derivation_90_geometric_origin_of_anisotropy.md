# Derivation 90: Geometric Origin of Anisotropy in the Ordered Quaternionic Map

**Date:** 2026-03-31  
**Phase:** I — First-Principles Derivation of Constants

## 1. The Pullback Metric
The ordered quaternionic state map is defined as:

$$
Q(\omega, \theta, \phi, \rho) = e^{\omega} e^{\theta i} e^{\phi j} e^{\rho k}
$$

The kinetic density in the Non-Linear Sigma Model (NLSM) is given by the pullback metric $G_{ij} = \partial_i Q_A \partial_j Q_A$ (where $A$ sums over quaternion components). From Derivation 75, we have:

$$
G = e^{2\omega} \begin{pmatrix} 
1 & 0 & 0 & 0 \\ 
0 & 1 & 0 & \sin(2\phi) \\ 
0 & 0 & 1 & 0 \\ 
0 & \sin(2\phi) & 0 & 1 
\end{pmatrix}
$$

where the coordinates are $\alpha^i = (\omega, \theta, \phi, \rho)$.

## 2. Eigenvalue Decomposition and Channel Stiffness
To find the intrinsic "stiffness" of the angular channels, we examine the eigenvalues of the angular sub-matrix $G_{ang}$ (the $3 \times 3$ block for $\theta, \phi, \rho$):

$$
G_{ang} = e^{2\omega} \begin{pmatrix} 
1 & 0 & \sin(2\phi) \\ 
0 & 1 & 0 \\ 
\sin(2\phi) & 0 & 1 
\end{pmatrix}
$$

The eigenvalues $\lambda$ are:
1.  $\lambda_\phi = 1$ (The $\phi$-channel is orthogonal and has unit stiffness).
2.  $\lambda_+ = 1 + \sin(2\phi)$ (The symmetric pairing $(\theta + \rho)$).
3.  $\lambda_- = 1 - \sin(2\phi)$ (The anti-symmetric pairing $(\theta - \rho)$).

## 3. Spontaneous Symmetry Breaking
In the previous "toy" phases (C–H), we manually introduced $\beta_a$ coefficients to break the $O(4)$ symmetry. However, we now see that the **geometry itself** breaks the symmetry:
- For any $\phi \neq 0, \pm \pi/2, \dots$, the stiffness of the $(\theta + \rho)$ and $(\theta - \rho)$ combinations is unequal.
- At the singular slices $\phi = \pm \pi/4$, one eigenvalue vanishes ($\lambda_- = 0$) while the other doubles ($\lambda_+ = 2$).

This implies that the "effective" $\beta_a$ values for the internal channels are determined by the local value of $\phi$:

$$
\beta_\theta(\phi) = 1, \quad \beta_\phi(\phi) = 1, \quad \beta_\rho(\phi) = 1, \quad \beta_{mix}(\phi) = \sin(2\phi)
$$

The interaction tensor $M_{ij}$ from Phase C is replaced by the metric $G_{ij}$ itself. The anisotropy is not a constant, but a **dynamical feature of the state**.

## 4. Conclusion
The anisotropic Maurer-Cartan coupling $\mathcal{L}_{MC} = \sum \beta_a (\Omega^a)^2$ is natively approximated by the pullback metric of the ordered map. The scale coordinate $\omega$ provides the global energy level, while $\phi$ acts as the "switch" that shifts stiffness between the $\theta$ and $\rho$ pairing states. This removes the need for phenomenological constants.
