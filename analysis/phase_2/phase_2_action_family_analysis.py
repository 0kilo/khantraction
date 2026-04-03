from __future__ import annotations

import csv
import json
import math
import sys
from pathlib import Path

import numpy as np


ROOT = Path(__file__).resolve().parents[2]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from analysis.phase_1 import phase_1_kinematic_redundancy_analysis as p1


OUT_ROOT = ROOT / "solutions" / "phase_2"
OUT_DIR = OUT_ROOT / "phase_2_action_families"
OUT_DIR.mkdir(parents=True, exist_ok=True)

ANCHORS = p1.ANCHORS
NAMED_ANCHORS = p1.NAMED_ANCHORS
SCAN_FAMILIES = p1.SCAN_FAMILIES
DOMAIN_MIN = p1.DOMAIN_MIN
DOMAIN_MAX = p1.DOMAIN_MAX

TOL = 1.0e-10


def mesh_for_axes(axis_points: dict[str, np.ndarray]) -> tuple[np.ndarray, np.ndarray, np.ndarray, np.ndarray]:
    omega = axis_points.get("omega", np.array([0.0]))
    theta = axis_points.get("theta", np.array([0.0]))
    phi = axis_points.get("phi", np.array([0.0]))
    rho = axis_points.get("rho", np.array([0.0]))
    return np.meshgrid(omega, theta, phi, rho, indexing="ij")


def angle_label(value: float) -> str:
    return p1.angle_label(value)


def q_derivatives(
    family: p1.FunctionFamily,
    omega: np.ndarray,
    theta: np.ndarray,
    phi: np.ndarray,
    rho: np.ndarray,
) -> dict[str, np.ndarray]:
    data = p1.evaluate_family(family, omega, theta, phi, rho)
    alpha = data["alpha"]
    beta = data["beta"]
    gamma = data["gamma"]
    delta = data["delta"]
    da = data["da"]
    db = data["db"]
    dc = data["dc"]
    dd = data["dd"]
    r = data["R"]
    sinc = data["sinc"]
    h = data["h"]
    ealpha = np.exp(alpha)

    x1 = beta
    x2 = gamma
    x3 = delta

    q0 = data["q0"]
    q1 = data["q1"]
    q2 = data["q2"]
    q3 = data["q3"]

    d_omega = np.stack([q0 * da, q1 * da, q2 * da, q3 * da], axis=-1)

    d_theta = np.stack(
        [
            -ealpha * sinc * x1 * db,
            ealpha * (sinc + h * x1 * x1) * db,
            ealpha * (h * x1 * x2) * db,
            ealpha * (h * x1 * x3) * db,
        ],
        axis=-1,
    )
    d_phi = np.stack(
        [
            -ealpha * sinc * x2 * dc,
            ealpha * (h * x2 * x1) * dc,
            ealpha * (sinc + h * x2 * x2) * dc,
            ealpha * (h * x2 * x3) * dc,
        ],
        axis=-1,
    )
    d_rho = np.stack(
        [
            -ealpha * sinc * x3 * dd,
            ealpha * (h * x3 * x1) * dd,
            ealpha * (h * x3 * x2) * dd,
            ealpha * (sinc + h * x3 * x3) * dd,
        ],
        axis=-1,
    )

    u = np.stack(
        [
            np.cos(r),
            sinc * x1,
            sinc * x2,
            sinc * x3,
        ],
        axis=-1,
    )
    d_u_omega = np.zeros_like(d_omega)
    d_u_theta = d_theta / ealpha[..., None]
    d_u_phi = d_phi / ealpha[..., None]
    d_u_rho = d_rho / ealpha[..., None]

    d_alpha = np.stack([da, np.zeros_like(da), np.zeros_like(da), np.zeros_like(da)], axis=-1)
    d_norm = np.stack([data["norm"] * da, np.zeros_like(da), np.zeros_like(da), np.zeros_like(da)], axis=-1)

    return {
        "data": data,
        "u": u,
        "d_omega": d_omega,
        "d_theta": d_theta,
        "d_phi": d_phi,
        "d_rho": d_rho,
        "d_u_omega": d_u_omega,
        "d_u_theta": d_u_theta,
        "d_u_phi": d_u_phi,
        "d_u_rho": d_u_rho,
        "d_alpha": d_alpha,
        "d_norm": d_norm,
    }


