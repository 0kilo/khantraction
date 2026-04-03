#!/usr/bin/env python3
r"""
Phase G: Classical handedness and chirality audit
Date: 2026-04-02
Purpose: Audit what the current exploratory Maurer-Cartan runtime actually
supports about chirality operators, mirror-pair objecthood, and angular
handedness structure.
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
DEFAULT_A0 = 0.005
DEFAULT_XP0 = (0.0, 0.01, 0.01, 0.0)
DEFAULT_R_MAX = 20.0
ONE_D_POINTS = 15
TWO_D_POINTS = 8

ROOT = Path(__file__).resolve().parents[2]
OUT_DIR = ROOT / "solutions" / "phase_g" / "phase_g_chirality"

OPERATOR_SAMPLES = {
    "base": (np.pi / 8.0, np.pi / 8.0, np.pi / 8.0),
    "offset_positive": (0.7, np.pi / 16.0, -0.9),
    "offset_negative": (-1.1, 3.0 * np.pi / 8.0, 1.2),
}

REPRESENTATIVE_RUNS = {
    "right_handed_base": (0.5, np.pi / 8.0, np.pi / 8.0, np.pi / 8.0),
    "parity_partner": (0.5, -np.pi / 8.0, -np.pi / 8.0, -np.pi / 8.0),
    "left_handed_flip": (0.5, np.pi / 8.0, np.pi / 8.0 + np.pi / 2.0, np.pi / 8.0),
    "right_handed_sheet": (0.5, 0.0, np.pi / 8.0, 0.0),
    "left_handed_sheet": (0.5, 0.0, np.pi / 8.0 + np.pi / 2.0, 0.0),
}

A_CHIRAL_SHEETS = [
    -3.0 * np.pi / 4.0,
    -np.pi / 4.0,
    np.pi / 4.0,
    3.0 * np.pi / 4.0,
]


def finite_range(values: list[float]) -> list[float]:
    arr = np.asarray(values, dtype=float)
    arr = arr[np.isfinite(arr)]
    if arr.size == 0:
        return [float("nan"), float("nan")]
    return [float(arr.min()), float(arr.max())]


class PhaseGChiralitySolver:
    def get_vielbeins(self, theta: float, phi: float, rho: float):
        del theta
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

    def get_chirality_density(self, theta: float, phi: float, rho: float) -> float:
        e_theta, e_phi, e_rho = self.get_vielbeins(theta, phi, rho)
        return float(np.linalg.det(np.stack((e_theta, e_phi, e_rho))))

    def equations(self, r: float, y: np.ndarray):
        w, th, ph, rh, wp, thp, php, rhp, m, grav_potential = y
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
        rho_total = 0.5 * e_neg2l * dq_sq + e_neg2l * omega_mc_sq + u + v_ang

        m_prime = 4.0 * np.pi * r**2 * rho_total
        phi_prime = (m + 4.0 * np.pi * r**3 * (rho_total - 2.0 * u - 2.0 * v_ang)) / (r * (r - 2.0 * m))

        h_prime = phi_prime - (m_prime / r - m / r**2) * e_2l + 2.0 / r
        w_pp = -h_prime * wp - (M_GLUE**2 + LAMBDA_Q * exp2w - 2.0 * XI * r_scalar) * e_2l
        th_pp = -h_prime * thp
        ph_pp = (
            -h_prime * php
            - 4.0 * ANGULAR_PHI_POTENTIAL * np.sin(2.0 * ph) * np.cos(2.0 * ph) * e_2l / g_reg[2, 2]
        )
        rh_pp = -h_prime * rhp
        return [wp, thp, php, rhp, w_pp, th_pp, ph_pp, rh_pp, m_prime, phi_prime]

    def solve(
        self,
        omega0: float,
        theta0: float,
        phi0: float,
        rho0: float,
        *,
        a0: float = DEFAULT_A0,
        xp0: tuple[float, float, float, float] = DEFAULT_XP0,
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
        ]

        def horizon_event(r, y):
            return y[8] - HORIZON_EVENT_FRACTION * r

        horizon_event.terminal = True
        return solve_ivp(
            self.equations,
            (1.0e-4, r_max),
            y0,
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
    a0: float,
    xp0: tuple[float, float, float, float],
    r_max: float,
) -> dict:
    event_radii = [float(v) for v in sol.t_events[0]] if len(sol.t_events) else []
    r_final = float(sol.t[-1])
    final_mass = float(sol.y[8, -1])
    return {
        "omega0": float(omega0),
        "theta0": float(theta0),
        "phi0": float(phi0),
        "rho0": float(rho0),
        "A0": float(a0),
        "xp0": [float(v) for v in xp0],
        "r_max": float(r_max),
        "status": int(sol.status),
        "status_message": str(sol.message),
        "terminated_early": bool(sol.status != 0 or len(event_radii) > 0),
        "horizon_event_radii": event_radii,
        "r_final": r_final,
        "final_mass": final_mass,
        "final_2m_over_r": (2.0 * final_mass / r_final) if r_final > 0.0 else float("nan"),
        "sample_count": int(len(sol.t)),
    }


def write_profile_csv(name: str, sol) -> None:
    pd.DataFrame({"r": sol.t, "mass_m": sol.y[8]}).to_csv(OUT_DIR / f"{name}_profile.csv", index=False)


def operator_checks(solver: PhaseGChiralitySolver) -> list[dict]:
    rows = []
    for sample_name, (theta, phi, rho) in OPERATOR_SAMPLES.items():
        chi = solver.get_chirality_density(theta, phi, rho)
        parity_chi = solver.get_chirality_density(-theta, -phi, -rho)
        flip_chi = solver.get_chirality_density(theta, phi + np.pi / 2.0, rho)
        rows.append(
            {
                "sample": sample_name,
                "theta": float(theta),
                "phi": float(phi),
                "rho": float(rho),
                "chi": float(chi),
                "parity_chi": float(parity_chi),
                "parity_delta": float(parity_chi - chi),
                "flip_chi": float(flip_chi),
                "flip_sum": float(flip_chi + chi),
                "parity_preserves_chi": bool(np.isclose(parity_chi, chi, atol=1e-12)),
                "flip_reverses_chi": bool(np.isclose(flip_chi, -chi, atol=1e-12)),
            }
        )
    pd.DataFrame(rows).to_csv(OUT_DIR / "operator_checks.csv", index=False)
    return rows


def a_chiral_reference(solver: PhaseGChiralitySolver) -> list[dict]:
    rows = []
    for phi in A_CHIRAL_SHEETS:
        rows.append({"phi": float(phi), "chi": float(solver.get_chirality_density(0.0, phi, 0.0))})
    pd.DataFrame(rows).to_csv(OUT_DIR / "a_chiral_reference.csv", index=False)
    return rows


def representative_runs(solver: PhaseGChiralitySolver) -> tuple[list[dict], dict[str, object]]:
    rows = []
    solutions: dict[str, object] = {}
    for run_name, params in REPRESENTATIVE_RUNS.items():
        sol = solver.solve(*params)
        solutions[run_name] = sol
        write_profile_csv(run_name, sol)
        row = {"run": run_name, "chirality_density": solver.get_chirality_density(*params[1:])}
        row.update(
            summarize_solution(
                sol,
                omega0=params[0],
                theta0=params[1],
                phi0=params[2],
                rho0=params[3],
                a0=DEFAULT_A0,
                xp0=DEFAULT_XP0,
                r_max=DEFAULT_R_MAX,
            )
        )
        rows.append(row)
    pd.DataFrame(rows).to_csv(OUT_DIR / "representative_runs.csv", index=False)
    return rows, solutions


def pair_comparisons(solver: PhaseGChiralitySolver, solutions: dict[str, object]) -> list[dict]:
    rows = []
    pairs = [
        ("parity_pair", "right_handed_base", "parity_partner"),
        ("sheet_mirror_pair", "right_handed_sheet", "left_handed_sheet"),
        ("base_mirror_pair", "right_handed_base", "left_handed_flip"),
    ]
    for pair_name, a_name, b_name in pairs:
        sol_a = solutions[a_name]
        sol_b = solutions[b_name]
        common_r = np.linspace(max(sol_a.t[0], sol_b.t[0]), min(sol_a.t[-1], sol_b.t[-1]), 200)
        mass_a = np.interp(common_r, sol_a.t, sol_a.y[8])
        mass_b = np.interp(common_r, sol_b.t, sol_b.y[8])
        params_a = REPRESENTATIVE_RUNS[a_name]
        params_b = REPRESENTATIVE_RUNS[b_name]
        chi_a = solver.get_chirality_density(*params_a[1:])
        chi_b = solver.get_chirality_density(*params_b[1:])
        rows.append(
            {
                "pair": pair_name,
                "run_a": a_name,
                "run_b": b_name,
                "status_a": int(sol_a.status),
                "status_b": int(sol_b.status),
                "r_final_a": float(sol_a.t[-1]),
                "r_final_b": float(sol_b.t[-1]),
                "mass_a": float(sol_a.y[8, -1]),
                "mass_b": float(sol_b.y[8, -1]),
                "mass_abs_diff": float(abs(sol_a.y[8, -1] - sol_b.y[8, -1])),
                "tail_max_abs_diff": float(np.max(np.abs(mass_a - mass_b))),
                "chi_a": float(chi_a),
                "chi_b": float(chi_b),
                "chirality_product": float(chi_a * chi_b),
                "same_chirality_sign": bool(np.sign(chi_a) == np.sign(chi_b)),
                "sign_reversed": bool(np.sign(chi_a) == -np.sign(chi_b)),
            }
        )
    pd.DataFrame(rows).to_csv(OUT_DIR / "pair_comparisons.csv", index=False)
    pd.DataFrame(
        [
            {
                "id": "Right-Handed",
                "mass": float(solutions["right_handed_base"].y[8, -1]),
                "chirality_density": float(solver.get_chirality_density(*REPRESENTATIVE_RUNS["right_handed_base"][1:])),
            },
            {
                "id": "Left-Handed",
                "mass": float(solutions["left_handed_flip"].y[8, -1]),
                "chirality_density": float(solver.get_chirality_density(*REPRESENTATIVE_RUNS["left_handed_flip"][1:])),
            },
        ]
    ).to_csv(OUT_DIR / "mirror_pair_results.csv", index=False)
    return rows


def run_slice_set(solver: PhaseGChiralitySolver) -> dict[str, dict]:
    summaries: dict[str, dict] = {}
    angles_1d = np.linspace(-2.0 * np.pi, 2.0 * np.pi, ONE_D_POINTS)
    angles_2d = np.linspace(-2.0 * np.pi, 2.0 * np.pi, TWO_D_POINTS)

    def make_row(sol, *, theta: float, phi: float, rho: float) -> dict:
        row = {
            "theta": float(theta),
            "phi": float(phi),
            "rho": float(rho),
            "chi": float(solver.get_chirality_density(theta, phi, rho)),
        }
        row.update(
            summarize_solution(
                sol,
                omega0=0.5,
                theta0=theta,
                phi0=phi,
                rho0=rho,
                a0=DEFAULT_A0,
                xp0=DEFAULT_XP0,
                r_max=DEFAULT_R_MAX,
            )
        )
        return row

    rows = {"slice_1d_theta_chi": [], "slice_1d_phi_chi": [], "slice_1d_rho_chi": []}
    for theta in angles_1d:
        sol = solver.solve(0.5, float(theta), np.pi / 8.0, 0.0)
        rows["slice_1d_theta_chi"].append(make_row(sol, theta=float(theta), phi=float(np.pi / 8.0), rho=0.0))
    for phi in angles_1d:
        sol = solver.solve(0.5, 0.0, float(phi), 0.0)
        rows["slice_1d_phi_chi"].append(make_row(sol, theta=0.0, phi=float(phi), rho=0.0))
    for rho in angles_1d:
        sol = solver.solve(0.5, 0.0, np.pi / 8.0, float(rho))
        rows["slice_1d_rho_chi"].append(make_row(sol, theta=0.0, phi=float(np.pi / 8.0), rho=float(rho)))

    for name, row_list in rows.items():
        df = pd.DataFrame(row_list)
        df.to_csv(OUT_DIR / f"{name}.csv", index=False)
        summaries[name] = {
            "chi_range": finite_range(df["chi"].tolist()),
            "mass_range": finite_range(df["final_mass"].tolist()),
            "terminated_early_count": int(df["terminated_early"].sum()),
        }

    rows_2d = {
        "slice_2d_theta_rho_chi": [],
        "slice_2d_phi_theta_chi": [],
        "slice_2d_phi_rho_chi": [],
    }
    for theta in angles_2d:
        for rho in angles_2d:
            sol = solver.solve(0.5, float(theta), np.pi / 8.0, float(rho))
            rows_2d["slice_2d_theta_rho_chi"].append(make_row(sol, theta=float(theta), phi=float(np.pi / 8.0), rho=float(rho)))
    for phi in angles_2d:
        for theta in angles_2d:
            sol = solver.solve(0.5, float(theta), float(phi), 0.0)
            rows_2d["slice_2d_phi_theta_chi"].append(make_row(sol, theta=float(theta), phi=float(phi), rho=0.0))
    for phi in angles_2d:
        for rho in angles_2d:
            sol = solver.solve(0.5, 0.0, float(phi), float(rho))
            rows_2d["slice_2d_phi_rho_chi"].append(make_row(sol, theta=0.0, phi=float(phi), rho=float(rho)))

    for name, row_list in rows_2d.items():
        df = pd.DataFrame(row_list)
        df.to_csv(OUT_DIR / f"{name}.csv", index=False)
        summaries[name] = {
            "chi_range": finite_range(df["chi"].tolist()),
            "mass_range": finite_range(df["final_mass"].tolist()),
            "terminated_early_count": int(df["terminated_early"].sum()),
        }

    # Compatibility alias from the original package.
    pd.read_csv(OUT_DIR / "slice_1d_phi_chi.csv")[["phi", "chi"]].to_csv(OUT_DIR / "slice_1d_chi.csv", index=False)
    return summaries


def rotation_proxy(solutions: dict[str, object]) -> list[dict]:
    base_mass = float(solutions["right_handed_base"].y[8, -1])
    rows = []
    for omega_rot in np.linspace(0.0, 0.1, 5):
        rows.append(
            {
                "omega_rot": float(omega_rot),
                "mass_proxy": float(base_mass * (1.0 + 5.0 * omega_rot**2)),
                "is_solver_backed": False,
                "interpretation": "analytic_proxy_only",
            }
        )
    pd.DataFrame(rows).to_csv(OUT_DIR / "rotational_stability.csv", index=False)
    return rows


def write_summary(
    operator_rows: list[dict],
    a_chiral_rows: list[dict],
    representative_rows: list[dict],
    pair_rows: list[dict],
    slice_summaries: dict[str, dict],
    rotation_rows: list[dict],
) -> dict:
    rep_by_name = {row["run"]: row for row in representative_rows}
    pair_by_name = {row["pair"]: row for row in pair_rows}
    summary = {
        "runtime": {
            "beta": [float(v) for v in BETA],
            "metric_regularization": METRIC_REGULARIZATION,
            "angular_phi_potential": ANGULAR_PHI_POTENTIAL,
            "horizon_event_fraction": HORIZON_EVENT_FRACTION,
            "A0": DEFAULT_A0,
            "xp0": [float(v) for v in DEFAULT_XP0],
            "r_max": DEFAULT_R_MAX,
        },
        "operator_checks": operator_rows,
        "a_chiral_reference": a_chiral_rows,
        "representative_runs": rep_by_name,
        "pair_comparisons": pair_by_name,
        "slice_summaries": slice_summaries,
        "rotation_proxy": rotation_rows,
        "key_results": {
            "parity_preserves_all_samples": all(row["parity_preserves_chi"] for row in operator_rows),
            "flip_reverses_all_samples": all(row["flip_reverses_chi"] for row in operator_rows),
            "base_mirror_mass_abs_diff": pair_by_name["base_mirror_pair"]["mass_abs_diff"],
            "sheet_mirror_mass_abs_diff": pair_by_name["sheet_mirror_pair"]["mass_abs_diff"],
            "parity_pair_mass_abs_diff": pair_by_name["parity_pair"]["mass_abs_diff"],
            "phi_slice_chi_range": slice_summaries["slice_1d_phi_chi"]["chi_range"],
            "theta_slice_chi_range": slice_summaries["slice_1d_theta_chi"]["chi_range"],
            "rho_slice_chi_range": slice_summaries["slice_1d_rho_chi"]["chi_range"],
        },
    }

    (OUT_DIR / "summary.json").write_text(json.dumps(summary, indent=2))

    lines = [
        "# Phase G Chirality Solutions Summary",
        "",
        "Generated by `analysis/phase_g/phase_g_chirality_analysis.py`.",
        "",
        "## Runtime model actually used",
        "- same exploratory symmetry-broken Maurer-Cartan runtime family inherited from audited Phases C to F",
        f"- anisotropic Maurer-Cartan weights: beta = {[float(v) for v in BETA]}",
        f"- metric regularization: {METRIC_REGULARIZATION}",
        f"- phi-localized angular potential coefficient: {ANGULAR_PHI_POTENTIAL}",
        f"- horizon event fraction: {HORIZON_EVENT_FRACTION}",
        f"- field seed amplitude: {DEFAULT_A0}",
        f"- derivative seed: {list(DEFAULT_XP0)}",
        "",
        "## Operator checks",
        f"- parity preserves chirality on all audit samples: {summary['key_results']['parity_preserves_all_samples']}",
        f"- topological chiral flip reverses chirality on all audit samples: {summary['key_results']['flip_reverses_all_samples']}",
        "",
        "## Representative runs",
    ]
    for run_name in ("right_handed_base", "parity_partner", "left_handed_flip", "right_handed_sheet", "left_handed_sheet"):
        row = rep_by_name[run_name]
        lines.append(
            f"- `{run_name}`: status={row['status']}, r_final={row['r_final']}, "
            f"mass={row['final_mass']}, chi={row['chirality_density']}"
        )
    lines.extend(
        [
            "",
            "## Pair comparisons",
            f"- parity pair mass abs diff: {pair_by_name['parity_pair']['mass_abs_diff']}",
            f"- base mirror pair mass abs diff: {pair_by_name['base_mirror_pair']['mass_abs_diff']}",
            f"- sheet mirror pair mass abs diff: {pair_by_name['sheet_mirror_pair']['mass_abs_diff']}",
            "",
            "## Slice summaries",
            f"- `theta`: chi range {slice_summaries['slice_1d_theta_chi']['chi_range']}, terminated_early={slice_summaries['slice_1d_theta_chi']['terminated_early_count']}",
            f"- `phi`: chi range {slice_summaries['slice_1d_phi_chi']['chi_range']}, terminated_early={slice_summaries['slice_1d_phi_chi']['terminated_early_count']}",
            f"- `rho`: chi range {slice_summaries['slice_1d_rho_chi']['chi_range']}, terminated_early={slice_summaries['slice_1d_rho_chi']['terminated_early_count']}",
            f"- `theta_rho`: chi range {slice_summaries['slice_2d_theta_rho_chi']['chi_range']}, terminated_early={slice_summaries['slice_2d_theta_rho_chi']['terminated_early_count']}",
            f"- `phi_theta`: chi range {slice_summaries['slice_2d_phi_theta_chi']['chi_range']}, terminated_early={slice_summaries['slice_2d_phi_theta_chi']['terminated_early_count']}",
            f"- `phi_rho`: chi range {slice_summaries['slice_2d_phi_rho_chi']['chi_range']}, terminated_early={slice_summaries['slice_2d_phi_rho_chi']['terminated_early_count']}",
            "",
            "## Rotational proxy",
            "- `rotational_stability.csv` is retained only as an analytic proxy table derived from the old mass-rescaling ansatz.",
            "- It is not a solved rotational stability result and should not be used as proof of spin-like robustness.",
            "",
            "## Interpretation",
            "- Chirality is controlled by `phi`: parity preserves `chi`, while a `phi -> phi + pi/2` chiral flip reverses it exactly.",
            "- Right-handed and left-handed mirror pairs remain nearly mass-degenerate on the audited active-runtime runs, supporting an enantiomer interpretation at the mapping/object level.",
            "- Theta and rho do not control chirality sign on the audited slices; they remain paired spectator coordinates for handedness.",
            "- The current package supports classical handedness architecture. It does not support a direct solved claim about rotational stability or hosted angular momentum.",
        ]
    )
    (OUT_DIR / "summary.md").write_text("\n".join(lines) + "\n")
    return summary


def run_chirality_analysis():
    print("--- Starting Phase G: Chirality Audit and Handedness Analysis ---")
    OUT_DIR.mkdir(parents=True, exist_ok=True)
    solver = PhaseGChiralitySolver()

    operator_rows = operator_checks(solver)
    a_chiral_rows = a_chiral_reference(solver)
    representative_rows, solutions = representative_runs(solver)
    pair_rows = pair_comparisons(solver, solutions)
    slice_summaries = run_slice_set(solver)
    rotation_rows = rotation_proxy(solutions)
    write_summary(operator_rows, a_chiral_rows, representative_rows, pair_rows, slice_summaries, rotation_rows)
    print("Analysis complete.")


if __name__ == "__main__":
    run_chirality_analysis()
