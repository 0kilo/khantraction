# Derivation 73: Fresh-Start Full Four-Component Radial System for Khantraction

**Date:** 2026-03-28  
**Purpose:** Reconstruct the active full four-component radial field equations in the fresh tree as the next required prerequisite for Phase B physical branch viability.

---

## 1. Why this derivation is now necessary

Phase B has reached the point where ordered-state viability has been rebuilt, but physical branch viability is still blocked.

The missing ingredient is not more seed scanning.
It is the actual full radial dynamical system for the quaternion-valued glue field.

So this note begins the honest reconstruction of that system from the toy-model Lagrangian stated in `khantraction_paper.md`.

---

## 2. Starting point: toy-model Lagrangian

The paper states the toy-model matter sector as
\[
\mathcal L=\sqrt{-g}\left[\tfrac{1}{2}g^{\mu\nu}(\partial_\mu s\partial_\nu s+\partial_\mu\vec v\!\cdot\!\partial_\nu\vec v)-U(|q|)+\xi R|q|^2\right]-\sqrt{-g}\left[\tfrac{1}{4}F_{\mu\nu}F^{\mu\nu}+\lambda|q|^2F_{\mu\nu}F^{\mu\nu}\right],
\]
with
\[
q=s+\vec v\cdot\vec\tau,
\qquad
|q|^2=s^2+\vec v\cdot\vec v,
\]
and potential
\[
U(|q|)=\tfrac{m_{\mathrm{glue}}^2}{2}|q|^2+\tfrac{\lambda_q}{4}|q|^4.
\]

For the fresh-start radial reconstruction we suppress the electromagnetic sector unless later notes require it explicitly, because the current branch-family discussion has been framed around the norm-based quaternion glue itself.

So the working action is
\[
S_q=\int d^4x\,\sqrt{-g}\left[\tfrac{1}{2}g^{\mu\nu}\partial_\mu q_A\partial_\nu q_A-U(|q|)+\xi R |q|^2\right],
\]
where
\[
q_A=(a,b,c,d),
\qquad
|q|^2=a^2+b^2+c^2+d^2.
\]

---

## 3. Full four-component field equations before symmetry reduction

Varying with respect to each component \(q_A\) gives
\[
\Box q_A + \frac{\partial U}{\partial q_A} - 2\xi R q_A = 0,
\]
with
\[
\frac{\partial U}{\partial q_A} = \left(m_{\mathrm{glue}}^2+\lambda_q |q|^2\right) q_A.
\]

So the component equations are
\[
\Box q_A + \left(m_{\mathrm{glue}}^2+\lambda_q |q|^2\right)q_A - 2\xi R q_A = 0.
\]

Equivalently,
\[
\Box q_A + \Big(m_{\mathrm{glue}}^2+\lambda_q(a^2+b^2+c^2+d^2)-2\xi R\Big)q_A = 0.
\]

This already shows an important fact:

> in the current norm-based toy model, all four components obey the same scalar-type radial operator, coupled only through the shared norm and the curvature scalar.

That is the fresh-start full multiplet system.

---

## 4. Static spherical reduction

Use the static spherically symmetric metric
\[
ds^2=-e^{2\Phi(r)}dt^2+e^{2\Lambda(r)}dr^2+r^2d\Omega^2,
\qquad
e^{-2\Lambda}=1-\frac{2m(r)}{r}.
\]

Assume the four components depend only on \(r\):
\[
a=a(r),\quad b=b(r),\quad c=c(r),\quad d=d(r).
\]

