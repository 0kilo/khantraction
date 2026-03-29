#!/usr/bin/env python3
"""Phase A analysis: ordered quaternion parameter geometry.

Computes component map, Jacobian, tangent Gram matrix, determinant/rank
behavior, and a coarse scan of symmetry/asymmetry features for
Q(omega,theta,phi,rho) = e^omega e^{theta i} e^{phi j} e^{rho k}.
"""

from __future__ import annotations

import csv
import json
import math
from pathlib import Path
from typing import Dict, List, Tuple


ROOT = Path(__file__).resolve().parents[1]
OUTDIR = ROOT / "solutions" / "phase_a_parameter_geometry"
OUTDIR.mkdir(parents=True, exist_ok=True)


def components(omega: float, theta: float, phi: float, rho: float) -> Tuple[float, float, float, float]:
    ct, st = math.cos(theta), math.sin(theta)
    cp, sp = math.cos(phi), math.sin(phi)
    cr, sr = math.cos(rho), math.sin(rho)

    a = ct * cp * cr - st * sp * sr
    b = st * cp * cr + ct * sp * sr
    c = ct * sp * cr - st * cp * sr
    d = ct * cp * sr + st * sp * cr
    scale = math.exp(omega)
    return scale * a, scale * b, scale * c, scale * d


def angular_components(theta: float, phi: float, rho: float) -> Tuple[float, float, float, float]:
    return components(0.0, theta, phi, rho)


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


def transpose(m: List[List[float]]) -> List[List[float]]:
    return [list(row) for row in zip(*m)]


def matmul(a: List[List[float]], b: List[List[float]]) -> List[List[float]]:
    bt = transpose(b)
    return [[dot(row, col) for col in bt] for row in a]


def det4(m: List[List[float]]) -> float:
    a = [row[:] for row in m]
    n = 4
    det = 1.0
    sign = 1.0
    for i in range(n):
        pivot = max(range(i, n), key=lambda r: abs(a[r][i]))
        if abs(a[pivot][i]) < 1e-12:
            return 0.0
        if pivot != i:
            a[i], a[pivot] = a[pivot], a[i]
            sign *= -1.0
        piv = a[i][i]
        det *= piv
        for r in range(i + 1, n):
            factor = a[r][i] / piv
            for c in range(i + 1, n):
                a[r][c] -= factor * a[i][c]
            a[r][i] = 0.0
    return det * sign


def rank(m: List[List[float]], tol: float = 1e-10) -> int:
    a = [row[:] for row in m]
    rows, cols = len(a), len(a[0])
    r = 0
    for c in range(cols):
        pivot = None
        for i in range(r, rows):
            if abs(a[i][c]) > tol:
                pivot = i
                break
        if pivot is None:
            continue
        a[r], a[pivot] = a[pivot], a[r]
        piv = a[r][c]
        for j in range(c, cols):
            a[r][j] /= piv
        for i in range(rows):
            if i != r and abs(a[i][c]) > tol:
                factor = a[i][c]
                for j in range(c, cols):
                    a[i][j] -= factor * a[r][j]
        r += 1
        if r == rows:
            break
    return r


def norm(v: List[float]) -> float:
    return math.sqrt(dot(v, v))


def summarize_grid() -> Dict[str, object]:
    samples = [k * math.pi / 8.0 for k in range(-8, 9)]
    omega = 0.0
    rows = []
    min_abs_det = None
    min_point = None
    max_offdiag = 0.0
    special = []

    for theta in samples:
        for phi in samples:
            for rho in samples:
                j = jacobian(omega, theta, phi, rho)
                jt = transpose(j)
                g = matmul(jt, j)
                ang_cols = [[j[r][1], j[r][2], j[r][3]] for r in range(4)]
                # Correct extraction of angular column vectors
                dtheta = [j[r][1] for r in range(4)]
                dphi = [j[r][2] for r in range(4)]
                drho = [j[r][3] for r in range(4)]
                ntheta, nphi, nrho = norm(dtheta), norm(dphi), norm(drho)
                ctp = dot(dtheta, dphi) / (ntheta * nphi) if ntheta * nphi else 0.0
                ctr = dot(dtheta, drho) / (ntheta * nrho) if ntheta * nrho else 0.0
                cpr = dot(dphi, drho) / (nphi * nrho) if nphi * nrho else 0.0
                offdiag = max(abs(ctp), abs(ctr), abs(cpr))
                detj = det4(j)
                abs_detj = abs(detj)
                rk = rank(j)
                rows.append({
                    "theta": theta,
                    "phi": phi,
                    "rho": rho,
                    "norm_dtheta": ntheta,
                    "norm_dphi": nphi,
                    "norm_drho": nrho,
                    "cos_theta_phi": ctp,
                    "cos_theta_rho": ctr,
                    "cos_phi_rho": cpr,
                    "detJ": detj,
                    "rankJ": rk,
                })
                if min_abs_det is None or abs_detj < min_abs_det:
                    min_abs_det = abs_detj
                    min_point = (theta, phi, rho, rk)
                if offdiag > max_offdiag:
                    max_offdiag = offdiag
                if rk < 4 or abs_detj < 1e-6:
                    special.append({
                        "theta": theta,
                        "phi": phi,
                        "rho": rho,
                        "detJ": detj,
                        "rankJ": rk,
                        "norm_dtheta": ntheta,
                        "norm_dphi": nphi,
                        "norm_drho": nrho,
                        "cos_theta_phi": ctp,
                        "cos_theta_rho": ctr,
                        "cos_phi_rho": cpr,
                    })

    with (OUTDIR / "coarse_scan.csv").open("w", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=list(rows[0].keys()))
        writer.writeheader()
        writer.writerows(rows)

    with (OUTDIR / "special_points.json").open("w") as f:
        json.dump(special, f, indent=2)

    return {
        "grid_points": len(rows),
        "min_abs_detJ": min_abs_det,
        "min_point": {
            "theta": min_point[0],
            "phi": min_point[1],
            "rho": min_point[2],
            "rankJ": min_point[3],
        } if min_point else None,
        "max_abs_angular_cosine": max_offdiag,
        "special_point_count": len(special),
    }


