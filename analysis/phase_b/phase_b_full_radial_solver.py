#!/usr/bin/env python3
"""Phase B full radial solver for the fresh-start Khantraction tree.

This runtime is honest about what is and is not reconstructed from the active
project materials.

What is reconstructed directly from the fresh tree:
- the ordered quaternion seed map Q(omega, theta, phi, rho)
- the four-component matter radial equations from derivation 73
- the active scan domain omega > 0, theta/phi/rho in [-2pi, 2pi], no quotienting
- regular-origin seeding in component variables
- branch/continuation scaffolding, diagnostics, and observable extraction hooks

What remains model-dependent in the active tree:
- the exact Einstein-sector closure for the nonminimally coupled xi R |q|^2 term
- the gravitational normalization constant and sign conventions
- the exact asymptotic boundary target for the full four-component branch family

So this solver implements explicit *closure modes* rather than pretending that a
unique physical closure has already been derived in the fresh tree.
The default mode is a provisional but standard Einstein-scalar closure with a
trace-based Ricci estimate and explicit reporting of that choice.
"""

from __future__ import annotations

import argparse
import csv
import json
import math
from dataclasses import asdict, dataclass
from pathlib import Path
from typing import Dict, Iterable, List, Sequence, Tuple

import numpy as np

ROOT = Path(__file__).resolve().parents[1]
OUTDIR = ROOT / "solutions" / "phase_b_full_radial_solver"
OUTDIR.mkdir(parents=True, exist_ok=True)

TWOPI = 2.0 * math.pi


@dataclass
class SolverConfig:
    m_glue: float = 0.1
    lambda_q: float = 0.01
    xi: float = 0.002
    kappa: float = 8.0 * math.pi
    closure_mode: str = "minimal_trace"
    r0: float = 1.0e-3
    r_max: float = 20.0
    dr: float = 0.01
    phi0: float = 0.0
    central_amplitude_base: float = 0.02
    max_field_norm: float = 20.0
    max_abs_component: float = 20.0
    max_mass: float = 10.0
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
class RunResult:
    label: str
    family: str
    source: str
    closure_mode: str
    success: bool
    failure_reason: str
    steps: int
    r_final: float
    horizon_hit: bool
    regularity_ok: bool
    boundary_residual_qnorm: float
    boundary_residual_qprime_norm: float
    final_mass: float
    integrated_abs_ricci: float
    peak_qnorm: float
    peak_imag_to_real_ratio: float
    half_mass_radius: float
    mass_90_radius: float
    ricci_half_radius: float
    ricci_90_radius: float
    settling_radius: float
    core_radius: float
    soft_region_width: float
    omega: float
    theta: float
    phi: float
    rho: float
    a0: float
    b0: float
    c0: float
    d0: float
    provisional: bool
    notes: str


@dataclass
class Profile:
    r: np.ndarray
    y: np.ndarray  # [a,b,c,d,ap,bp,cp,dp,m,phi]
    qnorm: np.ndarray
    ricci: np.ndarray
    energy_density: np.ndarray
    radial_pressure: np.ndarray
    tangential_pressure: np.ndarray


def ordered_quaternion_components(omega: float, theta: float, phi: float, rho: float) -> Tuple[float, float, float, float]:
    cth, sth = math.cos(theta), math.sin(theta)
    cph, sph = math.cos(phi), math.sin(phi)
    crh, srh = math.cos(rho), math.sin(rho)
    scale = math.exp(omega)
    a = scale * (cth * cph * crh - sth * sph * srh)
    b = scale * (sth * cph * crh + cth * sph * srh)
    c = scale * (cth * sph * crh - sth * cph * srh)
    d = scale * (cth * cph * srh + sth * sph * crh)
    return a, b, c, d


def qnorm_sq_from_state(y: np.ndarray) -> float:
    return float(np.dot(y[:4], y[:4]))


def deriv_norm_sq_from_state(y: np.ndarray) -> float:
    return float(np.dot(y[4:8], y[4:8]))


def potential(q2: float, cfg: SolverConfig) -> float:
    return 0.5 * cfg.m_glue ** 2 * q2 + 0.25 * cfg.lambda_q * q2 ** 2


def metric_A(r: float, m: float) -> float:
    return 1.0 - 2.0 * m / r


