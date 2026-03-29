# Derivation 75: Ordered Pullback Runtime and Exploratory Directional Phase B Upgrade

**Date:** 2026-03-28  
**Purpose:** Build the most honest next Phase B runtime upgrade currently supported by the project materials, specifically to reduce the near-total angular degeneracy seen in the component-norm solver while keeping baseline and exploratory pieces sharply separated.

---

## 1. Why an upgrade is needed

The current Phase B full radial solver is real and useful, but the stress test showed a severe limitation:

- at fixed `omega = 0.5`, the rich-neighborhood seeds had final-mass spread only about
  \[
  7.49\times 10^{-16},
  \]
- and integrated-`|R|` spread only about
  \[
  3.30\times 10^{-17}.
  \]

So the present runtime is almost completely degenerate across rich angular neighborhoods.

That is not surprising, because the active matter equations from Derivation 73 are component-symmetric and norm-coupled:
\[
q_A'' + \Big(\cdots\Big) q_A' + \frac{1}{A}\Big(m_{\rm glue}^2 + \lambda_q |q|^2 - 2\xi R\Big) q_A = 0.
\]
All angle dependence enters only through the seed-to-component embedding, and once the evolution is written purely in terms of `|q|^2`, many angular distinctions collapse.

So if the project wants to see whether angular-sector differences can ever appear honestly, the next step cannot just be “more of the same component-norm runtime.”
It has to use the ordered-state geometry already derived in Phase A.

---

## 2. Ordered coordinates as the natural next runtime variables

The active ordered map is
\[
Q(\omega,\theta,\phi,\rho)=e^{\omega}e^{\theta i}e^{\phi j}e^{\rho k}.
\]

Derivation 71 gave the component map and Jacobian.
The project’s Phase A geometry work already found two especially important facts:

1. the Jacobian determinant depends on `phi` through
   \[
   \det J = e^{4\omega}\cos(2\phi),
   \]
2. the angular tangent structure is not fully isotropic: `phi` controls the mixing relation between the `theta` and `rho` directions.

So the natural next move is to pull the component-space kinetic term back into ordered coordinates.

---

## 3. Pullback metric induced by the ordered map

Write the ordered coordinates as
\[
\alpha^i = (w,\theta,\phi,\rho),
\]
where in the runtime
\[
w = \log(A_0)+\omega
\]
so that the central norm remains anchored to the previously used small-amplitude Phase B scale
\[
|Q| = e^w = A_0 e^{\omega},
\qquad A_0 = 0.02.
\]

Using the Jacobian from Derivation 71, the pullback metric
\[
G_{ij} = \partial_i Q_A\,\partial_j Q_A
\]
becomes
\[
G = e^{2w}
\begin{pmatrix}
1 & 0 & 0 & 0 \\
0 & 1 & 0 & \sin(2\phi) \\
0 & 0 & 1 & 0 \\
0 & \sin(2\phi) & 0 & 1
\end{pmatrix}.
\]

So the ordered kinetic density is
\[
|Q'|^2
= \alpha'^T G \alpha'
= e^{2w}\Big(w'^2 + \theta'^2 + \phi'^2 + \rho'^2 + 2\sin(2\phi)\,\theta'\rho'\Big).
\]

This is already a genuine directional refinement relative to the component runtime, because the angular geometry is not just a flat isotropic Euclidean block.
In particular:

- `phi` is singled out as the controller of `theta-rho` mixing,
- the singular slices `cos(2 phi)=0` appear directly in the pullback geometry,
- the ordered coordinates therefore carry exactly the sort of channel asymmetry that the component-norm solver erases.

---

## 4. Baseline pullback mode

The first upgraded mode should still remain as conservative as possible.
So the runtime includes a **baseline pullback** mode:

- same norm potential as before,
- same provisional Einstein trace closure as before,
- but kinetic bookkeeping done in ordered coordinates with the exact pullback metric `G`.

The norm potential in ordered variables is simply
\[
V_{\rm norm}(w)=\frac{m_{\rm glue}^2}{2}e^{2w} + \frac{\lambda_q}{4}e^{4w},
\]
because
\[
|Q|^2 = e^{2w}.
\]

This mode answers a clean question:

> if we only rewrite the runtime in the project’s natural ordered geometry, without adding any new directional forcing, does angular differentiation already appear?

That is the baseline comparison inside the improved solver.

---

## 5. Why pullback geometry alone is not enough

If all angular derivatives vanish at the origin and the potential depends only on `w`, then the ordered angular variables remain frozen.
So the pullback kinetic structure by itself does **not** guarantee observable angular-sector splitting.

That means the project still needs a disciplined source of angular dynamics.
But that source should come from the project’s own geometry, not from arbitrary fake physics.

---

## 6. Exploratory directional potential built from existing ordered-map invariants

The project materials already point to two natural ordered invariants:

