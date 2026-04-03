# Phase H Semiclassical Proxy Summary

**Date:** 2026-04-02
**Phase:** H — Return to Stronger Quantum-Facing Work
**Data Source:** `analysis/phase_h/phase_h_quantum_analysis.py`

## Overview
This folder contains the refreshed Phase H outputs after the audit correction.
The package now records what the current Bohr-Sommerfeld proxy actually proves.
It is a semiclassical resonator ansatz on a hand-built quartic well, not a full wave-equation solve on a background extracted from the refreshed Phase F and Phase G runtimes.

## Representative spectra
- `Scalar Anchor`: chi = 1.0, mode_count = 1, E0 = 0.9173867490363242
- `Right-Handed Base`: chi = 0.7071067811865476, mode_count = 1, E0 = 0.9093699942084978
- `Parity Partner`: chi = 0.7071067811865476, mode_count = 1, E0 = 0.9093699942084978
- `Left-Handed Flip`: chi = -0.7071067811865477, mode_count = 1, E0 = 0.869622394058611

Only the ground-state proxy mode `n = 0` is found in the audited representative states within the fixed energy bracket.

## Pair checks
- Parity pair energy difference: 0.0
- Chiral-flip pair energy difference: 0.039747600149886875

Interpretation: parity preserves the proxy spectrum, while the true topological chiral flip shifts the ground-state energy because the ansatz couples directly to `chi = cos(2phi)`.

## Loading sensitivity
- `loading_sensitivity.csv` sweeps the right-handed base state from `loading = -0.1` to `loading = 0.1`.
- The proxy ground state rises monotonically with loading, with total span 0.06648914123729466.

## Slice behavior
- Theta slice width: 0.0
- Phi slice width: 0.05622564488235715
- Rho slice width: 0.0
- 2D phi/theta width: 0.05622564488235715
- 2D theta/rho width: 0.0
- 2D phi/rho width: 0.05622564488235715

Interpretation: the current proxy is phi-controlled. Theta and rho are exact spectators because the potential depends only on `chi(phi)` and the loading term.

## Files
- `excitation_spectrum.json`: representative spectra and chirality values.
- `representative_spectra.csv`: flat table of the representative mode outputs.
- `pair_comparisons.csv`: parity versus chiral-flip energy comparisons.
- `loading_sensitivity.csv`: loading scan for the right-handed base state.
- `slice_1d_theta_energy.csv`, `slice_1d_phi_energy.csv`, `slice_1d_rho_energy.csv`: full-domain 1D slices.
- `slice_2d_phi_theta_energy.csv`, `slice_2d_theta_rho_energy.csv`, `slice_2d_phi_rho_energy.csv`: full-domain 2D slices.
- `summary.json`: machine-readable audit summary.

## Bottom line
The refreshed Phase H package supports a provisional semiclassical claim: this proxy ansatz admits a ground-state root and that root is sensitive to chirality and loading. It does not, by itself, prove native Khantraction quantum mode ladders on a solver-backed hosted background.
