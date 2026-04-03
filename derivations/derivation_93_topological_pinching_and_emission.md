# Derivation 93: Topological Pinching and the Emission of Massless Packets

**Date:** 2026-03-31  
**Phase:** L — Topological Shedding / Particle Emission

> Audit note (2026-04-02): this document records the intended topological-emission ansatz for Phase L. The active audited runtime in `analysis/phase_l/phase_l_topological_shedding.py` does not implement this derivation directly; it uses a narrower algebraic emission proxy with a hand-built advected packet trajectory. In particular, the discrete mode-ladder step discussed below is still a target relation rather than an implemented Phase L result.

## 1. Background
In the transition to a "real physics model," we must identify how a structured fold loses energy. Unlike a classical ball losing heat, a spacetime-fold must lose energy in discrete, topologically consistent packets.

## 2. The Excitation State ($n=1$)
If a stronger successor to the current Phase H proxy establishes an excited fold state in a Maurer-Cartan-derived potential well, the transition from a first excited state $E_1$ to a lower state $E_0$ would require the release of energy $\Delta E = E_1 - E_0$.

## 3. The Pinching Condition
We propose that the energy release is mediated by a **Topological Pinch**. As the internal angular state $(\theta, \phi, \rho)$ rapidly shifts from the excited resonance to the ground anchor, the localized gradient energy $\mathcal{G}$ in the soft-region ($r \approx r_{90}$) exceeds the core's binding capacity.

The condition for "budding" is:

$$
\int_{r_{core}}^{r_{max}} |\partial_\mu Q_{ang}|^2 \, d^3x > \mathcal{T}_{binding}
$$

where $Q_{ang}$ is the purely angular part of the quaternionic state map.

## 4. Massless Wave-Packet (Photon Analogue)
For the emitted packet to be massless, it must decouple from the central scale $\omega$. In the ordered map:

$$
Q = e^\omega Q_{ang}(\theta, \phi, \rho)
$$

The packet consists of a propagating fluctuation in the $Q_{ang}$ manifold that satisfies the linear wave equation in the vacuum background:

$$
(-\partial_t^2 + \nabla^2) \delta Q_{ang} = 0
$$

## 5. Discrete Step Mapping
The emission event is mapped to the step-down in the Bohr-Sommerfeld integral:

$$
\Delta n = \frac{1}{\pi} \int \sqrt{E_{final}^2 - V_{eff}} \, dr - \frac{1}{\pi} \int \sqrt{E_{initial}^2 - V_{eff}} \, dr = -1
$$

This identifies the "Particle Split" as a discrete jump in the internal topology of the fold.

## 6. Target Implementation for Phase L
The intended strong implementation would simulate a dynamic "jump" in the internal parameters and measure the resulting outward-propagating energy flux to verify that it carries the exact $\Delta E$ required by the ladder step.

The current audited Phase L package is narrower. It implements:

- an algebraic excitation proxy proportional to $\theta^2 + \rho^2$,
- a $\phi$-dependent gating factor proportional to $1 - 0.9 |\cos(2\phi)|$,
- and a hand-built Gaussian packet translated at fixed speed.

So the current package is useful for mapping a candidate emission landscape, but it is not yet a direct realization of the pinch condition or the ladder-budget equation written above.

---
**Conclusion:** This ansatz outlines a possible geometric route to particle emission by topological shedding. A stronger future implementation would still need to realize the pinch condition dynamically, solve the emitted packet from the field equations, and connect the released energy to a solver-backed discrete ladder.
