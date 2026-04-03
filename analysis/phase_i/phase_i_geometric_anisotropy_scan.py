"""Phase I: direct pullback anisotropy and coefficient replacement study."""

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
    OrderedSeed,
    default_single_seed_set,
    pullback_eigenvalues,
    solve_direct_radial_profile,
)


OUT_DIR = ROOT / "solutions" / "phase_i" / "phase_i_geometric_anisotropy_scan"
OMEGA = 0.5
ANGLES_1D = np.linspace(-2.0 * np.pi, 2.0 * np.pi, 33)
ANGLES_2D = np.linspace(-2.0 * np.pi, 2.0 * np.pi, 17)
PHI_DENSE = np.linspace(-2.0 * np.pi, 2.0 * np.pi, 4001)


def determinant(phi: float, omega: float) -> float:
    return float(np.exp(4.0 * omega) * np.cos(2.0 * phi))


def anisotropy_ratio(lambda_plus: float, lambda_minus: float) -> float:
    low = min(lambda_plus, lambda_minus)
    high = max(lambda_plus, lambda_minus)
    if low <= 0.0:
        return float("inf")
    return float(high / low)


def row_from_phi(phi: float, omega: float = OMEGA) -> dict:
    lambda_phi, lambda_plus, lambda_minus = pullback_eigenvalues(omega, phi)
    return {
        "phi": float(phi),
        "omega": float(omega),
        "lambda_phi": float(lambda_phi),
        "lambda_plus": float(lambda_plus),
        "lambda_minus": float(lambda_minus),
        "detJ": determinant(phi, omega),
        "gap_active_scale": float(abs(lambda_plus - lambda_minus)),
        "gap_unit_scale": float(2.0 * abs(np.sin(2.0 * phi))),
        "anisotropy_ratio": anisotropy_ratio(lambda_plus, lambda_minus),
    }


def exact_sheet_family(base: float) -> list[float]:
    values: list[float] = []
    for n in range(-4, 5):
        phi = base + n * np.pi
        if -2.0 * np.pi - 1.0e-12 <= phi <= 2.0 * np.pi + 1.0e-12:
            values.append(float(phi))
    return sorted(set(values))


def write_csv(path: Path, rows: list[dict] | pd.DataFrame) -> None:
    if isinstance(rows, pd.DataFrame):
        rows.to_csv(path, index=False)
    else:
        pd.DataFrame(rows).to_csv(path, index=False)


