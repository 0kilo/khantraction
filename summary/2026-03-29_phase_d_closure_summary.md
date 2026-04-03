# Phase D Closure Summary — Identity and Persistence Audit

**Date:** 2026-03-29  
**Phase:** D — Identity and persistence  
**Status:** Closed after audit refresh

## 0. Project-level disposition

Phase D remains useful for local family persistence and phi-organized identity structure, but its older discrete rigid-species claim is retired in the project-level closure plan unless a new invariant is derived. It is not one of the decisive blockers for the final classical particle-level verdict. The governing synthesis is recorded in `summary/2026-04-02_gap_closure_summary.md`, `notes/2026-04-02_direct_data_closure_plan.md`, and `summary/2026-04-02_khantraction_model_conclusion.md`.

## 1. Scope and motivation

`khantraction_paper.md` presents Khantraction as a speculative toy model of structured spacetime-fold objects, not as a finished particle theory.

That framing matters again in Phase D.

After Phase C, the project had already learned that:
- the native linear-basis runtime is angularly blind,
- the active Maurer-Cartan-based runtime is exploratory rather than final,
- and phi is the dominant driver of the observed angular trait splitting.

So Phase D was not supposed to jump to fully quantized particle labels. Its narrower burden was:

- test neighborhood stability around multiple sectors,
- distinguish scale variation from angular and structural variation,
- see what kind of local family fingerprints exist,
- and test whether any strong rigidity claim survives contact with the data.

The active Phase D convention remained:

- `omega > 0`
- `theta, phi, rho in [-2pi, 2pi]`
- no redundancy quotienting

That framing is consistent with:
- `khantraction_paper.md`
- `notes/classical_exploration_plan.md`

---

## 2. Audit against `notes/classical_exploration_plan.md`

### 2.1 Goal 1 — Test neighborhood stability around multiple angular sectors

**Status:** Met after audit refresh.

**How it was tested:** The refreshed Phase D package now includes local neighborhoods around:

- scalar local `phi`,
- scalar local `theta`,
- scalar local `rho`,
- the exact `phi = pi/4` sheet,
- and an off-sheet `phi`-rich anchor at `phi = pi/4 - 0.1`.

Each run now records status, termination, event radii, and final integration radius.

**Why this proves the goal:** The plan required multiple sectors, not a single favored anchor. The refreshed package now checks several distinct local sectors and distinguishes regular neighborhoods from boundary points.

### 2.2 Goal 2 — Identify which deformations preserve object identity

**Status:** Met at the local-family level.

**How it was tested:** The neighborhood tables compare whether nearby perturbations remain regular, how their masses and concentration diagnostics move, and whether they terminate early.

**Why this proves the goal:** The data now shows which deformations remain inside the same broad regular family and which land on the phi-controlled boundary.

### 2.3 Goal 3 — Distinguish scale variation from angular and structural variation

**Status:** Met.

**How it was tested:** The refreshed package combines:

- a scalar-anchor omega sweep,
- local neighborhood tests,
- and the full 1D / 2D slice protocol.

**Why this proves the goal:** The omega sweep shows that scale changes concentration materially, while the neighborhoods and slices show that angular variation is highly anisotropic and dominated by phi.

### 2.4 Goal 4 — Build robust family fingerprints

**Status:** Partially met, but not in the strong species sense the old wording implied.

**How it was tested:** The analysis tracks mass, half-radius, compactness, termination behavior, final `2m/r`, and position relative to phi-sheet boundaries.

**Why this proves the goal:** These diagnostics are enough to build a local family description. But they do **not** yield a scale-invariant or discrete universal species fingerprint.

### 2.5 Goal 5 — Test internal rigidity

**Status:** Not met in the strong sense claimed by the old summary.

**How it was tested:** The refreshed package separates:

- amplitude sensitivity,
- and outer-box sensitivity

for three representative anchors:
- scalar,
- exact phi-sheet,
- and off-sheet phi-rich.

