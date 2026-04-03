"""Shared direct ordered-manifold machinery for Phases I, J, E, and K.

This module implements the exact pullback metric from Derivation 90, the weak-
gravity ordered-manifold wave operator from Derivation 91, and direct 3D
interaction-energy bookkeeping inspired by Derivation 92.

It intentionally avoids the old exploratory beta-coefficient path.
"""

from __future__ import annotations

import math
from dataclasses import dataclass
from typing import Iterable

import numpy as np


@dataclass(frozen=True)
class OrderedSeed:
    label: str
    omega: float
    theta: float
    phi: float
    rho: float


@dataclass(frozen=True)
class DirectRuntimeConfig:
    m_glue: float = 0.1
    lambda_q: float = 0.01
    xi: float = 0.002
    kappa: float = 8.0 * math.pi
    central_amplitude_base: float = 0.02
    phi_metric_regularization: float = 1.0e-3
    r0: float = 1.0e-3
    r_max: float = 12.0
    dr: float = 0.01
    horizon_margin: float = 1.0e-6
    max_mass: float = 10.0
    max_abs_state: float = 40.0
    max_steps: int = 300000
    decay_target: float = 5.0e-2
    grid_size: int = 15
    dx: float = 0.45
    dt: float = 0.04
    time_steps: int = 36


@dataclass
class RadialProfile:
    seed: OrderedSeed
    r: np.ndarray
    y: np.ndarray
    qnorm: np.ndarray
    energy_density: np.ndarray
    radial_pressure: np.ndarray
    tangential_pressure: np.ndarray
    ricci: np.ndarray
    final_mass: float
    compactness_90: float
    compactness_half: float
    boundary_qnorm: float
    boundary_state_prime_norm: float
    success: bool
    failure_reason: str
    horizon_hit: bool


def ordered_metric(w: float | np.ndarray, phi: float | np.ndarray) -> np.ndarray:
    exp2w = np.exp(2.0 * w)
    sin2phi = np.sin(2.0 * phi)
    g = np.zeros((4, 4) + np.shape(exp2w), dtype=float)
    g[0, 0] = exp2w
    g[1, 1] = exp2w
    g[2, 2] = exp2w
    g[3, 3] = exp2w
    g[1, 3] = exp2w * sin2phi
    g[3, 1] = g[1, 3]
    return g


def ordered_metric_inverse(
    w: float | np.ndarray,
    phi: float | np.ndarray,
    regularization: float,
) -> np.ndarray:
    exp_neg2w = np.exp(-2.0 * w)
    sin2phi = np.sin(2.0 * phi)
    denom = np.maximum(1.0 - sin2phi * sin2phi, regularization * regularization)
    g_inv = np.zeros((4, 4) + np.shape(exp_neg2w), dtype=float)
    g_inv[0, 0] = exp_neg2w
    g_inv[2, 2] = exp_neg2w
    g_inv[1, 1] = exp_neg2w / denom
    g_inv[3, 3] = exp_neg2w / denom
    g_inv[1, 3] = -exp_neg2w * sin2phi / denom
    g_inv[3, 1] = g_inv[1, 3]
    return g_inv


def metric_derivatives(w: float | np.ndarray, phi: float | np.ndarray) -> dict[int, np.ndarray]:
    g = ordered_metric(w, phi)
    dg_w = 2.0 * g
    exp2w = np.exp(2.0 * w)
    cos2phi = np.cos(2.0 * phi)
    dg_phi = np.zeros_like(g)
    dg_phi[1, 3] = 2.0 * exp2w * cos2phi
    dg_phi[3, 1] = dg_phi[1, 3]
    zero = np.zeros_like(g)
    return {0: dg_w, 1: zero, 2: dg_phi, 3: zero}


def christoffel(
    w: float | np.ndarray,
    phi: float | np.ndarray,
    regularization: float,
) -> np.ndarray:
    g_inv = ordered_metric_inverse(w, phi, regularization)
    dgs = metric_derivatives(w, phi)
    gamma = np.zeros((4, 4, 4) + np.shape(np.asarray(w)), dtype=float)
    for i in range(4):
        for j in range(4):
            for k in range(4):
                value = 0.0
                for ell in range(4):
                    value += g_inv[i, ell] * (dgs[j][ell, k] + dgs[k][ell, j] - dgs[ell][j, k])
                gamma[i, j, k] = 0.5 * value
    return gamma


def pullback_eigenvalues(omega: float, phi: float) -> tuple[float, float, float]:
    scale = math.exp(2.0 * omega)
    sin2phi = math.sin(2.0 * phi)
    return (
        float(scale),
        float(scale * (1.0 + sin2phi)),
        float(scale * (1.0 - sin2phi)),
    )


