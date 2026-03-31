#!/usr/bin/env bash
# Driver script to execute the Phase H quantum mode ladder scan and enantiomeric splitting validation.
# Date: 2026-03-30

set -e

echo "Starting Phase H Quantum Mode Ladder Analysis..."

mkdir -p solutions/phase_h/phase_h_quantum/
source venv/bin/activate && python analysis/phase_h/phase_h_quantum_analysis.py

echo "Phase H Analysis completed successfully."
echo "Results deposited in solutions/phase_h/phase_h_quantum/"
