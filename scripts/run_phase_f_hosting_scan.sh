#!/bin/bash

# scripts/run_phase_f_hosting_scan.sh
# Purpose: Orchestrate the Phase F Hosting Sensitivity Scan
# Following the Phase F Plan for Khantraction

# 1. Ensure the execution environment is set to the repository root
# 2. Verify output directories exist
mkdir -p solutions/phase_f_hosting_properties

echo "--- Initializing Phase F: Classical Hosting Properties ---"
echo "Target Domain: theta, phi, rho in [-2pi, 2pi], omega > 0"

# 3. Execute the analysis using the Python interpreter
# This avoids the shell syntax errors previously encountered.
source venv/bin/activate && python analysis/phase_f_hosting_sensitivity_scan.py

# 4. Final check of output status
if [ $? -eq 0 ]; then
    echo "--- Phase F Scan Complete ---"
    echo "Results available in solutions/phase_f_hosting_properties/"
else
    echo "--- Phase F Scan Failed ---"
    exit 1
fi