def norm_potential(w: float | np.ndarray, cfg: DirectRuntimeConfig) -> np.ndarray:
    exp2w = np.exp(2.0 * w)
    return 0.5 * cfg.m_glue * cfg.m_glue * exp2w + 0.25 * cfg.lambda_q * exp2w * exp2w


def norm_potential_gradient(w: float | np.ndarray, cfg: DirectRuntimeConfig) -> np.ndarray:
    exp2w = np.exp(2.0 * w)
    grad = np.zeros((4,) + np.shape(exp2w), dtype=float)
    grad[0] = cfg.m_glue * cfg.m_glue * exp2w + cfg.lambda_q * exp2w * exp2w
    return grad


def metric_contract(g: np.ndarray, left: np.ndarray, right: np.ndarray) -> np.ndarray:
    result = np.zeros_like(left[0])
    for i in range(4):
        for j in range(4):
            result += g[i, j] * left[i] * right[j]
    return result


def energy_density(
    fields: np.ndarray,
    velocities: np.ndarray,
    gradients: np.ndarray,
    cfg: DirectRuntimeConfig,
) -> np.ndarray:
    g = ordered_metric(fields[0], fields[2])
    kinetic_t = 0.5 * metric_contract(g, velocities, velocities)
    kinetic_x = np.zeros_like(kinetic_t)
    for axis in range(3):
        kinetic_x += 0.5 * metric_contract(g, gradients[axis], gradients[axis])
    return kinetic_t + kinetic_x + norm_potential(fields[0], cfg)


def first_radius_for_fraction(r: np.ndarray, density: np.ndarray, fraction: float) -> float:
    weight = 4.0 * math.pi * r * r * density
    cumulative = np.zeros_like(weight)
    cumulative[1:] = np.cumsum(0.5 * (weight[1:] + weight[:-1]) * np.diff(r))
    total = cumulative[-1]
    if total <= 0.0:
        return float("nan")
    idx = int(np.searchsorted(cumulative, fraction * total, side="left"))
    idx = min(max(idx, 0), len(r) - 1)
    return float(r[idx])


def radial_stress_terms(
    alpha: np.ndarray,
    alpha_p: np.ndarray,
    r: float,
    mass: float,
    cfg: DirectRuntimeConfig,
) -> tuple[float, float, float, float]:
    a_metric = 1.0 - 2.0 * mass / r
    g = ordered_metric(alpha[0], alpha[2])
    kinetic = float(alpha_p @ g @ alpha_p)
    potential = float(norm_potential(alpha[0], cfg))
    rho = 0.5 * a_metric * kinetic + potential
    p_r = 0.5 * a_metric * kinetic - potential
    p_t = -0.5 * a_metric * kinetic - potential
    trace_t = -rho + p_r + 2.0 * p_t
    ricci = -cfg.kappa * trace_t
    return rho, p_r, p_t, ricci


def radial_rhs(r: float, y: np.ndarray, cfg: DirectRuntimeConfig) -> np.ndarray:
    alpha = y[:4]
    alpha_p = y[4:8]
    mass = y[8]
    a_metric = 1.0 - 2.0 * mass / r
    if a_metric <= cfg.horizon_margin:
        raise FloatingPointError("horizon_or_metric_breakdown")

    rho, p_r, _p_t, ricci = radial_stress_terms(alpha, alpha_p, r, mass, cfg)
    phi_prime = (mass + 4.0 * math.pi * r ** 3 * p_r) / (r * (r - 2.0 * mass))
    m_prime = 4.0 * math.pi * r * r * rho
    a_prime = -2.0 * m_prime / r + 2.0 * mass / (r * r)
    lambda_prime = -a_prime / (2.0 * a_metric)
    damp = 2.0 / r + phi_prime - lambda_prime

    gamma = christoffel(alpha[0], alpha[2], cfg.phi_metric_regularization).squeeze()
    g_inv = ordered_metric_inverse(alpha[0], alpha[2], cfg.phi_metric_regularization).squeeze()
    grad_total = norm_potential_gradient(alpha[0], cfg).squeeze()
    grad_total[0] += -2.0 * cfg.xi * ricci * math.exp(2.0 * alpha[0])
    force = g_inv @ grad_total

    accel = np.zeros(4, dtype=float)
    for i in range(4):
        quad = 0.0
        for j in range(4):
            for k in range(4):
                quad += gamma[i, j, k] * alpha_p[j] * alpha_p[k]
        accel[i] = -damp * alpha_p[i] - quad - force[i] / a_metric

    out = np.zeros_like(y)
    out[:4] = alpha_p
    out[4:8] = accel
    out[8] = m_prime
    out[9] = phi_prime
    return out


