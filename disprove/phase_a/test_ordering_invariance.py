import numpy as np
import pandas as pd
import os
import itertools

def quat_mul(q1, q2):
    w1, x1, y1, z1 = q1
    w2, x2, y2, z2 = q2
    return np.array([
        w1*w2 - x1*x2 - y1*y2 - z1*z2,
        w1*x2 + x1*w2 + y1*z2 - z1*y2,
        w1*y2 - x1*z2 + y1*w2 + z1*x2,
        w1*z2 + x1*y2 - y1*x2 + z1*w2
    ])

def get_map(ordering):
    def map_func(omega, theta, phi, rho):
        ew = np.exp(omega)
        qi = np.array([np.cos(theta), np.sin(theta), 0, 0])
        qj = np.array([np.cos(phi), 0, np.sin(phi), 0])
        qk = np.array([np.cos(rho), 0, 0, np.sin(rho)])
        
        if ordering == 'theta_phi_rho': # Original
            q = quat_mul(qi, quat_mul(qj, qk))
        elif ordering == 'phi_theta_rho':
            q = quat_mul(qj, quat_mul(qi, qk))
        elif ordering == 'theta_rho_phi':
            q = quat_mul(qi, quat_mul(qk, qj))
        elif ordering == 'rho_phi_theta':
            q = quat_mul(qk, quat_mul(qj, qi))
        else:
            raise ValueError(f"Unknown ordering: {ordering}")
            
        return ew * q
    return map_func

def get_jacobian(f, omega, theta, phi, rho, eps=1e-6):
    j = np.zeros((4, 4))
    p = np.array([omega, theta, phi, rho])
    for i in range(4):
        p_plus = p.copy()
        p_plus[i] += eps
        p_minus = p.copy()
        p_minus[i] -= eps
        j[:, i] = (f(*p_plus) - f(*p_minus)) / (2 * eps)
    return j

def run_protocol(ordering_name, output_dir):
    f = get_map(ordering_name)
    omega_fixed = 0.5
    angles = ['theta', 'phi', 'rho']
    domain = np.linspace(-2*np.pi, 2*np.pi, 100)
    coarse_domain = np.linspace(-2*np.pi, 2*np.pi, 20)
    
    # 1. 1D Slices: Vary one, fix two (at 0.1 for non-singularity)
    for vary_idx, vary_name in enumerate(angles):
        results = []
        for val in domain:
            p = [omega_fixed, 0.1, 0.1, 0.1]
            p[vary_idx + 1] = val
            J = get_jacobian(f, *p)
            detJ = np.linalg.det(J)
            results.append({'val': val, 'detJ': detJ})
        
        df = pd.DataFrame(results)
        df.to_csv(f"{output_dir}/{ordering_name}_1d_{vary_name}.csv", index=False)

    # 2. 2D Slices: Vary two, fix one
    for fixed_idx, fixed_name in enumerate(angles):
        vary_names = [a for i, a in enumerate(angles) if i != fixed_idx]
        vary_indices = [i + 1 for i, a in enumerate(angles) if i != fixed_idx]
        
        results = []
        for v1 in coarse_domain:
            for v2 in coarse_domain:
                p = [omega_fixed, 0.1, 0.1, 0.1]
                p[vary_indices[0]] = v1
                p[vary_indices[1]] = v2
                J = get_jacobian(f, *p)
                detJ = np.linalg.det(J)
                results.append({vary_names[0]: v1, vary_names[1]: v2, 'detJ': detJ})
        
        df = pd.DataFrame(results)
        df.to_csv(f"{output_dir}/{ordering_name}_2d_{vary_names[0]}_{vary_names[1]}.csv", index=False)

if __name__ == "__main__":
    output_dir = 'disprove/phase_a'
    os.makedirs(output_dir, exist_ok=True)
    
    orderings = ['theta_phi_rho', 'phi_theta_rho', 'theta_rho_phi', 'rho_phi_theta']
    for ord_name in orderings:
        print(f"Running protocol for ordering: {ord_name}...")
        run_protocol(ord_name, output_dir)
    print("Done.")