def stress_terms(r: float, y: np.ndarray, cfg: SolverConfig) -> Tuple[float, float, float, float]:
    a = metric_A(r, y[8])
    q2 = qnorm_sq_from_state(y)
    dq2 = deriv_norm_sq_from_state(y)
    v = potential(q2, cfg)
    # Baseline provisional closure: standard static scalar-multiplet stress tensor.
    rho = 0.5 * a * dq2 + v
    p_r = 0.5 * a * dq2 - v
    p_t = -0.5 * a * dq2 - v
    trace_t = -rho + p_r + 2.0 * p_t
    base_ricci = -cfg.kappa * trace_t

    if cfg.closure_mode == "minimal_trace":
        ricci = base_ricci
    elif cfg.closure_mode == "numerical_ricci_off":
        ricci = 0.0
    elif cfg.closure_mode == "numerical_trace_half":
        ricci = 0.5 * base_ricci
    elif cfg.closure_mode == "numerical_trace_potential_only":
        ricci = 4.0 * cfg.kappa * v
    else:
        raise ValueError(f"unknown closure_mode: {cfg.closure_mode}")
    return rho, p_r, p_t, ricci


def rhs(r: float, y: np.ndarray, cfg: SolverConfig) -> np.ndarray:
    out = np.zeros_like(y)
    a_metric = metric_A(r, y[8])
    if a_metric <= cfg.horizon_margin:
        raise FloatingPointError("horizon_or_metric_breakdown")

    rho, p_r, _p_t, ricci = stress_terms(r, y, cfg)
    m = y[8]
    phi_prime = (m + 4.0 * math.pi * r ** 3 * p_r) / (r * (r - 2.0 * m))
    m_prime = 4.0 * math.pi * r ** 2 * rho
    a_prime = -2.0 * m_prime / r + 2.0 * m / (r ** 2)
    lambda_prime = -a_prime / (2.0 * a_metric)
    damp = 2.0 / r + phi_prime - lambda_prime
    q2 = qnorm_sq_from_state(y)
    eff = cfg.m_glue ** 2 + cfg.lambda_q * q2 - 2.0 * cfg.xi * ricci

    out[:4] = y[4:8]
    out[4:8] = -damp * y[4:8] - (eff / a_metric) * y[:4]
    out[8] = m_prime
    out[9] = phi_prime
    return out


def rk4_step(r: float, y: np.ndarray, h: float, cfg: SolverConfig) -> np.ndarray:
    k1 = rhs(r, y, cfg)
    k2 = rhs(r + 0.5 * h, y + 0.5 * h * k1, cfg)
    k3 = rhs(r + 0.5 * h, y + 0.5 * h * k2, cfg)
    k4 = rhs(r + h, y + h * k3, cfg)
    return y + (h / 6.0) * (k1 + 2.0 * k2 + 2.0 * k3 + k4)


