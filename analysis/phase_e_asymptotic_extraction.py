r"""
Phase E Asymptotic Extraction (Robust Logging)
Date: 2026-03-29
Purpose: Fixed floating-point modulo error to ensure data points are 
actually written to the CSV files for Phase E curve fitting.
"""

import numpy as np
import os
import csv
import sympy as sp

# --- Model Parameters & MC Constants ---
KAPPA = 8 * np.pi
XI = 0.0001      # Reduced from 0.002 to slow mass growth
M_GLUE = 0.01    # Reduced from 0.1 to thin the core
LAMBDA_Q = 0.001
BETA_1, BETA_2, BETA_3 = 0.01, 0.02, 0.03

def load_and_lambdify_mc_forces():
    omega, theta, phi, rho = sp.symbols('omega theta phi rho', real=True)
    b1, b2, b3 = sp.symbols('b1 b2 b3', real=True)
    w_i = sp.cos(2*phi)
    w_j = -sp.sin(2*phi)*sp.sin(2*rho)
    w_k = 1 + sp.sin(2*phi)*sp.cos(2*rho)
    L_MC = b1 * w_i**2 + b2 * w_j**2 + b3 * w_k**2
    forces = [sp.diff(L_MC, var) for var in [omega, theta, phi, rho]]
    lambdas = []
    for f in forces:
        f_sub = f.subs({b1: BETA_1, b2: BETA_2, b3: BETA_3})
        func = sp.lambdify((omega, theta, phi, rho), f_sub, "numpy")
        lambdas.append(func)
    return lambdas

def rk4_angular_step(r, state, dr, mc_funcs):
    w, th, ph, rh, w_p, th_p, ph_p, rh_p, m, metric_phi = state
    F_w = mc_funcs[0](w, th, ph, rh)
    F_th = mc_funcs[1](w, th, ph, rh)
    F_ph = mc_funcs[2](w, th, ph, rh)
    F_rh = mc_funcs[3](w, th, ph, rh)
    q_norm_sq = np.exp(2 * w)
    e_2lambda = (1 - 2*m/r)**(-1) if (r > 2*m and r > 0) else 1.0
    rho_density = 0.5 * (w_p**2 + th_p**2 + ph_p**2 + rh_p**2)/e_2lambda + 0.5*M_GLUE**2*q_norm_sq
    rho_density += (BETA_1 + BETA_2 + BETA_3) * 0.001 
    p_r = 0.5 * (w_p**2 + th_p**2 + ph_p**2 + rh_p**2)/e_2lambda - 0.5*M_GLUE**2*q_norm_sq
    m_p = 4 * np.pi * r**2 * rho_density
    metric_phi_p = (m + 4 * np.pi * r**3 * p_r) / (r * (r - 2*m)) if (r > 2*m and r > 0) else 0
    damping = 2/r if r > 0 else 0
    w_pp = -damping * w_p - M_GLUE**2 * np.exp(w) + F_w
    th_pp = -damping * th_p + F_th
    ph_pp = -damping * ph_p + F_ph
    rh_pp = -damping * rh_p + F_rh
    return state + dr * np.array([w_p, th_p, ph_p, rh_p, w_pp, th_pp, ph_pp, rh_pp, m_p, metric_phi_p])

def extract_asymptotic_tail(seed, mc_funcs, r_max=100.0, dr=0.01, tail_start=15.0):
    w0, th0, ph0, rh0 = seed['omega'], seed['theta'], seed['phi'], seed['rho']
    state = np.array([w0, th0, ph0, rh0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0])
    
    r_current = 1e-4
    tail_data = []
    step_count = 0 
    
    while r_current <= r_max:
        state = rk4_angular_step(r_current, state, dr, mc_funcs)
        r_current += dr
        step_count += 1
        
        # Log data starting at r=15.0
        if r_current >= tail_start:
            if step_count % 10 == 0:
                tail_data.append({
                    "r": round(r_current, 3), "omega": state[0],
                    "mass_m": state[8], "metric_phi": state[9]
                })
        
        if state[8] > r_current / 2:
            break
            
    return tail_data

if __name__ == "__main__":
    print("Initializing Phase E Stability Overhaul...")
    out_dir = "solutions/phase_e_asymptotic_extraction"
    os.makedirs(out_dir, exist_ok=True)
    mc_funcs = load_and_lambdify_mc_forces()
    
    # EXTREME SCALE REDUCTION
    w_fixed = 0.001 
    
    anchors = [
        {"name": "scalar", "omega": w_fixed, "theta": 0.0, "phi": 0.0, "rho": 0.0},
        {"name": "theta_dom", "omega": w_fixed, "theta": np.pi, "phi": 0.0, "rho": 0.0},
        {"name": "phi_dom", "omega": w_fixed, "theta": 0.0, "phi": -np.pi/2, "rho": 0.0},
        {"name": "fully_mixed", "omega": w_fixed, "theta": np.pi, "phi": -np.pi/2, "rho": np.pi/2}
    ]
    
    for anchor in anchors:
        print(f"Integrating {anchor['name']} (Scale: {w_fixed}) out to r=100.0...")
        tail_data = extract_asymptotic_tail(anchor, mc_funcs)
        
        csv_path = os.path.join(out_dir, f"{anchor['name']}_asymptotic_tail.csv")
        with open(csv_path, 'w', newline='') as f:
            writer = csv.DictWriter(f, fieldnames=["r", "omega", "mass_m", "metric_phi"])
            writer.writeheader()
            writer.writerows(tail_data)
            
    print(f"Deep integration complete. Check CSVs in {out_dir}/ for data rows.")