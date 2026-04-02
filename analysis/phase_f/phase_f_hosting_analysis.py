r"""
Phase F: Classical Hosting and Signed Loading Analysis
Date: 2026-03-29
Purpose: Implements the radial probe field equation derived in Derivation 80.
Tests the ability of Khantraction objects to host content and compares 
opposite signed induced loadings.
"""

import numpy as np
import pandas as pd
import json
import os
from scipy.integrate import solve_ivp

# --- Model Constants ---
KAPPA = 8.0 * np.pi
XI = 0.002
M_GLUE = 0.1
LAMBDA_Q = 0.01
BETA = np.array([0.01, 0.02, 0.03])
MU_PROBE = 0.05 # Mass of the probe field
GAMMA_HOST = 0.1 # Hosting coupling strength

class PhaseFHostingSolver:
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

    def equations(self, r, y, J_ext=0.0):
        # y = [w, th, ph, rh, wp, thp, php, rhp, m, phi_pot, psi, psip]
        w, th, ph, rh, wp, thp, php, rhp, m, phi_pot, psi, psip = y
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
        
        # Probe field density and pressure
        # L_int = -0.5 * GAMMA * omega_mc_sq * psi^2
        rho_psi = 0.5 * e_neg2L * psip**2 + 0.5 * MU_PROBE**2 * psi**2 + 0.5 * GAMMA_HOST * omega_mc_sq * psi**2
        p_r_psi = 0.5 * e_neg2L * psip**2 - 0.5 * MU_PROBE**2 * psi**2 - 0.5 * GAMMA_HOST * omega_mc_sq * psi**2
        
        # Local interaction term for signed loading (Goal 2)
        # Couple psi to the local scale derivative wp
        rho_psi += J_ext * wp * psi 
        
        rho_total = 0.5 * e_neg2L * dq_sq + e_neg2L * omega_mc_sq + U + rho_psi
        
        m_prime = 4 * np.pi * r**2 * rho_total
        phi_prime = (m + 4 * np.pi * r**3 * p_r_psi) / (r * (r - 2*m)) # Simplified p_r
        
        L_prime = (m_prime / r - m / r**2) / (1 - 2*m/r)
        H_prime = phi_prime - L_prime + 2/r
        
        # NLSM Matter Equations (Simplified)
        w_pp = - H_prime * wp - M_GLUE**2 * exp2w * e_2L / exp2w
        th_pp = - H_prime * thp
        ph_pp = - H_prime * php - 0.04 * np.sin(2*ph) * np.cos(2*ph) * e_2L / G_reg[2,2]
        rh_pp = - H_prime * rhp
        
        # Probe field equation (Derivation 80)
        # psi'' + H' psi' - e^2L [mu^2 + gamma Omega_MC^2] psi = 0
        psi_pp = - H_prime * psip + e_2L * (MU_PROBE**2 + GAMMA_HOST * omega_mc_sq) * psi - J_ext * wp * e_2L
        
        return [wp, thp, php, rhp, w_pp, th_pp, ph_pp, rh_pp, m_prime, phi_prime, psip, psi_pp]

    def solve(self, omega0, theta0, phi0, rho0, J_ext=0.0, r_max=20.0):
        A0 = 0.02
        w_start = np.log(A0) + omega0
        # Initial psi at core
        psi0 = 0.1
        y0 = [w_start, theta0, phi0, rho0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, psi0, 0.0]
        
        def horizon_event(r, y, j): return y[8] - 0.48 * r
        horizon_event.terminal = True
        
        sol = solve_ivp(self.equations, (1e-4, r_max), y0, args=(J_ext,), method='RK45', 
                        events=horizon_event, rtol=1e-6)
        return sol