def integrate_seed(seed: SeedSpec, cfg: SolverConfig) -> Tuple[RunResult, Profile | None]:
    raw_a0, raw_b0, raw_c0, raw_d0 = ordered_quaternion_components(seed.omega, seed.theta, seed.phi, seed.rho)
    raw = np.array([raw_a0, raw_b0, raw_c0, raw_d0], dtype=float)
    raw_norm = float(np.linalg.norm(raw))
    direction = raw / max(raw_norm, 1.0e-12)
    central_amp = cfg.central_amplitude_base * math.exp(seed.omega)
    a0, b0, c0, d0 = (central_amp * direction).tolist()
    y = np.array([a0, b0, c0, d0, 0.0, 0.0, 0.0, 0.0, 0.0, cfg.phi0], dtype=float)
    rho0, p_r0, p_t0, ricci0 = stress_terms(cfg.r0, y, cfg)
    y[8] = (4.0 * math.pi / 3.0) * rho0 * cfg.r0 ** 3

    rs: List[float] = [cfg.r0]
    ys: List[np.ndarray] = [y.copy()]
    rhos: List[float] = [rho0]
    prs: List[float] = [p_r0]
    pts: List[float] = [p_t0]
    riccis: List[float] = [ricci0]

    success = True
    failure_reason = ""
    horizon_hit = False

    try:
        steps = 0
        r = cfg.r0
        while r < cfg.r_max and steps < cfg.max_steps:
            a_metric = metric_A(r, y[8])
            if a_metric <= cfg.horizon_margin:
                horizon_hit = True
                success = False
                failure_reason = "horizon_or_metric_breakdown"
                break
            if np.linalg.norm(y[:4]) > cfg.max_field_norm or np.max(np.abs(y[:8])) > cfg.max_abs_component or abs(y[8]) > cfg.max_mass:
                success = False
                failure_reason = "field_or_mass_blowup"
                break
            y = rk4_step(r, y, cfg.dr, cfg)
            r += cfg.dr
            rho_i, pr_i, pt_i, ricci_i = stress_terms(r, y, cfg)
            rs.append(r)
            ys.append(y.copy())
            rhos.append(rho_i)
            prs.append(pr_i)
            pts.append(pt_i)
            riccis.append(ricci_i)
            steps += 1
        else:
            if steps >= cfg.max_steps:
                success = False
                failure_reason = "step_limit_reached"
    except FloatingPointError as exc:
        success = False
        failure_reason = str(exc)
        horizon_hit = "horizon" in failure_reason
    except (OverflowError, ZeroDivisionError, ValueError) as exc:
        success = False
        failure_reason = f"numerical_exception:{type(exc).__name__}"

    r_arr = np.asarray(rs)
    y_arr = np.vstack(ys)
    ricci_arr = np.asarray(riccis)
    rho_arr = np.asarray(rhos)
    pr_arr = np.asarray(prs)
    pt_arr = np.asarray(pts)
    qnorm_arr = np.sqrt(np.sum(y_arr[:, :4] ** 2, axis=1))

    profile = Profile(
        r=r_arr,
        y=y_arr,
        qnorm=qnorm_arr,
        ricci=ricci_arr,
        energy_density=rho_arr,
        radial_pressure=pr_arr,
        tangential_pressure=pt_arr,
    )

    obs = extract_observables(profile, cfg)
    boundary_residual_qnorm = float(qnorm_arr[-1])
    boundary_residual_qprime_norm = float(np.linalg.norm(y_arr[-1, 4:8]))
    regularity_ok = np.all(np.isfinite(y_arr)) and np.all(np.isfinite(ricci_arr)) and not horizon_hit
    if success and (boundary_residual_qnorm > cfg.decay_target or boundary_residual_qprime_norm > cfg.decay_target):
        failure_reason = "asymptotic_decay_not_reached"

    result = RunResult(
        label=seed.label,
        family=seed.family,
        source=seed.source,
        closure_mode=cfg.closure_mode,
        success=success,
        failure_reason=failure_reason,
        steps=len(r_arr) - 1,
        r_final=float(r_arr[-1]),
        horizon_hit=horizon_hit,
        regularity_ok=bool(regularity_ok),
        boundary_residual_qnorm=boundary_residual_qnorm,
        boundary_residual_qprime_norm=boundary_residual_qprime_norm,
        final_mass=float(y_arr[-1, 8]),
        integrated_abs_ricci=obs["integrated_abs_ricci"],
        peak_qnorm=obs["peak_qnorm"],
        peak_imag_to_real_ratio=obs["peak_imag_to_real_ratio"],
        half_mass_radius=obs["half_mass_radius"],
        mass_90_radius=obs["mass_90_radius"],
        ricci_half_radius=obs["ricci_half_radius"],
        ricci_90_radius=obs["ricci_90_radius"],
        settling_radius=obs["settling_radius"],
        core_radius=obs["core_radius"],
        soft_region_width=obs["soft_region_width"],
        omega=seed.omega,
        theta=seed.theta,
        phi=seed.phi,
        rho=seed.rho,
        a0=a0,
        b0=b0,
        c0=c0,
        d0=d0,
        provisional=True,
        notes=(
            f"Uses closure mode '{cfg.closure_mode}' with standard static scalar-multiplet stress bookkeeping and the corresponding configured Ricci-feedback rule. "
            "Ordered-state seeds are mapped into small regular-origin component amplitudes using central_amplitude_base * exp(omega), with the ordered map supplying component direction. "
            "Any non-baseline closure mode should be read as a numerical stress variant, not a uniquely derived fresh-tree closure for the xi R |q|^2 model."
        ),
    )
    return result, profile


def first_radius_for_fraction(r: np.ndarray, density: np.ndarray, fraction: float) -> float:
    weight = 4.0 * math.pi * r ** 2 * density
    cumulative = np.zeros_like(weight)
    cumulative[1:] = np.cumsum(0.5 * (weight[1:] + weight[:-1]) * np.diff(r))
    total = cumulative[-1]
    if total <= 0.0:
        return float("nan")
    target = fraction * total
    idx = int(np.searchsorted(cumulative, target, side="left"))
    idx = min(max(idx, 0), len(r) - 1)
    return float(r[idx])


