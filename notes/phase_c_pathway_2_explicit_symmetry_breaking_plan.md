# Phase C Exploration Plan — Pathway 2: Explicit Symmetry Breaking via Maurer-Cartan

**Date:** 2026-03-29
**Phase:** C — Distinct angular traits
**Status:** Active Pathway Selected

## Purpose
This note establishes the theoretical mandate and implementation roadmap for Phase C. Following the "Symmetry Bombshell" discovered in Phase B, we must explicitly break the native \(O(4)\) degeneracy of the Khantraction Lagrangian to determine if the internal angular variables (\(\theta, \phi, \rho\)) encode genuinely different macroscopic traits. 

We have rejected the Non-Linear Sigma Model (Pathway 1) as a mere coordinate transformation that cannot change macroscopic observables. Instead, we select **Pathway 2**: adding new quaternionic physics to the base Lagrangian.

---

## 1. The "Why": The Failure of the \(O(4)\) Norm
Phase B proved mathematically that the exact Einstein trace for the nonminimal coupling (\(\xi R|q|^2\)) algebraically decouples and interacts exclusively with the invariant \(O(4)\) norm (\(|q|^2 = a^2+b^2+c^2+d^2\)) and the flat kinetic sum. 

In the current formulation, the quaternion variables are just decorative parametrizations of a flat Euclidean sphere. Because the theory does not possess any non-commutative operations in its Lagrangian, it is mathematically blind to the difference between the scalar anchor (\(\theta=0, \phi=0, \rho=0\)) and the rich quaternion anchor (\(\theta=\pi, \phi=-\pi/2, \rho=\pi/2\)). They produce identical masses and core radii.

To answer the Phase C mandate—"Do the angular variables encode genuinely different object traits?"—the theory itself must be forced to "feel" the internal \(\mathfrak{su}(2)\)-like geometry isolated in Phase A.

---

## 2. The "What": The Maurer-Cartan Interaction
To explicitly break the \(O(4)\) symmetry down to a true quaternionic identity, we will introduce a purely quaternionic interaction term to the action. 

The most natural, geometrically rigorous candidate is an interaction built from the **Maurer-Cartan 1-form**:
\[ \omega_\mu = q^{-1} \partial_\mu q \]

Unlike the standard kinetic term (\(\partial_\mu \bar{q} \partial^\mu q\)), which yields the flat \(O(4)\) sum, the Maurer-Cartan form explicitly relies on quaternion multiplication (which is non-commutative). 

We will upgrade the Khantraction Lagrangian by adding a directional or topological coupling term. A strong candidate is a Skyrme-like commutator interaction:
\[ \mathcal{L}_{\text{MC}} = \lambda_{\text{MC}} \text{Tr}([ \omega_\mu, \omega_\nu ][ \omega^\mu, \omega^\nu ]) \]
*(Alternatively, a simpler directional coupling vector based on the imaginary components of \(\omega_\mu\) may be explored).*

Because quaternion multiplication rules (\(ij=k\), etc.) dictate the evaluation of \(\omega_\mu\), this new term will natively embed the singular chart architecture (\(\det J \propto \cos(2\phi)\)) directly into the system's energy profile. 

---

## 3. The "How": Implementation Roadmap
This pathway requires careful reconstruction to ensure we do not break the stable, horizon-free objecthood achieved in Phase B. 

### Step 1: Analytical Derivation (`derivations/derivation_78_maurer_cartan_tensor.md`)
- Evaluate the exact Maurer-Cartan 1-form \(\omega_\mu = q^{-1} \partial_\mu q\) using the ordered state map \(Q(\omega, \theta, \phi, \rho)\).
- Formulate the new Lagrangian term \(\mathcal{L}_{\text{MC}}\).
- Derive its exact contribution to the stress-energy tensor: \(\delta T_{\mu\nu}^{\text{MC}}\).

### Step 2: Einstein Trace Update (`derivations/derivation_79_einstein_trace_with_mc_breaking.md`)
- The inclusion of \(\delta T_{\mu\nu}^{\text{MC}}\) changes the canonical trace \(T^{(q)}\).
- Re-evaluate the exact Ricci scalar \(R\) by decoupling the nonminimal kinetic term (\(6\kappa\xi \square |q|^2\)) against the newly updated trace.

### Step 3: Solver Implementation (`analysis/phase_c_mc_radial_solver.py`)
- Write a new radial solver that incorporates the Maurer-Cartan potential gradients into the matter equations.
- Unlike Phase B, this solver cannot use the flat \((a,b,c,d)\) basis without resolving the non-commutative cross-terms. We will integrate the system directly using the angular parameters to cleanly track the symmetry breaking.

### Step 4: Trait Differentiation Scans (`solutions/phase_c_angular_traits/`)
- Run the 39 Phase B continuation seeds through the new MC-aware solver.
- **The Critical Test:** Observe if the final mass, integrated curvature, mass half-radius, and core radius finally *split*. If a scalar anchor yields a different mass and compactness than a rich-quaternion anchor seeded at the exact same scale (\(\omega\)), Phase C has succeeded.