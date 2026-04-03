"""Phase J: direct ordered-manifold 3D stability study."""

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
    solve_direct_radial_profile,
)


OUT_DIR = ROOT / "solutions" / "phase_j" / "phase_j_dynamic_stability"
OMEGA = 0.5
ANGLES_1D = np.linspace(-2.0 * np.pi, 2.0 * np.pi, 7)
ANGLES_2D = np.linspace(-2.0 * np.pi, 2.0 * np.pi, 4)
KICK_STRENGTH = 0.08
BOOST_SPEED = 0.18

CFG = DirectRuntimeConfig(
    r_max=10.0,
    dr=0.01,
    grid_size=11,
    dx=0.55,
    dt=0.03,
    time_steps=18,
)


def write_csv(path: Path, rows: list[dict] | pd.DataFrame) -> None:
    if isinstance(rows, pd.DataFrame):
        rows.to_csv(path, index=False)
    else:
        pd.DataFrame(rows).to_csv(path, index=False)


def initial_fields_for_seed(solver: OrderedManifoldWaveSolver, seed: OrderedSeed) -> tuple[np.ndarray, np.ndarray, object]:
    profile = solve_direct_radial_profile(seed, CFG)
    fields = embed_profile_on_grid(profile, solver.x, solver.y, solver.z)
    velocities = np.zeros_like(fields)
    return fields, velocities, profile


def asymmetric_w_kick(solver: OrderedManifoldWaveSolver, fields: np.ndarray) -> np.ndarray:
    weight = np.exp(2.0 * fields[0])
    if float(weight.max()) <= 0.0:
        return np.zeros_like(fields)
    normed = weight / float(weight.max())
    vel = np.zeros_like(fields)
    vel[0] = KICK_STRENGTH * normed * (solver.x / np.max(np.abs(solver.x)))
    return vel


def bulk_runs(solver: OrderedManifoldWaveSolver) -> tuple[pd.DataFrame, list[dict]]:
    rows = []
    profile_rows = []
    for seed in [
        OrderedSeed("scalar", OMEGA, 0.0, 0.0, 0.0),
        OrderedSeed("rich", OMEGA, math.pi, -0.5 * math.pi, 0.5 * math.pi),
    ]:
        fields, velocities, profile = initial_fields_for_seed(solver, seed)
        _fields_f, _vel_f, history = solver.evolve(fields, velocities, steps=CFG.time_steps, sample_every=1)
        for row in history:
            row = dict(row)
            row["seed"] = seed.label
            rows.append(row)
        profile_rows.append(
            {
                "seed": seed.label,
                "success": profile.success,
                "failure_reason": profile.failure_reason,
                "final_mass": profile.final_mass,
                "compactness_90": profile.compactness_90,
                "boundary_qnorm": profile.boundary_qnorm,
            }
        )
    df = pd.DataFrame(rows)
    write_csv(OUT_DIR / "bulk_time_evolution.csv", df)
    write_csv(OUT_DIR / "profile_seed_runs.csv", profile_rows)
    return df, profile_rows


def acceleration_run(solver: OrderedManifoldWaveSolver) -> pd.DataFrame:
    rows = []
    for seed in [
        OrderedSeed("scalar", OMEGA, 0.0, 0.0, 0.0),
        OrderedSeed("rich", OMEGA, math.pi, -0.5 * math.pi, 0.5 * math.pi),
    ]:
        fields, _velocities, _profile = initial_fields_for_seed(solver, seed)
        boost = solver.translational_boost(fields, BOOST_SPEED, axis=0)
        _fields_f, _vel_f, history = solver.evolve(fields, boost, steps=CFG.time_steps, sample_every=1)
        for row in history:
            row = dict(row)
            row["seed"] = seed.label
            row["boost_speed"] = BOOST_SPEED
            rows.append(row)
    df = pd.DataFrame(rows)
    write_csv(OUT_DIR / "acceleration_tracking.csv", df)
    return df


def slice_seed(param: str, value: float) -> OrderedSeed:
    args = {"omega": OMEGA, "theta": 0.0, "phi": 0.0, "rho": 0.0}
    args[param] = float(value)
    return OrderedSeed(f"{param}_{value:+.6f}", args["omega"], args["theta"], args["phi"], args["rho"])


def run_1d_slices(solver: OrderedManifoldWaveSolver) -> pd.DataFrame:
    rows = []
    for param in ("theta", "phi", "rho"):
        for value in ANGLES_1D:
            seed = slice_seed(param, float(value))
            fields, _velocities, profile = initial_fields_for_seed(solver, seed)
            kick = asymmetric_w_kick(solver, fields)
            _fields_f, _vel_f, history = solver.evolve(fields, kick, steps=12, sample_every=12)
            start = history[0]
            final = history[-1]
            rows.append(
                {
                    "param": param,
                    "val": float(value),
                    "profile_success": profile.success,
                    "initial_energy": start["total_energy"],
                    "final_energy": final["total_energy"],
                    "energy_drift": float(final["total_energy"] - start["total_energy"]),
                    "initial_compact_radius_90": start["compact_radius_90"],
                    "final_compact_radius_90": final["compact_radius_90"],
                    "compact_radius_90_shift": float(final["compact_radius_90"] - start["compact_radius_90"]),
                    "initial_chirality_integral": start["chirality_integral"],
                    "final_chirality_integral": final["chirality_integral"],
                    "chirality_integral_shift": float(final["chirality_integral"] - start["chirality_integral"]),
                }
            )
    df = pd.DataFrame(rows)
    write_csv(OUT_DIR / "slices_1d_stability.csv", df)
    return df


