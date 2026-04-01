import numpy as np
import pandas as pd
import os
import json

def get_pullback_eigenvalues(phi, omega=0.5):
    """
    Returns the three eigenvalues of the angular pullback metric.
    lambda_phi = 1
    lambda_plus = 1 + sin(2*phi)
    lambda_minus = 1 - sin(2*phi)
    Scaled by exp(2*omega).
    """
    scale = np.exp(2 * omega)
    sin2phi = np.sin(2 * phi)
    l_phi = 1.0 * scale
    l_plus = (1.0 + sin2phi) * scale
    l_minus = (1.0 - sin2phi) * scale
    return l_phi, l_plus, l_minus

def get_det_jacobian(phi, omega=0.5):
    """det J = exp(4*omega) * cos(2*phi)"""
    return np.exp(4 * omega) * np.cos(2 * phi)

def run_scan():
    output_dir = "solutions/phase_i/phase_i_geometric_anisotropy_scan"
    os.makedirs(output_dir, exist_ok=True)
    
    omega = 0.5
    angles = np.linspace(-2 * np.pi, 2 * np.pi, 100)
    
    # 1. 1D Slices
    # Vary phi (the primary controller)
    phi_scan = []
    for p in angles:
        l_phi, l_p, l_m = get_pullback_eigenvalues(p, omega)
        detJ = get_det_jacobian(p, omega)
        phi_scan.append({
            "phi": p, "l_phi": l_phi, "l_plus": l_p, "l_minus": l_m, "detJ": detJ,
            "anisotropy_ratio": max(l_p, l_m) / max(min(l_p, l_m), 1e-9)
        })
    pd.DataFrame(phi_scan).to_csv(f"{output_dir}/slice_1d_phi.csv", index=False)
    
    # Vary theta (constant stiffness)
    theta_scan = []
    for t in angles:
        l_phi, l_p, l_m = get_pullback_eigenvalues(0.0, omega) # phi=0
        detJ = get_det_jacobian(0.0, omega)
        theta_scan.append({"theta": t, "l_phi": l_phi, "l_plus": l_p, "l_minus": l_m, "detJ": detJ})
    pd.DataFrame(theta_scan).to_csv(f"{output_dir}/slice_1d_theta.csv", index=False)

    # Vary rho (constant stiffness)
    rho_scan = []
    for r in angles:
        l_phi, l_p, l_m = get_pullback_eigenvalues(0.0, omega)
        detJ = get_det_jacobian(0.0, omega)
        rho_scan.append({"rho": r, "l_phi": l_phi, "l_plus": l_p, "l_minus": l_m, "detJ": detJ})
    pd.DataFrame(rho_scan).to_csv(f"{output_dir}/slice_1d_rho.csv", index=False)

    # 2. 2D Slices
    # Vary (phi, rho)
    res_2d = 50
    angles_2d = np.linspace(-2 * np.pi, 2 * np.pi, res_2d)
    phi_rho_2d = []
    for p in angles_2d:
        for r in angles_2d:
            l_phi, l_p, l_m = get_pullback_eigenvalues(p, omega)
            phi_rho_2d.append({"phi": p, "rho": r, "l_plus": l_p, "l_minus": l_m})
    pd.DataFrame(phi_rho_2d).to_csv(f"{output_dir}/slice_2d_phi_rho.csv", index=False)

    # Vary (theta, phi)
    theta_phi_2d = []
    for t in angles_2d:
        for p in angles_2d:
            l_phi, l_p, l_m = get_pullback_eigenvalues(p, omega)
            theta_phi_2d.append({"theta": t, "phi": p, "l_plus": l_p, "l_minus": l_m})
    pd.DataFrame(theta_phi_2d).to_csv(f"{output_dir}/slice_2d_theta_phi.csv", index=False)

    # Vary (theta, rho) at mixed phi
    theta_rho_2d = []
    phi_mixed = np.pi / 8
    for t in angles_2d:
        for r in angles_2d:
            l_phi, l_p, l_m = get_pullback_eigenvalues(phi_mixed, omega)
            theta_rho_2d.append({"theta": t, "rho": r, "l_plus": l_p, "l_minus": l_m})
    pd.DataFrame(theta_rho_2d).to_csv(f"{output_dir}/slice_2d_theta_rho.csv", index=False)

    # 3. Bulk Summary
    summary = {
        "omega": omega,
        "max_anisotropy_ratio": float(np.max([s["anisotropy_ratio"] for s in phi_scan if abs(s["detJ"]) > 1e-3])),
        "singular_phi_locations": [float(p) for p in angles if abs(np.cos(2*p)) < 0.05],
        "stiffness_range": [float(np.exp(2*omega) * (1-1)), float(np.exp(2*omega) * (1+1))]
    }
    with open(f"{output_dir}/bulk_summary.json", "w") as f:
        json.dump(summary, f, indent=2)

    print(f"Scan complete. Results in {output_dir}")

if __name__ == "__main__":
    run_scan()
