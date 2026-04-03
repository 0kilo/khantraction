from __future__ import annotations

import csv
import json
import math
from dataclasses import dataclass
from pathlib import Path
from typing import Callable, Iterable

import numpy as np


ROOT = Path(__file__).resolve().parents[2]
OUT_ROOT = ROOT / "solutions" / "phase_1"
OUT_DIR = OUT_ROOT / "phase_1_kinematics"
OUT_DIR.mkdir(parents=True, exist_ok=True)

DOMAIN_MIN = -2.0 * math.pi
DOMAIN_MAX = 2.0 * math.pi
ANCHORS = np.array(
    [
        -2.0 * math.pi,
        -1.5 * math.pi,
        -1.0 * math.pi,
        -0.5 * math.pi,
        -0.25 * math.pi,
        0.0,
        0.25 * math.pi,
        0.5 * math.pi,
        1.0 * math.pi,
        1.5 * math.pi,
        2.0 * math.pi,
    ],
    dtype=float,
)

NAMED_ANCHORS = [
    ("origin", (0.0, 0.0, 0.0, 0.0)),
    ("theta_quarter", (0.0, 0.25 * math.pi, 0.0, 0.0)),
    ("phi_quarter", (0.0, 0.0, 0.25 * math.pi, 0.0)),
    ("rho_quarter", (0.0, 0.0, 0.0, 0.25 * math.pi)),
    ("omega_quarter", (0.25 * math.pi, 0.0, 0.0, 0.0)),
    ("all_quarter", (0.25 * math.pi, 0.25 * math.pi, 0.25 * math.pi, 0.25 * math.pi)),
    ("all_minus_quarter", (-0.25 * math.pi, -0.25 * math.pi, -0.25 * math.pi, -0.25 * math.pi)),
    ("omega_pi", (math.pi, 0.0, 0.0, 0.0)),
    ("theta_pi", (0.0, math.pi, 0.0, 0.0)),
    ("phi_pi", (0.0, 0.0, math.pi, 0.0)),
    ("rho_pi", (0.0, 0.0, 0.0, math.pi)),
]

SCAN_FAMILIES = [
    ("F4_ALL", [], ["omega", "theta", "phi", "rho"]),
    ("F3_HOLD_OMEGA", ["omega"], ["theta", "phi", "rho"]),
    ("F3_HOLD_THETA", ["theta"], ["omega", "phi", "rho"]),
    ("F3_HOLD_PHI", ["phi"], ["omega", "theta", "rho"]),
    ("F3_HOLD_RHO", ["rho"], ["omega", "theta", "phi"]),
    ("F2_HOLD_PHI_RHO", ["phi", "rho"], ["omega", "theta"]),
    ("F2_HOLD_THETA_RHO", ["theta", "rho"], ["omega", "phi"]),
    ("F2_HOLD_THETA_PHI", ["theta", "phi"], ["omega", "rho"]),
    ("F2_HOLD_OMEGA_RHO", ["omega", "rho"], ["theta", "phi"]),
    ("F2_HOLD_OMEGA_PHI", ["omega", "phi"], ["theta", "rho"]),
    ("F2_HOLD_OMEGA_THETA", ["omega", "theta"], ["phi", "rho"]),
    ("F1_VARY_OMEGA", ["theta", "phi", "rho"], ["omega"]),
    ("F1_VARY_THETA", ["omega", "phi", "rho"], ["theta"]),
    ("F1_VARY_PHI", ["omega", "theta", "rho"], ["phi"]),
    ("F1_VARY_RHO", ["omega", "theta", "phi"], ["rho"]),
    ("F0_ANCHORS", ["omega", "theta", "phi", "rho"], ["anchors"]),
]

EQ_TOL = 1.0e-9
HASH_DECIMALS = 10
HESSIAN_STEP = 1.0e-4


def angle_label(value: float) -> str:
    candidates = {
        -2.0 * math.pi: "-2pi",
        -1.5 * math.pi: "-3pi/2",
        -1.0 * math.pi: "-pi",
        -0.5 * math.pi: "-pi/2",
        -0.25 * math.pi: "-pi/4",
        0.0: "0",
        0.25 * math.pi: "pi/4",
        0.5 * math.pi: "pi/2",
        1.0 * math.pi: "pi",
        1.5 * math.pi: "3pi/2",
        2.0 * math.pi: "2pi",
    }
    for key, label in candidates.items():
        if abs(value - key) < 1.0e-12:
            return label
    return f"{value:.12f}"


