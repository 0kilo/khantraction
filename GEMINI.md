# Khantraction Project Context

## Project Overview
**Khantraction** is an exploratory physics toy model investigating localized spacetime contractions sustained by a quaternion-valued "glue field." The project uses numerical simulations to study regular radial solutions, branch structures (from scalar-dominated to quaternion-rich regimes), and ordered quaternionic state maps.

- **Primary Technologies:** Python 3 (NumPy, SciPy), Bash (Shell scripts), Markdown (Documentation, Derivations), LaTeX (Mathematical notation).
- **Core Research Areas:** Quaternionic field theory, nonminimal coupling to curvature, radial solver implementations, and proto-excitation spectrum analysis.

## Directory Structure & Responsibilities
The project follows a strict organizational layout as defined in `notes/implementation_workflow.md`:

- `analysis/`: Reusable Python analysis logic, simulations, parameter scans, and observable extraction.
- `derivations/`: Mathematical theory, Jacobian derivations, and operator ansatz documentation.
- `notes/`: Active interpretation, phase assessments, experiment reasoning, and closure notes.
- `scripts/`: Executable driver scripts and reproducible entry points for experiments.
- `solutions/`: Current generated outputs (CSV, JSON, profile dumps) organized by phase and topic.
- `summary/`: Polished milestone summaries and high-level research syntheses.

## Phase-Based Workflow
Research is organized into thematic phases (A–H):
- **Phase A:** Parameter foundation (scale vs. channels).
- **Phase B:** Structured-object picture (viability and stability).
- **Phase C:** Distinct angular traits ($\theta, \phi, \rho$).
- **Phase D:** Identity and persistence (family fingerprints).
- **Phase E:** External particle-likeness.
- **Phase F:** Hosting properties (external content sensitivity).
- **Phase G:** Handedness / chirality classes.
- **Phase H:** Quantum-facing work (excitation spectra).

## Development Conventions
- **Naming Convention:** Use `phase_{letter}_{topic}` for files in `analysis/`, `scripts/`, `notes/`, and subfolders in `solutions/`.
- **Experiment Protocol:**
    1.  Create/update an analysis file in `analysis/`.
    2.  Execute via a script in `scripts/`.
    3.  Store results in a dedicated subfolder in `solutions/`.
    4.  Document interpretation in a `notes/` assessment file.
- **Mathematical Style:** Derivations use standard LaTeX in Markdown. The primary state map is $Q(\omega, \theta, \phi, \rho) = e^{\omega} e^{\theta i} e^{\phi j} e^{\rho k}$.

## Building and Running
- **Running Analyses:** Use the provided shell scripts in `scripts/`.
    - Example: `./scripts/run_phase_b_full_radial_solver.sh`
- **Manual Execution:** Python files in `analysis/` can be run directly if arguments are provided.
    - Example: `python3 analysis/phase_b/phase_b_full_radial_solver.py --help`
- **Dependencies:** Ensure a Python environment is active (e.g., `source venv/bin/activate`) with `numpy` installed.

## Key Files
- `khantraction_paper.md`: The primary research report and theoretical overview.
- `notes/implementation_workflow.md`: The canonical guide for project structure and naming.
- `notes/classical_exploration_plan.md`: The strategic roadmap for the current research phase.
