#!/usr/bin/env bash
# Driver script for Phase D: Species Clustering and Identity Mapping
# Date: 2026-03-29

set -e

echo "Starting Phase D Species Clustering..."

mkdir -p solutions/phase_d_species_clustering/
source venv/bin/activate && python analysis/phase_d_species_clustering.py

echo "Phase D Species Clustering completed successfully. Results deposited."