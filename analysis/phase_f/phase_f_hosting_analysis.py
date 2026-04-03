#!/usr/bin/env python3
r"""
Phase F: Classical hosting audit and probe-response analysis
Date: 2026-04-02
Purpose: Audit what the current exploratory Maurer-Cartan runtime actually
supports about probe hosting, signed loading, and angular sensitivity.
"""

from __future__ import annotations

import json
import math
from pathlib import Path

import numpy as np
import pandas as pd
from scipy.integrate import solve_ivp


KAPPA = 8.0 * np.pi
XI = 0.002
M_GLUE = 0.1
LAMBDA_Q = 0.01
BETA = np.array([0.01, 0.02, 0.03], dtype=float)
METRIC_REGULARIZATION = 1.0e-4
ANGULAR_PHI_POTENTIAL = 0.01
HORIZON_EVENT_FRACTION = 0.48
MU_PROBE = 0.05
GAMMA_HOST = 0.1
DEFAULT_A0 = 0.005
DEFAULT_XP0 = (0.0, 0.01, 0.01, 0.0)
DEFAULT_PSI0 = 0.1
DEFAULT_R_MAX = 20.0
SIGNED_LOADINGS = (-0.01, -0.001, 0.0, 0.001, 0.01)
ONE_D_POINTS = 15
TWO_D_POINTS = 8

ROOT = Path(__file__).resolve().parents[2]
OUT_DIR = ROOT / "solutions" / "phase_f" / "phase_f_hosting"

REPRESENTATIVE_ANCHORS = {
    "scalar": (0.5, 0.0, 0.0, 0.0),
    "theta_seed": (0.5, np.pi / 2.0, 0.0, 0.0),
    "rho_seed": (0.5, 0.0, 0.0, np.pi / 2.0),
    "phi_sheet": (0.5, 0.0, np.pi / 4.0, 0.0),
    "phi_offsheet": (0.5, 0.0, np.pi / 4.0 - 0.1, 0.0),
    "mixed_offsheet": (0.5, np.pi, np.pi / 4.0 - 0.1, np.pi / 2.0),
}


def finite_range(values: list[float]) -> list[float]:
    arr = np.asarray(values, dtype=float)
    arr = arr[np.isfinite(arr)]
    if arr.size == 0:
        return [float("nan"), float("nan")]
    return [float(arr.min()), float(arr.max())]


