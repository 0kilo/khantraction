#!/usr/bin/env python3
"""Phase K: direct 3D same-background interaction-energy study."""

from __future__ import annotations

import json
import math
import sys
from pathlib import Path

import numpy as np
import pandas as pd

ROOT = Path(__file__).resolve().parents[2]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from analysis.direct_ordered_manifold import (  # noqa: E402
    DirectRuntimeConfig,
    OrderedManifoldWaveSolver,
    OrderedSeed,
    embed_profile_on_grid,
    interaction_energy_density,
    solve_direct_radial_profile,
    superpose_profiles_on_grid,
)


OUT_DIR = ROOT / "solutions" / "phase_k" / "phase_k_multi_fold_interaction"
CFG = DirectRuntimeConfig(
    r_max=10.0,
    dr=0.01,
    grid_size=15,
    dx=0.55,
    dt=0.03,
    time_steps=12,
)
DISTANCES = np.linspace(1.5, 4.5, 7)
FIXED_DISTANCE = 2.5
ANGLES_1D = np.linspace(-2.0 * np.pi, 2.0 * np.pi, 9)
ANGLES_2D = np.linspace(-2.0 * np.pi, 2.0 * np.pi, 4)


def write_csv(path: Path, rows: list[dict] | pd.DataFrame) -> None:
    if isinstance(rows, pd.DataFrame):
        rows.to_csv(path, index=False)
    else:
        pd.DataFrame(rows).to_csv(path, index=False)


def identical_seed_family() -> list[OrderedSeed]:
    return [
        OrderedSeed("scalar", 0.5, 0.0, 0.0, 0.0),
        OrderedSeed("rich", 0.5, math.pi, -0.5 * math.pi, 0.5 * math.pi),
        OrderedSeed("phi_offsheet", 0.5, 0.0, math.pi / 4.0 - 0.1, 0.0),
    ]


def fit_quality(distance: np.ndarray, values: np.ndarray) -> dict[str, float]:
    x = np.asarray(distance, dtype=float)
    y = np.abs(np.asarray(values, dtype=float))
    pb, pa = np.polyfit(np.log(x), np.log(y), 1)
    y_pow = np.exp(pa) * x**pb
    eb, ea = np.polyfit(x, np.log(y), 1)
    y_exp = np.exp(ea) * np.exp(eb * x)
    ss_tot = float(np.sum((y - y.mean()) ** 2))
    ss_res_pow = float(np.sum((y - y_pow) ** 2))
    ss_res_exp = float(np.sum((y - y_exp) ** 2))
    return {
        "power_exponent": float(pb),
        "power_r2_linear_space": 1.0 - ss_res_pow / ss_tot if ss_tot > 0.0 else float("nan"),
        "exp_exponent": float(eb),
        "exp_r2_linear_space": 1.0 - ss_res_exp / ss_tot if ss_tot > 0.0 else float("nan"),
    }


def pair_fields(
    solver: OrderedManifoldWaveSolver,
    profile,
    distance: float,
) -> tuple[np.ndarray, np.ndarray, np.ndarray]:
    ambient = profile.y[-1, :4]
    left_center = (-0.5 * float(distance), 0.0, 0.0)
    right_center = (0.5 * float(distance), 0.0, 0.0)
    left = embed_profile_on_grid(profile, solver.x, solver.y, solver.z, center=left_center, ambient=ambient)
    right = embed_profile_on_grid(profile, solver.x, solver.y, solver.z, center=right_center, ambient=ambient)
    total = superpose_profiles_on_grid(
        [(profile, left_center), (profile, right_center)],
        solver.x,
        solver.y,
        solver.z,
        ambient=ambient,
    )
    ambient_fields = ambient[:, None, None, None] * np.ones_like(total)
    return total, left, right, ambient_fields


