from __future__ import annotations

import csv
import json
import math
import sys
from dataclasses import replace
from pathlib import Path

import numpy as np


ROOT = Path(__file__).resolve().parents[2]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from analysis.phase_1 import phase_1_kinematic_redundancy_analysis as p1


OUT_ROOT = ROOT / "solutions" / "phase_3"
OUT_DIR = OUT_ROOT / "phase_3_topology"
OUT_DIR.mkdir(parents=True, exist_ok=True)

ANCHORS = p1.ANCHORS
NAMED_ANCHORS = p1.NAMED_ANCHORS
SCAN_FAMILIES = p1.SCAN_FAMILIES
DOMAIN_MIN = p1.DOMAIN_MIN
DOMAIN_MAX = p1.DOMAIN_MAX


TOPOLOGY_READY = p1.FunctionFamily(
    name="periodic_topology_ready",
    function_class="P",
    description="Periodic angle-respecting family with enough component amplitude to cover the logarithm ball |X| <= pi in a single chart.",
    a=lambda x: 0.35 * np.sin(x),
    da=lambda x: 0.35 * np.cos(x),
    b=lambda x: 3.50 * np.sin(x),
    db=lambda x: 3.50 * np.cos(x),
    c=lambda x: 3.50 * np.sin(x),
    dc=lambda x: 3.50 * np.cos(x),
    d=lambda x: 3.50 * np.sin(x),
    dd=lambda x: 3.50 * np.cos(x),
    formulas={
        "a": "0.35 sin(omega)",
        "b": "3.50 sin(theta)",
        "c": "3.50 sin(phi)",
        "d": "3.50 sin(rho)",
    },
)

FAMILIES = list(p1.FAMILIES) + [TOPOLOGY_READY]


def angle_label(value: float) -> str:
    return p1.angle_label(value)


def mesh_for_axes(axis_points: dict[str, np.ndarray]) -> tuple[np.ndarray, np.ndarray, np.ndarray, np.ndarray]:
    omega = axis_points.get("omega", np.array([0.0]))
    theta = axis_points.get("theta", np.array([0.0]))
    phi = axis_points.get("phi", np.array([0.0]))
    rho = axis_points.get("rho", np.array([0.0]))
    return np.meshgrid(omega, theta, phi, rho, indexing="ij")


def u_theta_phi_rho(
    family: p1.FunctionFamily,
    theta: np.ndarray,
    phi: np.ndarray,
    rho: np.ndarray,
) -> dict[str, np.ndarray]:
    zero = np.zeros_like(theta)
    data = p1.evaluate_family(family, zero, theta, phi, rho)
    alpha = data["alpha"]
    beta = data["beta"]
    gamma = data["gamma"]
    delta = data["delta"]
    db = data["db"]
    dc = data["dc"]
    dd = data["dd"]
    r = data["R"]
    sinc = data["sinc"]
    h = data["h"]

    u = np.stack(
        [
            np.cos(r),
            sinc * beta,
            sinc * gamma,
            sinc * delta,
        ],
        axis=-1,
    )

    d_theta = np.stack(
        [
            -sinc * beta * db,
            (sinc + h * beta * beta) * db,
            (h * beta * gamma) * db,
            (h * beta * delta) * db,
        ],
        axis=-1,
    )
    d_phi = np.stack(
        [
            -sinc * gamma * dc,
            (h * gamma * beta) * dc,
            (sinc + h * gamma * gamma) * dc,
            (h * gamma * delta) * dc,
        ],
        axis=-1,
    )
    d_rho = np.stack(
        [
            -sinc * delta * dd,
            (h * delta * beta) * dd,
            (h * delta * gamma) * dd,
            (sinc + h * delta * delta) * dd,
        ],
        axis=-1,
    )
    return {
        "data": data,
        "u": u,
        "d_theta": d_theta,
        "d_phi": d_phi,
        "d_rho": d_rho,
    }


def determinant4(cols: list[np.ndarray]) -> np.ndarray:
    mats = np.stack(cols, axis=-1)
    flat = mats.reshape(-1, 4, 4)
    dets = np.linalg.det(flat)
    return dets.reshape(cols[0].shape[:-1])


