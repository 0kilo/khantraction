# Phase H Assessment — Semiclassical Proxy Audit Refresh

**Date:** 2026-04-02
**Phase:** H — Return to Stronger Quantum-Facing Work
**Status:** Complete after audit refresh

## Purpose

This note records what the refreshed Phase H package actually proves after tracing:

- `khantraction_paper.md`
- `notes/classical_exploration_plan.md`
- `derivations/derivation_84_quantum_excitation_ansatz.md`
- `derivations/derivation_85_discrete_spectrum_conditions.md`
- `derivations/derivation_82_classical_chirality_operators.md`
- `summary/2026-03-29_phase_f_closure_summary.md`
- `notes/phase_f/phase_f_verified_hosting_assessment.md`
- `summary/2026-03-29_phase_g_closure_summary.md`
- `notes/phase_g/phase_g_verified_chirality_assessment.md`
- `analysis/phase_h/phase_h_quantum_analysis.py`
- `solutions/phase_h/phase_h_quantum/summary.json`
- `solutions/phase_h/phase_h_quantum/summary.md`
- `solutions/phase_h/phase_h_quantum/excitation_spectrum.json`
- `solutions/phase_h/phase_h_quantum/representative_spectra.csv`
- `solutions/phase_h/phase_h_quantum/pair_comparisons.csv`
- `solutions/phase_h/phase_h_quantum/loading_sensitivity.csv`
- `solutions/phase_h/phase_h_quantum/slice_1d_theta_energy.csv`
- `solutions/phase_h/phase_h_quantum/slice_1d_phi_energy.csv`
- `solutions/phase_h/phase_h_quantum/slice_1d_rho_energy.csv`
- `solutions/phase_h/phase_h_quantum/slice_2d_phi_theta_energy.csv`
- `solutions/phase_h/phase_h_quantum/slice_2d_theta_rho_energy.csv`
- `solutions/phase_h/phase_h_quantum/slice_2d_phi_rho_energy.csv`

---

## 1. What the active runtime actually is

The refreshed Phase H runtime is not a full quantum field solve and it is not built from a regenerated trapping well extracted from the audited Phase F backgrounds.

It is a narrower semiclassical proxy:

- a hand-built quartic resonator well with depth `0.999`,
- a direct chirality shift `lambda_chi * chi`,
- a Gaussian loading shift,
- a fixed Bohr-Sommerfeld box size `r_h = 3.0`,
- and a fixed energy bracket `[0.01, 2.0]`.

The `summary.json` file records that scope explicitly:

- `type = semiclassical_proxy`
- `hosting_depth_proxy = 0.999`
- `lambda_chi = 0.05`
- `mu_eff = 0.5`
- `r_h_proxy = 3.0`

So every Phase H claim has to be read as a result about this proxy ansatz, not as a proof that the refreshed classical runtime already generates a native quantum operator and spectrum from first principles.

---

## 2. Main audit corrections

### 2.1 The old handedness comparison was wrong

The previous Phase H script treated

- `phi = +pi/8`
- `phi = -pi/8`

as opposite-handed states by imposing a manual sign flip when `phi < 0`.

That is inconsistent with audited Phase G, where chirality is

`chi = det(J) = cos(2phi)`,

so parity preserves chirality. After the refresh:

- the parity partner at `phi = -pi/8` has the same chirality and the same energy as the right-handed base,
- the true left-handed comparison is the chiral-flip state `phi = pi/8 + pi/2 = 5pi/8`.

### 2.2 The old 2D slices violated the active domain protocol

The previous 2D slices only scanned `[-pi, pi]`.

The refreshed package now scans the full active domain:

- `theta, phi, rho in [-2pi, 2pi]`

for all 1D and 2D Phase H slice tables.

### 2.3 The old summary overstated the background derivation

Because Phase F no longer supports strong hosting-basin validation, the old statements

- "hosting basins established in Phase F,"
- "native quantum resonator,"
- and "rigorous geometric origin"

were too strong.

The refreshed package now describes the actual result as a provisional semiclassical proxy study.

---

## 3. Main findings

### 3.1 A sampled ground-state proxy mode exists, but a full ladder is not established

For the representative audited states:

- `Scalar Anchor`: `E0 = 0.9173867490363242`
- `Right-Handed Base`: `E0 = 0.9093699942084978`
- `Parity Partner`: `E0 = 0.9093699942084978`
- `Left-Handed Flip`: `E0 = 0.869622394058611`

Each representative state has:

- `mode_count = 1`
- only `n = 0` found within the fixed bracket

So the present package supports a sampled ground-state root, not a robust multi-level ladder claim.

### 3.2 Parity leaves the proxy spectrum unchanged; the true chiral flip splits it

The pair comparison table gives:

- parity pair energy gap: `0.0`
- chiral-flip pair energy gap: `0.039747600149886875`

That is the corrected handedness result:

- parity preserves the proxy spectrum,
- the true topological chiral flip changes the spectrum because the proxy couples directly to `chi`.

### 3.3 Loading sensitivity is real in the proxy model

The right-handed base loading scan gives:

- `loading = -0.1`: `E0 = 0.8755308759378563`
- `loading = 0.0`: `E0 = 0.9093699942084978`
- `loading = 0.1`: `E0 = 0.9420200171751509`

The total span is:

- `0.06648914123729466`

and the refreshed summary confirms this is monotone increasing across the sampled ladder.

### 3.4 The current proxy is phi-controlled

The slice widths are:

- `theta` width: `0.0`
- `phi` width: `0.05622564488235715`
- `rho` width: `0.0`
- `(phi, theta)` width: `0.05622564488235715`
- `(theta, rho)` width: `0.0`
- `(phi, rho)` width: `0.05622564488235715`

So the present proxy depends on `phi` alone through `chi = cos(2phi)`. Theta and rho are exact spectators in this runtime.

That is not an emergent discovery about full quantum structure. It is the direct consequence of how the current proxy potential is built.

---

## 4. Correct interpretation

The refreshed Phase H result is narrower than the old note claimed.

What survives:

- a draft semiclassical excitation ansatz exists,
- the current proxy admits a sampled ground-state root,
- the true chiral flip shifts that root,
- external loading shifts that root,
- and the full-domain slice protocol has now been satisfied.

What does not survive:

- the old claim that Phase F had already established the trapping basin used here,
- the old parity-based "left-handed" splitting claim,
- the old claim of a verified native Khantraction discrete spectrum,
- and the old claim that robustness under improved operators has already been demonstrated.

---

## 5. Bottom line

**Bottom line:** Phase H now supports a provisional semiclassical proxy result. The current Bohr-Sommerfeld ansatz admits a sampled `n = 0` root, parity leaves that proxy spectrum unchanged, the true chiral flip splits it, and loading shifts it monotonically. But this is still a hand-built resonator model, not a solver-backed quantum operator extracted from the refreshed classical Khantraction background, so strong native quantum-spectrum claims remain open.