def dot_last(a: np.ndarray, b: np.ndarray) -> np.ndarray:
    return np.sum(a * b, axis=-1)


def metric_from_columns(*cols: np.ndarray) -> np.ndarray:
    columns = list(cols)
    shape = cols[0].shape[:-1]
    out = np.zeros(shape + (len(columns), len(columns)), dtype=float)
    for i, ci in enumerate(columns):
        for j, cj in enumerate(columns):
            out[..., i, j] = dot_last(ci, cj)
    return out


def pure_imaginary_left_current(u: np.ndarray, du: np.ndarray) -> np.ndarray:
    u0 = u[..., 0]
    uv = u[..., 1:]
    du0 = du[..., 0]
    duv = du[..., 1:]
    return u0[..., None] * duv - du0[..., None] * uv - np.cross(uv, duv)


def topological_density(u: np.ndarray, d_theta: np.ndarray, d_phi: np.ndarray, d_rho: np.ndarray) -> np.ndarray:
    mats = np.stack([u, d_theta, d_phi, d_rho], axis=-1)
    flat = mats.reshape(-1, 4, 4)
    vals = np.linalg.det(flat)
    return vals.reshape(u.shape[:-1])


def named_anchor_metric_summary(metric: np.ndarray) -> dict[str, float]:
    eigvals = np.linalg.eigvalsh(metric)
    return {
        "eig0": float(eigvals[0]),
        "eig1": float(eigvals[1]),
        "eig2": float(eigvals[2]),
        "eig3": float(eigvals[3]),
        "trace": float(np.trace(metric)),
        "det": float(np.linalg.det(metric)),
        "rank": int(np.linalg.matrix_rank(metric, tol=1.0e-9)),
    }


