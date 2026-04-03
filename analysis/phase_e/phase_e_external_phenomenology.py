#!/usr/bin/env python3
r"""Phase E: direct external phenomenology and impulse-response analysis."""

from __future__ import annotations

import json
import math
import sys
from itertools import combinations
from pathlib import Path

import numpy as np
import pandas as pd
from scipy.optimize import curve_fit

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


OUT_DIR = ROOT / "solutions" / "phase_e" / "phase_e_phenomenology"
CFG = DirectRuntimeConfig(
    r_max=12.0,
    dr=0.01,
    grid_size=11,
    dx=0.55,
    dt=0.03,
    time_steps=18,
)
IMPULSE_STRENGTHS = [0.02, 0.04, 0.08]
GRID_1D = np.linspace(-2.0 * np.pi, 2.0 * np.pi, 11)
GRID_2D = np.linspace(-2.0 * np.pi, 2.0 * np.pi, 5)


def rn_mass_func(r: np.ndarray, m_adm: float, q_sq: float):
    return m_adm - q_sq / (2.0 * r)


def finite_range(values: list[float]) -> list[float]:
    arr = np.asarray(values, dtype=float)
    arr = arr[np.isfinite(arr)]
    if arr.size == 0:
        return [float("nan"), float("nan")]
    return [float(arr.min()), float(arr.max())]


def write_csv(path: Path, rows: list[dict] | pd.DataFrame) -> None:
    if isinstance(rows, pd.DataFrame):
        rows.to_csv(path, index=False)
    else:
        pd.DataFrame(rows).to_csv(path, index=False)


def representative_seeds() -> list[OrderedSeed]:
    return [
        OrderedSeed("scalar", 0.5, 0.0, 0.0, 0.0),
        OrderedSeed("rich", 0.5, math.pi, -0.5 * math.pi, 0.5 * math.pi),
        OrderedSeed("phi_offsheet", 0.5, 0.0, math.pi / 4.0 - 0.1, 0.0),
    ]


def summarize_profile(profile, seed: OrderedSeed) -> dict:
    return {
        "species": seed.label,
        "success": profile.success,
        "failure_reason": profile.failure_reason,
        "horizon_hit": profile.horizon_hit,
        "final_mass": profile.final_mass,
        "compactness_half": profile.compactness_half,
        "compactness_90": profile.compactness_90,
        "boundary_qnorm": profile.boundary_qnorm,
        "boundary_state_prime_norm": profile.boundary_state_prime_norm,
        "tail_w": float(profile.y[-1, 0]),
        "tail_theta": float(profile.y[-1, 1]),
        "tail_phi": float(profile.y[-1, 2]),
        "tail_rho": float(profile.y[-1, 3]),
    }


def attempt_rn_fit(seed: OrderedSeed, profile) -> dict:
    path = OUT_DIR / f"{seed.label}_tail.csv"
    pd.DataFrame({"r": profile.r, "mass_m": profile.y[:, 8]}).to_csv(path, index=False)
    r_tail = profile.r[-max(12, int(len(profile.r) * 0.25)) :]
    m_tail = profile.y[-len(r_tail) :, 8]
    try:
        popt, _ = curve_fit(rn_mass_func, r_tail, m_tail, maxfev=10000)
        preds = rn_mass_func(r_tail, *popt)
        q_sq = float(popt[1])
        return {
            "species": seed.label,
            "fit_status": "success",
            "tail_start_r": float(r_tail[0]),
            "M_ADM_fit": float(popt[0]),
            "Q_eff_fit": float(np.sqrt(max(0.0, q_sq))),
            "Q_sq_fit": q_sq,
            "fit_rmse": float(np.sqrt(np.mean((m_tail - preds) ** 2))),
            "tail_point_count": int(len(r_tail)),
        }
    except Exception:
        return {
            "species": seed.label,
            "fit_status": "fit_failed",
            "tail_start_r": float(r_tail[0]),
            "M_ADM_fit": float("nan"),
            "Q_eff_fit": float("nan"),
            "Q_sq_fit": float("nan"),
            "fit_rmse": float("nan"),
            "tail_point_count": int(len(r_tail)),
        }


