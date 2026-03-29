# Derivation 72: Phase A Jacobian Singularity Structure for the Ordered Quaternion Map

**Date:** 2026-03-28  
**Purpose:** Re-do the second Phase A substep using the active domain convention:
- \(\omega>0\)
- \(\theta,\phi,\rho \in [-2\pi,2\pi]\)
- no redundancy quotienting

---

## 1. Active map

The active ordered map is
\[
Q(\omega,\theta,\phi,\rho)=e^{\omega}e^{\theta i}e^{\phi j}e^{\rho k}.
\]

Write
\[
Q = x_0 + x_1 i + x_2 j + x_3 k,
\]
with
\[
x_\mu = e^{\omega} y_\mu(\theta,\phi,\rho).
\]

The Jacobian is
\[
J = \frac{\partial x}{\partial(\omega,\theta,\phi,\rho)}.
\]

---

## 2. Scale separation still holds

Because every component carries the same factor \(e^{\omega}\), each Jacobian column carries one overall \(e^{\omega}\) factor. Therefore
\[
\det J = e^{4\omega}\det J_{\mathrm{ang}}.
\]

So even on the widened working domain, the location of singular slices is governed entirely by the angular part.

---

## 3. Determinant structure on the active domain

The re-done scan over the active domain strongly supports
\[
\det J = e^{4\omega}\cos(2\phi).
\]

This is not merely a small-box statement. It remains valid across the explicit wider angle box
\[
\theta,\phi,\rho \in [-2\pi,2\pi],
\qquad
\omega>0,
\]
with no attempt made to quotient redundant angle descriptions.

So the determinant magnitude scales with \(\omega\), while the singular geometry itself depends only on \(\phi\).

---

## 4. Singular condition in the active domain

The singular condition is therefore
\[
\cos(2\phi)=0.
\]
Equivalently,
\[
\phi = \frac{\pi}{4}+\frac{n\pi}{2}, \qquad n\in\mathbb Z.
\]

Within the active working box \([-2\pi,2\pi]\), this gives the explicit singular \(\phi\)-slices:
\[
\phi \in \left\{-\frac{7\pi}{4},-\frac{5\pi}{4},-\frac{3\pi}{4},-\frac{\pi}{4},
\frac{\pi}{4},\frac{3\pi}{4},\frac{5\pi}{4},\frac{7\pi}{4}\right\}.
\]

So the wider domain does not change the singular rule. It reveals repeated singular sheets across multiple periods.

---

## 5. Interpretation

This matters for Phase A in a very specific way.

1. **\(\omega\)** remains a pure positive scale coordinate in the current convention.
2. **\(\phi\)** controls the chart-singularity architecture.
3. **\(\theta\)** and **\(\rho\)** remain locally independent away from the singular \(\phi\)-slices, but can collapse into local collinearity on those slices.
4. The repeated singular sheets in the larger angle box are not new physics by themselves; they are repeated manifestations of the same ordered-chart structure.

---

## 6. Important caution

Because the user explicitly wants the full box explored instead of quotienting redundancies, Phase A should presently treat these repeated singular sheets as part of the active computational landscape.

But interpretively, one should still distinguish between:
- repeated chart structure due to periodicity,
- and genuinely new physical trait structure.

The present derivation establishes only the first.

---

## 7. Bottom line

**Bottom line:** on the active domain
\[
\omega>0,
\qquad
\theta,\phi,\rho\in[-2\pi,2\pi],
\]
the ordered quaternion map has Jacobian determinant
\[
\det J = e^{4\omega}\cos(2\phi),
\]
so the singular slices occur exactly at
\[
\phi=\frac{\pi}{4}+\frac{n\pi}{2}.
\]
The larger box does not alter the fundamental singular law; it reveals its repeated-sheet structure across the full working angle domain.
