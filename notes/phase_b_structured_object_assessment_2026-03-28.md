# Phase B Assessment — Rebuilding the Structured-Object Picture

**Date:** 2026-03-28  
**Phase:** B — Structured-object picture  
**Status:** In progress

## Purpose

This note starts the active Phase B work in the fresh project tree.

Phase B asks:

> does Khantraction produce a coherent compact structured-object family, rather than merely a mathematically interesting branch of solutions?

This is the objecthood phase of the classical program.

---

## 1. Verified current file status

A check of the active `projects/physics/` tree shows that there are effectively **no Phase B implementation files yet** in the fresh-start layout.

So this note is not summarizing an already-populated Phase B folder.
It is establishing the assessment framework that the new active Phase B work should follow.

That matches the workflow rule in `notes/implementation_workflow.md`:

> because this is a fresh-start active tree, do not write notes as if prior phase files already exist here. Create them only when they are actually produced.

---

## 2. What Phase B inherits from Phase A

Phase A is now treated as closed.
Its main handoff is:
- \(\omega\) = pure scale coordinate
- \(\phi\) = orthogonal separator / mixing-control coordinate
- \(\theta,\rho\) = paired internal structural directions

That matters because Phase B should **not** revisit the parameter-foundation question.
Instead, it should ask whether the actual solution family supports a genuine structured-object interpretation.

So the logic is:
- Phase A established ordered internal geometry.
- Phase B must establish actual **classical objecthood**.

---

## 3. Core Phase B question

The right Phase B question is not:
- “did we find a rich branch?”

It is:

> is the rich/full-quaternion branch best interpreted as a coherent compact structured object with a stable external profile and organized interior?

That is the level of claim Phase B needs to justify.

---

## 4. What Phase B needs to prove

To count as successful, Phase B should establish four main things.

### 4.1 Family coherence

The strongest rich/full-quaternion regime should appear as one broad coherent family, not as an isolated special seed or a fragile artifact.

What to test:
- regularity across nearby seeds,
- continuity of observables across the family,
- whether the branch persists under reasonable seed variation,
- whether the family fragments into multiple incompatible subfamilies or remains one broad object class.

### 4.2 Compact external profile

The rich branch should be externally compact enough to justify object language.

Key observables from the roadmap:
- mass half-radius,
- mass 90% radius,
- curvature half-radius,
- curvature 90% radius,
- effective external settling radius.

The main issue is not whether the object is pointlike.
It is whether its exterior profile settles quickly enough that the object behaves compactly from the outside.

### 4.3 Internal organization

Compactness alone is not enough.
Phase B should also show that the object has internal structure that can be described coherently.

Target descriptive features:
- a recognizable core,
- a bulk/interior region,
- a transition or soft region,
- and some basis for saying the interior is folded/organized rather than shapeless.

This is the heart of the “structured-object” interpretation.

### 4.4 Stable object identity at the broad family level

Phase B does not need the full identity machinery of Phase D yet.
But it should show enough persistence that one can reasonably speak of:
- a scalar-like family,
- a rich/full-quaternion family,
- and one broad coherent structured-object class within the rich regime.

Without this, later questions about traits, hosting, or handedness are premature.

---

## 5. Current best Phase B interpretation target

If Phase B succeeds, the correct statement should look something like:

> Khantraction supports a coherent compact structured-object family whose rich/full-quaternion regime is more concentrated, internally organized, and externally settled than the scalar-like regime, making it the best current classical candidate for object-like or particle-like behavior.

That is the target wording level.

---

## 6. What Phase B should *not* overclaim

Even if Phase B goes well, it should still avoid claiming:
- literal point particles,
- validated Standard Model objects,
- hard species/topology labels,
- or trait assignments to \(\theta,\phi,\rho\) before Phase C.

Phase B is about **objecthood**, not yet full trait decomposition.

---

## 7. Immediate implementation plan for Phase B

The first active Phase B work in the fresh tree should probably be split into three concrete tasks.

### Task 1 — Branch viability / family coherence analysis
Create:
- `analysis/phase_b_branch_viability.py`
- outputs in `solutions/phase_b_branch_viability/`
- note interpreting whether the rich regime forms one broad coherent family

### Task 2 — Compactness / concentration analysis
Create:
- `analysis/phase_b_compactness_observables.py`
- outputs in `solutions/phase_b_compactness_observables/`
- note comparing key radii and concentration measures between scalar-like and rich regimes

### Task 3 — Structured profile interpretation
Create:
- `analysis/phase_b_profile_structure.py`
- outputs in `solutions/phase_b_profile_structure/`
- note defining core / bulk / soft-region diagnostics and checking whether the rich branch supports them

That would satisfy the workflow and give Phase B an orderly foundation.

---

## 8. Provisional Phase B stance before implementation

The project’s roadmap strongly suggests that the rich/full-quaternion regime is the best current candidate for a compact structured object.
But in the fresh tree that has not yet been re-established with active files.

So the correct current stance is:

> Phase B is plausible and well-motivated, but not yet active in the current tree. Its first job is to rebuild the objecthood evidence in a disciplined, observable-driven way.

---

## 9. Bottom line

**Bottom line:** Phase B should now be treated as the objecthood phase of Khantraction. Its task is to show that the rich/full-quaternion branch is a coherent compact structured-object family with a stable external profile and organized interior. The fresh tree currently has no active Phase B implementation files, so the next step is to create the first Phase B analyses that test family coherence, compactness/concentration observables, and internal profile structure.
