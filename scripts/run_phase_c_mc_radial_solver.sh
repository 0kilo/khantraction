#!/usr/bin/env bash
# Driver script to execute the Phase C Maurer-Cartan radial solver and test for angular trait splitting.
# Date: 2026-03-29

set -e

echo "Starting Phase C Angular Trait Extraction..."

mkdir -p solutions/phase_c_angular_traits/profiles/
source venv/bin/activate && python analysis/phase_c_mc_radial_solver.py

echo "Phase C Trait Extraction completed successfully."
echo "Results deposited in solutions/phase_c_angular_traits/"