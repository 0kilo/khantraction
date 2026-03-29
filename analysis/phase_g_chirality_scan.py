# analysis/phase_g_chirality_scan.py

import numpy as np
import pandas as pd
import json
import os
import time

"""
Phase G: Classical Chirality Scan
Goal: Perform mirror-pair tests to determine if angular configurations
(theta, phi, rho) and (-theta, -phi, -rho) represent distinct chirality classes.
Derived from: derivations/derivation_82_classical_chirality_operators.md
"""

# Constants from Phase C and Derivation 80/82
GAMMA = 0.5
BETA = [0.01, 0.02, 0.03] # Anisotropy constants that break O(4) symmetry

def get_mc_vielbeins(omega, theta, phi, rho):
    """
    Calculates the left-invariant Maurer-Cartan vielbeins.
    Logic established in Derivation 78 and Phase C.
    """
    j1 = np.exp(omega) * np.sin(phi) * np.cos(theta)
    j2 = np.exp(omega) * np.cos(phi) * np.sin(rho)
    j3 = np.exp(omega) * np.cos(theta + rho)
    return np.array([j1, j2, j3])

def calculate_chirality_density(j_vec):
    """
    Computes the pseudoscalar chirality density chi.
    chi = epsilon_abc * J^a * J^b * J^c
    In this 1D radial approximation, we evaluate the product of 
    the distinct internal algebraic flows.
    """
    return j_vec[0] * j_vec[1] * j_vec[2]

def run_chirality_scan():
    start_time = time.time()
    os.makedirs('solutions/phase_g_rotational_handedness', exist_ok=True)
    
    # Domain constraints: theta, phi, rho in [-2pi, 2pi], omega > 0
    # Sampling key species anchors from Phase D
    omega_fixed = 0.5
    sample_points = 25
    angular_values = np.linspace(-2 * np.pi, 2 * np.pi, sample_points)
    
    results = []

    print(f"--- Starting Phase G Chirality Scan (Omega: {omega_fixed}) ---")
    print(f"Objective: Test Parity P: (ang) -> (-ang) for trait invariance and flow reversal.")

    for i, theta in enumerate(angular_values):
        for phi in angular_values[::2]: # Strided for efficiency
            for rho in angular_values[::2]:
                
                # Original State (Right-handed candidate)
                j_orig = get_mc_vielbeins(omega_fixed, theta, phi, rho)
                chi_orig = calculate_chirality_density(j_orig)
                # Hosting/Trait proxy (Mass/Compactness sensitivity)
                trait_orig = 1.0 / (1.0 + sum(BETA[k] * (j_orig[k]**2) for k in range(3)))
                
                # Parity-Flipped State (Left-handed candidate)
                # P: (theta, phi, rho) -> (-theta, -phi, -rho)
                j_flip = get_mc_vielbeins(omega_fixed, -theta, -phi, -rho)
                chi_flip = calculate_chirality_density(j_flip)
                trait_flip = 1.0 / (1.0 + sum(BETA[k] * (j_flip[k]**2) for k in range(3)))
                
                # Determine Identity
                is_mirror_pair = np.isclose(trait_orig, trait_flip, atol=1e-7)
                sign_flip = not np.isclose(chi_orig, chi_flip, atol=1e-7) and np.isclose(chi_orig, -chi_flip, atol=1e-7)
                
                results.append({
                    'theta': theta,
                    'phi': phi,
                    'rho': rho,
                    'chi_orig': chi_orig,
                    'chi_flip': chi_flip,
                    'trait_val': trait_orig,
                    'trait_delta': abs(trait_orig - trait_flip),
                    'is_mirror': is_mirror_pair,
                    'sign_reversal': sign_flip
                })
        
        if (i + 1) % 5 == 0:
            print(f"  Progress: {((i+1)/sample_points)*100:.0f}% Complete. Points processed: {len(results)}")

    # Finalizing data
    df = pd.DataFrame(results)
    output_path = 'solutions/phase_g_rotational_handedness/chirality_comparison_results.csv'
    df.to_csv(output_path, index=False)
    
    # Identify A-Chiral vs Chiral Classes
    achiral_count = df[df['chi_orig'].abs() < 1e-8].shape[0]
    chiral_pairs = df[(df['is_mirror'] == True) & (df['sign_reversal'] == True)].shape[0]
    
    summary = {
        'status': 'complete',
        'total_points': len(results),
        'achiral_samples': achiral_count,
        'validated_chiral_pairs': chiral_pairs,
        'max_trait_divergence': df['trait_delta'].max(),
        'execution_time': time.time() - start_time
    }
    
    with open('solutions/phase_g_rotational_handedness/handedness_fingerprints.json', 'w') as f:
        json.dump(summary, f, indent=4)

    print(f"\nScan Complete. Validated {chiral_pairs} mirror-symmetric pairs.")
    print(f"Results saved to {output_path}")

if __name__ == "__main__":
    run_chirality_scan()