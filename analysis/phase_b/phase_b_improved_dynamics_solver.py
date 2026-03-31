#!/usr/bin/env python3
"""Phase B improved dynamics solver.

This runtime keeps the existing baseline Phase B component solver untouched and
adds a clearly labeled exploratory comparison runtime in ordered variables
(alpha = [w, theta, phi, rho]).

Why this is the next honest step:
- the current baseline is norm-symmetric in component space, so rich angular
  neighborhoods at fixed omega collapse almost completely in the runtime
  observables.
- the project already has an explicit ordered map and Jacobian geometry from
  derivation 71 / Phase A work.
- pulling the kinetic term back into ordered variables produces a nontrivial
  angular metric with phi-controlled theta-rho mixing.
- an additional small exploratory angular potential is built only from existing
  ordered-map invariants, and is kept fully optional / labeled.

Nothing here is claimed as final derived physics. The exploratory terms are a
motivated next probe of whether the project's own ordered geometry can begin to
resolve angular sectors without destroying family regularity.
"""

from __future__ import annotations

import argparse
import csv
import json
import math
from dataclasses import asdict, dataclass
from pathlib import Path
from typing import Dict, List, Sequence, Tuple

import numpy as np

ROOT = Path(__file__).resolve().parents[1]
BASELINE_SUMMARY_PATH = ROOT / "solutions" / "phase_b_full_radial_solver" / "run_summary.json"
STRESS_SUMMARY_PATH = ROOT / "solutions" / "phase_b_closure_stress_test" / "cross_scenario_summary.json"
OUTDIR = ROOT / "solutions" / "phase_b_improved_dynamics"
OUTDIR.mkdir(parents=True, exist_ok=True)


@dataclass
class OrderedConfig:
    m_glue: float = 0.1
    lambda_q: float = 0.01
    xi: float = 0.002
    kappa: float = 8.0 * math.pi
    r0: float = 1.0e-3
    r_max: float = 20.0
    dr: float = 0.01
    central_amplitude_base: float = 0.02
    phi_metric0: float = 0.0
    closure_mode: str = "minimal_trace"
    dynamics_mode: str = "exploratory_directional"
    angular_eta: float = 0.02
    angular_zeta: float = 0.015
    phi_regularization: float = 1.0e-3
    max_mass: float = 10.0
    max_abs_state: float = 30.0
    horizon_margin: float = 1.0e-6
    decay_target: float = 5.0e-2
    max_steps: int = 500000


@dataclass
class SeedSpec:
    label: str
    omega: float
    theta: float
    phi: float
    rho: float
    family: str
    source: str


@dataclass
class OrderedRunResult:
    label: str
    family: str
    source: str
    dynamics_mode: str
    closure_mode: str
    success: bool
    failure_reason: str
    steps: int
    r_final: float
    horizon_hit: bool
    regularity_ok: bool
    boundary_residual_qnorm: float
    boundary_residual_state_prime_norm: float
    final_mass: float
    integrated_abs_ricci: float
    peak_qnorm: float
    half_mass_radius: float
    mass_90_radius: float
    ricci_half_radius: float
    ricci_90_radius: float
    settling_radius: float
    core_radius: float
    soft_region_width: float
    theta_total_shift: float
    phi_total_shift: float
    rho_total_shift: float
    omega_seed: float
    theta_seed: float
    phi_seed: float
    rho_seed: float
    w0: float
    theta0: float
    phi0: float
    rho0: float
    notes: str


@dataclass
class Profile:
    r: np.ndarray
    y: np.ndarray
    qnorm: np.ndarray
    ricci: np.ndarray
    energy_density: np.ndarray
    radial_pressure: np.ndarray
    tangential_pressure: np.ndarray
    kinetic_density: np.ndarray
    directional_potential: np.ndarray


