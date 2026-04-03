#!/usr/bin/env bash

# Driver script to execute the Phase J anchored 3D wave-proxy stability audit.
# Date: 2026-03-31

set -e

echo "Starting Phase J anchored 3D wave-proxy stability audit..."

mkdir -p solutions/phase_j/phase_j_dynamic_stability/
source venv/bin/activate && python analysis/phase_j/phase_j_dynamic_stability_solver.py

echo "Phase J anchored stability audit completed successfully."
echo "Results deposited in solutions/phase_j/phase_j_dynamic_stability/"