def extract_observables(profile: Profile, cfg: SolverConfig) -> Dict[str, float]:
    y = profile.y
    a = y[:, 0]
    imag = np.sqrt(np.sum(y[:, 1:4] ** 2, axis=1))
    ratio = imag / np.maximum(np.abs(a), 1.0e-12)
    qnorm = profile.qnorm
    qmax = float(np.max(qnorm))
    peak_idx = int(np.argmax(qnorm))
    core_threshold = 0.9 * qmax
    soft_threshold = 0.2 * qmax
    core_idxs = np.where(qnorm >= core_threshold)[0]
    soft_idxs = np.where(qnorm >= soft_threshold)[0]
    core_radius = float(profile.r[core_idxs[-1]]) if len(core_idxs) else float("nan")
    soft_width = float(profile.r[soft_idxs[-1]] - profile.r[soft_idxs[0]]) if len(soft_idxs) >= 2 else float("nan")

    tail_threshold = max(cfg.decay_target, 0.05 * qmax)
    settle_candidates = np.where(qnorm <= tail_threshold)[0]
    settling_radius = float(profile.r[settle_candidates[0]]) if len(settle_candidates) else float("nan")

    ricci_density = np.abs(profile.ricci)
    return {
        "integrated_abs_ricci": float(np.trapezoid(np.abs(profile.ricci), profile.r)),
        "peak_qnorm": qmax,
        "peak_imag_to_real_ratio": float(np.max(ratio)),
        "half_mass_radius": first_radius_for_fraction(profile.r, np.maximum(profile.energy_density, 0.0), 0.5),
        "mass_90_radius": first_radius_for_fraction(profile.r, np.maximum(profile.energy_density, 0.0), 0.9),
        "ricci_half_radius": first_radius_for_fraction(profile.r, ricci_density, 0.5),
        "ricci_90_radius": first_radius_for_fraction(profile.r, ricci_density, 0.9),
        "settling_radius": settling_radius,
        "core_radius": core_radius,
        "soft_region_width": soft_width,
        "peak_radius": float(profile.r[peak_idx]),
    }


def continuation_seeds() -> List[SeedSpec]:
    scalar = np.array([0.20, 0.0, 0.0, 0.0])
    rich = np.array([0.50, math.pi, -0.5 * math.pi, 0.5 * math.pi])
    seeds: List[SeedSpec] = []
    for idx, t in enumerate(np.linspace(0.0, 1.0, 9)):
        vals = (1.0 - t) * scalar + t * rich
        seeds.append(
            SeedSpec(
                label=f"continuation_{idx:02d}",
                omega=float(vals[0]),
                theta=float(vals[1]),
                phi=float(vals[2]),
                rho=float(vals[3]),
                family="continuation",
                source="linear_ordered_path_scalar_to_rich",
            )
        )
    return seeds


def neighborhood_seeds() -> List[SeedSpec]:
    seeds: List[SeedSpec] = []
    anchor = (0.50, math.pi, -0.5 * math.pi, 0.5 * math.pi)
    deltas = [-0.25, 0.0, 0.25]
    idx = 0
    for dt in deltas:
        for dp in deltas:
            for dr in deltas:
                seeds.append(
                    SeedSpec(
                        label=f"rich_nbhd_{idx:02d}",
                        omega=anchor[0],
                        theta=anchor[1] + dt,
                        phi=anchor[2] + dp,
                        rho=anchor[3] + dr,
                        family="rich_neighborhood",
                        source="ordered_rich_anchor_neighborhood",
                    )
                )
                idx += 1
    return seeds


def coarse_domain_seeds() -> List[SeedSpec]:
    seeds: List[SeedSpec] = []
    omegas = [0.10, 0.35, 0.75]
    angles = [-math.pi, 0.0, math.pi]
    idx = 0
    for omega in omegas:
        for theta in angles:
            for phi in angles:
                for rho in angles:
                    seeds.append(
                        SeedSpec(
                            label=f"coarse_{idx:02d}",
                            omega=omega,
                            theta=theta,
                            phi=phi,
                            rho=rho,
                            family="coarse_domain",
                            source="coarse_active_box_grid",
                        )
                    )
                    idx += 1
    return seeds