def continuation_seeds() -> List[SeedSpec]:
    scalar = np.array([0.20, 0.0, 0.0, 0.0])
    rich = np.array([0.50, math.pi, -0.5 * math.pi, 0.5 * math.pi])
    seeds: List[SeedSpec] = []
    for idx, t in enumerate(np.linspace(0.0, 1.0, 9)):
        vals = (1.0 - t) * scalar + t * rich
        seeds.append(SeedSpec(f"continuation_{idx:02d}", float(vals[0]), float(vals[1]), float(vals[2]), float(vals[3]), "continuation", "linear_ordered_path_scalar_to_rich"))
    return seeds


def neighborhood_seeds() -> List[SeedSpec]:
    seeds: List[SeedSpec] = []
    anchor = (0.50, math.pi, -0.5 * math.pi, 0.5 * math.pi)
    deltas = [-0.25, 0.0, 0.25]
    idx = 0
    for dt in deltas:
        for dp in deltas:
            for dr in deltas:
                seeds.append(SeedSpec(f"rich_nbhd_{idx:02d}", anchor[0], anchor[1] + dt, anchor[2] + dp, anchor[3] + dr, "rich_neighborhood", "ordered_rich_anchor_neighborhood"))
                idx += 1
    return seeds


def coarse_reference_seeds() -> List[SeedSpec]:
    return [
        SeedSpec("coarse_scalar_like_00", 0.10, 0.0, 0.0, 0.0, "coarse_reference", "coarse_scalar_reference"),
        SeedSpec("coarse_scalar_like_01", 0.35, 0.0, 0.0, 0.0, "coarse_reference", "coarse_scalar_reference"),
        SeedSpec("coarse_scalar_like_02", 0.75, 0.0, 0.0, 0.0, "coarse_reference", "coarse_scalar_reference"),
    ]


def seed_list() -> List[SeedSpec]:
    return continuation_seeds() + neighborhood_seeds() + coarse_reference_seeds()


def ordered_components(w: float, theta: float, phi: float, rho: float) -> np.ndarray:
    cth, sth = math.cos(theta), math.sin(theta)
    cph, sph = math.cos(phi), math.sin(phi)
    crh, srh = math.cos(rho), math.sin(rho)
    ew = math.exp(w)
    return ew * np.array([
        cth * cph * crh - sth * sph * srh,
        sth * cph * crh + cth * sph * srh,
        cth * sph * crh - sth * cph * srh,
        cth * cph * srh + sth * sph * crh,
    ], dtype=float)


def ordered_metric(w: float, phi: float) -> np.ndarray:
    ew2 = math.exp(2.0 * w)
    s = math.sin(2.0 * phi)
    g = ew2 * np.array([
        [1.0, 0.0, 0.0, 0.0],
        [0.0, 1.0, 0.0, s],
        [0.0, 0.0, 1.0, 0.0],
        [0.0, s, 0.0, 1.0],
    ], dtype=float)
    return g


def ordered_metric_inverse(w: float, phi: float, cfg: OrderedConfig) -> np.ndarray:
    ew2_inv = math.exp(-2.0 * w)
    s = math.sin(2.0 * phi)
    denom = max(1.0 - s * s, cfg.phi_regularization ** 2)
    return ew2_inv * np.array([
        [1.0, 0.0, 0.0, 0.0],
        [0.0, 1.0 / denom, 0.0, -s / denom],
        [0.0, 0.0, 1.0, 0.0],
        [0.0, -s / denom, 0.0, 1.0 / denom],
    ], dtype=float)


def metric_derivatives(w: float, phi: float) -> Dict[int, np.ndarray]:
    g = ordered_metric(w, phi)
    dg_w = 2.0 * g
    ew2 = math.exp(2.0 * w)
    c = math.cos(2.0 * phi)
    dg_phi = ew2 * np.array([
        [0.0, 0.0, 0.0, 0.0],
        [0.0, 0.0, 0.0, 2.0 * c],
        [0.0, 0.0, 0.0, 0.0],
        [0.0, 2.0 * c, 0.0, 0.0],
    ], dtype=float)
    zero = np.zeros((4, 4), dtype=float)
    return {0: dg_w, 1: zero, 2: dg_phi, 3: zero}


