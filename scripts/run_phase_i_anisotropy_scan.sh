#!/usr/bin/env bash

# Driver script to execute the Phase I geometric anisotropy scan.
# Date: 2026-03-31

set -e

echo "Starting Phase I Geometric Anisotropy Scan..."

mkdir -p solutions/phase_i/phase_i_geometric_anisotropy_scan/
source venv/bin/activate && python analysis/phase_i/phase_i_geometric_anisotropy_scan.py

echo "Phase I Geometric Anisotropy Scan completed successfully."
echo "Results deposited in solutions/phase_i/phase_i_geometric_anisotropy_scan/"
