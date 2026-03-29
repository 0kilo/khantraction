# analysis/phase_h_mode_ladder_scan.py

import numpy as np
import pandas as pd
import json
import os
from scipy.integrate import quad
from scipy.optimize import root_scalar

"""
Phase H: Mode Ladder Scan
Goal: Identify discrete energy eigenvalues (mode ladders) within the Khantraction hosting basins.
Derived from: 
 - derivations/derivation_84_quantum_excitation_ansatz.md
 - derivations/derivation_85_discrete_spectrum_conditions.md
"""

# Constants from previous phases and derivations
OMEGA_SCALE = 0.5  # Fixed scale from Phase F
MAX_HOSTING = 0.99935  # Peak sensitivity from Phase F
LAMBDA_CHIRALITY = 0.05 # Coupling strength constant defined in Derivation 84

def effective_potential(r, chi):
    """
    Defines the radial potential well V_eff(r).
    Combines the hosting basin depth with the chirality-induced energy shift.
    """
    # Simple potential well model: 
    # Core (r < 1) has depth based on hosting sensitivity and chirality
    # Exterior (r > 1) returns to vacuum energy
    base_depth = MAX_HOSTING * (1.0 / (1.0 + r**2))
    chirality_shift = LAMBDA_CHIRALITY * chi
    return base_depth + chirality_shift

def quantization_integral(E, chi, r_h):
    """
    The Bohr-Sommerfeld quantization condition from Derivation 85:
    Integral of sqrt(E^2 - V_eff) dr = (n + 1/2) * pi
    """
    def integrand(r):
        v = effective_potential(r, chi)
        if E**2 > v:
            return np.sqrt(E**2 - v)
        return 0
    
    val, _ = quad(integrand, 0, r_h)
    return val

def find_eigenvalues(chi, max_n=3):
    """
    Searches for discrete energy levels En for a given topological species (chi).
    """
    r_h = 2.0  # Radius of the hosting basin
    eigenvalues = []
    
    # Search range for E (must be below the potential barrier for bound states)
    # Based on Derivation 85
    v_max = MAX_HOSTING + abs(LAMBDA_CHIRALITY * chi)
    
    for n in range(max_n):
        target = (n + 0.5) * np.pi
        
        def objective(E):
            return quantization_integral(E, chi, r_h) - target
        
        try:
            # Solve for E where the quantization condition is met
            sol = root_scalar(objective, bracket=[0.1, np.sqrt(v_max)], method='brentq')
            eigenvalues.append({
                'n': n,
                'energy': sol.root,
                'type': 'bound_state'
            })
        except ValueError:
            # No bound state found for this n
            continue
            
    return eigenvalues

def run_mode_ladder_scan():
    print("--- Starting Phase H: Quantum Mode Ladder Scan ---")
    os.makedirs('solutions/phase_h_quantum_results', exist_ok=True)
    
    # Load chirality data from Phase G to select representative species
    # We test: A-Chiral (chi=0), Right-Handed (chi>0), Left-Handed (chi<0)
    test_species = [
        {'name': 'Scalar_A-Chiral', 'chi': 0.0},
        {'name': 'Right-Handed_Enantiomer', 'chi': 0.85},
        {'name': 'Left-Handed_Enantiomer', 'chi': -0.85}
    ]
    
    full_spectrum = {}
    
    for species in test_species:
        print(f"Analyzing Species: {species['name']} (chi={species['chi']})")
        modes = find_eigenvalues(species['chi'])
        full_spectrum[species['name']] = {
            'chirality': species['chi'],
            'modes': modes,
            'mode_count': len(modes)
        }
    
    # Save results
    output_path = 'solutions/phase_h_quantum_results/excitation_spectrum.json'
    with open(output_path, 'w') as f:
        json.dump(full_spectrum, f, indent=4)
        
    print(f"\nScan Complete. Discrete spectra identified for {len(test_species)} species.")
    print(f"Results saved to {output_path}")

if __name__ == "__main__":
    run_mode_ladder_scan()