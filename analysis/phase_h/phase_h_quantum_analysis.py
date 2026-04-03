"""
Phase H: semiclassical excitation proxy audit

This script does not solve a full wave equation on a background extracted from
the refreshed Phase F and Phase G runtimes. Instead, it audits what the current
Phase H ansatz actually supports: a Bohr-Sommerfeld ground-state proxy on a
hand-built quartic well with chirality and loading shifts.
"""

from __future__ import annotations

import json
from pathlib import Path

import numpy as np
import pandas as pd
from scipy.integrate import quad
from scipy.optimize import root_scalar

ROOT = Path(__file__).resolve().parents[2]
OUT_DIR = ROOT / "solutions" / "phase_h" / "phase_h_quantum"

HOSTING_DEPTH_PROXY = 0.999
LAMBDA_CHI = 0.05
MU_EFF = 0.5
R_H_PROXY = 3.0
ENERGY_BRACKET = (0.01, 2.0)
LOADING_VALUES = np.linspace(-0.1, 0.1, 5)
ANGLES_1D = np.linspace(-2.0 * np.pi, 2.0 * np.pi, 17)
ANGLES_2D = np.linspace(-2.0 * np.pi, 2.0 * np.pi, 9)

REPRESENTATIVE_STATES = {
    "Scalar Anchor": (0.0, 0.0, 0.0),
    "Right-Handed Base": (0.0, np.pi / 8.0, 0.0),
    "Parity Partner": (0.0, -np.pi / 8.0, 0.0),
    "Left-Handed Flip": (0.0, 5.0 * np.pi / 8.0, 0.0),
}


class PhaseHQuantumProxy:
    def get_vielbeins(self, theta: float, phi: float, rho: float):
        del theta
        c2p, s2p = np.cos(2.0 * phi), np.sin(2.0 * phi)
        c2r, s2r = np.cos(2.0 * rho), np.sin(2.0 * rho)
        e_rho = np.array([0.0, 0.0, 1.0])
        e_phi = np.array([s2r, c2r, 0.0])
        e_theta = np.array([c2r * c2p, -s2r * c2p, s2p])
        return e_theta, e_phi, e_rho

    def get_chirality_density(self, theta: float, phi: float, rho: float) -> float:
        e_theta, e_phi, e_rho = self.get_vielbeins(theta, phi, rho)
        return float(np.linalg.det(np.stack((e_theta, e_phi, e_rho))))

    def effective_potential(self, r: float, chi: float, loading: float = 0.0) -> float:
        a = 0.5 * HOSTING_DEPTH_PROXY
        b = 0.25 * HOSTING_DEPTH_PROXY
        v_resonator = -a * r**2 + b * r**4
        v_chiral = LAMBDA_CHI * chi
        v_loading = loading * np.exp(-r**2 / 2.0)
        return float(v_resonator + v_chiral + v_loading)

    def quantization_integral(
        self,
        energy: float,
        chi: float,
        loading: float = 0.0,
        r_h: float = R_H_PROXY,
    ) -> float:
        def integrand(r: float) -> float:
            value = energy**2 - self.effective_potential(r, chi, loading)
            return float(np.sqrt(value)) if value > 0.0 else 0.0

        integral_value, _ = quad(integrand, 0.0, r_h, limit=200)
        return float(integral_value)

    def find_mode(self, target: float, chi: float, loading: float = 0.0):
        def objective(energy_value: float) -> float:
            return self.quantization_integral(energy_value, chi, loading) - target

        f_low = objective(ENERGY_BRACKET[0])
        f_high = objective(ENERGY_BRACKET[1])
        if not np.isfinite(f_low) or not np.isfinite(f_high) or f_low * f_high > 0.0:
            return None

        solution = root_scalar(objective, bracket=ENERGY_BRACKET, method="brentq")
        return float(solution.root) if solution.converged else None

    def find_eigenvalues(
        self,
        theta: float,
        phi: float,
        rho: float,
        loading: float = 0.0,
        max_n: int = 3,
    ):
        chi = self.get_chirality_density(theta, phi, rho)
        modes = []
        for n in range(max_n):
            target = (n + 0.5) * np.pi
            energy = self.find_mode(target, chi, loading)
            if energy is None:
                continue
            modes.append({"n": int(n), "energy": float(energy)})
        return modes

    def ground_state_energy(
        self,
        theta: float,
        phi: float,
        rho: float,
        loading: float = 0.0,
    ) -> float:
        modes = self.find_eigenvalues(theta, phi, rho, loading=loading, max_n=3)
        return float(modes[0]["energy"]) if modes else float("nan")