def christoffel(w: float, phi: float, cfg: OrderedConfig) -> np.ndarray:
    g_inv = ordered_metric_inverse(w, phi, cfg)
    dgs = metric_derivatives(w, phi)
    gamma = np.zeros((4, 4, 4), dtype=float)
    for i in range(4):
        for j in range(4):
            for k in range(4):
                val = 0.0
                for ell in range(4):
                    val += g_inv[i, ell] * (dgs[j][ell, k] + dgs[k][ell, j] - dgs[ell][j, k])
                gamma[i, j, k] = 0.5 * val
    return gamma


def norm_potential_and_grad(w: float, cfg: OrderedConfig) -> Tuple[float, np.ndarray]:
    e2w = math.exp(2.0 * w)
    e4w = e2w * e2w
    v = 0.5 * cfg.m_glue ** 2 * e2w + 0.25 * cfg.lambda_q * e4w
    grad = np.array([cfg.m_glue ** 2 * e2w + cfg.lambda_q * e4w, 0.0, 0.0, 0.0], dtype=float)
    return v, grad


def directional_potential_and_grad(alpha: np.ndarray, cfg: OrderedConfig) -> Tuple[float, np.ndarray]:
    if cfg.dynamics_mode != "exploratory_directional":
        return 0.0, np.zeros(4, dtype=float)
    w, theta, phi, rho = alpha
    e2w = math.exp(2.0 * w)
    delta = theta - rho
    s2 = math.sin(2.0 * phi)
    c2 = math.cos(2.0 * phi)
    sep_term = 0.5 * cfg.angular_eta * e2w * (1.0 - c2 * c2)
    pair_term = 0.5 * cfg.angular_zeta * e2w * (1.0 - math.cos(delta)) * (1.0 + c2)
    v = sep_term + pair_term
    grad = np.zeros(4, dtype=float)
    grad[0] = 2.0 * v
    grad[1] = 0.5 * cfg.angular_zeta * e2w * math.sin(delta) * (1.0 + c2)
    grad[2] = e2w * (cfg.angular_eta * 2.0 * s2 * c2 - cfg.angular_zeta * (1.0 - math.cos(delta)) * s2)
    grad[3] = -grad[1]
    return v, grad


def kinetic_density(alpha: np.ndarray, alpha_p: np.ndarray) -> float:
    g = ordered_metric(alpha[0], alpha[2])
    return float(alpha_p @ g @ alpha_p)


def stress_terms(alpha: np.ndarray, alpha_p: np.ndarray, r: float, mass: float, cfg: OrderedConfig) -> Tuple[float, float, float, float, float]:
    a_metric = 1.0 - 2.0 * mass / r
    kin = kinetic_density(alpha, alpha_p)
    v_norm, _ = norm_potential_and_grad(alpha[0], cfg)
    v_dir, _ = directional_potential_and_grad(alpha, cfg)
    v_total = v_norm + v_dir
    rho = 0.5 * a_metric * kin + v_total
    p_r = 0.5 * a_metric * kin - v_total
    p_t = -0.5 * a_metric * kin - v_total
    trace_t = -rho + p_r + 2.0 * p_t
    ricci = -cfg.kappa * trace_t if cfg.closure_mode == "minimal_trace" else 0.0
    return rho, p_r, p_t, ricci, v_dir