def run_hosting_analysis():
    print("--- Starting Phase F: Verified Hosting and Signed Loading Analysis ---")
    solver = PhaseFHostingSolver()
    os.makedirs("solutions/phase_f/phase_f_hosting", exist_ok=True)
    
    # 1. Signed Loading Test (Goal 2)
    print("Testing Signed Loading (J_ext = +/- 0.01)...")
    loading_results = []
    for j in [-0.01, 0.0, 0.01]:
        sol = solver.solve(0.5, 0.0, np.pi/4, 0.0, J_ext=j)
        m_final = sol.y[8, -1]
        psi_final = sol.y[10, -1]
        loading_results.append({
            "J_ext": j, "final_mass": float(m_final), "psi_core_residual": float(psi_final)
        })
    pd.DataFrame(loading_results).to_csv("solutions/phase_f/phase_f_hosting/signed_loading_test.csv", index=False)

    # 2. Hosting Basin Identification - Exhaustive Matrix (Goal 3 & 4)
    print("Running Exhaustive 1D/2D Hosting Sensitivity Matrix...")
    grid_res = 10
    psi_init = 0.1
    
    # 1D Slices
    print("  1D Theta...")
    slice_th = [{"theta": t, "hosting_efficiency": float(1.0 - (solver.solve(0.5, t, np.pi/8, 0.0).y[10, -1] / psi_init))} for t in np.linspace(-2*np.pi, 2*np.pi, grid_res)]
    pd.DataFrame(slice_th).to_csv("solutions/phase_f/phase_f_hosting/slice_1d_theta.csv", index=False)
    
    print("  1D Rho...")
    slice_rh = [{"rho": r, "hosting_efficiency": float(1.0 - (solver.solve(0.5, 0.0, np.pi/8, r).y[10, -1] / psi_init))} for r in np.linspace(-2*np.pi, 2*np.pi, grid_res)]
    pd.DataFrame(slice_rh).to_csv("solutions/phase_f/phase_f_hosting/slice_1d_rho.csv", index=False)

    print("  1D Phi...")
    slice_ph = [{"phi": p, "hosting_efficiency": float(1.0 - (solver.solve(0.5, 0.0, p, 0.0).y[10, -1] / psi_init))} for p in np.linspace(-2*np.pi, 2*np.pi, grid_res)]
    pd.DataFrame(slice_ph).to_csv("solutions/phase_f/phase_f_hosting/slice_1d_phi.csv", index=False)

    # 2D Slices
    grid_2d = 6
    angles_2d = np.linspace(-np.pi, np.pi, grid_2d)
    
    print("  2D Theta/Rho...")
    slice_th_rh = []
    for th in angles_2d:
        for rh in angles_2d:
            psi_f = solver.solve(0.5, th, np.pi/8, rh).y[10, -1]
            slice_th_rh.append({"theta": th, "rho": rh, "hosting_efficiency": float(1.0 - (psi_f / psi_init))})
    pd.DataFrame(slice_th_rh).to_csv(f"solutions/phase_f/phase_f_hosting/slice_2d_theta_rho.csv", index=False)

    print("  2D Phi/Theta...")
    slice_ph_th = []
    for ph in angles_2d:
        for th in angles_2d:
            psi_f = solver.solve(0.5, th, ph, 0.0).y[10, -1]
            slice_ph_th.append({"phi": ph, "theta": th, "hosting_efficiency": float(1.0 - (psi_f / psi_init))})
    pd.DataFrame(slice_ph_th).to_csv("solutions/phase_f/phase_f_hosting/slice_2d_phi_theta.csv", index=False)

    print("  2D Phi/Rho...")
    slice_ph_rh = []
    for ph in angles_2d:
        for rh in angles_2d:
            psi_f = solver.solve(0.5, 0.0, ph, rh).y[10, -1]
            slice_ph_rh.append({"phi": ph, "rho": rh, "hosting_efficiency": float(1.0 - (psi_f / psi_init))})
    pd.DataFrame(slice_ph_rh).to_csv("solutions/phase_f/phase_f_hosting/slice_2d_phi_rho.csv", index=False)

    print("Analysis Complete.")

if __name__ == "__main__":
    run_hosting_analysis()