def write_csv(path: Path, rows: list[dict]):
    pd.DataFrame(rows).to_csv(path, index=False)


def make_representative_outputs(solver: PhaseHQuantumProxy):
    spectrum = {}
    rows = []

    for run_name, (theta, phi, rho) in REPRESENTATIVE_STATES.items():
        chi = solver.get_chirality_density(theta, phi, rho)
        modes = solver.find_eigenvalues(theta, phi, rho, max_n=3)
        spectrum[run_name] = {
            "theta": float(theta),
            "phi": float(phi),
            "rho": float(rho),
            "chirality": float(chi),
            "mode_count": len(modes),
            "modes": modes,
        }
        for mode in modes:
            rows.append(
                {
                    "run": run_name,
                    "theta": float(theta),
                    "phi": float(phi),
                    "rho": float(rho),
                    "chirality": float(chi),
                    "mode_count": len(modes),
                    "n": int(mode["n"]),
                    "energy": float(mode["energy"]),
                }
            )

    with (OUT_DIR / "excitation_spectrum.json").open("w", encoding="utf-8") as handle:
        json.dump(spectrum, handle, indent=2)
    write_csv(OUT_DIR / "representative_spectra.csv", rows)
    return spectrum, rows


def make_pair_comparisons(solver: PhaseHQuantumProxy, spectrum: dict):
    del solver
    pairs = [
        ("parity_pair", "Right-Handed Base", "Parity Partner", "parity_preserves_chi"),
        ("chiral_flip_pair", "Right-Handed Base", "Left-Handed Flip", "phi_shift_pi_over_2"),
        ("scalar_vs_right_handed", "Scalar Anchor", "Right-Handed Base", "scalar_vs_chiral"),
    ]
    rows = []
    for pair_name, run_a, run_b, relation in pairs:
        entry_a = spectrum[run_a]
        entry_b = spectrum[run_b]
        e0_a = entry_a["modes"][0]["energy"] if entry_a["modes"] else float("nan")
        e0_b = entry_b["modes"][0]["energy"] if entry_b["modes"] else float("nan")
        chi_a = entry_a["chirality"]
        chi_b = entry_b["chirality"]
        rows.append(
            {
                "pair": pair_name,
                "run_a": run_a,
                "run_b": run_b,
                "relation": relation,
                "chi_a": float(chi_a),
                "chi_b": float(chi_b),
                "same_chirality_sign": bool(np.sign(chi_a) == np.sign(chi_b)),
                "e0_a": float(e0_a),
                "e0_b": float(e0_b),
                "e0_abs_diff": float(abs(e0_a - e0_b)),
            }
        )
    write_csv(OUT_DIR / "pair_comparisons.csv", rows)
    return rows


def make_loading_scan(solver: PhaseHQuantumProxy):
    theta, phi, rho = REPRESENTATIVE_STATES["Right-Handed Base"]
    rows = []
    for loading in LOADING_VALUES:
        energy = solver.ground_state_energy(theta, phi, rho, loading=loading)
        rows.append(
            {
                "loading": float(loading),
                "chirality": float(solver.get_chirality_density(theta, phi, rho)),
                "E0": float(energy),
            }
        )
    write_csv(OUT_DIR / "loading_sensitivity.csv", rows)
    return rows


def sample_1d_slice(solver: PhaseHQuantumProxy, variable: str):
    rows = []
    for value in ANGLES_1D:
        theta, phi, rho = 0.0, np.pi / 8.0, 0.0
        if variable == "theta":
            theta = value
        elif variable == "phi":
            phi = value
        elif variable == "rho":
            rho = value
        else:
            raise ValueError(f"Unknown 1D slice variable: {variable}")

        rows.append(
            {
                variable: float(value),
                "chi": float(solver.get_chirality_density(theta, phi, rho)),
                "E0": float(solver.ground_state_energy(theta, phi, rho)),
            }
        )
    path = OUT_DIR / f"slice_1d_{variable}_energy.csv"
    write_csv(path, rows)
    return rows


