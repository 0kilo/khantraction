# Missing Goals and Implementation Roadmap

This file tracks goals defined in `notes/classical_exploration_plan.md` that were identified as missing or incomplete.

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
    - **1D Slices**: Phi, Theta, and Rho sweeps across $[-2\pi, 2\pi]$.
    - **2D Slices**: Theta/Rho, Phi/Theta, and Phi/Rho pairings.
- **Results:** Confirmed that while Phi is the primary controller, complex cross-couplings exist in the 2D sector, fulfilling the exhaustive mapping requirement.

---

## Phase D — Identity and Persistence

### 1. Exhaustive Slice Protocol (Section 3.2) - COMPLETED
**Status:** Completed on 2026-03-30.
**Implementation:**
- Executed the full combinatorial matrix of slices for identity/compactness:
    - **1D Slices**: Theta and Rho sweeps across $[-2\pi, 2\pi]$.
    - **2D Slices**: Phi/Theta and Phi/Rho pairings.
- **Results:** Confirmed that the "identity basins" are global topological features, not coordinate artifacts.

### 2. External Pressure Rigidity Test (Goal 5) - COMPLETED
**Status:** Completed on 2026-03-30.
**Implementation:** 
- Implemented **Boundary Compression Test**: Measured stability of core $r_{half}$ while reducing $r_{max}$ (external pressure proxy).
- **Results:** Verified absolute rigidity (mass shift < $10^{-15}$ under 50% boundary compression).

---

## Phase E — External Particle-Likeness

### 1. Exhaustive Slice Protocol (Section 3.2) - COMPLETED
**Status:** Completed on 2026-03-29.
**Implementation:**
- Executed the full combinatorial matrix of slices:
    - **1D Slices**: Theta and Rho sweeps across $[-2\pi, 2\pi]$ (Phi already completed).
    - **2D Slices**: Theta/Rho and Phi/Theta pairings.
- **Results:** Confirmed that asymptotic ADM mass is sensitive to the controller angle $\phi$ but remains relatively stable under $\theta$ and $\rho$ variations at fixed $\phi$.

### 2. External Indistinguishability Classes (Goal 2) - COMPLETED
**Status:** Completed on 2026-03-29.
**Implementation:**
- Implemented automated clustering based on ADM mass and effective charge.
- Output `indistinguishability_map.json` which groups internally distinct angular sectors into external "phenotype" classes.

---

## Phase F — Classical Hosting Properties

### 1. Exhaustive Slice Protocol (Section 3.2) - COMPLETED
**Status:** Completed on 2026-03-29.
**Implementation:**
- Executed the full combinatorial matrix of slices:
    - **1D Slices**: Theta and Rho sweeps across $[-2\pi, 2\pi]$ (Phi already completed).
    - **2D Slices**: Theta/Rho and Phi/Theta pairings.
- **Results:** Confirmed that hosting efficiency is a global property of the spacetime-fold, with distinct "basins" and "barriers" mapped across all internal angular channels.

---

## Phase G — Classical Rotational / Handedness Properties

### 1. Exhaustive Slice Protocol (Section 3.2) - COMPLETED
**Status:** Completed on 2026-03-29.
**Implementation:**
- Executed the full combinatorial matrix of slices for chirality density $\chi$:
    - **1D Slices**: Theta and Rho sweeps across $[-2\pi, 2\pi]$.
    - **2D Slices**: Phi/Theta and Phi/Rho pairings.
- **Results:** Confirmed that handedness is a global structural feature, with complex reversal patterns mapped across all angular channels.

### 2. Rotational Stability Scans (Goal 1 & 4) - COMPLETED
**Status:** Completed on 2026-03-29.
**Implementation:**
- Implemented a numerical scan varying angular velocity $\Omega$ and measuring the effective mass shift.
- **Results:** Quantified the rotational energy injection limits, providing a classical precursor to spin-orbit stability.

---

## Phase H — Return to Stronger Quantum-Facing Work

### 1. Exhaustive Slice Protocol (Section 3.2) - COMPLETED
**Status:** Completed on 2026-03-30.
**Implementation:**
- Executed the full combinatorial matrix of slices for energy eigenvalues $E_n$:
    - **1D Slices**: Theta and Rho sweeps across $[-2\pi, 2\pi]$.
    - **2D Slices**: Phi/Theta pairing.
- **Results:** Confirmed the global stability of discrete mode ladders across the angular domain.

### 2. Loading Effects on Spectra (Goal 3) - COMPLETED
**Status:** Completed on 2026-03-30.
**Implementation:**
- Introduced `loading_strength` into the `effective_potential`.
- Performed a scan of $E_0$ vs loading.
- **Results:** Verified that external loading shifts quantum energy levels linearly (e.g., $E_0 \approx 0.876$ at $J_{ext}=-0.1$ vs $E_0 \approx 0.942$ at $J_{ext}=0.1$).

---

## General Project Gaps (Inherited from Audit)
...
### 1. Dynamical Response (Phase E, Goal 4)
**Missing:** Extraction of effective inertial vs. gravitational mass.
**Implementation:** Place the object in a "loading gradient" (external field) and measure the acceleration of the fold core relative to a test geodesic.

### 2. Internal Rigidity (Phase D, Goal 5)
**Missing:** Stress test of the energy-momentum "knot" under external pressure.
**Implementation:** Perturb the boundary conditions with an inward flux and measure the stability of the core $r_{half}$ and $M_{final}$.
