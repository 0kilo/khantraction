from __future__ import annotations

import json
from pathlib import Path

import numpy as np
import pandas as pd


ROOT = Path(__file__).resolve().parents[2]
OUTPUT_DIR = ROOT / "solutions" / "phase_l" / "phase_l_topological_shedding"


def simulate_emission(initial_params: dict[str, float], dt: float = 0.01, steps: int = 100):
    """
    Algebraic emission proxy used by the audited Phase L package.

    The active runtime does not solve a pinch-off PDE. It applies:

    - excitation energy proxy: 0.5 * (theta^2 + rho^2)
    - phi gate: 1 - 0.9 * |cos(2 phi)|
    - packet advection: Gaussian translated at fixed proxy speed
    """
    theta = float(initial_params["theta"])
    phi = float(initial_params["phi"])
    rho = float(initial_params["rho"])

    excitation_energy = 0.5 * (theta**2 + rho**2)
    phi_gate = 1.0 - 0.9 * abs(np.cos(2.0 * phi))
    e_flux = excitation_energy * phi_gate

    history = []
    for i in range(steps):
        t = i * dt
        pos = 1.0 + 2.0 * t
        amp = e_flux * np.exp(-0.5 * (pos - 2.0) ** 2)
        history.append({"t": t, "pos": pos, "amp": amp})

    return e_flux, pd.DataFrame(history)


def summarize_slice_width(df: pd.DataFrame) -> float:
    return float(df["e_flux"].max() - df["e_flux"].min())


def nearest_row(df: pd.DataFrame, column: str, target: float) -> dict[str, float]:
    idx = (df[column] - target).abs().idxmin()
    row = df.loc[idx]
    return {key: float(row[key]) for key in row.index}