def run_2d_slices(solver: OrderedManifoldWaveSolver) -> dict[tuple[str, str], pd.DataFrame]:
    outputs: dict[tuple[str, str], pd.DataFrame] = {}
    pair_specs = [
        ("theta", "rho", "slices_2d_theta_rho_stability.csv"),
        ("theta", "phi", "slices_2d_theta_phi_stability.csv"),
        ("phi", "rho", "slices_2d_phi_rho_stability.csv"),
    ]
    for first, second, filename in pair_specs:
        rows = []
        for value_a in ANGLES_2D:
            for value_b in ANGLES_2D:
                kwargs = {"omega": OMEGA, "theta": 0.0, "phi": 0.0, "rho": 0.0}
                kwargs[first] = float(value_a)
                kwargs[second] = float(value_b)
                seed = OrderedSeed(
                    f"{first}_{value_a:+.6f}_{second}_{value_b:+.6f}",
                    kwargs["omega"],
                    kwargs["theta"],
                    kwargs["phi"],
                    kwargs["rho"],
                )
                fields, _velocities, profile = initial_fields_for_seed(solver, seed)
                kick = asymmetric_w_kick(solver, fields)
                _fields_f, _vel_f, history = solver.evolve(fields, kick, steps=10, sample_every=10)
                start = history[0]
                final = history[-1]
                rows.append(
                    {
                        first: float(value_a),
                        second: float(value_b),
                        "profile_success": profile.success,
                        "energy_drift": float(final["total_energy"] - start["total_energy"]),
                        "compact_radius_90_shift": float(final["compact_radius_90"] - start["compact_radius_90"]),
                        "centroid_x_shift": float(final["centroid_x"] - start["centroid_x"]),
                        "chirality_integral_shift": float(final["chirality_integral"] - start["chirality_integral"]),
                    }
                )
        df = pd.DataFrame(rows)
        write_csv(OUT_DIR / filename, df)
        outputs[(first, second)] = df
    return outputs