def rhs(r: float, y: np.ndarray, cfg: OrderedConfig) -> np.ndarray:
    alpha = y[:4]
    alpha_p = y[4:8]
    mass = y[8]
    a_metric = 1.0 - 2.0 * mass / r
    if a_metric <= cfg.horizon_margin:
        raise FloatingPointError("horizon_or_metric_breakdown")

    rho, p_r, _p_t, ricci, _vdir = stress_terms(alpha, alpha_p, r, mass, cfg)
    phi_prime = (mass + 4.0 * math.pi * r ** 3 * p_r) / (r * (r - 2.0 * mass))
    m_prime = 4.0 * math.pi * r ** 2 * rho
    a_prime = -2.0 * m_prime / r + 2.0 * mass / (r ** 2)
    lambda_prime = -a_prime / (2.0 * a_metric)
    damp = 2.0 / r + phi_prime - lambda_prime

    gamma = christoffel(alpha[0], alpha[2], cfg)
    g_inv = ordered_metric_inverse(alpha[0], alpha[2], cfg)
    _vnorm, grad_norm = norm_potential_and_grad(alpha[0], cfg)
    _vd, grad_dir = directional_potential_and_grad(alpha, cfg)
    grad_total = grad_norm + grad_dir
    grad_total[0] += -2.0 * cfg.xi * ricci * math.exp(2.0 * alpha[0])

    accel = np.zeros(4, dtype=float)
    for i in range(4):
        quad = 0.0
        for j in range(4):
            for k in range(4):
                quad += gamma[i, j, k] * alpha_p[j] * alpha_p[k]
        accel[i] = -damp * alpha_p[i] - quad - float((g_inv @ grad_total)[i] / a_metric)

    out = np.zeros_like(y)
    out[:4] = alpha_p
    out[4:8] = accel
    out[8] = m_prime
    out[9] = phi_prime
    return out


def rk4_step(r: float, y: np.ndarray, h: float, cfg: OrderedConfig) -> np.ndarray:
    k1 = rhs(r, y, cfg)
    k2 = rhs(r + 0.5 * h, y + 0.5 * h * k1, cfg)
    k3 = rhs(r + 0.5 * h, y + 0.5 * h * k2, cfg)
    k4 = rhs(r + h, y + h * k3, cfg)
    return y + (h / 6.0) * (k1 + 2.0 * k2 + 2.0 * k3 + k4)


def first_radius_for_fraction(r: np.ndarray, density: np.ndarray, fraction: float) -> float:
    weight = 4.0 * math.pi * r ** 2 * density
    cumulative = np.zeros_like(weight)
    cumulative[1:] = np.cumsum(0.5 * (weight[1:] + weight[:-1]) * np.diff(r))
    total = cumulative[-1]
    if total <= 0.0:
        return float("nan")
    idx = int(np.searchsorted(cumulative, fraction * total, side="left"))
    idx = min(max(idx, 0), len(r) - 1)
    return float(r[idx])


def extract_observables(profile: Profile, cfg: OrderedConfig, y0: np.ndarray) -> Dict[str, float]:
    qnorm = profile.qnorm
    qmax = float(np.max(qnorm))
    core_idxs = np.where(qnorm >= 0.9 * qmax)[0]
    soft_idxs = np.where(qnorm >= 0.2 * qmax)[0]
    settling = np.where(qnorm <= max(cfg.decay_target, 0.05 * qmax))[0]
    y = profile.y
    return {
        "integrated_abs_ricci": float(np.trapezoid(np.abs(profile.ricci), profile.r)),
        "peak_qnorm": qmax,
        "half_mass_radius": first_radius_for_fraction(profile.r, np.maximum(profile.energy_density, 0.0), 0.5),
        "mass_90_radius": first_radius_for_fraction(profile.r, np.maximum(profile.energy_density, 0.0), 0.9),
        "ricci_half_radius": first_radius_for_fraction(profile.r, np.abs(profile.ricci), 0.5),
        "ricci_90_radius": first_radius_for_fraction(profile.r, np.abs(profile.ricci), 0.9),
        "settling_radius": float(profile.r[settling[0]]) if len(settling) else float("nan"),
        "core_radius": float(profile.r[core_idxs[-1]]) if len(core_idxs) else float("nan"),
        "soft_region_width": float(profile.r[soft_idxs[-1]] - profile.r[soft_idxs[0]]) if len(soft_idxs) >= 2 else float("nan"),
        "theta_total_shift": float(y[-1, 1] - y0[1]),
        "phi_total_shift": float(y[-1, 2] - y0[2]),
        "rho_total_shift": float(y[-1, 3] - y0[3]),
    }


