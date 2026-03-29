r"""
Phase E Metric Curve Fitting (Corrected)
Date: 2026-03-29
Purpose: Performs precision numerical regression on asymptotic tails. 
Fixed: Typo in scipy import and IndexError in tail masking.
"""

import os
import csv
import json
import numpy as np
from scipy.optimize import curve_fit

def rn_mass_model(r, M_adm, Q_eff_sq):
    """Reissner-Nordstrom mass function: M(r) = M - Q^2/(2r)"""
    return M_adm - Q_eff_sq / (2 * r)

def fit_species_tail(filepath):
    r_data, m_data = [], []
    with open(filepath, 'r') as f:
        reader = csv.DictReader(f)
        for row in reader:
            r_data.append(float(row['r']))
            m_data.append(float(row['mass_m']))
    
    r_data = np.array(r_data)
    m_data = np.array(m_data)
    
    # Robust tail selection: Use the last 50% of the available data 
    # to ensure the array is never empty regardless of r_max.
    n_points = len(r_data)
    if n_points < 2:
        return {"error": "Insufficient data points in tail file."}
        
    start_idx = n_points // 2
    r_fit = r_data[start_idx:]
    m_fit = m_data[start_idx:]
    
    try:
        # Initial guess: Final mass and zero charge
        popt, pcov = curve_fit(rn_mass_model, r_fit, m_fit, p0=[m_fit[-1], 0.0])
        
        return {
            "M_adm": float(popt[0]),
            "Q_eff_sq": float(popt[1]),
            "Q_eff": float(np.sqrt(abs(popt[1]))) if popt[1] > 0 else 0.0,
            "fit_success": True
        }
    except Exception as e:
        return {"error": str(e), "fit_success": False}

if __name__ == "__main__":
    print("Initializing Phase E Metric Curve Fitting...")
    data_dir = "solutions/phase_e_asymptotic_extraction"
    out_dir = "solutions/phase_e_metric_curve_fitting"
    os.makedirs(out_dir, exist_ok=True)
    
    results = {}
    for file in os.listdir(data_dir):
        if file.endswith("_asymptotic_tail.csv"):
            species_name = file.replace("_asymptotic_tail.csv", "")
            print(f"Fitting Reissner-Nordstrom profile for {species_name}...")
            fit_results = fit_species_tail(os.path.join(data_dir, file))
            results[species_name] = fit_results
            
    out_path = os.path.join(out_dir, "external_phenomenology_summary.json")
    with open(out_path, 'w') as f:
        json.dump(results, f, indent=4)
        
    print(f"Curve fitting complete. Results deposited in {out_path}")