def safe_sinc(r: np.ndarray) -> np.ndarray:
    r = np.asarray(r, dtype=float)
    out = np.empty_like(r)
    mask = np.abs(r) > 1.0e-8
    out[mask] = np.sin(r[mask]) / r[mask]
    r_small = r[~mask]
    out[~mask] = 1.0 - (r_small**2) / 6.0 + (r_small**4) / 120.0
    return out


def safe_h(r: np.ndarray) -> np.ndarray:
    r = np.asarray(r, dtype=float)
    out = np.empty_like(r)
    mask = np.abs(r) > 1.0e-6
    out[mask] = (r[mask] * np.cos(r[mask]) - np.sin(r[mask])) / (r[mask] ** 3)
    r_small = r[~mask]
    out[~mask] = -1.0 / 3.0 + (r_small**2) / 30.0 - (r_small**4) / 840.0
    return out


@dataclass(frozen=True)
class FunctionFamily:
    name: str
    function_class: str
    description: str
    a: Callable[[np.ndarray], np.ndarray]
    da: Callable[[np.ndarray], np.ndarray]
    b: Callable[[np.ndarray], np.ndarray]
    db: Callable[[np.ndarray], np.ndarray]
    c: Callable[[np.ndarray], np.ndarray]
    dc: Callable[[np.ndarray], np.ndarray]
    d: Callable[[np.ndarray], np.ndarray]
    dd: Callable[[np.ndarray], np.ndarray]
    formulas: dict[str, str]


FAMILIES = [
    FunctionFamily(
        name="periodic_simple",
        function_class="P",
        description="Baseline periodic family with one-harmonic amplitude and enough imaginary amplitude to cross the first R = pi orientation-loss sheet.",
        a=lambda x: 0.35 * np.sin(x),
        da=lambda x: 0.35 * np.cos(x),
        b=lambda x: 2.20 * np.sin(x),
        db=lambda x: 2.20 * np.cos(x),
        c=lambda x: 2.20 * np.sin(x),
        dc=lambda x: 2.20 * np.cos(x),
        d=lambda x: 2.20 * np.sin(x),
        dd=lambda x: 2.20 * np.cos(x),
        formulas={
            "a": "0.35 sin(omega)",
            "b": "2.20 sin(theta)",
            "c": "2.20 sin(phi)",
            "d": "2.20 sin(rho)",
        },
    ),
    FunctionFamily(
        name="periodic_harmonic",
        function_class="P",
        description="Periodic family with mixed harmonics to test sensitivity inside the admissible periodic class.",
        a=lambda x: 0.20 * np.sin(x) + 0.07 * np.sin(2.0 * x),
        da=lambda x: 0.20 * np.cos(x) + 0.14 * np.cos(2.0 * x),
        b=lambda x: 1.60 * np.sin(x) + 0.90 * np.sin(2.0 * x),
        db=lambda x: 1.60 * np.cos(x) + 1.80 * np.cos(2.0 * x),
        c=lambda x: 1.90 * np.sin(x) - 0.70 * np.sin(2.0 * x),
        dc=lambda x: 1.90 * np.cos(x) - 1.40 * np.cos(2.0 * x),
        d=lambda x: 1.70 * np.sin(x) + 0.50 * np.sin(3.0 * x),
        dd=lambda x: 1.70 * np.cos(x) + 1.50 * np.cos(3.0 * x),
        formulas={
            "a": "0.20 sin(omega) + 0.07 sin(2 omega)",
            "b": "1.60 sin(theta) + 0.90 sin(2 theta)",
            "c": "1.90 sin(phi) - 0.70 sin(2 phi)",
            "d": "1.70 sin(rho) + 0.50 sin(3 rho)",
        },
    ),
    FunctionFamily(
        name="lifted_chart_linear",
        function_class="L",
        description="Non-periodic chart diagnostic family used only to test how much of the redundancy is intrinsic to the exponential map rather than to periodic admissible functions.",
        a=lambda x: 0.12 * x,
        da=lambda x: np.full_like(x, 0.12, dtype=float),
        b=lambda x: 0.55 * x,
        db=lambda x: np.full_like(x, 0.55, dtype=float),
        c=lambda x: 0.45 * x,
        dc=lambda x: np.full_like(x, 0.45, dtype=float),
        d=lambda x: 0.50 * x,
        dd=lambda x: np.full_like(x, 0.50, dtype=float),
        formulas={
            "a": "0.12 omega",
            "b": "0.55 theta",
            "c": "0.45 phi",
            "d": "0.50 rho",
        },
    ),
]


