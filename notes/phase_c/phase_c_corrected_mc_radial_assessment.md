# Phase C Assessment — Exploratory Maurer-Cartan Trait Differentiation

**Date:** 2026-04-02
**Phase:** C — Distinct angular traits
**Status:** Complete after audit refresh

## Purpose

This note records what the refreshed Phase C solver actually proves after the audit pass.

Relevant files:
- `analysis/phase_c/phase_c_mc_radial_solver.py`
- `derivations/derivation_78_maurer_cartan_tensor.md`
- `derivations/derivation_79_einstein_trace_with_mc_breaking.md`
- `solutions/phase_c/phase_c_angular_traits/summary.json`
- `solutions/phase_c/phase_c_angular_traits/summary.md`
- `solutions/phase_c/phase_c_angular_traits/representative_seed_results.csv`
- `solutions/phase_c/phase_c_angular_traits/angle_only_anchor_results.csv`
- `solutions/phase_c/phase_c_angular_traits/slice_1d_theta.csv`
- `solutions/phase_c/phase_c_angular_traits/slice_1d_phi.csv`
- `solutions/phase_c/phase_c_angular_traits/slice_1d_rho.csv`
- `solutions/phase_c/phase_c_angular_traits/slice_2d_theta_rho.csv`
- `solutions/phase_c/phase_c_angular_traits/slice_2d_phi_theta.csv`
- `solutions/phase_c/phase_c_angular_traits/slice_2d_phi_rho.csv`
- `solutions/phase_c/phase_c_angular_traits/profiles/scalar.csv`
- `solutions/phase_c/phase_c_angular_traits/profiles/phi_dom.csv`

---

## 1. What the active runtime actually is

The derivation layer justifies an anisotropic Maurer-Cartan symmetry-breaking term. The active audited runtime is slightly broader than that derivation-only core.

The regenerated `summary.json` records the runtime actually used:
- anisotropic Maurer-Cartan weights `beta = [0.01, 0.02, 0.03]`,
- metric regularization `1e-4`,
- exploratory phi-localized angular potential coefficient `0.01`,
- horizon event threshold `2m/r = 0.45`.

So the current Phase C solver should be interpreted as an **exploratory symmetry-broken runtime**, not as a pure derivation-78/79 implementation with no extra runtime devices.

---

## 2. What was tested

The refreshed solver now checks four distinct layers:

1. **Representative seeded anchors**
   - scalar,
   - theta-dominant,
   - phi-dominant,
   - fully mixed.
2. **Angle-only anchors**
   - same angle values as the representative seeds,
   - but with zero initial angle-derivative seeding,
   - to separate angle-value effects from derivative-seeding effects.
3. **1D slice protocol**
   - vary `theta` with `omega = 0.5`, `phi = pi/8`, `rho = 0`,
   - vary `phi` with `omega = 0.5`, `theta = 0`, `rho = 0`,
   - vary `rho` with `omega = 0.5`, `theta = 0`, `phi = pi/8`,
   - always on `[-2pi, 2pi]`.
4. **2D slice protocol**
   - vary `(theta, rho)` with `omega = 0.5`, `phi = pi/8`,
   - vary `(phi, theta)` with `omega = 0.5`, `rho = 0`,
   - vary `(phi, rho)` with `omega = 0.5`, `theta = 0`,
   - always on `[-2pi, 2pi]^2`.

This now satisfies the Phase C plan requirement that all 1D channels and all 2D angle pairings be included on the active unquotiented domain.

---

## 3. Main findings

### 3.1 The active runtime does split the channels

The representative runs and the angle-only anchors show the same broad pattern:

- `scalar` and `theta_dom` both reach the full `r_max = 20` interval with
  - final mass about `0.108039`,
  - mass half-radius `14.6501`,
  - mass 90% radius `18.9801`,
  - core mass fraction about `2.04e-4`.
- `phi_dom` and `fully_mixed` both terminate early near the horizon event with
  - final mass about `1.465564`,
  - mass half-radius `2.6001`,
  - mass 90% radius `3.1601`,
  - core mass fraction about `2.78e-2`,
  - termination radius about `3.2701`,
  - event radius about `3.27676554`.

That means the symmetry-broken runtime does produce visibly different macroscopic diagnostics across angular sectors.

### 3.2 The strongest effect is phi, not theta

The 1D slice widths make the channel hierarchy explicit:

- `theta` slice mass width: `6.069374447470466e-10`
- `rho` slice mass width: `0.20494570186855265`
- `phi` slice mass width: `1.9239803098587736`

So on the audited standalone 1D slices:
- `theta` is nearly flat,
- `rho` has a moderate standalone effect,
- `phi` is the dominant driver of mass variation.

### 3.3 Theta is weak alone but not absent from the paired structure

The 2D slice widths are:

- `(theta, rho)` width: `0.1059810327281174`
- `(phi, theta)` width: `1.0914284604307958`
- `(phi, rho)` width: `1.0914284604307958`

This shows that theta is not the leading standalone driver, but it still participates in the paired angular structure once one leaves the trivial theta-only slice.

### 3.4 The strongest phi-rich representative states are not full-domain survivors

This is the most important correction to the older wording.

The high-mass representative `phi_dom` and `fully_mixed` states do **not** survive to the full `r_max = 20` interval. They terminate early at the horizon event with final `2m/r` about `0.896342`.

So the correct interpretation is:

> the Phase C runtime shows strong phi-driven trait differentiation, but the most dramatic phi-rich representative states are near-horizon exploratory diagnostics rather than fully settled full-domain survivors.

---

## 4. Correct interpretation

The refreshed Phase C conclusion is narrower and stronger at the same time:

- stronger, because it now rests on representative anchors, angle-only anchors, and all 1D/2D slice families on the active domain;
- narrower, because it no longer pretends that the strongest phi-rich states are already established as fully regular long-range objects.

The phase therefore supports the following audited statement:

> Once the angularly blind linear-basis runtime of Phase B is replaced by the present exploratory Maurer-Cartan-based symmetry-broken runtime, the angular variables produce genuinely different trait diagnostics, with phi as the dominant driver, rho as a secondary driver, and theta weak on the audited standalone slice.

---

## 5. Bottom line

**Bottom line:** Phase C now closes as an exploratory proof-of-principle trait-differentiation phase. It does show that the angular variables can produce different classical diagnostics once explicit symmetry-breaking machinery is introduced, but it does **not** yet prove that the strongest phi-rich states are fully regular species that persist to the full outer domain.
