from __future__ import annotations

import json
from pathlib import Path

import numpy as np
import pandas as pd


ROOT = Path(__file__).resolve().parents[2]
OUTPUT_DIR = ROOT / "solutions" / "phase_m" / "phase_m_creation_annihilation"
CREATION_THRESHOLD = 2.55
PAIR_REST_ENERGY = 1.0
ANNIHILATION_TOLERANCE = 0.08
PHI_WEIGHT = 0.25
THETA_WEIGHT = 0.25
RHO_WEIGHT = 0.25


def wrap_angle(angle: float) -> float:
    return float(np.arctan2(np.sin(angle), np.cos(angle)))


def periodic_gap(a: float, b: float) -> float:
    return abs(wrap_angle(a - b))


def get_chirality(params: dict[str, float]) -> float:
    """
    Audited Phase G chirality operator.

    Phase G established that chirality is controlled by phi alone:
    chi = cos(2 phi).
    """
    return float(np.cos(2.0 * params["phi"]))


def expected_partner_phi(params_left: dict[str, float]) -> float:
    """
    Exact enantiomer partner under the audited topological chiral flip.
    """
    return wrap_angle(params_left["phi"] - (np.pi / 2.0))


def simulate_annihilation(params_left: dict[str, float], params_right: dict[str, float]):
    """
    Simplified annihilation proxy.

    The active runtime does not solve a dynamical collision. It scores how
    closely the right state matches the audited exact enantiomer of the fixed
    left anchor, using:

    - chirality cancellation: |chi_L + chi_R|
    - right-state distance from the expected partner phi
    - theta/rho alignment with the left anchor
    """
    chi_left = get_chirality(params_left)
    chi_right = get_chirality(params_right)

    partner_phi = expected_partner_phi(params_left)
    chi_gap = abs(chi_left + chi_right)
    phi_gap = periodic_gap(params_right["phi"], partner_phi)
    theta_gap = periodic_gap(params_right["theta"], params_left["theta"])
    rho_gap = periodic_gap(params_right["rho"], params_left["rho"])

    pair_score = chi_gap + PHI_WEIGHT * phi_gap + THETA_WEIGHT * theta_gap + RHO_WEIGHT * rho_gap
    final_status = "Vacuum" if pair_score < ANNIHILATION_TOLERANCE else "Residual Dipole"
    released_energy_proxy = PAIR_REST_ENERGY if final_status == "Vacuum" else PAIR_REST_ENERGY * max(0.0, 1.0 - min(pair_score, 1.0))

    return {
        "status": final_status,
        "chi_left": chi_left,
        "chi_right": chi_right,
        "chi_gap": chi_gap,
        "expected_partner_phi": partner_phi,
        "phi_gap": phi_gap,
        "theta_gap": theta_gap,
        "rho_gap": rho_gap,
        "pair_score": pair_score,
        "released_energy_proxy": released_energy_proxy,
    }


def creation_sheet_susceptibility(phi: float) -> float:
    """
    Hand-built singular-sheet susceptibility used by the active creation model.
    """
    return float(1.0 / (abs(np.cos(2.0 * phi)) + 0.1))


def simulate_creation(initial_energy: float):
    """
    Simplified creation proxy.

    The active runtime uses an imposed energy threshold, not a dynamical vacuum
    tearing solve.
    """
    if initial_energy >= CREATION_THRESHOLD:
        return {
            "status": "L+R Pair Created",
            "surplus": float(initial_energy - PAIR_REST_ENERGY),
            "net_chirality": 0.0,
        }
    return {
        "status": "Sub-threshold fluctuation",
        "surplus": float(initial_energy),
        "net_chirality": 0.0,
    }


def nearest_row(df: pd.DataFrame, column: str, target: float) -> dict[str, float]:
    idx = (df[column] - target).abs().idxmin()
    row = df.loc[idx]
    out = {}
    for key in row.index:
        value = row[key]
        if isinstance(value, (np.floating, float, np.integer, int)):
            out[key] = float(value)
        else:
            out[key] = value
    return out