def angle_space_density_formula(data: dict[str, np.ndarray]) -> np.ndarray:
    r = data["R"]
    return (p1.safe_sinc(r) ** 2) * data["db"] * data["dc"] * data["dd"]


def family_range(family: p1.FunctionFamily, num: int = 4097) -> dict[str, tuple[float, float]]:
    pts = np.linspace(DOMAIN_MIN, DOMAIN_MAX, num, dtype=float)
    b_vals = family.b(pts)
    c_vals = family.c(pts)
    d_vals = family.d(pts)
    a_vals = family.a(pts)
    return {
        "a": (float(np.min(a_vals)), float(np.max(a_vals))),
        "b": (float(np.min(b_vals)), float(np.max(b_vals))),
        "c": (float(np.min(c_vals)), float(np.max(c_vals))),
        "d": (float(np.min(d_vals)), float(np.max(d_vals))),
    }


def interval_contains_pi_ball_component(interval: tuple[float, float]) -> bool:
    return interval[0] <= -math.pi and interval[1] >= math.pi


def compactified_hedgehog_grid(n: int, l: float, lam: float) -> tuple[np.ndarray, np.ndarray, np.ndarray, np.ndarray]:
    x = np.linspace(-l, l, n, dtype=float)
    y = np.linspace(-l, l, n, dtype=float)
    z = np.linspace(-l, l, n, dtype=float)
    dx = x[1] - x[0]
    X, Y, Z = np.meshgrid(x, y, z, indexing="ij")
    r = np.sqrt(X**2 + Y**2 + Z**2)
    r_safe = np.where(r > 1.0e-12, r, 1.0)
    F = 2.0 * np.arctan(lam / np.where(r > 1.0e-12, r, 1.0e-12))
    sinF = np.sin(F)
    u = np.zeros(X.shape + (4,), dtype=float)
    u[..., 0] = np.cos(F)
    u[..., 1] = sinF * X / r_safe
    u[..., 2] = sinF * Y / r_safe
    u[..., 3] = sinF * Z / r_safe
    u[r < 1.0e-12] = np.array([-1.0, 0.0, 0.0, 0.0])
    return X, Y, Z, u, dx


def finite_difference_derivatives(field: np.ndarray, spacing: float) -> tuple[np.ndarray, np.ndarray, np.ndarray]:
    grads = []
    for comp in range(field.shape[-1]):
        gx, gy, gz = np.gradient(field[..., comp], spacing, edge_order=2)
        grads.append((gx, gy, gz))
    dux = np.stack([g[0] for g in grads], axis=-1)
    duy = np.stack([g[1] for g in grads], axis=-1)
    duz = np.stack([g[2] for g in grads], axis=-1)
    return dux, duy, duz


def topological_degree_density(u: np.ndarray, dux: np.ndarray, duy: np.ndarray, duz: np.ndarray) -> np.ndarray:
    dets = determinant4([u, dux, duy, duz])
    return dets / (2.0 * math.pi**2)


def principal_log(u: np.ndarray) -> np.ndarray:
    u0 = np.clip(u[..., 0], -1.0, 1.0)
    uvec = u[..., 1:]
    sinR = np.linalg.norm(uvec, axis=-1)
    R = np.arctan2(sinR, u0)
    factor = np.zeros_like(R)
    mask = sinR > 1.0e-10
    factor[mask] = R[mask] / sinR[mask]
    x = np.zeros_like(uvec)
    x[mask] = uvec[mask] * factor[mask][..., None]
    return x


def scalar_angle_benchmark_fields(X: np.ndarray, Y: np.ndarray, Z: np.ndarray) -> dict[str, tuple[np.ndarray, np.ndarray, np.ndarray]]:
    r2 = X**2 + Y**2 + Z**2
    decay = np.exp(-r2 / 9.0)
    return {
        "cartesian_decay": (0.5 * X * decay, 0.5 * Y * decay, 0.5 * Z * decay),
        "mixed_polynomial": (1.5 * Y * Z / (1.0 + r2), 1.5 * Z * X / (1.0 + r2), 1.5 * X * Y / (1.0 + r2)),
        "trig_swirl": (1.2 * np.sin(X) * decay, 1.2 * np.sin(Y) * decay, 1.2 * np.sin(Z) * decay),
    }


