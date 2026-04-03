# Phase D Assessment — Identity and Persistence Audit Refresh

**Date:** 2026-04-02
**Phase:** D — Identity and persistence
**Status:** Complete after audit refresh

## Purpose

This note records what the refreshed Phase D analysis actually proves after tracing the Phase D code, regenerated solution package, and the inherited Phase A and Phase C support trail.

Relevant files:
- `analysis/phase_d/phase_d_identity_analysis.py`
- `derivations/derivation_72_phase_a_jacobian_singularity_structure.md`
- `derivations/derivation_78_maurer_cartan_tensor.md`
- `derivations/derivation_79_einstein_trace_with_mc_breaking.md`
- `solutions/phase_d/phase_d_identity/summary.json`
- `solutions/phase_d/phase_d_identity/summary.md`
- `solutions/phase_d/phase_d_identity/omega_sweep_invariance.csv`
- `solutions/phase_d/phase_d_identity/neighborhood_results.csv`
- `solutions/phase_d/phase_d_identity/phi_neighborhood_persistence.csv`
- `solutions/phase_d/phase_d_identity/amplitude_sensitivity.csv`
- `solutions/phase_d/phase_d_identity/outer_box_sensitivity.csv`
- `solutions/phase_d/phase_d_identity/rigidity_results.csv`
- `solutions/phase_d/phase_d_identity/slice_1d_theta.csv`
- `solutions/phase_d/phase_d_identity/slice_1d_phi.csv`
- `solutions/phase_d/phase_d_identity/slice_1d_rho.csv`
- `solutions/phase_d/phase_d_identity/slice_2d_phi_theta.csv`
- `solutions/phase_d/phase_d_identity/slice_2d_phi_rho.csv`
- `solutions/phase_d/phase_d_identity/slice_2d_theta_rho.csv`

---

## 1. What the active runtime actually is

Phase D does not introduce a new independent physical runtime. It reuses the same exploratory symmetry-broken Maurer-Cartan family audited in Phase C.

The regenerated `summary.json` records the active runtime:
- anisotropic Maurer-Cartan weights `beta = [0.01, 0.02, 0.03]`,
- metric regularization `1e-4`,
- exploratory phi-localized angular potential coefficient `0.01`,
- horizon event threshold `2m/r = 0.48`.

So the Phase D identity claims must be interpreted inside that same exploratory runtime, not as closure-independent statements about the whole theory.

---

## 2. What was tested

The refreshed Phase D package now checks four distinct layers:

1. **Scale sweep**
   - scalar-like anchor,
   - vary `omega` from `0.1` to `1.0`.
2. **Local neighborhood tests across multiple sectors**
   - scalar local `phi` neighborhood,
   - scalar local `theta` neighborhood,
   - scalar local `rho` neighborhood,
   - exact `phi = pi/4` sheet neighborhood,
   - off-sheet `phi = pi/4 - 0.1` neighborhood.
3. **Amplitude and outer-box sensitivity**
   - scalar anchor,
   - exact `phi`-sheet anchor,
   - off-sheet `phi`-rich anchor.
4. **Full 1D / 2D slice protocol**
   - 1D `theta`, `phi`, `rho`,
   - 2D `(phi, theta)`, `(phi, rho)`, `(theta, rho)`,
   - all on the active `[-2pi, 2pi]` domain.

The refreshed package also records:
- solver status,
- termination flag,
- event radii,
- final integration radius,
- final `2m/r`,
- mass half-radius,
- compactness.

That was missing from the old Phase D evidence trail and is why the old persistence and rigidity wording had to be corrected.

---

## 3. Main findings

### 3.1 Scale is not an identity invariant

The scalar-anchor omega sweep gives:
- mass range `0.048970575487133336` to `0.292827303719029`
- compactness range `0.0029769162186193245` to `0.018070097992401075`

So increasing `omega` changes concentration materially. The current runtime does **not** provide a scale-free fingerprint.

### 3.2 Local identity structure is phi-controlled

The neighborhood widths make the local hierarchy explicit:

