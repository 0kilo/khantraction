# Phase A Closure Summary — Ordered Quaternion Parameter Foundation

**Date:** 2026-03-28  
**Phase:** A — Parameter foundation  
**Status:** Closed

## 1. Scope of Phase A

Phase A was the mapping-foundation phase of the classical Khantraction restart.
Its job was to determine what can defensibly be said about the ordered quaternion parameter map

$$
Q(\omega,\theta,\phi,\rho)=e^{\omega}e^{\theta i}e^{\phi j}e^{\rho k}
$$

before stronger structured-object or particle-facing interpretation.

The active working convention during this phase was:
- $\omega>0$
- $\theta,\phi,\rho\in[-2\pi,2\pi]$
- no redundancy quotienting

The key burden of proof was:
- separate scale from angular structure,
- determine whether the angular channels are genuinely distinct,
- identify any robust asymmetry among them,
- and avoid collapsing the three-angle story prematurely.

---

## 2. Final Phase A conclusions

### 2.1 $\omega$ is a pure scale coordinate

**Claim:** $\omega$ controls overall scale magnitude and does not change the internal angular overlap geometry except through uniform rescaling.
**Methodology & Rationale:** To definitively separate scale from rotational deformation, we analytically expanded the ordered quaternion product into its four components and computed the exact Jacobian matrix. We then performed a numerical stress-test spanning $\omega \in [0.1, 2.5]$ to verify that the norms of the angular tangent vectors scale uniformly. This approach isolates the scalar effect from internal angular coordinate shifts.
**Results & Proof:** Both the analytical expansion and the numerical scaling check demonstrate that the factor $e^\omega$ cleanly factors out of every component. Across all Phase A stress tests, the angular tangent vector norms perfectly satisfied $\|\partial_\theta Q\|=\|\partial_\phi Q\|=\|\partial_\rho Q\|=e^{\omega}$ to machine precision. Thus, $\omega$ acts exclusively as a multiplicative scale factor and has no bearing on internal overlap geometry.

This conclusion is supported by:
- `derivations/derivation_71_exponential_quaternion_parameter_mapping_clean.md`
- `analysis/phase_a/phase_a_parameter_geometry.py`
- `analysis/phase_a/phase_a_role_stability_stress_test.py`
- `solutions/phase_a/phase_a_parameter_geometry/`
- `solutions/phase_a/phase_a_role_stability_stress_test/omega_scaling_check.csv`
- `solutions/phase_a/phase_a_role_stability_stress_test/summary.md`
- `notes/phase_a/phase_a_parameter_geometry_assessment_2026-03-28.md`
- `notes/phase_a/phase_a_role_stability_stress_test_assessment_2026-03-28.md`

---

### 2.2 $\theta,\phi,\rho$ are genuinely distinct local angular directions

**Claim:** Away from singular sheets, $\theta,\phi,$ and $\rho$ form three independent, genuine local tangent directions on the ordered-state manifold, rather than being a redundant repackaging of a single parameter.
**Methodology & Rationale:** We evaluated the rank of the Jacobian matrix across a coarse grid of 4,913 points in the broad $[-2\pi, 2\pi]$ domain without quotienting redundancies. This mathematically verifies whether the three angular variables provide independent degrees of freedom (rank 4 overall) or collapse into lower-dimensional dependencies in regular space.
**Results & Proof:** The scan verified that the Jacobian is generically full rank (rank 4). At named benchmark points (e.g., origin, quarter-turns), the angular tangent vectors were mutually orthogonal with equal norm. This proves that where the chart is regular, $\theta,\phi,$ and $\rho$ act as locally distinct coordinate channels, warranting symmetric treatment.

This conclusion is supported by:
- `derivations/derivation_71_exponential_quaternion_parameter_mapping_clean.md`
- `analysis/phase_a/phase_a_parameter_geometry.py`
- `solutions/phase_a/phase_a_parameter_geometry/coarse_scan.csv`
- `solutions/phase_a/phase_a_parameter_geometry/named_points.json`
- `solutions/phase_a/phase_a_parameter_geometry/special_points.json`
- `solutions/phase_a/phase_a_parameter_geometry/summary.md`
- `notes/phase_a/phase_a_parameter_geometry_assessment_2026-03-28.md`

---

### 2.3 The chart singularity architecture is controlled by $\phi$

