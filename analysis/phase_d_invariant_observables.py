r"""
Phase D Scale-Invariant Fingerprinting
Date: 2026-03-29
Purpose: Executes an \omega (scale) sweep across the Phase C angular anchors 
using the exact Maurer-Cartan radial solver. Extracts the mass, half-radius, 
and their invariant compactness ratio to establish classical species fingerprints.
"""

import numpy as np
import json
import os
import csv
import sympy as sp

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
    rho_density += (BETA_1 + BETA_2 + BETA_3) * 0.001 # MC penalty placeholder
    
    m_p = 4 * np.pi * r**2 * rho_density
    damping = 2/r if r > 0 else 0
    
    w_pp = -damping * w_p - M_GLUE**2 * np.exp(w) + F_w
    th_pp = -damping * th_p + F_th
    ph_pp = -damping * ph_p + F_ph
    rh_pp = -damping * rh_p + F_rh
    
    return state + dr * np.array([w_p, th_p, ph_p, rh_p, w_pp, th_pp, ph_pp, rh_pp, m_p, 0])

def integrate_and_fingerprint(seed, mc_funcs, r_max=20.0, dr=0.01):
    w0, th0, ph0, rh0 = seed['omega'], seed['theta'], seed['phi'], seed['rho']
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
    
    # The Core Phase D Observable
    compactness = final_mass / half_radius if half_radius else 0
    
    return {
        "omega": w0,
        "final_mass": final_mass,
        "half_radius": half_radius,
        "compactness_ratio": compactness
    }

if __name__ == "__main__":
    print("Initializing Phase D Scale-Invariant Fingerprinting...")
    os.makedirs("solutions/phase_d_invariant_observables", exist_ok=True)
    mc_funcs = load_and_lambdify_mc_forces()
    
    anchors = [
        {"name": "scalar", "th": 0.0, "ph": 0.0, "rh": 0.0},
        {"name": "theta_dom", "th": np.pi, "ph": 0.0, "rh": 0.0},
        {"name": "phi_dom", "th": 0.0, "ph": -np.pi/2, "rh": 0.0},
        {"name": "fully_mixed", "th": np.pi, "ph": -np.pi/2, "rh": np.pi/2}
    ]
    
    omega_sweep = np.linspace(0.1, 1.0, 10) # Sweep scale from small to large
    
    for anchor in anchors:
        print(f"Sweeping omega for {anchor['name']} species...")
        results = []
        for w in omega_sweep:
            seed = {"id": f"{anchor['name']}_w{w:.1f}", "omega": w, "theta": anchor['th'], "phi": anchor['ph'], "rho": anchor['rh']}
            res = integrate_and_fingerprint(seed, mc_funcs)
            results.append(res)
            
        csv_path = f"solutions/phase_d_invariant_observables/{anchor['name']}_omega_sweep.csv"
        with open(csv_path, 'w', newline='') as f:
            writer = csv.DictWriter(f, fieldnames=["omega", "final_mass", "half_radius", "compactness_ratio"])
            writer.writeheader()
            writer.writerows(results)
            
    print("Sweep complete. Species fingerprints extracted.")