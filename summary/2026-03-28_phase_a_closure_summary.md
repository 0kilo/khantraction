# Phase A Closure Summary — Ordered Quaternion Parameter Foundation

**Date:** 2026-03-28  
**Phase:** A — Parameter foundation  
**Status:** Closed after audit refresh

## 0. Project-level disposition

Phase A remains closed and foundational in the direct-data closure plan. It is not a blocking gap for the final classical particle-level verdict. The project-level synthesis is recorded in `summary/2026-04-02_gap_closure_summary.md`, `notes/2026-04-02_direct_data_closure_plan.md`, and `summary/2026-04-02_khantraction_model_conclusion.md`.

## 1. Scope and motivation

`khantraction_paper.md` frames Khantraction as an exploratory toy model for compact, structured spacetime-fold objects rather than a finished particle theory. In that setting, the ordered quaternion map

$$
Q(\omega,\theta,\phi,\rho)=e^{\omega}e^{\theta i}e^{\phi j}e^{\rho k}
$$

cannot be treated as mere notation. It has to be understood on its own terms before later phases attach structured-object, chirality, hosting, or proto-spectrum language to particular channels.

That is why Phase A exists. Its burden of proof was intentionally narrow:

- separate scale from angular structure,
- determine whether the angular channels are genuinely distinct,
- compare them symmetrically on the active unquotiented domain,
- identify any robust asymmetry without overclaiming physics,
- and establish the clean map plus Jacobian as the active foundation for later classical work.

The active Phase A convention was:

- $\omega>0$
- $\theta,\phi,\rho\in[-2\pi,2\pi]$
- no redundancy quotienting

That framing is consistent with:

- `khantraction_paper.md`
- `notes/classical_exploration_plan.md`

---

## 2. Audit against `notes/classical_exploration_plan.md`

The plan defines four explicit Phase A goals and three expected output classes. After tracing the derivations, analyses, notes, and raw solution artifacts, the audited status is:

### 2.1 Goal 1 — Treat $\omega$ as scale

**Status:** Met.

