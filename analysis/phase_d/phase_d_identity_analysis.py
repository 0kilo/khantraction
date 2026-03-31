r"""
Phase D: Identity, Persistence, and Rigidity Analysis
Date: 2026-03-29
Purpose: Defines the classical identity of Khantraction objects. 
Tests for scale-invariance of fingerprints, persistence under angular 
perturbation, and core rigidity under amplitude pressure.
"""

import numpy as np
import pandas as pd
import json
import os
import csv
from scipy.integrate import solve_ivp

# --- Re-importing Solver Logic (Standalone for Phase D) ---
KAPPA = 8.0 * np.pi
XI = 0.002
M_GLUE = 0.1
LAMBDA_Q = 0.01
BETA = np.array([0.01, 0.02, 0.03])

class PhaseDIdentitySolver:
    def get_vielbeins(self, theta, phi, rho):
        c2p, s2p = np.cos(2*phi), np.sin(2*phi)
        c2r, s2r = np.cos(2*rho), np.sin(2*rho)
        E_rho = np.array([0.0, 0.0, 1.0])
        E_phi = np.array([s2r, c2r, 0.0])
        E_theta = np.array([c2r * c2p, -s2r * c2p, s2p])
        return E_theta, E_phi, E_rho

    def get_vielbein_derivatives(self, theta, phi, rho):
        c2p, s2p = np.cos(2*phi), np.sin(2*phi)
        c2r, s2r = np.cos(2*rho), np.sin(2*rho)
        derivs = {}
        derivs[('phi', 'theta')] = np.array([-2*c2r*s2p, 2*s2r*s2p, 2*c2p])
        derivs[('phi', 'phi')] = np.array([0.0, 0.0, 0.0])
        derivs[('phi', 'rho')] = np.array([0.0, 0.0, 0.0])
        derivs[('rho', 'theta')] = np.array([-2*s2r*c2p, -2*c2r*c2p, 0.0])
        derivs[('rho', 'phi')] = np.array([2*c2r, -2*s2r, 0.0])
        derivs[('rho', 'rho')] = np.array([0.0, 0.0, 0.0])
        return derivs

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

    def get_metric_derivatives(self, omega, theta, phi, rho):
        exp2w = np.exp(2 * omega)
        E = self.get_vielbeins(theta, phi, rho)
        dE = self.get_vielbein_derivatives(theta, phi, rho)
        B = exp2w + 2 * BETA
        dG = np.zeros((4, 4, 4))
        dG[0, 0, 0] = 2 * exp2w
        for i in range(3):
            for j in range(3):
                dG[0, i+1, j+1] = 2 * exp2w * np.sum(E[i] * E[j])
        for k_idx, k_name in enumerate(['theta', 'phi', 'rho']):
            for i in range(3):
                for j in range(3):
                    term1 = dE.get((k_name, ['theta', 'phi', 'rho'][i]), np.zeros(3))
                    term2 = dE.get((k_name, ['theta', 'phi', 'rho'][j]), np.zeros(3))
                    dG[k_idx+1, i+1, j+1] = np.sum(B * (term1 * E[j] + E[i] * term2))
        return dG

    def equations(self, r, y, A0):
        w, th, ph, rh, wp, thp, php, rhp, m, phi_pot = y
        Xp = y[4:8]
        if r < 1e-10: return np.zeros_like(y)
        e_2L = 1.0 / (1.0 - 2.0 * m / r) if r > 2*m else 1e10
        e_neg2L = 1.0 / e_2L
        G = self.get_target_metric(w, th, ph, rh)
        G_reg = G + 1e-4 * np.eye(4)
        G_inv = np.linalg.inv(G_reg)
        dG = self.get_metric_derivatives(w, th, ph, rh)
        if w > 10.0: return np.zeros_like(y)
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
        V_ang = 0.01 * np.sin(2*ph)**2
        rho_dens = 0.5 * e_neg2L * dq_sq + e_neg2L * omega_mc_sq + U + V_ang
        V_eff_w = (M_GLUE**2 + LAMBDA_Q * exp2w - 2 * XI * R) * exp2w
        V_eff_ph = 0.04 * np.sin(2*ph) * np.cos(2*ph)
        m_prime = 4 * np.pi * r**2 * rho_dens
        phi_prime = (m + 4 * np.pi * r**3 * (rho_dens - 2*U - 2*V_ang)) / (r * (r - 2*m))
        L_prime = (m_prime / r - m / r**2) / (1 - 2*m/r)
        H_prime = phi_prime - L_prime + 2/r
        P_prime = np.zeros(4)
        for m_idx in range(4):
            term_geom = 0.5 * np.dot(Xp, dG[m_idx] @ Xp)
            term_damp = - H_prime * np.dot(G[m_idx], Xp)
            term_pot = - e_2L * (V_eff_w if m_idx == 0 else (V_eff_ph if m_idx == 2 else 0.0))
            P_prime[m_idx] = term_geom + term_damp + term_pot
        Xpp = G_inv @ (P_prime - np.array([np.dot(dG[:, m_idx, :].T @ Xp, Xp) for m_idx in range(4)]))
        return np.concatenate([Xp, Xpp, [m_prime, phi_prime]])

    def solve(self, omega0, theta0, phi0, rho0, A0=0.02, Xp0=[0,0,0,0], r_max=20.0):
        w_scaled = np.log(A0) + omega0
        y0 = [w_scaled, theta0, phi0, rho0, Xp0[0], Xp0[1], Xp0[2], Xp0[3], 0.0, 0.0]
        def horizon_event(r, y, A0): return y[8] - 0.48 * r
        horizon_event.terminal = True
        sol = solve_ivp(self.equations, (1e-4, r_max), y0, args=(A0,), method='RK45', 
                        events=horizon_event, rtol=1e-6, atol=1e-8)
        return sol