def family_inverse_sin_map(amplitude: float, field: np.ndarray) -> np.ndarray:
    ratio = np.clip(field / amplitude, -1.0, 1.0)
    return np.arcsin(ratio)


def write_csv(path: Path, fieldnames: list[str], rows: list[dict]) -> None:
    with path.open("w", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(rows)


def analyze() -> None:
    family_catalog = {
        family.name: {
            "class": family.function_class,
            "description": family.description,
            "formulas": family.formulas,
        }
        for family in FAMILIES
    }
    (OUT_DIR / "topology_family_catalog.json").write_text(json.dumps(family_catalog, indent=2))

    theta_g, phi_g, rho_g = np.meshgrid(ANCHORS, ANCHORS, ANCHORS, indexing="ij")

    angle_anchor_rows: list[dict] = []
    subset_rows: list[dict] = []
    coverage_rows: list[dict] = []
    named_rows: list[dict] = []
    benchmark_rows: list[dict] = []
    singularity_rows: list[dict] = []
    convergence_rows: list[dict] = []
    summary_payload: dict[str, dict] = {}

    for family in FAMILIES:
        derivs = u_theta_phi_rho(family, theta_g, phi_g, rho_g)
        data = derivs["data"]
        u = derivs["u"]
        d_theta = derivs["d_theta"]
        d_phi = derivs["d_phi"]
        d_rho = derivs["d_rho"]

        jang_direct = determinant4([u, d_theta, d_phi, d_rho])
        jang_formula = angle_space_density_formula(data)
        formula_error = np.abs(jang_direct - jang_formula)

        flat_coords = np.column_stack([theta_g.ravel(), phi_g.ravel(), rho_g.ravel()])
        for idx, point in enumerate(flat_coords):
            angle_anchor_rows.append(
                {
                    "family": family.name,
                    "function_class": family.function_class,
                    "theta": point[0],
                    "phi": point[1],
                    "rho": point[2],
                    "theta_label": angle_label(point[0]),
                    "phi_label": angle_label(point[1]),
                    "rho_label": angle_label(point[2]),
                    "beta": float(data["beta"].ravel()[idx]),
                    "gamma": float(data["gamma"].ravel()[idx]),
                    "delta": float(data["delta"].ravel()[idx]),
                    "R": float(data["R"].ravel()[idx]),
                    "J_ang_direct": float(jang_direct.ravel()[idx]),
                    "J_ang_formula": float(jang_formula.ravel()[idx]),
                    "formula_abs_error": float(formula_error.ravel()[idx]),
                    "vacuum_hit": bool(data["vacuum_hit"].ravel()[idx]),
                    "sign_flip_hit": bool(data["sign_flip_hit"].ravel()[idx]),
                    "singular_sheet_hit": bool(data["singular_sheet"].ravel()[idx]),
                }
            )

        family_rows = [row for row in angle_anchor_rows if row["family"] == family.name]
        subset_specs = [
            ("3D_ALL", [], ["theta", "phi", "rho"]),
            ("2D_HOLD_THETA", ["theta"], ["phi", "rho"]),
            ("2D_HOLD_PHI", ["phi"], ["theta", "rho"]),
            ("2D_HOLD_RHO", ["rho"], ["theta", "phi"]),
            ("1D_VARY_THETA", ["phi", "rho"], ["theta"]),
            ("1D_VARY_PHI", ["theta", "rho"], ["phi"]),
            ("1D_VARY_RHO", ["theta", "phi"], ["rho"]),
        ]
        for family_id, held_vars, varied_vars in subset_specs:
            grouped: dict[tuple, list[dict]] = {}
            for row in family_rows:
                key = tuple(row[var] for var in held_vars)
                grouped.setdefault(key, []).append(row)
            for key, rows in grouped.items():
                subset_rows.append(
                    {
                        "family": family.name,
                        "function_class": family.function_class,
                        "family_id": family_id,
                        "held_variables": "|".join(held_vars),
                        "varied_variables": "|".join(varied_vars),
                        "held_value_labels": "|".join(angle_label(v) for v in key),
                        "sample_count": len(rows),
                        "J_ang_min": min(row["J_ang_direct"] for row in rows),
                        "J_ang_max": max(row["J_ang_direct"] for row in rows),
                        "J_ang_abs_max": max(abs(row["J_ang_direct"]) for row in rows),
                        "sign_change": bool(any(row["J_ang_direct"] > 1.0e-10 for row in rows) and any(row["J_ang_direct"] < -1.0e-10 for row in rows)),
                        "vacuum_hits": int(sum(row["vacuum_hit"] for row in rows)),
                        "sign_flip_hits": int(sum(row["sign_flip_hit"] for row in rows)),
                        "singular_sheet_hits": int(sum(row["singular_sheet_hit"] for row in rows)),
                    }
                )

        ranges = family_range(family)
        b_ok = interval_contains_pi_ball_component(ranges["b"])
        c_ok = interval_contains_pi_ball_component(ranges["c"])
        d_ok = interval_contains_pi_ball_component(ranges["d"])
        ball_pi_contained = bool(b_ok and c_ok and d_ok)
        image_surjective_single_chart = ball_pi_contained
        coverage_rows.append(
            {
                "family": family.name,
                "function_class": family.function_class,
                "a_min": ranges["a"][0],
                "a_max": ranges["a"][1],
                "b_min": ranges["b"][0],
                "b_max": ranges["b"][1],
                "c_min": ranges["c"][0],
                "c_max": ranges["c"][1],
                "d_min": ranges["d"][0],
                "d_max": ranges["d"][1],
                "b_covers_minus_pi_to_pi": b_ok,
                "c_covers_minus_pi_to_pi": c_ok,
                "d_covers_minus_pi_to_pi": d_ok,
                "ball_pi_contained": ball_pi_contained,
                "single_chart_surjective_to_S3": image_surjective_single_chart,
                "route_S1_nonzero_degree_possible": False,
            }
        )

        for label, point in NAMED_ANCHORS:
            theta = np.array([point[1]])
            phi = np.array([point[2]])
            rho = np.array([point[3]])
            nd = u_theta_phi_rho(family, theta, phi, rho)
            n_u = nd["u"][0]
            n_j = determinant4([nd["u"], nd["d_theta"], nd["d_phi"], nd["d_rho"]])[0]
            n_formula = angle_space_density_formula(nd["data"])[0]
            named_rows.append(
                {
                    "family": family.name,
                    "anchor_label": label,
                    "theta": point[1],
                    "phi": point[2],
                    "rho": point[3],
                    "u0": float(n_u[0]),
                    "u1": float(n_u[1]),
                    "u2": float(n_u[2]),
                    "u3": float(n_u[3]),
                    "R": float(nd["data"]["R"][0]),
                    "J_ang_direct": float(n_j),
                    "J_ang_formula": float(n_formula),
                    "formula_abs_error": float(abs(n_j - n_formula)),
                    "vacuum_hit": bool(nd["data"]["vacuum_hit"][0]),
                    "sign_flip_hit": bool(nd["data"]["sign_flip_hit"][0]),
                }
            )

        summary_payload[family.name] = {
            "class": family.function_class,
            "max_abs_J_ang": float(np.max(np.abs(jang_direct))),
            "J_ang_sign_change": bool(np.any(jang_direct > 1.0e-10) and np.any(jang_direct < -1.0e-10)),
            "formula_abs_error_max": float(np.max(formula_error)),
            "ball_pi_contained": ball_pi_contained,
            "single_chart_surjective_to_S3": image_surjective_single_chart,
            "route_S1_nonzero_degree_possible": False,
        }

        convergence_specs = [
            ("1D", 257, [["theta"], ["phi"], ["rho"]]),
            ("1D", 1025, [["theta"], ["phi"], ["rho"]]),
            ("2D", 129, [["theta", "phi"], ["theta", "rho"], ["phi", "rho"]]),
            ("2D", 257, [["theta", "phi"], ["theta", "rho"], ["phi", "rho"]]),
            ("3D", 33, [["theta", "phi", "rho"]]),
            ("3D", 65, [["theta", "phi", "rho"]]),
        ]
        for dim_label, resolution, variable_sets in convergence_specs:
            for variable_set in variable_sets:
                axis_points = {name: np.linspace(DOMAIN_MIN, DOMAIN_MAX, resolution, dtype=float) for name in variable_set}
                theta_c, phi_c, rho_c = mesh_for_axes(axis_points)[1:]
                cd = u_theta_phi_rho(family, theta_c, phi_c, rho_c)
                c_j = determinant4([cd["u"], cd["d_theta"], cd["d_phi"], cd["d_rho"]])
                c_formula = angle_space_density_formula(cd["data"])
                convergence_rows.append(
                    {
                        "family": family.name,
                        "dimension_family": dim_label,
                        "free_variables": "|".join(variable_set),
                        "resolution": resolution,
                        "sample_count": int(c_j.size),
                        "J_ang_abs_max": float(np.max(np.abs(c_j))),
                        "formula_abs_error_max": float(np.max(np.abs(c_j - c_formula))),
                        "sign_change": bool(np.any(c_j > 1.0e-10) and np.any(c_j < -1.0e-10)),
                    }
                )

    # Direct S2 benchmark: degree-one unit quaternion field.
    for n in [33, 49, 65]:
        X, Y, Z, u, dx = compactified_hedgehog_grid(n=n, l=6.0, lam=1.0)
        dux, duy, duz = finite_difference_derivatives(u, dx)
        density = topological_degree_density(u, dux, duy, duz)
        degree = float(np.sum(density) * (dx**3))
        benchmark_rows.append(
            {
                "benchmark": "s2_direct_hedgehog",
                "resolution": n,
                "dx": dx,
                "integrated_degree": degree,
                "density_abs_max": float(np.max(np.abs(density))),
            }
        )
        xlog = principal_log(u)
        r = np.sqrt(X**2 + Y**2 + Z**2)
        for shell_radius in [0.15, 0.30, 0.60, 1.20]:
            mask = np.abs(r - shell_radius) <= dx
            shell = xlog[mask]
            if shell.shape[0] == 0:
                continue
            mean = np.mean(shell, axis=0)
            spread = np.max(np.linalg.norm(shell - mean, axis=1))
            singularity_rows.append(
                {
                    "benchmark": "s2_direct_hedgehog_principal_log",
                    "resolution": n,
                    "shell_radius": shell_radius,
                    "sample_count": int(shell.shape[0]),
                    "log_norm_min": float(np.min(np.linalg.norm(shell, axis=1))),
                    "log_norm_max": float(np.max(np.linalg.norm(shell, axis=1))),
                    "log_vector_spread": float(spread),
                }
            )

    # Route S1 smooth scalar-angle benchmarks: direct degree should remain zero.
    family = TOPOLOGY_READY
    for n in [33, 49]:
        x = np.linspace(-6.0, 6.0, n, dtype=float)
        dx = x[1] - x[0]
        X, Y, Z = np.meshgrid(x, x, x, indexing="ij")
        benchmarks = scalar_angle_benchmark_fields(X, Y, Z)
        for label, (beta_field, gamma_field, delta_field) in benchmarks.items():
            theta = family_inverse_sin_map(3.5, beta_field)
            phi = family_inverse_sin_map(3.5, gamma_field)
            rho = family_inverse_sin_map(3.5, delta_field)
            alpha_zero = np.zeros_like(theta)
            r = np.sqrt(beta_field**2 + gamma_field**2 + delta_field**2)
            sinc = p1.safe_sinc(r)
            u = np.stack(
                [
                    np.cos(r),
                    sinc * beta_field,
                    sinc * gamma_field,
                    sinc * delta_field,
                ],
                axis=-1,
            )
            dux, duy, duz = finite_difference_derivatives(u, dx)
            density = topological_degree_density(u, dux, duy, duz)
            benchmark_rows.append(
                {
                    "benchmark": f"s1_scalar_angle_{label}",
                    "resolution": n,
                    "dx": dx,
                    "integrated_degree": float(np.sum(density) * (dx**3)),
                    "density_abs_max": float(np.max(np.abs(density))),
                }
            )

    write_csv(
        OUT_DIR / "angle_space_topology_anchor_samples.csv",
        list(angle_anchor_rows[0].keys()),
        angle_anchor_rows,
    )
    write_csv(
        OUT_DIR / "topology_subset_summary.csv",
        list(subset_rows[0].keys()),
        subset_rows,
    )
    write_csv(
        OUT_DIR / "topology_chart_coverage.csv",
        list(coverage_rows[0].keys()),
        coverage_rows,
    )
    write_csv(
        OUT_DIR / "named_anchor_topology_table.csv",
        list(named_rows[0].keys()),
        named_rows,
    )
    write_csv(
        OUT_DIR / "physical_topology_benchmarks.csv",
        list(benchmark_rows[0].keys()),
        benchmark_rows,
    )
    write_csv(
        OUT_DIR / "principal_log_singularity_shells.csv",
        list(singularity_rows[0].keys()),
        singularity_rows,
    )
    write_csv(
        OUT_DIR / "topology_convergence_summary.csv",
        list(convergence_rows[0].keys()),
        convergence_rows,
    )

    summary = {
        "phase": "Phase 3",
        "headline": {
            "route_S1_global_scalar_angle_topology": "killed_exactly_by_null_homotopy",
            "route_S2_unit_quaternion_topology": "survives_in_principle",
            "main_conclusion": "Nontrivial topology cannot survive through the globally regular scalar-angle lift. It survives only if the unit-quaternion field is fundamental or the angle representation becomes multi-chart or singular.",
        },
        "families": summary_payload,
        "benchmark_summary": {
            "s2_direct_hedgehog_degree_values": [row["integrated_degree"] for row in benchmark_rows if row["benchmark"] == "s2_direct_hedgehog"],
            "s1_scalar_angle_degree_values": {
                row["benchmark"] + f"_n{row['resolution']}": row["integrated_degree"]
                for row in benchmark_rows
                if row["benchmark"].startswith("s1_scalar_angle_")
            },
        },
    }
    (OUT_DIR / "summary.json").write_text(json.dumps(summary, indent=2))

    summary_md = """# Phase 3 Solution Summary

Phase 3 tested whether the unit-quaternion sector can support real topological content after the spacetime lift.

## Main result
- The globally regular scalar-angle lift is topologically dead.
- The unit-quaternion route remains topologically alive.

## Why
- If `u(x) = exp(X(x))` with a globally continuous `X : S^3 -> R^3`, then `u` is null-homotopic through `u_t = exp(t X)`.
- Therefore the physical degree is exactly zero for the globally regular scalar-angle route.

## What the direct data adds
- The angle-space density `J_ang` is nonzero for the live families, so the topological avenue is locally real.
- But the direct S1 scalar-angle benchmarks still integrate to near zero degree.
- A direct S2 hedgehog benchmark integrates to approximately unit degree, showing that the `u` sector itself is topologically capable when treated as fundamental.
- The principal logarithm of that degree-one benchmark remains singular near the core, confirming that no global regular scalar-angle representation exists there.

## Strong implication
- "Knotted spacetime" cannot survive through the default globally regular scalar-angle lift.
- If Khantraction is going to remain topological, the program must elevate `u` to a fundamental field or use a tracked multi-chart / singular-angle construction.
"""
    (OUT_DIR / "summary.md").write_text(summary_md)
    OUT_ROOT.mkdir(parents=True, exist_ok=True)
    (OUT_ROOT / "summary.md").write_text(
        "# Phase 3 Summary\n\nSee `phase_3_topology/summary.md` for the full Phase 3 interpretation.\n"
    )


if __name__ == "__main__":
    analyze()
