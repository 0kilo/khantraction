# Derivation 74: Provisional Phase B Einstein Closure, Boundary Data, and Observable Formulas

**Date:** 2026-03-28  
**Purpose:** Record the strongest honest Einstein-sector / boundary-condition / observable reconstruction currently supportable for the fresh-tree Phase B full radial runtime.

---

## 1. Scope and honesty condition

The active tree still does **not** contain a full explicit derivation of the Einstein equations for the nonminimal coupling term

$$
\xi R |q|^2.
$$

So this note does **not** claim that the following closure is the final exact field-theory reduction.
Instead it records the provisional closure used by the new runtime and explains why that choice is currently the tightest explicit reconstruction the active materials support.

---

## 2. Matter-side equations inherited from Derivation 73

The four-component radial matter system already reconstructed in Derivation 73 is

$$
q_A''+\left(\frac{2}{r}+\Phi'-\Lambda'\right)q_A' + e^{2\Lambda}\Big(m_{\mathrm{glue}}^2+\lambda_q|q|^2-2\xi R\Big)q_A=0,
$$

for $q_A\in\{a,b,c,d\}$ and

$$
|q|^2=a^2+b^2+c^2+d^2.
$$

With

$$
A(r)=e^{-2\Lambda(r)} = 1-\frac{2m(r)}{r},
$$

one may also write

$$
\Lambda' = -\frac{A'}{2A},
\qquad
A' = -\frac{2m'}{r}+\frac{2m}{r^2}.
$$

So the matter equations become

$$
q_A''+\left(\frac{2}{r}+\Phi'+\frac{A'}{2A}\right)q_A' + \frac{1}{A}\Big(m_{\mathrm{glue}}^2+\lambda_q|q|^2-2\xi R\Big)q_A=0.
$$

---

## 3. Provisional Einstein closure used in the runtime

Because the exact nonminimal-coupling Einstein reduction is still absent, the runtime adopts the standard static scalar-multiplet stress reconstruction as the leading closure model.

Let

$$
q_A'=\frac{dq_A}{dr},
\qquad
|q'|^2 = a'^2+b'^2+c'^2+d'^2,
\qquad
V(|q|)=\frac{m_{\mathrm{glue}}^2}{2}|q|^2 + \frac{\lambda_q}{4}|q|^4.
$$

Then the provisional stress components are taken as

$$
\rho = \frac{1}{2}A|q'|^2 + V,
$$

$$
p_r = \frac{1}{2}A|q'|^2 - V,
$$

$$
p_t = -\frac{1}{2}A|q'|^2 - V.
$$

This gives the standard Misner–Sharp closures

$$
m' = 4\pi r^2 \rho,
$$

$$
\Phi' = \frac{m + 4\pi r^3 p_r}{r(r-2m)}.
$$

---

## 4. Ricci reconstruction used in the runtime

The runtime then estimates the Ricci scalar through the Einstein trace law

$$
R = -\kappa T,
$$

with

$$
T = -\rho + p_r + 2p_t.
$$

For the provisional stress model above,

$$
T = -A|q'|^2 - 4V.
$$

Hence

