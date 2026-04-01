import numpy as np
import os

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
        else:
            raise ValueError(f"Unknown ordering: {ordering}")
            
        return ew * q
    return map_func

def get_jacobian(f, omega, theta, phi, rho, eps=1e-7):
    j = np.zeros((4, 4))
    p = [omega, theta, phi, rho]
    for i in range(4):
        p_plus = list(p)
        p_plus[i] += eps
        p_minus = list(p)
        p_minus[i] -= eps
        j[:, i] = (f(*p_plus) - f(*p_minus)) / (2 * eps)
    return j

def prove_lock(ordering, middle_name, outer_names):
    f = get_map(ordering)
    omega, theta, phi, rho = 0.5, 0.1, 0.1, 0.1
    
    # Define singular point for middle angle
    # In both cases, det J ~ cos(2 * middle)
    singular_val = np.pi / 4
    
    if ordering == 'theta_phi_rho':
        p_sing = [0.5, 0.1, singular_val, 0.1]
        v_idx = [1, 3] # theta and rho
    else:
        p_sing = [0.5, singular_val, 0.1, 0.1]
        v_idx = [2, 3] # phi and rho
        
    J = get_jacobian(f, *p_sing)
    
    # Tangents of outer angles
    v1 = J[:, v_idx[0]]
    v2 = J[:, v_idx[1]]
    
    # Normalized overlap
    cos_sim = np.dot(v1, v2) / (np.linalg.norm(v1) * np.linalg.norm(v2))
    rank = np.linalg.matrix_rank(J)
    
    print(f"--- Proof for Ordering: {ordering} ---")
    print(f"Singular Middle Angle ({middle_name}): {singular_val:.4f}")
    print(f"Jacobian Rank: {rank}")
    print(f"Overlap between outer tangents ({outer_names[0]}, {outer_names[1]}): {cos_sim:.6f}")
    
    if abs(abs(cos_sim) - 1.0) < 1e-5:
        print("RESULT: Tangents are COLLINEAR. Gimbal lock confirmed.")
    else:
        print("RESULT: Tangents are independent.")
    print("")

if __name__ == "__main__":
    # Case 1: Original map, phi is middle
    prove_lock('theta_phi_rho', 'phi', ['theta', 'rho'])
    
    # Case 2: Disproof map, theta is middle
    prove_lock('phi_theta_rho', 'theta', ['phi', 'rho'])
