# Phase E Exploration Plan — External Particle-Likeness and Effective Charge

**Date:** 2026-03-29
**Phase:** E — External particle-likeness
**Status:** Active Pathway Selected

## Purpose
This note establishes the roadmap for Phase E. Phases A through D were strictly focused on the *internal* geometry of Khantraction objects, ultimately proving that they form discrete, quantized topological species separated by invariant compactness ratios. 

Phase E pivots the investigation outward. We must now determine if these complex extended spacetime folds masquerade as standard point-particles when viewed from a distance, and whether their internal non-commutative geometry leaks out as a measurable macroscopic "charge."

---

## 1. The Core Scientific Questions
1. **Asymptotic Metric Matching:** Does the external spacetime metric decay perfectly to the Schwarzschild vacuum (\(g_{tt} \approx -1 + \frac{2M}{r}\)), or does it carry a residual Reissner-Nordström-like \(1/r^2\) term (\(+ \frac{Q^2}{r^2}\))?
2. **Effective Topological Charge:** The Maurer-Cartan non-commutative gradients explicitly break \(O(4)\) symmetry in the core. Does this symmetry-breaking energy remain perfectly confined (like the strong nuclear force), or does it project an effective long-range force field (like electromagnetism)?
3. **Scalar Hair:** Does the internal quaternion field \(q\) settle perfectly into its vacuum state \(U(|q|) = 0\), or do the objects possess persistent "scalar hair" that bleeds into the surrounding spacetime?

---

## 2. The Implementation Roadmap

### Step 1: Deep Asymptotic Extraction (`analysis/phase_e_asymptotic_extraction.py`)
- The previous Phase C and D solvers terminated at \(r=20.0\) to save computational overhead, which is insufficient for precision asymptotic curve fitting.
- We will build a solver that integrates the 4 topological species (Scalar, \(\theta\)-dom, \(\phi\)-dom, Fully-mixed) out to a deep boundary (\(r_{\text{max}} = 100.0\)).
- The script will truncate the dense inner core data and heavily sample the outer tail (\(r > 20.0\)), extracting the Misner-Sharp mass \(m(r)\) and the metric potential \(\Phi(r)\).

### Step 2: Metric Curve Fitting (`analysis/phase_e_metric_curve_fitting.py`)
- We will ingest the asymptotic tails and perform a precision numerical regression against known general relativistic point-particle metrics.
- We will fit the extracted mass function \(m(r)\) against the model: \( m(r) = M_{\text{ADM}} - \frac{Q_{\text{eff}}^2}{2r} \).
- **Goal:** Isolate the ADM mass and the effective topological charge \(Q_{\text{eff}}\) for each species.

### Step 3: Species Phenomenology Assessment (`notes/phase_e_phenomenology_assessment.md`)
- Compare the extracted \(Q_{\text{eff}}\) across the 4 species. 
- If the scalar anchor produces \(Q_{\text{eff}} \approx 0\) but the fully-mixed anchor produces a distinct \(Q_{\text{eff}} > 0\), we will have mathematically proven that Khantraction generates charged particle families solely from geometric folds.
- Formally close Phase E.