def write_profile(label: str, profile: Profile) -> None:
    path = OUTDIR / "profiles" / f"{label}.csv"
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", newline="") as f:
        writer = csv.writer(f)
        writer.writerow([
            "r",
            "a",
            "b",
            "c",
            "d",
            "a_prime",
            "b_prime",
            "c_prime",
            "d_prime",
            "m",
            "Phi",
            "qnorm",
            "ricci",
            "energy_density",
            "radial_pressure",
            "tangential_pressure",
        ])
        for i in range(len(profile.r)):
            writer.writerow([
                profile.r[i],
                *profile.y[i].tolist(),
                profile.qnorm[i],
                profile.ricci[i],
                profile.energy_density[i],
                profile.radial_pressure[i],
                profile.tangential_pressure[i],
            ])


def build_assumption_report(cfg: SolverConfig) -> Dict[str, object]:
    return {
        "active_domain": {
            "omega": {"constraint": "> 0"},
            "theta": [-TWOPI, TWOPI],
            "phi": [-TWOPI, TWOPI],
            "rho": [-TWOPI, TWOPI],
            "quotient_redundancies": False,
        },
        "reconstructed_from_fresh_tree": [
            "ordered quaternion seed map Q(omega, theta, phi, rho) = exp(omega) exp(theta i) exp(phi j) exp(rho k)",
            "four-component matter radial equation template from derivation 73",
            "regular-origin seeding in component variables with q_A'(r0)=0",
            "component-symmetric norm coupling through |q|^2",
            "ordered-state seeds mapped into central component data by separating ordered direction from a small regular-origin amplitude scale anchored to the earlier reduced-profile magnitude",
        ],
        "provisional_closure_choice": {
            "closure_mode": cfg.closure_mode,
            "stress_tensor_model": "standard static scalar-multiplet energy density / pressure formulas",
            "ricci_estimate": "Einstein trace R = -kappa T with T = -rho + p_r + 2 p_t",
            "normalization": {"kappa": cfg.kappa, "Phi_gauge": cfg.phi0, "central_amplitude_base": cfg.central_amplitude_base},
        },
        "not_uniquely_fixed_by_fresh_tree": [
            "full nonminimal-coupling Einstein equations for the xi R |q|^2 term",
            "gravitational normalization / sign conventions beyond the paper-level statements",
            "exact asymptotic boundary conditions for the four-component branch family",
        ],
        "consequence": "Solver outputs are useful continuation/diagnostic data, but any physics claim that depends sensitively on closure should remain provisional until the Einstein sector is derived more tightly.",
    }


def run(cfg: SolverConfig, seed_limit: int | None) -> Dict[str, object]:
    seeds = continuation_seeds() + neighborhood_seeds() + coarse_domain_seeds()
    if seed_limit is not None:
        seeds = seeds[:seed_limit]

    results: List[RunResult] = []
    profiles_written = 0
    for seed in seeds:
        result, profile = integrate_seed(seed, cfg)
        results.append(result)
        if profile is not None and profiles_written < 12:
            write_profile(seed.label, profile)
            profiles_written += 1

    results_path = OUTDIR / "run_results.csv"
    with results_path.open("w", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=list(asdict(results[0]).keys()))
        writer.writeheader()
        for row in results:
            writer.writerow(asdict(row))

    summary = summarize(results, cfg)
    with (OUTDIR / "run_summary.json").open("w") as f:
        json.dump(summary, f, indent=2)

    with (OUTDIR / "assumptions_and_closure.json").open("w") as f:
        json.dump(build_assumption_report(cfg), f, indent=2)

    (OUTDIR / "summary.md").write_text(summary_markdown(summary, cfg))
    return summary