def rk4_step(r: float, y: np.ndarray, h: float, cfg: DirectRuntimeConfig) -> np.ndarray:
    k1 = radial_rhs(r, y, cfg)
    k2 = radial_rhs(r + 0.5 * h, y + 0.5 * h * k1, cfg)
    k3 = radial_rhs(r + 0.5 * h, y + 0.5 * h * k2, cfg)
    k4 = radial_rhs(r + h, y + h * k3, cfg)
    return y + (h / 6.0) * (k1 + 2.0 * k2 + 2.0 * k3 + k4)


def solve_direct_radial_profile(seed: OrderedSeed, cfg: DirectRuntimeConfig) -> RadialProfile:
    w0 = math.log(cfg.central_amplitude_base) + seed.omega
    y = np.array([w0, seed.theta, seed.phi, seed.rho, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0], dtype=float)
    rho0, pr0, pt0, ricci0 = radial_stress_terms(y[:4], y[4:8], cfg.r0, y[8], cfg)
    y[8] = (4.0 * math.pi / 3.0) * rho0 * cfg.r0 ** 3

    rs = [cfg.r0]
    ys = [y.copy()]
    rhos = [rho0]
    prs = [pr0]
    pts = [pt0]
    riccis = [ricci0]
    failure_reason = ""
    success = True
    horizon_hit = False

    try:
        r = cfg.r0
        steps = 0
        while r < cfg.r_max and steps < cfg.max_steps:
            if (1.0 - 2.0 * y[8] / r) <= cfg.horizon_margin:
                success = False
                horizon_hit = True
                failure_reason = "horizon_or_metric_breakdown"
                break
            if np.max(np.abs(y[:8])) > cfg.max_abs_state or abs(y[8]) > cfg.max_mass:
                success = False
                failure_reason = "state_or_mass_blowup"
                break
            y = rk4_step(r, y, cfg.dr, cfg)
            r += cfg.dr
            rho_i, pr_i, pt_i, ricci_i = radial_stress_terms(y[:4], y[4:8], r, y[8], cfg)
            rs.append(r)
            ys.append(y.copy())
            rhos.append(rho_i)
            prs.append(pr_i)
            pts.append(pt_i)
            riccis.append(ricci_i)
            steps += 1
        else:
            if steps >= cfg.max_steps:
                success = False
                failure_reason = "step_limit_reached"
    except FloatingPointError as exc:
        success = False
        failure_reason = str(exc)
        horizon_hit = "horizon" in failure_reason
    except (OverflowError, ZeroDivisionError, ValueError, np.linalg.LinAlgError) as exc:
        success = False
        failure_reason = f"numerical_exception:{type(exc).__name__}"

    r_arr = np.asarray(rs, dtype=float)
    y_arr = np.vstack(ys)
    qnorm = np.exp(y_arr[:, 0])
    energy_density_arr = np.asarray(rhos, dtype=float)
    radial_pressure_arr = np.asarray(prs, dtype=float)
    tangential_pressure_arr = np.asarray(pts, dtype=float)
    ricci_arr = np.asarray(riccis, dtype=float)

    return RadialProfile(
        seed=seed,
        r=r_arr,
        y=y_arr,
        qnorm=qnorm,
        energy_density=energy_density_arr,
        radial_pressure=radial_pressure_arr,
        tangential_pressure=tangential_pressure_arr,
        ricci=ricci_arr,
        final_mass=float(y_arr[-1, 8]),
        compactness_90=first_radius_for_fraction(r_arr, np.maximum(energy_density_arr, 0.0), 0.9),
        compactness_half=first_radius_for_fraction(r_arr, np.maximum(energy_density_arr, 0.0), 0.5),
        boundary_qnorm=float(qnorm[-1]),
        boundary_state_prime_norm=float(np.linalg.norm(y_arr[-1, 4:8])),
        success=success,
        failure_reason=failure_reason,
        horizon_hit=horizon_hit,
    )


def default_single_seed_set() -> list[OrderedSeed]:
    return [
        OrderedSeed("scalar", 0.5, 0.0, 0.0, 0.0),
        OrderedSeed("rich", 0.5, math.pi, -0.5 * math.pi, 0.5 * math.pi),
        OrderedSeed("phi_offsheet", 0.5, 0.0, math.pi / 4.0 - 0.1, 0.0),
    ]


