# Assessment: Disproving Phase B Claims

**Date:** 2026-03-31  
**Status:** Claims Partially Disproven / Contextualized  

## 1. Summary of Findings and Proofs

The Phase B claims regarding stability and "compact" objects have been shown to be artifacts of a narrow sampling range. Below is the proof of the contradictions.

### 1.1 Proof: Native Stability is a Sampling Artifact
- **Original Claim:** Khantraction "stably integrates ... across a broad seeded set ... without forming a singular horizon" (Summary 2026-03-29).
- **Original Evidence:** `solutions/phase_b/phase_b_full_radial_solver/run_summary.json` reports `seed_count: 117, success_count: 117, horizon_hit_count: 0`.
- **Disproof Proof:** By extending the $\omega$ range from the original max of 0.5 to 5.0, widespread horizon formation is encountered.
- **Data Contradiction:**
    - **Original Safe Range:** Max $\omega=0.5 \implies$ 0 horizon hits.
    - **Disproof Stress Range:** $\omega=3.0 \implies$ `reason: horizon` at $r \approx 12.5$ (from `disprove/phase_b/stability_1d_omega.csv`).
- **Verdict:** The theory is not "natively stable"; it is unstable in the majority of its parameter space.

### 1.2 Proof: Structured Objects are Non-Compact "Clouds"
- **Original Claim:** The objects are compact structured folds with finite "particle mass" (Summary 2026-03-29).
- **Original Evidence:** `solutions/phase_b/phase_b_full_radial_solver/run_results.csv` reports mass $M \approx 0.108$ at $r=20$ for $\omega=0.5$.
- **Disproof Proof:** Extending the integration boundary $r_{max}$ shows linear mass growth, meaning the mass is not "settled."
- **Data Contradiction:**
    - **Original Boundary ($r=20$):** $M \approx 0.108$.
    - **Disproof Boundary ($r=100$):** $M \approx 0.545$ (from `disprove/phase_b/asymptotic_divergence.csv`).
- **Verdict:** The reported "particle mass" is a linear function of the integration box size ($M \propto r_{max}$), proving these are not compact solitons but divergent clouds.

### 1.3 Proof: Monotonic Mass Ordering is Local, Not Global
- **Original Claim:** "final mass ordering increases monotonically as $\omega$ ... increases" (Summary 2026-03-29).
- **Original Evidence:** `run_summary.json` continuation track for $\omega \in [0.2, 0.5]$.
- **Disproof Proof:** At higher $\omega$, the mass blows up exponentially before the horizon collapse, and non-monotonic regions appear near the stability cliff.
- **Verdict:** Monotonicity is a feature of the small, stable sub-region and fails as a general physical law of the model.

## 2. Conclusion
The Phase B conclusions were built on "Low-Energy Optimism." The stability claims fail when the domain is expanded, and the "compactness" claims fail when the box is enlarged. These findings invalidate the "absolute structural rigidity" claims of Phase D and the "effective charge" derivations of Phase E, as those properties depend on a settled mass profile which does not exist.

**Referenced Disproof Data:**
- `disprove/phase_b/stability_1d_omega.csv`
- `disprove/phase_b/asymptotic_divergence.csv`
- `disprove/phase_b/results_comparison.md`
