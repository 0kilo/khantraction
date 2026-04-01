import numpy as np
import pandas as pd
import os

# Re-implementing the core solver logic locally for the degeneracy test
KAPPA = 8 * np.pi
XI_DEFAULT = 0.002
M_GLUE = 0.1
LAMBDA_Q = 0.01

def algebraic_ricci_decoupling(q_norm_sq, q_prime_sq, e_2lambda, xi):
    U = 0.5 * M_GLUE**2 * q_norm_sq + 0.25 * LAMBDA_Q * q_norm_sq**2
    T_q = 4 * U - (q_prime_sq / e_2lambda)
    S = 2 * (q_prime_sq / e_2lambda) - 2 * (M_GLUE**2 + LAMBDA_Q * q_norm_sq) * q_norm_sq
    denominator = 1 + 2 * KAPPA * xi * (1 - 12 * xi) * q_norm_sq
    R_exact = (-KAPPA * T_q + 6 * KAPPA * xi * S) / denominator
    return R_exact, U

def get_derivatives(r, state, xi):
    a, b, c, d, a_p, b_p, c_p, d_p, m, phi = state
    q_norm_sq = a**2 + b**2 + c**2 + d**2
    q_prime_sq = a_p**2 + b_p**2 + c_p**2 + d_p**2
    
    e_2lambda = (1 - 2*m/r)**(-1) if (r > 2*m and r > 0) else 1e10
    R_exact, U = algebraic_ricci_decoupling(q_norm_sq, q_prime_sq, e_2lambda, xi)
    
    rho = 0.5 * (q_prime_sq / e_2lambda) + U
    p_r = 0.5 * (q_prime_sq / e_2lambda) - U
    m_p = 4 * np.pi * r**2 * rho
    if r > 2*m and r > 0:
        phi_p = (m + 4 * np.pi * r**3 * p_r) / (r * (r - 2*m))
    else:
        phi_p = 0
    lambda_p = (m/r**2 - m_p) * e_2lambda if r > 0 else 0
    damping = (2/r + phi_p - lambda_p) if r > 0 else 0
    potential_factor = e_2lambda * (M_GLUE**2 + LAMBDA_Q * q_norm_sq - 2 * xi * R_exact)
    
    a_pp = -damping * a_p - potential_factor * a
    b_pp = -damping * b_p - potential_factor * b
    c_pp = -damping * c_p - potential_factor * c
    d_pp = -damping * d_p - potential_factor * d
    
    return np.array([a_p, b_p, c_p, d_p, a_pp, b_pp, c_pp, d_pp, m_p, phi_p])

def rk4_step(r, state, dr, xi):
    k1 = get_derivatives(r, state, xi)
    k2 = get_derivatives(r + 0.5*dr, state + 0.5*dr*k1, xi)
    k3 = get_derivatives(r + 0.5*dr, state + 0.5*dr*k2, xi)
    k4 = get_derivatives(r + dr, state + dr*k3, xi)
    return state + (dr/6.0) * (k1 + 2*k2 + 2*k3 + k4)

def run_sim(omega, theta, phi, rho, A0_base, r_max=20.0, dr=0.01):
    A0 = A0_base * np.exp(omega)
    # Full components from ordered map
    cth, sth = np.cos(theta), np.sin(theta)
    cph, sph = np.cos(phi), np.sin(phi)
    crh, srh = np.cos(rho), np.sin(rho)
    
    a0 = A0 * (cth * cph * crh - sth * sph * srh)
    b0 = A0 * (sth * cph * crh + cth * sph * srh)
    c0 = A0 * (cth * sph * crh - sth * cph * srh)
    d0 = A0 * (cth * cph * srh + sth * sph * crh)
    
    state = np.array([a0, b0, c0, d0, 0, 0, 0, 0, 0, 0])
    r = 1e-4
    while r < r_max:
        state = rk4_step(r, state, dr, XI_DEFAULT)
        r += dr
    return state[8]

def main():
    output_dir = "disprove/phase_b"
    # 2D Slice: theta vs phi at fixed omega=0.5
    omega = 0.5
    A0_base = 0.02
    theta_vals = np.linspace(-2*np.pi, 2*np.pi, 10)
    phi_vals = np.linspace(-2*np.pi, 2*np.pi, 10)
    
    results = []
    print("Running 2D angular sweep for degeneracy check...")
    for t in theta_vals:
        for p in phi_vals:
            m = run_sim(omega, t, p, 0.1, A0_base)
            results.append({"theta": t, "phi": p, "m": m})
            
    df = pd.DataFrame(results)
    df.to_csv(f"{output_dir}/degeneracy_2d_theta_phi.csv", index=False)
    
    print("Mass Stats across angular grid:")
    print(df['m'].describe())
    print(f"Relative Standard Deviation: {df['m'].std() / df['m'].mean():.2e}")

if __name__ == "__main__":
    main()
