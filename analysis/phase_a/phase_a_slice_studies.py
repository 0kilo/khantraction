#!/usr/bin/env python3
"""Phase A slice studies for the ordered quaternion parameter map.

Active domain:
- omega > 0
- theta, phi, rho in [-2*pi, 2*pi]
- no redundancy quotienting

This script builds explicit 1D and 2D slices:
- hold two angles fixed, vary one
- hold one angle fixed, vary two

Outputs are intended to make the chart geometry more interpretable than bulk scans.
"""

from __future__ import annotations

import csv
import json
import math
from pathlib import Path
from typing import Dict, List, Tuple

ROOT = Path(__file__).resolve().parents[2]
OUTDIR = ROOT / "solutions" / "phase_a" / "phase_a_slice_studies"
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


def dot(u: List[float], v: List[float]) -> float:
    return sum(a * b for a, b in zip(u, v))


def norm(v: List[float]) -> float:
    return math.sqrt(dot(v, v))


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


def one_d_slices() -> Dict[str, object]:
    omega = 0.75
    values = [k * math.pi / 16.0 for k in range(-32, 33)]
    slice_specs = {
        "vary_theta_phi0_rho0": ("theta", 0.0, 0.0),
        "vary_phi_theta0_rho0": ("phi", 0.0, 0.0),
        "vary_rho_theta0_phi0": ("rho", 0.0, 0.0),
        "vary_theta_phi_pi4_rho0": ("theta", math.pi / 4.0, 0.0),
        "vary_rho_theta0_phi_pi4": ("rho", 0.0, math.pi / 4.0),
        "vary_phi_theta1.1_rho-0.9": ("phi", 1.1, -0.9),
    }

    summary = {}

    for name, spec in slice_specs.items():
        var = spec[0]
        rows = []
        min_abs_det = None
        singular_count = 0
        for v in values:
            if var == "theta":
                theta, phi, rho = v, spec[1], spec[2]
            elif var == "phi":
                theta, phi, rho = spec[1], v, spec[2]
            else:
                theta, phi, rho = spec[1], spec[2], v

            j = jacobian(omega, theta, phi, rho)
            dtheta = [j[r][1] for r in range(4)]
            dphi = [j[r][2] for r in range(4)]
            drho = [j[r][3] for r in range(4)]
            detj = det4(j)
            abs_det = abs(detj)
            if min_abs_det is None or abs_det < min_abs_det:
                min_abs_det = abs_det
            if abs_det < 1e-8:
                singular_count += 1
            rows.append({
                "value": v,
                "detJ": detj,
                "rankJ": rank(j),
                "norm_dtheta": norm(dtheta),
                "norm_dphi": norm(dphi),
                "norm_drho": norm(drho),
                "cos_theta_phi": dot(dtheta, dphi) / (norm(dtheta) * norm(dphi)) if norm(dtheta) * norm(dphi) else 0.0,
                "cos_theta_rho": dot(dtheta, drho) / (norm(dtheta) * norm(drho)) if norm(dtheta) * norm(drho) else 0.0,
                "cos_phi_rho": dot(dphi, drho) / (norm(dphi) * norm(drho)) if norm(dphi) * norm(drho) else 0.0,
            })

        with (OUTDIR / f"{name}.csv").open("w", newline="") as f:
            writer = csv.DictWriter(f, fieldnames=list(rows[0].keys()))
            writer.writeheader()
            writer.writerows(rows)

        summary[name] = {
            "variable": var,
            "min_abs_detJ": min_abs_det,
            "singular_count": singular_count,
        }

    with (OUTDIR / "one_d_summary.json").open("w") as f:
        json.dump(summary, f, indent=2)
    return summary


