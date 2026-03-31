#!/usr/bin/env bash

# Driver script to execute the Phase B exact radial solver and generate observable outputs.
# Date: 2026-03-29

set -e

echo "Starting Phase B Exact Radial Update..."

mkdir -p solutions/phase_b/phase_b_exact_radial_solver/profiles/
source venv/bin/activate && python analysis/phase_b/phase_b_exact_radial_solver.py

echo "Phase B Exact Radial Update completed successfully."
echo "Results deposited in solutions/phase_b/phase_b_exact_radial_solver/"