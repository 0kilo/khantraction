# Derivation 85: Discrete Spectrum Conditions and Boundary Mapping

**Date:** 2026-03-30  
**Phase:** H — Return to Stronger Quantum-Facing Work  
**Status:** Drafted  

---

## 1. Purpose
This derivation establishes the specific boundary conditions and eigenvalue constraints required to produce a discrete energy spectrum within the Khantraction structured fold. Building on the wave equation ansatz from **Derivation 84**, we define the criteria for "bound states" within the hosting basins identified in Phase F.

---

## 2. The Radial Potential Well
The effective potential $V_{eff}(r)$ is derived from the interaction between the Reissner–Nordström-like metric profile and the hosting sensitivity $V_{host}$. For an excitation to be "trapped" as a discrete mode, the following condition must be met:

$$E^2 < \lim_{r \to \infty} V_{eff}(r)$$

### 2.1 The Hosting Barrier
The data from Phase F indicates a maximum hosting sensitivity of approximately **0.999** at the core. This value defines the depth of the potential well. A discrete spectrum exists if the wave function $\Psi$ satisfies:
1.  **Regularity at the Origin**: $\Psi(r \to 0)$ remains finite, governed by the internal $\mathfrak{su}(2)$ scale $\omega$.
2.  **Exponential Decay at Infinity**: $\Psi(r \to \infty) \sim e^{-\kappa r}$, where $\kappa = \sqrt{m^2_{eff} - E^2}$.

---

## 3. Angular Boundary Conditions
Unlike standard spherical systems, the Khantraction fold possesses internal angular boundaries defined by the singular-sheet architecture ($\phi = \pm\pi/4, \pm3\pi/4$) discovered in Phase A.

### 3.1 Sheet-Induced Quantization
The wave function must satisfy periodic boundary conditions across the internal angular coordinates $\theta$ and $\rho$, but it encounters "geometric phase shifts" when crossing the $\phi$ singular sheets:
$$\Psi(\phi + \pi/2) = e^{i\alpha} \Psi(\phi)$$
where $\alpha$ is a phase factor determined by the **Chirality Density** ($\chi$) from Phase G.

---

## 4. Eigenvalue Equation for Mode Ladders
The discrete energy levels $E_n$ are determined by the zeros of the Jost function or the matching of logarithmic derivatives at the hosting basin boundary $r_h$. The quantization condition is approximated as:

$$\int_{0}^{r_h} \sqrt{E_n^2 - V_{eff}(r)} \, dr = \left(n + \frac{1}{2}\right)\pi$$

Where:
* **$n$**: The principal quantum number of the excitation.
* **$r_h$**: The radius of the hosting basin where $V_{eff}(r)$ exceeds $E_n^2$.

---

## 5. Symmetry-Breaking and Level Splitting
The chirality results from Phase G imply that the discrete spectrum will exhibit **Enantiomeric Splitting**:
* **Mirror-Pair States**: While classical traits are identical (0.0 trait divergence), the coupling term $\lambda \chi$ from **Derivation 84** will lift the degeneracy between L-handed and R-handed configurations.
* **Spin-like Signature**: This splitting is the first evidence of a discrete quantum number arising directly from the classical topological handedness.

---

## 6. Analytical Objectives
Following this derivation, the project will:
1.  **Solve for $E_n$**: Use `analysis/phase_h/phase_h_mode_ladder_scan.py` to find the first three primary modes ($n=0, 1, 2$).
2.  **Map Species to Spectra**: Determine if $\theta$-dominant species support a different number of bound states than $\phi$-dominant species.
3.  **Confirm Persistence**: Verify that these discrete levels remain stable even when the "loaded" content is rotated at sub-critical velocities.

---
**Bottom Line:** Derivation 85 provides the formal "box" constraints for the Khantraction resonator. By mapping the classical hosting sensitivity of Phase F to quantum boundary conditions, we can now calculate the discrete energy signatures of the spacetime-fold.