**Claim:** The local indistinguishability (singularity) of the ordered coordinate chart is governed entirely by the parameter $\phi$.
**Methodology & Rationale:** We computed the exact analytical determinant of the Jacobian $\det J = e^{4\omega}\cos(2\phi)$ and systematically verified it against numerical outputs across a dense domain scan of 55,539 points in the unquotiented $[-2\pi, 2\pi]$ space. Finding the roots of the determinant pinpoints the precise boundaries where coordinate independence fails.
**Results & Proof:** Numerical sampling confirmed the analytical determinant law up to numerical precision (max absolute error $\sim 3.98 \times 10^{-13}$). The condition $\cos(2\phi)=0$ dictates that singular slices occur exactly at $\phi=\pi/4 + n\pi/2$. Inside the active domain, this produces repeated singular sheets (e.g., $\pm\pi/4, \pm 3\pi/4, \pm 5\pi/4, \pm 7\pi/4$). This establishes that $\phi$ is uniquely responsible for the topological rank-collapse of the chart mapping.

This conclusion is supported by:
- `derivations/derivation_72_phase_a_jacobian_singularity_structure.md`
- `analysis/phase_a/phase_a_singularity_structure.py`
- `solutions/phase_a/phase_a_singularity_structure/domain_singular_points.json`
- `solutions/phase_a/phase_a_singularity_structure/phi_slice_table.csv`
- `solutions/phase_a/phase_a_singularity_structure/summary.md`
- `notes/phase_a/phase_a_parameter_geometry_assessment_2026-03-28.md`

---

### 2.4 The angular distinction is not one of norm but of relational role

**Claim:** $\phi$ acts as an orthogonal separator and mixing controller that modulates the relation between $\theta$ and $\rho$, rather than functioning merely as a symmetric third angle.
**Methodology & Rationale:** Because coordinate-chart determinant language can be fragile, we examined the angular tangent bundle's geometry more robustly by computing the Gram matrix of Jacobian columns and analyzing pairwise cosine overlaps. A broad stress test covering 26,325 points compared the alignment between the three angles across variations.
**Results & Proof:** The results demonstrated a stark asymmetry in role rather than magnitude. The pairwise overlaps $\cos(\partial_\theta Q,\partial_\phi Q)$ and $\cos(\partial_\phi Q,\partial_\rho Q)$ remained nearly identically zero (max $\sim 10^{-31}$), indicating that $\phi$ stays strictly orthogonal. Concurrently, the overlap $\cos(\partial_\theta Q,\partial_\rho Q)$ freely swept the entire $[-1, 1]$ interval. This definitively proves $\phi$ acts differently—controlling the geometric coupling of the $(\theta, \rho)$ pair.

This conclusion is supported by:
- `analysis/phase_a/phase_a_channel_role_hypothesis.py`
- `analysis/phase_a/phase_a_invariant_channel_comparison.py`
- `analysis/phase_a/phase_a_role_stability_stress_test.py`
- `solutions/phase_a/phase_a_invariant_channel_comparison/phi_scan.csv`
- `solutions/phase_a/phase_a_invariant_channel_comparison/theta_scan_phi0.csv`
- `solutions/phase_a/phase_a_invariant_channel_comparison/rho_scan_phi0.csv`
- `solutions/phase_a/phase_a_invariant_channel_comparison/named_points.json`
- `solutions/phase_a/phase_a_invariant_channel_comparison/summary.md`
- `solutions/phase_a/phase_a_channel_role_hypothesis/broad_phi_control_scan.csv`
- `solutions/phase_a/phase_a_channel_role_hypothesis/phi_profile_fixed_pair.csv`
- `solutions/phase_a/phase_a_channel_role_hypothesis/theta_rho_independence_scan.csv`
- `solutions/phase_a/phase_a_channel_role_hypothesis/summary.md`
- `solutions/phase_a/phase_a_role_stability_stress_test/stress_scan.csv`
- `solutions/phase_a/phase_a_role_stability_stress_test/stress_summary.json`
- `solutions/phase_a/phase_a_role_stability_stress_test/summary.md`
- `notes/phase_a/phase_a_invariant_channel_comparison_assessment_2026-03-28.md`
- `notes/phase_a/phase_a_channel_role_hypothesis_assessment_2026-03-28.md`
- `notes/phase_a/phase_a_role_stability_stress_test_assessment_2026-03-28.md`

---

### 2.5 $\theta$ and $\rho$ form the active paired subsystem