def sample_named_points() -> List[Dict[str, object]]:
    named = {
        "origin": (0.0, 0.0, 0.0, 0.0),
        "rich_sector_guess": (0.0, math.pi, -math.pi / 2.0, math.pi / 2.0),
        "all_quarter_turn": (0.0, math.pi / 2.0, math.pi / 2.0, math.pi / 2.0),
        "theta_quarter": (0.0, math.pi / 2.0, 0.0, 0.0),
        "phi_quarter": (0.0, 0.0, math.pi / 2.0, 0.0),
        "rho_quarter": (0.0, 0.0, 0.0, math.pi / 2.0),
    }
    report = []
    for name, (omega, theta, phi, rho) in named.items():
        x = components(omega, theta, phi, rho)
        j = jacobian(omega, theta, phi, rho)
        dtheta = [j[r][1] for r in range(4)]
        dphi = [j[r][2] for r in range(4)]
        drho = [j[r][3] for r in range(4)]
        report.append({
            "name": name,
            "components": x,
            "norm_dtheta": norm(dtheta),
            "norm_dphi": norm(dphi),
            "norm_drho": norm(drho),
            "detJ": det4(j),
            "rankJ": rank(j),
            "cos_theta_phi": dot(dtheta, dphi) / (norm(dtheta) * norm(dphi)) if norm(dtheta) * norm(dphi) else 0.0,
            "cos_theta_rho": dot(dtheta, drho) / (norm(dtheta) * norm(drho)) if norm(dtheta) * norm(drho) else 0.0,
            "cos_phi_rho": dot(dphi, drho) / (norm(dphi) * norm(drho)) if norm(dphi) * norm(drho) else 0.0,
        })
    with (OUTDIR / "named_points.json").open("w") as f:
        json.dump(report, f, indent=2)
    return report


def write_summary(summary: Dict[str, object], named: List[Dict[str, object]]) -> None:
    lines = []
    lines.append("# Phase A Parameter Geometry Summary")
    lines.append("")
    lines.append("This file is generated by `analysis/phase_a_parameter_geometry.py`.")
    lines.append("")
    lines.append(f"- Grid points scanned: {summary['grid_points']}")
    lines.append(f"- Minimum |det J| on coarse grid: {summary['min_abs_detJ']}")
    lines.append(f"- Max absolute cosine between angular tangent directions: {summary['max_abs_angular_cosine']}")
    lines.append(f"- Number of coarse special/singular points detected: {summary['special_point_count']}")
    lines.append("")
    lines.append("## Named-point snapshots")
    lines.append("")
    for item in named:
        lines.append(f"### {item['name']}")
        lines.append(f"- components: {item['components']}")
        lines.append(f"- angular tangent norms: theta={item['norm_dtheta']:.6f}, phi={item['norm_dphi']:.6f}, rho={item['norm_drho']:.6f}")
        lines.append(f"- pairwise angular cosines: (theta,phi)={item['cos_theta_phi']:.6f}, (theta,rho)={item['cos_theta_rho']:.6f}, (phi,rho)={item['cos_phi_rho']:.6f}")
        lines.append(f"- detJ={item['detJ']:.6f}, rankJ={item['rankJ']}")
        lines.append("")
    (OUTDIR / "summary.md").write_text("\n".join(lines))


def main() -> None:
    summary = summarize_grid()
    named = sample_named_points()
    write_summary(summary, named)
    print(json.dumps({"summary": summary, "named_points": named}, indent=2))


if __name__ == "__main__":
    main()