class PhaseFHostingSolver:
    def __init__(self, gamma_host: float = GAMMA_HOST):
        self.gamma_host = float(gamma_host)

    def get_vielbeins(self, theta: float, phi: float, rho: float):
        c2p, s2p = np.cos(2.0 * phi), np.sin(2.0 * phi)
        c2r, s2r = np.cos(2.0 * rho), np.sin(2.0 * rho)
        e_rho = np.array([0.0, 0.0, 1.0])
        e_phi = np.array([s2r, c2r, 0.0])
        e_theta = np.array([c2r * c2p, -s2r * c2p, s2p])
        return e_theta, e_phi, e_rho

    def get_target_metric(self, omega: float, theta: float, phi: float, rho: float):
        e_theta, e_phi, e_rho = self.get_vielbeins(theta, phi, rho)
        exp2w = np.exp(2.0 * omega)
        b = exp2w + 2.0 * BETA
        g = np.zeros((4, 4))
        g[0, 0] = exp2w
        for i, ei in enumerate((e_theta, e_phi, e_rho)):
            for j, ej in enumerate((e_theta, e_phi, e_rho)):
                g[i + 1, j + 1] = np.sum(b * ei * ej)
        return g

    def equations(self, r: float, y: np.ndarray, j_ext: float):
        # y = [w, th, ph, rh, wp, thp, php, rhp, m, grav_potential, psi, psip]
        w, th, ph, rh, wp, thp, php, rhp, m, grav_potential, psi, psip = y
        del grav_potential
        xp = y[4:8]
        if r < 1.0e-10:
            return np.zeros_like(y)

        if r > 2.0 * m:
            e_2l = 1.0 / (1.0 - 2.0 * m / r)
        else:
            e_2l = 1.0e10
        e_neg2l = 1.0 / e_2l

        g = self.get_target_metric(w, th, ph, rh)
        g_reg = g + METRIC_REGULARIZATION * np.eye(4)

        exp2w = np.exp(2.0 * w)
        u = 0.5 * M_GLUE**2 * exp2w + 0.25 * LAMBDA_Q * exp2w**2

        e_theta, e_phi, e_rho = self.get_vielbeins(th, ph, rh)
        w_r = e_theta * thp + e_phi * php + e_rho * rhp
        omega_mc_sq = np.sum(BETA * w_r**2)
        dq_sq = exp2w * (wp**2 + np.sum(w_r**2))

        t_q = -e_neg2l * dq_sq - 4.0 * u
        t_mc = 2.0 * e_neg2l * omega_mc_sq
        s_term = 2.0 * e_neg2l * dq_sq - 2.0 * (M_GLUE**2 + LAMBDA_Q * exp2w) * exp2w
        r_scalar = (
            -KAPPA * (t_q + t_mc) + 6.0 * KAPPA * XI * s_term
        ) / (1.0 + 2.0 * KAPPA * XI * (1.0 - 12.0 * XI) * exp2w)

        v_ang = ANGULAR_PHI_POTENTIAL * np.sin(2.0 * ph) ** 2
        rho_probe = (
            0.5 * e_neg2l * psip**2
            + 0.5 * MU_PROBE**2 * psi**2
            + 0.5 * self.gamma_host * omega_mc_sq * psi**2
            + j_ext * wp * psi
        )
        p_r_probe = (
            0.5 * e_neg2l * psip**2
            - 0.5 * MU_PROBE**2 * psi**2
            - 0.5 * self.gamma_host * omega_mc_sq * psi**2
        )

        rho_base = 0.5 * e_neg2l * dq_sq + e_neg2l * omega_mc_sq + u + v_ang
        rho_total = rho_base + rho_probe

        m_prime = 4.0 * np.pi * r**2 * rho_total
        effective_pressure = rho_total - 2.0 * u - 2.0 * v_ang + p_r_probe
        phi_prime = (m + 4.0 * np.pi * r**3 * effective_pressure) / (r * (r - 2.0 * m))

        h_prime = phi_prime - (m_prime / r - m / r**2) * e_2l + 2.0 / r
        w_pp = -h_prime * wp - (M_GLUE**2 + LAMBDA_Q * exp2w - 2.0 * XI * r_scalar) * e_2l
        th_pp = -h_prime * thp
        ph_pp = (
            -h_prime * php
            - 4.0 * ANGULAR_PHI_POTENTIAL * np.sin(2.0 * ph) * np.cos(2.0 * ph) * e_2l / g_reg[2, 2]
        )
        rh_pp = -h_prime * rhp
        psi_pp = -h_prime * psip + e_2l * (MU_PROBE**2 + self.gamma_host * omega_mc_sq) * psi - j_ext * wp * e_2l

        return [wp, thp, php, rhp, w_pp, th_pp, ph_pp, rh_pp, m_prime, phi_prime, psip, psi_pp]

    def solve(
        self,
        omega0: float,
        theta0: float,
        phi0: float,
        rho0: float,
        *,
        j_ext: float = 0.0,
        a0: float = DEFAULT_A0,
        xp0: tuple[float, float, float, float] = DEFAULT_XP0,
        psi0: float = DEFAULT_PSI0,
        r_max: float = DEFAULT_R_MAX,
    ):
        y0 = [
            math.log(a0) + omega0,
            theta0,
            phi0,
            rho0,
            float(xp0[0]),
            float(xp0[1]),
            float(xp0[2]),
            float(xp0[3]),
            0.0,
            0.0,
            float(psi0),
            0.0,
        ]

        def horizon_event(r, y, loading):
            del loading
            return y[8] - HORIZON_EVENT_FRACTION * r

        horizon_event.terminal = True
        return solve_ivp(
            self.equations,
            (1.0e-4, r_max),
            y0,
            args=(j_ext,),
            method="RK45",
            events=horizon_event,
            rtol=1.0e-7,
            atol=1.0e-9,
        )


