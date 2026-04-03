#!/usr/bin/env python3
r"""
Phase D: Identity, Persistence, and Rigidity Analysis
Date: 2026-04-02
Purpose: Audit what the current exploratory Maurer-Cartan runtime actually
supports about classical identity, neighborhood persistence, scale variation,
and rigidity-like sensitivity claims.
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
BETA = np.array([0.01, 0.02, 0.03])
METRIC_REGULARIZATION = 1.0e-4
ANGULAR_PHI_POTENTIAL = 0.01
HORIZON_EVENT_FRACTION = 0.48


def first_radius_at_fraction(times: np.ndarray, masses: np.ndarray, fraction: float) -> float:
    target = fraction * float(masses[-1])
    idx = np.where(masses >= target)[0]
    return float(times[idx[0]]) if len(idx) else float("nan")


def finite_range(values: list[float]) -> list[float]:
    arr = np.asarray(values, dtype=float)
    arr = arr[np.isfinite(arr)]
    if arr.size == 0:
        return [float("nan"), float("nan")]
    return [float(arr.min()), float(arr.max())]


class PhaseDIdentitySolver:
    def get_vielbeins(self, theta: float, phi: float, rho: float):
        c2p, s2p = np.cos(2.0 * phi), np.sin(2.0 * phi)
        c2r, s2r = np.cos(2.0 * rho), np.sin(2.0 * rho)
        e_rho = np.array([0.0, 0.0, 1.0])
        e_phi = np.array([s2r, c2r, 0.0])
        e_theta = np.array([c2r * c2p, -s2r * c2p, s2p])
        return e_theta, e_phi, e_rho

    def get_vielbein_derivatives(self, theta: float, phi: float, rho: float):
        del theta
        c2p, s2p = np.cos(2.0 * phi), np.sin(2.0 * phi)
        c2r, s2r = np.cos(2.0 * rho), np.sin(2.0 * rho)
        derivs = {}
        derivs[("phi", "theta")] = np.array([-2.0 * c2r * s2p, 2.0 * s2r * s2p, 2.0 * c2p])
        derivs[("phi", "phi")] = np.array([0.0, 0.0, 0.0])
        derivs[("phi", "rho")] = np.array([0.0, 0.0, 0.0])
        derivs[("rho", "theta")] = np.array([-2.0 * s2r * c2p, -2.0 * c2r * c2p, 0.0])
        derivs[("rho", "phi")] = np.array([2.0 * c2r, -2.0 * s2r, 0.0])
        derivs[("rho", "rho")] = np.array([0.0, 0.0, 0.0])
        return derivs

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

    def get_metric_derivatives(self, omega: float, theta: float, phi: float, rho: float):
        exp2w = np.exp(2.0 * omega)
        e_theta, e_phi, e_rho = self.get_vielbeins(theta, phi, rho)
        e = (e_theta, e_phi, e_rho)
        d_e = self.get_vielbein_derivatives(theta, phi, rho)
        b = exp2w + 2.0 * BETA
        d_g = np.zeros((4, 4, 4))
        d_g[0, 0, 0] = 2.0 * exp2w
        for i, ei in enumerate(e):
            for j, ej in enumerate(e):
                d_g[0, i + 1, j + 1] = 2.0 * exp2w * np.sum(ei * ej)
        channel_names = ("theta", "phi", "rho")
        for k_idx, k_name in enumerate(channel_names, start=1):
            for i, i_name in enumerate(channel_names):
                for j, j_name in enumerate(channel_names):
                    term1 = d_e.get((k_name, i_name), np.zeros(3))
                    term2 = d_e.get((k_name, j_name), np.zeros(3))
                    d_g[k_idx, i + 1, j + 1] = np.sum(b * (term1 * e[j] + e[i] * term2))
        return d_g

    def equations(self, r: float, y: np.ndarray, a0: float):
        w, th, ph, rh, wp, thp, php, rhp, m, grav_potential = y
        del grav_potential, a0
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
        g_inv = np.linalg.inv(g_reg)
        d_g = self.get_metric_derivatives(w, th, ph, rh)

        if w > 10.0:
            return np.zeros_like(y)

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
        rho_dens = 0.5 * e_neg2l * dq_sq + e_neg2l * omega_mc_sq + u + v_ang
        v_eff_w = (M_GLUE**2 + LAMBDA_Q * exp2w - 2.0 * XI * r_scalar) * exp2w
        v_eff_ph = 4.0 * ANGULAR_PHI_POTENTIAL * np.sin(2.0 * ph) * np.cos(2.0 * ph)

        m_prime = 4.0 * np.pi * r**2 * rho_dens
        phi_prime = (m + 4.0 * np.pi * r**3 * (rho_dens - 2.0 * u - 2.0 * v_ang)) / (r * (r - 2.0 * m))
        l_prime = (m_prime / r - m / r**2) / (1.0 - 2.0 * m / r)
        h_prime = phi_prime - l_prime + 2.0 / r

        p_prime = np.zeros(4)
        for m_idx in range(4):
            term_geom = 0.5 * np.dot(xp, d_g[m_idx] @ xp)
            term_damp = -h_prime * np.dot(g[m_idx], xp)
            term_pot = -e_2l * (v_eff_w if m_idx == 0 else (v_eff_ph if m_idx == 2 else 0.0))
            p_prime[m_idx] = term_geom + term_damp + term_pot

        quadratic_terms = np.array(
            [np.dot(d_g[:, m_idx, :].T @ xp, xp) for m_idx in range(4)]
        )
        xpp = g_inv @ (p_prime - quadratic_terms)
        return np.concatenate([xp, xpp, [m_prime, phi_prime]])

    def solve(
        self,
        omega0: float,
        theta0: float,
        phi0: float,
        rho0: float,
        a0: float = 0.02,
        xp0: list[float] | tuple[float, float, float, float] = (0.0, 0.0, 0.0, 0.0),
        r_max: float = 20.0,
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

        def horizon_event(r, y, a0):
            del a0
            return y[8] - HORIZON_EVENT_FRACTION * r

        horizon_event.terminal = True
        return solve_ivp(
            self.equations,
            (1.0e-4, r_max),
            y0,
            args=(a0,),
            method="RK45",
            events=horizon_event,
            rtol=1.0e-6,
            atol=1.0e-8,
        )


def summarize_solution(
    sol,
    *,
    omega0: float,
    theta0: float,
    phi0: float,
    rho0: float,
    a0: float,
    xp0: list[float] | tuple[float, float, float, float],
    r_max: float,
) -> dict:
    final_mass = float(sol.y[8, -1])
    r_half = first_radius_at_fraction(sol.t, sol.y[8], 0.5)
    compactness = final_mass / r_half if np.isfinite(r_half) and r_half != 0.0 else float("nan")
    event_radii = [float(v) for v in sol.t_events[0]] if len(sol.t_events) else []
    r_final = float(sol.t[-1])
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
        "mass_half_radius": r_half,
        "compactness": compactness,
        "final_2m_over_r": (2.0 * final_mass / r_final) if r_final > 0.0 else float("nan"),
    }


def neighborhood_rows(solver: PhaseDIdentitySolver, specs: list[dict]) -> list[dict]:
    rows = []
    deltas = np.linspace(-0.2, 0.2, 5)
    for spec in specs:
        for delta in deltas:
            theta0 = spec["theta0"]
            phi0 = spec["phi0"]
            rho0 = spec["rho0"]
            if spec["axis"] == "theta":
                theta0 += float(delta)
            elif spec["axis"] == "phi":
                phi0 += float(delta)
            elif spec["axis"] == "rho":
                rho0 += float(delta)
            sol = solver.solve(
                spec["omega0"],
                theta0,
                phi0,
                rho0,
                a0=spec["A0"],
                xp0=spec["xp0"],
                r_max=spec["r_max"],
            )
            row = {
                "sector": spec["sector"],
                "axis": spec["axis"],
                "delta": float(delta),
                "center_theta0": float(spec["theta0"]),
                "center_phi0": float(spec["phi0"]),
                "center_rho0": float(spec["rho0"]),
            }
            row.update(
                summarize_solution(
                    sol,
                    omega0=spec["omega0"],
                    theta0=theta0,
                    phi0=phi0,
                    rho0=rho0,
                    a0=spec["A0"],
                    xp0=spec["xp0"],
                    r_max=spec["r_max"],
                )
            )
            rows.append(row)
    return rows


def analyze_variation(rows: list[dict], group_key: str) -> dict:
    summary = {}
    grouped = {}
    for row in rows:
        grouped.setdefault(row[group_key], []).append(row)
    for key, group in grouped.items():
        masses = [row["final_mass"] for row in group]
        compactnesses = [row["compactness"] for row in group]
        r_halves = [row["mass_half_radius"] for row in group]
        summary[key] = {
            "sample_count": len(group),
            "mass_range": finite_range(masses),
            "mass_range_width": float(np.nanmax(masses) - np.nanmin(masses)),
            "compactness_range": finite_range(compactnesses),
            "r_half_range": finite_range(r_halves),
            "terminated_early_count": int(sum(1 for row in group if row["terminated_early"])),
        }
    return summary


def write_summary_markdown(summary: dict, out_path: Path):
    lines = [
        "# Phase D Identity Analysis Summary",
        "",
        "Generated by `analysis/phase_d/phase_d_identity_analysis.py`.",
        "",
        "## Runtime model actually used",
        "- exploratory anisotropic Maurer-Cartan weights: beta = [0.01, 0.02, 0.03]",
        f"- metric regularization added to target metric inverse: {METRIC_REGULARIZATION}",
        f"- exploratory phi-localized angular potential coefficient: {ANGULAR_PHI_POTENTIAL}",
        f"- horizon event fraction: {HORIZON_EVENT_FRACTION}",
        "- interpretation: this is the same exploratory symmetry-broken runtime family audited in Phase C, now reused for identity and persistence diagnostics.",
        "",
        "## Scale sweep",
    ]

    omega_summary = summary["omega_sweep"]
    lines.extend(
        [
            f"- scalar-anchor omega sweep mass range: {omega_summary['mass_range']}",
            f"- scalar-anchor omega sweep compactness range: {omega_summary['compactness_range']}",
            "- interpretation: omega changes concentration measurably, so scale is not an identity invariant in the current runtime.",
            "",
            "## Local neighborhood tests",
        ]
    )
    for sector, sector_summary in summary["neighborhoods"].items():
        lines.append(
            f"- `{sector}`: mass range {sector_summary['mass_range']}, terminated_early={sector_summary['terminated_early_count']} of {sector_summary['sample_count']}"
        )
    lines.extend(
        [
            "- interpretation: local identity behavior is strongly phi-controlled. Scalar-theta and scalar-rho neighborhoods are nearly flat, scalar-phi neighborhoods vary smoothly, and the exact phi-sheet neighborhood contains an early-termination boundary point.",
            "",
            "## Amplitude and outer-box sensitivity",
        ]
    )
    for label in ("amplitude_sensitivity", "outer_box_sensitivity"):
        lines.append(f"### `{label}`")
        for config, config_summary in summary[label].items():
            lines.append(
                f"- `{config}`: mass range {config_summary['mass_range']}, r_half range {config_summary['r_half_range']}, terminated_early={config_summary['terminated_early_count']} of {config_summary['sample_count']}"
            )
    lines.extend(
        [
            "- interpretation: there is no evidence here for absolute rigidity. Full-domain survivors are materially sensitive to both amplitude and outer-box choice, while the old sheet-anchor boundary test looked rigid only because it terminated before reaching the tested outer boundaries.",
            "",
            "## 1D slices",
        ]
    )
    for axis, axis_summary in summary["slice_1d"].items():
        lines.append(
            f"- `{axis}`: mass range {axis_summary['mass_range']}, terminated_early={axis_summary['terminated_early_count']} of {axis_summary['sample_count']}"
        )
    lines.extend(
        [
            "",
            "## 2D slices",
        ]
    )
    for plane, plane_summary in summary["slice_2d"].items():
        lines.append(
            f"- `{plane}`: mass range {plane_summary['mass_range']}, terminated_early={plane_summary['terminated_early_count']} of {plane_summary['sample_count']}"
        )
    lines.extend(
        [
            "",
            "## Interpretation",
            "- The current Phase D package does distinguish scale variation from angular variation, but it does not show a scale-invariant identity fingerprint.",
            "- The strongest local organization remains phi-controlled: off the singular sheets, nearby configurations can deform smoothly; landing on the exact phi sheet can trigger early termination.",
            "- Theta and rho do not support a robust independent species hierarchy in this runtime; theta is especially weak away from phi-driven structure.",
            "- The data supports a boundary-organized family picture rather than a discrete quantized-species picture.",
            "- The refreshed rigidity reading is negative: amplitude and outer-box sensitivity remain significant for full-domain survivors.",
        ]
    )
    out_path.write_text("\n".join(lines) + "\n")


def run_identity_analysis():
    print("--- Starting Phase D: Identity and Persistence Audit Analysis ---")
    solver = PhaseDIdentitySolver()
    out_dir = Path("solutions/phase_d/phase_d_identity")
    out_dir.mkdir(parents=True, exist_ok=True)

    # 1. Scale sweep on the scalar-like anchor
    print("Running omega sweep...")
    omega_rows = []
    for omega in np.linspace(0.1, 1.0, 5):
        sol = solver.solve(omega, 0.0, 0.0, 0.0)
        row = summarize_solution(
            sol,
            omega0=float(omega),
            theta0=0.0,
            phi0=0.0,
            rho0=0.0,
            a0=0.02,
            xp0=(0.0, 0.0, 0.0, 0.0),
            r_max=20.0,
        )
        row["configuration"] = "scalar_anchor"
        omega_rows.append(row)
    pd.DataFrame(omega_rows).to_csv(out_dir / "omega_sweep_invariance.csv", index=False)

    # 2. Local neighborhood tests around multiple sectors
    print("Running neighborhood sweeps...")
    neighborhood_specs = [
        {
            "sector": "scalar_phi_local",
            "axis": "phi",
            "omega0": 0.5,
            "theta0": 0.0,
            "phi0": 0.0,
            "rho0": 0.0,
            "A0": 0.02,
            "xp0": (0.0, 0.0, 0.0, 0.0),
            "r_max": 20.0,
        },
        {
            "sector": "scalar_theta_local",
            "axis": "theta",
            "omega0": 0.5,
            "theta0": 0.0,
            "phi0": 0.0,
            "rho0": 0.0,
            "A0": 0.02,
            "xp0": (0.0, 0.0, 0.0, 0.0),
            "r_max": 20.0,
        },
        {
            "sector": "scalar_rho_local",
            "axis": "rho",
            "omega0": 0.5,
            "theta0": 0.0,
            "phi0": 0.0,
            "rho0": 0.0,
            "A0": 0.02,
            "xp0": (0.0, 0.0, 0.0, 0.0),
            "r_max": 20.0,
        },
        {
            "sector": "phi_sheet_local",
            "axis": "phi",
            "omega0": 0.5,
            "theta0": 0.0,
            "phi0": math.pi / 4.0,
            "rho0": 0.0,
            "A0": 0.02,
            "xp0": (0.0, 0.0, 0.01, 0.0),
            "r_max": 20.0,
        },
        {
            "sector": "phi_offsheet_local",
            "axis": "phi",
            "omega0": 0.5,
            "theta0": 0.0,
            "phi0": math.pi / 4.0 - 0.1,
            "rho0": 0.0,
            "A0": 0.02,
            "xp0": (0.0, 0.0, 0.01, 0.0),
            "r_max": 20.0,
        },
    ]
    neighborhood_result_rows = neighborhood_rows(solver, neighborhood_specs)
    pd.DataFrame(neighborhood_result_rows).to_csv(out_dir / "neighborhood_results.csv", index=False)
    pd.DataFrame(
        [row for row in neighborhood_result_rows if row["sector"] == "phi_sheet_local"]
    ).to_csv(out_dir / "phi_neighborhood_persistence.csv", index=False)

    # 3. Amplitude sensitivity and outer-box sensitivity on representative configurations
    print("Running amplitude and outer-box sensitivity tests...")
    config_specs = [
        {
            "configuration": "scalar_anchor",
            "omega0": 0.5,
            "theta0": 0.0,
            "phi0": 0.0,
            "rho0": 0.0,
            "xp0": (0.0, 0.0, 0.0, 0.0),
        },
        {
            "configuration": "phi_sheet_anchor",
            "omega0": 0.5,
            "theta0": 0.0,
            "phi0": math.pi / 4.0,
            "rho0": 0.0,
            "xp0": (0.0, 0.0, 0.01, 0.0),
        },
        {
            "configuration": "phi_offsheet_anchor",
            "omega0": 0.5,
            "theta0": 0.0,
            "phi0": math.pi / 4.0 - 0.1,
            "rho0": 0.0,
            "xp0": (0.0, 0.0, 0.01, 0.0),
        },
    ]

    amplitude_rows = []
    for spec in config_specs:
        for a0 in (0.01, 0.02, 0.04):
            sol = solver.solve(
                spec["omega0"],
                spec["theta0"],
                spec["phi0"],
                spec["rho0"],
                a0=a0,
                xp0=spec["xp0"],
                r_max=20.0,
            )
            row = {"configuration": spec["configuration"], "test_type": "amplitude_sensitivity", "parameter": float(a0)}
            row.update(
                summarize_solution(
                    sol,
                    omega0=spec["omega0"],
                    theta0=spec["theta0"],
                    phi0=spec["phi0"],
                    rho0=spec["rho0"],
                    a0=a0,
                    xp0=spec["xp0"],
                    r_max=20.0,
                )
            )
            amplitude_rows.append(row)
    pd.DataFrame(amplitude_rows).to_csv(out_dir / "amplitude_sensitivity.csv", index=False)
    pd.DataFrame(
        [row for row in amplitude_rows if row["configuration"] == "phi_sheet_anchor"]
    ).to_csv(out_dir / "amplitude_rigidity.csv", index=False)

    outer_box_rows = []
    for spec in config_specs:
        for r_max in (20.0, 15.0, 10.0, 5.0):
            sol = solver.solve(
                spec["omega0"],
                spec["theta0"],
                spec["phi0"],
                spec["rho0"],
                a0=0.02,
                xp0=spec["xp0"],
                r_max=r_max,
            )
            row = {"configuration": spec["configuration"], "test_type": "outer_box_sensitivity", "parameter": float(r_max)}
            row.update(
                summarize_solution(
                    sol,
                    omega0=spec["omega0"],
                    theta0=spec["theta0"],
                    phi0=spec["phi0"],
                    rho0=spec["rho0"],
                    a0=0.02,
                    xp0=spec["xp0"],
                    r_max=r_max,
                )
            )
            outer_box_rows.append(row)
    pd.DataFrame(outer_box_rows).to_csv(out_dir / "outer_box_sensitivity.csv", index=False)

    rigidity_rows = amplitude_rows + outer_box_rows
    pd.DataFrame(rigidity_rows).to_csv(out_dir / "rigidity_results.csv", index=False)

    # 4. Full 1D / 2D slice protocol on the active regular comparison setup
    print("Running full 1D / 2D slice protocol...")
    grid_1d = np.linspace(-2.0 * np.pi, 2.0 * np.pi, 20)
    grid_2d = np.linspace(-2.0 * np.pi, 2.0 * np.pi, 10)

    slice_1d_specs = {
        "theta": {"fixed": {"omega0": 0.5, "phi0": np.pi / 8.0, "rho0": 0.0}, "vary": "theta0"},
        "phi": {"fixed": {"omega0": 0.5, "theta0": 0.0, "rho0": 0.0}, "vary": "phi0"},
        "rho": {"fixed": {"omega0": 0.5, "theta0": 0.0, "phi0": np.pi / 8.0}, "vary": "rho0"},
    }
    slice_1d_summary = {}
    for axis, spec in slice_1d_specs.items():
        rows = []
        for angle in grid_1d:
            params = {"theta0": 0.0, "phi0": 0.0, "rho0": 0.0}
            params.update(spec["fixed"])
            params[spec["vary"]] = float(angle)
            sol = solver.solve(
                params["omega0"],
                params["theta0"],
                params["phi0"],
                params["rho0"],
                r_max=10.0,
            )
            row = {axis: float(angle)}
            row.update(
                summarize_solution(
                    sol,
                    omega0=params["omega0"],
                    theta0=params["theta0"],
                    phi0=params["phi0"],
                    rho0=params["rho0"],
                    a0=0.02,
                    xp0=(0.0, 0.0, 0.0, 0.0),
                    r_max=10.0,
                )
            )
            rows.append(row)
        path = out_dir / f"slice_1d_{axis}.csv"
        pd.DataFrame(rows).to_csv(path, index=False)
        if axis == "phi":
            pd.DataFrame(rows).to_csv(out_dir / "slice_1d_identity.csv", index=False)
        masses = [row["final_mass"] for row in rows]
        slice_1d_summary[axis] = {
            "path": str(path),
            "sample_count": len(rows),
            "mass_range": finite_range(masses),
            "mass_range_width": float(np.nanmax(masses) - np.nanmin(masses)),
            "terminated_early_count": int(sum(1 for row in rows if row["terminated_early"])),
            "domain": [-2.0 * np.pi, 2.0 * np.pi],
            "r_max": 10.0,
        }

    slice_2d_specs = {
        "phi_theta": {"axes": ("phi0", "theta0"), "fixed": {"omega0": 0.5, "rho0": 0.0}},
        "phi_rho": {"axes": ("phi0", "rho0"), "fixed": {"omega0": 0.5, "theta0": 0.0}},
        "theta_rho": {"axes": ("theta0", "rho0"), "fixed": {"omega0": 0.5, "phi0": np.pi / 8.0}},
    }
    slice_2d_summary = {}
    for plane, spec in slice_2d_specs.items():
        axis1, axis2 = spec["axes"]
        rows = []
        for angle1 in grid_2d:
            for angle2 in grid_2d:
                params = {"theta0": 0.0, "phi0": 0.0, "rho0": 0.0}
                params.update(spec["fixed"])
                params[axis1] = float(angle1)
                params[axis2] = float(angle2)
                sol = solver.solve(
                    params["omega0"],
                    params["theta0"],
                    params["phi0"],
                    params["rho0"],
                    r_max=5.0,
                )
                row = {
                    axis1.replace("0", ""): float(angle1),
                    axis2.replace("0", ""): float(angle2),
                }
                row.update(
                    summarize_solution(
                        sol,
                        omega0=params["omega0"],
                        theta0=params["theta0"],
                        phi0=params["phi0"],
                        rho0=params["rho0"],
                        a0=0.02,
                        xp0=(0.0, 0.0, 0.0, 0.0),
                        r_max=5.0,
                    )
                )
                rows.append(row)
        path = out_dir / f"slice_2d_{plane}.csv"
        pd.DataFrame(rows).to_csv(path, index=False)
        masses = [row["final_mass"] for row in rows]
        slice_2d_summary[plane] = {
            "path": str(path),
            "sample_count": len(rows),
            "mass_range": finite_range(masses),
            "mass_range_width": float(np.nanmax(masses) - np.nanmin(masses)),
            "terminated_early_count": int(sum(1 for row in rows if row["terminated_early"])),
            "domain": [-2.0 * np.pi, 2.0 * np.pi],
            "r_max": 5.0,
        }

    summary = {
        "config": {
            "beta": BETA.tolist(),
            "metric_regularization": METRIC_REGULARIZATION,
            "angular_phi_potential": ANGULAR_PHI_POTENTIAL,
            "horizon_event_fraction": HORIZON_EVENT_FRACTION,
            "kappa": KAPPA,
            "xi": XI,
            "m_glue": M_GLUE,
            "lambda_q": LAMBDA_Q,
        },
        "omega_sweep": {
            "sample_count": len(omega_rows),
            "mass_range": finite_range([row["final_mass"] for row in omega_rows]),
            "compactness_range": finite_range([row["compactness"] for row in omega_rows]),
            "terminated_early_count": int(sum(1 for row in omega_rows if row["terminated_early"])),
            "path": str(out_dir / "omega_sweep_invariance.csv"),
        },
        "neighborhoods": analyze_variation(neighborhood_result_rows, "sector"),
        "amplitude_sensitivity": analyze_variation(amplitude_rows, "configuration"),
        "outer_box_sensitivity": analyze_variation(outer_box_rows, "configuration"),
        "slice_1d": slice_1d_summary,
        "slice_2d": slice_2d_summary,
        "status": "phase_d_identity_audit_complete",
    }

    (out_dir / "summary.json").write_text(json.dumps(summary, indent=2))
    write_summary_markdown(summary, out_dir / "summary.md")
    print("Phase D identity audit analysis complete.")


if __name__ == "__main__":
    run_identity_analysis()
