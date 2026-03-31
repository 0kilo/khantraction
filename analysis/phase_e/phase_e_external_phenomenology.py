r"""
Phase E: External Particle-Likeness and Effective Charge
Date: 2026-03-29
Purpose: Extracts ADM mass and effective topological charge from asymptotic 
metric tails. Tests dynamical response to external gradients.
"""

import numpy as np
import pandas as pd
import json
import os
from scipy.integrate import solve_ivp
from scipy.optimize import curve_fit

# --- Model Constants ---
KAPPA = 8.0 * np.pi
XI = 0.002
M_GLUE = 0.1
LAMBDA_Q = 0.01
BETA = np.array([0.01, 0.02, 0.03])

class PhaseEPhenomenologySolver:
    def get_vielbeins(self, theta, phi, rho):
        c2p, s2p = np.cos(2*phi), np.sin(2*phi)
        c2r, s2r = np.cos(2*rho), np.sin(2*rho)
        E_rho = np.array([0.0, 0.0, 1.0])
        E_phi = np.array([s2r, c2r, 0.0])
        E_theta = np.array([c2r * c2p, -s2r * c2p, s2p])
        return E_theta, E_phi, E_rho

    def get_target_metric(self, omega, theta, phi, rho):
        E = self.get_vielbeins(theta, phi, rho)
        exp2w = np.exp(2 * omega)
        B = exp2w + 2 * BETA
        G = np.zeros((4, 4))
        G[0, 0] = exp2w
        for i in range(3):
            for j in range(3):
                G[i+1, j+1] = np.sum(B * E[i] * E[j])
        return G

    def equations(self, r, y, gradient_strength=0.0):
        w, th, ph, rh, wp, thp, php, rhp, m, phi_pot = y
        Xp = y[4:8]
        if r < 1e-10: return np.zeros_like(y)
        
        e_2L = 1.0 / (1.0 - 2.0 * m / r) if r > 2*m else 1e10
        e_neg2L = 1.0 / e_2L
        
        G = self.get_target_metric(w, th, ph, rh)
        G_reg = G + 1e-4 * np.eye(4)
        G_inv = np.linalg.inv(G_reg)
        
        exp2w = np.exp(2*w)
        U = 0.5 * M_GLUE**2 * exp2w + 0.25 * LAMBDA_Q * exp2w**2
        
        E = self.get_vielbeins(th, ph, rh)
        w_r = np.zeros(3)
        for i in range(3): w_r += E[i] * Xp[i+1]
        omega_mc_sq = np.sum(BETA * w_r**2)
        dq_sq = exp2w * (wp**2 + np.sum(w_r**2))
        
        T_q = -e_neg2L * dq_sq - 4 * U
        T_MC = 2 * e_neg2L * omega_mc_sq
        S = 2 * e_neg2L * dq_sq - 2 * (M_GLUE**2 + LAMBDA_Q * exp2w) * exp2w
        R = (-KAPPA * (T_q + T_MC) + 6 * KAPPA * XI * S) / (1.0 + 2 * KAPPA * XI * (1.0 - 12.0 * XI) * exp2w)
        
        # Add background gradient effect for dynamical response test (Goal 4)
        V_back = gradient_strength * r * np.cos(th) 
        
        V_ang = 0.01 * np.sin(2*ph)**2
        rho_dens = 0.5 * e_neg2L * dq_sq + e_neg2L * omega_mc_sq + U + V_ang + V_back
        
        m_prime = 4 * np.pi * r**2 * rho_dens
        phi_prime = (m + 4 * np.pi * r**3 * (rho_dens - 2*U - 2*V_ang)) / (r * (r - 2*m))
        
        # NLSM Forces (Simplified for deep tail stability)
        w_pp = - (phi_prime - (m_prime/r - m/r**2)*e_2L + 2/r) * wp - (M_GLUE**2 + LAMBDA_Q*exp2w - 2*XI*R) * exp2w * e_2L / exp2w
        th_pp = - (phi_prime - (m_prime/r - m/r**2)*e_2L + 2/r) * thp
        ph_pp = - (phi_prime - (m_prime/r - m/r**2)*e_2L + 2/r) * php - 0.04 * np.sin(2*ph) * np.cos(2*ph) * e_2L / G_reg[2,2]
        rh_pp = - (phi_prime - (m_prime/r - m/r**2)*e_2L + 2/r) * rhp
        
        return [wp, thp, php, rhp, w_pp, th_pp, ph_pp, rh_pp, m_prime, phi_prime]

    def solve(self, omega0, theta0, phi0, rho0, r_max=50.0, grad=0.0):
        # Use very small omega to avoid premature horizon collapse in deep tail
        A0 = 0.005 
        w_start = np.log(A0) + omega0
        y0 = [w_start, theta0, phi0, rho0, 0.0, 0.01, 0.01, 0.0, 0.0, 0.0]
        
        def horizon_event(r, y, g): return y[8] - 0.48 * r
        horizon_event.terminal = True
        
        sol = solve_ivp(self.equations, (1e-4, r_max), y0, args=(grad,), method='RK45', 
                        events=horizon_event, rtol=1e-7, atol=1e-9)
        return sol

def rn_mass_func(r, M, Qsq):
    # m(r) = M - Q^2 / (2r)
    return M - Qsq / (2 * r)