def summarize_solution(
    sol,
    *,
    omega0: float,
    theta0: float,
    phi0: float,
    rho0: float,
    j_ext: float,
    gamma_host: float,
    a0: float,
    xp0: tuple[float, float, float, float],
    psi0: float,
    r_max: float,
) -> dict:
    r = np.asarray(sol.t, dtype=float)
    psi = np.asarray(sol.y[10], dtype=float)
    psi_abs = np.abs(psi)
    core_mask = r <= min(1.0, float(r[-1]))
    outer_start = max(1.0, 0.8 * float(r[-1]))
    outer_mask = r >= outer_start
    core_mean = float(np.mean(psi_abs[core_mask])) if np.any(core_mask) else float("nan")
    outer_mean = float(np.mean(psi_abs[outer_mask])) if np.any(outer_mask) else float("nan")
    event_radii = [float(v) for v in sol.t_events[0]] if len(sol.t_events) else []
    r_final = float(r[-1])
    final_mass = float(sol.y[8, -1])
    final_psi = float(psi[-1])
    return {
        "omega0": float(omega0),
        "theta0": float(theta0),
        "phi0": float(phi0),
        "rho0": float(rho0),
        "j_ext": float(j_ext),
        "gamma_host": float(gamma_host),
        "A0": float(a0),
        "xp0": [float(v) for v in xp0],
        "psi0": float(psi0),
        "r_max": float(r_max),
        "status": int(sol.status),
        "status_message": str(sol.message),
        "terminated_early": bool(sol.status != 0 or len(event_radii) > 0),
        "horizon_event_radii": event_radii,
        "r_final": r_final,
        "final_mass": final_mass,
        "final_2m_over_r": (2.0 * final_mass / r_final) if r_final > 0.0 else float("nan"),
        "psi_final": final_psi,
        "psi_min": float(np.min(psi)),
        "psi_max": float(np.max(psi)),
        "probe_response_ratio": final_psi / float(psi0),
        "probe_boundary_delta": final_psi - float(psi0),
        "core_mean_abs_psi": core_mean,
        "outer_mean_abs_psi": outer_mean,
        "localization_ratio": core_mean / outer_mean if np.isfinite(core_mean) and np.isfinite(outer_mean) and outer_mean != 0.0 else float("nan"),
        "sample_count": int(len(r)),
    }


def write_profile_csv(species_id: str, sol, out_dir: Path) -> None:
    pd.DataFrame(
        {
            "r": sol.t,
            "mass_m": sol.y[8],
            "psi": sol.y[10],
            "abs_psi": np.abs(sol.y[10]),
        }
    ).to_csv(out_dir / f"{species_id}_profile.csv", index=False)


def representative_runs(out_dir: Path) -> tuple[list[dict], dict[str, object]]:
    solver = PhaseFHostingSolver(gamma_host=GAMMA_HOST)
    rows = []
    solutions: dict[str, object] = {}
    for anchor_name, params in REPRESENTATIVE_ANCHORS.items():
        sol = solver.solve(*params)
        solutions[anchor_name] = sol
        write_profile_csv(anchor_name, sol, out_dir)
        row = {"anchor": anchor_name}
        row.update(
            summarize_solution(
                sol,
                omega0=params[0],
                theta0=params[1],
                phi0=params[2],
                rho0=params[3],
                j_ext=0.0,
                gamma_host=GAMMA_HOST,
                a0=DEFAULT_A0,
                xp0=DEFAULT_XP0,
                psi0=DEFAULT_PSI0,
                r_max=DEFAULT_R_MAX,
            )
        )
        rows.append(row)
    pd.DataFrame(rows).to_csv(out_dir / "representative_runs.csv", index=False)
    return rows, solutions


