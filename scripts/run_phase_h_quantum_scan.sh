#!/bin/bash

# scripts/run_phase_h_quantum_scan.sh
# Purpose: Orchestrate the Phase H Quantum Mode Ladder Scan
# Transitions from classical hosting/chirality to discrete excitations.

# 1. Ensure the execution environment is set to the repository root
# 2. Verify output directories exist for quantum results
mkdir -p solutions/phase_h_quantum_results

echo "--- Initializing Phase H: Quantum-Facing Work ---"
echo "Target: Searching for discrete eigenvalues (En) in hosting basins."
echo "Parameters: Using Phase F hosting depths and Phase G chirality density."

# 3. Execute the mode ladder analysis using the Python interpreter
# This script solves the quantization conditions derived in Derivation 85.
source venv/bin/activate && python analysis/phase_h_mode_ladder_scan.py

# 4. Final check of output status
if [ $? -eq 0 ]; then
    echo "--- Phase H Quantum Scan Complete ---"
    echo "Excitation Spectrum: solutions/phase_h_quantum_results/excitation_spectrum.json"
    echo "Transitioning to final assessment..."
else
    echo "--- Phase H Quantum Scan Failed ---"
    exit 1
fi