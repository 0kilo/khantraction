# Direct-Data Closure Plan - 2026-04-02

## Purpose

This document answers the project-level question that remains after the Phase A-M audit refresh:

> What would it take, using original and direct data rather than proxy evidence, to determine whether Khantraction can serve as a classical particle-level model?

The answer below is based on the refreshed closure summaries in `summary/`, the audit trackers in `notes/missing_items.md` and `notes/missing_goals.md`, and the paper framing in `khantraction_paper.md`.

## Implementation outcome (2026-04-02 direct runtime pass)

The critical path was not left hypothetical. A direct implementation pass has now been executed for the classical-core phases:

- **Phase I:** exact pullback coefficients are now implemented in `analysis/direct_ordered_manifold.py` and used downstream by Phases J, E, and K.
- **Phase J:** the old anchored proxy has been replaced by a direct weak-gravity ordered-manifold 3D solver.
- **Phase E:** the old beta-driven gradient probe has been replaced by direct pullback profiles plus a direct 3D impulse-response ladder.
- **Phase K:** the old one-dimensional overlap proxy has been replaced, for the directly defined same-background case, by a real 3D interaction-energy density computation on a shared grid.

The resulting gate outcomes are:

- **Gate A - Coefficient realism:** passed at the implementation level.
- **Gate B - 3D identity survival:** localized objecthood survives on the audited window, but discrete species identity does not.
- **Gate C - Interaction realism:** same-background direct interaction exists, but species-specific interaction structure does not.
- **Gate D - Motion response:** a clean family-level response law exists, but it is species-blind.

So the direct-data pass changes the final decision materially: the model no longer fails because the critical path was unimplemented. It fails because the rebuilt direct chain universalizes the audited seed family instead of producing particle-level species structure.

The remaining sections below preserve the original closure logic and the rationale for that implementation program. Where the historical plan wording and the direct implementation outcome differ, this implementation-outcome section takes precedence.

## 1. Decision standard

For the remainder of this program, a claim only counts toward the particle-level verdict if it is supported by:

1. a derivation that actually reaches solver-ready equations,
2. an implementation that directly evolves or solves those equations,
3. outputs regenerated from that implementation,
4. and an interpretation that does not rely on hand-built gates, hand-built resonators, or algebraic stand-ins for the target dynamics.

That means:

- direct solver-backed data counts,
- exploratory geometry scans count only as precursor evidence,
- proxy-only phases do not close particle-level claims,
- and later quantum-style phases do not rescue unresolved classical-core gaps.

## 2. Per-phase gap classification

### Phase A

- **Surviving result:** ordered-map foundation is solid.
- **Gap type:** none that block the classical verdict.
- **Decision:** keep as closed.
- **Role in final verdict:** foundational but not blocking.

### Phase B

- **Surviving result:** static structured objecthood exists; continuous scalar-to-rich family exists.
- **Gap:** raw size observables are setup-dependent; exact linear-basis dynamics are angularly blind.
- **Needed to close:** different observable strategy, not the old raw-radius claim.
- **Decision:** retire the old absolute-size-invariance claim. If needed, replace it with scale-free or asymptotic observables only.
- **Role in final verdict:** important precursor, but not the main blocker.

### Phase C

- **Surviving result:** exploratory Maurer-Cartan symmetry breaking can make angular traits visible.
- **Gap:** strongest trait splitting lives in a runtime that still depends on exploratory coefficients and includes near-horizon terminations.
- **Needed to close:** re-run the angular-trait program only after Phase I replaces the exploratory coefficients in the active solver chain.
- **Decision:** keep as exploratory evidence only; do not treat as direct proof of stable classical species.
- **Role in final verdict:** subordinate to Phase I.

### Phase D

- **Surviving result:** local family persistence and phi-organized identity structure.
- **Gap:** no discrete rigid species, no scale-invariant fingerprint, no universal rigidity.
- **Needed to close:** either derive a new conserved topological invariant that truly partitions species, or abandon the discrete-species claim.
- **Decision:** retire the old discrete rigid-species claim from the model’s core promise unless a new invariant is derived. Keep only the local-family result.
- **Role in final verdict:** secondary. J will matter more than D for true particle-level objecthood.

### Phase E

