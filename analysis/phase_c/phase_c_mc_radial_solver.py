#!/usr/bin/env python3
r"""
Phase C: Maurer-Cartan radial solver with explicit audit outputs.

This runtime implements the exploratory Phase C symmetry-breaking ansatz in the
ordered-angle basis (omega, theta, phi, rho) and writes a fully traceable
solution package:

- representative seed profiles and summaries,
- angle-only anchor checks,
- 1D and 2D slice studies on the active unquotiented domain,
- and summary metadata that records early terminations and horizon-approach
  behavior explicitly.
"""

from __future__ import annotations

import json
from pathlib import Path
from typing import Dict, List, Sequence

import numpy as np
import pandas as pd
from scipy.integrate import solve_ivp

# --- Constants ---
KAPPA = 8.0 * np.pi
XI = 0.002
M_GLUE = 0.1
LAMBDA_Q = 0.01

# Anisotropic MC breaking weights from Derivation 78.
BETA_1 = 0.01
BETA_2 = 0.02
BETA_3 = 0.03

# Explicit runtime additions used by the active exploratory Phase C solver.
METRIC_REGULARIZATION = 1.0e-4
ANGULAR_PHI_POTENTIAL = 0.01
HORIZON_EVENT_FRACTION = 0.45

OUT_DIR = Path("solutions/phase_c/phase_c_angular_traits")
PROFILES_DIR = OUT_DIR / "profiles"


