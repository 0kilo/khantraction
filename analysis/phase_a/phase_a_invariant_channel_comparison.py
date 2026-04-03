#!/usr/bin/env python3
"""Phase A invariant-ish channel comparison.

Goal:
Compare theta, phi, rho using quantities less tied to raw coordinate-chart
singularity language. We use Jacobian-column Gram data and singular values,
which still come from the chart but are more geometric than a raw determinant
alone.

Active domain:
- omega > 0
- theta, phi, rho in [-2*pi, 2*pi]
- no redundancy quotienting
"""

from __future__ import annotations

import csv
import json
import math
from pathlib import Path
from typing import Dict, List, Tuple

ROOT = Path(__file__).resolve().parents[2]
OUTDIR = ROOT / "solutions" / "phase_a" / "phase_a_invariant_channel_comparison"
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


def transpose(m: List[List[float]]) -> List[List[float]]:
    return [list(row) for row in zip(*m)]


def matmul(a: List[List[float]], b: List[List[float]]) -> List[List[float]]:
    bt = transpose(b)
    return [[dot(row, col) for col in bt] for row in a]


def eigenvalues_sym3(m: List[List[float]]) -> List[float]:
    # Closed-form symmetric 3x3 eigenvalues
    a11, a12, a13 = m[0]
    _, a22, a23 = m[1]
    _, _, a33 = m[2]
    p1 = a12 * a12 + a13 * a13 + a23 * a23
    if abs(p1) < 1e-14:
        return sorted([a11, a22, a33], reverse=True)
    q = (a11 + a22 + a33) / 3.0
    b11 = a11 - q
    b22 = a22 - q
    b33 = a33 - q
    p2 = b11 * b11 + b22 * b22 + b33 * b33 + 2.0 * p1
    p = math.sqrt(p2 / 6.0)
    B = [
        [b11 / p, a12 / p, a13 / p],
        [a12 / p, b22 / p, a23 / p],
        [a13 / p, a23 / p, b33 / p],
    ]
    r = (
        B[0][0] * (B[1][1] * B[2][2] - B[1][2] * B[2][1])
        - B[0][1] * (B[1][0] * B[2][2] - B[1][2] * B[2][0])
        + B[0][2] * (B[1][0] * B[2][1] - B[1][1] * B[2][0])
    ) / 2.0
    r = max(-1.0, min(1.0, r))
    phi = math.acos(r) / 3.0
    eig1 = q + 2.0 * p * math.cos(phi)
    eig3 = q + 2.0 * p * math.cos(phi + (2.0 * math.pi / 3.0))
    eig2 = 3.0 * q - eig1 - eig3
    return sorted([eig1, eig2, eig3], reverse=True)


def channel_metrics(omega: float, theta: float, phi: float, rho: float) -> Dict[str, float]:
    j = jacobian(omega, theta, phi, rho)
    dtheta = [j[r][1] for r in range(4)]
    dphi = [j[r][2] for r in range(4)]
    drho = [j[r][3] for r in range(4)]

    g = [
        [dot(dtheta, dtheta), dot(dtheta, dphi), dot(dtheta, drho)],
        [dot(dphi, dtheta), dot(dphi, dphi), dot(dphi, drho)],
        [dot(drho, dtheta), dot(drho, dphi), dot(drho, drho)],
    ]
    eigs = eigenvalues_sym3(g)
    svals = [math.sqrt(max(ev, 0.0)) for ev in eigs]
    cond = svals[0] / svals[-1] if svals[-1] > 1e-14 else float("inf")
    return {
        "norm_dtheta": norm(dtheta),
        "norm_dphi": norm(dphi),
        "norm_drho": norm(drho),
        "cos_theta_phi": dot(dtheta, dphi) / (norm(dtheta) * norm(dphi)) if norm(dtheta) * norm(dphi) else 0.0,
        "cos_theta_rho": dot(dtheta, drho) / (norm(dtheta) * norm(drho)) if norm(dtheta) * norm(drho) else 0.0,
        "cos_phi_rho": dot(dphi, drho) / (norm(dphi) * norm(drho)) if norm(dphi) * norm(drho) else 0.0,
        "sigma_max": svals[0],
        "sigma_mid": svals[1],
        "sigma_min": svals[2],
        "condition": cond,
    }


def build_phi_scan() -> Dict[str, object]:
    omega = 0.75
    theta = 1.1
    rho = -0.9
    phis = [k * math.pi / 32.0 for k in range(-64, 65)]
    rows = []
    for phi in phis:
        row = {"phi": phi}
        row.update(channel_metrics(omega, theta, phi, rho))
        rows.append(row)
    with (OUTDIR / "phi_scan.csv").open("w", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=list(rows[0].keys()))
        writer.writeheader()
        writer.writerows(rows)
    return {
        "scan_name": "phi_scan",
        "min_sigma_min": min(r["sigma_min"] for r in rows),
        "max_condition": max(r["condition"] for r in rows if math.isfinite(r["condition"])),
    }