def bulk_force_law(solver: OrderedManifoldWaveSolver, profiles: dict[str, object]) -> tuple[pd.DataFrame, list[dict]]:
    bulk_rows = []
    pair_rows = []
    for distance in DISTANCES:
        row = {"distance": float(distance)}
        for label, profile in profiles.items():
            total, left, right, ambient = pair_fields(solver, profile, float(distance))
            rho_int = interaction_energy_density(total, left, right, ambient, CFG)
            row[f"dm_{label}_pair"] = float(np.sum(rho_int) * CFG.dx ** 3)
        bulk_rows.append(row)

    bulk = pd.DataFrame(bulk_rows)
    for label in profiles:
        bulk[f"force_{label}_pair"] = -np.gradient(bulk[f"dm_{label}_pair"], bulk["distance"])
        fit_dm = fit_quality(bulk["distance"].to_numpy(), bulk[f"dm_{label}_pair"].to_numpy())
        fit_force = fit_quality(bulk["distance"].to_numpy(), bulk[f"force_{label}_pair"].to_numpy())
        near_idx = int(np.argmin(np.abs(bulk["distance"] - FIXED_DISTANCE)))
        pair_rows.append(
            {
                "pair": f"{label}_pair",
                "seed": label,
                "dm_at_fixed_distance": float(bulk[f"dm_{label}_pair"].iloc[near_idx]),
                "force_at_fixed_distance": float(bulk[f"force_{label}_pair"].iloc[near_idx]),
                "dm_power_exponent": fit_dm["power_exponent"],
                "dm_power_r2_linear_space": fit_dm["power_r2_linear_space"],
                "dm_exp_exponent": fit_dm["exp_exponent"],
                "dm_exp_r2_linear_space": fit_dm["exp_r2_linear_space"],
                "force_power_exponent": fit_force["power_exponent"],
                "force_power_r2_linear_space": fit_force["power_r2_linear_space"],
                "force_exp_exponent": fit_force["exp_exponent"],
                "force_exp_r2_linear_space": fit_force["exp_r2_linear_space"],
            }
        )

    write_csv(OUT_DIR / "bulk_force_law.csv", bulk)
    write_csv(OUT_DIR / "pair_comparisons.csv", pair_rows)
    return bulk, pair_rows


def identical_seed_from_param(param: str, value: float) -> OrderedSeed:
    kwargs = {"omega": 0.5, "theta": 0.0, "phi": 0.0, "rho": 0.0}
    kwargs[param] = float(value)
    return OrderedSeed(f"{param}_{value:+.6f}", kwargs["omega"], kwargs["theta"], kwargs["phi"], kwargs["rho"])


def slice_1d_interactions(solver: OrderedManifoldWaveSolver) -> pd.DataFrame:
    rows = []
    for param in ("theta", "phi", "rho"):
        for value in ANGLES_1D:
            seed = identical_seed_from_param(param, float(value))
            profile = solve_direct_radial_profile(seed, CFG)
            total, left, right, ambient = pair_fields(solver, profile, FIXED_DISTANCE)
            rho_int = interaction_energy_density(total, left, right, ambient, CFG)
            rows.append(
                {
                    "param": param,
                    "val": float(value),
                    "profile_success": profile.success,
                    "dm": float(np.sum(rho_int) * CFG.dx ** 3),
                    "pair_compactness": profile.compactness_90,
                }
            )
    df = pd.DataFrame(rows)
    write_csv(OUT_DIR / "slices_1d_angle_interaction.csv", df)
    return df


def slice_2d_interactions(solver: OrderedManifoldWaveSolver) -> dict[tuple[str, str], pd.DataFrame]:
    outputs: dict[tuple[str, str], pd.DataFrame] = {}
    for first, second, filename in [
        ("theta", "rho", "slices_2d_theta_rho_interaction.csv"),
        ("theta", "phi", "slices_2d_theta_phi_interaction.csv"),
        ("phi", "rho", "slices_2d_phi_rho_interaction.csv"),
    ]:
        rows = []
        for value_a in ANGLES_2D:
            for value_b in ANGLES_2D:
                kwargs = {"omega": 0.5, "theta": 0.0, "phi": 0.0, "rho": 0.0}
                kwargs[first] = float(value_a)
                kwargs[second] = float(value_b)
                seed = OrderedSeed(
                    f"{first}_{value_a:+.6f}_{second}_{value_b:+.6f}",
                    kwargs["omega"],
                    kwargs["theta"],
                    kwargs["phi"],
                    kwargs["rho"],
                )
                profile = solve_direct_radial_profile(seed, CFG)
                total, left, right, ambient = pair_fields(solver, profile, FIXED_DISTANCE)
                rho_int = interaction_energy_density(total, left, right, ambient, CFG)
                rows.append(
                    {
                        first: float(value_a),
                        second: float(value_b),
                        "profile_success": profile.success,
                        "dm": float(np.sum(rho_int) * CFG.dx ** 3),
                        "pair_compactness": profile.compactness_90,
                    }
                )
        df = pd.DataFrame(rows)
        write_csv(OUT_DIR / filename, df)
        outputs[(first, second)] = df
    return outputs