def write_csv(path: Path, fieldnames: list[str], rows: list[dict]) -> None:
    with path.open("w", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(rows)


def analyze() -> None:
    OUT_DIR.mkdir(parents=True, exist_ok=True)

    action_catalog = {
        "A0_norm_only": {
            "route": "S1",
            "status": "retired_for_species",
            "reason": "Depends only on |q| = exp(a(omega)); blind to theta, phi, rho.",
        },
        "A1_full_quaternion_sigma": {
            "route": "S1",
            "status": "viable_core",
            "reason": "Derivative term sees the full quaternion map.",
        },
        "A2_split_sigma": {
            "route": "S2",
            "status": "viable_core",
            "reason": "Explicitly separates scale alpha and unit-quaternion orientation u.",
        },
        "A3_split_sigma_skyrme": {
            "route": "S2",
            "status": "viable_core",
            "reason": "Adds a direct quartic stabilizer and a live topological avenue.",
        },
        "A4_curvature_scale_only": {
            "route": "S1",
            "status": "retired_for_species",
            "reason": "Curvature coupling through the norm channel still remains angle-blind.",
        },
        "A5_curvature_split": {
            "route": "S2/S3",
            "status": "viable_but_unresolved",
            "reason": "Potentially viable if curvature sees more than alpha, but tensor structure is not fixed yet.",
        },
        "A6_frame_connection": {
            "route": "S3",
            "status": "structurally_incomplete",
            "reason": "Maurer-Cartan structure is present, but the direct action principle is not yet fixed.",
        },
    }
    (OUT_DIR / "action_family_catalog.json").write_text(json.dumps(action_catalog, indent=2))

    omega_g, theta_g, phi_g, rho_g = np.meshgrid(ANCHORS, ANCHORS, ANCHORS, ANCHORS, indexing="ij")
    flat_coords = np.column_stack([omega_g.ravel(), theta_g.ravel(), phi_g.ravel(), rho_g.ravel()])

    anchor_rows: list[dict] = []
    subset_rows: list[dict] = []
    named_rows: list[dict] = []
    metric_rows: list[dict] = []
    classification_rows: list[dict] = []
    convergence_rows: list[dict] = []
    summary_payload: dict[str, dict] = {}

    for family in p1.FAMILIES:
        derivs = q_derivatives(family, omega_g, theta_g, phi_g, rho_g)
        data = derivs["data"]
        u = derivs["u"]

        dcols_q = [derivs["d_omega"], derivs["d_theta"], derivs["d_phi"], derivs["d_rho"]]
        dcols_u = [derivs["d_u_omega"], derivs["d_u_theta"], derivs["d_u_phi"], derivs["d_u_rho"]]
        G_norm = metric_from_columns(derivs["d_norm"], np.zeros_like(derivs["d_norm"]), np.zeros_like(derivs["d_norm"]), np.zeros_like(derivs["d_norm"]))
        G_full = metric_from_columns(*dcols_q)
        G_u = metric_from_columns(*dcols_u)
        G_split = metric_from_columns(derivs["d_alpha"], derivs["d_u_theta"], derivs["d_u_phi"], derivs["d_u_rho"])

        l_theta = pure_imaginary_left_current(u, derivs["d_u_theta"])
        l_phi = pure_imaginary_left_current(u, derivs["d_u_phi"])
        l_rho = pure_imaginary_left_current(u, derivs["d_u_rho"])
        skyrme_density = (
            np.sum(np.cross(l_theta, l_phi) ** 2, axis=-1)
            + np.sum(np.cross(l_theta, l_rho) ** 2, axis=-1)
            + np.sum(np.cross(l_phi, l_rho) ** 2, axis=-1)
        )
        topo_density = topological_density(u, derivs["d_u_theta"], derivs["d_u_phi"], derivs["d_u_rho"])

        trace_norm = np.trace(G_norm, axis1=-2, axis2=-1)
        trace_full = np.trace(G_full, axis1=-2, axis2=-1)
        trace_u = np.trace(G_u, axis1=-2, axis2=-1)
        trace_split = np.trace(G_split, axis1=-2, axis2=-1)

        flat_u = u.reshape(-1, 4)
        flat_topo = topo_density.ravel()
        flat_skyrme = skyrme_density.ravel()
        flat_trace_norm = trace_norm.ravel()
        flat_trace_full = trace_full.ravel()
        flat_trace_u = trace_u.ravel()
        flat_trace_split = trace_split.ravel()

        for idx, point in enumerate(flat_coords):
            anchor_rows.append(
                {
                    "family": family.name,
                    "function_class": family.function_class,
                    "omega": point[0],
                    "theta": point[1],
                    "phi": point[2],
                    "rho": point[3],
                    "omega_label": angle_label(point[0]),
                    "theta_label": angle_label(point[1]),
                    "phi_label": angle_label(point[2]),
                    "rho_label": angle_label(point[3]),
                    "alpha": float(data["alpha"].ravel()[idx]),
                    "R": float(data["R"].ravel()[idx]),
                    "norm": float(data["norm"].ravel()[idx]),
                    "u0": float(flat_u[idx, 0]),
                    "u1": float(flat_u[idx, 1]),
                    "u2": float(flat_u[idx, 2]),
                    "u3": float(flat_u[idx, 3]),
                    "trace_G_norm": float(flat_trace_norm[idx]),
                    "trace_G_full": float(flat_trace_full[idx]),
                    "trace_G_u": float(flat_trace_u[idx]),
                    "trace_G_split": float(flat_trace_split[idx]),
                    "skyrme_density": float(flat_skyrme[idx]),
                    "topological_density": float(flat_topo[idx]),
                    "vacuum_hit": bool(data["vacuum_hit"].ravel()[idx]),
                }
            )

        family_anchor_rows = [row for row in anchor_rows if row["family"] == family.name]
        for family_id, held_vars, varied_vars in SCAN_FAMILIES:
            grouped: dict[tuple, list[dict]] = {}
            for row in family_anchor_rows:
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
                        "held_value_labels": "|".join(angle_label(value) for value in key),
                        "sample_count": len(rows),
                        "unique_norm_trace_count": len({round(row["trace_G_norm"], 10) for row in rows}),
                        "unique_full_trace_count": len({round(row["trace_G_full"], 10) for row in rows}),
                        "unique_u_trace_count": len({round(row["trace_G_u"], 10) for row in rows}),
                        "unique_split_trace_count": len({round(row["trace_G_split"], 10) for row in rows}),
                        "unique_skyrme_density_count": len({round(row["skyrme_density"], 10) for row in rows}),
                        "topological_density_abs_max": max(abs(row["topological_density"]) for row in rows),
                        "norm_trace_min": min(row["trace_G_norm"] for row in rows),
                        "norm_trace_max": max(row["trace_G_norm"] for row in rows),
                        "full_trace_min": min(row["trace_G_full"] for row in rows),
                        "full_trace_max": max(row["trace_G_full"] for row in rows),
                        "split_trace_min": min(row["trace_G_split"] for row in rows),
                        "split_trace_max": max(row["trace_G_split"] for row in rows),
                        "skyrme_density_min": min(row["skyrme_density"] for row in rows),
                        "skyrme_density_max": max(row["skyrme_density"] for row in rows),
                    }
                )

        for label, point in NAMED_ANCHORS:
            omega_p = np.array([point[0]])
            theta_p = np.array([point[1]])
            phi_p = np.array([point[2]])
            rho_p = np.array([point[3]])
            point_derivs = q_derivatives(family, omega_p, theta_p, phi_p, rho_p)
            point_u = point_derivs["u"][0]
            point_l_theta = pure_imaginary_left_current(point_u[None, :], point_derivs["d_u_theta"])[0]
            point_l_phi = pure_imaginary_left_current(point_u[None, :], point_derivs["d_u_phi"])[0]
            point_l_rho = pure_imaginary_left_current(point_u[None, :], point_derivs["d_u_rho"])[0]
            point_skyrme = (
                float(np.sum(np.cross(point_l_theta, point_l_phi) ** 2))
                + float(np.sum(np.cross(point_l_theta, point_l_rho) ** 2))
                + float(np.sum(np.cross(point_l_phi, point_l_rho) ** 2))
            )
            point_topo = float(topological_density(point_u[None, :], point_derivs["d_u_theta"], point_derivs["d_u_phi"], point_derivs["d_u_rho"])[0])
            G_norm_point = metric_from_columns(
                point_derivs["d_norm"],
                np.zeros_like(point_derivs["d_norm"]),
                np.zeros_like(point_derivs["d_norm"]),
                np.zeros_like(point_derivs["d_norm"]),
            )[0]
            G_full_point = metric_from_columns(
                point_derivs["d_omega"],
                point_derivs["d_theta"],
                point_derivs["d_phi"],
                point_derivs["d_rho"],
            )[0]
            G_u_point = metric_from_columns(
                point_derivs["d_u_omega"],
                point_derivs["d_u_theta"],
                point_derivs["d_u_phi"],
                point_derivs["d_u_rho"],
            )[0]
            G_split_point = metric_from_columns(
                point_derivs["d_alpha"],
                point_derivs["d_u_theta"],
                point_derivs["d_u_phi"],
                point_derivs["d_u_rho"],
            )[0]

            named_rows.append(
                {
                    "family": family.name,
                    "anchor_label": label,
                    "omega": point[0],
                    "theta": point[1],
                    "phi": point[2],
                    "rho": point[3],
                    "trace_G_norm": float(np.trace(G_norm_point)),
                    "trace_G_full": float(np.trace(G_full_point)),
                    "trace_G_u": float(np.trace(G_u_point)),
                    "trace_G_split": float(np.trace(G_split_point)),
                    "skyrme_density": point_skyrme,
                    "topological_density": point_topo,
                    **{f"norm_{k}": v for k, v in named_anchor_metric_summary(G_norm_point).items()},
                    **{f"full_{k}": v for k, v in named_anchor_metric_summary(G_full_point).items()},
                    **{f"u_{k}": v for k, v in named_anchor_metric_summary(G_u_point).items()},
                    **{f"split_{k}": v for k, v in named_anchor_metric_summary(G_split_point).items()},
                }
            )

        family_subset_rows = [row for row in subset_rows if row["family"] == family.name]
        non_norm_slice_support = any(row["unique_full_trace_count"] > 1 or row["unique_split_trace_count"] > 1 for row in family_subset_rows if row["varied_variables"] != "anchors")
        skyrme_nonzero = bool(np.any(flat_skyrme > TOL))
        topo_nonzero = bool(np.any(np.abs(flat_topo) > TOL))
        topo_sign_change = bool(np.any(flat_topo > TOL) and np.any(flat_topo < -TOL))

        classification_rows.extend(
            [
                {
                    "family": family.name,
                    "action_family": "A0_norm_only",
                    "status": "retired_for_species",
                    "angle_sensitive_on_sampled_domain": False,
                    "nontrivial_kinetic_rank_possible": False,
                    "topological_route_detected": False,
                    "reason": "Norm channel depends only on omega through exp(a(omega)).",
                },
                {
                    "family": family.name,
                    "action_family": "A1_full_quaternion_sigma",
                    "status": "viable_core",
                    "angle_sensitive_on_sampled_domain": bool(non_norm_slice_support),
                    "nontrivial_kinetic_rank_possible": bool(np.any(flat_trace_full > TOL)),
                    "topological_route_detected": bool(topo_nonzero),
                    "reason": "Full quaternion derivatives remain nontrivial beyond the norm channel.",
                },
                {
                    "family": family.name,
                    "action_family": "A2_split_sigma",
                    "status": "viable_core",
                    "angle_sensitive_on_sampled_domain": bool(np.any(flat_trace_u > TOL)),
                    "nontrivial_kinetic_rank_possible": bool(np.any(flat_trace_split > TOL)),
                    "topological_route_detected": bool(topo_nonzero),
                    "reason": "The unit-quaternion sector carries non-norm orientation structure directly.",
                },
                {
                    "family": family.name,
                    "action_family": "A3_split_sigma_skyrme",
                    "status": "viable_core",
                    "angle_sensitive_on_sampled_domain": bool(np.any(flat_trace_u > TOL)),
                    "nontrivial_kinetic_rank_possible": bool(np.any(flat_skyrme > TOL)),
                    "topological_route_detected": bool(topo_nonzero),
                    "reason": "Quartic Maurer-Cartan structure is nonzero on the sampled domain.",
                },
                {
                    "family": family.name,
                    "action_family": "A4_curvature_scale_only",
                    "status": "retired_for_species",
                    "angle_sensitive_on_sampled_domain": False,
                    "nontrivial_kinetic_rank_possible": False,
                    "topological_route_detected": False,
                    "reason": "Curvature through the norm channel still remains angle-blind.",
                },
                {
                    "family": family.name,
                    "action_family": "A5_curvature_split",
                    "status": "viable_but_unresolved",
                    "angle_sensitive_on_sampled_domain": bool(np.any(flat_trace_u > TOL)),
                    "nontrivial_kinetic_rank_possible": True,
                    "topological_route_detected": bool(topo_nonzero),
                    "reason": "The split route survives, but the explicit curvature tensor couplings are not fixed yet.",
                },
                {
                    "family": family.name,
                    "action_family": "A6_frame_connection",
                    "status": "structurally_incomplete",
                    "angle_sensitive_on_sampled_domain": bool(np.any(flat_trace_u > TOL)),
                    "nontrivial_kinetic_rank_possible": bool(np.any(np.linalg.norm(np.vstack([l_theta.ravel(), l_phi.ravel(), l_rho.ravel()]), axis=0) > 0)),
                    "topological_route_detected": bool(topo_nonzero),
                    "reason": "Maurer-Cartan data is present, but the direct connection action is not fixed yet.",
                },
            ]
        )

        summary_payload[family.name] = {
            "class": family.function_class,
            "max_trace_norm": float(np.max(flat_trace_norm)),
            "max_trace_full": float(np.max(flat_trace_full)),
            "max_trace_u": float(np.max(flat_trace_u)),
            "max_trace_split": float(np.max(flat_trace_split)),
            "max_skyrme_density": float(np.max(flat_skyrme)),
            "max_abs_topological_density": float(np.max(np.abs(flat_topo))),
            "topological_density_sign_change": topo_sign_change,
            "non_norm_slice_support": non_norm_slice_support,
        }

        convergence_specs = [
            ("1D", 65, [["omega"], ["theta"], ["phi"], ["rho"]]),
            ("1D", 257, [["omega"], ["theta"], ["phi"], ["rho"]]),
            ("1D", 1025, [["omega"], ["theta"], ["phi"], ["rho"]]),
            ("2D", 33, [["omega", "theta"], ["omega", "phi"], ["omega", "rho"], ["theta", "phi"], ["theta", "rho"], ["phi", "rho"]]),
            ("2D", 129, [["omega", "theta"], ["omega", "phi"], ["omega", "rho"], ["theta", "phi"], ["theta", "rho"], ["phi", "rho"]]),
            ("3D", 17, [["theta", "phi", "rho"], ["omega", "phi", "rho"], ["omega", "theta", "rho"], ["omega", "theta", "phi"]]),
            ("3D", 33, [["theta", "phi", "rho"], ["omega", "phi", "rho"], ["omega", "theta", "rho"], ["omega", "theta", "phi"]]),
            ("4D", 11, [["omega", "theta", "phi", "rho"]]),
            ("4D", 17, [["omega", "theta", "phi", "rho"]]),
        ]
        for dim_label, resolution, variable_sets in convergence_specs:
            for variable_set in variable_sets:
                axis_points = {name: np.linspace(DOMAIN_MIN, DOMAIN_MAX, resolution, dtype=float) for name in variable_set}
                omega_c, theta_c, phi_c, rho_c = mesh_for_axes(axis_points)
                cd = q_derivatives(family, omega_c, theta_c, phi_c, rho_c)
                cu = cd["u"]
                c_full = metric_from_columns(cd["d_omega"], cd["d_theta"], cd["d_phi"], cd["d_rho"])
                c_u = metric_from_columns(cd["d_u_omega"], cd["d_u_theta"], cd["d_u_phi"], cd["d_u_rho"])
                c_split = metric_from_columns(cd["d_alpha"], cd["d_u_theta"], cd["d_u_phi"], cd["d_u_rho"])
                c_trace_full = np.trace(c_full, axis1=-2, axis2=-1)
                c_trace_u = np.trace(c_u, axis1=-2, axis2=-1)
                c_trace_split = np.trace(c_split, axis1=-2, axis2=-1)
                c_topo = topological_density(cu, cd["d_u_theta"], cd["d_u_phi"], cd["d_u_rho"])
                c_ltheta = pure_imaginary_left_current(cu, cd["d_u_theta"])
                c_lphi = pure_imaginary_left_current(cu, cd["d_u_phi"])
                c_lrho = pure_imaginary_left_current(cu, cd["d_u_rho"])
                c_skyrme = (
                    np.sum(np.cross(c_ltheta, c_lphi) ** 2, axis=-1)
                    + np.sum(np.cross(c_ltheta, c_lrho) ** 2, axis=-1)
                    + np.sum(np.cross(c_lphi, c_lrho) ** 2, axis=-1)
                )
                convergence_rows.append(
                    {
                        "family": family.name,
                        "dimension_family": dim_label,
                        "free_variables": "|".join(variable_set),
                        "resolution": resolution,
                        "sample_count": int(c_trace_full.size),
                        "trace_full_min": float(np.min(c_trace_full)),
                        "trace_full_max": float(np.max(c_trace_full)),
                        "trace_u_min": float(np.min(c_trace_u)),
                        "trace_u_max": float(np.max(c_trace_u)),
                        "trace_split_min": float(np.min(c_trace_split)),
                        "trace_split_max": float(np.max(c_trace_split)),
                        "skyrme_density_max": float(np.max(c_skyrme)),
                        "topological_density_abs_max": float(np.max(np.abs(c_topo))),
                    }
                )

    write_csv(
        OUT_DIR / "action_anchor_samples.csv",
        list(anchor_rows[0].keys()),
        anchor_rows,
    )
    write_csv(
        OUT_DIR / "subset_action_sensitivity.csv",
        list(subset_rows[0].keys()),
        subset_rows,
    )
    write_csv(
        OUT_DIR / "named_anchor_action_table.csv",
        list(named_rows[0].keys()),
        named_rows,
    )
    write_csv(
        OUT_DIR / "action_family_classification.csv",
        list(classification_rows[0].keys()),
        classification_rows,
    )
    write_csv(
        OUT_DIR / "action_convergence_summary.csv",
        list(convergence_rows[0].keys()),
        convergence_rows,
    )

    summary = {
        "phase": "Phase 2",
        "headline": {
            "norm_only_route": "retired_for_species",
            "strongest_current_route": "A3_split_sigma_skyrme",
            "main_conclusion": "After Phase 0 and Phase 1, only non-norm action families built from the full quaternion sector or the split unit-quaternion sector remain viable particle-level routes.",
        },
        "families": summary_payload,
        "action_catalog": action_catalog,
    }
    (OUT_DIR / "summary.json").write_text(json.dumps(summary, indent=2))

    summary_md = """# Phase 2 Solution Summary

Phase 2 classified the direct action families that still survive after the Phase 0 and Phase 1 constraints.

## What was tested
- norm-only kinetic structure,
- full quaternion sigma-model structure,
- split `q = e^alpha u` structure,
- Maurer-Cartan / Skyrme quartic structure,
- candidate angle-space topological density,
- exhaustive hold/vary subset summaries on the required anchor lattice,
- canonical convergence summaries for the action-building observables.

## Main result
- Norm-only and scale-only curvature routes are retired as particle-species routes.
- The surviving core routes are:
  - full quaternion sigma,
  - split sigma,
  - split sigma plus Skyrme stabilizer.
- The strongest current route is the split sigma plus Skyrme family because it combines:
  - non-norm angular sensitivity,
  - nontrivial kinetic rank,
  - and a direct topological avenue through the unit-quaternion sector.

## Why
- `|q| = exp(a(omega))` makes the norm-only route blind to `theta`, `phi`, and `rho`.
- The full quaternion and split routes retain nontrivial derivative structure.
- The Skyrme quartic density and the candidate topological density are nonzero on the sampled domain for the nontrivial families.

## What survives to later phases
- A1 full quaternion sigma
- A2 split sigma
- A3 split sigma plus Skyrme
- A5 curvature-coupled split route
- A6 frame/connection route, but only as structurally incomplete

## What is retired
- A0 norm-only scalar route as a species route
- A4 curvature-coupled scale-only route as a species route
"""
    (OUT_DIR / "summary.md").write_text(summary_md)
    OUT_ROOT.mkdir(parents=True, exist_ok=True)
    (OUT_ROOT / "summary.md").write_text(
        "# Phase 2 Summary\n\nSee `phase_2_action_families/summary.md` for the full Phase 2 interpretation.\n"
    )


if __name__ == "__main__":
    analyze()