def run_pair_suite() -> None:
    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)

    right_anchor = {"w": 0.5, "theta": np.pi / 2.0, "phi": np.pi / 8.0, "rho": 0.0}
    left_anchor = {"w": 0.5, "theta": np.pi / 2.0, "phi": 5.0 * np.pi / 8.0, "rho": 0.0}
    parity_partner = {"w": 0.5, "theta": np.pi / 2.0, "phi": -np.pi / 8.0, "rho": 0.0}
    same_handed_copy = dict(left_anchor)

    energies = np.linspace(0.0, 5.0, 50)
    creation_rows = []
    for energy in energies:
        event = simulate_creation(float(energy))
        creation_rows.append({"input_energy": float(energy), **event})
    creation_df = pd.DataFrame(creation_rows)
    creation_df.to_csv(OUTPUT_DIR / "bulk_creation_sweep.csv", index=False)

    angles_1d = np.linspace(-2.0 * np.pi, 2.0 * np.pi, 100)
    theta_rows = []
    phi_rows = []
    rho_rows = []
    for angle in angles_1d:
        right_state = dict(right_anchor)
        right_state["theta"] = float(angle)
        theta_rows.append({"param": "theta", "val": float(angle), **simulate_annihilation(left_anchor, right_state)})

        right_state = dict(right_anchor)
        right_state["phi"] = float(angle)
        phi_rows.append({"param": "phi", "val": float(angle), **simulate_annihilation(left_anchor, right_state)})

        right_state = dict(right_anchor)
        right_state["rho"] = float(angle)
        rho_rows.append({"param": "rho", "val": float(angle), **simulate_annihilation(left_anchor, right_state)})

    theta_df = pd.DataFrame(theta_rows)
    phi_df = pd.DataFrame(phi_rows)
    rho_df = pd.DataFrame(rho_rows)
    theta_df.to_csv(OUTPUT_DIR / "slices_1d_annihilation_theta.csv", index=False)
    phi_df.to_csv(OUTPUT_DIR / "slices_1d_annihilation_phi.csv", index=False)
    rho_df.to_csv(OUTPUT_DIR / "slices_1d_annihilation_rho.csv", index=False)
    pd.concat([theta_df, phi_df, rho_df], ignore_index=True).to_csv(OUTPUT_DIR / "slices_1d_annihilation.csv", index=False)

    pair_reference_rows = []
    for label, right_state in [
        ("exact_enantiomer", right_anchor),
        ("parity_partner", parity_partner),
        ("same_handed_copy", same_handed_copy),
    ]:
        pair_reference_rows.append(
            {
                "label": label,
                "theta": right_state["theta"],
                "phi": right_state["phi"],
                "rho": right_state["rho"],
                **simulate_annihilation(left_anchor, right_state),
            }
        )
    pair_reference_df = pd.DataFrame(pair_reference_rows)
    pair_reference_df.to_csv(OUTPUT_DIR / "pair_reference_checks.csv", index=False)

    res_2d = 30
    angles_2d = np.linspace(-2.0 * np.pi, 2.0 * np.pi, res_2d)
    theta_phi_rows = []
    theta_rho_rows = []
    phi_rho_rows = []
    for a1 in angles_2d:
        for a2 in angles_2d:
            theta_phi_rows.append(
                {
                    "theta": float(a1),
                    "phi": float(a2),
                    "rho": 0.0,
                    "creation_prob_proxy": creation_sheet_susceptibility(float(a2)),
                    "chi": float(np.cos(2.0 * a2)),
                }
            )
            theta_rho_rows.append(
                {
                    "theta": float(a1),
                    "phi": 0.0,
                    "rho": float(a2),
                    "creation_prob_proxy": creation_sheet_susceptibility(0.0),
                    "chi": float(np.cos(0.0)),
                }
            )
            phi_rho_rows.append(
                {
                    "theta": 0.0,
                    "phi": float(a1),
                    "rho": float(a2),
                    "creation_prob_proxy": creation_sheet_susceptibility(float(a1)),
                    "chi": float(np.cos(2.0 * a1)),
                }
            )

    theta_phi_df = pd.DataFrame(theta_phi_rows)
    theta_rho_df = pd.DataFrame(theta_rho_rows)
    phi_rho_df = pd.DataFrame(phi_rho_rows)
    theta_phi_df.to_csv(OUTPUT_DIR / "slices_2d_creation_theta_phi.csv", index=False)
    theta_rho_df.to_csv(OUTPUT_DIR / "slices_2d_creation_theta_rho.csv", index=False)
    phi_rho_df.to_csv(OUTPUT_DIR / "slices_2d_creation_phi_rho.csv", index=False)
    theta_phi_df.to_csv(OUTPUT_DIR / "slices_2d_creation_probability.csv", index=False)

    phi_reference_df = pd.DataFrame(
        [
            {"label": "phi_zero", "phi": 0.0, "creation_prob_proxy": creation_sheet_susceptibility(0.0), "chi": np.cos(0.0)},
            {"label": "phi_pos_pi_over_4", "phi": np.pi / 4.0, "creation_prob_proxy": creation_sheet_susceptibility(np.pi / 4.0), "chi": np.cos(np.pi / 2.0)},
            {"label": "phi_neg_pi_over_4", "phi": -np.pi / 4.0, "creation_prob_proxy": creation_sheet_susceptibility(-np.pi / 4.0), "chi": np.cos(-np.pi / 2.0)},
            {"label": "phi_pi_over_2", "phi": np.pi / 2.0, "creation_prob_proxy": creation_sheet_susceptibility(np.pi / 2.0), "chi": np.cos(np.pi)},
        ]
    )
    phi_reference_df.to_csv(OUTPUT_DIR / "creation_phi_reference.csv", index=False)

    created_rows = creation_df[creation_df["status"] == "L+R Pair Created"]
    first_created_energy = float(created_rows["input_energy"].iloc[0]) if not created_rows.empty else None

    summary = {
        "status": "audited_pair_lifecycle_refresh",
        "type": "pair_lifecycle_proxy",
        "chirality_formula": "cos(2phi)",
        "creation_gate_type": "fixed_threshold_plus_sheet_susceptibility_proxy",
        "annihilation_tolerance": ANNIHILATION_TOLERANCE,
        "imposed_creation_threshold": CREATION_THRESHOLD,
        "sampled_first_created_energy": first_created_energy,
        "pair_rest_energy_proxy": PAIR_REST_ENERGY,
        "left_anchor": {key: float(value) for key, value in left_anchor.items()},
        "right_anchor": {key: float(value) for key, value in right_anchor.items()},
        "pair_reference_checks": pair_reference_df.to_dict(orient="records"),
        "phi_reference_points": {
            "near_zero": nearest_row(phi_reference_df, "phi", 0.0),
            "near_pos_pi_over_4": nearest_row(phi_reference_df, "phi", np.pi / 4.0),
            "near_neg_pi_over_4": nearest_row(phi_reference_df, "phi", -np.pi / 4.0),
            "near_pi_over_2": nearest_row(phi_reference_df, "phi", np.pi / 2.0),
        },
        "annihilation_status_counts": {
            "theta": theta_df["status"].value_counts().to_dict(),
            "phi": phi_df["status"].value_counts().to_dict(),
            "rho": rho_df["status"].value_counts().to_dict(),
        },
        "slice_2d_rows": {
            "theta_phi": int(len(theta_phi_df)),
            "theta_rho": int(len(theta_rho_df)),
            "phi_rho": int(len(phi_rho_df)),
        },
        "creation_prob_proxy_range": {
            "theta_phi": [float(theta_phi_df["creation_prob_proxy"].min()), float(theta_phi_df["creation_prob_proxy"].max())],
            "theta_rho": [float(theta_rho_df["creation_prob_proxy"].min()), float(theta_rho_df["creation_prob_proxy"].max())],
            "phi_rho": [float(phi_rho_df["creation_prob_proxy"].min()), float(phi_rho_df["creation_prob_proxy"].max())],
        },
        "conclusion": (
            "The active Phase M package supports a chirality-cancellation and sheet-susceptibility pair-lifecycle proxy. "
            "It does not directly implement dynamical annihilation collisions or vacuum tearing."
        ),
    }
    with (OUTPUT_DIR / "summary.json").open("w", encoding="utf-8") as handle:
        json.dump(summary, handle, indent=2)

    summary_md = """# Phase M Analysis Summary: Pair Creation and Annihilation

## 1. Objective
Interpret the refreshed Phase M outputs for the active pair-lifecycle runtime.

## 2. What the active runtime is
The current Phase M script is a pair-lifecycle proxy, not a dynamical field solve.

It uses:
- audited chirality `chi = cos(2phi)`,
- a pair-matching annihilation score,
- an imposed creation threshold,
- and a hand-built singular-sheet susceptibility.

## 3. Main regenerated outputs
- `bulk_creation_sweep.csv`: fixed-threshold creation gate over energy.
- `slices_1d_annihilation_*.csv`: annihilation score across theta, phi, and rho.
- `pair_reference_checks.csv`: exact enantiomer, parity partner, and same-handed reference comparisons.
- `slices_2d_creation_*.csv`: full-domain sheet-susceptibility maps.
- `creation_phi_reference.csv`: named phi reference points for the creation susceptibility.

## 4. Interpretation
- The exact enantiomer reference returns the `Vacuum` state in the current proxy.
- Parity and same-handed references do not.
- Creation turns on only after the imposed threshold is crossed in the bulk gate.
- Creation susceptibility is strongest near the singular sheets and flat on the theta-rho slice with phi fixed at zero.

## 5. Limits
These outputs do not prove a dynamical collision solve, Maurer-Cartan vielbein cancellation in spacetime, or vacuum tearing from first principles.
"""
    with (OUTPUT_DIR / "summary.md").open("w", encoding="utf-8") as handle:
        handle.write(summary_md)

    print(f"Phase M pair-lifecycle refresh complete. Results in {OUTPUT_DIR}")


if __name__ == "__main__":
    run_pair_suite()
