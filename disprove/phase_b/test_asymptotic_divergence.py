import numpy as np
import pandas as pd
import os

# Re-implementing the core solver logic locally for the divergence test
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
    if e_2lambda > 1e11: e_2lambda = 1e11 # Clamp for stability

    R_exact, U = algebraic_ricci_decoupling(q_norm_sq, q_prime_sq, e_2lambda, xi)
    
    rho = 0.5 * (q_prime_sq / e_2lambda) + U
    p_r = 0.5 * (q_prime_sq / e_2lambda) - U
    
    m_p = 4 * np.pi * r**2 * rho
    if r > 2*m and r > 0:
        phi_p = (m + 4 * np.pi * r**3 * p_r) / (r * (r - 2*m))
    else:
        phi_p = 1e6 # Extreme damping if near horizon
        
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

def run_sim(omega, A0_base, xi, r_max, dr=0.01):
    A0 = A0_base * np.exp(omega)
    state = np.array([A0, 0, 0, 0, 0, 0, 0, 0, 0, 0])
    r = 1e-4
    while r < r_max:
        state = rk4_step(r, state, dr, xi)
        r += dr
        if state[8] > r / 2: return {"success": False, "m": state[8]}
    return {"success": True, "m": state[8]}

def main():
    output_dir = "disprove/phase_b"
    os.makedirs(output_dir, exist_ok=True)
    
    # 1D Slice: r_max sweep [20, 100] for a few omega values
    omegas = [0.1, 0.5, 1.0, 1.5, 2.0]
    r_max_vals = np.linspace(20, 100, 10)
    
    results = []
    for w in omegas:
        print(f"Testing divergence for omega={w}...")
        for r_max in r_max_vals:
            res = run_sim(w, 0.02, XI_DEFAULT, r_max)
            res['omega'] = w
            res['r_max'] = r_max
            results.append(res)
            
    pd.DataFrame(results).to_csv(f"{output_dir}/asymptotic_divergence.csv", index=False)
    print("Done.")

if __name__ == "__main__":
    main()
