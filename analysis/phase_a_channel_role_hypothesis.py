#!/usr/bin/env python3
"""Phase A channel-role hypothesis test.

Working hypothesis emerging from earlier Phase A steps:
- omega = pure scale coordinate
- phi = separation / mixing controller for the theta-rho pair
- theta and rho = paired internal directions whose mutual relation is modulated by phi

This script tests that hypothesis on broader regular-domain grids using less
singularity-centric quantities.
"""

from __future__ import annotations

import csv
import json
import math
from pathlib import Path
from typing import Dict, List, Tuple

ROOT = Path(__file__).resolve().parents[1]
OUTDIR = ROOT / "solutions" / "phase_a_channel_role_hypothesis"
OUTDIR.mkdir(parents=True, exist_ok=True)


def components(omega: float, theta: float, phi: float, rho: float) -> Tuple[float, float, float, float]:
    ct, st = math.cos(theta), math.sin(theta)
    cp, sp = math.cos(phi), math.sin(phi)
    cr, sr = math.cos(rho), math.sin(rho)
    a = ct * cp * cr - st * sp * sr
    b = st * cp * cr + ct * sp * sr
    c = ct * sp * cr - st * cp * sr
    d = ct * cp * sr + st * sp * cr
    ew = math.exp(omega)
    return ew * a, ew * b, ew * c, ew * d


def jacobian(omega: float, theta: float, phi: float, rho: float) -> List[List[float]]:
    x0, x1, x2, x3 = components(omega, theta, phi, rho)
    ct, st = math.cos(theta), math.sin(theta)
    cp, sp = math.cos(phi), math.sin(phi)
    cr, sr = math.cos(rho), math.sin(rho)
    ew = math.exp(omega)
    a = ct * cp * cr - st * sp * sr

    da_dt = -st * cp * cr - ct * sp * sr
    db_dt = a
    dc_dt = -st * sp * cr - ct * cp * sr
    dd_dt = -st * cp * sr + ct * sp * cr

    da_dp = -ct * sp * cr - st * cp * sr
    db_dp = -st * sp * cr + ct * cp * sr
    dc_dp = ct * cp * cr + st * sp * sr
    dd_dp = -ct * sp * sr + st * cp * cr

    da_dr = -ct * cp * sr - st * sp * cr
    db_dr = -st * cp * sr + ct * sp * cr
    dc_dr = -ct * sp * sr - st * cp * cr
    dd_dr = a

    return [
        [x0, ew * da_dt, ew * da_dp, ew * da_dr],
        [x1, ew * db_dt, ew * db_dp, ew * db_dr],
        [x2, ew * dc_dt, ew * dc_dp, ew * dc_dr],
        [x3, ew * dd_dt, ew * dd_dp, ew * dd_dr],
    ]


def dot(u: List[float], v: List[float]) -> float:
    return sum(a * b for a, b in zip(u, v))


def norm(v: List[float]) -> float:
    return math.sqrt(dot(v, v))


def metrics(omega: float, theta: float, phi: float, rho: float) -> Dict[str, float]:
    j = jacobian(omega, theta, phi, rho)
    dtheta = [j[r][1] for r in range(4)]
    dphi = [j[r][2] for r in range(4)]
    drho = [j[r][3] for r in range(4)]
    ntheta, nphi, nrho = norm(dtheta), norm(dphi), norm(drho)
    return {
        "norm_dtheta": ntheta,
        "norm_dphi": nphi,
        "norm_drho": nrho,
        "cos_theta_phi": dot(dtheta, dphi) / (ntheta * nphi) if ntheta * nphi else 0.0,
        "cos_theta_rho": dot(dtheta, drho) / (ntheta * nrho) if ntheta * nrho else 0.0,
        "cos_phi_rho": dot(dphi, drho) / (nphi * nrho) if nphi * nrho else 0.0,
    }


def broad_phi_control_scan() -> Dict[str, object]:
    omega = 0.75
    thetas = [k * math.pi / 8.0 for k in range(-16, 17)]
    phis = [k * math.pi / 16.0 for k in range(-32, 33)]
    rhos = [k * math.pi / 8.0 for k in range(-16, 17)]

    rows = []
    max_tp = -1.0
    min_tp = 1.0
    max_abs_phi_pair = 0.0

    for theta in thetas[::4]:
        for rho in rhos[::4]:
            for phi in phis:
                m = metrics(omega, theta, phi, rho)
                max_tp = max(max_tp, m["cos_theta_rho"])
                min_tp = min(min_tp, m["cos_theta_rho"])
                max_abs_phi_pair = max(max_abs_phi_pair, abs(m["cos_theta_phi"]), abs(m["cos_phi_rho"]))
                rows.append({
                    "theta": theta,
                    "phi": phi,
                    "rho": rho,
                    **m,
                })

    with (OUTDIR / "broad_phi_control_scan.csv").open("w", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=list(rows[0].keys()))
        writer.writeheader()
        writer.writerows(rows)

    return {
        "rows": len(rows),
        "max_cos_theta_rho": max_tp,
        "min_cos_theta_rho": min_tp,
        "max_abs_cross_with_phi": max_abs_phi_pair,
    }