- `scalar_phi_local` mass width: `0.22487621802996025`
- `scalar_theta_local` mass width: `1.0433934272136014e-10`
- `scalar_rho_local` mass width: `1.0433934272136014e-10`

So near the scalar anchor:
- theta and rho perturbations are effectively flat,
- phi perturbations change the diagnostics smoothly and substantially.

### 3.3 The exact phi sheet is a boundary, not a stable anchor

The `phi_sheet_local` neighborhood has:
- mass range `1.624428095692695` to `3.546781283731745`
- one early-termination point out of five,
- the exact center `phi = pi/4` terminating at `r_final = 3.3842251993597814`
- final `2m/r = 0.96` at termination.

The nearby off-sheet configurations survive the full interval.

That means the exact sheet behaves like a boundary or cliff in the current runtime, not like a regular persistent anchor.

### 3.4 Off-sheet phi-rich families do persist locally on the regular side of the boundary

The `phi_offsheet_local` neighborhood shows:
- four regular full-interval survivors out of five,
- the only failure occurs when the perturbation lands exactly on the sheet point `phi = pi/4`,
- off-sheet masses vary smoothly from `1.6600901450754204` up to `3.546781283731745`.

So local persistence does exist, but it is a **basin on the regular side of the phi-sheet boundary**, not a globally rigid or discrete species classification.

### 3.5 Absolute rigidity is not supported

This is the strongest correction to the old Phase D wording.

For the full-domain survivor anchors:

- `scalar_anchor` amplitude sweep mass range:
  - `0.027643479141357258` to `0.43000782356100903`
- `phi_offsheet_anchor` amplitude sweep mass range:
  - `3.298437414992291` to `4.411386960981549`
- `scalar_anchor` outer-box mass range:
  - `0.0027560790801170907` to `0.1081453845055517`
- `phi_offsheet_anchor` outer-box mass range:
  - `1.1714031692048743` to `3.546781283731745`

Those are large sensitivities, not rigidity.

The old rigid-looking result at the exact `phi` sheet was a confound:
- the `phi_sheet_anchor` terminates early at `r ≈ 3.384`,
- so changing `r_max` from `20` to `15`, `10`, or `5` does not probe extra outer structure at all.

So the current Phase D data does **not** justify an absolute-rigidity claim.

### 3.6 The full slice protocol supports continuous families organized by phi boundaries, not discrete quantized species

The refreshed slice widths are:

- 1D theta width: `2.809530386116421e-12`
- 1D phi width: `2.4327877853861755`
- 1D rho width: `0.20970378739973938`
- 2D `(phi, theta)` width: `1.2541278883210587`
- 2D `(phi, rho)` width: `1.2541278883210587`
- 2D `(theta, rho)` width: `0.1072005551222078`

These slices are smooth on their audited regular regions, with no early terminations on the finite `r_max = 10` and `r_max = 5` slice boxes.

That supports:
- continuous families inside regular regions,
- strong phi-controlled differentiation,
- weaker theta/rho structure away from phi boundaries.

It does **not** by itself support a discrete quantized-species claim.

---

## 4. Correct interpretation

The refreshed Phase D result is narrower and more disciplined than the old wording:

- identity is currently best described as **local family structure inside regular phi-controlled basins**,
- the exact phi sheets act as boundaries where behavior can change sharply,
- scale variation is not an invariant identity direction,
- and universal rigidity is not supported by the regenerated sensitivity tests.

The phase therefore supports the following audited statement:

> In the current exploratory symmetry-broken runtime, Khantraction identity is local and boundary-organized rather than scale-invariant or discretely quantized. The strongest organizing variable remains phi, and the present data does not support an absolute rigidity claim.

---

## 5. Bottom line

**Bottom line:** Phase D does distinguish scale variation from angular variation and does identify locally persistent regular families away from the phi singular sheets. But it does **not** prove scale-invariant fingerprints, absolute rigidity, or discrete quantized classical species. The strongest supported reading is a phi-boundary-organized family picture inside the current exploratory runtime.
