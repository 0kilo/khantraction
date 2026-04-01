#!/usr/bin/env bash

# Driver script to execute the Phase K multi-fold interaction suite.
# Date: 2026-03-31

set -e

echo "Starting Phase K Multi-Fold Interaction Suite..."

mkdir -p solutions/phase_k/phase_k_multi_fold_interaction/
source venv/bin/activate && python analysis/phase_k/phase_k_multi_fold_force_law.py

echo "Phase K Multi-Fold Interaction Suite completed successfully."
echo "Results deposited in solutions/phase_k/phase_k_multi_fold_interaction/"