def run_identity_analysis():
    print("--- Starting Phase D: Verified Identity and Rigidity Analysis ---")
    solver = PhaseDIdentitySolver()
    out_dir = "solutions/phase_d/phase_d_identity"
    os.makedirs(out_dir, exist_ok=True)
    
    # 1. Scale-Invariance Test (Omega Sweep)
    print("Running Omega Sweep (Scale-Invariance)...")
    omega_vals = np.linspace(0.1, 1.0, 5)
    invariance_results = []
    for w in omega_vals:
        sol = solver.solve(w, 0.0, 0.0, 0.0)
        m_final = sol.y[8, -1]
        half_m = m_final * 0.5
        idx = np.where(sol.y[8] >= half_m)[0]
        r_half = sol.t[idx[0]] if len(idx) > 0 else np.nan
        invariance_results.append({
            "omega": w, "mass": m_final, "r_half": r_half, "compactness": m_final/r_half
        })
    pd.DataFrame(invariance_results).to_csv(f"{out_dir}/omega_sweep_invariance.csv", index=False)

    # 2. Neighborhood Persistence Test
    print("Running Neighborhood Sweep (Persistence)...")
    perturbations = np.linspace(-0.2, 0.2, 5)
    persistence_results = []
    # Around Phi-dom anchor
    for dp in perturbations:
        sol = solver.solve(0.5, 0.0, np.pi/4 + dp, 0.0, Xp0=[0,0,0.01,0])
        m_final = sol.y[8, -1]
        half_m = m_final * 0.5
        idx = np.where(sol.y[8] >= half_m)[0]
        r_half = sol.t[idx[0]] if len(idx) > 0 else np.nan
        persistence_results.append({
            "d_phi": dp, "mass": m_final, "r_half": r_half, "compactness": m_final/r_half
        })
    pd.DataFrame(persistence_results).to_csv(f"{out_dir}/phi_neighborhood_persistence.csv", index=False)

    # 3. Rigidity Test (Amplitude & External Pressure)
    print("Running Rigidity Tests (Goal 5)...")
    # 3.1 Seeding Rigidity (A0 Sweep)
    amp_vals = [0.01, 0.02, 0.04]
    rigidity_results = []
    for a in amp_vals:
        sol = solver.solve(0.5, 0.0, np.pi/4, 0.0, A0=a, Xp0=[0,0,0.01,0])
        m_final = sol.y[8, -1]
        idx = np.where(sol.y[8] >= m_final * 0.5)[0]
        r_half = sol.t[idx[0]] if len(idx) > 0 else np.nan
        rigidity_results.append({
            "test_type": "seeding_pressure", "parameter": a, "mass": m_final, "r_half": r_half
        })
    
    # 3.2 External Boundary Compression (Goal 5 - Inward Push)
    # We simulate this by reducing r_max significantly to force boundary settling
    r_max_vals = [20.0, 15.0, 10.0]
    for rm in r_max_vals:
        sol = solver.solve(0.5, 0.0, np.pi/4, 0.0, r_max=rm, Xp0=[0,0,0.01,0])
        m_final = sol.y[8, -1]
        idx = np.where(sol.y[8] >= m_final * 0.5)[0]
        r_half = sol.t[idx[0]] if len(idx) > 0 else np.nan
        rigidity_results.append({
            "test_type": "boundary_compression", "parameter": rm, "mass": m_final, "r_half": r_half
        })
    pd.DataFrame(rigidity_results).to_csv(f"{out_dir}/rigidity_results.csv", index=False)

    # 4. Mandatory Slice Protocol - Exhaustive Matrix (Section 3.2)
    print("Running Exhaustive 1D/2D Slice Matrix...")
    grid_res = 10
    
    # 1D Rho Sweep
    slice_rh = [{"rho": r, "mass": float(solver.solve(0.5, 0.0, np.pi/8, r, r_max=10.0).y[8, -1])} for r in np.linspace(-2*np.pi, 2*np.pi, grid_res)]
    pd.DataFrame(slice_rh).to_csv(f"{out_dir}/slice_1d_rho.csv", index=False)
    
    # 2D Phi/Theta
    angles = np.linspace(-np.pi, np.pi, 6)
    slice_ph_th = []
    for ph in angles:
        for th in angles:
            slice_ph_th.append({"phi": ph, "theta": th, "mass": float(solver.solve(0.5, th, ph, 0.0, r_max=5.0).y[8, -1])})
    pd.DataFrame(slice_ph_th).to_csv(f"{out_dir}/slice_2d_phi_theta.csv", index=False)

    # 2D Phi/Rho
    slice_ph_rh = []
    for ph in angles:
        for rh in angles:
            slice_ph_rh.append({"phi": ph, "rho": rh, "mass": float(solver.solve(0.5, 0.0, ph, rh, r_max=5.0).y[8, -1])})
    pd.DataFrame(slice_ph_rh).to_csv(f"{out_dir}/slice_2d_phi_rho.csv", index=False)

    print("Analysis Complete.")

if __name__ == "__main__":
    run_identity_analysis()
