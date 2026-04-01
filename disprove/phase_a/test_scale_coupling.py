import numpy as np
import os

def get_q(omega, theta, phi, rho):
    ew = np.exp(omega)
    qi = np.array([np.cos(theta), np.sin(theta), 0, 0])
    qj = np.array([np.cos(phi), 0, np.sin(phi), 0])
    qk = np.array([np.cos(rho), 0, 0, np.sin(rho)])
    
    # Original ordering
    def quat_mul(q1, q2):
        w1, x1, y1, z1 = q1
        w2, x2, y2, z2 = q2
        return np.array([
            w1*w2 - x1*x2 - y1*y2 - z1*z2,
            w1*x2 + x1*w2 + y1*z2 - z1*y2,
            w1*y2 - x1*z2 + y1*w2 + z1*x2,
            w1*z2 + x1*y2 - y1*x2 + z1*w2
        ])
    
    q = quat_mul(qi, quat_mul(qj, qk))
    return ew * q

def get_jacobian(omega, theta, phi, rho, eps=1e-6):
    j = np.zeros((4, 4))
    p = np.array([omega, theta, phi, rho])
    for i in range(4):
        p_plus = p.copy()
        p_plus[i] += eps
        p_minus = p.copy()
        p_minus[i] -= eps
        j[:, i] = (get_q(*p_plus) - get_q(*p_minus)) / (2 * eps)
    return j

def get_metric(omega, theta, phi, rho):
    J = get_jacobian(omega, theta, phi, rho)
    return J.T @ J

def analyze_scale_coupling():
    # We want to see how the metric and derived quantities scale with omega
    test_points = [
        (0.5, 0.1, 0.2, 0.3),
        (1.0, 0.1, 0.2, 0.3),
        (2.0, 0.1, 0.2, 0.3)
    ]
    
    print("--- Metric Scaling with Omega ---")
    for w, t, p, r in test_points:
        G = get_metric(w, t, p, r)
        # Check if G scales as exp(2*w)
        # Normalized metric
        G_norm = G / np.exp(2*w)
        print(f"Omega={w:.1f}, G[0,0]/exp(2w)={G_norm[0,0]:.4f}, G[1,1]/exp(2w)={G_norm[1,1]:.4f}")

    print("\n--- Non-minimal Coupling Scaling ---")
    # Ricci scalar R scales as exp(-2*omega)
    # Potentail V = xi * R * |Q|^2
    # |Q|^2 scales as exp(2*omega)
    # So V should be independent of omega?
    
    # Let's check the kinetic term vs a hypothetical potential V = |Q|^2
    for w, t, p, r in test_points:
        Q = get_q(w, t, p, r)
        Q2 = np.sum(Q**2)
        # Kinetic term scale (e.g. G[1,1])
        G = get_metric(w, t, p, r)
        kin_scale = G[1,1]
        
        ratio = kin_scale / Q2
        print(f"Omega={w:.1f}, Kinetic/|Q|^2 ratio={ratio:.4f}")
        
    print("\nObservation: If V is not proportional to exp(2*omega), then the dynamics change with omega.")
    print("If V = xi * R * |Q|^2, and R ~ exp(-2w), |Q|^2 ~ exp(2w), then V ~ const.")
    print("Kinetic ~ exp(2w). Ratio Kinetic/V ~ exp(2w).")
    print("This means for large omega, kinetic terms dominate, making the 'fold' unstable or different.")

if __name__ == "__main__":
    analyze_scale_coupling()
