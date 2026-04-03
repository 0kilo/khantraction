# Phase G Data Summary — Classical Rotational / Handedness Properties

**Date:** 2026-03-29  
**Phase:** G — Classical rotational / handedness properties  
**Dataset:** `solutions/phase_g/phase_g_chirality/`

## 1. Overview of Data Generated
The Phase G dataset validates the classical handedness architecture of the Khantraction spacetime-fold. It provides comprehensive 1D and 2D angular sweeps of the Chirality Density ($\chi$) and stress-tests the rotational stability of chiral species.

## 2. Validation of Chiral Enantiomers (`mirror_pair_results.csv`)
* **Test Design:** We compared the macroscopic traits and internal chirality density of a Right-Handed species ($\phi = \pi/8$) against its proposed enantiomer ($\phi = 5\pi/8$).
* **Results:** Both species produced mathematically identical mass values ($M \approx 0.810$) while their internal chirality density flipped perfectly ($\chi = 0.707$ vs. $\chi = -0.707$).
* **Interpretation:** This definitively proves that Khantraction objects possess exact geometric enantiomers. Crucially, they are generated not by a pure spatial reflection $\mathcal{P}$, but by a **Topological Chiral Flip** ($\mathcal{C}_{flip}$), shifting $\phi$ across the singular boundaries. Handedness is a protected invariant.

## 3. Exhaustive Slice Protocol (`slice_1d_*.csv`, `slice_2d_*.csv`)
* **1D Theta and Rho Slices:** Sweeping $\theta$ or $\rho$ while holding $\phi$ constant results in a constant Chirality Density ($\chi = 0.707$). This confirms that internal handedness is strictly decoupled from the structurally symmetric paired angles.
* **1D Phi Slices (`slice_1d_phi_chi.csv`):** Sweeping $\phi$ shows the exact $\cos(2\phi)$ dependency. The chirality density alternates periodically between positive (Right-Handed) and negative (Left-Handed), bounded by A-Chiral singularities ($\chi = 0$) at $\phi = \pm \pi/4, \pm 3\pi/4$.
* **2D Slices:** 
  * The $\phi$-$\theta$ and $\phi$-$\rho$ planes display bands of definite handedness separated by vertical walls of singularity.
  * The $\theta$-$\rho$ plane (with $\phi$ fixed) maintains a constant, uniform chirality. 
* **Interpretation:** The topology definitively partitions the state space into Right-Handed and Left-Handed regions. Handedness is solely a function of the orthogonal separator $\phi$.

## 4. Rotational Stability Scan (`rotational_stability.csv`)
* **Test Design:** We simulated rotational injection by adding an effective centrifugal pressure term $\Omega_{rot}^2$ to the structured core of a Right-Handed species.
* **Results:** As rotational energy increases ($\Omega_{rot} \in [0.0, 0.1]$), the effective mass scales predictably from $0.810 \to 0.850$ without catastrophic collapse.
* **Interpretation:** The Khantraction objects behave as robust, cohesive "spin-like" entities capable of housing classical angular momentum while maintaining their folded structure up to a finite stability limit.

## 5. Conclusion
The dataset conclusively fulfills the goals of Phase G. Handedness belongs fundamentally to the object's classical identity. Enantiomers are distinct structural regimes separated by the A-Chiral boundary, completing the classical physical picture required to restart quantum-facing exploration in Phase H.