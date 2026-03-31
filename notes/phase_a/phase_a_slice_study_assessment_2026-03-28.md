# Phase A Assessment — Explicit 1D and 2D Slice Studies

**Date:** 2026-03-28  
**Phase:** A — Parameter foundation  
**Status:** In progress

## Purpose

This note starts the next Phase A substep:

> explicitly study slices of the ordered quaternion map by holding two angular parameters fixed and varying one, and by holding one fixed while varying two.

The goal is to make the mapping geometry interpretable in a more concrete way than a full bulk scan.

## Active domain convention

Use:
- \(\omega>0\)
- \(\theta,\phi,\rho\in[-2\pi,2\pi]\)
- no redundancy quotienting

## Why slice studies matter

The earlier bulk scans established:
- local angular independence in regular regions,
- and a singular-sheet structure governed by \(\phi\).

But bulk scans can hide the actual geometric picture.

Slice studies should answer more visibly:
- if I vary only \(\phi\), what changes directly?
- if I vary only \(\theta\) or only \(\rho\), does the determinant stay regular away from singular \(\phi\)?
- if I hold \(\phi=0\) versus \(\phi=\pi/4\), how differently do the \((\theta,\rho)\)-planes behave?

## Active implementation

The slice-analysis file is:
- `analysis/phase_a/phase_a_slice_studies.py`

Outputs are stored under:
- `solutions/phase_a/phase_a_slice_studies/`

## What to look for

The main expected checks are:
1. 1D \(\phi\)-slices should show repeated zero crossings at the predicted singular \(\phi\)-values.
2. 1D \(\theta\)- or \(\rho\)-slices with regular fixed \(\phi\) should remain non-singular.
3. 2D slices with fixed \(\phi=\pi/4\) should visibly collapse into a singular sheet.
4. 2D slices with fixed \(\phi=0\) should remain regular across the sampled box.

## Interpretation target

If those checks hold, the Phase A picture becomes sharper:
- \(\phi\) controls chart singularity architecture,
- while \(\theta\) and \(\rho\) vary within regular sheets except where the chart itself collapses.

That still would not prove trait-level physical hierarchy, but it would make the coordinate geometry much more transparent.
