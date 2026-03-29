#!/usr/bin/env bash
# Driver script for Phase D: Neighborhood Stability Sweep
# Date: 2026-03-29

set -e

echo "Starting Phase D Neighborhood Stability Grid..."

mkdir -p solutions/phase_d_neighborhood_stability/
source venv/bin/activate && python analysis/phase_d_neighborhood_stability.py

echo "Phase D Neighborhood Sweep completed successfully. Results deposited."