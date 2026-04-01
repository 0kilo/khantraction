#!/usr/bin/env bash

# Driver script to execute the Phase M pair creation and annihilation suite.
# Date: 2026-03-31

set -e

echo "Starting Phase M Pair Creation and Annihilation Suite..."

mkdir -p solutions/phase_m/phase_m_creation_annihilation/
source venv/bin/activate && python analysis/phase_m/phase_m_creation_annihilation_sim.py

echo "Phase M Pair Creation and Annihilation Suite completed successfully."
echo "Results deposited in solutions/phase_m/phase_m_creation_annihilation/"