**Why this proves the goal:** This is the right test because it separates a genuine survivor-anchor sensitivity check from the earlier confounded sheet-anchor test.

### 2.6 Common slice protocol

**Status:** Met after audit refresh.

The audited Phase D slice set is:

- 1D `theta` slice: fix `omega = 0.5`, `phi = pi/8`, `rho = 0`
- 1D `phi` slice: fix `omega = 0.5`, `theta = 0`, `rho = 0`
- 1D `rho` slice: fix `omega = 0.5`, `theta = 0`, `phi = pi/8`
- 2D `(phi, theta)` slice: fix `omega = 0.5`, `rho = 0`
- 2D `(phi, rho)` slice: fix `omega = 0.5`, `theta = 0`
- 2D `(theta, rho)` slice: fix `omega = 0.5`, `phi = pi/8`

All use the active `[-2pi, 2pi]` angular box.

### 2.7 Phase D key question

The plan asks:

> What makes one Khantraction object the “same kind” of object in classical terms, and is its core rigid enough to persist?

After the audit, the answer is:

- **same-kind identity:** currently best described as local family membership inside regular phi-controlled basins,
- **global discrete species:** not established,
- **scale-invariant fingerprint:** not established,
- **universal rigidity:** not established.

That is the actual Phase D result.

---

## 3. Final Phase D conclusions

### 3.1 Scale is not an identity invariant in the current runtime

**Claim:** Varying `omega` changes concentration materially, so scale is not a neutral identity direction in the current exploratory runtime.

**Method and rationale:** The correct test is a scalar-anchor omega sweep. If scale were a true identity-invariant direction, compactness-like diagnostics would remain effectively fixed under omega variation.

**Results:** The refreshed omega sweep finds:

- mass range = `0.048970575487133336` to `0.292827303719029`
- compactness range = `0.0029769162186193245` to `0.018070097992401075`

with no early terminations on the audited sweep.

**Why this proves the claim:** Those changes are substantial, not floating-point noise. So scale is not an invariant fingerprint axis here.

**Supporting documents:**

- `analysis/phase_d/phase_d_identity_analysis.py`
- `solutions/phase_d/phase_d_identity/omega_sweep_invariance.csv`
- `solutions/phase_d/phase_d_identity/summary.json`
- `solutions/phase_d/phase_d_identity/summary.md`
- `notes/phase_d/phase_d_verified_identity_assessment.md`

---

### 3.2 Local family structure is strongly phi-controlled

**Claim:** In the refreshed Phase D runtime, local identity structure is dominated by phi, while theta and rho remain much weaker around scalar-like sectors.

**Method and rationale:** The right test is not just global slices. It is local neighborhoods around multiple sectors, because identity and persistence are local-family questions first.

**Results:** Around the scalar anchor, the neighborhood widths are:

- `scalar_phi_local` mass width = `0.22487621802996025`
- `scalar_theta_local` mass width = `1.0433934272136014e-10`
- `scalar_rho_local` mass width = `1.0433934272136014e-10`

The refreshed 1D slice widths are consistent with that pattern:

- 1D `theta` width = `2.809530386116421e-12`
- 1D `phi` width = `2.4327877853861755`
- 1D `rho` width = `0.20970378739973938`

**Why this proves the claim:** Theta and rho are nearly flat around the scalar neighborhood, while phi changes the diagnostics strongly. So the local family structure is not symmetric across the angles.

**Supporting documents:**

- `analysis/phase_d/phase_d_identity_analysis.py`
- `solutions/phase_d/phase_d_identity/neighborhood_results.csv`
- `solutions/phase_d/phase_d_identity/slice_1d_theta.csv`
- `solutions/phase_d/phase_d_identity/slice_1d_phi.csv`
- `solutions/phase_d/phase_d_identity/slice_1d_rho.csv`
- `solutions/phase_d/phase_d_identity/summary.json`
- `solutions/phase_d/phase_d_identity/summary.md`
- `notes/phase_d/phase_d_verified_identity_assessment.md`