def integrate_seed(seed: SeedSpec, cfg: OrderedConfig) -> Tuple[OrderedRunResult, Profile]:
    w0 = math.log(cfg.central_amplitude_base) + seed.omega
    y = np.array([w0, seed.theta, seed.phi, seed.rho, 0.0, 0.0, 0.0, 0.0, 0.0, cfg.phi_metric0], dtype=float)
    rho0, pr0, pt0, ricci0, vdir0 = stress_terms(y[:4], y[4:8], cfg.r0, y[8], cfg)
    y[8] = (4.0 * math.pi / 3.0) * rho0 * cfg.r0 ** 3

    rs = [cfg.r0]
    ys = [y.copy()]
    rhos = [rho0]
    prs = [pr0]
    pts = [pt0]
    riccis = [ricci0]
    kinds = [kinetic_density(y[:4], y[4:8])]
    vdirs = [vdir0]
    success = True
    failure_reason = ""
    horizon_hit = False

    try:
        r = cfg.r0
        steps = 0
        while r < cfg.r_max and steps < cfg.max_steps:
            if (1.0 - 2.0 * y[8] / r) <= cfg.horizon_margin:
                success = False
                horizon_hit = True
                failure_reason = "horizon_or_metric_breakdown"
                break
            if np.max(np.abs(y[:8])) > cfg.max_abs_state or abs(y[8]) > cfg.max_mass:
                success = False
                failure_reason = "state_or_mass_blowup"
                break
            y = rk4_step(r, y, cfg.dr, cfg)
            r += cfg.dr
            rho_i, pr_i, pt_i, ricci_i, vdir_i = stress_terms(y[:4], y[4:8], r, y[8], cfg)
            rs.append(r)
            ys.append(y.copy())
            rhos.append(rho_i)
            prs.append(pr_i)
            pts.append(pt_i)
            riccis.append(ricci_i)
            kinds.append(kinetic_density(y[:4], y[4:8]))
            vdirs.append(vdir_i)
            steps += 1
        else:
            if steps >= cfg.max_steps:
                success = False
                failure_reason = "step_limit_reached"
    except FloatingPointError as exc:
        success = False
        failure_reason = str(exc)
        horizon_hit = "horizon" in failure_reason
    except (OverflowError, ZeroDivisionError, ValueError, np.linalg.LinAlgError) as exc:
        success = False
        failure_reason = f"numerical_exception:{type(exc).__name__}"

    r_arr = np.asarray(rs)
    y_arr = np.vstack(ys)
    qnorm = np.exp(y_arr[:, 0])
    profile = Profile(
        r=r_arr,
        y=y_arr,
        qnorm=qnorm,
        ricci=np.asarray(riccis),
        energy_density=np.asarray(rhos),
        radial_pressure=np.asarray(prs),
        tangential_pressure=np.asarray(pts),
        kinetic_density=np.asarray(kinds),
        directional_potential=np.asarray(vdirs),
    )
    obs = extract_observables(profile, cfg, ys[0])
    boundary_q = float(qnorm[-1])
    boundary_dp = float(np.linalg.norm(y_arr[-1, 4:8]))
    regularity_ok = bool(np.all(np.isfinite(y_arr)) and np.all(np.isfinite(profile.ricci)) and not horizon_hit)
    note = (
        "Pullback ordered-variable runtime using the exact Jacobian-induced metric G on (w,theta,phi,rho). "
        f"dynamics_mode={cfg.dynamics_mode}. exploratory_directional adds small angular potentials built from cos(2phi), sin(2phi), and theta-rho separation; baseline_pullback keeps only the norm potential."
    )
    result = OrderedRunResult(
        label=seed.label,
        family=seed.family,
        source=seed.source,
        dynamics_mode=cfg.dynamics_mode,
        closure_mode=cfg.closure_mode,
        success=success,
        failure_reason=failure_reason,
        steps=len(r_arr) - 1,
        r_final=float(r_arr[-1]),
        horizon_hit=horizon_hit,
        regularity_ok=regularity_ok,
        boundary_residual_qnorm=boundary_q,
        boundary_residual_state_prime_norm=boundary_dp,
        final_mass=float(y_arr[-1, 8]),
        integrated_abs_ricci=obs["integrated_abs_ricci"],
        peak_qnorm=obs["peak_qnorm"],
        half_mass_radius=obs["half_mass_radius"],
        mass_90_radius=obs["mass_90_radius"],
        ricci_half_radius=obs["ricci_half_radius"],
        ricci_90_radius=obs["ricci_90_radius"],
        settling_radius=obs["settling_radius"],
        core_radius=obs["core_radius"],
        soft_region_width=obs["soft_region_width"],
        theta_total_shift=obs["theta_total_shift"],
        phi_total_shift=obs["phi_total_shift"],
        rho_total_shift=obs["rho_total_shift"],
        omega_seed=seed.omega,
        theta_seed=seed.theta,
        phi_seed=seed.phi,
        rho_seed=seed.rho,
        w0=w0,
        theta0=seed.theta,
        phi0=seed.phi,
        rho0=seed.rho,
        notes=note,
    )
    return result, profile


