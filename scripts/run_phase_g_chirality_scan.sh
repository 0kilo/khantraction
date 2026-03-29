#!/bin/bash

# scripts/run_phase_g_chirality_scan.sh
# Purpose: Orchestrate the Phase G Chirality and Mirror-Pair Scan
# Following the Phase G Plan for Khantraction

# 1. Ensure the execution environment is set to the repository root
# 2. Verify output directories exist for rotational/handedness results
mkdir -p solutions/phase_g_rotational_handedness

echo "--- Initializing Phase G: Classical Rotational / Handedness Properties ---"
echo "Target Domain: theta, phi, rho in [-2pi, 2pi], omega > 0"
echo "Objective: Validating P-transformation and mirror-pair trait invariance."

# 3. Execute the chirality analysis using the Python interpreter
# This script performs the parity mapping P: (ang) -> (-ang)
source venv/bin/activate && python analysis/phase_g_chirality_scan.py

# 4. Final check of output status and location of generated data
if [ $? -eq 0 ]; then
    echo "--- Phase G Chirality Scan Complete ---"
    echo "Mirror-pair results: solutions/phase_g_rotational_handedness/chirality_comparison_results.csv"
    echo "Species fingerprints: solutions/phase_g_rotational_handedness/handedness_fingerprints.json"
else
    echo "--- Phase G Chirality Scan Failed ---"
    exit 1
fi