---

### 3.3 The exact phi sheets act like identity boundaries, not regular stable anchors

**Claim:** The exact `phi = pi/4` sheet is not a regular persistent anchor in the active runtime. It behaves like a boundary or cliff between regular neighboring families.

**Method and rationale:** Phase A already established that phi controls the singular-sheet architecture of the ordered map. The right Phase D test is therefore to run local neighborhoods across and near the sheet while recording status and termination behavior.

**Results:** In the refreshed `phi_sheet_local` neighborhood:

- the exact center `phi = pi/4` terminates early,
- `status = 1`,
- event radius `r = 3.3842251993597814`,
- final `2m/r = 0.96`,
- nearby off-sheet points survive to the full `r_max = 20`.

The `phi_offsheet_local` neighborhood confirms the same picture:
- regular off-sheet points survive,
- the one perturbation that lands exactly on `phi = pi/4` is the one that terminates early.

**Why this proves the claim:** The sheet point is dynamically special in exactly the way the inherited Phase A geometry suggests. It acts like a boundary, not a flat stable anchor basin.

**Supporting documents:**

- `derivations/derivation_72_phase_a_jacobian_singularity_structure.md`
- `notes/phase_a/phase_a_singularity_structure_assessment_2026-03-28.md`
- `analysis/phase_d/phase_d_identity_analysis.py`
- `solutions/phase_d/phase_d_identity/neighborhood_results.csv`
- `solutions/phase_d/phase_d_identity/phi_neighborhood_persistence.csv`
- `solutions/phase_d/phase_d_identity/summary.json`
- `solutions/phase_d/phase_d_identity/summary.md`
- `notes/phase_d/phase_d_verified_identity_assessment.md`

---

### 3.4 The current evidence supports continuous regular families separated by phi boundaries, not discrete quantized species

**Claim:** The refreshed Phase D evidence supports a boundary-organized family picture, not a discrete quantized-species picture.

**Method and rationale:** To support discrete species, the data would need to show something stronger than smooth regular-region variation plus boundary effects. The full neighborhood and slice package is the right test because it reveals whether the landscape is continuous inside regular regions.

**Results:** The refreshed 2D slice widths are:

- `(phi, theta)` width = `1.2541278883210587`
- `(phi, rho)` width = `1.2541278883210587`
- `(theta, rho)` width = `0.1072005551222078`

and the audited 1D / 2D slice boxes contain no early terminations on their finite `r_max = 10` and `r_max = 5` domains.

The neighborhoods also move smoothly inside regular regions until the exact phi boundary is hit.

**Why this proves the claim:** Smooth regular-region variation plus a sharp sheet boundary is evidence for continuous families separated by boundaries. It is not yet evidence for discrete quantized species.

**Supporting documents:**

- `analysis/phase_d/phase_d_identity_analysis.py`
- `solutions/phase_d/phase_d_identity/neighborhood_results.csv`
- `solutions/phase_d/phase_d_identity/slice_2d_phi_theta.csv`
- `solutions/phase_d/phase_d_identity/slice_2d_phi_rho.csv`
- `solutions/phase_d/phase_d_identity/slice_2d_theta_rho.csv`
- `solutions/phase_d/phase_d_identity/summary.json`
- `solutions/phase_d/phase_d_identity/summary.md`
- `notes/phase_d/phase_d_verified_identity_assessment.md`
- `notes/phase_d/phase_d_synthesis_2026-04-02.md`

---

### 3.5 Absolute rigidity is not supported by the refreshed sensitivity tests

**Claim:** The old absolute-rigidity wording is not defensible after the audit refresh.

**Method and rationale:** The refreshed Phase D package separates:

- amplitude sensitivity,
- and outer-box sensitivity

for three anchors:
- scalar,
- exact phi-sheet,
- off-sheet phi-rich.

That is the right test because it exposes whether the apparent rigidity survives once the confounded sheet-anchor case is separated from full-domain survivors.