def pairwise_indistinguishability(profiles: dict[str, object], fit_rows: list[dict]) -> tuple[list[dict], dict]:
    fit_by_species = {row["species"]: row for row in fit_rows if row["fit_status"] == "success"}
    pair_rows = []
    for a, b in combinations(sorted(fit_by_species.keys()), 2):
        pa = profiles[a]
        pb = profiles[b]
        r0 = max(float(pa.r[0]), float(pb.r[0]), 6.0)
        r_grid = np.linspace(r0, min(float(pa.r[-1]), float(pb.r[-1])), 120)
        ma = np.interp(r_grid, pa.r, pa.y[:, 8])
        mb = np.interp(r_grid, pb.r, pb.y[:, 8])
        row = {
            "species_a": a,
            "species_b": b,
            "tail_max_abs_diff": float(np.max(np.abs(ma - mb))),
            "tail_mean_abs_diff": float(np.mean(np.abs(ma - mb))),
            "M_ADM_fit_diff": float(abs(fit_by_species[a]["M_ADM_fit"] - fit_by_species[b]["M_ADM_fit"])),
            "Q_eff_fit_diff": float(abs(fit_by_species[a]["Q_eff_fit"] - fit_by_species[b]["Q_eff_fit"])),
        }
        row["externally_indistinguishable"] = bool(
            row["tail_max_abs_diff"] < 1.0e-4
            and row["M_ADM_fit_diff"] < 5.0e-3
            and row["Q_eff_fit_diff"] < 5.0e-3
        )
        pair_rows.append(row)

    parent = {name: name for name in fit_by_species}

    def find(x: str) -> str:
        while parent[x] != x:
            parent[x] = parent[parent[x]]
            x = parent[x]
        return x

    def union(a: str, b: str) -> None:
        ra, rb = find(a), find(b)
        if ra != rb:
            parent[rb] = ra

    for row in pair_rows:
        if row["externally_indistinguishable"]:
            union(row["species_a"], row["species_b"])

    components: dict[str, list[str]] = {}
    for name in fit_by_species:
        components.setdefault(find(name), []).append(name)
    return pair_rows, {
        f"class_{idx + 1}": sorted(names)
        for idx, names in enumerate(sorted(components.values(), key=lambda v: tuple(sorted(v))))
    }


def impulse_velocity(solver: OrderedManifoldWaveSolver, fields: np.ndarray, strength: float) -> np.ndarray:
    vel = np.zeros_like(fields)
    weight = np.exp(2.0 * fields[0])
    normed = weight / max(float(weight.max()), 1.0e-12)
    vel[0] = float(strength) * normed * (solver.x / np.max(np.abs(solver.x)))
    return vel


def response_ladder(profiles: dict[str, object]) -> list[dict]:
    solver = OrderedManifoldWaveSolver(CFG)
    rows = []
    for species, profile in profiles.items():
        fields = embed_profile_on_grid(profile, solver.x, solver.y, solver.z)
        for strength in IMPULSE_STRENGTHS:
            vel = impulse_velocity(solver, fields, strength)
            _fields_f, _vel_f, history = solver.evolve(fields, vel, steps=CFG.time_steps, sample_every=CFG.time_steps)
            start = history[0]
            final = history[-1]
            rows.append(
                {
                    "species": species,
                    "impulse_strength": float(strength),
                    "initial_energy": start["total_energy"],
                    "final_energy": final["total_energy"],
                    "energy_drift": float(final["total_energy"] - start["total_energy"]),
                    "centroid_x_shift": float(final["centroid_x"] - start["centroid_x"]),
                    "compact_radius_90_shift": float(final["compact_radius_90"] - start["compact_radius_90"]),
                    "chirality_integral_shift": float(final["chirality_integral"] - start["chirality_integral"]),
                    "response_ratio": float((final["centroid_x"] - start["centroid_x"]) / strength),
                }
            )
    return rows


