# Missing Goals and Implementation Roadmap

This file tracks goals defined in `notes/classical_exploration_plan.md` and `notes/real_physics_transition_plan.md` that were identified as missing or incomplete.

---

## Project-Level Closure Decision (2026-04-02)

The saved project-level synthesis is:

- `notes/2026-04-02_direct_data_closure_plan.md`
- `summary/2026-04-02_gap_closure_summary.md`
- `summary/2026-04-02_khantraction_model_conclusion.md`

The resulting decision is:

- the classical particle-level verdict was decided on the implemented I, J, E, and K direct chain,
- H, L, and M remain deferred out of the current classical verdict,
- several older claims remain retired,
- and the direct implementation result is that Khantraction supports universal localized objecthood rather than a particle-level species model.

---

## Phase C — Distinct Classical Characteristics

### 1. Incomplete Comparison Metrics (Goal 2) - COMPLETED
**Status:** Completed on 2026-03-29.
**Implementation:**
- Updated `PhaseCMCRadialSolver` to calculate:
    - **Mass 90% Radius ($r_{90}$)**: Extracted from mass profiles.
    - **Core-to-Bulk Ratio**: Calculated as `core_mass_fraction` (r < 1.0).
    - **Profile Skewness**: Implemented `skewness_proxy` using the mean radius of mass distribution.
- **Results:** Verified distinct structural signatures (e.g., Scalar core fraction ~0.0002 vs Phi-dom ~0.027).

### 2. Exhaustive Slice Protocol (Section 3.2) - COMPLETED
**Status:** Completed on 2026-03-29.
**Implementation:**
- Executed the **full combinatorial matrix** of slices:
    - **1D Slices:** Phi, Theta, and Rho sweeps across $[-2\pi, 2\pi]$.
    - **2D Slices:** Theta/Rho, Phi/Theta, and Phi/Rho pairings.
- **Results:** Confirmed that while Phi is the primary controller, complex cross-couplings exist in the 2D sector, fulfilling the exhaustive mapping requirement.

---

## Phase D — Identity and Persistence

### 1. Exhaustive Slice Protocol (Section 3.2) - COMPLETED
**Status:** Completed on 2026-03-30.
**Implementation:**
- Executed the full combinatorial matrix of slices for identity/compactness:
    - **1D Slices:** Theta and Rho sweeps across $[-2\pi, 2\pi]$.
    - **2D Slices:** Phi/Theta and Phi/Rho pairings.
- **Results:** Confirmed that the "identity basins" are global topological features, not coordinate artifacts.

### 2. External Pressure Rigidity Test (Goal 5) - REVISED AFTER AUDIT
**Status:** The old completion claim was replaced on 2026-04-02.
**Implementation:** 
- A boundary-compression test exists, but the refreshed Phase D audit no longer treats it as proof of absolute rigidity.
- **Results:** The old absolute-rigidity wording was too strong. Phase D closes on local identity structure, while broader rigidity under amplitude and boundary stress remains open.

---

## Phase E — External Particle-Likeness

### 1. Exhaustive Slice Protocol (Section 3.2) - COMPLETED
**Status:** Completed after audit refresh on 2026-04-02.
**Implementation:**
- Executed the full combinatorial matrix of slices:
    - **1D Slices:** Theta, Phi, and Rho sweeps across $[-2\pi, 2\pi]$.
    - **2D Slices:** Theta/Rho, Phi/Theta, and Phi/Rho pairings across $[-2\pi, 2\pi]^2$.
- **Results:** Confirmed that the external mass proxy remains strongly phi-dominated, with theta nearly flat on the audited 1D slice and rho providing a secondary standalone effect.

### 2. External Indistinguishability Classes (Goal 2) - COMPLETED
**Status:** Completed after audit refresh on 2026-04-02.
**Implementation:**
- Implemented pairwise tail and RN-fit comparisons on the successful full-domain survivor runs.
- Output `indistinguishability_map.json` and `indistinguishability_pairs.csv` to group externally matching survivor sectors.

---

## Phase F — Classical Hosting Properties

### 1. Exhaustive Slice Protocol (Section 3.2) - COMPLETED
**Status:** Completed after audit refresh on 2026-04-02.
**Implementation:**
- Executed the full combinatorial matrix of slices:
    - **1D Slices:** Theta, Phi, and Rho sweeps across $[-2\pi, 2\pi]$.
    - **2D Slices:** Theta/Rho, Phi/Theta, and Phi/Rho pairings across $[-2\pi, 2\pi]^2$.
