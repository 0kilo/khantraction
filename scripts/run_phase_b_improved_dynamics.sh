#!/usr/bin/env bash
set -euo pipefail

ROOT="/home/mcesel/.openclaw/workspace/projects/physics"
cd "$ROOT"

python3 analysis/phase_b/phase_b_improved_dynamics_solver.py "$@"
