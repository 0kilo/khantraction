#!/usr/bin/env bash
# Driver script to execute the Phase D identity, persistence, and rigidity analysis.
# Date: 2026-03-29

set -e

echo "Starting Phase D Identity and Rigidity Analysis..."

mkdir -p solutions/phase_d/phase_d_identity/
source venv/bin/activate && python analysis/phase_d/phase_d_identity_analysis.py

echo "Phase D Analysis completed successfully."
echo "Results deposited in solutions/phase_d/phase_d_identity/"
