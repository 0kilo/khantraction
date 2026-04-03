# Phase G Synthesis — Audit Refresh

**Date:** 2026-04-02
**Phase:** G — Classical rotational / handedness properties

## Purpose

This note summarizes the audited Phase G result after tracing the paper framing, the exploration plan, the inherited Phase C to Phase F runtime chain, the chirality derivation, the rotational ansatz, the active Phase G analysis code, and the regenerated solution package.

## Synthesis

Phase G asks a sharper question than the earlier phases:

> does the object have a real classical handedness architecture, or are the apparent left/right sectors just coordinate artifacts?

The refreshed answer is clear on the handedness side and narrower on the rotational side.

What survives:
- parity preserves chirality,
- the topological chiral flip reverses chirality,
- phi partitions the domain into right-handed and left-handed sectors,
- mirror pairs remain nearly mass-degenerate on solved runs.

What fails:
- the old numerical rotational-stability claim.

The key audit correction is simple:

- the old rotational file was a mass-rescaling proxy,
- so it was never evidence of solved spin-like stability.

So the Phase G handoff is:

> classical handedness is real, but rotational dynamics still needs an actual solver-backed treatment.
