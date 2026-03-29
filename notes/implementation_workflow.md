# Implementation Workflow for `classical_exploration_plan.md`

## Current inventory

Top-level structure present:
- `analysis/`
- `derivations/`
- `notes/`
- `scripts/`
- `solutions/`
- `summary/`
- `khantraction_paper.md`
- `history.html`

The active implementation folders should be treated as a fresh start.
Use the roadmap in `notes/classical_exploration_plan.md` as the canonical plan and create implementation files phase by phase in the active layout.

---

## Folder responsibilities

To avoid the earlier archive/solutions confusion, use this layout strictly:

### `derivations/`
Use for mathematical derivations and theory writeups.
Examples:
- parameter maps
- Jacobian work
- operator ansatz derivations
- Maurer–Cartan notes

### `analysis/`
Use for analysis code that computes, scans, classifies, or extracts observables.
Examples:
- parameter sweeps
- family fingerprint analysis
- viable-region filters
- operator comparison scripts

### `scripts/`
Use for executable driver scripts and reproducible entry points.
Examples:
- run a scan
- rerun a phase
- generate a table/report from analyses

Rule of thumb:
- `analysis/` = reusable analysis logic
- `scripts/` = runnable orchestration / experiment entrypoints

### `solutions/`
Use for all current generated outputs.
Examples:
- CSVs
- TXT summaries
- generated tables
- profile dumps
- scan outputs

No new current results should go into `archive/`.

### `notes/`
Use for active interpretation, phase assessments, closure notes, workflow notes, and research reasoning.
Examples:
- phase assessments
- phase closure notes
- experiment interpretation
- next-step operator plans

### `summary/`
Use only for polished summaries.
Examples:
- research-state summary
- milestone summary
- high-level synthesis for later reference

Do **not** put active plans or unfinished operator notes here.

---

## Naming workflow

Use a stable pattern so the tree stays readable.

### Analysis files
- `analysis/phase_a_<topic>.py`
- `analysis/phase_b_<topic>.py`
- ...
- `analysis/phase_h_<topic>.py`

### Script files
- `scripts/run_phase_a_<topic>.sh`
- `scripts/run_phase_b_<topic>.sh`
- or `scripts/run_<experiment>.py` if Python is cleaner

### Solution outputs
- `solutions/phase_a_<topic>/...`
- `solutions/phase_b_<topic>/...`
- etc.

Each experiment gets its own subfolder under `solutions/`.

### Notes
- `notes/phase_a_<topic>_assessment.md`
- `notes/phase_a_closure.md`
- and similarly for later phases

### Summary files
- `summary/<date>_<milestone>_summary.md`

---

## Phase-by-phase implementation workflow

## Phase A — Parameter foundation
Goal:
- cleanly establish \(\omega\) as scale and \(\theta,\phi,\rho\) as distinct channels

### Outputs to create
- derivation note for the clean parameter map / Jacobian comparison
- parameter sweep analysis
- generated sweep outputs in `solutions/phase_a_*`
- Phase A assessment note
- Phase A closure note

---

## Phase B — Structured-object picture
Goal:
- establish coherent compact structured-object family

### Outputs to create
- branch viability analysis
- stress test analysis
- scale-vs-structure analysis
- generated outputs in `solutions/phase_b_*`
- Phase B assessment note
- Phase B closure note

---

## Phase C — Distinct angular traits
Goal:
- determine whether \(\theta,\phi,\rho\) correspond to different object traits

### Outputs to create
- ordered-parameter bridge analysis
- profile-comparison analysis
- angle-sensitive diagnostic analysis
- geometry-informed operator analysis
- generated outputs in `solutions/phase_c_*`
- Phase C assessment note
- Phase C closure note

---

## Phase D — Identity and persistence
Goal:
- define same-family vs different-family

### Outputs to create
- viable-region analysis
- family-fingerprint analysis
- generated outputs in `solutions/phase_d_*`
- Phase D identity assessment note
- Phase D closure note

---

## Phase E — External particle-likeness
Goal:
- determine whether objects are externally particle-like up to normalization or stronger

### Outputs to create
- external-shape analysis
- viable external-overlap analysis
- generated outputs in `solutions/phase_e_*`
- Phase E assessment note
- Phase E closure note

---

## Phase F — Hosting properties
Goal:
- test whether the object can host externally supplied content

### Outputs to create
- hosting probe analysis
- signed loading scan
- hosting-region analysis
- generated outputs in `solutions/phase_f_*`
- Phase F assessment note
- Phase F closure note

---

## Phase G — Handedness / chirality
Goal:
- determine whether angular sectors define chirality classes

### Outputs to create
- chirality scan
- mirror comparison analysis
- generated outputs in `solutions/phase_g_*`
- Phase G assessment note
- Phase G closure note

---

## Phase H — Return to quantum-facing work
Only after A–G are complete enough.

---

## Experiment protocol

For every new experiment:

1. **Create/update one analysis file** in `analysis/`
2. **Run it via a script or direct command** from `scripts/` or shell
3. **Write outputs into one dedicated subfolder** under `solutions/`
4. **Write one interpretation note** in `notes/`
5. If a phase burden of proof is met, **write a closure note** in `notes/`
6. Only after a milestone is stable, write a high-level summary into `summary/`

---

## Minimal rules going forward

1. No new current outputs in `archive/`
2. No active work notes in `summary/`
3. Every major claim in a note should point to either:
   - a derivation in `derivations/`, or
   - a generated result in `solutions/`
4. Notes should interpret; solutions should store raw/generated values.
5. Always keep all parameters in play unless a reduced slice is explicitly declared.
6. Because this is a fresh-start active tree, do not write notes as if prior phase files already exist here. Create them only when they are actually produced.

---

## Immediate next implementation step

Because the tree is now a fresh start, the correct next step is:

> create the first active files for the next phase in the proper `analysis/`, `solutions/`, and `notes/` layout.

That means starting implementation from the roadmap directly, not assuming prior active results already exist in this tree.