def sample_2d_slice(solver: PhaseHQuantumProxy, variable_a: str, variable_b: str, fixed_name: str, fixed_value: float):
    rows = []
    for value_a in ANGLES_2D:
        for value_b in ANGLES_2D:
            state = {"theta": 0.0, "phi": 0.0, "rho": 0.0}
            state[fixed_name] = fixed_value
            state[variable_a] = value_a
            state[variable_b] = value_b
            theta = state["theta"]
            phi = state["phi"]
            rho = state["rho"]
            rows.append(
                {
                    variable_a: float(value_a),
                    variable_b: float(value_b),
                    "chi": float(solver.get_chirality_density(theta, phi, rho)),
                    "E0": float(solver.ground_state_energy(theta, phi, rho)),
                }
            )
    write_csv(OUT_DIR / f"slice_2d_{variable_a}_{variable_b}_energy.csv", rows)
    return rows


def finite_width(rows: list[dict], key: str) -> float:
    values = np.array([row[key] for row in rows], dtype=float)
    finite = values[np.isfinite(values)]
    if finite.size == 0:
        return float("nan")
    return float(finite.max() - finite.min())


def build_summary(pair_rows, loading_rows, theta_rows, phi_rows, rho_rows, phi_theta_rows, theta_rho_rows, phi_rho_rows):
    pair_lookup = {row["pair"]: row for row in pair_rows}
    loading_energies = np.array([row["E0"] for row in loading_rows], dtype=float)
    summary = {
        "phase": "H",
        "status": "audit_refresh",
        "model_scope": {
            "type": "semiclassical_proxy",
            "background_statement": (
                "Hand-built quartic well plus chirality and loading shifts; "
                "not a solved wave equation on an audited Phase F trapping background."
            ),
            "chirality_statement": "Chirality matches Phase G: chi = det(J) = cos(2phi).",
        },
        "config": {
            "hosting_depth_proxy": HOSTING_DEPTH_PROXY,
            "lambda_chi": LAMBDA_CHI,
            "mu_eff": MU_EFF,
            "r_h_proxy": R_H_PROXY,
            "energy_bracket": list(ENERGY_BRACKET),
            "angles_1d_points": int(len(ANGLES_1D)),
            "angles_2d_points_per_axis": int(len(ANGLES_2D)),
        },
        "key_results": {
            "parity_pair_e0_abs_diff": float(pair_lookup["parity_pair"]["e0_abs_diff"]),
            "chiral_flip_pair_e0_abs_diff": float(pair_lookup["chiral_flip_pair"]["e0_abs_diff"]),
            "loading_e0_span": float(loading_energies.max() - loading_energies.min()),
            "loading_monotone_increasing": bool(np.all(np.diff(loading_energies) > 0.0)),
            "theta_slice_width": finite_width(theta_rows, "E0"),
            "phi_slice_width": finite_width(phi_rows, "E0"),
            "rho_slice_width": finite_width(rho_rows, "E0"),
            "phi_theta_slice_width": finite_width(phi_theta_rows, "E0"),
            "theta_rho_slice_width": finite_width(theta_rho_rows, "E0"),
            "phi_rho_slice_width": finite_width(phi_rho_rows, "E0"),
            "theta_slice_valid_count": int(np.isfinite([row["E0"] for row in theta_rows]).sum()),
            "phi_slice_valid_count": int(np.isfinite([row["E0"] for row in phi_rows]).sum()),
            "rho_slice_valid_count": int(np.isfinite([row["E0"] for row in rho_rows]).sum()),
        },
    }
    with (OUT_DIR / "summary.json").open("w", encoding="utf-8") as handle:
        json.dump(summary, handle, indent=2)
    return summary