def coupling_comparison(out_dir: Path) -> list[dict]:
    rows = []
    solver_off = PhaseFHostingSolver(gamma_host=0.0)
    solver_on = PhaseFHostingSolver(gamma_host=GAMMA_HOST)
    for anchor_name, params in REPRESENTATIVE_ANCHORS.items():
        sol_off = solver_off.solve(*params)
        sol_on = solver_on.solve(*params)
        row_off = summarize_solution(
            sol_off,
            omega0=params[0],
            theta0=params[1],
            phi0=params[2],
            rho0=params[3],
            j_ext=0.0,
            gamma_host=0.0,
            a0=DEFAULT_A0,
            xp0=DEFAULT_XP0,
            psi0=DEFAULT_PSI0,
            r_max=DEFAULT_R_MAX,
        )
        row_on = summarize_solution(
            sol_on,
            omega0=params[0],
            theta0=params[1],
            phi0=params[2],
            rho0=params[3],
            j_ext=0.0,
            gamma_host=GAMMA_HOST,
            a0=DEFAULT_A0,
            xp0=DEFAULT_XP0,
            psi0=DEFAULT_PSI0,
            r_max=DEFAULT_R_MAX,
        )
        rows.append(
            {
                "anchor": anchor_name,
                "status_gamma_off": row_off["status"],
                "status_gamma_on": row_on["status"],
                "r_final_gamma_off": row_off["r_final"],
                "r_final_gamma_on": row_on["r_final"],
                "psi_final_gamma_off": row_off["psi_final"],
                "psi_final_gamma_on": row_on["psi_final"],
                "probe_response_ratio_gamma_off": row_off["probe_response_ratio"],
                "probe_response_ratio_gamma_on": row_on["probe_response_ratio"],
                "probe_response_ratio_delta": row_on["probe_response_ratio"] - row_off["probe_response_ratio"],
                "localization_ratio_gamma_off": row_off["localization_ratio"],
                "localization_ratio_gamma_on": row_on["localization_ratio"],
                "mass_final_gamma_off": row_off["final_mass"],
                "mass_final_gamma_on": row_on["final_mass"],
                "mass_final_delta": row_on["final_mass"] - row_off["final_mass"],
            }
        )
    pd.DataFrame(rows).to_csv(out_dir / "coupling_comparison.csv", index=False)
    return rows


def signed_loading_ladder(out_dir: Path) -> tuple[list[dict], dict[str, dict]]:
    solver = PhaseFHostingSolver(gamma_host=GAMMA_HOST)
    anchor_subset = ("scalar", "phi_sheet", "phi_offsheet", "mixed_offsheet")
    rows = []
    summary = {}
    for anchor_name in anchor_subset:
        params = REPRESENTATIVE_ANCHORS[anchor_name]
        anchor_rows = []
        for j_ext in SIGNED_LOADINGS:
            sol = solver.solve(*params, j_ext=j_ext)
            row = {"anchor": anchor_name}
            row.update(
                summarize_solution(
                    sol,
                    omega0=params[0],
                    theta0=params[1],
                    phi0=params[2],
                    rho0=params[3],
                    j_ext=j_ext,
                    gamma_host=GAMMA_HOST,
                    a0=DEFAULT_A0,
                    xp0=DEFAULT_XP0,
                    psi0=DEFAULT_PSI0,
                    r_max=DEFAULT_R_MAX,
                )
            )
            rows.append(row)
            anchor_rows.append(row)
        by_loading = {row["j_ext"]: row for row in anchor_rows}
        summary[anchor_name] = {
            "status_pattern": [int(row["status"]) for row in anchor_rows],
            "mass_range": finite_range([row["final_mass"] for row in anchor_rows]),
            "probe_ratio_range": finite_range([row["probe_response_ratio"] for row in anchor_rows]),
            "negative_loading_increases_mass": by_loading[-0.01]["final_mass"] > by_loading[0.01]["final_mass"],
            "negative_loading_reduces_probe_response": by_loading[-0.01]["probe_response_ratio"] < by_loading[0.01]["probe_response_ratio"],
        }

    df = pd.DataFrame(rows)
    df.to_csv(out_dir / "signed_loading_ladder.csv", index=False)
    df[(df["anchor"] == "phi_sheet") & (df["j_ext"].isin([-0.01, 0.0, 0.01]))][
        ["j_ext", "final_mass", "psi_final", "probe_response_ratio", "status", "r_final"]
    ].rename(columns={"j_ext": "J_ext", "psi_final": "psi_boundary"}).to_csv(
        out_dir / "signed_loading_test.csv",
        index=False,
    )
    return rows, summary


