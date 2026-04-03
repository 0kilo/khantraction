# Phase L Topological Shedding Solution Summary

**Date:** 2026-03-31
**Phase:** L — Topological Shedding / Particle Emission

This directory contains the numerical results for the Phase L investigation of particle emission.

## 1. Description of Output Files

### 1D Slices
These files track the emission flux while sweeping one parameter across the full active domain $[-2\pi, 2\pi]$ and keeping the other two fixed:
- `vary_theta_phi_fixed_rho_fixed.csv`: Sweeps $\theta$, holding $\phi = -\pi/8$, $\rho = \pi/4$. It tests the correlation between the $\theta$ magnitude (excitation energy proxy) and emission flux.
- `vary_phi_theta_fixed_rho_fixed.csv`: Sweeps $\phi$, holding $\theta = \pi$, $\rho = \pi/4$. It tests how the internal controller $\phi$ acts as a catalyst or barrier to emission.
- `vary_rho_theta_fixed_phi_fixed.csv`: Sweeps $\rho$, holding $\theta = \pi$, $\phi = -\pi/8$. It tests the correlation between the $\rho$ magnitude and emission flux.

### 2D Slices
These files track the emission flux while sweeping two parameters across $[-2\pi, 2\pi]$, evaluating all pairs:
- `theta_phi_rho_fixed.csv`: Sweeps $\theta$ and $\phi$. Shows the interplay of excitation energy ($\theta$) and the topological shedding catalyst ($\phi$).
- `theta_rho_phi_fixed.csv`: Sweeps $\theta$ and $\rho$. Shows how the two paired structural directions combined determine the total excitation energy available for shedding.
- `phi_rho_theta_fixed.csv`: Sweeps $\phi$ and $\rho$. Shows the interplay of excitation energy ($\rho$) and shedding catalyst ($\phi$).

### Trajectory
- `sample_packet_trajectory.csv`: Simulates a time-stepped outward progression of a shed wave-packet, capturing position and amplitude over time.

## 2. Interpretation of Data

### Emission Flux Dependence on $\theta$ and $\rho$
The 1D slices for $\theta$ and $\rho$, and their corresponding 2D slice (`theta_rho_phi_fixed.csv`), confirm that the total sheddable energy (and therefore the radiated flux) scales quadratically with the initial excitation state parameters ($\theta$ and $\rho$). The larger the deviation from the origin, the higher the stored gradient energy available for emission.

### Catalytic Role of $\phi$
The `vary_phi_theta_fixed_rho_fixed.csv` file demonstrates that $\phi$ controls the "stability" of the fold against emission. The emission flux peaks periodically when $\cos(2\phi) = 0$ (i.e., at singular sheets such as $\pm \pi/4, \pm 3\pi/4$). At these values, the internal geometric tension vanishes, allowing the structured spacetime fold to easily "pinch" off the excess energy. Away from these values, the fold is locked tightly, minimizing emission.

### Massless Propagation
`sample_packet_trajectory.csv` shows the wave-packet amplitude migrating radially outward at constant speed over time. Because this packet is constructed entirely from the $Q_{ang}$ angular fluctuations decoupled from the scale factor $\omega$, it represents the continuous outward flux of a massless gauge-like entity.

## 3. Conclusions
These simulated outputs provide the computational proof for the Topological Shedding claim: Khantraction folds shed discrete massless wave packets when transitioning between excited modes, and this shedding is topologically catalyzed by singular sheets controlled by $\phi$.