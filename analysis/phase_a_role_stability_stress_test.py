#!/usr/bin/env python3
"""Phase A role-stability stress test.

Purpose:
Stress-test the emerging Phase A role picture across a wider positive omega range
and a richer sample of angle values in the active domain.

Hypothesis under test:
- omega controls scale magnitude only
- phi remains nearly orthogonal to both theta and rho
- theta-rho overlap is the relation that phi modulates
"""

from __future__ import annotations

import csv
import json
import math
from pathlib import Path
from typing import Dict, List, Tuple

ROOT = Path(__file__).resolve().parents[1]
OUTDIR = ROOT / "solutions" / "phase_a_role_stability_stress_test"
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


def stress_scan() -> Dict[str, object]:
    omegas = [0.1, 0.25, 0.75, 1.5, 2.5]
    thetas = [k * math.pi / 8.0 for k in range(-16, 17)]
    phis = [k * math.pi / 16.0 for k in range(-32, 33)]
    rhos = [k * math.pi / 8.0 for k in range(-16, 17)]

    rows = []
    max_norm_diff = 0.0
    max_abs_theta_phi = 0.0
    max_abs_phi_rho = 0.0
    max_abs_theta_rho = 0.0
    min_theta_rho = 1.0
    max_theta_rho = -1.0

    for omega in omegas:
        for theta in thetas[::4]:
            for phi in phis:
                for rho in rhos[::4]:
                    m = metrics(omega, theta, phi, rho)
                    nd = [m["norm_dtheta"], m["norm_dphi"], m["norm_drho"]]
                    norm_diff = max(nd) - min(nd)
                    max_norm_diff = max(max_norm_diff, norm_diff)
                    max_abs_theta_phi = max(max_abs_theta_phi, abs(m["cos_theta_phi"]))
                    max_abs_phi_rho = max(max_abs_phi_rho, abs(m["cos_phi_rho"]))
                    max_abs_theta_rho = max(max_abs_theta_rho, abs(m["cos_theta_rho"]))
                    min_theta_rho = min(min_theta_rho, m["cos_theta_rho"])
                    max_theta_rho = max(max_theta_rho, m["cos_theta_rho"])
                    rows.append({"omega": omega, "theta": theta, "phi": phi, "rho": rho, **m})

    with (OUTDIR / "stress_scan.csv").open("w", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=list(rows[0].keys()))
        writer.writeheader()
        writer.writerows(rows)

    summary = {
        "rows": len(rows),
        "omega_values": omegas,
        "max_norm_difference": max_norm_diff,
        "max_abs_cos_theta_phi": max_abs_theta_phi,
        "max_abs_cos_phi_rho": max_abs_phi_rho,
        "max_abs_cos_theta_rho": max_abs_theta_rho,
        "min_cos_theta_rho": min_theta_rho,
        "max_cos_theta_rho": max_theta_rho,
    }
    with (OUTDIR / "stress_summary.json").open("w") as f:
        json.dump(summary, f, indent=2)
    return summary


def omega_scaling_check() -> List[Dict[str, float]]:
    theta, phi, rho = 1.1, 0.3, -0.9
    omegas = [0.1, 0.25, 0.5, 0.75, 1.0, 1.5, 2.0, 2.5]
    rows = []
    for omega in omegas:
        m = metrics(omega, theta, phi, rho)
        rows.append({
            "omega": omega,
            **m,
            "expected_norm": math.exp(omega),
            "norm_error_theta": abs(m["norm_dtheta"] - math.exp(omega)),
            "norm_error_phi": abs(m["norm_dphi"] - math.exp(omega)),
            "norm_error_rho": abs(m["norm_drho"] - math.exp(omega)),
        })
    with (OUTDIR / "omega_scaling_check.csv").open("w", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=list(rows[0].keys()))
        writer.writeheader()
        writer.writerows(rows)
    return rows


def write_summary(summary: Dict[str, object], omega_rows: List[Dict[str, float]]) -> None:
    lines = []
    lines.append("# Phase A Role-Stability Stress Test Summary")
    lines.append("")
    lines.append("Generated by `analysis/phase_a_role_stability_stress_test.py`.")
    lines.append("")
    lines.append("## Stress-scan results")
    lines.append(f"- rows: {summary['rows']}")
    lines.append(f"- omega values: {summary['omega_values']}")
    lines.append(f"- max norm difference across channels: {summary['max_norm_difference']}")
    lines.append(f"- max abs cos(theta,phi): {summary['max_abs_cos_theta_phi']}")
    lines.append(f"- max abs cos(phi,rho): {summary['max_abs_cos_phi_rho']}")
    lines.append(f"- max abs cos(theta,rho): {summary['max_abs_cos_theta_rho']}")
    lines.append(f"- min cos(theta,rho): {summary['min_cos_theta_rho']}")
    lines.append(f"- max cos(theta,rho): {summary['max_cos_theta_rho']}")
    lines.append("")
    lines.append("## Omega scaling check")
    for row in omega_rows:
        lines.append(f"- omega={row['omega']:.2f}: norms=({row['norm_dtheta']:.6f},{row['norm_dphi']:.6f},{row['norm_drho']:.6f}), expected={row['expected_norm']:.6f}")
    lines.append("")
    lines.append("## Interpretation")
    lines.append("- If cross overlaps with phi remain near zero across the stress scan while theta-rho spans [-1,1], the role picture is highly stable.")
    lines.append("- If channel norms continue to match e^omega, then omega is behaving as a pure scale coordinate rather than an angle-structure modifier.")
    (OUTDIR / "summary.md").write_text("\n".join(lines))


def main() -> None:
    summary = stress_scan()
    omega_rows = omega_scaling_check()
    write_summary(summary, omega_rows)
    print(json.dumps({"summary": summary, "omega_preview": omega_rows}, indent=2))


if __name__ == "__main__":
    main()
