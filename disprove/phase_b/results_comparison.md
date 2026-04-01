# Results Comparison: Phase B Disproof

This report provides a side-by-side comparison between the original claims of Phase B and the counter-evidence obtained in the disproof phase.

## 1. The Stability "Cliff" (C1)

| Assertion from Summary 2026-03-29 | Original Data (solutions/phase_b/) | Disproof Evidence (disprove/phase_b/) | Verdict |
| :--- | :--- | :--- | :--- |
| "stably integrate ... across a broad seeded set ... without forming a singular horizon." | `run_summary.json` shows `horizon_hit_count: 0` for 117 seeds. | `stability_1d_omega.csv` shows `reason: horizon` starting at $\omega \approx 2.75$. | **Contradicted.** The "native stability" is a low-energy sampling artifact. |

### Data Comparison:
- **Original Max Sample ($\omega=0.5$):** `success: True`, `horizon_hit: False`.
- **Disproof Sample ($\omega=3.0$):** `success: False`, `reason: horizon` at $r \approx 12.5$.
- *Conclusion:* The model collapses into a singularity in a large portion of the "active domain" $[0, 5.0]$. The claim of general stability is false.

---

## 2. Asymptotic "Cloud" Divergence (C2)

| Assertion from Summary 2026-03-29 | Original Data (solutions/phase_b/) | Disproof Evidence (disprove/phase_b/) | Verdict |
| :--- | :--- | :--- | :--- |
| "Khantraction natively supports a regular, coherent family of structured objects." | `run_results.csv` shows finite masses (e.g., $M \approx 0.108$ at $r=20$). | `asymptotic_divergence.csv` shows $M \approx 0.545$ at $r=100$. | **Contradicted.** The objects are not compact; they are infinite-mass clouds. |

### Data Comparison ($\omega=0.5$):
- **Original Boundary ($r=20$):** $M \approx 0.108$.
- **Disproof Boundary ($r=100$):** $M \approx 0.545$.
- *Conclusion:* Mass scales near-linearly with the integration radius ($M(100) \approx 5 \times M(20)$). The reported "particle mass" is merely a function of the integration box size.

---

## 3. Monotonicity Failure (C3)

| Assertion from Summary 2026-03-29 | Original Data (solutions/phase_b/) | Disproof Evidence (disprove/phase_b/) | Verdict |
| :--- | :--- | :--- | :--- |
| "final mass ordering increases monotonically as $\omega$ ... increases." | `continuation_track` shows increasing mass for $\omega \in [0.2, 0.5]$. | `stability_1d_omega.csv` shows mass blowup followed by horizon collapse. | **Contextualized.** Monotonicity only holds in the unstable "low-energy" regime. |

### Result:
Phase B's "Structured Objecthood" is a numerical mirage caused by truncating the integration of divergent fields and avoiding high-energy parameters where the theory fails due to horizon formation.
