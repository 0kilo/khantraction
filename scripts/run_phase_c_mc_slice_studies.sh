#!/usr/bin/env bash

# Driver script to execute the Phase C Maurer-Cartan Slice Studies
# Date: 2026-03-29

set -e

echo "Starting Phase C Maurer-Cartan 1D and 2D Slice Scans..."

mkdir -p solutions/phase_c_mc_slice_studies/
source venv/bin/activate && python analysis/phase_c_mc_anisotropy_slice_studies.py

echo "Phase C Slice Scans completed successfully."