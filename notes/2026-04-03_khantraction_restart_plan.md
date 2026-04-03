# Khantraction Restart Plan

## Objective
Test from scratch whether Khantraction can be a viable classical particle-level model when the state variable is taken to be

```text
q(omega, theta, phi, rho) = exp(a(omega) + b(theta) i + c(phi) j + d(rho) k)
```

The task is not to preserve earlier claims. The task is to decide, using direct mathematics and direct numerical data, whether this ansatz can support:
- finite-energy localized states,
- stable transportable objecthood,
- nontrivial invariant structure,
- non-universal interaction behavior,
- and, if possible, true particle-like species.

If it cannot, the program must say so clearly and retire the unsupported claim.

## Starting Formulation

In this restart program:
- `omega, theta, phi, rho` are angular variables.
- `a, b, c, d` are scalar functions acting on those angular variables.
- The starting ansatz is a map on angle space.
- A later spacetime interpretation, if one exists, must be built explicitly from this angle-space object rather than silently assumed.

Define

```text
alpha = a(omega)
beta  = b(theta)
gamma = c(phi)
delta = d(rho)
V = beta i + gamma j + delta k
R = sqrt(beta^2 + gamma^2 + delta^2)
```

Then

```text
q = e^alpha [cos(R) + (V/R) sin(R)]
```

for `R != 0`, and `q = e^alpha` when `R = 0`.

This already exposes a central risk: the four input channels may reduce to one scale, one magnitude, and one unit direction. If that happens dynamically, then raw angle labels will not define particle species.

## Non-Negotiable Rules

1. Use direct equations and direct numerical solves only.
2. Do not use proxy, surrogate, or hand-built replacement dynamics.
3. Every claim must have:
   - a derivation,
   - executable analysis code,
   - saved raw outputs,
   - and a `summary.md` interpreting the outputs.
4. The default direct exploration domain is `omega, theta, phi, rho in [-2pi, 2pi]`.
5. Any reduced domain, identified periodicity, or symmetry quotient must be proved and documented before it is used to shrink the scans.
6. Any claim that fails derivationally or numerically is retired immediately rather than softened by rhetoric.

## Viability Criteria

Khantraction is only viable as a classical particle-level model if the direct program establishes all of the following:

1. **Well-posed field equations**
   - The governing equations come from an explicit action or equally explicit geometric law built from the angle-space ansatz and its derived spacetime interpretation.
   - The evolution problem is mathematically well-posed in the relevant regimes.

2. **Finite-energy localized states**
   - There exist regular direct solutions with finite energy or finite physically relevant mass functional.

3. **Invariant identity structure**
   - Distinct object classes are separated by real invariants, not by arbitrary seed labels or coordinate choices.

4. **Direct stability**
   - The candidate states survive direct perturbation and direct time evolution.

5. **Transportability**
   - Localized states can move without dissolving into a universal lump or pure radiation.

6. **Nontrivial direct interaction**
   - Two-body or many-body dynamics are not just universal overlap effects.
   - If multiple species are claimed, interaction differences must track the actual invariant structure.

7. **Clear falsifiability**
   - The program must define explicit failure conditions and use them.

If any of items 2 through 6 fails decisively, the particle-level claim fails even if the geometry remains interesting.

## Fresh Workflow

## Repository Layout
The restart program uses a clean structure:

```text
analysis/
derivations/
notes/
scripts/
solutions/
summary/
```

Each phase must create a complete packet:

1. `derivations/phase_xx_*.md`
2. `analysis/phase_xx/*.py`
3. `scripts/run_phase_xx_*.sh` if orchestration is needed
4. `solutions/phase_xx/...` raw outputs
5. `solutions/phase_xx/.../summary.md`
6. `notes/phase_xx/*.md`
7. `summary/YYYY-MM-DD_phase_xx_closure_summary.md`

## Standard Phase Workflow

For every phase:

1. Write the derivation first.
2. Review the derivation for hidden assumptions.
3. Implement the direct equations only.
4. Validate the code numerically on trivial or symmetry-check cases.
5. Run the full scan protocol.
6. Save raw outputs and an interpretive `summary.md`.
7. Write a phase assessment note.
8. Write a closure summary with explicit claim status:
   - met,
   - partially met,
   - not met,
   - or retired.
9. Run a contradiction pass:
   - check whether the result can be explained by symmetry collapse, coordinate redundancy, discretization artifacts, or boundary-condition tuning.
10. Decide whether the claim advances, gets revised, or is retired.

## Review Discipline

No phase is considered closed unless it includes:
- the mathematical claim,
- why the chosen method is the right test,
- what the raw result was,
- why that result does or does not support the claim,
- and exact references to supporting files.

## Global Scan Protocol

## Variable Domains