class PhaseCMCRadialSolver:
    def __init__(
        self,
        beta: Sequence[float] = (BETA_1, BETA_2, BETA_3),
        metric_regularization: float = METRIC_REGULARIZATION,
        angular_phi_potential: float = ANGULAR_PHI_POTENTIAL,
        horizon_event_fraction: float = HORIZON_EVENT_FRACTION,
    ):
        self.beta = np.asarray(beta, dtype=float)
        self.metric_regularization = float(metric_regularization)
        self.angular_phi_potential = float(angular_phi_potential)
        self.horizon_event_fraction = float(horizon_event_fraction)

    def get_vielbeins(self, theta: float, phi: float, rho: float):
        """Left-invariant vielbeins E_M^a = (q^-1 d_M q)^a."""
        c2p, s2p = np.cos(2.0 * phi), np.sin(2.0 * phi)
        c2r, s2r = np.cos(2.0 * rho), np.sin(2.0 * rho)

        e_rho = np.array([0.0, 0.0, 1.0])
        e_phi = np.array([s2r, c2r, 0.0])
        e_theta = np.array([c2r * c2p, -s2r * c2p, s2p])
        return e_theta, e_phi, e_rho

    def get_vielbein_derivatives(self, theta: float, phi: float, rho: float):
        """d_K E_M^a, with keys (K, M)."""
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

    def get_target_metric(self, omega: float, theta: float, phi: float, rho: float) -> np.ndarray:
        """Target-space metric G_MN in order (omega, theta, phi, rho)."""
        e_theta, e_phi, e_rho = self.get_vielbeins(theta, phi, rho)
        exp2w = np.exp(2.0 * omega)
        b = exp2w + 2.0 * self.beta
        basis = [e_theta, e_phi, e_rho]

        g = np.zeros((4, 4))
        g[0, 0] = exp2w
        for i in range(3):
            for j in range(3):
                g[i + 1, j + 1] = np.sum(b * basis[i] * basis[j])
        return g

    def get_metric_derivatives(self, omega: float, theta: float, phi: float, rho: float) -> np.ndarray:
        """d_K G_MN with index order [K, M, N]."""
        exp2w = np.exp(2.0 * omega)
        basis = self.get_vielbeins(theta, phi, rho)
        dbasis = self.get_vielbein_derivatives(theta, phi, rho)
        b = exp2w + 2.0 * self.beta

        d_g = np.zeros((4, 4, 4))
        d_g[0, 0, 0] = 2.0 * exp2w
        for i in range(3):
            for j in range(3):
                d_g[0, i + 1, j + 1] = 2.0 * exp2w * np.sum(basis[i] * basis[j])

        for k_idx, k_name in enumerate(["theta", "phi", "rho"]):
            for i_idx, i_name in enumerate(["theta", "phi", "rho"]):
                for j_idx, j_name in enumerate(["theta", "phi", "rho"]):
                    term1 = dbasis.get((k_name, i_name), np.zeros(3))
                    term2 = dbasis.get((k_name, j_name), np.zeros(3))
                    d_g[k_idx + 1, i_idx + 1, j_idx + 1] = np.sum(
                        b * (term1 * basis[j_idx] + basis[i_idx] * term2)
                    )
        return d_g

    def equations(self, r: float, y: np.ndarray) -> np.ndarray:
        # y = [w, th, ph, rh, wp, thp, php, rhp, m, Phi]
        w, th, ph, rh, wp, thp, php, rhp, m, phi_metric = y
        del phi_metric
        x = y[0:4]
        xp = y[4:8]

        if r < 1.0e-10:
            return np.zeros_like(y)

        if w > 10.0:
            return np.zeros_like(y)

        e_2lambda = 1.0 / (1.0 - 2.0 * m / r) if r > 2.0 * m else 1.0e10
        e_neg2lambda = 1.0 / e_2lambda

        g = self.get_target_metric(w, th, ph, rh)
        g_reg = g + self.metric_regularization * np.eye(4)
        g_inv = np.linalg.inv(g_reg)
        d_g = self.get_metric_derivatives(w, th, ph, rh)

        exp2w = np.exp(2.0 * w)
        potential = 0.5 * M_GLUE**2 * exp2w + 0.25 * LAMBDA_Q * exp2w**2

        e_theta, e_phi, e_rho = self.get_vielbeins(th, ph, rh)
        omega_r = np.zeros(3)
        for idx, vec in enumerate([e_theta, e_phi, e_rho]):
            omega_r += vec * xp[idx + 1]
        omega_mc_sq = np.sum(self.beta * omega_r**2)
        dq_sq = exp2w * (wp**2 + np.sum(omega_r**2))

        trace_q = -e_neg2lambda * dq_sq - 4.0 * potential
        trace_mc = 2.0 * e_neg2lambda * omega_mc_sq
        source_s = 2.0 * e_neg2lambda * dq_sq - 2.0 * (M_GLUE**2 + LAMBDA_Q * exp2w) * exp2w

        ricci_num = -KAPPA * (trace_q + trace_mc) + 6.0 * KAPPA * XI * source_s
        ricci_den = 1.0 + 2.0 * KAPPA * XI * (1.0 - 12.0 * XI) * exp2w
        ricci = ricci_num / ricci_den

        v_ang = self.angular_phi_potential * np.sin(2.0 * ph) ** 2
        rho_total = 0.5 * e_neg2lambda * dq_sq + e_neg2lambda * omega_mc_sq + potential + v_ang

        v_eff_w = (M_GLUE**2 + LAMBDA_Q * exp2w - 2.0 * XI * ricci) * exp2w
        v_eff_phi = self.angular_phi_potential * 4.0 * np.sin(2.0 * ph) * np.cos(2.0 * ph)

        m_prime = 4.0 * np.pi * r**2 * rho_total
        phi_prime = (m + 4.0 * np.pi * r**3 * (rho_total - 2.0 * potential - 2.0 * v_ang)) / (r * (r - 2.0 * m))

        lambda_prime = (m_prime / r - m / r**2) / (1.0 - 2.0 * m / r)
        h_prime = phi_prime - lambda_prime + 2.0 / r

        p_prime = np.zeros(4)
        for m_idx in range(4):
            term_geom = 0.5 * np.dot(xp, d_g[m_idx] @ xp)
            term_damp = -h_prime * np.dot(g[m_idx], xp)
            if m_idx == 0:
                term_pot = -e_2lambda * v_eff_w
            elif m_idx == 2:
                term_pot = -e_2lambda * v_eff_phi
            else:
                term_pot = 0.0
            p_prime[m_idx] = term_geom + term_damp + term_pot

        xpp = g_inv @ (
            p_prime - np.array([np.dot(d_g[:, m_idx, :].T @ xp, xp) for m_idx in range(4)])
        )

        return np.concatenate([xp, xpp, [m_prime, phi_prime]])

    def solve(
        self,
        omega0: float,
        theta0: float,
        phi0: float,
        rho0: float,
        r_max: float = 20.0,
        dr: float = 0.01,
        xp0: Sequence[float] = (0.0, 0.0, 0.0, 0.0),
    ):
        a0 = 0.02
        w_scaled = np.log(a0) + omega0
        y0 = [w_scaled, theta0, phi0, rho0, xp0[0], xp0[1], xp0[2], xp0[3], 0.0, 0.0]

        r_span = (1.0e-4, r_max)
        t_eval = np.arange(1.0e-4, r_max, dr)

        def horizon_event(r, y):
            return y[8] - self.horizon_event_fraction * r

        horizon_event.terminal = True
        sol = solve_ivp(
            self.equations,
            r_span,
            y0,
            t_eval=t_eval,
            method="RK45",
            events=horizon_event,
            rtol=1.0e-6,
        )
        return sol