1. **phi-singularity / separation control** via `cos(2 phi)` and `sin(2 phi)`
2. **theta-rho pairing** suggested by the pullback metric and the earlier Phase A channel-role hypothesis

So the runtime adds a clearly labeled exploratory directional potential
\[
V_{\rm dir}(w,\theta,\phi,\rho)
=
\frac{\eta}{2}e^{2w}\big(1-\cos^2(2\phi)\big)
+
\frac{\zeta}{2}e^{2w}\big(1-\cos(\theta-\rho)\big)\big(1+\cos(2\phi)\big).
\]

In code, the tested values were
\[
\eta = 0.02,
\qquad
\zeta = 0.015.
\]

### 6.1 Why these terms are the least arbitrary next exploratory choice

They are not claimed to be derived final physics.
But they are motivated by the project’s own established structure:

- `1 - cos^2(2 phi) = sin^2(2 phi)` measures distance from the special `phi` slices singled out by the Jacobian determinant.
- `1 - cos(theta-rho)` measures the relative displacement inside the `theta-rho` pair.
- the factor `1 + cos(2 phi)` makes the pair-coupling explicitly `phi`-modulated rather than treating all three angles as equivalent.

So this is not a random component hack.
It is a disciplined exploratory closure based on the ordered map’s own anisotropic geometry.

---

## 7. Ordered equations used in the runtime

The runtime treats the ordered variables as generalized coordinates with kinetic metric `G`.
The resulting ODE system is written in the standard sigma-model form
\[
\alpha^{i\prime\prime}
+ \Gamma^i_{jk}(\alpha)\,\alpha^{j\prime}\alpha^{k\prime}
+ \Big(\frac{2}{r}+\Phi'-\Lambda'\Big)\alpha^{i\prime}
+ \frac{1}{A}G^{ij}\partial_j V_{\rm total}
=0,
\]
with
\[
V_{\rm total} = V_{\rm norm} + V_{\rm dir} - \xi R e^{2w}.
\]

The same provisional Einstein bookkeeping is then reused, but with kinetic density
\[
K = \alpha'^T G \alpha'.
\]
So the provisional closure becomes
\[
\rho = \frac{1}{2} A K + V_{\rm norm}+V_{\rm dir},
\qquad
p_r = \frac{1}{2} A K - V_{\rm norm}-V_{\rm dir},
\qquad
p_t = -\frac{1}{2} A K - V_{\rm norm}-V_{\rm dir},
\]
and
\[
R=-\kappa T,
\qquad
T=-\rho+p_r+2p_t.
\]

This keeps the improved solver comparable to the old one while changing only the ordered-variable structure.

---

## 8. Singular `phi` slices and why a small regularization is necessary

Because
\[
\det J = e^{4w}\cos(2\phi),
\]
the pullback metric becomes singular when
\[
\cos(2\phi)=0.
\]
The continuation path used in Phase B passes through exactly such a slice at midpoint:
\[
\phi=-\frac{\pi}{4}.
\]

So a raw pullback inverse would make the runtime numerically ill-posed there.
To avoid fake breakdowns from that known coordinate singularity, the runtime uses a tiny explicit inverse regularization
\[
\cos^2(2\phi) \mapsto \max\big(\cos^2(2\phi),\varepsilon_\phi^2\big),
\qquad
\varepsilon_\phi = 10^{-3}.
\]

This is not claimed as physics.
It is a numerical coordinate regularization, and it is labeled as such.
Its purpose is only to let the ordered runtime cross known Jacobian-singular slices without spurious solver collapse.

---

## 9. What the improved runtime is meant to test

The improved solver is therefore testing three nested claims.

### 9.1 Claim A: pullback geometry is the correct ordered baseline

Using the induced ordered metric is more faithful to the project’s own ordered-state geometry than collapsing everything back into norm-only component evolution.

### 9.2 Claim B: pullback geometry alone may still remain degenerate

If baseline pullback stays nearly identical across rich angular sectors, that means the missing ingredient is not just coordinate choice.

### 9.3 Claim C: a small geometry-motivated directional potential may begin to resolve sectors honestly

If the exploratory directional mode creates real neighborhood spread while keeping the continuation family regular, then the project has identified a plausible next runtime family:

- baseline piece = exact ordered pullback geometry,
- exploratory piece = small angular closure built from established ordered-map invariants.

That is a much stronger and cleaner next step than inventing arbitrary component asymmetries.

---

## 10. Bottom line

**Bottom line:** the most honest next Phase B runtime upgrade is to move from the norm-symmetric component IVP into ordered variables with the exact pullback metric induced by
\[
Q(\omega,\theta,\phi,\rho)=e^{\omega}e^{\theta i}e^{\phi j}e^{\rho k},
\]
then compare that conservative baseline against a clearly labeled exploratory directional potential built from the project’s own Jacobian / channel-geometry invariants. This preserves a strict baseline-vs-exploratory distinction, exposes where angular structure can enter, and directly targets the angular degeneracy diagnosed in the Phase B stress test.