def split_centroids(weight: np.ndarray, x: np.ndarray) -> tuple[float, float]:
    left_mask = x < 0.0
    right_mask = x > 0.0
    left_weight = weight * left_mask
    right_weight = weight * right_mask
    left_total = float(np.sum(left_weight))
    right_total = float(np.sum(right_weight))
    left_centroid = float(np.sum(left_weight * x) / left_total) if left_total > 0.0 else float("nan")
    right_centroid = float(np.sum(right_weight * x) / right_total) if right_total > 0.0 else float("nan")
    return left_centroid, right_centroid


def representative_pair_evolution(solver: OrderedManifoldWaveSolver, profiles: dict[str, object]) -> pd.DataFrame:
    rows = []
    for label in ("scalar", "rich"):
        total, _left, _right, _ambient = pair_fields(solver, profiles[label], FIXED_DISTANCE)
        velocities = np.zeros_like(total)
        _fields_f, _vel_f, history = solver.evolve(total, velocities, steps=CFG.time_steps, sample_every=1)
        for row in history:
            row = dict(row)
            row["pair"] = f"{label}_pair"
            row["distance"] = FIXED_DISTANCE
            rows.append(row)
    df = pd.DataFrame(rows)
    write_csv(OUT_DIR / "representative_pair_evolution.csv", df)
    return df


