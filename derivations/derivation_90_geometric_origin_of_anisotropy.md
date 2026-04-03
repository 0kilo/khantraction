# Derivation 90: Geometry-Level Origin of Pullback Anisotropy in the Ordered Quaternionic Map

**Date:** 2026-03-31  
**Phase:** I — First-Principles Derivation of Constants  
**Status:** Audit-refreshed geometry derivation

## 1. Purpose

The Phase I question from `notes/real_physics_transition_plan.md` is whether the ordered quaternionic state map already contains a native mechanism that distinguishes internal angular channels, rather than requiring hand-inserted anisotropy coefficients.

This derivation addresses that question at the **geometry level** only.

It does **not** by itself:

- replace the exploratory `beta_a` coefficients in the active dynamical solver chain,
- derive a spontaneous-symmetry-breaking potential,
- or map the resulting geometric quantities to physical observables.

What it does establish is the exact angular pullback metric and its eigenstructure.

## 2. Ordered pullback metric

The ordered quaternionic state map is

$$
Q(\omega,\theta,\phi,\rho)=e^{\omega}e^{\theta i}e^{\phi j}e^{\rho k}.
$$

Using the Jacobian from `derivations/derivation_71_exponential_quaternion_parameter_mapping_clean.md` and the pullback construction summarized in `derivations/derivation_75_ordered_pullback_and_exploratory_directional_phase_b_runtime.md`, the exact pullback metric is

$$
G = e^{2\omega}
\begin{pmatrix}
1 & 0 & 0 & 0 \\
0 & 1 & 0 & \sin(2\phi) \\
0 & 0 & 1 & 0 \\
0 & \sin(2\phi) & 0 & 1
\end{pmatrix},
$$

in the coordinate basis $(\omega,\theta,\phi,\rho)$.

The angular block is therefore

$$
G_{\rm ang}=e^{2\omega}
\begin{pmatrix}
1 & 0 & \sin(2\phi) \\
0 & 1 & 0 \\
\sin(2\phi) & 0 & 1
\end{pmatrix}.
$$

So the kinetic density carried by the ordered coordinates is

$$
\alpha'^T G \alpha'
=
e^{2\omega}\Big(
\omega'^2+\theta'^2+\phi'^2+\rho'^2+2\sin(2\phi)\theta'\rho'
\Big).
$$

## 3. Eigenvalue decomposition

The angular eigenmodes are:

1. the orthogonal `phi` direction,
2. the symmetric `theta + rho` direction,
3. the antisymmetric `theta - rho` direction.

Their exact eigenvalues are

$$
\lambda_\phi = e^{2\omega},
\qquad
\lambda_+ = e^{2\omega}\big(1+\sin(2\phi)\big),
\qquad
\lambda_- = e^{2\omega}\big(1-\sin(2\phi)\big).
$$

So:

- `phi` keeps a constant stiffness at fixed `omega`,
- `phi` alone redistributes stiffness between the paired `theta-rho` modes,
- and the paired subsystem is isotropic only when `\sin(2\phi)=0`, i.e. `\phi = n\pi/2`.

## 4. Exact soft-sheet families

The two paired-mode eigenvalues do **not** vanish on the same singular sheets.

They vanish on alternating families:

$$
\lambda_+ = 0
\quad\Longleftrightarrow\quad
\sin(2\phi)=-1
\quad\Longleftrightarrow\quad
\phi=-\frac{\pi}{4}+n\pi,
$$

$$
\lambda_- = 0
\quad\Longleftrightarrow\quad
\sin(2\phi)=+1
\quad\Longleftrightarrow\quad
\phi=\frac{\pi}{4}+n\pi.
$$

Inside the active domain `[-2pi, 2pi]`, these become:

- `lambda_+ = 0` on `{-5pi/4, -pi/4, 3pi/4, 7pi/4}`,
- `lambda_- = 0` on `{-7pi/4, -3pi/4, pi/4, 5pi/4}`.

These are exactly the alternating singular-sheet families already visible in the Phase A determinant law

$$
\det J = e^{4\omega}\cos(2\phi),
$$

because the paired-mode degeneracy occurs whenever `cos(2phi)=0`.

## 5. What this geometry does prove

This derivation proves a narrower but still important result:

- the ordered map contains a native `phi`-controlled anisotropy in its pullback geometry,
- the `theta-rho` pair is the only sector whose relative stiffness is redistributed,
- and the singular-sheet architecture corresponds to exact softening of alternating paired modes.

So the ordered map does provide a genuine **candidate geometric origin** for later anisotropy constructions.

## 6. What this geometry does not yet prove

This derivation does **not** prove:

- that the active Phase C to H exploratory `beta_a` coefficients have already been replaced in the actual solver chain,
- that the geometry alone generates the full symmetry-breaking dynamics used in the exploratory runtime,
- that exact self-coupling limits for stable branches have been derived,
- or that quantities like a mass gap or fine-structure analog have already been mapped to observables.

Those stronger claims require additional derivation and implementation beyond this pullback scan.

## 7. Bottom line

**Bottom line:** the ordered quaternionic state map carries an exact, `phi`-controlled pullback anisotropy. At fixed `omega`, `lambda_\phi` is constant while the paired `theta-rho` modes split as `\lambda_\pm = e^{2\omega}(1 \pm \sin(2\phi))`, with alternating singular-sheet families where either the symmetric or antisymmetric mode softens to zero. This is a real geometry-level anisotropy mechanism, but it is not yet a full first-principles replacement for the exploratory constants used in the active solver chain.
