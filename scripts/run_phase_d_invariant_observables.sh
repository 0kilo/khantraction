#!/usr/bin/env bash
# Driver script for Phase D: Scale-Invariant Fingerprinting
# Date: 2026-03-29

set -e

echo "Starting Phase D Invariant Observable Sweep..."

mkdir -p solutions/phase_d_invariant_observables/
source venv/bin/activate && python analysis/phase_d_invariant_observables.py

echo "Phase D Sweep completed successfully. Results deposited."