def two_d_slices() -> Dict[str, object]:
    omega = 0.75
    values = [k * math.pi / 8.0 for k in range(-16, 17)]
    slice_specs = {
        "theta_phi_rho0": ("theta", "phi", 0.0),
        "theta_rho_phi0": ("theta", "rho", 0.0),
        "phi_rho_theta0": ("phi", "rho", 0.0),
        "theta_rho_phi_pi4": ("theta", "rho", math.pi / 4.0),
    }

    summary = {}

    for name, spec in slice_specs.items():
        ax1, ax2, fixed = spec
        rows = []
        singular_count = 0
        for v1 in values:
            for v2 in values:
                theta = phi = rho = None
                if ax1 == "theta" and ax2 == "phi":
                    theta, phi, rho = v1, v2, fixed
                elif ax1 == "theta" and ax2 == "rho":
                    theta, rho, phi = v1, v2, fixed
                elif ax1 == "phi" and ax2 == "rho":
                    phi, rho, theta = v1, v2, fixed
                j = jacobian(omega, theta, phi, rho)
                detj = det4(j)
                rk = rank(j)
                if abs(detj) < 1e-8:
                    singular_count += 1
                rows.append({
                    ax1: v1,
                    ax2: v2,
                    "detJ": detj,
                    "rankJ": rk,
                })

        with (OUTDIR / f"{name}.csv").open("w", newline="") as f:
            writer = csv.DictWriter(f, fieldnames=list(rows[0].keys()))
            writer.writeheader()
            writer.writerows(rows)

        summary[name] = {
            "axes": [ax1, ax2],
            "fixed": fixed,
            "grid_points": len(rows),
            "singular_count": singular_count,
        }

    with (OUTDIR / "two_d_summary.json").open("w") as f:
        json.dump(summary, f, indent=2)
    return summary


def write_summary(one_d: Dict[str, object], two_d: Dict[str, object]) -> None:
    lines = []
    lines.append("# Phase A Slice Study Summary")
    lines.append("")
    lines.append("Generated by `analysis/phase_a/phase_a_slice_studies.py`.")
    lines.append("")
    lines.append("## Active domain")
    lines.append("- omega > 0")
    lines.append("- theta, phi, rho in [-2pi, 2pi]")
    lines.append("- no redundancy quotienting")
    lines.append("")
    lines.append("## Question")
    lines.append("")
    lines.append("- Under the explicit 1D and 2D slice protocol, which variable sweeps create singular collapse and which remain regular?")
    lines.append("")
    lines.append("## Method")
    lines.append("")
    lines.append("- Build 1D slices by fixing two angles and varying the third across the active domain.")
    lines.append("- Build 2D slices by fixing one angle and varying the other two.")
    lines.append("- Record determinant and Jacobian rank on every slice point.")
    lines.append("")
    lines.append("## 1D slices")
    for name, item in one_d.items():
        lines.append(f"- {name}: variable={item['variable']}, min |detJ|={item['min_abs_detJ']}, singular_count={item['singular_count']}")
    lines.append("")
    lines.append("## 2D slices")
    for name, item in two_d.items():
        lines.append(f"- {name}: axes={item['axes']}, fixed={item['fixed']}, grid_points={item['grid_points']}, singular_count={item['singular_count']}")
    lines.append("")
    lines.append("## Interpretation")
    lines.append("")
    lines.append("- The phi sweeps expose the repeated singular crossings directly: there are eight singular hits across the active interval whenever phi is the variable.")
    lines.append("- Theta or rho sweeps stay fully regular when phi is fixed at a regular value, but become entirely singular when phi is fixed at pi/4.")
    lines.append("- The theta-rho plane is therefore regular at phi = 0 and fully collapsed at phi = pi/4, showing that phi controls whether the paired theta-rho subsystem remains locally distinct.")
    (OUTDIR / "summary.md").write_text("\n".join(lines))


def main() -> None:
    one_d = one_d_slices()
    two_d = two_d_slices()
    write_summary(one_d, two_d)
    print(json.dumps({"one_d": one_d, "two_d": two_d}, indent=2))


if __name__ == "__main__":
    main()
