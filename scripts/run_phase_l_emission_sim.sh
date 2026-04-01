#!/usr/bin/env bash

# Driver script to execute the Phase L topological shedding and particle emission suite.
# Date: 2026-03-31

set -e

echo "Starting Phase L Topological Shedding Suite..."

mkdir -p solutions/phase_l/phase_l_topological_shedding/
source venv/bin/activate && python analysis/phase_l/phase_l_topological_shedding.py

echo "Phase L Topological Shedding Suite completed successfully."
echo "Results deposited in solutions/phase_l/phase_l_topological_shedding/"