def summarize(results: Sequence[RunResult], cfg: SolverConfig) -> Dict[str, object]:
    success_count = sum(1 for r in results if r.success)
    failure_counts: Dict[str, int] = {}
    for r in results:
        key = r.failure_reason or "completed_without_decay_failure"
        failure_counts[key] = failure_counts.get(key, 0) + 1

    rich = [r for r in results if r.family in {"continuation", "rich_neighborhood"}]
    return {
        "config": asdict(cfg),
        "seed_count": len(results),
        "success_count": success_count,
        "regularity_ok_count": sum(1 for r in results if r.regularity_ok),
        "horizon_hit_count": sum(1 for r in results if r.horizon_hit),
        "failure_counts": failure_counts,
        "boundary_decay_pass_count": sum(
            1
            for r in results
            if r.boundary_residual_qnorm <= cfg.decay_target and r.boundary_residual_qprime_norm <= cfg.decay_target
        ),
        "peak_imag_to_real_ratio_range": [
            float(min(r.peak_imag_to_real_ratio for r in results)),
            float(max(r.peak_imag_to_real_ratio for r in results)),
        ],
        "final_mass_range": [
            float(min(r.final_mass for r in results)),
            float(max(r.final_mass for r in results)),
        ],
        "integrated_abs_ricci_range": [
            float(min(r.integrated_abs_ricci for r in results)),
            float(max(r.integrated_abs_ricci for r in results)),
        ],
        "continuation_track": [
            {
                "label": r.label,
                "omega": r.omega,
                "theta": r.theta,
                "phi": r.phi,
                "rho": r.rho,
                "success": r.success,
                "failure_reason": r.failure_reason,
                "peak_imag_to_real_ratio": r.peak_imag_to_real_ratio,
                "final_mass": r.final_mass,
                "boundary_residual_qnorm": r.boundary_residual_qnorm,
                "boundary_residual_qprime_norm": r.boundary_residual_qprime_norm,
            }
            for r in results
            if r.family == "continuation"
        ],
        "rich_neighborhood_success_fraction": (
            float(sum(1 for r in rich if r.success)) / float(len(rich)) if rich else float("nan")
        ),
        "status": "provisional_closure_runtime_complete",
    }


def summary_markdown(summary: Dict[str, object], cfg: SolverConfig) -> str:
    lines: List[str] = []
    lines.append("# Phase B Full Radial Solver Summary")
    lines.append("")
    lines.append("Generated by `analysis/phase_b/phase_b_full_radial_solver.py`.")
    lines.append("")
    lines.append("## Reconstruction status")
    lines.append("- Matter-side four-component radial equations are implemented from Derivation 73.")
    lines.append(f"- Einstein closure mode used here: `{cfg.closure_mode}`.")
    lines.append("- This closure is explicit and reproducible, but still provisional because the fresh tree does not yet uniquely derive the full xi R |q|^2 Einstein sector.")
    lines.append("")
    lines.append("## Active domain convention")
    lines.append("- omega > 0")
    lines.append("- theta, phi, rho in [-2*pi, 2*pi]")
    lines.append("- no redundancy quotienting")
    lines.append("")
    lines.append("## Run totals")
    lines.append(f"- seeds run: {summary['seed_count']}")
    lines.append(f"- successful integrations: {summary['success_count']}")
    lines.append(f"- regularity-ok integrations: {summary['regularity_ok_count']}")
    lines.append(f"- horizon hits: {summary['horizon_hit_count']}")
    lines.append(f"- boundary decay passes: {summary['boundary_decay_pass_count']}")
    lines.append("")
    lines.append("## Failure reasons")
    for key, value in summary["failure_counts"].items():
        lines.append(f"- {key}: {value}")
    lines.append("")
    lines.append("## Observable ranges")
    lines.append(f"- peak imag/real ratio range: {summary['peak_imag_to_real_ratio_range']}")
    lines.append(f"- final mass range: {summary['final_mass_range']}")
    lines.append(f"- integrated |R| range: {summary['integrated_abs_ricci_range']}")
    lines.append("")
    lines.append("## Interpretation")
    lines.append("- The runtime genuinely integrates a coupled four-component matter-plus-metric system and reports horizons, blowups, and boundary residuals.")
    lines.append("- It supports seeded continuation and neighborhood scans in the active ordered-state box.")
    lines.append("- But decay at finite r_max is usually not achieved automatically, so these are IVP/continuation diagnostics rather than fully validated asymptotically matched solitons.")
    lines.append("- Any branch-coherence claim that depends on the exact Einstein closure remains provisional until the nonminimal-coupling sector is derived more tightly.")
    return "\n".join(lines)


def parse_args() -> argparse.Namespace:
    p = argparse.ArgumentParser()
    p.add_argument("--seed-limit", type=int, default=None)
    p.add_argument("--dr", type=float, default=0.01)
    p.add_argument("--r-max", type=float, default=20.0)
    return p.parse_args()


def main() -> None:
    args = parse_args()
    cfg = SolverConfig(dr=args.dr, r_max=args.r_max)
    summary = run(cfg, args.seed_limit)
    print(json.dumps(summary, indent=2))


if __name__ == "__main__":
    main()