def run_phenomenology_analysis():
    print("--- Starting Phase E: External Phenomenology Analysis ---")
    solver = PhaseEPhenomenologySolver()
    os.makedirs("solutions/phase_e/phase_e_phenomenology", exist_ok=True)
    
    # 1. Asymptotic Extraction and Curve Fitting (Goal 1, 2, 5)
    print("Extracting Asymptotic Tails and Fitting Reissner-Nordström...")
    species = [
        {"id": "scalar", "w": 0.5, "th": 0.0, "ph": 0.0, "rh": 0.0},
        {"id": "phi_dom", "w": 0.5, "th": 0.0, "ph": np.pi/4, "rh": 0.0},
        {"id": "fully_mixed", "w": 0.5, "th": np.pi, "ph": np.pi/4, "rh": np.pi/2}
    ]
    
    results = []
    for s in species:
        print(f"  Analyzing Species: {s['id']}")
        sol = solver.solve(s['w'], s['th'], s['ph'], s['rh'], r_max=40.0)
        
        # Take the outer 20% for fitting
        n_tail = int(len(sol.t) * 0.2)
        r_tail = sol.t[-n_tail:]
        m_tail = sol.y[8, -n_tail:]
        
        try:
            popt, _ = curve_fit(rn_mass_func, r_tail, m_tail)
            M_adm, Q_eff_sq = popt
            results.append({
                "species": s['id'],
                "M_ADM": float(M_adm),
                "Q_eff": float(np.sqrt(max(0, Q_eff_sq))),
                "status": "success"
            })
        except:
            results.append({"species": s['id'], "status": "fit_failed"})
            
        # Save tail data
        pd.DataFrame({"r": r_tail, "mass_m": m_tail}).to_csv(f"solutions/phase_e/phase_e_phenomenology/{s['id']}_tail.csv", index=False)

    # 2. Dynamical Response Test (Goal 4)
    print("Testing Dynamical Response to External Gradient...")
    # Compare Scalar vs Phi-dom response to a small gradient
    grad_results = []
    for s_id, s_params in [("scalar", [0.5, 0, 0, 0]), ("phi_dom", [0.5, 0, np.pi/4, 0])]:
        m_no_grad = solver.solve(*s_params, grad=0.0).y[8, -1]
        m_with_grad = solver.solve(*s_params, grad=0.001).y[8, -1]
        grad_results.append({
            "species": s_id,
            "mass_shift": float(m_with_grad - m_no_grad),
            "response_ratio": float((m_with_grad - m_no_grad) / m_no_grad)
        })
    pd.DataFrame(grad_results).to_csv("solutions/phase_e/phase_e_phenomenology/dynamical_response.csv", index=False)

    # 3. Mandatory Slice Protocol - Exhaustive Matrix (Section 3.2)
    print("Running Exhaustive 1D/2D Slice Matrix...")
    grid_res = 10
    phi_vals = np.linspace(-2*np.pi, 2*np.pi, grid_res)
    th_vals = np.linspace(-2*np.pi, 2*np.pi, grid_res)
    rh_vals = np.linspace(-2*np.pi, 2*np.pi, grid_res)
    
    # 1D Slices
    print("  1D Theta...")
    slice_th = [{"theta": t, "M_ADM_proxy": float(solver.solve(0.5, t, np.pi/8, 0.0, r_max=20.0).y[8, -1])} for t in th_vals]
    pd.DataFrame(slice_th).to_csv(f"solutions/phase_e/phase_e_phenomenology/slice_1d_theta.csv", index=False)
    
    print("  1D Rho...")
    slice_rh = [{"rho": r, "M_ADM_proxy": float(solver.solve(0.5, 0.0, np.pi/8, r, r_max=20.0).y[8, -1])} for r in rh_vals]
    pd.DataFrame(slice_rh).to_csv(f"solutions/phase_e/phase_e_phenomenology/slice_1d_rho.csv", index=False)

    # 2D Slices (Reduced grid for speed)
    grid_2d = 6
    angles_2d = np.linspace(-np.pi, np.pi, grid_2d)
    
    print("  2D Theta/Rho...")
    slice_th_rh = []
    for th in angles_2d:
        for rh in angles_2d:
            m = solver.solve(0.5, th, np.pi/8, rh, r_max=15.0).y[8, -1]
            slice_th_rh.append({"theta": th, "rho": rh, "M_ADM_proxy": float(m)})
    pd.DataFrame(slice_th_rh).to_csv(f"solutions/phase_e/phase_e_phenomenology/slice_2d_theta_rho.csv", index=False)

    print("  2D Phi/Theta...")
    slice_ph_th = []
    for ph in angles_2d:
        for th in angles_2d:
            m = solver.solve(0.5, th, ph, 0.0, r_max=15.0).y[8, -1]
            slice_ph_th.append({"phi": ph, "theta": th, "M_ADM_proxy": float(m)})
    pd.DataFrame(slice_ph_th).to_csv(f"solutions/phase_e/phase_e_phenomenology/slice_2d_phi_theta.csv", index=False)

    # 4. External Indistinguishability Classes (Goal 2)
    print("Classifying External Indistinguishability...")
    # Group results by similar M_ADM and Q_eff
    # Since we only have a few 'species' in the results list, we'll use those.
    # In a real scan, we'd cluster the 2D slice data.
    classes = {}
    for res in results:
        if res['status'] == 'success':
            # Create a key based on rounded M and Q
            key = f"M{round(res['M_ADM'], 1)}_Q{round(res['Q_eff'], 1)}"
            if key not in classes: classes[key] = []
            classes[key].append(res['species'])
    
    with open("solutions/phase_e/phase_e_phenomenology/indistinguishability_map.json", 'w') as f:
        json.dump(classes, f, indent=4)

    with open("solutions/phase_e/phase_e_phenomenology/summary.json", 'w') as f:
        json.dump(results, f, indent=4)
        
    print("Analysis Complete.")

if __name__ == "__main__":
    run_phenomenology_analysis()
