# Phase E Phenomenology Solutions Summary

**Date:** 2026-03-29
**Phase:** E — External particle-likeness

This directory contains the numerical results establishing the external particle-like behavior and effective charge of Khantraction folds.

## Asymptotic Extraction Data
- `scalar_tail.csv`, `phi_dom_tail.csv`, `fully_mixed_tail.csv`: Contain the ADM mass integration tails ($m(r)$) extracted up to $r = 40.0$.
- `summary.json`: Summarizes the Reissner-Nordström curve-fit results, providing the extracted ADM Mass ($M_{ADM}$) and Effective Topological Charge ($Q_{eff}$) for each species.

## Dynamical Response
- `dynamical_response.csv`: Measures the shift in total mass when a background gradient is applied. It shows that compact objects (Phi-dominant) have a significant inertial resistance compared to more scalar-like objects.

## Exhaustive Slice Matrices
These files fulfill the Phase E requirement to check all 6 combinations of 1D and 2D angular variation for the deep external mass proxy.
- `slice_1d_theta.csv`, `slice_1d_phi.csv`, `slice_1d_rho.csv`: 1D variations of individual angles.
- `slice_2d_theta_rho.csv`, `slice_2d_phi_theta.csv`, `slice_2d_phi_rho.csv`: 2D variations holding one angle constant.
These files demonstrate that $\phi$ variation drives substantial changes in external ADM mass and effective charge, reflecting its role as the orthogonal separator. In contrast, variations in the paired $(\theta, \rho)$ channels tend to cluster, yielding similar external configurations.

## Indistinguishability Map
- `indistinguishability_map.json`: Groups internally distinct configurations by their external $(M_{ADM}, Q_{eff})$ footprint, identifying sets of "externally identical" objects. This demonstrates that disparate internal structures can project the exact same classical external properties.