def grid_from_config(cfg: DirectRuntimeConfig) -> tuple[np.ndarray, np.ndarray, np.ndarray, np.ndarray]:
    axis = np.linspace(
        -0.5 * (cfg.grid_size - 1) * cfg.dx,
        0.5 * (cfg.grid_size - 1) * cfg.dx,
        cfg.grid_size,
    )
    x, y, z = np.meshgrid(axis, axis, axis, indexing="ij")
    return axis, x, y, z


def radial_interpolant(profile: RadialProfile, radii: np.ndarray) -> np.ndarray:
    flat_r = radii.reshape(-1)
    values = np.empty((4,) + radii.shape, dtype=float)
    for idx in range(4):
        values[idx] = np.interp(flat_r, profile.r, profile.y[:, idx]).reshape(radii.shape)
    return values


def embed_profile_on_grid(
    profile: RadialProfile,
    x: np.ndarray,
    y: np.ndarray,
    z: np.ndarray,
    *,
    center: tuple[float, float, float] = (0.0, 0.0, 0.0),
    ambient: np.ndarray | None = None,
) -> np.ndarray:
    if ambient is None:
        ambient = profile.y[-1, :4]
    radii = np.sqrt((x - center[0]) ** 2 + (y - center[1]) ** 2 + (z - center[2]) ** 2)
    embedded = radial_interpolant(profile, radii)
    fields = ambient[:, None, None, None] + (embedded - ambient[:, None, None, None])
    return fields


def superpose_profiles_on_grid(
    profiles: Iterable[tuple[RadialProfile, tuple[float, float, float]]],
    x: np.ndarray,
    y: np.ndarray,
    z: np.ndarray,
    *,
    ambient: np.ndarray,
) -> np.ndarray:
    fields = ambient[:, None, None, None] * np.ones((4,) + x.shape, dtype=float)
    for profile, center in profiles:
        embedded = embed_profile_on_grid(profile, x, y, z, center=center, ambient=ambient)
        fields += embedded - ambient[:, None, None, None]
    return fields


def edge_padded(field: np.ndarray) -> np.ndarray:
    return np.pad(field, 1, mode="edge")


def laplacian(field: np.ndarray, dx: float) -> np.ndarray:
    padded = edge_padded(field)
    return (
        padded[2:, 1:-1, 1:-1]
        + padded[:-2, 1:-1, 1:-1]
        + padded[1:-1, 2:, 1:-1]
        + padded[1:-1, :-2, 1:-1]
        + padded[1:-1, 1:-1, 2:]
        + padded[1:-1, 1:-1, :-2]
        - 6.0 * padded[1:-1, 1:-1, 1:-1]
    ) / (dx * dx)


def gradient_components(field: np.ndarray, dx: float) -> np.ndarray:
    padded = edge_padded(field)
    gx = (padded[2:, 1:-1, 1:-1] - padded[:-2, 1:-1, 1:-1]) / (2.0 * dx)
    gy = (padded[1:-1, 2:, 1:-1] - padded[1:-1, :-2, 1:-1]) / (2.0 * dx)
    gz = (padded[1:-1, 1:-1, 2:] - padded[1:-1, 1:-1, :-2]) / (2.0 * dx)
    return np.stack([gx, gy, gz], axis=0)


def field_gradients(fields: np.ndarray, dx: float) -> np.ndarray:
    return np.stack([gradient_components(fields[idx], dx) for idx in range(4)], axis=1)


def acceleration(fields: np.ndarray, velocities: np.ndarray, cfg: DirectRuntimeConfig) -> np.ndarray:
    laps = np.stack([laplacian(fields[idx], cfg.dx) for idx in range(4)], axis=0)
    grads = field_gradients(fields, cfg.dx)
    gamma = christoffel(fields[0], fields[2], cfg.phi_metric_regularization)
    force = np.zeros_like(fields)
    force[0] = cfg.m_glue * cfg.m_glue + cfg.lambda_q * np.exp(2.0 * fields[0])

    contractions = np.zeros((4, 4) + fields.shape[1:], dtype=float)
    for j in range(4):
        for k in range(4):
            space_dot = np.sum(grads[:, j] * grads[:, k], axis=0)
            contractions[j, k] = velocities[j] * velocities[k] - space_dot

    accel = laps - force
    for i in range(4):
        conn = np.zeros_like(fields[0])
        for j in range(4):
            for k in range(4):
                conn += gamma[i, j, k] * contractions[j, k]
        accel[i] += conn
    return accel


