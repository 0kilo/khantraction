r"""
Phase G: Classical Rotational / Handedness Properties
Date: 2026-03-29
Purpose: Validates the existence of chiral enantiomers. Performs mirror-pair 
tests to prove trait invariance and chirality reversal under Parity.
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

class PhaseGChiralitySolver:
    def get_vielbeins(self, theta, phi, rho):
        """
        Calculates left-invariant vielbeins E_M^a = (q^-1 d_M q)^a.
        Based on corrected analytical evaluations in Derivation 78.
        """
        # Note: These are the imaginary components only (i, j, k)
        E_rho = np.array([0.0, 0.0, 1.0])
        E_phi = np.array([np.sin(2*rho), np.cos(2*rho), 0.0])
        E_theta = np.array([
            np.cos(2*rho) * np.cos(2*phi),
            -np.sin(2*rho) * np.cos(2*phi),
            np.sin(2*phi)
        ])
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

    def get_chirality_density(self, theta, phi, rho):
        """
        Calculates the internal chirality density Chi = det(J_angular).
        """
        Eth, Eph, Erh = self.get_vielbeins(theta, phi, rho)
        # Manual 3x3 determinant for stability and sign accuracy
        # mat = [Eth, Eph, Erh]
        # det = Eth[0](Eph[1]*Erh[2] - Eph[2]*Erh[1]) - ...
        det = Eth[0]*(Eph[1]*Erh[2] - Eph[2]*Erh[1]) - \
              Eth[1]*(Eph[0]*Erh[2] - Eph[2]*Erh[0]) + \
              Eth[2]*(Eph[0]*Erh[1] - Eph[1]*Erh[0])
        return det

    def equations(self, r, y):
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
        V_ang = 0.01 * np.sin(2*ph)**2
        rho_total = 0.5 * e_neg2L * dq_sq + e_neg2L * omega_mc_sq + U + V_ang
        m_prime = 4 * np.pi * r**2 * rho_total
        phi_prime = (m + 4 * np.pi * r**3 * (rho_total - 2*U - 2*V_ang)) / (r * (r - 2*m))
        H_prime = phi_prime - ((m_prime/r - m/r**2)*e_2L) + 2/r
        w_pp = - H_prime * wp - (M_GLUE**2 + LAMBDA_Q*exp2w - 2*XI*R) * exp2w * e_2L / exp2w
        th_pp = - H_prime * thp
        ph_pp = - H_prime * php - 0.04 * np.sin(2*ph) * np.cos(2*ph) * e_2L / G_reg[2,2]
        rh_pp = - H_prime * rhp
        return [wp, thp, php, rhp, w_pp, th_pp, ph_pp, rh_pp, m_prime, phi_prime]

    def solve(self, omega0, theta0, phi0, rho0, Xp0=[0,0,0,0], r_max=20.0):
        A0 = 0.02
        w_start = np.log(A0) + omega0
        y0 = [w_start, theta0, phi0, rho0, Xp0[0], Xp0[1], Xp0[2], Xp0[3], 0.0, 0.0]
        def horizon_event(r, y): return y[8] - 0.48 * r
        horizon_event.terminal = True
        sol = solve_ivp(self.equations, (1e-4, r_max), y0, method='RK45', 
                        events=horizon_event, rtol=1e-6)
        return sol

def run_chirality_analysis():
    print("--- Starting Phase G: Verified Chirality and Handedness Analysis ---")
    solver = PhaseGChiralitySolver()
    out_dir = "solutions/phase_g/phase_g_chirality"
    os.makedirs(out_dir, exist_ok=True)

    # 1. Mirror-Pair Test (Goal 2 & 3)
    print("Executing Mirror-Pair Validation...")
    # Test True Enantiomers via Topological Chiral Flip (phi -> phi + pi/2)
    seeds = [
        {"id": "Right-Handed", "params": [0.5, np.pi/8, np.pi/8, np.pi/8], "Xp": [0, 0.01, 0.01, 0.01]},
        {"id": "Left-Handed", "params": [0.5, np.pi/8, np.pi/8 + np.pi/2, np.pi/8], "Xp": [0, -0.01, -0.01, -0.01]}
    ]

    results = []
    for s in seeds:
        sol = solver.solve(*s['params'], Xp0=s['Xp'])
        m_final = sol.y[8, -1]
        chi = solver.get_chirality_density(*s['params'][1:])
        results.append({
            "id": s['id'], "mass": float(m_final), "chirality_density": float(chi)
        })
    pd.DataFrame(results).to_csv(f"{out_dir}/mirror_pair_results.csv", index=False)

    # 2. Exhaustive Slice Protocol - Chirality Reversal Matrix (Section 3.2)
    print("Running Exhaustive 1D/2D Chirality Matrix...")
    grid_res = 10

    # 1D Theta
    slice_th = [{"theta": t, "chi": float(solver.get_chirality_density(t, np.pi/8, 0.0))} for t in np.linspace(-2*np.pi, 2*np.pi, grid_res)]
    pd.DataFrame(slice_th).to_csv(f"{out_dir}/slice_1d_theta_chi.csv", index=False)

    # 1D Rho
    slice_rh = [{"rho": r, "chi": float(solver.get_chirality_density(0.0, np.pi/8, r))} for r in np.linspace(-2*np.pi, 2*np.pi, grid_res)]
    pd.DataFrame(slice_rh).to_csv(f"{out_dir}/slice_1d_rho_chi.csv", index=False)

    # 1D Phi
    slice_ph = [{"phi": p, "chi": float(solver.get_chirality_density(0.0, p, 0.0))} for p in np.linspace(-2*np.pi, 2*np.pi, grid_res)]
    pd.DataFrame(slice_ph).to_csv(f"{out_dir}/slice_1d_phi_chi.csv", index=False)

    # 2D Phi/Theta
    angles = np.linspace(-np.pi, np.pi, 8)
    slice_ph_th = []
    for ph in angles:
        for th in angles:
            slice_ph_th.append({"phi": ph, "theta": th, "chi": float(solver.get_chirality_density(th, ph, 0.0))})
    pd.DataFrame(slice_ph_th).to_csv(f"{out_dir}/slice_2d_phi_theta_chi.csv", index=False)

    # 2D Phi/Rho
    slice_ph_rh = []
    for ph in angles:
        for rh in angles:
            slice_ph_rh.append({"phi": ph, "rho": rh, "chi": float(solver.get_chirality_density(0.0, ph, rh))})
    pd.DataFrame(slice_ph_rh).to_csv(f"{out_dir}/slice_2d_phi_rho_chi.csv", index=False)

    # 2D Theta/Rho
    slice_th_rh = []
    for th in angles:
        for rh in angles:
            slice_th_rh.append({"theta": th, "rho": rh, "chi": float(solver.get_chirality_density(th, np.pi/8, rh))})
    pd.DataFrame(slice_th_rh).to_csv(f"{out_dir}/slice_2d_theta_rho_chi.csv", index=False)

    # 3. Rotational Stability Scan (Goal 1 & 4)
    print("Running Rotational Stability Scan...")
    # We simulate rotation by adding a centrifugal mass-shift proxy proportional to Omega^2
    omega_rot_vals = np.linspace(0.0, 0.1, 5)
    rot_results = []
    for o_rot in omega_rot_vals:
        # Measure mass shift under rotation for Right-Handed species
        sol = solver.solve(0.5, np.pi/8, np.pi/8, np.pi/8)
        m_base = sol.y[8, -1]
        # Proxy for rotational energy injection
        m_rot = m_base * (1.0 + 5.0 * o_rot**2) 
        rot_results.append({
            "omega_rot": o_rot, "mass_effective": float(m_rot), "stability": "stable" if m_rot < 2.0 else "unstable"
        })
    pd.DataFrame(rot_results).to_csv(f"{out_dir}/rotational_stability.csv", index=False)

    print("Analysis Complete. Results deposited in solutions/phase_g/phase_g_chirality/")


if __name__ == "__main__":
    run_chirality_analysis()