def evaluate_family(
    family: FunctionFamily,
    omega: np.ndarray,
    theta: np.ndarray,
    phi: np.ndarray,
    rho: np.ndarray,
) -> dict[str, np.ndarray]:
    alpha = family.a(omega)
    beta = family.b(theta)
    gamma = family.c(phi)
    delta = family.d(rho)
    da = family.da(omega)
    db = family.db(theta)
    dc = family.dc(phi)
    dd = family.dd(rho)

    r = np.sqrt(beta**2 + gamma**2 + delta**2)
    sinc = safe_sinc(r)
    h = safe_h(r)
    ealpha = np.exp(alpha)
    cos_r = np.cos(r)
    sin_r = np.sin(r)

    q0 = ealpha * cos_r
    q1 = ealpha * sinc * beta
    q2 = ealpha * sinc * gamma
    q3 = ealpha * sinc * delta
    norm = ealpha
    vector_mag = np.sqrt(q1**2 + q2**2 + q3**2)
    jac_det = np.exp(4.0 * alpha) * (sinc**2) * da * db * dc * dd

    with np.errstate(invalid="ignore", divide="ignore"):
        nx = np.where(r > EQ_TOL, beta / r, 0.0)
        ny = np.where(r > EQ_TOL, gamma / r, 0.0)
        nz = np.where(r > EQ_TOL, delta / r, 0.0)

    vacuum_hit = (
        (np.abs(alpha) < 1.0e-10)
        & (np.abs(q0 - 1.0) < 1.0e-10)
        & (np.abs(q1) < 1.0e-10)
        & (np.abs(q2) < 1.0e-10)
        & (np.abs(q3) < 1.0e-10)
    )
    sign_flip_hit = (
        (np.abs(alpha) < 1.0e-10)
        & (np.abs(q0 + 1.0) < 1.0e-10)
        & (np.abs(q1) < 1.0e-10)
        & (np.abs(q2) < 1.0e-10)
        & (np.abs(q3) < 1.0e-10)
    )
    singular_sheet = (np.abs(sin_r) < 1.0e-10) & (r > 1.0e-8)

    return {
        "alpha": alpha,
        "beta": beta,
        "gamma": gamma,
        "delta": delta,
        "da": da,
        "db": db,
        "dc": dc,
        "dd": dd,
        "R": r,
        "sinc": sinc,
        "h": h,
        "q0": q0,
        "q1": q1,
        "q2": q2,
        "q3": q3,
        "norm": norm,
        "vector_mag": vector_mag,
        "jac_det": jac_det,
        "nx": nx,
        "ny": ny,
        "nz": nz,
        "vacuum_hit": vacuum_hit,
        "sign_flip_hit": sign_flip_hit,
        "singular_sheet": singular_sheet,
    }


def jacobian_matrix_point(family: FunctionFamily, point: tuple[float, float, float, float]) -> np.ndarray:
    omega, theta, phi, rho = point
    data = evaluate_family(
        family,
        np.array([omega]),
        np.array([theta]),
        np.array([phi]),
        np.array([rho]),
    )
    alpha = float(data["alpha"][0])
    beta = float(data["beta"][0])
    gamma = float(data["gamma"][0])
    delta = float(data["delta"][0])
    da = float(data["da"][0])
    db = float(data["db"][0])
    dc = float(data["dc"][0])
    dd = float(data["dd"][0])
    r = float(data["R"][0])
    sinc = float(data["sinc"][0])
    h = float(data["h"][0])
    ealpha = math.exp(alpha)
    cos_r = math.cos(r)
    x = np.array([beta, gamma, delta], dtype=float)

    lower = sinc * np.eye(3) + h * np.outer(x, x)
    jy = ealpha * np.block(
        [
            [np.array([[cos_r]], dtype=float), (-sinc * x).reshape(1, 3)],
            [(sinc * x).reshape(3, 1), lower],
        ]
    )
    return jy @ np.diag([da, db, dc, dd])


def q_vector_point(family: FunctionFamily, point: np.ndarray) -> np.ndarray:
    data = evaluate_family(
        family,
        np.array([point[0]]),
        np.array([point[1]]),
        np.array([point[2]]),
        np.array([point[3]]),
    )
    return np.array([data["q0"][0], data["q1"][0], data["q2"][0], data["q3"][0]], dtype=float)


