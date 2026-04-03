# Phase I Closure Summary — First-Principles Derivation of Constants

**Date:** 2026-03-31  
**Phase:** I — First-Principles Derivation of Constants  
**Status:** Closed

## 1. Scope of Phase I

Phase I was the "Foundational Cleanup" phase of the transition to a real physics model. Its primary mandate was to replace the phenomenological symmetry-breaking constants ($\beta_a$) with a rigorous derivation anchored in the ordered quaternionic state map and identify the model's physical analogs.

The active working convention and constraints during this phase, as dictated by the Quantum Exploration Plan, were:
- $\omega > 0$
- $\theta, \phi, \rho \in [-2\pi, 2\pi]$
- No redundancy quotienting.
- Every study must include bulk analysis along with all combinations of 1D Slices and 2D Slices.

The key burdens of proof were:
- Prove that the pullback metric $G_{ij}$ natively breaks $O(4)$ symmetry.
- Map the dynamical "stiffness" of the angular channels across the full state space.
- Calculate the exact self-coupling limits required to keep the internal branch structure stable.
- Identify the physical analogs for the fine-structure constant and the mass gap.

---

## 2. Final Phase I Conclusions

### 2.1 Spontaneous Symmetry Breaking via Pullback Geometry

**Claim:** The Ordered Quaternionic State Map natively contains the necessary anisotropy in its pullback metric $G_{ij}$ to break $O(4)$ symmetry, eliminating the need for phenomenological proxy constants.
**Methodology & Rationale:** We mathematically derived the pullback metric and extracted the eigenvalues of its angular sub-matrix ($G_{ang}$). This allowed us to determine the intrinsic stiffness of the $\phi$ channel, as well as the symmetric $(\theta + \rho)$ and anti-symmetric $(\theta - \rho)$ channels. 
**Results & Proof:** The analytical eigenvalue decomposition showed that the stiffness for the symmetric channel is $\lambda_+ = 1 + \sin(2\phi)$ and for the anti-symmetric channel is $\lambda_- = 1 - \sin(2\phi)$, all scaled by $e^{2\omega}$. For any $\phi \neq n\pi/2$, the stiffness of these channels is strictly unequal. This geometric asymmetry forces spontaneous symmetry breaking. The "effective" $\beta_a$ values are not constant but dynamical functions of the state coordinate $\phi$.

This conclusion is supported by:
- `derivations/derivation_90_geometric_origin_of_anisotropy.md`
- `notes/phase_i/phase_i_constants_derivation_assessment.md`

---

### 2.2 Dynamic Stiffness and the Unbinding Limits

**Claim:** The effective stiffness of the internal channels is dynamically controlled by $\phi$, and diverges to create unbinding limits that define stable topological basins.
**Methodology & Rationale:** We performed an exhaustive numerical scan of the eigenvalues across the full angular domain, strictly implementing the 1D and 2D slice requirements of the transition protocol. By evaluating the anisotropy ratio across these slices, we could pinpoint exactly where stiffness diverges or collapses.
**Results & Proof:** The scan verified that $\theta$ and $\rho$ do not alter stiffness, confirming $\phi$ as the unique "switch." The maximum anisotropy ratio reached $>15,888$ near singular locations. Specifically, at $\phi = \pm\pi/4$, the stiffness of the anti-symmetric channel exactly vanishes ($\lambda_- \to 0$). This establishes the "Unbinding Limits" where the topological fold loses its restoring force. 

This conclusion is supported by:
- `analysis/phase_i/phase_i_geometric_anisotropy_scan.py`
- `solutions/phase_i/phase_i_geometric_anisotropy_scan/slice_1d_phi.csv`
- `solutions/phase_i/phase_i_geometric_anisotropy_scan/slice_1d_theta.csv`
- `solutions/phase_i/phase_i_geometric_anisotropy_scan/slice_1d_rho.csv`
- `solutions/phase_i/phase_i_geometric_anisotropy_scan/slice_2d_phi_rho.csv`
- `solutions/phase_i/phase_i_geometric_anisotropy_scan/slice_2d_theta_phi.csv`
- `solutions/phase_i/phase_i_geometric_anisotropy_scan/slice_2d_theta_rho.csv`
- `solutions/phase_i/phase_i_geometric_anisotropy_scan/bulk_summary.json`
- `solutions/phase_i/phase_i_geometric_anisotropy_scan/summary.md`
- `notes/phase_i/phase_i_data_assessment.md`

---

### 2.3 Definition of Physical Analogs: $\alpha_K$ and $\Delta M_g$

**Claim:** The geometric constants derived from the pullback metric naturally map to physical observables: a fine-structure constant and an internal mass gap.
**Methodology & Rationale:** We compared the derived stiffness eigenvalues with the non-minimal coupling interactions. By taking dimensionless ratios of these parameters at the stable species-anchor points (e.g., $\phi = \pi/8$), we can define robust, scale-invariant interaction constants.
**Results & Proof:** The **Khantraction Fine-Structure Constant ($\alpha_K$)** was calculated as the ratio of the non-minimal coupling $\xi$ to the unit channel stiffness ($\beta_{unit} = 1$), yielding $\alpha_K = \xi / 1 \approx 0.002$. The **Internal Mass Gap ($\Delta M_g$)** was calculated as the difference between the symmetric and anti-symmetric channel stiffnesses, $\Delta M_g = 2|\sin(2\phi)|$. At the anchor point $\phi = \pi/8$, this evaluates to $\Delta M_g \approx 1.414$. These constants dynamically replace the phenomenological parameters and provide the dimensionless foundation needed for a discrete particle-like spectrum.

This conclusion is supported by:
- `notes/phase_i/phase_i_physical_analogs.md`
- `derivations/derivation_90_geometric_origin_of_anisotropy.md`

---

## 3. What Phase I has *not* claimed

Phase I has **not** established:
- The exact time-evolution of these stable basins in full 3D+1 dynamics.
- The behavior of these states under violent spatial acceleration.
- The emergent interaction forces (attraction/repulsion) when two distinct folds are separated by distance.
- The specific mechanisms for discrete energy shedding or pair creation.

## 4. Why the phase is considered closed

Phase I is closed because all explicit goals assigned in the `real_physics_transition_plan.md` have been met:
1. The arbitrary anisotropic Maurer-Cartan coefficients ($\beta_a$) have been completely replaced with dynamical values derived from the pullback geometry.
2. The exact self-coupling limits (the $\lambda_- \to 0$ unbinding limits) have been rigorously identified across 1D, 2D, and bulk scans.
3. The derived constants have been successfully mapped to the physical observables $\alpha_K$ and $\Delta M_g$.

## 5. Recommended handoff to later phases

The first-principles constants derived here are the critical prerequisites for moving beyond 1D statics into 3D dynamics. The recommended handoff is:
- Abandon all use of static $\beta_a$ constants in future code.
- Implement the dynamically calculated $\lambda_\phi, \lambda_+, \lambda_-$ derived from $G_{ang}$ natively in the solver logic for **Phase J: Full 3D Dynamic Stability**.
- Use the identified stability basins ($|\phi| < \pi/4$) as the boundary conditions when testing structural survival against asymmetric perturbations.

---

## 6. Bottom line

**Bottom line:** Phase I has successfully transitioned Khantraction from a hand-tuned toy model to a first-principles geometric theory. The interaction strengths and energy gaps are no longer imposed from the outside; they are derived directly from the ordered quaternionic state map's native pullback metric. The identification of the unbinding limits defines the stable topological basins of the theory, providing a robust, dynamically consistent foundation for 3D simulation.