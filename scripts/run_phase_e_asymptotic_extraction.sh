#!/usr/bin/env bash
# Driver script for Phase E: Deep Asymptotic Extraction
# Date: 2026-03-29

set -e

echo "Starting Phase E Deep Asymptotic Extraction..."

mkdir -p solutions/phase_e_asymptotic_extraction/
source venv/bin/activate && python analysis/phase_e_asymptotic_extraction.py

echo "Phase E Asymptotic Extraction completed successfully. Results deposited."