- **Results:** Confirmed that probe response varies globally across the angular domain and is primarily phi-controlled. The refreshed audit no longer treats these maps as proof of strong hosting basins.

---

## Phase G — Classical Rotational / Handedness Properties

### 1. Exhaustive Slice Protocol (Section 3.2) - COMPLETED
**Status:** Completed after audit refresh on 2026-04-02.
**Implementation:**
- Executed the full combinatorial matrix of slices for chirality density $\chi$:
    - **1D Slices:** Theta, Phi, and Rho sweeps across $[-2\pi, 2\pi]$.
    - **2D Slices:** Theta/Rho, Phi/Theta, and Phi/Rho pairings across $[-2\pi, 2\pi]^2$.
- **Results:** Confirmed that chirality sign is controlled by phi alone; theta and rho are spectators for handedness.

### 2. Rotational Stability Scans - REVISED AFTER AUDIT
**Status:** The old completion claim was replaced on 2026-04-02.
**Implementation:**
- The existing `rotational_stability.csv` file is an analytic proxy based on mass rescaling, not a solver-backed rotational dynamics run.
- **Results:** Phase G closes on handedness architecture. Rotational stability and angular-momentum hosting remain open.

---

## Phase H — Return to Stronger Quantum-Facing Work

### 1. Exhaustive Slice Protocol (Section 3.2) - COMPLETED AFTER AUDIT REFRESH
**Status:** Completed after audit refresh on 2026-04-02.
**Implementation:**
- Rebuilt the Phase H slice package so it now executes the full combinatorial matrix:
    - **1D Slices:** Theta, Phi, and Rho sweeps across $[-2\pi, 2\pi]$.
    - **2D Slices:** Phi/Theta, Theta/Rho, and Phi/Rho pairings across $[-2\pi, 2\pi]^2$.
- **Results:** The refreshed proxy is phi-only. Theta and rho are exact spectators, while phi controls the proxy spectrum through $\chi = \cos(2\phi)$.

### 2. Loading Effects on Spectra (Goal 3) - COMPLETED AS A PROXY RESULT
**Status:** Completed after audit refresh on 2026-04-02.
**Implementation:**
- Kept the loading term in the Phase H resonator proxy and reran the ground-state scan.
- **Results:** Verified monotone proxy loading sensitivity (e.g., $E_0 \approx 0.8755$ at `loading = -0.1` versus $E_0 \approx 0.9420$ at `loading = 0.1`).

### 3. Native Mode-Ladder Proof - REVISED AFTER AUDIT
**Status:** The old completion claim was replaced on 2026-04-02.
**Implementation:**
- The refreshed Phase H package now records representative spectra, parity/chiral-flip comparisons, and summary metadata for the actual proxy runtime.
- **Results:** The current package finds a sampled `n = 0` root on representative states, but not a robust solver-backed multi-level ladder derived from regenerated classical backgrounds. Strong native quantum-spectrum claims remain open.

---

## Phase I — First-Principles Derivation of Constants

### 1. Exhaustive Slice Protocol (Section 2) - COMPLETED AFTER AUDIT REFRESH
**Status:** Completed after audit refresh on 2026-04-02.
**Implementation:**
- Rebuilt the Phase I pullback package so it now executes the full combinatorial matrix:
    - **1D Slices:** Phi, Theta, and Rho sweeps across $[-2\pi, 2\pi]$.
    - **2D Slices:** Phi/Rho, Theta/Phi, and Theta/Rho pairings across $[-2\pi, 2\pi]^2$.
- **Results:** Confirmed that the pullback anisotropy is phi-controlled. Theta and rho are spectator coordinates unless phi changes.

### 2. Replacement of Exploratory `beta_a` Coefficients - REVISED AFTER AUDIT
**Status:** The old completion claim was replaced on 2026-04-02.
**Implementation:**
- The refreshed Phase I package derives and scans the pullback-metric eigenvalues and records exact sheet families.
- **Results:** Phase I identifies a native geometry-level anisotropy mechanism, but the active solver chain still has not replaced the exploratory `beta_a` coefficients with those pullback-derived stiffnesses.

### 3. Physical Observable Mapping - REVISED AFTER AUDIT
**Status:** Not completed as of 2026-04-02.
**Implementation:**
- The current notes record only heuristic candidate quantities such as the unit-scale and active-scale stiffness gaps.
- **Results:** No dynamically extracted fine-structure analog or mass gap has yet been produced. Goal 3 remains open.