def write_profile(subdir: Path, label: str, profile: Profile) -> None:
    path = subdir / "profiles" / f"{label}.csv"
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", newline="") as f:
        writer = csv.writer(f)
        writer.writerow(["r", "w", "theta", "phi", "rho", "w_prime", "theta_prime", "phi_prime", "rho_prime", "m", "Phi", "qnorm", "ricci", "energy_density", "radial_pressure", "tangential_pressure", "kinetic_density", "directional_potential"])
        for i in range(len(profile.r)):
            writer.writerow([
                profile.r[i], *profile.y[i].tolist(), profile.qnorm[i], profile.ricci[i], profile.energy_density[i], profile.radial_pressure[i], profile.tangential_pressure[i], profile.kinetic_density[i], profile.directional_potential[i]
            ])


def summarize(rows: Sequence[OrderedRunResult]) -> Dict[str, object]:
    def rng(vals: Sequence[float]) -> List[float]:
        return [float(min(vals)), float(max(vals))]

    rich = [r for r in rows if r.family == "rich_neighborhood"]
    cont = [r for r in rows if r.family == "continuation"]
    rich_mass_spread = max(r.final_mass for r in rich) - min(r.final_mass for r in rich)
    rich_ricci_spread = max(r.integrated_abs_ricci for r in rich) - min(r.integrated_abs_ricci for r in rich)
    rich_theta_shift = max(abs(r.theta_total_shift) for r in rich)
    rich_phi_shift = max(abs(r.phi_total_shift) for r in rich)
    rich_rho_shift = max(abs(r.rho_total_shift) for r in rich)
    cont_masses = [r.final_mass for r in cont]
    monotone = all(cont_masses[i + 1] >= cont_masses[i] - 1.0e-12 for i in range(len(cont_masses) - 1))
    return {
        "seed_count": len(rows),
        "success_count": sum(1 for r in rows if r.success),
        "regularity_ok_count": sum(1 for r in rows if r.regularity_ok),
        "horizon_hit_count": sum(1 for r in rows if r.horizon_hit),
        "final_mass_range": rng([r.final_mass for r in rows]),
        "integrated_abs_ricci_range": rng([r.integrated_abs_ricci for r in rows]),
        "rich_neighborhood_final_mass_spread": float(rich_mass_spread),
        "rich_neighborhood_integrated_abs_ricci_spread": float(rich_ricci_spread),
        "rich_neighborhood_max_abs_theta_shift": float(rich_theta_shift),
        "rich_neighborhood_max_abs_phi_shift": float(rich_phi_shift),
        "rich_neighborhood_max_abs_rho_shift": float(rich_rho_shift),
        "continuation_final_mass_monotone": monotone,
        "continuation_track": [{"label": r.label, "final_mass": r.final_mass, "theta_total_shift": r.theta_total_shift, "phi_total_shift": r.phi_total_shift, "rho_total_shift": r.rho_total_shift} for r in cont],
    }