- **Surviving result:** partial external particle-likeness; some survivor sectors have smooth outer tails and external indistinguishability classes.
- **Gap:** no clean effective equation of motion, no direct inertial-mass law, incomplete interaction-law extraction.
- **Needed to close:** derive and implement a direct perturbation-response program on solved backgrounds, then extract collective motion and asymptotic charges without relying on tiny imposed gradients.
- **Decision:** pursue. This is a direct blocker for any classical particle-level claim.
- **Role in final verdict:** core blocker.

### Phase F

- **Surviving result:** signed probe-response asymmetry exists.
- **Gap:** no strong trapping or hosting in a classical bound-state sense.
- **Needed to close:** only worth pursuing if hosted external content is still part of the particle-level target after E/J/K are solved.
- **Decision:** defer. Do not use Phase F as a viability blocker for the classical particle verdict.
- **Role in final verdict:** secondary / optional.

### Phase G

- **Surviving result:** classical handedness architecture is real and solver-backed at the static level.
- **Gap:** no solver-backed rotational dynamics or hosted angular-momentum stability.
- **Needed to close:** derive the relevant rotational current / Noether structure and solve real rotational perturbations.
- **Decision:** defer as a secondary enrichment. Keep the chirality architecture; do not block the classical particle verdict on spin-like extensions.
- **Role in final verdict:** supportive, not blocking.

### Phase H

- **Surviving result:** only a corrected semiclassical proxy.
- **Gap:** no native solver-backed quantum operator or ladder.
- **Needed to close:** stronger operator on regenerated classical backgrounds.
- **Decision:** defer entirely. This is not part of the minimal classical particle-level verdict.
- **Role in final verdict:** out of scope for the current decision.

### Phase I

- **Surviving result:** ordered-map pullback metric carries a real anisotropy mechanism.
- **Gap:** solver still uses exploratory `beta_a`; no mapping to physical observables.
- **Needed to close:** derive a solver-ready stiffness tensor / coefficient map from the pullback metric, wire it into the active dynamics, then regenerate downstream phases from that non-exploratory basis.
- **Decision:** pursue immediately. This is a foundational blocker.
- **Role in final verdict:** core blocker.

### Phase J

- **Surviving result:** bounded 3D anchored-wave behavior exists in a proxy sense.
- **Gap:** no full ordered-manifold PDE, no invariant tracking, no proof of identity preservation under violent dynamics.
- **Needed to close:** derive and implement the full ordered-manifold 3D+1 system, then define and track a conserved or quasi-conserved objecthood invariant.
- **Decision:** pursue immediately. This is a foundational blocker.
- **Role in final verdict:** core blocker.

### Phase K

- **Surviving result:** signed overlap trends exist in a one-dimensional reduced model.
- **Gap:** no real 3D interaction law, no defensible charge/chirality rule, no direct scattering foundation.
- **Needed to close:** direct two-fold field evolution on solved backgrounds from the real J runtime, followed by force extraction from actual trajectories or momentum exchange.
- **Decision:** pursue immediately after I and J. This is a foundational blocker.
- **Role in final verdict:** core blocker.

### Phase L

- **Surviving result:** only an emission proxy.
- **Gap:** no dynamical shedding, no emergent massless packet, no direct ladder mapping.
- **Needed to close:** a full dynamic shedding solve on stronger backgrounds.
- **Decision:** defer. Not required for the classical particle-level verdict.
- **Role in final verdict:** out of scope for the current decision.

### Phase M

- **Surviving result:** only a simplified pair-lifecycle model.
- **Gap:** no real collision solve, no vacuum tearing, imposed creation threshold.
- **Needed to close:** a full dynamic creation-annihilation program on solved backgrounds.
- **Decision:** defer. Not required for the classical particle-level verdict.
- **Role in final verdict:** out of scope for the current decision.

## 3. Claims to retire now

These claims should be removed from the project’s active promise set unless new direct evidence appears:

1. **Phase B:** raw closure-independent size invariance from the current finite-box observables.
2. **Phase D:** discrete rigid classical species from the current continuous-family architecture.
3. **Phase K:** attraction / repulsion governed by chirality or topological charge in the current reduced model.
4. **Phase H:** native quantum ladder from the current resonator construction.
5. **Phase L:** direct radiative shedding from the current algebraic model.
6. **Phase M:** dynamic pair creation / annihilation from the current simplified model.

