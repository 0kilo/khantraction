# Rigorous Disprove Plan: Phase B — The "Stability" Overgeneralization

**Objective:** Demonstrate that the "native stability" claimed in Phase B is a sampling artifact by finding "Stability Cliffs" and "Asymptotic Divergence" that contradict the "completed_without_failure" status.

---

## 1. Targeted Claims and Contradiction Mapping

| Claim from Summary 2026-03-29 | Original Evidence (solutions/phase_b/) | Disproof Strategy | Expected Contradiction |
| :--- | :--- | :--- | :--- |
| **C1: Native Stability.** "stably integrate ... across a broad seeded set ... without forming a singular horizon." | `run_summary.json` shows: `seed_count: 117, success_count: 117, horizon_hit_count: 0`. | Extend $\omega$ and $A_0$ (Central Amplitude) beyond the original "safe" seeds. | Show `horizon_hit: True` for parameters within the "active domain" (e.g., $\omega=3.0$). |
| **C2: Structured Objecthood.** "Khantraction natively supports a regular, coherent family of structured objects." | `run_results.csv` shows finite final masses $M \approx 0.17$. | Run integration with $r_{max} \gg 20.0$ (e.g., $r_{max} = 100$). | Show that $M(r)$ continues to grow linearly, contradicting the "settled" compact object claim. |
| **C3: Monotonic Mass.** "final mass ordering increases monotonically as $\omega$ ... increases." | `run_summary.json` continuation track shows increasing mass with $\omega$. | Search for "Stability Cliffs" where mass either blows up or collapses abruptly. | Show a non-monotonic or singular transition at high $\omega$ or high $\xi$. |

---

## 2. Execution Protocol

### 2.1 The Stability Cliff (Horizon Discovery)
- **Script:** `disprove/phase_b/test_stability_cliffs.py`
- **Action:** 
    1. Locate the "safe" range in `solutions/phase_b/phase_b_full_radial_solver/run_summary.json` (max $\omega = 0.5$).
    2. Sweep $\omega$ from $0.5$ to $5.0$.
    3. Document the *exact* $\omega$ value where the "0 horizon hits" claim fails.

### 2.2 The Asymptotic "Cloud" (Non-Compactness)
- **Script:** `disprove/phase_b/test_asymptotic_divergence.py`
- **Action:**
    1. Select `continuation_08` ($\omega=0.5, M=0.108$) from the original summary.
    2. Re-run with $r_{max} = 100$.
    3. Show that $M$ at $r=100$ is significantly larger than at $r=20$, proving the mass is not "settled" but is a divergent "cloud."

---

## 3. Implementation and Reporting
- Results will be saved in `disprove/phase_b/results_comparison.md`.
- Contradictions will be formatted as: 
    - **Original Assertion:** [Quote from summary]
    - **Counter-Evidence:** [New Data]
    - **Verdict:** [Specific contradiction statement]