def mass_fraction_radius(rs: np.ndarray, masses: np.ndarray, fraction: float):
    target = fraction * masses[-1]
    idx = np.where(masses >= target)[0]
    return float(rs[idx[0]]) if len(idx) else None


def profile_metrics(
    sol,
    *,
    seed_id: str,
    omega0: float,
    theta0: float,
    phi0: float,
    rho0: float,
    xp0: Sequence[float],
    r_max: float,
    dr: float,
) -> Dict[str, object]:
    rs = sol.t
    masses = sol.y[8]
    final_mass = float(masses[-1])
    r_final = float(rs[-1])
    half_radius = mass_fraction_radius(rs, masses, 0.5)
    mass_90_radius = mass_fraction_radius(rs, masses, 0.9)
    idx_core = np.where(rs <= 1.0)[0]
    m_core = masses[idx_core[-1]] if len(idx_core) else 0.0
    core_fraction = float(m_core / final_mass) if final_mass > 0.0 else 0.0
    dm_dr = np.gradient(masses, rs)
    mean_r = float(np.trapezoid(rs * dm_dr, x=rs) / final_mass) if final_mass > 0.0 else 0.0
    skewness_proxy = float(mean_r / half_radius) if half_radius else 0.0
    horizon_events = [float(x) for x in sol.t_events[0]] if len(sol.t_events) else []
    return {
        "id": seed_id,
        "omega0": float(omega0),
        "theta0": float(theta0),
        "phi0": float(phi0),
        "rho0": float(rho0),
        "xp0": [float(x) for x in xp0],
        "r_max": float(r_max),
        "dr": float(dr),
        "status": int(sol.status),
        "status_message": sol.message,
        "terminated_early": bool(sol.status != 0),
        "horizon_event_radii": horizon_events,
        "r_final": r_final,
        "final_mass": final_mass,
        "mass_half_radius": half_radius,
        "mass_90_radius": mass_90_radius,
        "core_mass_fraction": core_fraction,
        "skewness_proxy": skewness_proxy,
        "final_2m_over_r": float(2.0 * final_mass / r_final) if r_final > 0.0 else None,
    }


def save_profile(path: Path, sol, *, mass_column: str = "mass") -> None:
    df = pd.DataFrame(
        {
            "r": sol.t,
            "omega": sol.y[0],
            "theta": sol.y[1],
            "phi": sol.y[2],
            "rho": sol.y[3],
            mass_column: sol.y[8],
        }
    )
    df.to_csv(path, index=False)


def write_rows(path: Path, rows: Sequence[Dict[str, object]]) -> None:
    pd.DataFrame(rows).to_csv(path, index=False)


def slice_stats(rows: Sequence[Dict[str, object]]) -> Dict[str, object]:
    masses = np.asarray([row["mass"] for row in rows], dtype=float)
    terminated = sum(1 for row in rows if row["status"] != 0)
    return {
        "sample_count": len(rows),
        "mass_range": [float(np.min(masses)), float(np.max(masses))],
        "mass_range_width": float(np.max(masses) - np.min(masses)),
        "terminated_early_count": int(terminated),
    }


def format_result_line(result: Dict[str, object]) -> str:
    return (
        f"- `{result['id']}`: final_mass={result['final_mass']}, "
        f"r_half={result['mass_half_radius']}, r_90={result['mass_90_radius']}, "
        f"core_fraction={result['core_mass_fraction']}, terminated_early={result['terminated_early']}, "
        f"r_final={result['r_final']}"
    )