---

## Phase J — Full 3D Dynamic Stability

### 1. Exhaustive Slice Protocol (Section 2) - COMPLETED AFTER AUDIT REFRESH
**Status:** Completed after audit refresh on 2026-04-02.
**Implementation:**
- Rebuilt the Phase J proxy package so it now executes the full combinatorial matrix:
    - **1D Slices:** Theta, Phi, and Rho sweeps across `[-2pi, 2pi]`.
    - **2D Slices:** Theta/Rho, Theta/Phi, and Phi/Rho pairings across `[-2pi, 2pi]^2`.
- **Results:** The refreshed package now satisfies the transition-plan sampling protocol and records full-domain retention / drift diagnostics.

### 2. Full 3D+1 Ordered-Manifold Time Evolution - REVISED AFTER AUDIT
**Status:** Partially met after audit refresh on 2026-04-02.
**Implementation:**
- The active Phase J solver now documents itself honestly as a 3D anchored Cartesian damped-wave proxy with a Gaussian restoring anchor and explicit time evolution on a `24^3` grid.
- **Results:** Phase J now moves beyond static radial ODE work in a real 3D+1 proxy sense, but it still does not implement the ordered-manifold PDE from `derivation_91` with target-metric, Christoffel, and potential-gradient terms.

### 3. Acceleration Tracking (Goal 3) - COMPLETED AS A PROXY RESULT
**Status:** Completed after audit refresh on 2026-04-02.
**Implementation:**
- Kept the moving-anchor diagnostic and refreshed the interpretation around peak tracking and motion lag.
- **Results:** The packet follows the moving anchor partway across the grid, ending at `core_x = 1.0643478260869563` for a target end position `1.18`, with final lag `0.11565217391304361`.

### 4. Strong Dynamic Objecthood / Discrete Identity - REVISED AFTER AUDIT
**Status:** Not completed as of 2026-04-02.
**Implementation:**
- The refreshed package records bulk boundedness, slice retention / drift, and transport lag, but it does not evolve a conserved invariant or a fully implemented ordered-manifold PDE.
- **Results:** The old "guaranteed resilience" and "true particle" wording was too strong. Phase J now closes on bounded 3D proxy behavior rather than proof of rigid discrete identity under violent dynamics.

---

## Phase K — Multi-Particle Interactions

### 1. Exhaustive Slice Protocol (Section 2) - COMPLETED AFTER AUDIT REFRESH
**Status:** Completed after audit refresh on 2026-04-02.
**Implementation:**
- Rebuilt the Phase K proxy package so it now executes the full combinatorial matrix:
    - **1D Slices:** Theta, Phi, and Rho sweeps across `[-2pi, 2pi]`.
    - **2D Slices:** Theta/Rho, Theta/Phi, and Phi/Rho pairings across `[-2pi, 2pi]^2`.
- **Results:** The refreshed package now satisfies the transition-plan sampling protocol for its interaction proxy outputs.

### 2. Spatial Interaction of Separated Folds - REVISED AFTER AUDIT
**Status:** Met in proxy form only after audit refresh on 2026-04-02.
**Implementation:**
- The active Phase K solver now documents itself honestly as a one-dimensional signed overlap proxy between separated exponential anchor envelopes.
- **Results:** The package does produce distance-dependent interaction masses and force gradients, but not from a full 3D two-fold field solve.

### 3. Effective Force-Law Extraction - REVISED AFTER AUDIT
**Status:** Partially met in proxy form after audit refresh on 2026-04-02.
**Implementation:**
- Added fit-quality diagnostics comparing the old power-law reading against an exponential fit.
- **Results:** The old inverse-square claim did not survive. The log-log slope is about `-2.9721`, but the power-fit linear-space `R^2` is strongly negative while the exponential fit is materially better.

### 4. Charge / Chirality Interaction Rule - REVISED AFTER AUDIT
**Status:** Not completed as of 2026-04-02.
**Implementation:**
- Added representative pair comparisons using the audited chirality operator `chi = cos(2phi)`.
- **Results:** The current proxy does not show "same charge repels, opposite charge attracts." The attractive `base_vs_sign_flipped` pair is same-chirality, while the opposite-chirality `base_vs_chiral_flip` pair remains repulsive.

---

## Phase L — Topological Shedding and Particle Emission

