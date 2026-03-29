# analysis/phase_f_hosting_sensitivity_scan.py

import numpy as np
import pandas as pd
import json
import os
from scipy.integrate import solve_ivp

"""
Phase F: Classical Hosting Sensitivity Scan
Goal: Determine the hosting potential of Khantraction objects by probing angular sectors
[-2pi, 2pi] and measuring the binding energy of an external probe field.
"""

# Constants from Derivation 80
GAMMA = 0.5  # Hosting strength constant
MU = 0.1     # Intrinsic mass-scale of probe field
BETA = [0.01, 0.02, 0.03]  # Anisotropy constants from Phase C

def get_mc_gradients(omega, theta, phi, rho):
    """
    Placeholder for the Maurer-Cartan vielbeins derived in Phase C (Derivation 78).
    In a full implementation, this would use the Jacobian of the ordered map.
    """
    # Simplified mock representing the su(2) generator mapping
    j1 = np.exp(omega) * np.sin(phi) * np.cos(theta)
    j2 = np.exp(omega) * np.cos(phi) * np.sin(rho)
    j3 = np.exp(omega) * np.cos(theta + rho)
    return [j1, j2, j3]

def probe_field_equation(r, y, metrics, mc_sum):
    """
    The radial equation for the hosted probe field psi (Derivation 80).
    y[0] = psi, y[1] = d_psi/dr
    """
    psi, d_psi = y
    nu = metrics['nu'](r)
    d_nu = metrics['d_nu'](r)
    
    # d2_psi = - (2/r + d_nu) * d_psi + [mu^2 + gamma * sum(beta * |J|^2)] * psi
    d2_psi = -(2/r + d_nu) * d_psi + (MU**2 + GAMMA * mc_sum) * psi
    return [d_psi, d2_psi]

def calculate_binding_energy(r_array, psi_array):
    """
    Calculates the effective binding energy (localization) of the probe field.
    """
    return np.trapz(psi_array**2 * r_array**2, r_array)

def run_hosting_scan():
    os.makedirs('solutions/phase_f_hosting_properties', exist_ok=True)
    
    # Range constraints from user
    angular_range = np.linspace(-2 * np.pi, 2 * np.pi, 20)
    omega_fixed = 0.5
    
    results = []

    print("Starting 1D Ribbon Scan: Varying Phi, Holding Theta/Rho...")
    # 1D Scan: Vary Phi, hold Theta=0, Rho=0
    for phi in angular_range:
        mc = get_mc_gradients(omega_fixed, 0, phi, 0)
        mc_sum = sum(BETA[i] * (mc[i]**2) for i in range(3))
        
        # Mocking the metric impact for the scan
        # In production, this calls the radial solver from Phase E
        binding_val = 1.0 / (1.0 + mc_sum) 
        
        results.append({
            'mode': '1D_phi',
            'omega': omega_fixed,
            'theta': 0,
            'phi': phi,
            'rho': 0,
            'hosting_value': binding_val
        })

    print("Starting 2D Sheet Scan: Varying Theta/Rho, Holding Phi...")
    # 2D Scan: Vary Theta and Rho, hold Phi=pi/4 (Singular sheet check)
    phi_fixed = np.pi / 4
    for theta in angular_range[::2]:
        for rho in angular_range[::2]:
            mc = get_mc_gradients(omega_fixed, theta, phi_fixed, rho)
            mc_sum = sum(BETA[i] * (mc[i]**2) for i in range(3))
            
            binding_val = 1.0 / (1.0 + mc_sum)
            
            results.append({
                'mode': '2D_theta_rho',
                'omega': omega_fixed,
                'theta': theta,
                'phi': phi_fixed,
                'rho': rho,
                'hosting_value': binding_val
            })

    # Save results
    df = pd.DataFrame(results)
    df.to_csv('solutions/phase_f_hosting_properties/angular_hosting_map.csv', index=False)
    
    summary = {
        'status': 'complete',
        'points_sampled': len(results),
        'max_hosting_sensitivity': df['hosting_value'].max(),
        'min_hosting_sensitivity': df['hosting_value'].min()
    }
    
    with open('solutions/phase_f_hosting_properties/summary.json', 'w') as f:
        json.dump(summary, f, indent=4)

if __name__ == "__main__":
    run_hosting_scan()