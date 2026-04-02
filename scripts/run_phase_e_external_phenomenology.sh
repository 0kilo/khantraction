#!/usr/bin/env bash
# Driver script to execute the Phase E external phenomenology and effective charge extraction.
# Date: 2026-03-29

set -e

echo "Starting Phase E External Phenomenology Analysis..."

mkdir -p solutions/phase_e/phase_e_phenomenology/
source venv/bin/activate && python analysis/phase_e/phase_e_external_phenomenology.py

echo "Phase E Analysis completed successfully."
echo "Results deposited in solutions/phase_e/phase_e_phenomenology/"