def phi_profile_at_fixed_pair() -> List[Dict[str, float]]:
    omega = 0.75
    theta = 1.1
    rho = -0.9
    phis = [k * math.pi / 64.0 for k in range(-128, 129)]
    rows = []
    for phi in phis:
        m = metrics(omega, theta, phi, rho)
        rows.append({"phi": phi, **m})
    with (OUTDIR / "phi_profile_fixed_pair.csv").open("w", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=list(rows[0].keys()))
        writer.writeheader()
        writer.writerows(rows)
    return rows


def theta_rho_independence_scan() -> Dict[str, object]:
    omega = 0.75
    # keep phi away from singular slices
    regular_phis = [-1.2, -0.3, 0.3, 1.2, 2.0]
    values = [k * math.pi / 8.0 for k in range(-16, 17)]
    rows = []
    max_abs_tp = 0.0
    max_abs_pr = 0.0
    max_abs_tr = 0.0
    for phi in regular_phis:
        for theta in values[::2]:
            for rho in values[::2]:
                m = metrics(omega, theta, phi, rho)
                max_abs_tp = max(max_abs_tp, abs(m["cos_theta_phi"]))
                max_abs_pr = max(max_abs_pr, abs(m["cos_phi_rho"]))
                max_abs_tr = max(max_abs_tr, abs(m["cos_theta_rho"]))
                rows.append({"phi": phi, "theta": theta, "rho": rho, **m})
    with (OUTDIR / "theta_rho_independence_scan.csv").open("w", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=list(rows[0].keys()))
        writer.writeheader()
        writer.writerows(rows)
    return {
        "rows": len(rows),
        "max_abs_cos_theta_phi": max_abs_tp,
        "max_abs_cos_phi_rho": max_abs_pr,
        "max_abs_cos_theta_rho": max_abs_tr,
    }


def write_summary(phi_control: Dict[str, object], theta_rho: Dict[str, object], phi_profile: List[Dict[str, float]]) -> None:
    lines = []
    lines.append("# Phase A Channel-Role Hypothesis Summary")
    lines.append("")
    lines.append("Generated by `analysis/phase_a_channel_role_hypothesis.py`.")
    lines.append("")
    lines.append("## Working hypothesis")
    lines.append("- omega = scale")
    lines.append("- phi = separation / mixing controller")
    lines.append("- theta and rho = paired internal directions")
    lines.append("")
    lines.append("## Broad phi-control scan")
    lines.append(f"- rows: {phi_control['rows']}")
    lines.append(f"- max cos(theta,rho): {phi_control['max_cos_theta_rho']}")
    lines.append(f"- min cos(theta,rho): {phi_control['min_cos_theta_rho']}")
    lines.append(f"- max abs cross with phi: {phi_control['max_abs_cross_with_phi']}")
    lines.append("")
    lines.append("## Regular-phi theta/rho scan")
    lines.append(f"- rows: {theta_rho['rows']}")
    lines.append(f"- max abs cos(theta,phi): {theta_rho['max_abs_cos_theta_phi']}")
    lines.append(f"- max abs cos(phi,rho): {theta_rho['max_abs_cos_phi_rho']}")
    lines.append(f"- max abs cos(theta,rho): {theta_rho['max_abs_cos_theta_rho']}")
    lines.append("")
    lines.append("## First interpretation")
    lines.append("- If phi stays nearly orthogonal to both theta and rho while theta-rho overlap ranges across [-1,1], that strongly supports the mediator/separator role hypothesis.")
    lines.append("- If theta-rho overlap spans the full range while phi-cross overlaps remain near zero, then phi is acting less like a peer direction and more like the controller of their relation.")
    (OUTDIR / "summary.md").write_text("\n".join(lines))


def main() -> None:
    phi_control = broad_phi_control_scan()
    phi_profile = phi_profile_at_fixed_pair()
    theta_rho = theta_rho_independence_scan()
    write_summary(phi_control, theta_rho, phi_profile)
    print(json.dumps({
        "phi_control": phi_control,
        "theta_rho": theta_rho,
        "phi_profile_preview": phi_profile[:8],
    }, indent=2))


if __name__ == "__main__":
    main()