**Claim:** The ordered map houses a paired subsystem consisting of $\theta$ and $\rho$, where $\phi$ operates as the explicit determinant of their mutual local distinctness.
**Methodology & Rationale:** We conducted direct 1D and 2D numerical slice studies—holding one or two variables fixed while sweeping the others. This isolates structural responses visually and exposes exactly which variable sweeps induce chart collapse versus regular variation.
**Results & Proof:** The slice studies clearly showed that the $(\theta, \rho)$-plane remains entirely regular when fixing $\phi = 0$ (0 singular points among 1,089), whereas fixing $\phi = \pi/4$ causes the entire $(\theta, \rho)$-plane to collapse into singularity (1,089/1,089 singular points). Conversely, holding $\phi$ at a regular value and sweeping $\theta$ or $\rho$ never forces a zero determinant. This proves $\phi$ independently determines whether the $(\theta, \rho)$ pair remains locally distinct or aligns indistinguishably.

This conclusion is supported by:
- `analysis/phase_a/phase_a_slice_studies.py`
- `solutions/phase_a/phase_a_slice_studies/vary_theta_phi0_rho0.csv`
- `solutions/phase_a/phase_a_slice_studies/vary_phi_theta0_rho0.csv`
- `solutions/phase_a/phase_a_slice_studies/vary_rho_theta0_phi0.csv`
- `solutions/phase_a/phase_a_slice_studies/vary_theta_phi_pi4_rho0.csv`
- `solutions/phase_a/phase_a_slice_studies/vary_rho_theta0_phi_pi4.csv`
- `solutions/phase_a/phase_a_slice_studies/vary_phi_theta1.1_rho-0.9.csv`
- `solutions/phase_a/phase_a_slice_studies/theta_phi_rho0.csv`
- `solutions/phase_a/phase_a_slice_studies/theta_rho_phi0.csv`
- `solutions/phase_a/phase_a_slice_studies/phi_rho_theta0.csv`
- `solutions/phase_a/phase_a_slice_studies/theta_rho_phi_pi4.csv`
- `solutions/phase_a/phase_a_slice_studies/one_d_summary.json`
- `solutions/phase_a/phase_a_slice_studies/two_d_summary.json`
- `solutions/phase_a/phase_a_slice_studies/summary.md`
- `notes/phase_a/phase_a_slice_study_assessment_2026-03-28.md`

---

## 3. Final Phase A role picture

At the mapping-geometric level, the strongest current role assignment is:

- **$\omega$** = scale coordinate
- **$\phi$** = orthogonal separator / mixing-control coordinate
- **$\theta$, $\rho$** = paired internal structural directions

This is the cleanest distilled result of Phase A. It directly fulfills the key Phase A goal in `notes/classical_exploration_plan.md` to establish what the angular parameters represent symmetrically and distinctively.

It is explicitly synthesized in:
- `notes/phase_a/phase_a_synthesis_2026-03-28.md`

---

## 4. What Phase A has *not* claimed

Phase A has **not** established:
- a full classical structured-object interpretation yet,
- a field-equation or operator-side dynamical dominance claim,
- a direct particle-property interpretation,
- or a completed physical trait map of the richer Khantraction objects.

What Phase A has established is narrower but important:

> The ordered quaternion parameter foundation is now coherent, nontrivial, and structured enough to support later phases without collapsing the three-angle story prematurely.

---

## 5. Why the phase is considered closed

Phase A is considered closed because its core burden of proof now appears met:

1. Scale has been cleanly separated from angular structure.
2. The three angular channels have been shown to be locally real and distinct.
3. A robust angular asymmetry has been identified and repeatedly stress-tested.
4. That asymmetry has been interpreted in a disciplined mapping-level way without overclaiming physics.
5. The results are consistent across coarse scans, singular-structure analysis, slice studies, invariant-style comparisons, role-hypothesis tests, and broader stress tests.

At this point, more Phase A work would likely repeat the same foundational conclusion rather than materially change it.

---

## 6. Recommended handoff to later phases

The recommended handoff from Phase A is:

- take $\omega$ as the established scale coordinate,
- take $\phi$ as the established separator / mixing-control channel,
- take $\theta,\rho$ as the established paired internal directions,
- and test in later phases whether these mapping-level roles correlate with:
  - structured-object traits,
  - concentration / compactness changes,
  - external profile behavior,
  - hosting properties,
  - and handedness/chirality architecture.

That is the right way to let Phase A inform Phase B and Phase C without overextending it.

---

## 7. Bottom line

**Bottom line:** Phase A successfully rebuilt the ordered quaternion parameter foundation for Khantraction. The phase established one pure scale coordinate $\omega$, a repeated singular-sheet architecture controlled by $\phi$, equal-strength angular channels in norm, and a stable relational role picture in which $\phi$ acts as an orthogonal separator / mixing controller for the paired directions $\theta$ and $\rho$. This is now a sufficiently coherent and stress-tested foundation to treat Phase A as complete and move on to later classical structured-object work.