def run_emission_suite() -> None:
    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)

    excited_state = {"w": 0.5, "theta": np.pi, "phi": -np.pi / 8.0, "rho": np.pi / 4.0}

    bulk_angles = np.linspace(-2.0 * np.pi, 2.0 * np.pi, 20)
    bulk_rows = []
    for phi in bulk_angles:
        for theta in bulk_angles:
            for rho in bulk_angles:
                params = {"w": 0.5, "theta": theta, "phi": phi, "rho": rho}
                e_flux, _ = simulate_emission(params, steps=1)
                bulk_rows.append({"theta": theta, "phi": phi, "rho": rho, "e_flux": e_flux})
    bulk_df = pd.DataFrame(bulk_rows)
    bulk_df.to_csv(OUTPUT_DIR / "bulk_emission_scan.csv", index=False)

    test_angles = np.linspace(-2.0 * np.pi, 2.0 * np.pi, 100)
    slice_1d_theta = []
    slice_1d_phi = []
    slice_1d_rho = []
    for angle in test_angles:
        params = dict(excited_state)
        params["theta"] = angle
        e_flux, _ = simulate_emission(params, steps=1)
        slice_1d_theta.append(
            {"theta": angle, "phi": excited_state["phi"], "rho": excited_state["rho"], "e_flux": e_flux}
        )

        params = dict(excited_state)
        params["phi"] = angle
        e_flux, _ = simulate_emission(params, steps=1)
        slice_1d_phi.append(
            {"theta": excited_state["theta"], "phi": angle, "rho": excited_state["rho"], "e_flux": e_flux}
        )

        params = dict(excited_state)
        params["rho"] = angle
        e_flux, _ = simulate_emission(params, steps=1)
        slice_1d_rho.append(
            {"theta": excited_state["theta"], "phi": excited_state["phi"], "rho": angle, "e_flux": e_flux}
        )

    theta_df = pd.DataFrame(slice_1d_theta)
    phi_df = pd.DataFrame(slice_1d_phi)
    rho_df = pd.DataFrame(slice_1d_rho)
    theta_df.to_csv(OUTPUT_DIR / "vary_theta_phi_fixed_rho_fixed.csv", index=False)
    phi_df.to_csv(OUTPUT_DIR / "vary_phi_theta_fixed_rho_fixed.csv", index=False)
    rho_df.to_csv(OUTPUT_DIR / "vary_rho_theta_fixed_phi_fixed.csv", index=False)

    res_2d = 30
    angles_2d = np.linspace(-2.0 * np.pi, 2.0 * np.pi, res_2d)
    slice_2d_theta_phi = []
    slice_2d_theta_rho = []
    slice_2d_phi_rho = []
    for angle_1 in angles_2d:
        for angle_2 in angles_2d:
            params = dict(excited_state)
            params["theta"] = angle_1
            params["phi"] = angle_2
            e_flux, _ = simulate_emission(params, steps=1)
            slice_2d_theta_phi.append(
                {"theta": angle_1, "phi": angle_2, "rho": excited_state["rho"], "e_flux": e_flux}
            )

            params = dict(excited_state)
            params["theta"] = angle_1
            params["rho"] = angle_2
            e_flux, _ = simulate_emission(params, steps=1)
            slice_2d_theta_rho.append(
                {"theta": angle_1, "phi": excited_state["phi"], "rho": angle_2, "e_flux": e_flux}
            )

            params = dict(excited_state)
            params["phi"] = angle_1
            params["rho"] = angle_2
            e_flux, _ = simulate_emission(params, steps=1)
            slice_2d_phi_rho.append(
                {"theta": excited_state["theta"], "phi": angle_1, "rho": angle_2, "e_flux": e_flux}
            )

    theta_phi_df = pd.DataFrame(slice_2d_theta_phi)
    theta_rho_df = pd.DataFrame(slice_2d_theta_rho)
    phi_rho_df = pd.DataFrame(slice_2d_phi_rho)
    theta_phi_df.to_csv(OUTPUT_DIR / "theta_phi_rho_fixed.csv", index=False)
    theta_rho_df.to_csv(OUTPUT_DIR / "theta_rho_phi_fixed.csv", index=False)
    phi_rho_df.to_csv(OUTPUT_DIR / "phi_rho_theta_fixed.csv", index=False)

    omega_rows = []
    for omega in np.linspace(0.1, 2.0, 8):
        params = dict(excited_state)
        params["w"] = float(omega)
        e_flux, _ = simulate_emission(params, steps=1)
        omega_rows.append({"w": omega, "theta": params["theta"], "phi": params["phi"], "rho": params["rho"], "e_flux": e_flux})
    omega_df = pd.DataFrame(omega_rows)
    omega_df.to_csv(OUTPUT_DIR / "omega_blindness_check.csv", index=False)

    representative_flux, packet_df = simulate_emission(excited_state, steps=100)
    packet_df.to_csv(OUTPUT_DIR / "sample_packet_trajectory.csv", index=False)

    bulk_max_row = bulk_df.loc[bulk_df["e_flux"].idxmax()]
    packet_peak_idx = packet_df["amp"].idxmax()
    packet_peak = packet_df.loc[packet_peak_idx]

    summary = {
        "status": "audited_proxy_refresh",
        "type": "algebraic_emission_proxy",
        "bulk_rows": int(len(bulk_df)),
        "slice_1d_rows": {
            "theta": int(len(theta_df)),
            "phi": int(len(phi_df)),
            "rho": int(len(rho_df)),
        },
        "slice_2d_rows": {
            "theta_phi": int(len(theta_phi_df)),
            "theta_rho": int(len(theta_rho_df)),
            "phi_rho": int(len(phi_rho_df)),
        },
        "representative_state": {key: float(value) for key, value in excited_state.items()},
        "representative_flux": float(representative_flux),
        "bulk_max_emission_flux": float(bulk_max_row["e_flux"]),
        "bulk_max_state": {
            "theta": float(bulk_max_row["theta"]),
            "phi": float(bulk_max_row["phi"]),
            "rho": float(bulk_max_row["rho"]),
        },
        "slice_widths": {
            "theta": summarize_slice_width(theta_df),
            "phi": summarize_slice_width(phi_df),
            "rho": summarize_slice_width(rho_df),
        },
        "phi_reference_points": {
            "near_zero": nearest_row(phi_df, "phi", 0.0),
            "near_pos_pi_over_4": nearest_row(phi_df, "phi", np.pi / 4.0),
            "near_neg_pi_over_4": nearest_row(phi_df, "phi", -np.pi / 4.0),
            "near_pi_over_2": nearest_row(phi_df, "phi", np.pi / 2.0),
        },
        "omega_flux_span": float(omega_df["e_flux"].max() - omega_df["e_flux"].min()),
        "packet_speed_proxy": 2.0,
        "packet_peak": {
            "t": float(packet_peak["t"]),
            "pos": float(packet_peak["pos"]),
            "amp": float(packet_peak["amp"]),
        },
        "packet_terminal_state": {
            "t": float(packet_df["t"].iloc[-1]),
            "pos": float(packet_df["pos"].iloc[-1]),
            "amp": float(packet_df["amp"].iloc[-1]),
        },
        "discrete_step_mapping": "not_implemented",
        "phase_h_dependency": "no_direct_phase_h_mode_solver_connection",
        "conclusion": (
            "The active Phase L package supports a phi-gated algebraic emission proxy and a hand-built "
            "advected packet trajectory. It does not directly implement a dynamical pinch-off or a "
            "discrete Phase H ladder transition."
        ),
    }
    with (OUTPUT_DIR / "summary.json").open("w", encoding="utf-8") as handle:
        json.dump(summary, handle, indent=2)

    print(f"Phase L emission proxy refresh complete. Results in {OUTPUT_DIR}")


if __name__ == "__main__":
    run_emission_suite()