def generate_slice_outputs() -> tuple[list[dict], list[dict], list[dict], list[dict], list[dict], list[dict]]:
    phi_rows = [row_from_phi(phi) for phi in ANGLES_1D]
    lambda_phi0, lambda_plus0, lambda_minus0 = pullback_eigenvalues(OMEGA, 0.0)
    det_j0 = determinant(0.0, OMEGA)
    theta_rows = [
        {
            "theta": float(theta),
            "omega": float(OMEGA),
            "lambda_phi": lambda_phi0,
            "lambda_plus": lambda_plus0,
            "lambda_minus": lambda_minus0,
            "detJ": det_j0,
            "gap_active_scale": 0.0,
            "anisotropy_ratio": 1.0,
        }
        for theta in ANGLES_1D
    ]
    rho_rows = [
        {
            "rho": float(rho),
            "omega": float(OMEGA),
            "lambda_phi": lambda_phi0,
            "lambda_plus": lambda_plus0,
            "lambda_minus": lambda_minus0,
            "detJ": det_j0,
            "gap_active_scale": 0.0,
            "anisotropy_ratio": 1.0,
        }
        for rho in ANGLES_1D
    ]

    phi_rho_rows: list[dict] = []
    theta_phi_rows: list[dict] = []
    theta_rho_rows: list[dict] = []
    phi_anchor = np.pi / 8.0
    lambda_phi_anchor, lambda_plus_anchor, lambda_minus_anchor = pullback_eigenvalues(OMEGA, phi_anchor)
    det_anchor = determinant(phi_anchor, OMEGA)

    for phi in ANGLES_2D:
        base = row_from_phi(phi)
        for rho in ANGLES_2D:
            phi_rho_rows.append(
                {
                    "phi": float(phi),
                    "rho": float(rho),
                    "lambda_phi": base["lambda_phi"],
                    "lambda_plus": base["lambda_plus"],
                    "lambda_minus": base["lambda_minus"],
                    "detJ": base["detJ"],
                    "gap_active_scale": base["gap_active_scale"],
                    "anisotropy_ratio": base["anisotropy_ratio"],
                }
            )
        for theta in ANGLES_2D:
            theta_phi_rows.append(
                {
                    "theta": float(theta),
                    "phi": float(phi),
                    "lambda_phi": base["lambda_phi"],
                    "lambda_plus": base["lambda_plus"],
                    "lambda_minus": base["lambda_minus"],
                    "detJ": base["detJ"],
                    "gap_active_scale": base["gap_active_scale"],
                    "anisotropy_ratio": base["anisotropy_ratio"],
                }
            )

    for theta in ANGLES_2D:
        for rho in ANGLES_2D:
            theta_rho_rows.append(
                {
                    "theta": float(theta),
                    "rho": float(rho),
                    "phi_fixed": float(phi_anchor),
                    "lambda_phi": lambda_phi_anchor,
                    "lambda_plus": lambda_plus_anchor,
                    "lambda_minus": lambda_minus_anchor,
                    "detJ": det_anchor,
                    "gap_active_scale": float(abs(lambda_plus_anchor - lambda_minus_anchor)),
                    "anisotropy_ratio": anisotropy_ratio(lambda_plus_anchor, lambda_minus_anchor),
                }
            )

    write_csv(OUT_DIR / "slice_1d_phi.csv", phi_rows)
    write_csv(OUT_DIR / "slice_1d_theta.csv", theta_rows)
    write_csv(OUT_DIR / "slice_1d_rho.csv", rho_rows)
    write_csv(OUT_DIR / "slice_2d_phi_rho.csv", phi_rho_rows)
    write_csv(OUT_DIR / "slice_2d_theta_phi.csv", theta_phi_rows)
    write_csv(OUT_DIR / "slice_2d_theta_rho.csv", theta_rho_rows)
    return phi_rows, theta_rows, rho_rows, phi_rho_rows, theta_phi_rows, theta_rho_rows


def reference_tables() -> tuple[list[dict], dict]:
    reference_phis = [
        -7.0 * np.pi / 4.0,
        -5.0 * np.pi / 4.0,
        -3.0 * np.pi / 4.0,
        -np.pi / 4.0,
        0.0,
        np.pi / 8.0,
        np.pi / 4.0,
        3.0 * np.pi / 4.0,
        5.0 * np.pi / 4.0,
        7.0 * np.pi / 4.0,
    ]
    rows = []
    for phi in reference_phis:
        row = row_from_phi(phi)
        row["sheet_role"] = (
            "lambda_plus_zero"
            if np.isclose(row["lambda_plus"], 0.0, atol=1.0e-12)
            else "lambda_minus_zero"
            if np.isclose(row["lambda_minus"], 0.0, atol=1.0e-12)
            else "regular"
        )
        rows.append(row)

    sheet_families = {
        "lambda_plus_zero_sheets": exact_sheet_family(-np.pi / 4.0),
        "lambda_minus_zero_sheets": exact_sheet_family(np.pi / 4.0),
    }
    sheet_families["combined_singular_sheets"] = sorted(
        set(sheet_families["lambda_plus_zero_sheets"] + sheet_families["lambda_minus_zero_sheets"])
    )
    write_csv(OUT_DIR / "named_phi_reference.csv", rows)
    (OUT_DIR / "sheet_families.json").write_text(json.dumps(sheet_families, indent=2), encoding="utf-8")
    return rows, sheet_families


def width(rows: list[dict], key: str) -> float:
    values = np.asarray([row[key] for row in rows], dtype=float)
    finite = values[np.isfinite(values)]
    return float(finite.max() - finite.min()) if finite.size else float("nan")


