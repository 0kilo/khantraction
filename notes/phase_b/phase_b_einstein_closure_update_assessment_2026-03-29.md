# Phase B Assessment — Einstein Closure Update

**Date:** 2026-03-29
**Phase:** B — Structured-object picture
**Status:** Derivation complete; solver update required

## Purpose
This note interprets the newly completed exact derivation of the Einstein-sector equations for the nonminimal \(\xi R|q|^2\) coupling model (`derivations/derivation_76_full_einstein_equations_nonminimal_coupling.md`) and establishes the mandate for the next solver iteration.

## 1. Status of the Provisional Closure
The exact derivation answers the explicit next-step mandate of Phase B. 
The provisional trace closure (\(R = -\kappa T\)) used in the first full radial solver (`analysis/phase_b/phase_b_full_radial_solver.py`) is technically incomplete. While it was a stable numerical proxy, it omits the kinetic trace correction \(6\kappa\xi \square |q|^2\). Because this correction relies on the second derivatives of the local profile norm, it is structurally significant exactly where the object folds into a compact core. 

## 2. Impact on Objecthood Claims
The earlier closure stress test showed that compactness observables (mass half-radius, core size) were highly sensitive to setup parameters. Now that we know the Ricci feedback was omitting the true geometric trace response of the field's variation, those compactness profiles must be re-evaluated. The "structured object" claims remain plausible, but their specific geometric dimensions are strictly tied to a mathematically inexact boundary.

## 3. Next Implementation Mandate
The immediate next steps to close the implementation gap:
1. **Create `analysis/phase_b/phase_b_exact_radial_solver.py`**: Upgrade the matter-side equations to ingest the dynamically evaluated \(R = \frac{-\kappa T + 6\kappa\xi \square |q|^2}{1 + 2\kappa\xi |q|^2}\). This will require substituting \(\square |q|^2\) in static spherically symmetric coordinates.
2. **Re-run the Neighborhood Stress Test**: Execute the new exact solver over the same 39 scalar-to-rich continuation seeds to observe if the objecthood compactness shifts, and if the near-degenerate angular sectors finally break symmetry dynamically.
3. **Write `solutions/phase_b/phase_b_exact_radial_solver/` outputs.**