**How it was tested:** Derivation 71 expands the ordered product exactly, showing that every component carries the same factor $e^\omega$. The dedicated stress test then checks the angular tangent norms over $\omega\in[0.1,2.5]`.

**Why this proves the goal:** If every component and every angular tangent norm scales by the same $e^\omega$ factor, then $\omega$ changes overall magnitude without changing the internal overlap geometry.

### 2.2 Goal 2 — Treat $\theta,\phi,\rho$ as distinct internal angles

**Status:** Met at the mapping level.

**How it was tested:** The regenerated active-domain geometry scan checks Jacobian rank and angular tangent behavior on 35,937 sampled grid points at fixed $\omega=0$, with named-point checks at the origin, quarter turns, and the rich-sector guess.

**Why this proves the goal:** Away from singular sheets, the chart is locally full rank and the three angular directions are independent tangent directions with equal norm. So the angles are not a fake repackaging of one local coordinate.

### 2.3 Goal 3 — Compare the angular channels symmetrically

**Status:** Met.

**How it was tested:** Phase A does not rely on one diagnostic. It uses:

- local rank and tangent geometry,
- determinant and singular-sheet structure,
- Gram-matrix / singular-value comparisons,
- 1D slices,
- 2D slices,
- and a wider stress test over the active domain.

**Why this proves the goal:** The comparison is symmetric at the level of method. Only after the symmetric comparison is complete does a consistent relational asymmetry emerge.

### 2.4 Goal 4 — Use the clean map and Jacobian as the active foundation

**Status:** Met.

**How it was tested:** Every Phase A analysis script works directly from the ordered map in Derivation 71 and its exact Jacobian entries; the singularity analysis extends that foundation on the full active domain.

**Why this proves the goal:** Later role language is not inferred loosely from the paper narrative. It is anchored to the explicit ordered map and its Jacobian geometry.

### 2.5 Expected outputs

**Status:** Produced and now fully traceable.

The expected outputs from the plan were:

- clean mapping derivations,
- Jacobian comparison work,
- angle-role comparison notes.

Those now exist as:

- `derivations/derivation_71_exponential_quaternion_parameter_mapping_clean.md`
- `derivations/derivation_72_phase_a_jacobian_singularity_structure.md`
- `analysis/phase_a/phase_a_parameter_geometry.py`
- `analysis/phase_a/phase_a_singularity_structure.py`
- `analysis/phase_a/phase_a_channel_role_hypothesis.py`
- `analysis/phase_a/phase_a_invariant_channel_comparison.py`
- `analysis/phase_a/phase_a_slice_studies.py`
- `analysis/phase_a/phase_a_role_stability_stress_test.py`
- the corresponding `solutions/phase_a/...` solution directories
- the corresponding `notes/phase_a/...` assessment notes

Each Phase A solution directory now includes an interpretive solution summary, not only raw CSV/JSON output.

---

## 3. Final Phase A conclusions

### 3.1 $\omega$ is a pure scale coordinate

**Claim:** $\omega$ controls overall scale magnitude and does not change the internal angular overlap geometry except through uniform rescaling.

**Method and rationale:** Derivation 71 analytically expands the ordered quaternion product and shows that every component is multiplied by $e^\omega$. The role-stability stress test then samples $\omega\in[0.1,2.5]$ and checks whether the angular tangent norms continue to scale uniformly.

**Results:** The regenerated `solutions/phase_a/phase_a_role_stability_stress_test/omega_scaling_check.csv` file confirms

$$
\|\partial_\theta Q\|=\|\partial_\phi Q\|=\|\partial_\rho Q\|=e^\omega
$$

up to floating-point noise across the sampled range, with the largest cross-channel norm mismatch only

$$
1.7763568394002505\times10^{-15}.
$$

**Why this proves the claim:** If every component and every angular tangent norm is multiplied by the same $e^\omega$ factor, then $\omega$ changes overall magnitude only. It does not change the relative angular geometry.

**Supporting documents:**

- `derivations/derivation_71_exponential_quaternion_parameter_mapping_clean.md`
- `analysis/phase_a/phase_a_parameter_geometry.py`
- `analysis/phase_a/phase_a_role_stability_stress_test.py`
- `solutions/phase_a/phase_a_parameter_geometry/summary.md`
- `solutions/phase_a/phase_a_role_stability_stress_test/omega_scaling_check.csv`
- `solutions/phase_a/phase_a_role_stability_stress_test/stress_summary.json`
- `solutions/phase_a/phase_a_role_stability_stress_test/summary.md`
- `notes/phase_a/phase_a_parameter_geometry_assessment_2026-03-28.md`
- `notes/phase_a/phase_a_role_stability_stress_test_assessment_2026-03-28.md`

---

### 3.2 $\theta,\phi,\rho$ are genuinely distinct local angular directions

**Claim:** Away from singular sheets, $\theta,\phi,\rho$ form three independent local tangent directions on the ordered-state manifold rather than a redundant repackaging of one parameter.

**Method and rationale:** The updated parameter-geometry scan evaluates the Jacobian on 35,937 active-domain grid points at fixed $\omega=0$, records rank and determinant behavior, and checks named benchmark points. This tests local coordinate independence directly.

**Results:** The scan is generically full rank, with the named benchmark points all satisfying:

- `rankJ = 4`
- equal angular tangent norms
- pairwise angular cosines numerically zero

The 8,712 coarse special points occur on repeated singular sheets rather than throughout the domain.

**Why this proves the claim:** A regular local chart with rank 4 and three independent angular tangent directions is sufficient to show that the three angular variables are locally real coordinate channels, not fake duplicates.

**Supporting documents:**

- `derivations/derivation_71_exponential_quaternion_parameter_mapping_clean.md`
- `analysis/phase_a/phase_a_parameter_geometry.py`
- `solutions/phase_a/phase_a_parameter_geometry/coarse_scan.csv`
- `solutions/phase_a/phase_a_parameter_geometry/named_points.json`
- `solutions/phase_a/phase_a_parameter_geometry/special_points.json`
- `solutions/phase_a/phase_a_parameter_geometry/summary.md`
- `notes/phase_a/phase_a_parameter_geometry_assessment_2026-03-28.md`

---

### 3.3 The chart singularity architecture is controlled by $\phi$

**Claim:** The loss of local angular-coordinate independence in the ordered chart is governed by $\phi$.

**Method and rationale:** Using the exact Jacobian entries from the ordered map, the singularity analysis compares `detJ` to the candidate law

$$
\det J = e^{4\omega}\cos(2\phi)
$$

across 55,539 sampled points on the active domain. A separate 71,825-row unit-scale factor check compares `detJ` directly to `cos(2phi)` at $\omega=0$.

**Results:** The active-domain scan finds maximum absolute discrepancy

$$
3.979039320256561\times10^{-13},
$$

while the unit-scale factor check finds maximum absolute discrepancy

$$
9.992007221626409\times10^{-16}.
$$

The singular condition is therefore

$$
\cos(2\phi)=0
\quad\Longleftrightarrow\quad
\phi=\frac{\pi}{4}+\frac{n\pi}{2},
$$

which yields the repeated slices $\pm\pi/4$, $\pm3\pi/4$, $\pm5\pi/4$, and $\pm7\pi/4$ inside the active box.

**Why this proves the claim:** The determinant law shows that $\omega$ only rescales magnitude while $\phi$ alone decides where the chart loses angular rank. The widened unquotiented box reveals repeated copies of the same singular law, not a different rule.

**Supporting documents:**

- `derivations/derivation_72_phase_a_jacobian_singularity_structure.md`
- `analysis/phase_a/phase_a_singularity_structure.py`
- `solutions/phase_a/phase_a_singularity_structure/candidate_factor_check.csv`
- `solutions/phase_a/phase_a_singularity_structure/domain_singular_points.json`
- `solutions/phase_a/phase_a_singularity_structure/phi_reference_table.json`
- `solutions/phase_a/phase_a_singularity_structure/phi_slice_table.csv`
- `solutions/phase_a/phase_a_singularity_structure/summary.md`
- `notes/phase_a/phase_a_singularity_structure_assessment_2026-03-28.md`

---

### 3.4 The angular asymmetry is relational, not a norm hierarchy

**Claim:** $\phi$ acts as an orthogonal separator or mixing controller for the $\theta$-$\rho$ pair rather than as just another equal-role peer direction.

**Method and rationale:** This claim is supported only after symmetric comparison. Phase A combines:

- Gram-matrix / singular-value diagnostics,
- direct pairwise cosine scans,
- and the wider role-stability stress test.

These methods test whether any asymmetry survives beyond raw determinant-zero language.

**Results:** The evidence is consistent across all three supporting analyses:

- channel norms remain equal everywhere sampled,
- `cos(theta,phi)` and `cos(phi,rho)` remain near zero to machine precision,
- `cos(theta,rho)` spans the full `[-1,1]` range in the broad phi-control scan,
- the dense fixed-pair phi profile also sweeps continuously from `-1.0` to `1.0000000000000002`,
- the `phi_scan` drives `sigma_min` to `0.0` and the condition number to `100458282.95159373`,
- the `theta_scan_phi0` and `rho_scan_phi0` keep condition `1.0` throughout.

**Why this proves the claim:** If the three channels remain equal in norm but only $\phi$ controls the angular conditioning and the relation between $\theta$ and $\rho`, then the asymmetry is geometric and relational rather than a raw magnitude hierarchy.