### Angular variables
- `omega, theta, phi, rho in [-2pi, 2pi]`
- No reduced `[-pi, pi]` shortcut is allowed unless a symmetry is first proved and explicitly documented.
- If later derivations show that one or more of `a, b, c, d` are non-periodic or deliberately break the naive angular periodicity, that extended structure must be stated explicitly and re-tested.

## Mandatory Scan Families

All phases that probe dependence on `(omega, theta, phi, rho)` must include every free-variable subset:

### 4-variable family
- Vary all four:
  - `(omega, theta, phi, rho)`

### 3-variable families
- Hold `omega`, vary `(theta, phi, rho)`
- Hold `theta`, vary `(omega, phi, rho)`
- Hold `phi`, vary `(omega, theta, rho)`
- Hold `rho`, vary `(omega, theta, phi)`

### 2-variable families
- Hold `(phi, rho)`, vary `(omega, theta)`
- Hold `(theta, rho)`, vary `(omega, phi)`
- Hold `(theta, phi)`, vary `(omega, rho)`
- Hold `(omega, rho)`, vary `(theta, phi)`
- Hold `(omega, phi)`, vary `(theta, rho)`
- Hold `(omega, theta)`, vary `(phi, rho)`

### 1-variable families
- Hold `(theta, phi, rho)`, vary `omega`
- Hold `(omega, phi, rho)`, vary `theta`
- Hold `(omega, theta, rho)`, vary `phi`
- Hold `(omega, theta, phi)`, vary `rho`

### 0-variable anchors
- Evaluate named anchor states used for cross-phase reference and regression testing.

## Fixed-Value Anchor Sets

### Angular anchors
Use at minimum:

```text
{-2pi, -3pi/2, -pi, -pi/2, -pi/4, 0, pi/4, pi/2, pi, 3pi/2, 2pi}
```

If a feature appears between anchor points, refine locally until the feature location is stable to the declared tolerance.

### Omega anchors
Use a direct angular anchor set at minimum:

```text
{-2pi, -3pi/2, -pi, -pi/2, -pi/4, 0, pi/4, pi/2, pi, 3pi/2, 2pi}
```

If a later phase identifies special features in `omega` between these points, refine locally until the feature location is stable to the declared tolerance.

## Resolution Policy

Each phase uses three passes:

1. **Coarse discovery pass**
   - Detect structure, symmetries, singular sets, and candidate branches.

2. **Feature refinement pass**
   - Densify near zero crossings, singular sheets, bifurcations, and stability boundaries.

3. **Convergence pass**
   - Increase resolution until the key observables used in the phase stop changing beyond the declared tolerance.

A phase summary must report both the coarse protocol and the final converged protocol.

## Program Phases

## Phase 0: Formal Reset and Specification

### Goals
- Fix notation, conventions, and admissible function classes for `a, b, c, d`.
- Define how, if at all, the angle-space object `q(omega, theta, phi, rho)` is promoted to a spacetime-dependent structure.
- Define the precise meaning of:
  - energy,
  - regularity,
  - localization,
  - stability,
  - identity,
  - and viability.
- Decide what the primary independent variable set is:
  - flat spacetime first,
  - curved spacetime later,
  - or both in parallel.

### Required Outputs
- Master specification note
- Boundary-condition note
- Scan-protocol note
- Fresh tracker files

### Gate
- Do not proceed until the program vocabulary is unambiguous.

## Phase 1: Quaternion Kinematics and Geometry

### Goals
- Derive the exact algebraic structure of the ansatz.
- Compute:
  - `q`,
  - `q^-1`,
  - derivatives,
  - norm structure,
  - Jacobians,
  - Hessians,
  - singular sets,
  - and redundancy maps.
- Determine whether the ansatz has unavoidable degeneracies that reduce nominal four-channel freedom.
- Determine whether the angle-space map itself supports any invariant classes before introducing spacetime dynamics.

### Key Questions
- Do different angle triples collapse to the same `q` or the same invariants?
- Are there sheets, branches, or locking sectors?
- Can `a, b, c, d` be chosen to preserve genuine distinctions, or do they collapse everything to `alpha`, `R`, and unit direction?

### Required Tests
- All scan families on the kinematic observables
- Symmetry detection
- Redundancy classification
- Sensitivity to admissible choices of `a, b, c, d`

### Gate
- If no nontrivial structure survives beyond coordinate redundancy, the particle-species ambition is already in serious trouble.

## Phase 2: Direct Action Families

### Goals
- Build mathematically explicit direct theories starting from the ansatz.
- Incorporate the Phase 0 and Phase 1 constraints directly, rather than re-testing already-failed assumptions.
- Reject norm-only species claims immediately.
- Identify which direct action families still preserve a plausible route to nontrivial identity.
- Classify each candidate avenue as:
  - retired,
  - viable core,
  - viable but unresolved,
  - or structurally incomplete.