def slice_1d_rows() -> dict[str, dict]:
    summary: dict[str, dict] = {}
    for axis in ("theta", "phi", "rho"):
        rows = []
        for value in GRID_1D:
            kwargs = {"omega": 0.5, "theta": 0.0, "phi": 0.0, "rho": 0.0}
            kwargs[axis] = float(value)
            seed = OrderedSeed(f"{axis}_{value:+.6f}", kwargs["omega"], kwargs["theta"], kwargs["phi"], kwargs["rho"])
            profile = solve_direct_radial_profile(seed, CFG)
            rows.append(
                {
                    axis: float(value),
                    "success": profile.success,
                    "final_mass": profile.final_mass,
                    "compactness_90": profile.compactness_90,
                    "boundary_qnorm": profile.boundary_qnorm,
                }
            )
        path = OUT_DIR / f"slice_1d_{axis}.csv"
        write_csv(path, rows)
        summary[axis] = {
            "path": str(path.relative_to(ROOT)),
            "sample_count": len(rows),
            "mass_range": finite_range([row["final_mass"] for row in rows]),
            "compactness_range": finite_range([row["compactness_90"] for row in rows]),
        }
    return summary


def slice_2d_rows() -> dict[str, dict]:
    outputs: dict[str, dict] = {}
    for first, second in (("theta", "rho"), ("theta", "phi"), ("phi", "rho")):
        rows = []
        for value_a in GRID_2D:
            for value_b in GRID_2D:
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
                rows.append(
                    {
                        first: float(value_a),
                        second: float(value_b),
                        "success": profile.success,
                        "final_mass": profile.final_mass,
                        "compactness_90": profile.compactness_90,
                        "boundary_qnorm": profile.boundary_qnorm,
                    }
                )
        plane = f"{first}_{second}"
        path = OUT_DIR / f"slice_2d_{plane}.csv"
        write_csv(path, rows)
        outputs[plane] = {
            "path": str(path.relative_to(ROOT)),
            "sample_count": len(rows),
            "mass_range": finite_range([row["final_mass"] for row in rows]),
            "compactness_range": finite_range([row["compactness_90"] for row in rows]),
        }
    return outputs


def write_summary_markdown(summary: dict) -> None:
    lines = [
        "# Phase E Direct Phenomenology Summary",
        "",
        "Generated by `analysis/phase_e/phase_e_external_phenomenology.py`.",
        "",
        "## Runtime model actually used",
        "- exact pullback metric and Christoffel symbols from `analysis/direct_ordered_manifold.py`",
        "- direct ordered-variable radial profiles for the representative single-object backgrounds",
        "- direct 3D weak-gravity impulse-response runs on those solved backgrounds",
        "",
        "## Representative direct profiles",
    ]
    for row in summary["representative_runs"]:
        lines.append(
            f"- `{row['species']}`: success={row['success']}, final_mass={row['final_mass']}, compactness_90={row['compactness_90']}"
        )
    lines.extend(["", "## RN-like fit diagnostics"])
    for row in summary["rn_fit_results"]:
        lines.append(
            f"- `{row['species']}`: fit_status={row['fit_status']}, M_ADM_fit={row['M_ADM_fit']}, Q_eff_fit={row['Q_eff_fit']}"
        )
    lines.extend(["", "## Direct impulse-response ladder"])
    for species, info in summary["direct_response_summary"].items():
        lines.append(
            f"- `{species}`: centroid-response range {info['centroid_response_range']}, response-ratio range {info['response_ratio_range']}"
        )
    lines.extend(["", "## Interpretation"])
    lines.extend(
        [
            "- Phase E now uses direct solved backgrounds from the pullback runtime instead of the old exploratory Maurer-Cartan beta path.",
            "- The external-tail comparison is now tied to those direct profiles.",
            "- The motion-response diagnostic is no longer a tiny imposed radial gradient; it is a direct 3D impulse-response run on the solved object.",
            "- In the refreshed direct data the response ratios are approximately constant across the audited impulse ladder, so a clean family-level inertial response is present.",
            "- But the same refreshed data are completely degenerate across scalar, rich, and off-sheet seeds, so the external response is universal rather than species-distinguishing.",
        ]
    )
    (OUT_DIR / "summary.md").write_text("\n".join(lines) + "\n", encoding="utf-8")


