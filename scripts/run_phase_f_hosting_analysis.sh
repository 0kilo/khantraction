#!/usr/bin/env bash
# Driver script to execute the Phase F classical hosting and signed loading analysis.
# Date: 2026-03-29

set -e

echo "Starting Phase F Hosting and Signed Loading Analysis..."

mkdir -p solutions/phase_f/phase_f_hosting/
source venv/bin/activate && python analysis/phase_f/phase_f_hosting_analysis.py

echo "Phase F Analysis completed successfully."
echo "Results deposited in solutions/phase_f/phase_f_hosting/"