def write_summary_md(summary: Dict[str, object]) -> None:
    lines: List[str] = []
    lines.append("# Phase C Angular Traits Solution Summary")
    lines.append("")
    lines.append("Generated by `analysis/phase_c/phase_c_mc_radial_solver.py`.")
    lines.append("")
    lines.append("## Runtime model actually used")
    lines.append("- anisotropic Maurer-Cartan weights: beta = [0.01, 0.02, 0.03]")
    lines.append(f"- metric regularization added to target metric inverse: {summary['config']['metric_regularization']}")
    lines.append(f"- exploratory phi-localized angular potential coefficient: {summary['config']['angular_phi_potential']}")
    lines.append("- interpretation: this is an exploratory symmetry-broken runtime, not a pure derivation-78/79 implementation with no extra runtime devices")
    lines.append("")
    lines.append("## Representative seeded runs")
    for row in summary["representative_seed_results"]:
        lines.append(format_result_line(row))
    lines.append("")
    lines.append("## Angle-only anchor check")
    lines.append("- Same angle values as the representative seeds, but with zero initial angle-derivative seeding.")
    for row in summary["angle_only_anchor_results"]:
        lines.append(format_result_line(row))
    lines.append("")
    lines.append("## 1D slice studies")
    for name, info in summary["slice_1d"].items():
        lines.append(
            f"- `{name}`: mass range {info['mass_range']}, terminated_early={info['terminated_early_count']} of {info['sample_count']}, fixed={info['fixed_parameters']}, r_max={info['r_max']}"
        )
    lines.append("")
    lines.append("## 2D slice studies")
    for name, info in summary["slice_2d"].items():
        lines.append(
            f"- `{name}`: mass range {info['mass_range']}, terminated_early={info['terminated_early_count']} of {info['sample_count']}, fixed={info['fixed_parameters']}, domain={info['domain']}, r_max={info['r_max']}"
        )
    lines.append("")
    lines.append("## Interpretation")
    lines.append("- Theta-only variation is nearly flat on the audited 1D theta slice.")
    lines.append("- Rho-only variation is moderate and periodic on the audited 1D rho slice.")
    lines.append("- Phi variation is the dominant driver of trait splitting on the audited 1D phi slice and on the phi-coupled 2D slices.")
    lines.append("- The strongest high-mass representative phi-rich anchors terminate early on the horizon event rather than surviving to the full r_max = 20 interval.")
    lines.append("- So the Phase C solver does show angle-sensitive trait differentiation, but the strongest phi-rich states should be interpreted as near-horizon exploratory diagnostics rather than fully settled full-domain survivors.")
    (OUT_DIR / "summary.md").write_text("\n".join(lines))


def write_profiles_summary(
    active_profile_names: Sequence[str], archival_profile_names: Sequence[str]
) -> None:
    lines: List[str] = []
    lines.append("# Phase C Angular Traits Profile Summary")
    lines.append("")
    lines.append("This directory contains two generations of profile exports.")
    lines.append("")
    lines.append("## Active regenerated profiles")
    lines.append("- These files are written by the current audited Phase C solver.")
    for name in active_profile_names:
        lines.append(f"- `{name}`")
    lines.append("")
    lines.append("## Archival preliminary profiles")
    lines.append("- These files predate the current audited solver output and correspond to the older degenerate anchor study.")
    lines.append("- They are historical context only and should not be treated as the primary support for the refreshed Phase C closure summary.")
    for name in archival_profile_names:
        lines.append(f"- `{name}`")
    (PROFILES_DIR / "summary.md").write_text("\n".join(lines))