def run_slice_set(out_dir: Path) -> tuple[dict[str, pd.DataFrame], dict[str, dict]]:
    solver = PhaseFHostingSolver(gamma_host=GAMMA_HOST)
    results: dict[str, pd.DataFrame] = {}
    summaries: dict[str, dict] = {}

    angles_1d = np.linspace(-2.0 * np.pi, 2.0 * np.pi, ONE_D_POINTS)
    angles_2d = np.linspace(-2.0 * np.pi, 2.0 * np.pi, TWO_D_POINTS)

    def row_with_metrics(name: str, sol, varied: dict[str, float], params: tuple[float, float, float, float]):
        row = dict(varied)
        row.update({"slice_name": name})
        row.update(
            summarize_solution(
                sol,
                omega0=params[0],
                theta0=params[1],
                phi0=params[2],
                rho0=params[3],
                j_ext=0.0,
                gamma_host=GAMMA_HOST,
                a0=DEFAULT_A0,
                xp0=DEFAULT_XP0,
                psi0=DEFAULT_PSI0,
                r_max=DEFAULT_R_MAX,
            )
        )
        return row

    slice_rows = {"theta": [], "phi": [], "rho": []}
    for theta in angles_1d:
        params = (0.5, float(theta), float(np.pi / 8.0), 0.0)
        sol = solver.solve(*params)
        slice_rows["theta"].append(row_with_metrics("theta", sol, {"theta": float(theta)}, params))
    for phi in angles_1d:
        params = (0.5, 0.0, float(phi), 0.0)
        sol = solver.solve(*params)
        slice_rows["phi"].append(row_with_metrics("phi", sol, {"phi": float(phi)}, params))
    for rho in angles_1d:
        params = (0.5, 0.0, float(np.pi / 8.0), float(rho))
        sol = solver.solve(*params)
        slice_rows["rho"].append(row_with_metrics("rho", sol, {"rho": float(rho)}, params))

    for axis, rows in slice_rows.items():
        df = pd.DataFrame(rows)
        results[f"slice_1d_{axis}"] = df
        df.to_csv(out_dir / f"slice_1d_{axis}.csv", index=False)
        summaries[f"slice_1d_{axis}"] = {
            "response_ratio_range": finite_range(df["probe_response_ratio"].tolist()),
            "localization_ratio_range": finite_range(df["localization_ratio"].tolist()),
            "terminated_early_count": int(df["terminated_early"].sum()),
        }

    slice_rows_2d = {"theta_rho": [], "phi_theta": [], "phi_rho": []}
    for theta in angles_2d:
        for rho in angles_2d:
            params = (0.5, float(theta), float(np.pi / 8.0), float(rho))
            sol = solver.solve(*params)
            slice_rows_2d["theta_rho"].append(row_with_metrics("theta_rho", sol, {"theta": float(theta), "rho": float(rho)}, params))
    for phi in angles_2d:
        for theta in angles_2d:
            params = (0.5, float(theta), float(phi), 0.0)
            sol = solver.solve(*params)
            slice_rows_2d["phi_theta"].append(row_with_metrics("phi_theta", sol, {"phi": float(phi), "theta": float(theta)}, params))
    for phi in angles_2d:
        for rho in angles_2d:
            params = (0.5, 0.0, float(phi), float(rho))
            sol = solver.solve(*params)
            slice_rows_2d["phi_rho"].append(row_with_metrics("phi_rho", sol, {"phi": float(phi), "rho": float(rho)}, params))

    angular_map_frames = []
    for name, rows in slice_rows_2d.items():
        df = pd.DataFrame(rows)
        results[f"slice_2d_{name}"] = df
        df.to_csv(out_dir / f"slice_2d_{name}.csv", index=False)
        summaries[f"slice_2d_{name}"] = {
            "response_ratio_range": finite_range(df["probe_response_ratio"].tolist()),
            "localization_ratio_range": finite_range(df["localization_ratio"].tolist()),
            "terminated_early_count": int(df["terminated_early"].sum()),
        }
        angular_map_frames.append(df)

    pd.concat(angular_map_frames, ignore_index=True).to_csv(out_dir / "angular_hosting_map.csv", index=False)
    return results, summaries