def direct_profile_runs(cfg: DirectRuntimeConfig) -> list[dict]:
    rows: list[dict] = []
    for seed in default_single_seed_set():
        profile = solve_direct_radial_profile(seed, cfg)
        rows.append(
            {
                "label": seed.label,
                "omega": seed.omega,
                "theta": seed.theta,
                "phi": seed.phi,
                "rho": seed.rho,
                "success": profile.success,
                "failure_reason": profile.failure_reason,
                "horizon_hit": profile.horizon_hit,
                "final_mass": profile.final_mass,
                "compactness_half": profile.compactness_half,
                "compactness_90": profile.compactness_90,
                "boundary_qnorm": profile.boundary_qnorm,
                "boundary_state_prime_norm": profile.boundary_state_prime_norm,
                "tail_w": float(profile.y[-1, 0]),
            }
        )
    write_csv(OUT_DIR / "direct_profile_runs.csv", rows)
    return rows


def branch_stability_scan() -> list[dict]:
    rows: list[dict] = []
    lambda_values = [0.005, 0.01, 0.02, 0.04]
    amplitude_values = [0.01, 0.02, 0.03, 0.04]
    for lam in lambda_values:
        for amp in amplitude_values:
            cfg = DirectRuntimeConfig(lambda_q=lam, central_amplitude_base=amp, r_max=10.0, dr=0.01)
            profile = solve_direct_radial_profile(OrderedSeed("scalar", 0.5, 0.0, 0.0, 0.0), cfg)
            rows.append(
                {
                    "lambda_q": lam,
                    "central_amplitude_base": amp,
                    "success": profile.success,
                    "failure_reason": profile.failure_reason,
                    "final_mass": profile.final_mass,
                    "compactness_90": profile.compactness_90,
                    "boundary_qnorm": profile.boundary_qnorm,
                    "regular_branch_candidate": bool(
                        profile.success and not profile.horizon_hit and profile.boundary_qnorm < 0.08
                    ),
                }
            )
    write_csv(OUT_DIR / "branch_stability_scan.csv", rows)
    return rows


def direct_runtime_coefficients() -> dict:
    phis = np.linspace(-2.0 * np.pi, 2.0 * np.pi, 65)
    rows = []
    for phi in phis:
        lambda_phi, lambda_plus, lambda_minus = pullback_eigenvalues(OMEGA, float(phi))
        rows.append(
            {
                "phi": float(phi),
                "omega": OMEGA,
                "effective_w_stiffness": float(np.exp(2.0 * OMEGA)),
                "effective_phi_stiffness": lambda_phi,
                "effective_pair_symmetric_stiffness": lambda_plus,
                "effective_pair_antisymmetric_stiffness": lambda_minus,
                "theta_rho_mixing": float(np.exp(2.0 * OMEGA) * np.sin(2.0 * phi)),
            }
        )
    write_csv(OUT_DIR / "coefficient_map.csv", rows)
    coeffs = {
        "runtime_module": "analysis/direct_ordered_manifold.py",
        "replacement_statement": (
            "Downstream direct-runtime phases now use the exact pullback metric and Christoffel symbols "
            "instead of exploratory beta coefficients."
        ),
        "omega_fixed_for_scan": OMEGA,
        "coefficient_rows": len(rows),
    }
    (OUT_DIR / "direct_runtime_coefficients.json").write_text(json.dumps(coeffs, indent=2), encoding="utf-8")
    return coeffs


