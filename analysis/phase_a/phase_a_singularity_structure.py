#!/usr/bin/env python3
"""Phase A singularity structure analysis for the ordered quaternion map.

Active domain convention for this project step:
- omega > 0
- theta, phi, rho in [-2*pi, 2*pi]
- do not quotient out angular redundancies

Goal:
- verify Jacobian determinant structure on the active domain,
- characterize singular slices within the wider angle box,
- save outputs for the ongoing Phase A notes.
"""

from __future__ import annotations

import csv
import json
import math
from pathlib import Path
from typing import Dict, List, Tuple

ROOT = Path(__file__).resolve().parents[1]
OUTDIR = ROOT / "solutions" / "phase_a_singularity_structure"
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


def scan_domain() -> Dict[str, object]:
    omegas = [0.25, 0.75, 1.5]
    angles = [k * math.pi / 8.0 for k in range(-16, 17)]  # [-2pi, 2pi]

    max_err = 0.0
    min_abs_det = None
    singular_rows = []
    total = 0

    for omega in omegas:
        for theta in angles:
            for phi in angles:
                for rho in angles[::2]:
                    detj = det4(jacobian(omega, theta, phi, rho))
                    candidate = math.exp(4.0 * omega) * math.cos(2.0 * phi)
                    err = abs(detj - candidate)
                    max_err = max(max_err, err)
                    total += 1
                    abs_det = abs(detj)
                    if min_abs_det is None or abs_det < min_abs_det:
                        min_abs_det = abs_det
                    if abs_det < 1e-8:
                        singular_rows.append({
                            "omega": omega,
                            "theta": theta,
                            "phi": phi,
                            "rho": rho,
                            "detJ": detj,
                            "candidate": candidate,
                            "rankJ": rank(jacobian(omega, theta, phi, rho)),
                        })

    with (OUTDIR / "domain_singular_points.json").open("w") as f:
        json.dump(singular_rows, f, indent=2)

    return {
        "sample_count": total,
        "max_err_det_minus_exp4w_cos2phi": max_err,
        "singular_point_count": len(singular_rows),
        "min_abs_detJ": min_abs_det,
        "omega_values": omegas,
        "angle_domain": [-2.0 * math.pi, 2.0 * math.pi],
    }


def produce_phi_slice_table() -> List[Dict[str, object]]:
    omega = 0.75
    theta = 1.1
    rho = -0.9
    phis = [k * math.pi / 8.0 for k in range(-16, 17)]
    rows = []
    for phi in phis:
        detj = det4(jacobian(omega, theta, phi, rho))
        candidate = math.exp(4.0 * omega) * math.cos(2.0 * phi)
        rows.append({
            "phi": phi,
            "detJ": detj,
            "exp4w_cos2phi": candidate,
            "abs_err": abs(detj - candidate),
        })
    with (OUTDIR / "phi_slice_table.csv").open("w", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=list(rows[0].keys()))
        writer.writeheader()
        writer.writerows(rows)
    return rows


def write_summary(domain: Dict[str, object], rows: List[Dict[str, object]]) -> None:
    lines = []
    lines.append("# Phase A Singularity Structure Summary")
    lines.append("")
    lines.append("Generated by `analysis/phase_a_singularity_structure.py`.")
    lines.append("")
    lines.append("## Active domain convention")
    lines.append("")
    lines.append("- omega > 0")
    lines.append("- theta, phi, rho in [-2pi, 2pi]")
    lines.append("- no redundancy quotienting")
    lines.append("")
    lines.append("## Main result on the active domain")
    lines.append("")
    lines.append(r"Across the sampled active domain, the Jacobian determinant matches")
    lines.append(r"\[")
    lines.append(r"\det J = e^{4\omega}\cos(2\phi)")
    lines.append(r"\]")
    lines.append(r"to numerical precision.")
    lines.append("")
    lines.append(f"- sampled points: {domain['sample_count']}")
    lines.append(f"- max |detJ - e^(4w)cos(2phi)|: {domain['max_err_det_minus_exp4w_cos2phi']}")
    lines.append(f"- singular sampled points: {domain['singular_point_count']}")
    lines.append(f"- minimum |detJ| seen: {domain['min_abs_detJ']}")
    lines.append("")
    lines.append("## Singular slices")
    lines.append("")
    lines.append(r"The singular condition is")
    lines.append(r"\[")
    lines.append(r"\cos(2\phi)=0 \iff \phi = \pi/4 + n\pi/2")
    lines.append(r"\]")
    lines.append(r"within the active box \([-2\pi,2\pi]\).")
    lines.append("")
    lines.append("So inside the current working domain the singular phi slices are:")
    for k in range(-4, 5):
        val = math.pi / 4.0 + k * math.pi / 2.0
        if -2.0 * math.pi - 1e-9 <= val <= 2.0 * math.pi + 1e-9:
            lines.append(f"- phi = {val:.12f}")
    lines.append("")
    lines.append("## Interpretation")
    lines.append("")
    lines.append("The wider angle domain does not change the core mapping result; it simply reveals more repeated singular slices because the ordered-angle chart is being sampled across multiple periods.")
    lines.append("")
    lines.append("Omega rescales the determinant magnitude through e^(4 omega), while the singular architecture itself remains controlled by phi.")
    lines.append("")
    lines.append("## Reference phi-slice check")
    lines.append("")
    for row in rows[:9]:
        lines.append(f"- phi={row['phi']:.6f}: detJ={row['detJ']:.6f}, e^(4w)cos(2phi)={row['exp4w_cos2phi']:.6f}, abs_err={row['abs_err']:.3e}")
    (OUTDIR / "summary.md").write_text("\n".join(lines))


def main() -> None:
    domain = scan_domain()
    rows = produce_phi_slice_table()
    write_summary(domain, rows)
    print(json.dumps({"domain": domain, "phi_slice_preview": rows[:9]}, indent=2))


if __name__ == "__main__":
    main()