def build_theta_scan() -> Dict[str, object]:
    omega = 0.75
    phi = 0.0
    rho = -0.9
    thetas = [k * math.pi / 32.0 for k in range(-64, 65)]
    rows = []
    for theta in thetas:
        row = {"theta": theta}
        row.update(channel_metrics(omega, theta, phi, rho))
        rows.append(row)
    with (OUTDIR / "theta_scan_phi0.csv").open("w", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=list(rows[0].keys()))
        writer.writeheader()
        writer.writerows(rows)
    return {
        "scan_name": "theta_scan_phi0",
        "min_sigma_min": min(r["sigma_min"] for r in rows),
        "max_condition": max(r["condition"] for r in rows if math.isfinite(r["condition"])),
    }


def build_rho_scan() -> Dict[str, object]:
    omega = 0.75
    phi = 0.0
    theta = 1.1
    rhos = [k * math.pi / 32.0 for k in range(-64, 65)]
    rows = []
    for rho in rhos:
        row = {"rho": rho}
        row.update(channel_metrics(omega, theta, phi, rho))
        rows.append(row)
    with (OUTDIR / "rho_scan_phi0.csv").open("w", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=list(rows[0].keys()))
        writer.writeheader()
        writer.writerows(rows)
    return {
        "scan_name": "rho_scan_phi0",
        "min_sigma_min": min(r["sigma_min"] for r in rows),
        "max_condition": max(r["condition"] for r in rows if math.isfinite(r["condition"])),
    }


def build_named_points() -> List[Dict[str, object]]:
    points = {
        "regular_origin_like": (0.75, 0.0, 0.0, 0.0),
        "regular_generic": (0.75, 1.1, 0.3, -0.9),
        "singular_phi_pi4": (0.75, 1.1, math.pi / 4.0, -0.9),
        "singular_phi_3pi4": (0.75, 1.1, 3.0 * math.pi / 4.0, -0.9),
        "rich_sector_guess_scaled": (0.75, math.pi, -math.pi / 2.0, math.pi / 2.0),
    }
    rows = []
    for name, (omega, theta, phi, rho) in points.items():
        row = {"name": name, "omega": omega, "theta": theta, "phi": phi, "rho": rho}
        row.update(channel_metrics(omega, theta, phi, rho))
        rows.append(row)
    with (OUTDIR / "named_points.json").open("w") as f:
        json.dump(rows, f, indent=2)
    return rows


def write_summary(scans: List[Dict[str, object]], named: List[Dict[str, object]]) -> None:
    lines = []
    lines.append("# Phase A Invariant-Channel Comparison Summary")
    lines.append("")
    lines.append("Generated by `analysis/phase_a/phase_a_invariant_channel_comparison.py`.")
    lines.append("")
    lines.append("## Question")
    lines.append("")
    lines.append("- Do the three angular channels remain equal in strength while differing in conditioning and overlap structure?")
    lines.append("")
    lines.append("## Method")
    lines.append("")
    lines.append("- Build the angular Gram matrix from the theta, phi, and rho Jacobian columns.")
    lines.append("- Compare norms, pairwise overlaps, singular values, and condition numbers under separate phi, theta, and rho scans.")
    lines.append("")
    lines.append("## Scan summaries")
    lines.append("")
    for scan in scans:
        lines.append(f"- {scan['scan_name']}: min sigma_min={scan['min_sigma_min']}, max condition={scan['max_condition']}")
    lines.append("")
    lines.append("The phi scan alone drives sigma_min to zero and the condition number to its extreme values, while the theta and rho scans at phi = 0 keep the angular Gram spectrum perfectly isotropic (condition 1 throughout).")
    lines.append("")
    lines.append("## Named points")
    lines.append("")
    for row in named:
        lines.append(f"### {row['name']}")
        lines.append(f"- norms: theta={row['norm_dtheta']:.6f}, phi={row['norm_dphi']:.6f}, rho={row['norm_drho']:.6f}")
        lines.append(f"- cosines: tp={row['cos_theta_phi']:.6f}, tr={row['cos_theta_rho']:.6f}, pr={row['cos_phi_rho']:.6f}")
        lines.append(f"- singular values: max={row['sigma_max']:.6f}, mid={row['sigma_mid']:.6f}, min={row['sigma_min']:.6f}, condition={row['condition']}")
        lines.append("")
    lines.append("## Interpretation")
    lines.append("")
    lines.append("- The three channels remain equal in norm at every sampled point, so no channel is stronger by amplitude.")
    lines.append("- Phi is the channel that changes the angular conditioning: varying phi can collapse the smallest singular value to zero, while theta and rho sweeps at regular phi do not.")
    lines.append("- This supports the Phase A conclusion that the asymmetry is geometric and relational, not a norm hierarchy.")
    (OUTDIR / "summary.md").write_text("\n".join(lines))


def main() -> None:
    scans = [build_phi_scan(), build_theta_scan(), build_rho_scan()]
    named = build_named_points()
    write_summary(scans, named)
    print(json.dumps({"scans": scans, "named_points": named}, indent=2))


if __name__ == "__main__":
    main()