$$
R = \kappa\Big(A|q'|^2 + 4V\Big).
$$

In the present runtime,

$$
\kappa = 8\pi.
$$

So the matter operator effectively uses

$$
m_{\mathrm{eff}}^2(r)=m_{\mathrm{glue}}^2 + \lambda_q |q|^2 - 2\xi R(r),
$$

with $R$ supplied by the provisional trace closure above.

---

## 5. Why this is still provisional

This closure is useful and standard-looking, but it is still provisional for two reasons.

### 5.1 Nonminimal coupling is not fully re-derived

The term $\xi R|q|^2$ generally modifies the Einstein equations directly, not only the matter equation through an effective Ricci-dependent mass.
So a fully faithful reduction would usually contain additional curvature-side and derivative-coupling contributions.
Those terms are not yet derived in the fresh tree.

### 5.2 Conventions are not uniquely fixed in the paper text

The paper gives the toy-model action and matter equations but does not fully pin down:
- the gravitational normalization,
- the exact stress-tensor sign conventions in the full reduced system,
- or how the nonminimal term is partitioned between matter and geometry in the reduced ODE closure.

So the present closure is best understood as:

> the strongest explicit solver-usable Einstein reconstruction currently available from the active materials, not the final uniquely derived closure.

---

## 6. Regular-origin boundary data reconstruction

The fresh tree does not yet contain a full matched BVP prescription.
So the runtime uses regular-origin IVP data.

At a small radius $r_0\ll 1$, impose

$$
q_A'(r_0)=0
$$

for all four components to enforce leading regularity.

Take

$$
\Phi(r_0)=0
$$

as a gauge choice.

Then initialize the mass from the local density,

$$
m(r_0) \approx \frac{4\pi}{3}\rho(r_0) r_0^3.
$$

This is the standard local regularity-compatible small-$r$ start used by the runtime.

---

## 7. Ordered-state seed-to-component map used at the origin

The active ordered-state map is

$$
Q(\omega,\theta,\phi,\rho)=e^{\omega}e^{\theta i}e^{\phi j}e^{\rho k}.
$$

Let its components be

$$
Q = q_0 + q_1 i + q_2 j + q_3 k.
$$

Since $|Q|=e^{\omega}$, the runtime separates:
- ordered-state **direction** $\hat q_A = q_A/|Q|$,
- from central amplitude scaling.

Then the reconstructed origin data are

$$
q_A(r_0)=A_0 e^{\omega}\hat q_A(\theta,\phi,\rho),
$$

with

$$
A_0 = 0.02
$$

in the current runtime.

This choice is anchored to the earlier reduced successful profile scale quoted in `khantraction_paper.md`, where the successful regular-origin scalar amplitude was of order `0.02`.
So the runtime uses:
- $\omega$ to modulate the central scale,
- $(\theta,\phi,\rho)$ to set the component direction,
- and the small amplitude base to keep the integration in the same regular-origin regime as the earlier documented reduced success.

---

## 8. Continuation setup reconstructed for Phase B

The runtime implements three seed classes.

### 8.1 Ordered continuation path
A direct linear path in ordered variables between:
- a scalar-like anchor,
- and the historically emphasized rich ordered anchor
  $(\pi,-\pi/2,+\pi/2)$
  at positive $\omega$.

This is not claimed to be the unique physical continuation parameterization.
It is the explicit reproducible continuation hook used to test broad family behavior.

### 8.2 Rich-sector neighborhood probes
Small offsets around the rich ordered anchor test whether the runtime remains regular in the neighborhood of the locked sector.

### 8.3 Coarse active-box scan
A broad coarse grid over positive $\omega$ and representative angle values provides a first physical runtime sweep over the active domain.

---

## 9. Observable formulas used in the runtime

These observables are implemented as explicit extraction formulas.
They should currently be interpreted as closure-dependent diagnostics.

### 9.1 Final mass

$$
M_{\mathrm{final}} = m(r_{\max}).
$$

### 9.2 Integrated curvature magnitude

$$
\mathcal I_R = \int_{r_0}^{r_{\max}} |R(r)|\,dr.
$$

### 9.3 Mass concentration radii
Using the provisional energy density,

$$
W_M(r)=4\pi r^2 \rho(r),
$$

let

$$
C_M(r)=\int_{r_0}^{r} W_M(\tilde r)\,d\tilde r.
$$

Then:
- mass half-radius: first $r$ with $C_M(r)\ge \tfrac12 C_M(r_{\max})$
- mass 90% radius: first $r$ with $C_M(r)\ge 0.9 C_M(r_{\max})$

### 9.4 Curvature concentration radii
Using

$$
W_R(r)=4\pi r^2 |R(r)|,
$$

let

$$
C_R(r)=\int_{r_0}^{r} W_R(\tilde r)\,d\tilde r.
$$

Then define half and 90% radii analogously.

### 9.5 Settling radius
The first radius at which

$$
|q(r)| \le \max\big(\text{decay target}, 0.05\,|q|_{\max}\big)
$$

within the sampled domain.

### 9.6 Core radius
The last radius where

$$
|q(r)| \ge 0.9\,|q|_{\max}.
$$

### 9.7 Soft-region width
The radial width of the region where

$$
|q(r)| \ge 0.2\,|q|_{\max}.
$$

### 9.8 Peak imaginary-to-real ratio

$$
\max_r \frac{\sqrt{b(r)^2+c(r)^2+d(r)^2}}{\max(|a(r)|,\epsilon)}
$$

with a small $\epsilon$ floor in code to avoid division by zero.

---

## 10. What this derivation now accomplishes

This note does not solve the nonminimal Einstein-sector ambiguity.
But it does convert the old vague blockage into a precise explicit statement:

- the matter-side equations are known,
- a concrete provisional Einstein closure is now written down,
- regular-origin data are specified,
- continuation hooks are specified,
- observable formulas are specified,
- and every one of those choices is explicitly labeled provisional where the active tree does not yet justify uniqueness.

That is enough to support a real Phase B runtime without pretending the derivation is complete.

---

## 11. Bottom line

**Bottom line:** the current fresh-tree Phase B runtime closes the four-component matter equations with a provisional static scalar-multiplet Einstein reconstruction, regular-origin IVP data, ordered-state directional seeding, and explicit concentration/curvature observables. This is a real and usable solver-level closure, but it remains provisional until the full nonminimal-coupling Einstein sector for $\xi R|q|^2$ is derived explicitly in the fresh tree.
