# Phase I Note — Heuristic Physical-Analog Proposals and Current Limits

**Date:** 2026-04-02  
**Phase:** I — First-Principles Derivation of Constants

## Purpose

This note records the current status of the “physical analog” part of Phase I after the audit refresh.

## 1. What survives

The pullback scan does provide useful geometric quantities that could later be compared to observables:

- a unit-scale paired-mode gap
  $$
  \Delta_{\text{unit}}(\phi)=2|\sin(2\phi)|
  $$
- an active-scale paired-mode gap
  $$
  \Delta_{\text{active}}(\phi,\omega)=2e^{2\omega}|\sin(2\phi)|
  $$

At `phi = pi/8`:

- `Delta_unit = 1.414213562373095`
- `Delta_active(omega = 0.5) = 3.844231028159116`

These are real geometric diagnostics of channel splitting.

## 2. What does not survive

The earlier note treated two quantities as if they had already been mapped to observables:

- `alpha_K = xi`
- `Delta M_g = 2|sin(2phi)|`

That is too strong.

Reasons:

- `xi` is still an input model parameter, not an observable extracted from a new first-principles interaction calculation.
- `2|sin(2phi)|` is only the **unit-scale** stiffness split of the pullback scan. It is not yet a measured mass gap from a dynamical spectrum.
- the active scan at fixed `omega = 0.5` actually carries the scale factor `e^{2omega}`, so even the raw geometric gap depends on how the comparison is normalized.

## 3. Correct interpretation

The honest Phase I reading is:

- geometric gap diagnostics exist,
- those diagnostics may become candidates for later observable analogs,
- but the mapping to physical observables remains open.

So Goal 3 of `notes/real_physics_transition_plan.md` is not yet closed.

## 4. Bottom line

**Bottom line:** Phase I currently offers heuristic geometric candidates for later observable analogs, not derived observable constants. Any future “fine-structure” or “mass-gap” language has to come from a later dynamical extraction, not from the present pullback scan alone.