### Candidate Avenue Set

1. **Minimal norm-symmetric model**
   - `q` enters only through norm-like invariants and standard kinetic terms.
   - After Phases 0 and 1, this avenue can still be studied as a baseline localized-lump model, but it is already disqualified as a direct source of angle-defined species.

2. **Derivative-anisotropic model**
   - Derivative structure treats different internal directions differently because of quaternion geometry, not because of arbitrary inserted labels.
   - This avenue is now mandatory because Phase 1 showed that any surviving identity must come from non-norm structure.

3. **Curvature-coupled model**
   - a derived spacetime object built from `q(omega, theta, phi, rho)` is coupled directly to spacetime curvature or contraction variables.
   - A curvature-coupled model is only viable if the coupled object retains more information than `|q|`.

4. **Scale-plus-unit-quaternion split**
   - Rewrite `q = e^alpha u` with `u` a unit quaternion-valued angle-space map, then derive any spacetime field version explicitly.
   - After Phase 1, this is a priority avenue because `u` is the first place where topology or nontrivial orientation structure can survive.

5. **Geometric connection/frame reinterpretation**
   - Test whether `q` should be treated as part of a frame, connection, or internal orientation bundle rather than as a multiplet scalar.
   - This avenue remains open, but it must now be judged against the Phase 1 redundancy result rather than assumed to rescue the model automatically.

### Required Outputs
- One derivation note per avenue
- Exact field equations
- Energy functionals
- Well-posedness notes
- Rejection notes for avenues that fail immediately
- A direct classification table stating:
  - whether the avenue is norm-blind to `theta, phi, rho`,
  - whether it has a nontrivial kinetic rank,
  - whether it supports a topological route,
  - and whether it survives to later phases.

### Gate
- Ill-posed or trivially degenerate avenues are retired early.
- Any action family that depends only on `|q|` and yet claims angle-defined species is retired immediately.
- At least one non-norm avenue must survive with a mathematically explicit direct action, or the program loses its particle-level path before Phase 3.

## Phase 3: Topological Machinery

### Goals
- Test whether Khantraction can literally be "knotted spacetime" rather than just a shaped lump.
- Derive candidate conserved topological quantities.
- Incorporate the Phase 2 narrowing:
  - norm-only routes are already retired,
  - so topology now lives or dies entirely through the `u` sector and its spacetime lift.
- Determine whether the default scalar-angle lift
  - `u(x) = exp(b(Theta(x)) i + c(Phi(x)) j + d(Rho(x)) k)`
  can support a nonzero physical topological charge at all.
- If the scalar-angle lift kills topology, elevate the unit-quaternion route from optional to necessary.

### Required Work
- Boundary conditions at spatial infinity
- Compactification logic where appropriate
- Candidate maps such as:
  - `angle space -> unit quaternion manifold`
  - `physical space -> unit quaternion manifold` only after the spacetime lift is derived
  - or other geometric defect maps
- Candidate charges:
  - degree / winding,
  - linking / Hopf-type structure,
  - defect number,
  - or a geometric invariant tied to curvature and the internal field
- A direct obstruction test:
  - whether a globally regular scalar-angle factorization through `R^3` forces the physical map to be null-homotopic
- A chart-coverage test:
  - whether the tested admissible families can even cover the `|v| <= pi` logarithm ball needed for full `S^3` reach

### Key Question
- Are there dynamically protected sectors that cannot relax into each other?
- Before that: does a nonzero topological sector even exist after the physical-space lift, or is it killed by the global scalar-angle parametrization?

### Gate
- If no real topological invariant exists, retire the strong "knotted species" claim and continue only with non-topological localized-state testing.
- If the scalar-angle lift is proven null-homotopic whenever the angle fields are globally regular, then nontrivial topology can only survive through:
  - the unit-quaternion field treated as fundamental,
  - or a multi-chart / singular-angle construction.

## Phase 4: Static Direct Solutions on Fixed Background

### Goals
- Solve the actual direct static equations for localized finite-energy states.
- Search for:
  - existence,
  - multiplicity,
  - branch structure,
  - compactness,
  - and invariant classification.

### Required Tests
- Radial and non-radial direct solves where derivationally justified
- Full seed scan across all variable-family subsets
- Regularity and finite-energy checks
- Dependence on `a, b, c, d` choices within the admissible class

### Gate
- If direct finite-energy localized solutions do not exist, the classical particle-level program fails here.

## Phase 5: Self-Gravitating Backreaction

### Goals
- Couple the viable static sectors to spacetime dynamics directly.
- Determine whether localization survives self-gravity without becoming pathological.