def build_summary(
    bulk: pd.DataFrame,
    pair_rows: list[dict],
    slices_1d: pd.DataFrame,
    slices_2d: dict[tuple[str, str], pd.DataFrame],
) -> dict:
    pair_df = pd.DataFrame(pair_rows)
    summary = {
        "phase": "K",
        "status": "direct_same_background_refresh",
        "model_scope": {
            "type": "direct_3d_interaction_energy_same_background_pairs",
            "statement": (
                "Phase K now integrates the 3D interaction-energy density directly on a shared grid for same-background pair initial data. "
                "This replaces the old one-dimensional overlap proxy for the directly defined part of the problem."
            ),
        },
        "config": {
            "distance_min": float(DISTANCES.min()),
            "distance_max": float(DISTANCES.max()),
            "distance_points": int(len(DISTANCES)),
            "fixed_distance": float(FIXED_DISTANCE),
            "angles_1d_points": int(len(ANGLES_1D)),
            "angles_2d_points_per_axis": int(len(ANGLES_2D)),
            "grid_size": CFG.grid_size,
            "dx": CFG.dx,
        },
        "key_results": {
            "scalar_dm_range": [float(bulk["dm_scalar_pair"].min()), float(bulk["dm_scalar_pair"].max())],
            "rich_dm_range": [float(bulk["dm_rich_pair"].min()), float(bulk["dm_rich_pair"].max())],
            "phi_offsheet_dm_range": [float(bulk["dm_phi_offsheet_pair"].min()), float(bulk["dm_phi_offsheet_pair"].max())],
            "scalar_force_power_exponent": float(pair_df.loc[pair_df["pair"] == "scalar_pair", "force_power_exponent"].iloc[0]),
            "scalar_force_power_r2_linear_space": float(pair_df.loc[pair_df["pair"] == "scalar_pair", "force_power_r2_linear_space"].iloc[0]),
            "scalar_force_exp_r2_linear_space": float(pair_df.loc[pair_df["pair"] == "scalar_pair", "force_exp_r2_linear_space"].iloc[0]),
            "phi_1d_dm_range": [
                float(slices_1d[slices_1d["param"] == "phi"]["dm"].min()),
                float(slices_1d[slices_1d["param"] == "phi"]["dm"].max()),
            ],
            "theta_1d_dm_range": [
                float(slices_1d[slices_1d["param"] == "theta"]["dm"].min()),
                float(slices_1d[slices_1d["param"] == "theta"]["dm"].max()),
            ],
            "rho_1d_dm_range": [
                float(slices_1d[slices_1d["param"] == "rho"]["dm"].min()),
                float(slices_1d[slices_1d["param"] == "rho"]["dm"].max()),
            ],
            "theta_rho_2d_dm_range": [
                float(slices_2d[("theta", "rho")]["dm"].min()),
                float(slices_2d[("theta", "rho")]["dm"].max()),
            ],
            "theta_phi_2d_dm_range": [
                float(slices_2d[("theta", "phi")]["dm"].min()),
                float(slices_2d[("theta", "phi")]["dm"].max()),
            ],
            "phi_rho_2d_dm_range": [
                float(slices_2d[("phi", "rho")]["dm"].min()),
                float(slices_2d[("phi", "rho")]["dm"].max()),
            ],
        },
        "goal_status": {
            "direct_interaction_energy_density": "met_for_same_background_pairs",
            "effective_force_gradient": "met_for_same_background_pairs",
            "inverse_square_force_law": "not_met",
            "species_specific_interaction_structure": "not_met",
            "mixed_background_multi_species_pairing_rule": "not_met",
        },
    }
    (OUT_DIR / "summary.json").write_text(json.dumps(summary, indent=2), encoding="utf-8")

    lines = [
        "# Phase K Direct Interaction Summary",
        "",
        "**Date:** 2026-04-02",
        "**Phase:** K — Multi-Particle Interactions",
        "**Data Source:** `analysis/phase_k/phase_k_multi_fold_force_law.py`",
        "",
        "## Overview",
        "This package replaces the old one-dimensional overlap proxy with a direct 3D interaction-energy computation for same-background pair initial data.",
        "",
        "## Direct interaction-energy ranges",
        f"- scalar pair `Delta M(D)` range: {summary['key_results']['scalar_dm_range']}",
        f"- rich pair `Delta M(D)` range: {summary['key_results']['rich_dm_range']}",
        f"- phi-offsheet pair `Delta M(D)` range: {summary['key_results']['phi_offsheet_dm_range']}",
        "",
        "## Distance scaling",
        f"- scalar force log-log slope: {summary['key_results']['scalar_force_power_exponent']}",
        f"- scalar power-fit linear-space R^2: {summary['key_results']['scalar_force_power_r2_linear_space']}",
        f"- scalar exponential-fit linear-space R^2: {summary['key_results']['scalar_force_exp_r2_linear_space']}",
        "",
        "Interpretation: Phase K now has a real 3D interaction-energy dataset for the directly defined same-background case. But the refreshed direct data are species-blind across scalar, rich, and off-sheet same-background pairs. The remaining open gaps are both a mathematically clean mixed-background multi-species composition law and any direct evidence that different internal species interact differently.",
        "",
        "## Bottom line",
        "Phase K now supports a narrower but substantially stronger claim than the old proxy version: same-background pair initial data have a direct 3D interaction-energy density and an extractable force gradient. But the current direct runtime produces the same interaction data for scalar, rich, and off-sheet families, so it does not support particle-species interaction structure. What remains open is whether mixed-background species comparisons and Standard-Model-like polarity rules can be defined without additional many-object composition machinery.",
        "",
    ]
    (OUT_DIR / "summary.md").write_text("\n".join(lines), encoding="utf-8")
    return summary


def run_interaction_suite() -> None:
    OUT_DIR.mkdir(parents=True, exist_ok=True)
    solver = OrderedManifoldWaveSolver(CFG)
    profiles = {seed.label: solve_direct_radial_profile(seed, CFG) for seed in identical_seed_family()}
    bulk, pair_rows = bulk_force_law(solver, profiles)
    slices_1d = slice_1d_interactions(solver)
    slices_2d = slice_2d_interactions(solver)
    representative_pair_evolution(solver, profiles)
    build_summary(bulk, pair_rows, slices_1d, slices_2d)
    print(f"Phase K direct interaction tests complete. Results in {OUT_DIR.relative_to(ROOT)}")


if __name__ == "__main__":
    run_interaction_suite()
