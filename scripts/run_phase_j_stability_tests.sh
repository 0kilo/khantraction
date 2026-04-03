#!/usr/bin/env bash

# Driver script to execute the Phase J 3D dynamic stability tests.
# Date: 2026-03-31

set -e

echo "Starting Phase J 3D Dynamic Stability Tests..."

mkdir -p solutions/phase_j/phase_j_dynamic_stability/
source venv/bin/activate && python analysis/phase_j/phase_j_dynamic_stability_solver.py

echo "Phase J Dynamic Stability Tests completed successfully."
echo "Results deposited in solutions/phase_j/phase_j_dynamic_stability/"