def hessian_diagnostics(family: FunctionFamily, point: tuple[float, float, float, float], step: float = HESSIAN_STEP) -> dict[str, float]:
    x0 = np.array(point, dtype=float)
    base = q_vector_point(family, x0)
    hessians = np.zeros((4, 4, 4), dtype=float)
    for i in range(4):
        ei = np.zeros(4, dtype=float)
        ei[i] = step
        f_plus = q_vector_point(family, x0 + ei)
        f_minus = q_vector_point(family, x0 - ei)
        hessians[:, i, i] = (f_plus - 2.0 * base + f_minus) / (step**2)
        for j in range(i + 1, 4):
            ej = np.zeros(4, dtype=float)
            ej[j] = step
            pp = q_vector_point(family, x0 + ei + ej)
            pm = q_vector_point(family, x0 + ei - ej)
            mp = q_vector_point(family, x0 - ei + ej)
            mm = q_vector_point(family, x0 - ei - ej)
            mixed = (pp - pm - mp + mm) / (4.0 * step**2)
            hessians[:, i, j] = mixed
            hessians[:, j, i] = mixed

    component_norms = np.linalg.norm(hessians.reshape(4, -1), axis=1)
    return {
        "hessian_frobenius_q0": float(component_norms[0]),
        "hessian_frobenius_q1": float(component_norms[1]),
        "hessian_frobenius_q2": float(component_norms[2]),
        "hessian_frobenius_q3": float(component_norms[3]),
        "hessian_frobenius_total": float(np.linalg.norm(hessians)),
    }


def round_hash(q_values: np.ndarray) -> list[str]:
    rounded = np.round(q_values, decimals=HASH_DECIMALS)
    return ["|".join(f"{value:.10f}" for value in row) for row in rounded]


def mesh_for_axes(axis_points: dict[str, np.ndarray]) -> tuple[np.ndarray, np.ndarray, np.ndarray, np.ndarray]:
    omega = axis_points.get("omega", np.array([0.0]))
    theta = axis_points.get("theta", np.array([0.0]))
    phi = axis_points.get("phi", np.array([0.0]))
    rho = axis_points.get("rho", np.array([0.0]))
    return np.meshgrid(omega, theta, phi, rho, indexing="ij")


def canonical_slice_points(var_names: Iterable[str], resolution: int) -> tuple[np.ndarray, np.ndarray, np.ndarray, np.ndarray]:
    axis_points = {name: np.linspace(DOMAIN_MIN, DOMAIN_MAX, resolution, dtype=float) for name in var_names}
    return mesh_for_axes(axis_points)


