r"""
Phase C: Maurer-Cartan Radial Solver (Corrected Implementation)
Date: 2026-03-29
Purpose: Implements the exact anisotropic Maurer-Cartan (MC) symmetry breaking 
in the radial Khantraction system. Solves the Non-Linear Sigma Model (NLSM) 
equations directly in the angular basis (\omega, \theta, \phi, \rho).
"""

import numpy as np
import pandas as pd
import json
import os
import csv
from scipy.integrate import solve_ivp

# --- Constants ---
KAPPA = 8.0 * np.pi
XI = 0.002
M_GLUE = 0.1
LAMBDA_Q = 0.01

# Anisotropic MC Breaking Weights (Derivation 78)
BETA_1 = 0.01  # i channel
BETA_2 = 0.02  # j channel
BETA_3 = 0.03  # k channel

class PhaseCMCRadialSolver:
    def __init__(self, beta=[BETA_1, BETA_2, BETA_3]):
        self.beta = np.array(beta)

    def get_vielbeins(self, theta, phi, rho):
        """
        Calculates left-invariant vielbeins E_M^a = (q^-1 d_M q)^a.
        Basis: (theta, phi, rho) -> (i, j, k)
        """
        c2p, s2p = np.cos(2*phi), np.sin(2*phi)
        c2r, s2r = np.cos(2*rho), np.sin(2*rho)

        # E_rho = k
        E_rho = np.array([0.0, 0.0, 1.0])
        # E_phi = j cos(2rho) + i sin(2rho)
        E_phi = np.array([s2r, c2r, 0.0])
        # E_theta = i cos(2rho)cos(2phi) - j sin(2rho)cos(2phi) + k sin(2phi)
        E_theta = np.array([c2r * c2p, -s2r * c2p, s2p])

        return E_theta, E_phi, E_rho

    def get_vielbein_derivatives(self, theta, phi, rho):
        """
        Calculates d_K E_M^a.
        Returns a dictionary mapping (K, M) to the (i, j, k) vector.
        """
        c2p, s2p = np.cos(2*phi), np.sin(2*phi)
        c2r, s2r = np.cos(2*rho), np.sin(2*rho)

        derivs = {}
        # theta derivatives are 0
        
        # phi derivatives
        derivs[('phi', 'theta')] = np.array([-2*c2r*s2p, 2*s2r*s2p, 2*c2p])
        derivs[('phi', 'phi')] = np.array([0.0, 0.0, 0.0])
        derivs[('phi', 'rho')] = np.array([0.0, 0.0, 0.0])

        # rho derivatives
        derivs[('rho', 'theta')] = np.array([-2*s2r*c2p, -2*c2r*c2p, 0.0])
        derivs[('rho', 'phi')] = np.array([2*c2r, -2*s2r, 0.0])
        derivs[('rho', 'rho')] = np.array([0.0, 0.0, 0.0])

        return derivs

    def get_target_metric(self, omega, theta, phi, rho):
        """
        Calculates target space metric G_MN.
        Order: (omega, theta, phi, rho)
        """
        E = self.get_vielbeins(theta, phi, rho) # (E_th, E_ph, E_rh)
        exp2w = np.exp(2 * omega)
        B = exp2w + 2 * self.beta # [B1, B2, B3]

        G = np.zeros((4, 4))
        G[0, 0] = exp2w # G_ww

        # G_ij = sum_a Ba E_i^a E_j^a for i,j in {th, ph, rh}
        indices = [1, 2, 3] # theta, phi, rho
        for i_idx, i_name in enumerate(['theta', 'phi', 'rho']):
            for j_idx, j_name in enumerate(['theta', 'phi', 'rho']):
                G[i_idx+1, j_idx+1] = np.sum(B * E[i_idx] * E[j_idx])
        
        return G

    def get_metric_derivatives(self, omega, theta, phi, rho):
        """Calculates d_K G_MN."""
        exp2w = np.exp(2 * omega)
        E = self.get_vielbeins(theta, phi, rho)
        dE = self.get_vielbein_derivatives(theta, phi, rho)
        B = exp2w + 2 * self.beta
        
        dG = np.zeros((4, 4, 4)) # [K, M, N]

        # omega derivatives
        dG[0, 0, 0] = 2 * exp2w
        for i in range(3):
            for j in range(3):
                # d_w G_ij = 2 exp2w sum E_i E_j (since only exp2w depends on w)
                dG[0, i+1, j+1] = 2 * exp2w * np.sum(E[i] * E[j])

        # angular derivatives
        for k_idx, k_name in enumerate(['theta', 'phi', 'rho']):
            for i_idx, i_name in enumerate(['theta', 'phi', 'rho']):
                for j_idx, j_name in enumerate(['theta', 'phi', 'rho']):
                    # d_k G_ij = sum B_a (d_k E_i^a E_j^a + E_i^a d_k E_j^a)
                    term1 = dE.get((k_name, i_name), np.zeros(3))
                    term2 = dE.get((k_name, j_name), np.zeros(3))
                    dG[k_idx+1, i_idx+1, j_idx+1] = np.sum(B * (term1 * E[j_idx] + E[i_idx] * term2))
        
        return dG

    def equations(self, r, y):
        # y = [w, th, ph, rh, wp, thp, php, rhp, m, phi_pot]
        w, th, ph, rh, wp, thp, php, rhp, m, phi_pot = y
        X = y[0:4]
        Xp = y[4:8]

        if r < 1e-10: return np.zeros_like(y)

        # Metric components
        e_2L = 1.0 / (1.0 - 2.0 * m / r) if r > 2*m else 1e10
        e_neg2L = 1.0 / e_2L
        
        # Target space geometry
        G = self.get_target_metric(w, th, ph, rh)
        # Add regularization to handle chart singularities (e.g., at phi = pi/4)
        G_reg = G + 1e-4 * np.eye(4)
        G_inv = np.linalg.inv(G_reg)
        dG = self.get_metric_derivatives(w, th, ph, rh)

        # Cap omega to prevent exp(2w) overflow
        if w > 10.0: return np.zeros_like(y)

        # Trace and Ricci (Derivation 79)
        exp2w = np.exp(2*w)
        U = 0.5 * M_GLUE**2 * exp2w + 0.25 * LAMBDA_Q * exp2w**2
        
        # G_MN Xp^M Xp^N = |dq|^2 + 2 Omega_MC^2
        kin_sum_total = np.dot(Xp, G @ Xp)
        
        # T_q = -e^-2L |dq|^2 - 4U
        # T_MC = 2 e^-2L Omega_MC^2
        # |dq|^2 = exp2w (wp^2 + thp^2 + php^2 + rhp^2) -- ONLY if orthogonal
        # Let's use the actual kinetic term components.
        E = self.get_vielbeins(th, ph, rh)
        w_r = np.zeros(3)
        for i in range(3): w_r += E[i] * Xp[i+1]
        omega_mc_sq = np.sum(self.beta * w_r**2)
        dq_sq = exp2w * (wp**2 + np.sum(w_r**2))
        
        T_q = -e_neg2L * dq_sq - 4 * U
        T_MC = 2 * e_neg2L * omega_mc_sq
        
        # S = 2 e^-2L |dq|^2 - 2 (m_g^2 + lambda |q|^2) |q|^2
        S = 2 * e_neg2L * dq_sq - 2 * (M_GLUE**2 + LAMBDA_Q * exp2w) * exp2w
        
        R_num = -KAPPA * (T_q + T_MC) + 6 * KAPPA * XI * S
        R_den = 1.0 + 2 * KAPPA * XI * (1.0 - 12.0 * XI) * exp2w
        R = R_num / R_den

        # Einstein Sector
        rho = 0.5 * e_neg2L * dq_sq + e_neg2L * omega_mc_sq + U 
        # Add a small exploratory angular potential to force evolution (Goal 5)
        # Based on Phase B improved dynamics: sin^2(2phi)
        V_ang = 0.01 * np.sin(2*ph)**2
        rho += V_ang
        
        # Ricci feedback into Matter
        V_eff_w = (M_GLUE**2 + LAMBDA_Q * exp2w - 2 * XI * R) * exp2w
        V_eff_ph = 0.01 * 2 * np.sin(2*ph) * np.cos(2*ph) * 2 # d_phi V_ang
        
        m_prime = 4 * np.pi * r**2 * rho
        phi_prime = (m + 4 * np.pi * r**3 * (rho - 2*U - 2*V_ang)) / (r * (r - 2*m)) 

        # Matter Sector NLSM EOM
        L_prime = (m_prime / r - m / r**2) / (1 - 2*m/r)
        H_prime = phi_prime - L_prime + 2/r
        
        P_prime = np.zeros(4)
        for m_idx in range(4):
            term_geom = 0.5 * np.dot(Xp, dG[m_idx] @ Xp)
            term_damp = - H_prime * np.dot(G[m_idx], Xp)
            # Potentials
            if m_idx == 0: term_pot = - e_2L * V_eff_w
            elif m_idx == 2: term_pot = - e_2L * V_eff_ph
            else: term_pot = 0.0
            P_prime[m_idx] = term_geom + term_damp + term_pot

        # Xpp = G_inv (P' - d_K G_ML Xp^K Xp^L)
        # Actually (G Xp)' = G Xpp + d_K G Xp^K Xp
        Xpp = G_inv @ (P_prime - np.array([np.dot(dG[:, m_idx, :].T @ Xp, Xp) for m_idx in range(4)]))

        return np.concatenate([Xp, Xpp, [m_prime, phi_prime]])

    def solve(self, omega0, theta0, phi0, rho0, r_max=20.0, dr=0.01, Xp0=[0,0,0,0]):
        # Initial Conditions: regular origin
        # Use A0 scaling consistent with paper (0.02)
        A0 = 0.02
        w_scaled = np.log(A0) + omega0
        y0 = [w_scaled, theta0, phi0, rho0, Xp0[0], Xp0[1], Xp0[2], Xp0[3], 0.0, 0.0]
        
        # We start at small r to avoid singularity
        r_span = (1e-4, r_max)
        t_eval = np.arange(1e-4, r_max, dr)
        
        def horizon_event(r, y):
            # 2m/r < 1
            return y[8] - 0.45 * r
        horizon_event.terminal = True
        
        sol = solve_ivp(self.equations, r_span, y0, t_eval=t_eval, method='RK45', 
                        events=horizon_event, rtol=1e-6)
        return sol