def run_ordered_mode(cfg: OrderedConfig, subname: str) -> Dict[str, object]:
    subdir = OUTDIR / subname
    subdir.mkdir(parents=True, exist_ok=True)
    rows: List[OrderedRunResult] = []
    for idx, seed in enumerate(seed_list()):
        row, profile = integrate_seed(seed, cfg)
        rows.append(row)
        if idx < 12:
            write_profile(subdir, seed.label, profile)
    with (subdir / "run_results.csv").open("w", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=list(asdict(rows[0]).keys()))
        writer.writeheader()
        for row in rows:
            writer.writerow(asdict(row))
    summary = {"config": asdict(cfg), **summarize(rows)}
    with (subdir / "run_summary.json").open("w") as f:
        json.dump(summary, f, indent=2)
    return summary


def run_baseline_reference() -> Dict[str, object]:
    baseline_summary = json.loads(BASELINE_SUMMARY_PATH.read_text())
    stress_summary = json.loads(STRESS_SUMMARY_PATH.read_text())
    return {
        "baseline_run_summary": baseline_summary,
        "stress_cross_summary": stress_summary,
    }


def build_comparison(baseline: Dict[str, object], pullback: Dict[str, object], exploratory: Dict[str, object]) -> Dict[str, object]:
    stress_baseline = baseline["stress_cross_summary"]["baseline_reference"]
    base_rich_mass_spread = stress_baseline["rich_neighborhood_final_mass"]["range"]
    base_rich_ricci_spread = stress_baseline["rich_neighborhood_integrated_abs_ricci"]["range"]
    return {
        "baseline_component_reference": {
            "solver": "analysis/phase_b/phase_b_full_radial_solver.py",
            "rich_neighborhood_final_mass_spread": base_rich_mass_spread,
            "rich_neighborhood_integrated_abs_ricci_spread": base_rich_ricci_spread,
            "summary_seed_count": baseline["baseline_run_summary"].get("seed_count"),
            "summary_success_count": baseline["baseline_run_summary"].get("success_count"),
        },
        "baseline_pullback": {
            "rich_neighborhood_final_mass_spread": pullback["rich_neighborhood_final_mass_spread"],
            "rich_neighborhood_integrated_abs_ricci_spread": pullback["rich_neighborhood_integrated_abs_ricci_spread"],
            "continuation_final_mass_monotone": pullback["continuation_final_mass_monotone"],
            "rich_neighborhood_max_abs_phi_shift": pullback["rich_neighborhood_max_abs_phi_shift"],
        },
        "exploratory_directional": {
            "rich_neighborhood_final_mass_spread": exploratory["rich_neighborhood_final_mass_spread"],
            "rich_neighborhood_integrated_abs_ricci_spread": exploratory["rich_neighborhood_integrated_abs_ricci_spread"],
            "continuation_final_mass_monotone": exploratory["continuation_final_mass_monotone"],
            "rich_neighborhood_max_abs_phi_shift": exploratory["rich_neighborhood_max_abs_phi_shift"],
        },
        "spread_ratios_vs_component_baseline": {
            "baseline_pullback_mass_spread_ratio": float(pullback["rich_neighborhood_final_mass_spread"] / base_rich_mass_spread) if base_rich_mass_spread else float("nan"),
            "exploratory_directional_mass_spread_ratio": float(exploratory["rich_neighborhood_final_mass_spread"] / base_rich_mass_spread) if base_rich_mass_spread else float("nan"),
            "baseline_pullback_ricci_spread_ratio": float(pullback["rich_neighborhood_integrated_abs_ricci_spread"] / base_rich_ricci_spread) if base_rich_ricci_spread else float("nan"),
            "exploratory_directional_ricci_spread_ratio": float(exploratory["rich_neighborhood_integrated_abs_ricci_spread"] / base_rich_ricci_spread) if base_rich_ricci_spread else float("nan"),
        },
    }