Then for any radial scalar-like field \(f(r)\),
\[
\Box f = e^{-2\Lambda}\left[f''+\left(\frac{2}{r}+\Phi'-\Lambda'\right)f'\right].
\]

Therefore each quaternion component obeys
\[
e^{-2\Lambda}\left[q_A''+\left(\frac{2}{r}+\Phi'-\Lambda'\right)q_A'\right]
+\Big(m_{\mathrm{glue}}^2+\lambda_q|q|^2-2\xi R\Big)q_A=0.
\]

Multiplying by \(e^{2\Lambda}\) gives the radial ODE form
\[
q_A''+\left(\frac{2}{r}+\Phi'-\Lambda'\right)q_A'
+e^{2\Lambda}\Big(m_{\mathrm{glue}}^2+\lambda_q|q|^2-2\xi R\Big)q_A=0.
\]

So explicitly,
\[
a''+\left(\frac{2}{r}+\Phi'-\Lambda'\right)a' + e^{2\Lambda}\Big(m_{\mathrm{glue}}^2+\lambda_q|q|^2-2\xi R\Big)a=0,
\]
\[
b''+\left(\frac{2}{r}+\Phi'-\Lambda'\right)b' + e^{2\Lambda}\Big(m_{\mathrm{glue}}^2+\lambda_q|q|^2-2\xi R\Big)b=0,
\]
\[
c''+\left(\frac{2}{r}+\Phi'-\Lambda'\right)c' + e^{2\Lambda}\Big(m_{\mathrm{glue}}^2+\lambda_q|q|^2-2\xi R\Big)c=0,
\]
\[
d''+\left(\frac{2}{r}+\Phi'-\Lambda'\right)d' + e^{2\Lambda}\Big(m_{\mathrm{glue}}^2+\lambda_q|q|^2-2\xi R\Big)d=0,
\]
with
\[
|q|^2=a^2+b^2+c^2+d^2.
\]

---

## 5. What this derivation *does* establish

This gives the fresh tree its first explicit full four-component radial matter equations.

That is already a real improvement over the previous blocked status, because the active tree can now stop saying only “the equations are missing.”
At least the matter-side multiplet equations are now written clearly.

---

## 6. What still remains missing

However, this derivation does **not** yet complete the full trustworthy solver system.
Several essential ingredients are still absent or incomplete.

### 6.1 Einstein-sector closure

The metric functions \(m(r)\), \(\Phi(r)\), and the curvature scalar \(R(r)\) still require explicit closure from the stress-energy tensor of the full norm-based four-component model.

### 6.2 Explicit expression for \(R\)

The reduced paper equations invoke \(R\), but the fresh tree still needs either:
- an explicit formula for \(R\) in terms of \(m,\Phi\) and their derivatives,
- or a fully reduced Einstein equation system from which \(R\) can be eliminated consistently.

### 6.3 Boundary conditions

A trustworthy radial solver still needs regular-origin and asymptotic boundary conditions for:
- \(a,b,c,d\),
- \(m\),
- \(\Phi\),
- and any continuation parameterization.

### 6.4 Observable formulas

Phase B objecthood work still needs physical extraction formulas for:
- mass profile,
- curvature profile,
- core radius,
- soft-region width,
- and settling radius.

---

## 7. Immediate structural interpretation

Even before full closure, this derivation makes the model’s current architecture very clear.

The full four-component radial toy model is:
- **component-symmetric** in the matter operator,
- **norm-coupled** through \(|q|^2\),
- and **geometry-coupled** through \(R\), \(\Phi\), and \(\Lambda\).

So any asymmetry among the internal ordered variables \((\theta,\phi,\rho)\) is not coming from unequal bare component equations here.
It must arise from:
- the ordered parameter embedding into component space,
- the nonlinear norm coupling,
- the metric closure,
- boundary conditions,
- and solution-family selection.

That is conceptually important for later Phase B and Phase C interpretation.

---

## 8. Active domain convention

The current project convention remains:
- \(\omega>0\)
- \(\theta,\phi,\rho\in[-2\pi,2\pi]\)
- no redundancy quotienting

That convention belongs to the ordered-state scan and seeding layer.
The radial ODE system itself is written directly in \((a,b,c,d)\) component variables, but later fresh-tree runtime code should preserve the active ordered-angle seeding convention when mapping seeds into component initial data.

---

## 9. Bottom line

**Bottom line:** the fresh tree now has an explicit full four-component radial matter system for the norm-based quaternion glue field:
\[
q_A''+\left(\frac{2}{r}+\Phi'-\Lambda'\right)q_A' + e^{2\Lambda}\Big(m_{\mathrm{glue}}^2+\lambda_q|q|^2-2\xi R\Big)q_A=0,
\]
for \(q_A\in\{a,b,c,d\}\) and \(|q|^2=a^2+b^2+c^2+d^2\).
This removes one major blockage. But a trustworthy Phase B physical branch solver still requires the Einstein-sector closure, boundary conditions, continuation setup, and observable-extraction formulas to be written down explicitly in the fresh tree.
