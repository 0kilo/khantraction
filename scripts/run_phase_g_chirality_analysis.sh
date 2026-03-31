#!/usr/bin/env bash
# Driver script to execute the Phase G classical chirality and handedness analysis.
# Date: 2026-03-29

set -e

echo "Starting Phase G Chirality and Handedness Analysis..."

mkdir -p solutions/phase_g/phase_g_chirality/
source venv/bin/activate && python analysis/phase_g/phase_g_chirality_analysis.py

echo "Phase G Analysis completed successfully."
echo "Results deposited in solutions/phase_g/phase_g_chirality/"
