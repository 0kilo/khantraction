#!/usr/bin/env bash
# Driver script for Phase E: Metric Curve Fitting
# Date: 2026-03-29

set -e

echo "Starting Phase E Asymptotic Curve Fitting..."

mkdir -p solutions/phase_e_metric_curve_fitting/
source venv/bin/activate && python analysis/phase_e_metric_curve_fitting.py

echo "Phase E Curve Fitting completed successfully."