def write_summary_md(comp: Dict[str, object], pullback: Dict[str, object], exploratory: Dict[str, object]) -> None:
    lines: List[str] = []
    lines.append("# Phase B Improved Dynamics Comparison")
    lines.append("")
    lines.append("Generated by `analysis/phase_b/phase_b_improved_dynamics_solver.py`.")
    lines.append("")
    lines.append("## Modes")
    lines.append("- component baseline = existing `analysis/phase_b/phase_b_full_radial_solver.py`")
    lines.append("- baseline_pullback = ordered-variable runtime with exact pullback kinetic metric only")
    lines.append("- exploratory_directional = baseline_pullback plus small angular potential from ordered-map invariants")
    lines.append("")
    lines.append("## Rich-neighborhood angular differentiation")
    lines.append(f"- component baseline mass spread: {comp['baseline_component_reference']['rich_neighborhood_final_mass_spread']}")
    lines.append(f"- baseline_pullback mass spread: {comp['baseline_pullback']['rich_neighborhood_final_mass_spread']}")
    lines.append(f"- exploratory_directional mass spread: {comp['exploratory_directional']['rich_neighborhood_final_mass_spread']}")
    lines.append(f"- component baseline |R| spread: {comp['baseline_component_reference']['rich_neighborhood_integrated_abs_ricci_spread']}")
    lines.append(f"- baseline_pullback |R| spread: {comp['baseline_pullback']['rich_neighborhood_integrated_abs_ricci_spread']}")
    lines.append(f"- exploratory_directional |R| spread: {comp['exploratory_directional']['rich_neighborhood_integrated_abs_ricci_spread']}")
    lines.append("")
    lines.append("## Continuation regularity")
    lines.append(f"- baseline_pullback continuation final mass monotone: {comp['baseline_pullback']['continuation_final_mass_monotone']}")
    lines.append(f"- exploratory_directional continuation final mass monotone: {comp['exploratory_directional']['continuation_final_mass_monotone']}")
    lines.append("")
    lines.append("## Interpretation")
    lines.append("- If baseline_pullback remains nearly degenerate, then simply rewriting the kinetic term in ordered coordinates is not enough.")
    lines.append("- If exploratory_directional shows a much larger rich-neighborhood spread while remaining regular and monotone on continuation seeds, then the project has an honest next runtime that begins to resolve angular sectors without claiming fully derived final physics.")
    (OUTDIR / "summary.md").write_text("\n".join(lines))


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--r-max", type=float, default=20.0)
    parser.add_argument("--dr", type=float, default=0.01)
    args = parser.parse_args()

    baseline_summary = run_baseline_reference()

    pullback_cfg = OrderedConfig(r_max=args.r_max, dr=args.dr, dynamics_mode="baseline_pullback", angular_eta=0.0, angular_zeta=0.0)
    exploratory_cfg = OrderedConfig(r_max=args.r_max, dr=args.dr, dynamics_mode="exploratory_directional", angular_eta=0.02, angular_zeta=0.015)

    pullback_summary = run_ordered_mode(pullback_cfg, "baseline_pullback")
    exploratory_summary = run_ordered_mode(exploratory_cfg, "exploratory_directional")
    comparison = build_comparison(baseline_summary, pullback_summary, exploratory_summary)

    with (OUTDIR / "comparison_summary.json").open("w") as f:
        json.dump(comparison, f, indent=2)
    write_summary_md(comparison, pullback_summary, exploratory_summary)

    print(json.dumps({
        "baseline_component": comparison["baseline_component_reference"],
        "baseline_pullback": pullback_summary,
        "exploratory_directional": exploratory_summary,
        "comparison": comparison,
    }, indent=2))


if __name__ == "__main__":
    main()