**Supporting documents:**

- `analysis/phase_a/phase_a_channel_role_hypothesis.py`
- `analysis/phase_a/phase_a_invariant_channel_comparison.py`
- `analysis/phase_a/phase_a_role_stability_stress_test.py`
- `solutions/phase_a/phase_a_channel_role_hypothesis/broad_phi_control_scan.csv`
- `solutions/phase_a/phase_a_channel_role_hypothesis/phi_profile_fixed_pair.csv`
- `solutions/phase_a/phase_a_channel_role_hypothesis/theta_rho_independence_scan.csv`
- `solutions/phase_a/phase_a_channel_role_hypothesis/summary.md`
- `solutions/phase_a/phase_a_invariant_channel_comparison/phi_scan.csv`
- `solutions/phase_a/phase_a_invariant_channel_comparison/theta_scan_phi0.csv`
- `solutions/phase_a/phase_a_invariant_channel_comparison/rho_scan_phi0.csv`
- `solutions/phase_a/phase_a_invariant_channel_comparison/named_points.json`
- `solutions/phase_a/phase_a_invariant_channel_comparison/summary.md`
- `solutions/phase_a/phase_a_role_stability_stress_test/stress_scan.csv`
- `solutions/phase_a/phase_a_role_stability_stress_test/stress_summary.json`
- `solutions/phase_a/phase_a_role_stability_stress_test/summary.md`
- `notes/phase_a/phase_a_channel_role_hypothesis_assessment_2026-03-28.md`
- `notes/phase_a/phase_a_invariant_channel_comparison_assessment_2026-03-28.md`
- `notes/phase_a/phase_a_role_stability_stress_test_assessment_2026-03-28.md`

---

### 3.5 $\theta$ and $\rho$ form the active paired subsystem under the Phase A slice protocol

**Claim:** The ordered map contains a paired subsystem $(\theta,\rho)$ whose local distinctness is controlled by $\phi$.

