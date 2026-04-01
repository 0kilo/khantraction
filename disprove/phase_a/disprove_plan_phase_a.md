# Rigorous Disprove Plan: Phase A — The "Artifact" Hypothesis

**Objective:** Explicitly demonstrate that the Phase A "fundamental" asymmetries are coordinate artifacts by providing direct side-by-side comparisons between original data and disproof data.

---

## 1. Targeted Claims and Contradiction Mapping

| Claim from Summary 2026-03-28 | Original Evidence (solutions/phase_a/) | Disproof Strategy | Expected Contradiction |
| :--- | :--- | :--- | :--- |
| **C1: $\phi$ is the unique separator.** "Chart singularity architecture is controlled by $\phi$" | `coarse_scan.csv` shows $\det J$ varying only with $\phi$ (e.g., $\det J \approx 0.707$ for $\phi = \pi/8$, regardless of $\theta, \rho$). | Change ordering to $e^{\omega} e^{\phi j} e^{\theta i} e^{\rho k}$. | Show $\det J$ now varies *only* with $\theta$ in the new data. |
| **C2: $\omega$ is a pure scale coordinate.** "$\omega$ does not alter internal angular overlap geometry." | `role_stability_stress_test/omega_scaling_check.csv` shows invariant overlaps across $\omega$. | Analyze EOM (Equation of Motion) ratios: Kinetic / Non-minimal Potential. | Show that the *ratio* of terms in the physical equations scales as $e^{2\omega}$, altering the balance of forces. |
| **C3: $(\theta, \rho)$ is a paired subsystem.** "the map contains a paired internal subsystem $(\theta, \rho)$." | `slice_studies/theta_rho_phi0.csv` shows alignment sensitivity between $\theta$ and $\rho$. | Show that this "pairing" is just the interaction of the two "non-middle" angles in the sequence. | In ordering $e^{\omega} e^{\rho k} e^{\theta i} e^{\phi j}$, show that $\rho$ and $\theta$ are now the "paired" ones. |

---

## 2. Execution Protocol

### 2.1 Direct Data Contradiction (Ordering)
- **Script:** `disprove/phase_a/test_ordering_invariance.py`
- **Action:** 
    1. Extract a specific point from `solutions/phase_a/phase_a_parameter_geometry/coarse_scan.csv` (e.g., row 18: $\theta=-\pi, \phi=-2.74, \rho=-\pi, \det J \approx 0.707$).
    2. Calculate $\det J$ for the *same* parameter values but with a *different* ordering in the disproof script.
    3. Tabulate the difference to show that $\det J$ is not a property of the state $(\theta, \phi, \rho)$ but of the map $Q$.

### 2.2 Dynamical Coupling (Scale)
- **Script:** `disprove/phase_a/test_scale_coupling.py`
- **Action:**
    1. Reference `solutions/phase_a/phase_a_role_stability_stress_test/omega_scaling_check.csv` which claims invariance.
    2. Compute the Ricci scalar $R$ coupling term $2\xi R |q|^2$ vs. kinetic term $G^{ij} \partial_i q \partial_j q$.
    3. Show that while the *angles* don't change, the *physical importance* of the angular sector relative to the scale sector changes by orders of magnitude as $\omega$ varies.

---

## 3. Implementation and Reporting
- Results will be saved in `disprove/phase_a/results_comparison.md`.
- Contradictions will be highlighted using "Original Value" vs "Disproof Value" tables.