def write_solution_summary(spectrum: dict, pair_rows: list[dict], summary: dict):
    right = spectrum["Right-Handed Base"]
    parity = spectrum["Parity Partner"]
    left = spectrum["Left-Handed Flip"]
    scalar = spectrum["Scalar Anchor"]

    lines = [
        "# Phase H Semiclassical Proxy Summary",
        "",
        "**Date:** 2026-04-02",
        "**Phase:** H — Return to Stronger Quantum-Facing Work",
        "**Data Source:** `analysis/phase_h/phase_h_quantum_analysis.py`",
        "",
        "## Overview",
        "This folder contains the refreshed Phase H outputs after the audit correction.",
        "The package now records what the current Bohr-Sommerfeld proxy actually proves.",
        "It is a semiclassical resonator ansatz on a hand-built quartic well, not a full wave-equation solve on a background extracted from the refreshed Phase F and Phase G runtimes.",
        "",
        "## Representative spectra",
        f"- `Scalar Anchor`: chi = {scalar['chirality']}, mode_count = {scalar['mode_count']}, E0 = {scalar['modes'][0]['energy']}",
        f"- `Right-Handed Base`: chi = {right['chirality']}, mode_count = {right['mode_count']}, E0 = {right['modes'][0]['energy']}",
        f"- `Parity Partner`: chi = {parity['chirality']}, mode_count = {parity['mode_count']}, E0 = {parity['modes'][0]['energy']}",
        f"- `Left-Handed Flip`: chi = {left['chirality']}, mode_count = {left['mode_count']}, E0 = {left['modes'][0]['energy']}",
        "",
        "Only the ground-state proxy mode `n = 0` is found in the audited representative states within the fixed energy bracket.",
        "",
        "## Pair checks",
        f"- Parity pair energy difference: {pair_rows[0]['e0_abs_diff']}",
        f"- Chiral-flip pair energy difference: {pair_rows[1]['e0_abs_diff']}",
        "",
        "Interpretation: parity preserves the proxy spectrum, while the true topological chiral flip shifts the ground-state energy because the ansatz couples directly to `chi = cos(2phi)`.",
        "",
        "## Loading sensitivity",
        "- `loading_sensitivity.csv` sweeps the right-handed base state from `loading = -0.1` to `loading = 0.1`.",
        f"- The proxy ground state rises monotonically with loading, with total span {summary['key_results']['loading_e0_span']}.",
        "",
        "## Slice behavior",
        f"- Theta slice width: {summary['key_results']['theta_slice_width']}",
        f"- Phi slice width: {summary['key_results']['phi_slice_width']}",
        f"- Rho slice width: {summary['key_results']['rho_slice_width']}",
        f"- 2D phi/theta width: {summary['key_results']['phi_theta_slice_width']}",
        f"- 2D theta/rho width: {summary['key_results']['theta_rho_slice_width']}",
        f"- 2D phi/rho width: {summary['key_results']['phi_rho_slice_width']}",
        "",
        "Interpretation: the current proxy is phi-controlled. Theta and rho are exact spectators because the potential depends only on `chi(phi)` and the loading term.",
        "",
        "## Files",
        "- `excitation_spectrum.json`: representative spectra and chirality values.",
        "- `representative_spectra.csv`: flat table of the representative mode outputs.",
        "- `pair_comparisons.csv`: parity versus chiral-flip energy comparisons.",
        "- `loading_sensitivity.csv`: loading scan for the right-handed base state.",
        "- `slice_1d_theta_energy.csv`, `slice_1d_phi_energy.csv`, `slice_1d_rho_energy.csv`: full-domain 1D slices.",
        "- `slice_2d_phi_theta_energy.csv`, `slice_2d_theta_rho_energy.csv`, `slice_2d_phi_rho_energy.csv`: full-domain 2D slices.",
        "- `summary.json`: machine-readable audit summary.",
        "",
        "## Bottom line",
        "The refreshed Phase H package supports a provisional semiclassical claim: this proxy ansatz admits a ground-state root and that root is sensitive to chirality and loading. It does not, by itself, prove native Khantraction quantum mode ladders on a solver-backed hosted background.",
        "",
    ]
    (OUT_DIR / "summary.md").write_text("\n".join(lines), encoding="utf-8")


def run_quantum_analysis():
    print("--- Starting Phase H: Semiclassical Proxy Audit ---")
    OUT_DIR.mkdir(parents=True, exist_ok=True)
    solver = PhaseHQuantumProxy()

    spectrum, _ = make_representative_outputs(solver)
    pair_rows = make_pair_comparisons(solver, spectrum)
    loading_rows = make_loading_scan(solver)

    theta_rows = sample_1d_slice(solver, "theta")
    phi_rows = sample_1d_slice(solver, "phi")
    rho_rows = sample_1d_slice(solver, "rho")
    write_csv(OUT_DIR / "slice_1d_energy.csv", phi_rows)

    phi_theta_rows = sample_2d_slice(solver, "phi", "theta", "rho", 0.0)
    theta_rho_rows = sample_2d_slice(solver, "theta", "rho", "phi", np.pi / 8.0)
    phi_rho_rows = sample_2d_slice(solver, "phi", "rho", "theta", 0.0)

    summary = build_summary(
        pair_rows,
        loading_rows,
        theta_rows,
        phi_rows,
        rho_rows,
        phi_theta_rows,
        theta_rho_rows,
        phi_rho_rows,
    )
    write_solution_summary(spectrum, pair_rows, summary)
    print("Analysis Complete.")


if __name__ == "__main__":
    run_quantum_analysis()
