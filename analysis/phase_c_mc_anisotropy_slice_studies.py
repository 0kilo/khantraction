"""
Phase C Maurer-Cartan Slice Studies
Date: 2026-03-29
Purpose: Evaluates the left-invariant vector fields (E_theta, E_phi, E_rho) 
across 1D and 2D angular slices from -2pi to 2pi. Maps how the ordered 
parameters project onto the internal (i, j, k) generators.
"""

import numpy as np
import os
import csv
import json

def quat_mult(q1, q2):
    """Multiplies two quaternions [r, i, j, k]"""
    r1, i1, j1, k1 = q1
    r2, i2, j2, k2 = q2
    return np.array([
        r1*r2 - i1*i2 - j1*j2 - k1*k2,
        r1*i2 + i1*r2 + j1*k2 - k1*j2,
        r1*j2 - i1*k2 + j1*r2 + k1*i2,
        r1*k2 + i1*j2 - j1*i2 + k1*r2
    ])

def quat_inv(q):
    """Inverse of a unit quaternion"""
    r, i, j, k = q
    return np.array([r, -i, -j, -k])

def evaluate_vielbeins(theta, phi, rho):
    """
    Computes E_M = q^{-1} \partial_M q mapping to [r, i, j, k].
    Analytically:
    E_rho = k
    E_phi = e^{-rho k} j e^{rho k}
    E_theta = e^{-rho k} e^{-phi j} i e^{phi j} e^{rho k}
    """
    # Exponentials
    e_theta_i = np.array([np.cos(theta), np.sin(theta), 0, 0])
    e_phi_j = np.array([np.cos(phi), 0, np.sin(phi), 0])
    e_rho_k = np.array([np.cos(rho), 0, 0, np.sin(rho)])
    
    # Inverses
    inv_rho_k = quat_inv(e_rho_k)
    inv_phi_j = quat_inv(e_phi_j)
    
    # Base generators
    base_i = np.array([0, 1, 0, 0])
    base_j = np.array([0, 0, 1, 0])
    base_k = np.array([0, 0, 0, 1])
    
    # E_rho = k
    E_rho = base_k
    
    # E_phi = inv(e_rho_k) * j * e_rho_k
    E_phi = quat_mult(quat_mult(inv_rho_k, base_j), e_rho_k)
    
    # E_theta = inv(e_rho_k) * inv(e_phi_j) * i * e_phi_j * e_rho_k
    E_theta = quat_mult(quat_mult(quat_mult(quat_mult(inv_rho_k, inv_phi_j), base_i), e_phi_j), e_rho_k)
    
    return E_theta, E_phi, E_rho

def run_1d_slices(domain, out_dir):
    print("Running 1D Slices...")
    slices = [
        ("vary_theta_phi0_rho0", lambda x: (x, 0.0, 0.0)),
        ("vary_phi_theta0_rho0", lambda x: (0.0, x, 0.0)),
        ("vary_rho_theta0_phi0", lambda x: (0.0, 0.0, x))
    ]
    
    for name, func in slices:
        path = os.path.join(out_dir, f"{name}.csv")
        with open(path, 'w', newline='') as f:
            writer = csv.writer(f)
            writer.writerow(["angle_val", "E_theta_i", "E_theta_j", "E_theta_k", "E_phi_i", "E_phi_j", "E_phi_k", "E_rho_k"])
            for val in domain:
                th, ph, rh = func(val)
                Eth, Eph, Erh = evaluate_vielbeins(th, ph, rh)
                writer.writerow([val, Eth[1], Eth[2], Eth[3], Eph[1], Eph[2], Eph[3], Erh[3]])

def run_2d_slices(domain, out_dir):
    print("Running 2D Slices...")
    slices = [
        ("vary_theta_phi_rho0", lambda x, y: (x, y, 0.0)),
        ("vary_theta_rho_phi0", lambda x, y: (x, 0.0, y)),
        ("vary_phi_rho_theta0", lambda x, y: (0.0, x, y))
    ]
    
    for name, func in slices:
        path = os.path.join(out_dir, f"{name}.csv")
        with open(path, 'w', newline='') as f:
            writer = csv.writer(f)
            writer.writerow(["var1", "var2", "E_theta_i", "E_theta_j", "E_theta_k", "E_phi_i", "E_phi_j", "E_phi_k"])
            for v1 in domain:
                for v2 in domain:
                    th, ph, rh = func(v1, v2)
                    Eth, Eph, Erh = evaluate_vielbeins(th, ph, rh)
                    writer.writerow([v1, v2, Eth[1], Eth[2], Eth[3], Eph[1], Eph[2], Eph[3]])

if __name__ == "__main__":
    out_dir = "solutions/phase_c_mc_slice_studies"
    os.makedirs(out_dir, exist_ok=True)
    
    domain = np.linspace(-2*np.pi, 2*np.pi, 100)
    
    run_1d_slices(domain, out_dir)
    run_2d_slices(domain, out_dir)
    
    with open(os.path.join(out_dir, "summary.json"), 'w') as f:
        json.dump({"status": "Complete", "domain": "[-2pi, 2pi]", "points": 100}, f)
    
    print("All combinations calculated and deposited safely.")