**Results:** For full-domain survivors:

- `scalar_anchor` amplitude mass range = `0.027643479141357258` to `0.43000782356100903`
- `phi_offsheet_anchor` amplitude mass range = `3.298437414992291` to `4.411386960981549`
- `scalar_anchor` outer-box mass range = `0.0027560790801170907` to `0.1081453845055517`
- `phi_offsheet_anchor` outer-box mass range = `1.1714031692048743` to `3.546781283731745`

By contrast, the exact `phi_sheet_anchor` shows zero outer-box variation only because:
- it terminates early at `r ≈ 3.384`,
- so all tested `r_max` values lie outside the actual solved interval.

**Why this proves the claim:** Full-domain survivors are materially sensitive to both amplitude and outer-box choice. So the current data does not justify a universal rigidity claim. The old sheet-anchor rigidity story was an event-truncation artifact.

**Supporting documents:**

- `analysis/phase_d/phase_d_identity_analysis.py`
- `solutions/phase_d/phase_d_identity/amplitude_sensitivity.csv`
- `solutions/phase_d/phase_d_identity/outer_box_sensitivity.csv`
- `solutions/phase_d/phase_d_identity/rigidity_results.csv`
- `solutions/phase_d/phase_d_identity/summary.json`
- `solutions/phase_d/phase_d_identity/summary.md`
- `notes/phase_d/phase_d_verified_identity_assessment.md`
- `notes/phase_d/phase_d_synthesis_2026-04-02.md`

---

### 3.6 Phase D closes as a clarification phase on local identity, not as a proof of rigid discrete species

**Claim:** Phase D is complete, but the closed claim is narrower than the old wording.

**Method and rationale:** A phase can close by answering its key question negatively or conditionally, as long as the answer is clear and well supported.

**Results:** The refreshed package now supports the following final statement:

- scale is not an identity invariant,
- local family structure is phi-controlled,
- exact phi sheets act like identity boundaries,
- continuous regular families exist on the regular side of those boundaries,
- discrete quantized species are not established,
- absolute rigidity is not established.

**Why this proves the claim:** That is enough to answer the Phase D key question honestly. It clarifies what later phases may treat as established and what remains open.

**Supporting documents:**

- `khantraction_paper.md`
- `notes/classical_exploration_plan.md`
- `summary/2026-03-28_phase_a_closure_summary.md`
- `summary/2026-03-29_phase_c_closure_summary.md`
- `analysis/phase_d/phase_d_identity_analysis.py`
- `solutions/phase_d/summary.md`
- `solutions/phase_d/phase_d_identity/summary.md`
- `notes/phase_d/phase_d_verified_identity_assessment.md`
- `notes/phase_d/phase_d_synthesis_2026-04-02.md`
- `phase_d_audit_report.md`

---

## 4. What Phase D has not established

Phase D has **not** established:

- a scale-invariant identity fingerprint,
- discrete quantized classical species,
- universal core rigidity,
- an exact transition law between neighboring regular families,
- external particle-like behavior,
- hosting, chirality, or quantum spectra.

Those belong to later phases.

---

## 5. Why the phase is considered closed

Phase D is considered closed because its actual burden of proof has now been met in audited form:

- the multi-sector neighborhood requirement is satisfied,
- the full slice protocol is present,
- the active solver and outputs are traceable,
- the old rigidity confound is now explicit,
- and the key question has been answered honestly.

That answer is not “Phase D discovered rigid quantized species.” The answer is:

> in the current exploratory runtime, identity is local and phi-boundary-organized, while robust rigidity remains unproven.

---

## 6. Bottom line

**Bottom line:** Phase D does not justify the old claim that Khantraction already supports discrete, rigid classical species. What it does show is more disciplined and more useful: scale changes concentration, phi organizes the local identity landscape, exact phi sheets behave like boundary points, regular off-sheet families can persist locally, and universal rigidity is not supported by the refreshed sensitivity tests. That is the real Phase D result, and it is the one this closure summary now records.