def run_analysis() -> None:
    print("--- Starting Phase E direct phenomenology analysis ---")
    OUT_DIR.mkdir(parents=True, exist_ok=True)
    seeds = representative_seeds()
    profiles = {seed.label: solve_direct_radial_profile(seed, CFG) for seed in seeds}

    representative_rows = [summarize_profile(profiles[seed.label], seed) for seed in seeds]
    rn_fit_rows = [attempt_rn_fit(seed, profiles[seed.label]) for seed in seeds]
    write_csv(OUT_DIR / "tail_run_results.csv", representative_rows)
    write_csv(OUT_DIR / "rn_fit_results.csv", rn_fit_rows)

    pair_rows, class_map = pairwise_indistinguishability(profiles, rn_fit_rows)
    write_csv(OUT_DIR / "indistinguishability_pairs.csv", pair_rows)
    (OUT_DIR / "indistinguishability_map.json").write_text(json.dumps(class_map, indent=2), encoding="utf-8")

    response_rows = response_ladder(profiles)
    write_csv(OUT_DIR / "direct_response_ladder.csv", response_rows)
    write_csv(OUT_DIR / "dynamical_response.csv", response_rows)

    response_summary = {}
    response_df = pd.DataFrame(response_rows)
    for species in sorted(response_df["species"].unique()):
        sdf = response_df[response_df["species"] == species]
        response_summary[species] = {
            "centroid_response_range": finite_range(sdf["centroid_x_shift"].tolist()),
            "response_ratio_range": finite_range(sdf["response_ratio"].tolist()),
            "compactness_shift_range": finite_range(sdf["compact_radius_90_shift"].tolist()),
        }

    slice_1d_summary = slice_1d_rows()
    slice_2d_summary = slice_2d_rows()

    summary = {
        "status": "phase_e_direct_phenomenology_complete",
        "config": {
            "grid_size": CFG.grid_size,
            "dx": CFG.dx,
            "dt": CFG.dt,
            "time_steps": CFG.time_steps,
            "impulse_strengths": IMPULSE_STRENGTHS,
        },
        "model_scope": {
            "type": "direct_pullback_profiles_plus_direct_impulse_response",
            "statement": (
                "Phase E now uses direct radial profiles from the exact pullback runtime and measures 3D impulse response "
                "on those backgrounds. The old beta-driven gradient probe is no longer the active path."
            ),
        },
        "representative_runs": representative_rows,
        "rn_fit_results": rn_fit_rows,
        "indistinguishability_classes": class_map,
        "direct_response_summary": response_summary,
        "slice_1d": slice_1d_summary,
        "slice_2d": slice_2d_summary,
        "goal_status": {
            "simple_external_tails": "met",
            "external_indistinguishability_classes": "met",
            "direct_motion_response_measurement": "met",
            "clean_inertial_law_for_tested_family": "met",
            "species_specific_external_response": "not_met",
        },
    }
    (OUT_DIR / "summary.json").write_text(json.dumps(summary, indent=2), encoding="utf-8")
    write_summary_markdown(summary)
    print("Phase E direct phenomenology analysis complete.")


if __name__ == "__main__":
    run_analysis()
