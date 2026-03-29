#!/usr/bin/env bash
# Driver script to generate the exact symbolic gradients for the Anisotropic Maurer-Cartan Lagrangian
# Date: 2026-03-29

set -e

echo "Starting Phase C Maurer-Cartan Equation Generation..."

mkdir -p solutions/phase_c_mc_equations/
source venv/bin/activate && python analysis/phase_c_mc_equation_generator.py

echo "Phase C MC Equation Generation completed successfully."