### Required Tests
- Backreacted static solves
- Horizon checks
- Curvature regularity checks
- Mass and size functional comparisons to the fixed-background states
- Full scan-family dependence

### Gate
- If the only self-consistent states are singular, horizon-trapped, or require boundary tuning with no physical interpretation, the particle claim weakens severely or fails.

## Phase 6: Linear Stability and Mode Structure

### Goals
- Linearize around direct static solutions.
- Compute the actual perturbation spectrum.

### Required Tests
- Radial and non-radial perturbations
- Growth/decay rates
- Dependence on `omega`, `theta`, `phi`, `rho`
- Separation between gauge or coordinate zero modes and genuine instabilities

### Gate
- If all candidate states are linearly unstable, the particle claim fails.

## Phase 7: Nonlinear Time Evolution and Transport

### Goals
- Test whether candidate objects survive direct time evolution.
- Establish whether they can move, scatter off perturbations, and retain identity.

### Required Tests
- 3D+1 direct evolution
- Kicks, boosts, asymmetric perturbations
- Tracking of:
  - energy,
  - size,
  - center motion,
  - internal invariants,
  - topological charges if present
- Full subset scan protocol for perturbation dependence

### Gate
- If all localized states dissolve, universalize, or lose invariant identity under direct evolution, the particle claim fails.

## Phase 8: Two-Body and Many-Body Interaction

### Goals
- Build direct multi-object initial data from the viable sectors.
- Determine whether interactions are universal or species-sensitive.

### Required Tests
- Same-sector pairs
- Distinct-sector pairs
- Mixed-background composition if the theory supports it
- Force extraction from direct evolution
- Scattering, merger, repulsion, binding, and exchange behavior
- Dependence on orientation and full scan-family subsets

### Gate
- If all interactions are universal and no invariant-specific behavior appears, the model may still describe one classical lump type, but not a particle spectrum.

## Phase 9: Vacuum Injection, Creation, Annihilation, and Emission

### Goals
- Test the original intuition directly:
  - can structured energy injection into vacuum nucleate a localized contraction?
  - can such contractions annihilate, emit radiation, or shed structure?

### Required Work
- Direct source/injection protocol from the actual equations
- Nucleation tests
- Pair-creation tests if the theory has opposite sectors
- Annihilation and radiation tests

### Constraint
- This phase is only meaningful if Phases 4 through 8 already establish a viable core object.

### Gate
- If the core object is not viable, this phase becomes descriptive only and cannot rescue the model.

## Phase 10: Observable Mapping and Viability Decision

### Goals
- Translate the direct results into a final model judgment.

### Required Questions
- Does the theory produce one universal object or multiple invariant classes?
- Are those classes stable and transportable?
- Do interactions distinguish them meaningfully?
- Does topology matter, or is the knot language unsupported?
- Is additional mathematics likely to rescue the model, or does the ansatz itself collapse the distinction?

### Final Decision Categories
- **Viable**
  - The direct program supports particle-level objecthood with genuine invariant sectors.
- **Interesting but not viable as a particle model**
  - The theory supports localized geometry but not true species-level particle structure.
- **Not viable**
  - The direct equations fail to support stable localized finite-energy objects or meaningful invariant identity.
- **Underdetermined**
  - The program cannot decide because a mathematically necessary piece is still missing.

## Explicit Abandon Criteria

Retire specific claims immediately if any of the following happens:

1. The ansatz is shown to collapse to redundant coordinates with no invariant distinction.
2. No finite-energy localized direct states exist.
3. All candidate localized states are linearly or nonlinearly unstable.
4. Distinct seeds relax to the same universal object with no invariant separator.
5. Interaction behavior is entirely universal and species-blind.
6. The "knot" idea has no actual conserved topological content.

If one or more of these occurs and cannot be repaired by a mathematically justified extension, the particle-level Khantraction claim should be abandoned rather than patched.

## Immediate Execution Order

Start with the phases most likely to kill or validate the model efficiently:

1. Phase 0: formal specification
2. Phase 1: quaternion kinematics and redundancy analysis
3. Phase 2: direct action families
4. Phase 3: topology
5. Phase 4: static direct solutions

Only if those survive should the program spend substantial effort on:

6. Phase 5: backreaction
7. Phase 6: stability
8. Phase 7: transport
9. Phase 8: interaction
10. Phase 9: creation / annihilation / emission
11. Phase 10: final decision

## What Counts as Success at the End

At the end of the restart program, there must be a single conclusion document answering:

1. Can Khantraction be a viable classical particle-level model?
2. If yes, what exact direct evidence supports that?
3. If no, what exact failure mode killed it?
4. If maybe, what missing mathematics is genuinely necessary rather than optional?

That conclusion must be based on the new direct program only, not on archived claims.