### 1. Exhaustive Slice Protocol (Section 6) - COMPLETED AFTER AUDIT REFRESH
**Status:** Completed after audit refresh on 2026-04-02.
**Implementation:**
- Rebuilt the Phase L package so it now executes the full combinatorial matrix:
    - **Bulk scan:** `8000` sampled states across `theta`, `phi`, and `rho`.
    - **1D Slices:** Theta, Phi, and Rho sweeps across `[-2pi, 2pi]`.
    - **2D Slices:** Theta/Phi, Theta/Rho, and Phi/Rho pairings across `[-2pi, 2pi]^2`.
- Added `bulk_emission_scan.csv` and `summary.json` so summary claims are backed by explicit regenerated outputs.
- **Results:** The refreshed package now satisfies the transition-plan sampling protocol for its active proxy runtime.

### 2. Dynamic Energy-Loss Modeling (Goal 1) - REVISED AFTER AUDIT
**Status:** Partially met in proxy form after audit refresh on 2026-04-02.
**Implementation:**
- The active Phase L solver now documents itself honestly as an algebraic emission proxy with emitted flux
  `0.5 * (theta^2 + rho^2) * (1 - 0.9 * |cos(2phi)|)`.
- **Results:** Phase L now maps a full-domain shedding landscape, but it still does not evolve time-dependent core depletion or a solved pinch instability.

### 3. Massless Packet Shedding (Goal 2) - REVISED AFTER AUDIT
**Status:** Partially met in proxy form after audit refresh on 2026-04-02.
**Implementation:**
- Added `omega_blindness_check.csv` and kept the packet-trajectory diagnostic in the refreshed package.
- **Results:** The current runtime is exactly `omega`-blind and produces a constant-speed packet trajectory, but both features are imposed by construction rather than derived from field equations.

### 4. Direct Mode-Ladder Step Mapping (Goal 3) - REVISED AFTER AUDIT
**Status:** Not completed as of 2026-04-02.
**Implementation:**
- The refreshed package now states this explicitly in `summary.json` with `discrete_step_mapping = not_implemented`.
- **Results:** No direct `E_n -> E_(n-1)` energy accounting tied to audited Phase H spectral data has yet been implemented.

---

## Phase M — Pair Creation and Annihilation

### 1. Exhaustive Slice Protocol (Section 7) - COMPLETED AFTER AUDIT REFRESH
**Status:** Completed after audit refresh on 2026-04-02.
**Implementation:**
- Rebuilt the Phase M package so it now executes the full combinatorial matrix:
    - **Bulk scan:** energy sweep over `50` sampled values.
    - **1D Slices:** annihilation scans over Theta, Phi, and Rho across `[-2pi, 2pi]`.
    - **2D Slices:** creation scans over Theta/Phi, Theta/Rho, and Phi/Rho across `[-2pi, 2pi]^2`.
- Added explicit annihilation and creation reference tables plus `summary.json`.
- **Results:** The refreshed package now satisfies the transition-plan sampling protocol for its active simplified runtime.

### 2. Mirror-Pair Annihilation (Goal 1) - REVISED AFTER AUDIT
**Status:** Partially met in simplified form after audit refresh on 2026-04-02.
**Implementation:**
- The active Phase M solver now documents itself honestly as a pair-lifecycle model using:
  - audited chirality `chi = cos(2phi)`,
  - an exact-partner annihilation score,
  - and angular alignment penalties.
- **Results:** The exact chiral-flip partner returns `Vacuum`, while parity and same-handed reference states do not. But the package still does not solve a collision in spacetime.

### 3. Pair Creation from Extreme Energy (Goal 2) - REVISED AFTER AUDIT
**Status:** Partially met in simplified form after audit refresh on 2026-04-02.
**Implementation:**
- Kept a fixed creation threshold gate and a singular-sheet susceptibility rule, then refreshed the outputs and interpretation around that scope.
- **Results:** The package records an imposed threshold `2.55`, with the first sampled created row at `2.5510204081632653`, and shows strong phi-localization near the singular sheets. It does not derive vacuum tearing from the equations of motion.

---

## General Project Gaps (Inherited from Audit)
...
### 1. Dynamical Response (Phase E, Goal 4)
**Missing:** A clean effective inertial-vs.-gravitational mass extraction.
**Implementation:** Replace the current simple background-gradient probe with a loading model that stays perturbative and admits a defensible equation-of-motion interpretation.

### 2. Internal Rigidity (Phase D, Goal 5)
**Missing:** Stress test of the energy-momentum "knot" under external pressure.
**Implementation:** Perturb the boundary conditions with an inward flux and measure the stability of the core $r_{half}$ and $M_{final}$.
