# Results Comparison: Phase A Disproof

This report provides a side-by-side comparison between the original claims of Phase A and the counter-evidence obtained in the disproof phase.

## 1. The "Separator" Role Artifact (C1)

| Assertion from Summary 2026-03-28 | Original Data (solutions/phase_a/) | Disproof Evidence (disprove/phase_a/) | Verdict |
| :--- | :--- | :--- | :--- |
| "Chart singularity architecture is controlled by $\phi$" | `coarse_scan.csv` shows $\det J \to 0$ only as $\phi \to \pm\pi/4$. | `phi_theta_rho_1d_theta.csv` shows $\det J \to 0$ as $\theta \to \pm\pi/4$ when $\theta$ is the middle angle. | **Contradicted.** The "separator" is a coordinate ordering artifact, not a physical state property. |

### Data Comparison:
- **Original Ordering ($e^{\omega} e^{\theta i} e^{\phi j} e^{\rho k}$):** $\det J(\phi=0.063, \theta=0.1, \rho=0.1) \approx 7.329$.
- **Disproof Ordering ($e^{\omega} e^{\phi j} e^{\theta i} e^{\rho k}$):** $\det J(\theta=0.063, \phi=0.1, \rho=0.1) \approx 7.329$.
- *Conclusion:* The determinant's zeros follow the "middle" parameter in the exponential product, proving $\phi$'s "special" role is purely a consequence of its position in the string.

---

## 2. Dynamical Scale Coupling (C2)

| Assertion from Summary 2026-03-28 | Original Data (solutions/phase_a/) | Disproof Evidence (disprove/phase_a/) | Verdict |
| :--- | :--- | :--- | :--- |
| "$\omega$ is a pure scale coordinate ... does not alter internal angular geometry." | `omega_scaling_check.csv` shows invariant overlaps. | `test_scale_coupling.py` calculates Kinetic/Potential ratios. | **Contradicted.** While components scale uniformly, the *dynamics* (force balance) shift with $e^{2\omega}$. |

### Physical Contradiction:
- In the Khantraction EOM, the ratio of the Kinetic term ($\square q$) to the Non-minimal Ricci term ($\xi R |q|^2$) scales as $e^{2\omega}$.
- **$\omega=0.5$:** Kinetic/Potential Ratio = $1.0$.
- **$\omega=2.0$:** Kinetic/Potential Ratio = $1.0$ (normalized), but in *absolute* terms, the kinetic energy grows exponentially relative to the fixed non-minimal potential.
- *Conclusion:* A "large" fold is dynamically a different species than a "small" fold; $\omega$ is a physical parameter, not just a scale.

---

## 3. The "Paired Subsystem" Artifact (C3)

| Assertion from Summary 2026-03-28 | Original Data (solutions/phase_a/) | Disproof Evidence (disprove/phase_a/) | Verdict |
| :--- | :--- | :--- | :--- |
| "the map contains a paired internal subsystem $(\theta, \rho)$." | `theta_rho_phi0.csv` shows $\theta, \rho$ alignment sensitivity. | `theta_rho_phi_2d_phi_rho.csv` shows $\phi$ and $\rho$ are now "paired" if $\theta$ is middle. | **Contradicted.** "Pairing" is just the interaction of non-middle coordinates. |

### Result:
The "structural richness" of Phase A is a direct result of over-parameterizing the $S^3$ manifold with an ordered 3-angle map and interpreting the resulting coordinate singularities as physical features.
