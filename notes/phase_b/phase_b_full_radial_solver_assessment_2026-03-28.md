# Phase B Assessment — Full Radial Solver Implementation

**Date:** 2026-03-28  
**Phase:** B — Structured-object picture  
**Status:** Real runtime implemented; closure remains provisional

## Purpose

This note records the first honest fresh-tree implementation of a **full Phase B radial solver/runtime** for the four-component norm-based Khantraction system.

The goal was not to fake a uniquely settled physical solver.
It was to push the reconstruction as far as the active project materials actually support, implement a real runtime around that reconstruction, and make every remaining model-dependent choice explicit.

---

## 1. What was reconstructed

### 1.1 Matter-side radial equations

Using `derivations/derivation_73_full_four_component_radial_system_fresh_start.md`, the runtime implements the component-symmetric matter system
\[
q_A''+\left(\frac{2}{r}+\Phi'-\Lambda'\right)q_A' + e^{2\Lambda}\Big(m_{\mathrm{glue}}^2+\lambda_q|q|^2-2\xi R\Big)q_A=0,
\]
for \(q_A \in \{a,b,c,d\}\) and \(|q|^2=a^2+b^2+c^2+d^2\).

### 1.2 Ordered-state seeding layer

Using `derivations/derivation_71_exponential_quaternion_parameter_mapping_clean.md`, the runtime maps ordered-state seeds from
\[
Q(\omega,\theta,\phi,\rho)=e^{\omega}e^{\theta i}e^{\phi j}e^{\rho k}
\]
into component directions.

The active convention is preserved explicitly:
- \(\omega > 0\)
- \(\theta,\phi,\rho \in [-2\pi, 2\pi]\)
- no redundancy quotienting

### 1.3 Einstein-sector reconstruction used by the runtime

The fresh tree still does **not** uniquely derive the full Einstein equations for the nonminimal coupling term \(\xi R |q|^2\).
So the runtime uses an explicit provisional closure mode:

- a standard static scalar-multiplet stress model for \(\rho\), \(p_r\), and \(p_t\)
- Misner–Sharp closure
  \[
  m' = 4\pi r^2 \rho
  \]
- metric-potential closure
  \[
  \Phi' = \frac{m + 4\pi r^3 p_r}{r(r-2m)}
  \]
- Ricci estimate from the Einstein trace
  \[
  R = -\kappa T,
  \qquad
  T = -\rho + p_r + 2 p_t
  \]
  with \(\kappa = 8\pi\)

This is a **reconstructed closure choice**, not a uniquely justified fresh-tree derivation of the full nonminimal-coupling Einstein sector.
That limitation is recorded in machine-readable form in:
- `solutions/phase_b/phase_b_full_radial_solver/assumptions_and_closure.json`

### 1.4 Regular-origin and continuation setup

Because the paper and active notes do not yet supply a full asymptotically matched BVP prescription, the implemented runtime uses a regular-origin IVP/continuation strategy:

- \(q_A'(r_0)=0\) at small \(r_0\)
- \(m(r_0)\) initialized from the local energy density
- \(\Phi(r_0)=0\) as a gauge choice
- ordered-state seeds mapped into small central component amplitudes via
  \[
  q_A(r_0) = A_0 e^{\omega} \hat q_A(\theta,\phi,\rho)
  \]
  with `central_amplitude_base = 0.02` and `\hat q_A` the normalized ordered-state direction

This amplitude scaling was chosen because the earlier reduced successful profile quoted in `khantraction_paper.md` used a small regular-origin amplitude of order `0.02`.
So the runtime uses the ordered map for **directional component structure** while anchoring the overall center amplitude to the only explicit successful small-amplitude seed scale currently documented in the active materials.

That is a defensible reconstruction, but still a reconstruction.

---

## 2. What was implemented

New active files:
- `analysis/phase_b/phase_b_full_radial_solver.py`
- `scripts/run_phase_b_full_radial_solver.sh`
- `solutions/phase_b/phase_b_full_radial_solver/`
- `notes/phase_b/phase_b_full_radial_solver_assessment_2026-03-28.md`

Generated outputs include:
- `solutions/phase_b/phase_b_full_radial_solver/run_results.csv`
- `solutions/phase_b/phase_b_full_radial_solver/run_summary.json`
- `solutions/phase_b/phase_b_full_radial_solver/assumptions_and_closure.json`
- `solutions/phase_b/phase_b_full_radial_solver/summary.md`
- `solutions/phase_b/phase_b_full_radial_solver/profiles/*.csv`

The runtime includes:
- RK4 integration for the coupled four-component matter + metric IVP
- continuation seeds from scalar-like to rich ordered sectors
- neighborhood probes around the locked rich sector
- coarse active-box scans
- explicit diagnostics for:
  - horizon / metric breakdown
  - field or mass blowup
  - asymptotic residuals
  - regularity checks
- observable extraction for:
  - final mass
  - integrated \(|R|\)
  - mass half-radius and 90% radius
  - Ricci half-radius and 90% radius
  - settling radius
  - core radius
  - soft-region width
  - peak imaginary-to-real ratio

---

## 3. What actually ran successfully

From `solutions/phase_b/phase_b_full_radial_solver/run_summary.json`:

- seeds run: **117**
- successful integrations: **117**
- regularity-ok integrations: **117**
- horizon hits: **0**
- boundary decay passes: **117**

Reported ranges in this closure mode:
- final mass range: **0.048671600859654246 to 0.17822380681078998**
- integrated \(|R|\) range: **0.003527253379195638 to 0.012931544814019142**
- peak imaginary/real ratio range: **0.0 to 32974425414.002563**

That last extreme ratio is not a claim of a physically validated gigantic richness scale by itself.
It occurs when the real component passes very near zero, so the ratio can spike dramatically even when the total profile remains small and regular.
So any interpretation of that ratio must be tied to the full profile, not just the quotient.

The continuation track from scalar-like to the rich ordered anchor ran without horizon formation in this provisional closure, with final mass increasing monotonically along the sampled path.
That is a real runtime result.

---

## 4. What remains provisional or blocked

### 4.1 Exact Einstein-sector closure is still not settled

The largest remaining gap is still the same one identified in the reconstruction note:

> the fresh tree does not yet contain a uniquely justified full Einstein-sector derivation for the nonminimal \(\xi R|q|^2\) model.

So the current solver is **real** but **closure-provisional**.

### 4.2 Boundary-value status remains weaker than a full soliton proof

The current runtime is an IVP/continuation solver with boundary residual diagnostics.
It is not yet a full matched shooting/BVP solver that proves a unique asymptotically selected family.

What the current finite-radius residual checks do show is:
- the sampled runs stayed regular,
- no horizons formed in the recorded sweep,
- the fields remained small by the outer boundary,
- the runtime can now distinguish clean completion from actual breakdown.

What they do **not** yet prove is:
- uniqueness of the asymptotic branch,
- true asymptotic decay to the exact desired physical vacuum,
- or closure-independent structured-object observables.

### 4.3 Observable formulas are still closure-dependent

The runtime now computes objecthood observables, but their physical interpretation is still tied to the provisional closure mode because:
- energy density depends on the chosen stress reconstruction,
- Ricci depends on the chosen trace closure,
- concentration radii therefore remain closure-sensitive.

So these observables should presently be read as **runtime diagnostics and comparison hooks**, not as fully closure-independent physical facts.

---

## 5. Current best interpretation

The fresh tree has now advanced beyond “the full solver is missing.”

The defensible new statement is:

> Phase B now has a real four-component radial runtime with ordered-state seeding, continuation support, metric integration, regularity diagnostics, horizon checks, and observable extraction. It runs successfully across a broad seeded set in the active domain. But the Einstein-sector closure used by that runtime is still a transparent provisional reconstruction rather than a uniquely derived consequence of the active-tree nonminimal-coupling model.

That is a meaningful implementation milestone.
It is also the correct level of restraint.

---

## 6. Immediate next derivation burden

The most important next step is now very specific:

1. derive the full Einstein equations for the \(\xi R |q|^2\) system in the same fresh-tree notation
2. decide whether the current provisional closure survives that derivation or needs correction
3. then upgrade the solver from IVP-continuation diagnostics to a stronger asymptotic matching / continuation solver if justified

---

## 7. Bottom line

**Bottom line:** a real Phase B full radial solver/runtime now exists in the fresh tree and produces reproducible runs plus structured diagnostics across ordered-state scans. The matter-side four-component system is implemented, continuation hooks work, and seeded runs complete cleanly in the current provisional closure. But the Einstein-sector closure for the nonminimal \(\xi R|q|^2\) model remains incompletely derived in the active materials, so all current physical branch and observable claims should still be treated as provisional to that closure choice.