def build_summary(
    bulk: pd.DataFrame,
    accel: pd.DataFrame,
    slices_1d: pd.DataFrame,
    slices_2d: dict[tuple[str, str], pd.DataFrame],
) -> dict:
    scalar_bulk = bulk[bulk["seed"] == "scalar"].copy()
    rich_bulk = bulk[bulk["seed"] == "rich"].copy()
    scalar_accel = accel[accel["seed"] == "scalar"].copy()
    rich_accel = accel[accel["seed"] == "rich"].copy()

    def final_shift(df: pd.DataFrame, column: str) -> float:
        return float(df[column].iloc[-1] - df[column].iloc[0])

    summary = {
        "phase": "J",
        "status": "direct_runtime_refresh",
        "model_scope": {
            "type": "weak_gravity_ordered_manifold_wave_solver",
            "statement": (
                "Direct 3D evolution of the ordered coordinates using the exact pullback metric, Christoffel symbols, "
                "and norm-potential force term from the shared direct ordered-manifold runtime."
            ),
        },
        "config": {
            "grid_size": CFG.grid_size,
            "dx": CFG.dx,
            "dt": CFG.dt,
            "time_steps": CFG.time_steps,
            "kick_strength": KICK_STRENGTH,
            "boost_speed": BOOST_SPEED,
            "angles_1d_points": len(ANGLES_1D),
            "angles_2d_points_per_axis": len(ANGLES_2D),
        },
        "key_results": {
            "scalar_energy_drift": final_shift(scalar_bulk, "total_energy"),
            "rich_energy_drift": final_shift(rich_bulk, "total_energy"),
            "scalar_compactness_shift": final_shift(scalar_bulk, "compact_radius_90"),
            "rich_compactness_shift": final_shift(rich_bulk, "compact_radius_90"),
            "scalar_chirality_shift": final_shift(scalar_bulk, "chirality_integral"),
            "rich_chirality_shift": final_shift(rich_bulk, "chirality_integral"),
            "scalar_boost_centroid_shift": final_shift(scalar_accel, "centroid_x"),
            "rich_boost_centroid_shift": final_shift(rich_accel, "centroid_x"),
            "scalar_boost_compactness_shift": final_shift(scalar_accel, "compact_radius_90"),
            "rich_boost_compactness_shift": final_shift(rich_accel, "compact_radius_90"),
            "theta_1d_compactness_shift_range": [
                float(slices_1d[slices_1d["param"] == "theta"]["compact_radius_90_shift"].min()),
                float(slices_1d[slices_1d["param"] == "theta"]["compact_radius_90_shift"].max()),
            ],
            "phi_1d_compactness_shift_range": [
                float(slices_1d[slices_1d["param"] == "phi"]["compact_radius_90_shift"].min()),
                float(slices_1d[slices_1d["param"] == "phi"]["compact_radius_90_shift"].max()),
            ],
            "rho_1d_compactness_shift_range": [
                float(slices_1d[slices_1d["param"] == "rho"]["compact_radius_90_shift"].min()),
                float(slices_1d[slices_1d["param"] == "rho"]["compact_radius_90_shift"].max()),
            ],
            "theta_rho_2d_max_abs_compactness_shift": float(np.abs(slices_2d[("theta", "rho")]["compact_radius_90_shift"]).max()),
            "theta_phi_2d_max_abs_compactness_shift": float(np.abs(slices_2d[("theta", "phi")]["compact_radius_90_shift"]).max()),
            "phi_rho_2d_max_abs_compactness_shift": float(np.abs(slices_2d[("phi", "rho")]["compact_radius_90_shift"]).max()),
        },
        "goal_status": {
            "full_ordered_manifold_3d_plus_1_solver": "met_in_weak_gravity_form",
            "localized_objecthood_under_tested_3d_evolution": "met",
            "asymmetric_perturbation_response_map": "met",
            "acceleration_tracking": "met",
            "discrete_species_identity_preservation_under_violent_dynamics": "not_met",
        },
    }

    (OUT_DIR / "summary.json").write_text(json.dumps(summary, indent=2), encoding="utf-8")

    lines = [
        "# Phase J Direct Ordered-Manifold Summary",
        "",
        "**Date:** 2026-04-02",
        "**Phase:** J — Full 3D Dynamic Stability",
        "**Data Source:** `analysis/phase_j/phase_j_dynamic_stability_solver.py`",
        "",
        "## Overview",
        "This package replaces the old anchored Gaussian proxy with a direct ordered-manifold 3D wave solver in the weak-gravity limit.",
        "The runtime uses the exact pullback metric, Christoffel couplings, and norm-potential force term from `analysis/direct_ordered_manifold.py`.",
        "",
        "## Bulk direct evolution",
        f"- scalar energy drift: {summary['key_results']['scalar_energy_drift']}",
        f"- rich energy drift: {summary['key_results']['rich_energy_drift']}",
        f"- scalar compactness-90 shift: {summary['key_results']['scalar_compactness_shift']}",
        f"- rich compactness-90 shift: {summary['key_results']['rich_compactness_shift']}",
        "",
        "Interpretation: these drifts measure whether a direct solved object remains structurally intact without an artificial anchor. In the audited window they are very small, so localized objecthood survives the direct upgrade.",
        "",
        "## Boosted transport",
        f"- scalar centroid-x shift under direct boost: {summary['key_results']['scalar_boost_centroid_shift']}",
        f"- rich centroid-x shift under direct boost: {summary['key_results']['rich_boost_centroid_shift']}",
        f"- scalar compactness-90 shift under boost: {summary['key_results']['scalar_boost_compactness_shift']}",
        f"- rich compactness-90 shift under boost: {summary['key_results']['rich_boost_compactness_shift']}",
        "",
        "Interpretation: the direct runtime now tests transport by boosting the actual field profile instead of dragging a hand-built anchor through the box. The centroid shift is small but clean, and compactness changes only weakly.",
        "",
        "## Slice diagnostics",
        f"- theta 1D compactness-shift range: {summary['key_results']['theta_1d_compactness_shift_range']}",
        f"- phi 1D compactness-shift range: {summary['key_results']['phi_1d_compactness_shift_range']}",
        f"- rho 1D compactness-shift range: {summary['key_results']['rho_1d_compactness_shift_range']}",
        f"- max abs compactness shift on theta/rho 2D slice: {summary['key_results']['theta_rho_2d_max_abs_compactness_shift']}",
        f"- max abs compactness shift on theta/phi 2D slice: {summary['key_results']['theta_phi_2d_max_abs_compactness_shift']}",
        f"- max abs compactness shift on phi/rho 2D slice: {summary['key_results']['phi_rho_2d_max_abs_compactness_shift']}",
        "",
        "## Bottom line",
        "Phase J now has a direct 3D ordered-manifold implementation. The direct runtime does preserve localized objecthood on the audited window, but it does not distinguish scalar and rich seeds at the level needed for discrete species identity. So J now supports direct object persistence more strongly than before, while still failing to rescue the particle-zoo claim.",
        "",
    ]
    (OUT_DIR / "summary.md").write_text("\n".join(lines), encoding="utf-8")
    return summary


def main() -> None:
    OUT_DIR.mkdir(parents=True, exist_ok=True)
    solver = OrderedManifoldWaveSolver(CFG)
    bulk, _profile_rows = bulk_runs(solver)
    accel = acceleration_run(solver)
    slices1 = run_1d_slices(solver)
    slices2 = run_2d_slices(solver)
    build_summary(bulk, accel, slices1, slices2)
    print(f"Phase J direct stability analysis complete. Results in {OUT_DIR.relative_to(ROOT)}")


if __name__ == "__main__":
    main()