def build_summary(
    phi_rows: list[dict],
    theta_rows: list[dict],
    rho_rows: list[dict],
    phi_rho_rows: list[dict],
    theta_phi_rows: list[dict],
    theta_rho_rows: list[dict],
    sheet_families: dict,
    profile_rows: list[dict],
    stability_rows: list[dict],
) -> dict:
    ratios = []
    for phi in PHI_DENSE:
        _, lambda_plus, lambda_minus = pullback_eigenvalues(OMEGA, float(phi))
        ratio = anisotropy_ratio(lambda_plus, lambda_minus)
        if np.isfinite(ratio):
            ratios.append(ratio)

    profile_df = pd.DataFrame(profile_rows)
    stability_df = pd.DataFrame(stability_rows)
    stable_candidates = stability_df[stability_df["regular_branch_candidate"]]
    summary = {
        "phase": "I",
        "status": "direct_runtime_refresh",
        "model_scope": {
            "type": "pullback_geometry_plus_direct_ordered_radial_runtime",
            "statement": (
                "Phase I now combines the exact pullback anisotropy map with a direct ordered-variable runtime "
                "used by downstream Phases J, E, and K. The old exploratory beta coefficients are not used in that new chain."
            ),
        },
        "config": {
            "omega": OMEGA,
            "angles_1d_points": len(ANGLES_1D),
            "angles_2d_points_per_axis": len(ANGLES_2D),
            "dense_phi_points": len(PHI_DENSE),
        },
        "key_results": {
            "theta_slice_lambda_plus_width": width(theta_rows, "lambda_plus"),
            "phi_slice_lambda_plus_width": width(phi_rows, "lambda_plus"),
            "rho_slice_lambda_plus_width": width(rho_rows, "lambda_plus"),
            "theta_rho_lambda_minus_width": width(theta_rho_rows, "lambda_minus"),
            "theta_phi_lambda_minus_width": width(theta_phi_rows, "lambda_minus"),
            "phi_rho_lambda_minus_width": width(phi_rho_rows, "lambda_minus"),
            "max_regular_sampled_anisotropy_ratio": float(max(ratios)),
            "lambda_phi_constant": bool(np.allclose([row["lambda_phi"] for row in phi_rows], np.exp(2.0 * OMEGA))),
            "direct_runtime_profile_success_count": int(profile_df["success"].sum()),
            "direct_runtime_profile_mass_spread": float(profile_df["final_mass"].max() - profile_df["final_mass"].min()),
            "direct_runtime_profile_compactness_spread": float(profile_df["compactness_90"].max() - profile_df["compactness_90"].min()),
            "stable_branch_candidate_count": int(len(stable_candidates)),
            "stable_branch_lambda_range": [
                float(stable_candidates["lambda_q"].min()) if len(stable_candidates) else float("nan"),
                float(stable_candidates["lambda_q"].max()) if len(stable_candidates) else float("nan"),
            ],
            "stable_branch_amplitude_range": [
                float(stable_candidates["central_amplitude_base"].min()) if len(stable_candidates) else float("nan"),
                float(stable_candidates["central_amplitude_base"].max()) if len(stable_candidates) else float("nan"),
            ],
            "active_scale_gap_at_phi_pi_over_8": float(abs(pullback_eigenvalues(OMEGA, np.pi / 8.0)[1] - pullback_eigenvalues(OMEGA, np.pi / 8.0)[2])),
        },
        "goal_status": {
            "native_geometric_anisotropy_identified": "met",
            "beta_replacement_in_new_direct_solver_chain": "met",
            "exact_self_coupling_limits_for_branch_stability": "partially_met",
            "mapping_to_physical_observables": "partially_met",
        },
        "downstream_link": {
            "shared_runtime_module": "analysis/direct_ordered_manifold.py",
            "used_by": [
                "analysis/phase_j/phase_j_dynamic_stability_solver.py",
                "analysis/phase_e/phase_e_external_phenomenology.py",
                "analysis/phase_k/phase_k_multi_fold_force_law.py",
            ],
        },
    }

    bulk_summary = {
        "omega": OMEGA,
        "max_regular_sampled_anisotropy_ratio": float(max(ratios)),
        "lambda_plus_zero_sheets": sheet_families["lambda_plus_zero_sheets"],
        "lambda_minus_zero_sheets": sheet_families["lambda_minus_zero_sheets"],
        "combined_singular_sheets": sheet_families["combined_singular_sheets"],
        "stable_branch_candidate_count": int(len(stable_candidates)),
        "direct_profile_labels": profile_df["label"].tolist(),
    }

    (OUT_DIR / "summary.json").write_text(json.dumps(summary, indent=2), encoding="utf-8")
    (OUT_DIR / "bulk_summary.json").write_text(json.dumps(bulk_summary, indent=2), encoding="utf-8")

    lines = [
        "# Phase I Direct Pullback Runtime Summary",
        "",
        "**Date:** 2026-04-02",
        "**Phase:** I — First-Principles Derivation of Constants",
        "**Data Source:** `analysis/phase_i/phase_i_geometric_anisotropy_scan.py`",
        "",
        "## Overview",
        "This package now does more than scan the pullback geometry.",
        "It keeps the exact pullback eigenvalue study, adds a direct ordered-variable radial runtime, and uses that runtime as the coefficient bridge for downstream Phases J, E, and K.",
        "",
        "## Geometry results",
        f"- `lambda_phi` stays constant at `e^(2omega) = {np.exp(2.0 * OMEGA)}` for fixed `omega = {OMEGA}`.",
        f"- maximum regular sampled anisotropy ratio on the dense phi sweep: {summary['key_results']['max_regular_sampled_anisotropy_ratio']}",
        f"- active-scale paired-mode gap at `phi = pi/8`: {summary['key_results']['active_scale_gap_at_phi_pi_over_8']}",
        "",
        "## Direct runtime bridge",
        f"- direct profile success count on the representative seed set: {summary['key_results']['direct_runtime_profile_success_count']}",
        f"- direct profile mass spread across scalar/rich/off-sheet seeds: {summary['key_results']['direct_runtime_profile_mass_spread']}",
        f"- direct profile compactness-90 spread across scalar/rich/off-sheet seeds: {summary['key_results']['direct_runtime_profile_compactness_spread']}",
        "- downstream direct-runtime phases now import the exact pullback metric and Christoffel symbols from `analysis/direct_ordered_manifold.py`.",
        "- the old exploratory `beta_a` coefficients are not used in that new chain.",
        "",
        "## Branch-stability scan",
        f"- regular branch candidate count on the `(lambda_q, A0)` scan: {summary['key_results']['stable_branch_candidate_count']}",
        f"- regular candidate lambda range: {summary['key_results']['stable_branch_lambda_range']}",
        f"- regular candidate central-amplitude range: {summary['key_results']['stable_branch_amplitude_range']}",
        "",
        "Interpretation: Phase I now supports a real coefficient replacement claim for the new direct runtime. The exact pullback geometry is no longer only an interpretation layer; it is the active kinetic structure used downstream. But the direct representative seed set is degenerate in mass and compactness, so coefficient replacement alone does not reproduce the exploratory trait splitting. The self-coupling scan is still empirical and does not yet amount to a full analytical stability bound.",
        "",
        "## Bottom line",
        "Phase I now closes at a stronger level than the audit-only version. The exact pullback anisotropy remains the controlling geometric mechanism, and the new direct runtime uses that mechanism in place of the exploratory beta-coefficient path. But the resulting direct representative profiles remain degenerate, so the new chain supports universal objecthood rather than distinct particle-like species. What remains open is a full analytical self-coupling derivation and a sharper mapping from those direct coefficients to physical observables.",
        "",
    ]
    (OUT_DIR / "summary.md").write_text("\n".join(lines), encoding="utf-8")
    return summary


def main() -> None:
    OUT_DIR.mkdir(parents=True, exist_ok=True)
    phi_rows, theta_rows, rho_rows, phi_rho_rows, theta_phi_rows, theta_rho_rows = generate_slice_outputs()
    _reference_rows, sheet_families = reference_tables()
    _coeffs = direct_runtime_coefficients()
    cfg = DirectRuntimeConfig(r_max=12.0, dr=0.01, grid_size=15, dx=0.45, dt=0.04, time_steps=24)
    profile_rows = direct_profile_runs(cfg)
    stability_rows = branch_stability_scan()
    build_summary(
        phi_rows,
        theta_rows,
        rho_rows,
        phi_rho_rows,
        theta_phi_rows,
        theta_rho_rows,
        sheet_families,
        profile_rows,
        stability_rows,
    )
    print(f"Phase I direct pullback analysis complete. Results in {OUT_DIR.relative_to(ROOT)}")


if __name__ == "__main__":
    main()