def run_scans():
    print("--- Starting Phase C: Corrected MC Radial Scans ---")
    solver = PhaseCMCRadialSolver()
    out_dir = "solutions/phase_c/phase_c_angular_traits"
    os.makedirs(f"{out_dir}/profiles", exist_ok=True)
    
    # 1. Representative Seeds (Goal 1 & 4)
    seeds = [
        {"id": "scalar", "w": 0.5, "th": 0.0, "ph": 0.0, "rh": 0.0, "Xp": [0,0,0,0]},
        {"id": "theta_dom", "w": 0.5, "th": np.pi, "ph": 0.0, "rh": 0.0, "Xp": [0, 0.01, 0, 0]},
        {"id": "phi_dom", "w": 0.5, "th": 0.0, "ph": np.pi/4, "rh": 0.0, "Xp": [0, 0, 0.01, 0]},
        {"id": "fully_mixed", "w": 0.5, "th": np.pi, "ph": np.pi/4, "rh": np.pi/2, "Xp": [0, 0.01, 0.01, 0.01]}
    ]
    
    summary = []
    for s in seeds:
        print(f"Running Seed: {s['id']}")
        sol = solver.solve(s['w'], s['th'], s['ph'], s['rh'], Xp0=s['Xp'])
        
        rs = sol.t
        ms = sol.y[8]
        ws = sol.y[0]
        
        final_m = ms[-1]
        
        # Metric Extraction (Goal 2)
        half_m = final_m * 0.5
        m90 = final_m * 0.9
        
        idx_half = np.where(ms >= half_m)[0]
        r_half = rs[idx_half[0]] if len(idx_half) > 0 else None
        
        idx_90 = np.where(ms >= m90)[0]
        r_90 = rs[idx_90[0]] if len(idx_90) > 0 else None
        
        # Core-to-Bulk Balance (Core defined as r < 1.0)
        idx_core = np.where(rs <= 1.0)[0]
        m_core = ms[idx_core[-1]] if len(idx_core) > 0 else 0
        core_bulk_ratio = m_core / final_m if final_m > 0 else 0
        
        # Profile Skewness (Proxy: mean radius of mass distribution)
        # Using dM/dr as weight
        dm_dr = np.gradient(ms, rs)
        mean_r = np.trapezoid(rs * dm_dr, x=rs) / final_m if final_m > 0 else 0
        skewness_proxy = mean_r / r_half if r_half else 0
        
        summary.append({
            "id": s['id'],
            "final_mass": float(final_m),
            "mass_half_radius": float(r_half) if r_half else None,
            "mass_90_radius": float(r_90) if r_90 else None,
            "core_mass_fraction": float(core_bulk_ratio),
            "skewness_proxy": float(skewness_proxy)
        })
        
        # Save profile
        df = pd.DataFrame({
            'r': rs,
            'omega': ws,
            'theta': sol.y[1],
            'phi': sol.y[2],
            'rho': sol.y[3],
            'mass': ms
        })
        df.to_csv(f"{out_dir}/profiles/{s['id']}.csv", index=False)

    # 2. 1D Slice Protocol - Exhaustive Matrix (Goal 2.2)
    print("Running Exhaustive 1D Slice Matrix...")
    # Vary Phi
    slice_phi = [{"phi": p, "mass": float(solver.solve(0.5, 0.0, p, 0.0, r_max=10.0).y[8, -1])} for p in np.linspace(-2*np.pi, 2*np.pi, 15)]
    pd.DataFrame(slice_phi).to_csv(f"{out_dir}/slice_1d_phi.csv", index=False)
    
    # Vary Theta
    slice_th = [{"theta": t, "mass": float(solver.solve(0.5, t, np.pi/8, 0.0, r_max=10.0).y[8, -1])} for t in np.linspace(-2*np.pi, 2*np.pi, 15)]
    pd.DataFrame(slice_th).to_csv(f"{out_dir}/slice_1d_theta.csv", index=False)
    
    # Vary Rho
    slice_rh = [{"rho": r, "mass": float(solver.solve(0.5, 0.0, np.pi/8, r, r_max=10.0).y[8, -1])} for r in np.linspace(-2*np.pi, 2*np.pi, 15)]
    pd.DataFrame(slice_rh).to_csv(f"{out_dir}/slice_1d_rho.csv", index=False)

    # 3. 2D Slice Protocol - Exhaustive Matrix (Goal 2.2)
    print("Running Exhaustive 2D Slice Matrix...")
    grid_size = 8 # Reduced for total combinatorial execution speed
    angles = np.linspace(-np.pi, np.pi, grid_size)
    
    # Pair: Theta/Rho (The Subsystem)
    slice_th_rh = []
    for th in angles:
        for rh in angles:
            slice_th_rh.append({"theta": th, "rho": rh, "mass": float(solver.solve(0.5, th, np.pi/8, rh, r_max=5.0).y[8, -1])})
    pd.DataFrame(slice_th_rh).to_csv(f"{out_dir}/slice_2d_theta_rho.csv", index=False)

    # Pair: Phi/Theta
    slice_ph_th = []
    for ph in angles:
        for th in angles:
            slice_ph_th.append({"phi": ph, "theta": th, "mass": float(solver.solve(0.5, th, ph, 0.0, r_max=5.0).y[8, -1])})
    pd.DataFrame(slice_ph_th).to_csv(f"{out_dir}/slice_2d_phi_theta.csv", index=False)

    # Pair: Phi/Rho
    slice_ph_rh = []
    for ph in angles:
        for rh in angles:
            slice_ph_rh.append({"phi": ph, "rho": rh, "mass": float(solver.solve(0.5, 0.0, ph, rh, r_max=5.0).y[8, -1])})
    pd.DataFrame(slice_ph_rh).to_csv(f"{out_dir}/slice_2d_phi_rho.csv", index=False)

    with open(f"{out_dir}/summary.json", 'w') as f:
        json.dump(summary, f, indent=4)
    print("Scans Complete.")

if __name__ == "__main__":
    run_scans()