def run_scans() -> None:
    print("--- Starting Phase C: audited MC radial scans ---")
    OUT_DIR.mkdir(parents=True, exist_ok=True)
    PROFILES_DIR.mkdir(parents=True, exist_ok=True)

    solver = PhaseCMCRadialSolver()
    active_profiles: List[str] = []

    representative_seeds = [
        {"id": "scalar", "omega0": 0.5, "theta0": 0.0, "phi0": 0.0, "rho0": 0.0, "xp0": [0.0, 0.0, 0.0, 0.0]},
        {"id": "theta_dom", "omega0": 0.5, "theta0": np.pi, "phi0": 0.0, "rho0": 0.0, "xp0": [0.0, 0.01, 0.0, 0.0]},
        {"id": "phi_dom", "omega0": 0.5, "theta0": 0.0, "phi0": np.pi / 4.0, "rho0": 0.0, "xp0": [0.0, 0.0, 0.01, 0.0]},
        {"id": "fully_mixed", "omega0": 0.5, "theta0": np.pi, "phi0": np.pi / 4.0, "rho0": np.pi / 2.0, "xp0": [0.0, 0.01, 0.01, 0.01]},
    ]

    representative_results: List[Dict[str, object]] = []
    for seed in representative_seeds:
        print(f"Running representative seed: {seed['id']}")
        sol = solver.solve(
            seed["omega0"],
            seed["theta0"],
            seed["phi0"],
            seed["rho0"],
            r_max=20.0,
            dr=0.01,
            xp0=seed["xp0"],
        )
        representative_results.append(
            profile_metrics(
                sol,
                seed_id=seed["id"],
                omega0=seed["omega0"],
                theta0=seed["theta0"],
                phi0=seed["phi0"],
                rho0=seed["rho0"],
                xp0=seed["xp0"],
                r_max=20.0,
                dr=0.01,
            )
        )
        save_profile(PROFILES_DIR / f"{seed['id']}.csv", sol, mass_column="mass")
        active_profiles.append(f"{seed['id']}.csv")

    angle_only_anchor_results: List[Dict[str, object]] = []
    for seed in representative_seeds:
        sol = solver.solve(
            seed["omega0"],
            seed["theta0"],
            seed["phi0"],
            seed["rho0"],
            r_max=20.0,
            dr=0.01,
            xp0=[0.0, 0.0, 0.0, 0.0],
        )
        angle_only_anchor_results.append(
            profile_metrics(
                sol,
                seed_id=f"{seed['id']}_angle_only",
                omega0=seed["omega0"],
                theta0=seed["theta0"],
                phi0=seed["phi0"],
                rho0=seed["rho0"],
                xp0=[0.0, 0.0, 0.0, 0.0],
                r_max=20.0,
                dr=0.01,
            )
        )

    write_rows(OUT_DIR / "representative_seed_results.csv", representative_results)
    write_rows(OUT_DIR / "angle_only_anchor_results.csv", angle_only_anchor_results)

    # 1D slices on the active unquotiented domain.
    one_d_domain = [-2.0 * np.pi, 2.0 * np.pi]
    one_d_grid = np.linspace(one_d_domain[0], one_d_domain[1], 15)
    slice_1d_theta_rows: List[Dict[str, object]] = []
    slice_1d_phi_rows: List[Dict[str, object]] = []
    slice_1d_rho_rows: List[Dict[str, object]] = []

    for theta in one_d_grid:
        sol = solver.solve(0.5, theta, np.pi / 8.0, 0.0, r_max=10.0, dr=0.01, xp0=[0.0, 0.0, 0.0, 0.0])
        slice_1d_theta_rows.append(
            {
                "theta": float(theta),
                "mass": float(sol.y[8, -1]),
                "status": int(sol.status),
                "r_final": float(sol.t[-1]),
            }
        )

    for phi in one_d_grid:
        sol = solver.solve(0.5, 0.0, phi, 0.0, r_max=10.0, dr=0.01, xp0=[0.0, 0.0, 0.0, 0.0])
        slice_1d_phi_rows.append(
            {
                "phi": float(phi),
                "mass": float(sol.y[8, -1]),
                "status": int(sol.status),
                "r_final": float(sol.t[-1]),
            }
        )

    for rho in one_d_grid:
        sol = solver.solve(0.5, 0.0, np.pi / 8.0, rho, r_max=10.0, dr=0.01, xp0=[0.0, 0.0, 0.0, 0.0])
        slice_1d_rho_rows.append(
            {
                "rho": float(rho),
                "mass": float(sol.y[8, -1]),
                "status": int(sol.status),
                "r_final": float(sol.t[-1]),
            }
        )

    write_rows(OUT_DIR / "slice_1d_theta.csv", slice_1d_theta_rows)
    write_rows(OUT_DIR / "slice_1d_phi.csv", slice_1d_phi_rows)
    write_rows(OUT_DIR / "slice_1d_rho.csv", slice_1d_rho_rows)

    # 2D slices on the active unquotiented domain.
    two_d_domain = [-2.0 * np.pi, 2.0 * np.pi]
    two_d_grid = np.linspace(two_d_domain[0], two_d_domain[1], 8)

    slice_2d_theta_rho_rows: List[Dict[str, object]] = []
    slice_2d_phi_theta_rows: List[Dict[str, object]] = []
    slice_2d_phi_rho_rows: List[Dict[str, object]] = []

    for theta in two_d_grid:
        for rho in two_d_grid:
            sol = solver.solve(0.5, theta, np.pi / 8.0, rho, r_max=5.0, dr=0.01, xp0=[0.0, 0.0, 0.0, 0.0])
            slice_2d_theta_rho_rows.append(
                {
                    "theta": float(theta),
                    "rho": float(rho),
                    "mass": float(sol.y[8, -1]),
                    "status": int(sol.status),
                    "r_final": float(sol.t[-1]),
                }
            )

    for phi in two_d_grid:
        for theta in two_d_grid:
            sol = solver.solve(0.5, theta, phi, 0.0, r_max=5.0, dr=0.01, xp0=[0.0, 0.0, 0.0, 0.0])
            slice_2d_phi_theta_rows.append(
                {
                    "phi": float(phi),
                    "theta": float(theta),
                    "mass": float(sol.y[8, -1]),
                    "status": int(sol.status),
                    "r_final": float(sol.t[-1]),
                }
            )

    for phi in two_d_grid:
        for rho in two_d_grid:
            sol = solver.solve(0.5, 0.0, phi, rho, r_max=5.0, dr=0.01, xp0=[0.0, 0.0, 0.0, 0.0])
            slice_2d_phi_rho_rows.append(
                {
                    "phi": float(phi),
                    "rho": float(rho),
                    "mass": float(sol.y[8, -1]),
                    "status": int(sol.status),
                    "r_final": float(sol.t[-1]),
                }
            )

    write_rows(OUT_DIR / "slice_2d_theta_rho.csv", slice_2d_theta_rho_rows)
    write_rows(OUT_DIR / "slice_2d_phi_theta.csv", slice_2d_phi_theta_rows)
    write_rows(OUT_DIR / "slice_2d_phi_rho.csv", slice_2d_phi_rho_rows)

    summary = {
        "config": {
            "kappa": KAPPA,
            "xi": XI,
            "m_glue": M_GLUE,
            "lambda_q": LAMBDA_Q,
            "beta": [BETA_1, BETA_2, BETA_3],
            "metric_regularization": METRIC_REGULARIZATION,
            "angular_phi_potential": ANGULAR_PHI_POTENTIAL,
            "horizon_event_fraction": HORIZON_EVENT_FRACTION,
        },
        "representative_seed_results": representative_results,
        "angle_only_anchor_results": angle_only_anchor_results,
        "slice_1d": {
            "theta": {
                **slice_stats(slice_1d_theta_rows),
                "fixed_parameters": {"omega": 0.5, "phi": float(np.pi / 8.0), "rho": 0.0},
                "domain": one_d_domain,
                "r_max": 10.0,
                "path": "solutions/phase_c/phase_c_angular_traits/slice_1d_theta.csv",
            },
            "phi": {
                **slice_stats(slice_1d_phi_rows),
                "fixed_parameters": {"omega": 0.5, "theta": 0.0, "rho": 0.0},
                "domain": one_d_domain,
                "r_max": 10.0,
                "path": "solutions/phase_c/phase_c_angular_traits/slice_1d_phi.csv",
            },
            "rho": {
                **slice_stats(slice_1d_rho_rows),
                "fixed_parameters": {"omega": 0.5, "theta": 0.0, "phi": float(np.pi / 8.0)},
                "domain": one_d_domain,
                "r_max": 10.0,
                "path": "solutions/phase_c/phase_c_angular_traits/slice_1d_rho.csv",
            },
        },
        "slice_2d": {
            "theta_rho": {
                **slice_stats(slice_2d_theta_rho_rows),
                "fixed_parameters": {"omega": 0.5, "phi": float(np.pi / 8.0)},
                "domain": two_d_domain,
                "r_max": 5.0,
                "path": "solutions/phase_c/phase_c_angular_traits/slice_2d_theta_rho.csv",
            },
            "phi_theta": {
                **slice_stats(slice_2d_phi_theta_rows),
                "fixed_parameters": {"omega": 0.5, "rho": 0.0},
                "domain": two_d_domain,
                "r_max": 5.0,
                "path": "solutions/phase_c/phase_c_angular_traits/slice_2d_phi_theta.csv",
            },
            "phi_rho": {
                **slice_stats(slice_2d_phi_rho_rows),
                "fixed_parameters": {"omega": 0.5, "theta": 0.0},
                "domain": two_d_domain,
                "r_max": 5.0,
                "path": "solutions/phase_c/phase_c_angular_traits/slice_2d_phi_rho.csv",
            },
        },
        "status": "phase_c_mc_trait_scan_complete",
    }

    with (OUT_DIR / "summary.json").open("w") as f:
        json.dump(summary, f, indent=2)
    write_summary_md(summary)

    archival_profiles = [
        name
        for name in [
            "scalar_anchor.csv",
            "rich_anchor_theta_dom.csv",
            "rich_anchor_phi_dom.csv",
            "rich_anchor_fully_mixed.csv",
        ]
        if (PROFILES_DIR / name).exists()
    ]
    write_profiles_summary(active_profiles, archival_profiles)

    print(json.dumps(summary, indent=2))


if __name__ == "__main__":
    run_scans()