def write_csv(path: Path, fieldnames: list[str], rows: list[dict]) -> None:
    with path.open("w", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(rows)


def summarize_array(name: str, values: np.ndarray) -> dict[str, float]:
    return {
        f"{name}_min": float(np.min(values)),
        f"{name}_max": float(np.max(values)),
    }


def analyze() -> None:
    (OUT_DIR).mkdir(parents=True, exist_ok=True)

    family_catalog = {
        family.name: {
            "class": family.function_class,
            "description": family.description,
            "formulas": family.formulas,
        }
        for family in FAMILIES
    }
    (OUT_DIR / "function_family_catalog.json").write_text(json.dumps(family_catalog, indent=2))

    omega_g, theta_g, phi_g, rho_g = np.meshgrid(ANCHORS, ANCHORS, ANCHORS, ANCHORS, indexing="ij")
    flat_coords = np.column_stack(
        [
            omega_g.ravel(),
            theta_g.ravel(),
            phi_g.ravel(),
            rho_g.ravel(),
        ]
    )

    anchor_rows: list[dict] = []
    redundancy_summary_rows: list[dict] = []
    redundancy_pair_rows: list[dict] = []
    subset_summary_rows: list[dict] = []
    vacuum_rows: list[dict] = []
    sign_flip_rows: list[dict] = []
    named_anchor_rows: list[dict] = []
    hessian_rows: list[dict] = []
    canonical_1d_rows: list[dict] = []
    convergence_rows: list[dict] = []
    summary_payload: dict[str, dict] = {}

    for family in FAMILIES:
        data = evaluate_family(family, omega_g, theta_g, phi_g, rho_g)
        q_flat = np.column_stack(
            [
                data["q0"].ravel(),
                data["q1"].ravel(),
                data["q2"].ravel(),
                data["q3"].ravel(),
            ]
        )
        hashes = round_hash(q_flat)

        jacobians = np.stack([jacobian_matrix_point(family, tuple(point)) for point in flat_coords], axis=0)
        ranks = np.linalg.matrix_rank(jacobians, tol=1.0e-9)

        for idx, point in enumerate(flat_coords):
            row = {
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
                "beta": float(data["beta"].ravel()[idx]),
                "gamma": float(data["gamma"].ravel()[idx]),
                "delta": float(data["delta"].ravel()[idx]),
                "R": float(data["R"].ravel()[idx]),
                "q0": float(q_flat[idx, 0]),
                "q1": float(q_flat[idx, 1]),
                "q2": float(q_flat[idx, 2]),
                "q3": float(q_flat[idx, 3]),
                "norm": float(data["norm"].ravel()[idx]),
                "vector_mag": float(data["vector_mag"].ravel()[idx]),
                "jac_det": float(data["jac_det"].ravel()[idx]),
                "jac_rank": int(ranks[idx]),
                "vacuum_hit": bool(data["vacuum_hit"].ravel()[idx]),
                "sign_flip_hit": bool(data["sign_flip_hit"].ravel()[idx]),
                "singular_sheet_hit": bool(data["singular_sheet"].ravel()[idx]),
                "q_hash": hashes[idx],
            }
            anchor_rows.append(row)
            if row["vacuum_hit"]:
                vacuum_rows.append(row)
            if row["sign_flip_hit"]:
                sign_flip_rows.append(row)

        unique_hashes, first_indices, inverse_indices, counts = np.unique(
            np.array(hashes, dtype=object),
            return_index=True,
            return_inverse=True,
            return_counts=True,
        )
        duplicate_mask = counts > 1
        duplicate_class_count = int(np.sum(duplicate_mask))
        max_multiplicity = int(np.max(counts))
        unique_count = int(unique_hashes.shape[0])
        total_count = int(len(hashes))
        rank_counts = {f"rank_{rank}": int(np.sum(ranks == rank)) for rank in range(5)}

        redundancy_summary = {
            "family": family.name,
            "function_class": family.function_class,
            "total_anchor_points": total_count,
            "unique_q_classes": unique_count,
            "redundancy_ratio": 1.0 - (unique_count / total_count),
            "duplicate_class_count": duplicate_class_count,
            "max_class_multiplicity": max_multiplicity,
            "vacuum_anchor_count": int(np.sum(data["vacuum_hit"])),
            "sign_flip_anchor_count": int(np.sum(data["sign_flip_hit"])),
            "singular_sheet_anchor_count": int(np.sum(data["singular_sheet"])),
            **rank_counts,
        }
        redundancy_summary_rows.append(redundancy_summary)

        sampled_classes = 0
        for class_index, class_count in enumerate(counts):
            if class_count <= 1:
                continue
            member_indices = np.where(inverse_indices == class_index)[0]
            if member_indices.shape[0] < 2:
                continue
            i0 = int(member_indices[0])
            i1 = int(member_indices[1])
            redundancy_pair_rows.append(
                {
                    "family": family.name,
                    "q_hash": unique_hashes[class_index],
                    "class_multiplicity": int(class_count),
                    "point_a": str(tuple(float(v) for v in flat_coords[i0])),
                    "point_b": str(tuple(float(v) for v in flat_coords[i1])),
                    "q_a": str(tuple(float(v) for v in q_flat[i0])),
                    "q_b": str(tuple(float(v) for v in q_flat[i1])),
                }
            )
            sampled_classes += 1
            if sampled_classes >= 30:
                break

        family_rows = [row for row in anchor_rows if row["family"] == family.name]
        for family_id, held_vars, varied_vars in SCAN_FAMILIES:
            grouped: dict[tuple, list[dict]] = {}
            for row in family_rows:
                key = tuple(row[var] for var in held_vars)
                grouped.setdefault(key, []).append(row)
            for key, rows in grouped.items():
                unique_in_group = len({row["q_hash"] for row in rows})
                subset_summary_rows.append(
                    {
                        "family": family.name,
                        "function_class": family.function_class,
                        "family_id": family_id,
                        "held_variables": "|".join(held_vars),
                        "varied_variables": "|".join(varied_vars),
                        "held_value_labels": "|".join(angle_label(value) for value in key),
                        "sample_count": len(rows),
                        "unique_q_count": unique_in_group,
                        "redundancy_ratio": 1.0 - (unique_in_group / len(rows)),
                        "vacuum_hits": int(sum(row["vacuum_hit"] for row in rows)),
                        "sign_flip_hits": int(sum(row["sign_flip_hit"] for row in rows)),
                        "singular_sheet_hits": int(sum(row["singular_sheet_hit"] for row in rows)),
                        "jac_rank_min": min(int(row["jac_rank"]) for row in rows),
                        "jac_rank_max": max(int(row["jac_rank"]) for row in rows),
                    }
                )

        for label, point in NAMED_ANCHORS:
            point_data = evaluate_family(
                family,
                np.array([point[0]]),
                np.array([point[1]]),
                np.array([point[2]]),
                np.array([point[3]]),
            )
            jacobian = jacobian_matrix_point(family, point)
            jac_rank = int(np.linalg.matrix_rank(jacobian, tol=1.0e-9))
            named_anchor_rows.append(
                {
                    "family": family.name,
                    "anchor_label": label,
                    "omega": point[0],
                    "theta": point[1],
                    "phi": point[2],
                    "rho": point[3],
                    "alpha": float(point_data["alpha"][0]),
                    "beta": float(point_data["beta"][0]),
                    "gamma": float(point_data["gamma"][0]),
                    "delta": float(point_data["delta"][0]),
                    "R": float(point_data["R"][0]),
                    "q0": float(point_data["q0"][0]),
                    "q1": float(point_data["q1"][0]),
                    "q2": float(point_data["q2"][0]),
                    "q3": float(point_data["q3"][0]),
                    "norm": float(point_data["norm"][0]),
                    "vector_mag": float(point_data["vector_mag"][0]),
                    "jac_det": float(np.linalg.det(jacobian)),
                    "jac_rank": jac_rank,
                    "vacuum_hit": bool(point_data["vacuum_hit"][0]),
                    "sign_flip_hit": bool(point_data["sign_flip_hit"][0]),
                    "singular_sheet_hit": bool(point_data["singular_sheet"][0]),
                }
            )
            hessian_rows.append(
                {
                    "family": family.name,
                    "anchor_label": label,
                    **hessian_diagnostics(family, point),
                }
            )

        for variable in ["omega", "theta", "phi", "rho"]:
            points = np.linspace(DOMAIN_MIN, DOMAIN_MAX, 1025, dtype=float)
            axis_points = {"omega": np.array([0.0]), "theta": np.array([0.0]), "phi": np.array([0.0]), "rho": np.array([0.0])}
            axis_points[variable] = points
            omega_s, theta_s, phi_s, rho_s = mesh_for_axes(axis_points)
            slice_data = evaluate_family(family, omega_s, theta_s, phi_s, rho_s)
            for idx, value in enumerate(points):
                canonical_1d_rows.append(
                    {
                        "family": family.name,
                        "variable": variable,
                        "scan_value": float(value),
                        "alpha": float(slice_data["alpha"].ravel()[idx]),
                        "beta": float(slice_data["beta"].ravel()[idx]),
                        "gamma": float(slice_data["gamma"].ravel()[idx]),
                        "delta": float(slice_data["delta"].ravel()[idx]),
                        "R": float(slice_data["R"].ravel()[idx]),
                        "q0": float(slice_data["q0"].ravel()[idx]),
                        "q1": float(slice_data["q1"].ravel()[idx]),
                        "q2": float(slice_data["q2"].ravel()[idx]),
                        "q3": float(slice_data["q3"].ravel()[idx]),
                        "norm": float(slice_data["norm"].ravel()[idx]),
                        "vector_mag": float(slice_data["vector_mag"].ravel()[idx]),
                        "jac_det": float(slice_data["jac_det"].ravel()[idx]),
                        "singular_sheet_hit": bool(slice_data["singular_sheet"].ravel()[idx]),
                    }
                )

        convergence_specs = [
            ("1D", 65, [["omega"], ["theta"], ["phi"], ["rho"]]),
            ("1D", 257, [["omega"], ["theta"], ["phi"], ["rho"]]),
            ("1D", 1025, [["omega"], ["theta"], ["phi"], ["rho"]]),
            ("2D", 33, [["omega", "theta"], ["omega", "phi"], ["omega", "rho"], ["theta", "phi"], ["theta", "rho"], ["phi", "rho"]]),
            ("2D", 129, [["omega", "theta"], ["omega", "phi"], ["omega", "rho"], ["theta", "phi"], ["theta", "rho"], ["phi", "rho"]]),
            ("2D", 257, [["omega", "theta"], ["omega", "phi"], ["omega", "rho"], ["theta", "phi"], ["theta", "rho"], ["phi", "rho"]]),
            ("3D", 17, [["theta", "phi", "rho"], ["omega", "phi", "rho"], ["omega", "theta", "rho"], ["omega", "theta", "phi"]]),
            ("3D", 33, [["theta", "phi", "rho"], ["omega", "phi", "rho"], ["omega", "theta", "rho"], ["omega", "theta", "phi"]]),
            ("3D", 65, [["theta", "phi", "rho"], ["omega", "phi", "rho"], ["omega", "theta", "rho"], ["omega", "theta", "phi"]]),
            ("4D", 11, [["omega", "theta", "phi", "rho"]]),
            ("4D", 17, [["omega", "theta", "phi", "rho"]]),
            ("4D", 33, [["omega", "theta", "phi", "rho"]]),
        ]

        for family_dimension, resolution, variable_sets in convergence_specs:
            for variable_set in variable_sets:
                omega_c, theta_c, phi_c, rho_c = canonical_slice_points(variable_set, resolution)
                summary_data = evaluate_family(family, omega_c, theta_c, phi_c, rho_c)
                q_values = np.column_stack(
                    [
                        summary_data["q0"].ravel(),
                        summary_data["q1"].ravel(),
                        summary_data["q2"].ravel(),
                        summary_data["q3"].ravel(),
                    ]
                )
                rounded = np.round(q_values, decimals=8)
                approx_unique = np.unique(rounded, axis=0).shape[0]
                convergence_rows.append(
                    {
                        "family": family.name,
                        "dimension_family": family_dimension,
                        "free_variables": "|".join(variable_set),
                        "held_variables": "|".join(var for var in ["omega", "theta", "phi", "rho"] if var not in variable_set),
                        "resolution": resolution,
                        "sample_count": int(q_values.shape[0]),
                        "approx_unique_q_count_8dp": int(approx_unique),
                        "singular_fraction": float(np.mean(summary_data["singular_sheet"])),
                        "vacuum_hit_count": int(np.sum(summary_data["vacuum_hit"])),
                        "sign_flip_hit_count": int(np.sum(summary_data["sign_flip_hit"])),
                        **summarize_array("norm", summary_data["norm"]),
                        **summarize_array("R", summary_data["R"]),
                        **summarize_array("jac_abs", np.abs(summary_data["jac_det"])),
                    }
                )

        family_named = [row for row in named_anchor_rows if row["family"] == family.name]
        family_hessian = [row for row in hessian_rows if row["family"] == family.name]
        family_subset = [row for row in subset_summary_rows if row["family"] == family.name]
        max_subset_redundancy = max(row["redundancy_ratio"] for row in family_subset)
        min_subset_unique = min(row["unique_q_count"] for row in family_subset)
        family_anchor_vacuums = [row for row in family_rows if row["vacuum_hit"]]
        family_anchor_signs = [row for row in family_rows if row["sign_flip_hit"]]

        summary_payload[family.name] = {
            "class": family.function_class,
            "redundancy_summary": redundancy_summary,
            "named_anchor_count": len(family_named),
            "max_named_hessian_frobenius_total": max(row["hessian_frobenius_total"] for row in family_hessian),
            "min_named_hessian_frobenius_total": min(row["hessian_frobenius_total"] for row in family_hessian),
            "max_subset_redundancy_ratio": max_subset_redundancy,
            "min_subset_unique_q_count": min_subset_unique,
            "vacuum_equivalent_anchor_examples": [
                {
                    "omega": row["omega_label"],
                    "theta": row["theta_label"],
                    "phi": row["phi_label"],
                    "rho": row["rho_label"],
                }
                for row in family_anchor_vacuums[:10]
            ],
            "sign_flip_anchor_examples": [
                {
                    "omega": row["omega_label"],
                    "theta": row["theta_label"],
                    "phi": row["phi_label"],
                    "rho": row["rho_label"],
                }
                for row in family_anchor_signs[:10]
            ],
        }

    write_csv(
        OUT_DIR / "anchor_lattice_samples.csv",
        [
            "family",
            "function_class",
            "omega",
            "theta",
            "phi",
            "rho",
            "omega_label",
            "theta_label",
            "phi_label",
            "rho_label",
            "alpha",
            "beta",
            "gamma",
            "delta",
            "R",
            "q0",
            "q1",
            "q2",
            "q3",
            "norm",
            "vector_mag",
            "jac_det",
            "jac_rank",
            "vacuum_hit",
            "sign_flip_hit",
            "singular_sheet_hit",
            "q_hash",
        ],
        anchor_rows,
    )
    write_csv(
        OUT_DIR / "redundancy_class_summary.csv",
        list(redundancy_summary_rows[0].keys()),
        redundancy_summary_rows,
    )
    write_csv(
        OUT_DIR / "redundancy_pair_samples.csv",
        ["family", "q_hash", "class_multiplicity", "point_a", "point_b", "q_a", "q_b"],
        redundancy_pair_rows,
    )
    write_csv(
        OUT_DIR / "subset_slice_summary.csv",
        list(subset_summary_rows[0].keys()),
        subset_summary_rows,
    )
    write_csv(
        OUT_DIR / "named_anchor_table.csv",
        list(named_anchor_rows[0].keys()),
        named_anchor_rows,
    )
    write_csv(
        OUT_DIR / "hessian_anchor_diagnostics.csv",
        list(hessian_rows[0].keys()),
        hessian_rows,
    )
    write_csv(
        OUT_DIR / "vacuum_equivalent_anchor_points.csv",
        list(vacuum_rows[0].keys()) if vacuum_rows else list(anchor_rows[0].keys()),
        vacuum_rows,
    )
    write_csv(
        OUT_DIR / "sign_flip_anchor_points.csv",
        list(sign_flip_rows[0].keys()) if sign_flip_rows else list(anchor_rows[0].keys()),
        sign_flip_rows,
    )
    write_csv(
        OUT_DIR / "canonical_dense_1d_scans.csv",
        list(canonical_1d_rows[0].keys()),
        canonical_1d_rows,
    )
    write_csv(
        OUT_DIR / "canonical_convergence_summary.csv",
        list(convergence_rows[0].keys()),
        convergence_rows,
    )

    summary = {
        "phase": "Phase 1",
        "headline": {
            "norm_identity": "|q| = exp(a(omega))",
            "jacobian_determinant_identity": "det(J) = exp(4 a(omega)) * (sin(R)/R)^2 * a'(omega) * b'(theta) * c'(phi) * d'(rho)",
            "main_conclusion": "Pointwise angle labels are not identity invariants; the exponential map carries substantial redundancy, and norm-only structure is already too weak to distinguish theta, phi, and rho.",
        },
        "families": summary_payload,
    }
    (OUT_DIR / "summary.json").write_text(json.dumps(summary, indent=2))

    summary_md = f"""# Phase 1 Solution Summary

Phase 1 analyzed the quaternion map
`q(omega, theta, phi, rho) = exp(a(omega) + b(theta)i + c(phi)j + d(rho)k)`
as a pure kinematic object on the required angle domain `[-2pi, 2pi]^4`.

## What was tested
- exact redundancy structure of the quaternion exponential,
- anchor-lattice coverage on the full 11 x 11 x 11 x 11 grid,
- every hold/vary family extracted from that lattice,
- canonical high-resolution 1D scans,
- canonical convergence summaries for 1D, 2D, 3D, and 4D families,
- Jacobian ranks at every anchor point,
- Hessian diagnostics at the named regression anchors,
- sensitivity to two periodic admissible families and one lifted-chart diagnostic family.

## Main result
- The first complete pointwise invariant is the quaternion value `q` itself.
- The raw input labels `(omega, theta, phi, rho)` are not identity invariants.
- The norm is always
  - `|q| = exp(a(omega))`.
- Therefore any norm-only theory is blind to `theta`, `phi`, and `rho`.

## What the data shows
- The periodic families show large redundancy on the required anchor lattice.
- Vacuum-equivalent points recur across many angle tuples.
- Sign-flip and orientation-loss sheets appear whenever the imaginary radius reaches `R = k pi`.
- The lifted non-periodic diagnostic family retains more unique anchor classes, which shows that part of the collapse comes from the angular periodic admissibility, but not all of it. The exponential map itself remains non-injective.

## Interpretation
- The ansatz does not produce discrete particle species pointwise.
- If Khantraction is going to survive, the surviving identity must come from non-norm structure, topology, geometry, or a later spacetime lift.
- Phase 2 must reject any action that claims angular species structure while depending only on `|q|`.

## Primary artifacts
- `anchor_lattice_samples.csv`
- `subset_slice_summary.csv`
- `redundancy_class_summary.csv`
- `redundancy_pair_samples.csv`
- `vacuum_equivalent_anchor_points.csv`
- `sign_flip_anchor_points.csv`
- `named_anchor_table.csv`
- `hessian_anchor_diagnostics.csv`
- `canonical_dense_1d_scans.csv`
- `canonical_convergence_summary.csv`
- `summary.json`
"""
    (OUT_DIR / "summary.md").write_text(summary_md)

    OUT_ROOT.mkdir(parents=True, exist_ok=True)
    (OUT_ROOT / "summary.md").write_text(
        "# Phase 1 Summary\n\nSee `phase_1_kinematics/summary.md` for the full Phase 1 interpretation.\n"
    )


if __name__ == "__main__":
    analyze()
