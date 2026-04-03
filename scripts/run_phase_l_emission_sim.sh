#!/usr/bin/env bash

# Driver script to execute the refreshed Phase L emission proxy suite.
# Date: 2026-03-31

set -e

echo "Starting Phase L emission proxy suite..."

mkdir -p solutions/phase_l/phase_l_topological_shedding/
source venv/bin/activate && python analysis/phase_l/phase_l_topological_shedding.py

echo "Phase L emission proxy suite completed successfully."
echo "Results deposited in solutions/phase_l/phase_l_topological_shedding/"