**Method and rationale:** The plan requires both 1D and 2D slices. Phase A therefore tests the claim with explicit slices rather than only bulk scans:

- hold two variables fixed and sweep one,
- hold one variable fixed and sweep two.

This makes the singular architecture and paired-subsystem behavior directly visible.

**Results:** The regenerated slice studies show:

- phi sweeps hit `8` singular points across the active interval,
- `vary_theta_phi0_rho0` and `vary_rho_theta0_phi0` remain completely regular,
- `vary_theta_phi_pi4_rho0` and `vary_rho_theta0_phi_pi4` are singular at all `65 / 65` sampled points,
- `theta_rho_phi0` contains `0 / 1089` singular points,
- `theta_rho_phi_pi4` contains `1089 / 1089` singular points.

The mixed `theta-phi` and `phi-rho` 2D slices show repeated singular sheets because $\phi$ is one of the scanned axes.

**Why this proves the claim:** The 1D and 2D slices show directly that $\theta$ and $\rho$ vary regularly as a pair when $\phi$ is regular, and collapse together when $\phi$ is set to a singular value. That is the cleanest concrete demonstration of the paired-subsystem interpretation.

**Supporting documents:**

- `analysis/phase_a/phase_a_slice_studies.py`
- `solutions/phase_a/phase_a_slice_studies/one_d_summary.json`
- `solutions/phase_a/phase_a_slice_studies/two_d_summary.json`
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
- `solutions/phase_a/phase_a_slice_studies/summary.md`
- `notes/phase_a/phase_a_slice_study_assessment_2026-03-28.md`

---

## 4. Final Phase A answer to the plan’s key question

The key Phase A question in `notes/classical_exploration_plan.md` is:

> Are the angular parameters genuinely different classical characteristics?

The audited answer is:

- **Yes at the mapping level.** The three angles are locally distinct coordinate directions away from singular sheets.
- **Yes in a relational sense.** The channels are not interchangeable peers: $\phi$ is structurally different because it controls singularity placement and the coupling geometry of the $\theta$-$\rho$ pair.
- **Not yet at the object-observable level.** Phase A does not by itself prove that the same role structure already appears in later classical observables or in the field equations.

So the clean Phase A role picture is:

- **$\omega$** = scale coordinate
- **$\phi$** = orthogonal separator / mixing-control coordinate
- **$\theta,\rho$** = paired internal structural directions

This role picture is synthesized in:

- `notes/phase_a/phase_a_synthesis_2026-03-28.md`

---

## 5. What Phase A has not established

Phase A has **not** established:

- a full classical structured-object interpretation,
- a dynamical field-equation dominance claim for one angular channel,
- a particle-property interpretation,
- or a completed object-level trait map for later phases.

The phase establishes something narrower but necessary:

> the ordered quaternion parameter foundation is coherent, stress-tested, and structured enough to support later classical work without collapsing the three-angle story prematurely.

---

## 6. Why closure is justified

Phase A is closed because its explicit burden of proof is met:

1. scale is cleanly separated from angular geometry,
2. the three angular channels are locally real and distinct,
3. the singular architecture is identified precisely and tied to $\phi$,
4. the angular asymmetry is shown to be relational rather than a norm hierarchy,
5. the paired-subsystem interpretation is visible directly in the required slice protocol,
6. and every supporting Phase A solution directory now has an interpretive summary tied to the raw outputs.

Further Phase A work would mostly repeat the same mapping-level conclusion unless a new objection appears.

---

## 7. Recommended handoff

Later phases should treat the Phase A result as a foundation, not as a substitute for object-level evidence:

1. use $\omega$ as the established scale coordinate,
2. preserve the paired-role picture of $(\theta,\rho)$ with $\phi$ as controller,
3. test in Phases B and C whether these mapping-level roles correlate with compactness, concentration, external profile behavior, and other structured-object traits,
4. avoid translating the Phase A asymmetry directly into physical dominance claims without later-phase support.

---

## 8. Bottom line

**Bottom line:** Phase A now supports a complete and traceable ordered-map foundation for Khantraction. The paper’s toy-model motivation requires exactly this kind of disciplined starting point: one pure scale coordinate $\omega$, three locally distinct angular directions, a repeated singular-sheet architecture controlled by $\phi$, and a robust relational role picture in which $\phi$ acts as the orthogonal separator or mixing controller for the paired directions $\theta$ and $\rho$. That is sufficient to close the parameter-foundation phase and proceed to later structured-object work without overclaiming what the map alone can prove.