These are not proven impossible in principle. They are retired because the current architecture and data do not justify using them as active conclusions.

## 4. Critical path for a direct-data verdict

The shortest honest path to a classical particle-level verdict is:

### Stage 1 - Replace exploratory dynamics

1. **Complete Phase I in solver form**
   - derive the pullback-driven stiffness / anisotropy coefficients in a solver-ready form,
   - implement them in the active radial and 3D runtimes,
   - re-run the angular trait phases on that non-exploratory basis.

2. **Lock the observable language**
   - replace setup-dependent raw size claims with scale-free or asymptotic observables,
   - define the actual quantities that will count as particle-level signatures.

### Stage 2 - Build real direct dynamics

3. **Complete Phase J in full ordered-manifold form**
   - implement the target-metric, Christoffel, and potential-gradient structure,
   - build invariant tracking,
   - test whether localized objects preserve identity under violent 3D evolution.

If Stage 2 fails, the classical particle-level claim should be abandoned.

### Stage 3 - Build real motion and interaction data

4. **Rebuild Phase E without proxy forcing**
   - perturb solved objects directly,
   - extract equation-of-motion-like response from actual evolved fields,
   - determine whether an inertial / effective mass concept survives.

5. **Rebuild Phase K without reduced overlap models**
   - initialize two solved objects on a shared 3D domain,
   - evolve them directly,
   - measure scattering, deflection, momentum exchange, and force law from the evolution.

If Stage 3 fails, the classical particle-level claim should be abandoned.

### Stage 4 - Only after the classical core passes

6. **Revisit secondary classical enrichments**
   - Phase F trapping / hosting if still needed,
   - Phase G rotational dynamics if spin-like classical structure is still desired.

7. **Only then revisit the quantum-facing phases**
   - H, L, M should restart only after the classical core is genuinely direct-data complete.

## 5. Required new mathematical machinery

The project does need more mathematics, but not in every direction at once.

The minimum new machinery required is:

1. **Solver-ready pullback anisotropy map**
   - a direct bridge from Phase I geometry to the active equations of motion.

2. **Ordered-manifold 3D+1 evolution equations with conserved diagnostics**
   - enough structure to test whether objects persist as objects.

3. **Observable extraction framework**
   - asymptotic charges,
   - scale-free compactness measures,
   - motion-response observables,
   - interaction observables.

4. **Direct two-body initial-data construction**
   - not a proxy overlap, but actual multi-object initial data consistent with the field equations.

The project does **not** need more proxy-style spectral or lifecycle elaborations before those classical-core pieces exist.

## 6. Different approach where needed

Several gaps should be closed by changing the approach, not by polishing the current reduced models:

1. **Stop using later quantum-style phases to justify the classical model.**
   - H, L, and M are downstream and currently proxy-heavy.

2. **Stop treating finite-box raw radii as physical constants.**
   - use asymptotic or scale-free observables instead.

3. **Stop treating current reduced interaction, emission, and creation rules as if they were partial solutions of the target PDEs.**
   - they are diagnostic toys, not closure evidence.

## 7. Direct-data decision gates

The final particle-level verdict should be made at these gates:

### Gate A - Coefficient realism
If Phase I cannot replace the exploratory coefficients with solver-level direct data, the model should not be claimed as a particle-level classical theory.

### Gate B - 3D identity survival
If the full J runtime cannot preserve localized identity under strong evolution with an invariant-tracking diagnostic, the model should not be claimed as a particle-level classical theory.

### Gate C - Interaction realism
If direct two-body evolution cannot produce a coherent force / scattering law in K, the model should not be claimed as a particle-level classical theory.

### Gate D - Motion response
If E cannot yield a clean direct-data motion-response picture, the model should not be claimed as a classical particle model.

## 8. Project-level recommendation

For the purpose of deciding whether Khantraction can model classical particle physics:

- **Pursue directly:** I, J, E, K
- **Keep as supporting structure:** A, B, G
- **Treat as exploratory and re-run later:** C, D
- **Defer as secondary:** F
- **Defer out of current scope:** H, L, M

That is the most disciplined path to a final answer without proxy inflation.