def compute_compact_radius(weight: np.ndarray, x: np.ndarray, y: np.ndarray, z: np.ndarray, fraction: float) -> float:
    total = float(np.sum(weight))
    if total <= 0.0:
        return float("nan")
    cx = float(np.sum(weight * x) / total)
    cy = float(np.sum(weight * y) / total)
    cz = float(np.sum(weight * z) / total)
    radii = np.sqrt((x - cx) ** 2 + (y - cy) ** 2 + (z - cz) ** 2).reshape(-1)
    weights = weight.reshape(-1)
    order = np.argsort(radii)
    cumulative = np.cumsum(weights[order])
    idx = int(np.searchsorted(cumulative, fraction * total, side="left"))
    idx = min(max(idx, 0), len(order) - 1)
    return float(radii[order[idx]])


def diagnostics(
    fields: np.ndarray,
    velocities: np.ndarray,
    x: np.ndarray,
    y: np.ndarray,
    z: np.ndarray,
    cfg: DirectRuntimeConfig,
) -> dict[str, float]:
    grads = field_gradients(fields, cfg.dx)
    rho = energy_density(fields, velocities, grads, cfg)
    weight = np.exp(2.0 * fields[0])
    total_weight = float(np.sum(weight))
    centroid_x = float(np.sum(weight * x) / total_weight) if total_weight > 0.0 else float("nan")
    centroid_y = float(np.sum(weight * y) / total_weight) if total_weight > 0.0 else float("nan")
    centroid_z = float(np.sum(weight * z) / total_weight) if total_weight > 0.0 else float("nan")
    return {
        "total_energy": float(np.sum(rho) * cfg.dx ** 3),
        "peak_qnorm": float(np.exp(fields[0]).max()),
        "centroid_x": centroid_x,
        "centroid_y": centroid_y,
        "centroid_z": centroid_z,
        "compact_radius_half": compute_compact_radius(weight, x, y, z, 0.5),
        "compact_radius_90": compute_compact_radius(weight, x, y, z, 0.9),
        "chirality_integral": float(np.sum(weight * np.cos(2.0 * fields[2])) * cfg.dx ** 3),
        "weight_integral": float(total_weight * cfg.dx ** 3),
    }


class OrderedManifoldWaveSolver:
    def __init__(self, cfg: DirectRuntimeConfig):
        self.cfg = cfg
        self.axis, self.x, self.y, self.z = grid_from_config(cfg)

    def evolve(
        self,
        fields0: np.ndarray,
        velocities0: np.ndarray | None = None,
        *,
        steps: int | None = None,
        sample_every: int = 1,
    ) -> tuple[np.ndarray, np.ndarray, list[dict[str, float]]]:
        if velocities0 is None:
            velocities0 = np.zeros_like(fields0)
        fields = fields0.copy()
        velocities = velocities0.copy()
        accel = acceleration(fields, velocities, self.cfg)
        history: list[dict[str, float]] = []
        total_steps = self.cfg.time_steps if steps is None else int(steps)

        for step in range(total_steps + 1):
            if step % sample_every == 0:
                row = {"step": float(step), "time": float(step * self.cfg.dt)}
                row.update(diagnostics(fields, velocities, self.x, self.y, self.z, self.cfg))
                history.append(row)
            if step == total_steps:
                break
            fields_next = fields + self.cfg.dt * velocities + 0.5 * self.cfg.dt * self.cfg.dt * accel
            accel_next = acceleration(fields_next, velocities, self.cfg)
            velocities_next = velocities + 0.5 * self.cfg.dt * (accel + accel_next)
            fields, velocities, accel = fields_next, velocities_next, accel_next
        return fields, velocities, history

    def translational_boost(self, fields: np.ndarray, speed: float, axis: int = 0) -> np.ndarray:
        grads = field_gradients(fields, self.cfg.dx)
        return -float(speed) * grads[axis]


def interaction_energy_density(
    total_fields: np.ndarray,
    left_fields: np.ndarray,
    right_fields: np.ndarray,
    ambient_fields: np.ndarray,
    cfg: DirectRuntimeConfig,
) -> np.ndarray:
    zeros = np.zeros_like(total_fields)
    total_grads = field_gradients(total_fields, cfg.dx)
    left_grads = field_gradients(left_fields, cfg.dx)
    right_grads = field_gradients(right_fields, cfg.dx)
    ambient_grads = field_gradients(ambient_fields, cfg.dx)
    rho_total = energy_density(total_fields, zeros, total_grads, cfg)
    rho_left = energy_density(left_fields, zeros, left_grads, cfg)
    rho_right = energy_density(right_fields, zeros, right_grads, cfg)
    rho_ambient = energy_density(ambient_fields, zeros, ambient_grads, cfg)
    return rho_total - rho_left - rho_right + rho_ambient
