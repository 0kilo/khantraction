r"""
Phase D Neighborhood Stability Sweep
Date: 2026-03-29
Purpose: Executes a dense micro-perturbation grid around the 4 established 
angular anchors. Evaluates the invariant compactness ratio to determine if 
the objects form continuous trait gradients or discrete, stable species clusters.
"""

import numpy as np
import json
import os
import csv
import sympy as sp
import itertools

# --- Model Parameters & MC Constants ---
M_GLUE = 0.1
BETA_1, BETA_2, BETA_3 = 0.01, 0.02, 0.03

def load_and_lambdify_mc_forces():
    """Compiles the anisotropic MC gradients from Phase C."""
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
    
    m_p = 4 * np.pi * r**2 * rho_density
    damping = 2/r if r > 0 else 0
    
    w_pp = -damping * w_p - M_GLUE**2 * np.exp(w) + F_w
    th_pp = -damping * th_p + F_th
    ph_pp = -damping * ph_p + F_ph
    rh_pp = -damping * rh_p + F_rh
    
    return state + dr * np.array([w_p, th_p, ph_p, rh_p, w_pp, th_pp, ph_pp, rh_pp, m_p, 0])

def integrate_and_fingerprint(w0, th0, ph0, rh0, mc_funcs, r_max=20.0, dr=0.01):
    state = np.array([w0, th0, ph0, rh0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0])
    r_current = 1e-4
    history_m, history_r = [], []
    
    while r_current <= r_max:
        state = rk4_angular_step(r_current, state, dr, mc_funcs)
        r_current += dr
        history_m.append(state[8])
        history_r.append(r_current)
        if state[8] > r_current / 2: break
            
    final_mass = history_m[-1]
    half_mass = final_mass * 0.5
    half_radius = next((history_r[i] for i, m in enumerate(history_m) if m >= half_mass), None)
    
    compactness = final_mass / half_radius if half_radius else 0
    return final_mass, half_radius, compactness

if __name__ == "__main__":
    print("Initializing Phase D Neighborhood Stability Sweeps...")
    out_dir = "solutions/phase_d_neighborhood_stability"
    os.makedirs(out_dir, exist_ok=True)
    mc_funcs = load_and_lambdify_mc_forces()
    
    anchors = [
        {"name": "scalar", "th": 0.0, "ph": 0.0, "rh": 0.0},
        {"name": "theta_dom", "th": np.pi, "ph": 0.0, "rh": 0.0},
        {"name": "phi_dom", "th": 0.0, "ph": -np.pi/2, "rh": 0.0},
        {"name": "fully_mixed", "th": np.pi, "ph": -np.pi/2, "rh": np.pi/2}
    ]
    
    # Generate micro-perturbations: -0.2, 0.0, +0.2 radians
    perturbations = [-0.2, 0.0, 0.2]
    fixed_omega = 0.5
    
    for anchor in anchors:
        print(f"Sweeping 3D angular neighborhood around {anchor['name']}...")
        results = []
        
        # Grid of 3x3x3 = 27 local states per anchor
        grid = itertools.product(perturbations, perturbations, perturbations)
        
        for d_th, d_ph, d_rh in grid:
            th = anchor['th'] + d_th
            ph = anchor['ph'] + d_ph
            rh = anchor['rh'] + d_rh
            
            m_fin, r_half, comp = integrate_and_fingerprint(fixed_omega, th, ph, rh, mc_funcs)
            
            results.append({
                "d_theta": d_th, "d_phi": d_ph, "d_rho": d_rh,
                "abs_theta": th, "abs_phi": ph, "abs_rho": rh,
                "final_mass": m_fin, "half_radius": r_half, "compactness_ratio": comp
            })
            
        csv_path = os.path.join(out_dir, f"{anchor['name']}_neighborhood.csv")
        with open(csv_path, 'w', newline='') as f:
            writer = csv.DictWriter(f, fieldnames=["d_theta", "d_phi", "d_rho", "abs_theta", "abs_phi", "abs_rho", "final_mass", "half_radius", "compactness_ratio"])
            writer.writeheader()
            writer.writerows(results)
            
    print("Neighborhood sweeps complete. Data deposited.")