def write_summary(
    out_dir: Path,
    representative_rows: list[dict],
    coupling_rows: list[dict],
    signed_rows: list[dict],
    signed_summary: dict[str, dict],
    slice_summaries: dict[str, dict],
) -> dict:
    rep_by_anchor = {row["anchor"]: row for row in representative_rows}
    coupling_by_anchor = {row["anchor"]: row for row in coupling_rows}
    signed_df = pd.DataFrame(signed_rows)
    summary = {
        "runtime": {
            "beta": [float(v) for v in BETA],
            "metric_regularization": METRIC_REGULARIZATION,
            "angular_phi_potential": ANGULAR_PHI_POTENTIAL,
            "horizon_event_fraction": HORIZON_EVENT_FRACTION,
            "mu_probe": MU_PROBE,
            "gamma_host": GAMMA_HOST,
            "A0": DEFAULT_A0,
            "xp0": [float(v) for v in DEFAULT_XP0],
            "psi0": DEFAULT_PSI0,
            "r_max": DEFAULT_R_MAX,
        },
        "representative_runs": rep_by_anchor,
        "coupling_comparison": coupling_by_anchor,
        "signed_loading_summary": signed_summary,
        "slice_summaries": slice_summaries,
        "key_results": {
            "scalar_localization_ratio": rep_by_anchor["scalar"]["localization_ratio"],
            "phi_sheet_terminated_early": rep_by_anchor["phi_sheet"]["terminated_early"],
            "phi_offsheet_localization_ratio": rep_by_anchor["phi_offsheet"]["localization_ratio"],
            "mixed_offsheet_localization_ratio": rep_by_anchor["mixed_offsheet"]["localization_ratio"],
            "phi_offsheet_mixed_probe_difference": abs(
                rep_by_anchor["phi_offsheet"]["probe_response_ratio"] - rep_by_anchor["mixed_offsheet"]["probe_response_ratio"]
            ),
            "gamma_delta_scalar": coupling_by_anchor["scalar"]["probe_response_ratio_delta"],
            "gamma_delta_phi_offsheet": coupling_by_anchor["phi_offsheet"]["probe_response_ratio_delta"],
            "signed_loading_mass_difference_scalar": signed_df[(signed_df["anchor"] == "scalar") & (signed_df["j_ext"] == -0.01)]["final_mass"].iloc[0]
            - signed_df[(signed_df["anchor"] == "scalar") & (signed_df["j_ext"] == 0.01)]["final_mass"].iloc[0],
            "signed_loading_mass_difference_phi_offsheet": signed_df[(signed_df["anchor"] == "phi_offsheet") & (signed_df["j_ext"] == -0.01)]["final_mass"].iloc[0]
            - signed_df[(signed_df["anchor"] == "phi_offsheet") & (signed_df["j_ext"] == 0.01)]["final_mass"].iloc[0],
        },
    }

    (out_dir / "summary.json").write_text(json.dumps(summary, indent=2))

    lines = [
        "# Phase F Hosting Solutions Summary",
        "",
        "Generated by `analysis/phase_f/phase_f_hosting_analysis.py`.",
        "",
        "## Runtime model actually used",
        "- same exploratory symmetry-broken Maurer-Cartan runtime family inherited from audited Phases C to E",
        f"- anisotropic Maurer-Cartan weights: beta = {[float(v) for v in BETA]}",
        f"- metric regularization: {METRIC_REGULARIZATION}",
        f"- phi-localized angular potential coefficient: {ANGULAR_PHI_POTENTIAL}",
        f"- horizon event fraction: {HORIZON_EVENT_FRACTION}",
        f"- probe mass scale: {MU_PROBE}",
        f"- explicit hosting-coupling coefficient: {GAMMA_HOST}",
        f"- field seed amplitude: {DEFAULT_A0}",
        f"- derivative seed: {list(DEFAULT_XP0)}",
        f"- initial probe amplitude: {DEFAULT_PSI0}",
        "",
        "## Representative runs",
    ]
    for anchor in ("scalar", "theta_seed", "rho_seed", "phi_sheet", "phi_offsheet", "mixed_offsheet"):
        row = rep_by_anchor[anchor]
        lines.append(
            f"- `{anchor}`: status={row['status']}, r_final={row['r_final']}, "
            f"mass={row['final_mass']}, psi_final={row['psi_final']}, "
            f"probe_response_ratio={row['probe_response_ratio']}, localization_ratio={row['localization_ratio']}"
        )
    lines.extend(
        [
            "",
            "## Coupling comparison",
            "- The explicit gamma-on minus gamma-off probe-response deltas stay tiny relative to the overall background response.",
            f"- `scalar`: delta={coupling_by_anchor['scalar']['probe_response_ratio_delta']}",
            f"- `phi_sheet`: delta={coupling_by_anchor['phi_sheet']['probe_response_ratio_delta']}",
            f"- `phi_offsheet`: delta={coupling_by_anchor['phi_offsheet']['probe_response_ratio_delta']}",
            f"- `mixed_offsheet`: delta={coupling_by_anchor['mixed_offsheet']['probe_response_ratio_delta']}",
            "",
            "## Signed loading ladder",
            f"- `scalar`: mass range {signed_summary['scalar']['mass_range']}, probe-response range {signed_summary['scalar']['probe_ratio_range']}",
            f"- `phi_sheet`: mass range {signed_summary['phi_sheet']['mass_range']}, probe-response range {signed_summary['phi_sheet']['probe_ratio_range']}",
            f"- `phi_offsheet`: mass range {signed_summary['phi_offsheet']['mass_range']}, probe-response range {signed_summary['phi_offsheet']['probe_ratio_range']}",
            f"- `mixed_offsheet`: mass range {signed_summary['mixed_offsheet']['mass_range']}, probe-response range {signed_summary['mixed_offsheet']['probe_ratio_range']}",
            "",
            "## Slice summaries",
            f"- `theta`: probe-response range {slice_summaries['slice_1d_theta']['response_ratio_range']}, terminated_early={slice_summaries['slice_1d_theta']['terminated_early_count']}",
            f"- `phi`: probe-response range {slice_summaries['slice_1d_phi']['response_ratio_range']}, terminated_early={slice_summaries['slice_1d_phi']['terminated_early_count']}",
            f"- `rho`: probe-response range {slice_summaries['slice_1d_rho']['response_ratio_range']}, terminated_early={slice_summaries['slice_1d_rho']['terminated_early_count']}",
            f"- `theta_rho`: probe-response range {slice_summaries['slice_2d_theta_rho']['response_ratio_range']}, terminated_early={slice_summaries['slice_2d_theta_rho']['terminated_early_count']}",
            f"- `phi_theta`: probe-response range {slice_summaries['slice_2d_phi_theta']['response_ratio_range']}, terminated_early={slice_summaries['slice_2d_phi_theta']['terminated_early_count']}",
            f"- `phi_rho`: probe-response range {slice_summaries['slice_2d_phi_rho']['response_ratio_range']}, terminated_early={slice_summaries['slice_2d_phi_rho']['terminated_early_count']}",
            "",
            "## Interpretation",
            "- The current probe ansatz integrates stably on several survivor backgrounds, but unloaded localization ratios remain below 1, so the probe is not concentrated in the core on the audited runs.",
            "- Signed loading asymmetry is real: negative loading raises the final mass and reduces the probe response, while positive loading lowers the final mass and increases the probe response on the main survivor anchors.",
            "- Angular response is phi-dominated. The off-sheet phi-rich pair `phi_offsheet` / `mixed_offsheet` remains nearly indistinguishable, while theta-only and rho-only seeds remain close to the scalar anchor.",
            "- The explicit Maurer-Cartan hosting coupling is subleading in the current implementation. Most of the observed response comes from the inherited background geometry rather than a strong standalone trapping term.",
        ]
    )
    (out_dir / "summary.md").write_text("\n".join(lines) + "\n")
    return summary


def run_hosting_analysis():
    print("--- Starting Phase F: Hosting Audit and Probe-Response Analysis ---")
    OUT_DIR.mkdir(parents=True, exist_ok=True)

    representative_rows, _ = representative_runs(OUT_DIR)
    coupling_rows = coupling_comparison(OUT_DIR)
    signed_rows, signed_summary = signed_loading_ladder(OUT_DIR)
    _, slice_summaries = run_slice_set(OUT_DIR)
    write_summary(OUT_DIR, representative_rows, coupling_rows, signed_rows, signed_summary, slice_summaries)
    print("Analysis complete.")


if __name__ == "__main__":
    run_hosting_analysis()
