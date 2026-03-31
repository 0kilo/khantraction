# Derivation 71: Clean Exponential / Ordered Quaternion Parameter Mapping

**Date:** 2026-03-28  
**Purpose:** Establish a clean canonical parameter mapping for the quaternionic state description used in Khantraction, with corrected algebra and explicit Jacobian.

---

## 1. Why this document is now central

The project is being reset around the parameter mapping itself.

The key reason is that the angular parameters
$$
\theta,\phi,\rho
$$
should not be prematurely collapsed into one dominant story. They must be treated as potentially distinct varying characteristics.

So this document is meant to be the clean base camp for future work.

---

## 2. Canonical interpretation

The canonical parameterization is
$$
Q(\omega,\theta,\phi,\rho)=e^{\omega}e^{\theta i}e^{\phi j}e^{\rho k}.
$$

This should be interpreted as an **ordered factorized quaternionic state map**.

It should **not** be casually identified with the commuting expression
$$
e^{\omega+\theta i+\phi j+\rho k}
$$
without further justification, because quaternion units do not commute.

---

## 3. Roles of the parameters

The present working interpretation is:
- $\omega$ = **scale factor**
- $\theta,\phi,\rho$ = **distinct internal angles**

So the project should now treat $\omega$ differently from the angular variables.

The angular variables are not to be assumed equivalent unless future analysis proves that.

---

## 4. Elementary factor expansions

Since $\omega$ is real,
$$
e^{\omega}=\cosh\omega+\sinh\omega = e^{\omega}.
$$

For the pure imaginary quaternion directions,
$$
e^{\theta i}=\cos\theta+i\sin\theta,
$$
$$
e^{\phi j}=\cos\phi+j\sin\phi,
$$
$$
e^{\rho k}=\cos\rho+k\sin\rho.
$$

Therefore
$$
Q=e^{\omega}(\cos\theta+i\sin\theta)(\cos\phi+j\sin\phi)(\cos\rho+k\sin\rho).
$$

---

## 5. Quaternion multiplication rules

Use the standard quaternion identities
$$
i^2=j^2=k^2=ijk=-1,
$$
$$
ij=k,
\qquad
jk=i,
\qquad
ki=j,
$$
with reversed order giving minus signs:
$$
ji=-k,
\qquad
kj=-i,
\qquad
ik=-j.
$$

---

## 6. Component expansion

Write
$$
Q = x_0 + x_1 i + x_2 j + x_3 k.
$$

Expanding the ordered product gives
$$
Q=e^{\omega}(a+bi+cj+dk),
$$
where
$$
a=\cos\theta\cos\phi\cos\rho-\sin\theta\sin\phi\sin\rho,
$$
$$
b=\sin\theta\cos\phi\cos\rho+\cos\theta\sin\phi\sin\rho,
$$
$$
c=\cos\theta\sin\phi\cos\rho-\sin\theta\cos\phi\sin\rho,
$$
$$
d=\cos\theta\cos\phi\sin\rho+\sin\theta\sin\phi\cos\rho.
$$

So the coordinates are
$$
x_0=e^{\omega}a,
\qquad
x_1=e^{\omega}b,
\qquad
x_2=e^{\omega}c,
\qquad
x_3=e^{\omega}d.
$$

---

## 7. Immediate structural observation

The scale factor $\omega$ multiplies all four components uniformly.

That means the angular structure is entirely encoded in the normalized quaternion
$$
\frac{Q}{|Q|}=a+bi+cj+dk.
$$

So future work should distinguish carefully between:
- overall scaling effects carried by $\omega$,
- and orientation / internal-state effects carried by $\theta,\phi,\rho$.

---

## 8. Jacobian of the parameter map

Let
$$
\alpha=(\omega,\theta,\phi,\rho),
\qquad
x=(x_0,x_1,x_2,x_3).
$$

The Jacobian is
$$
K_{ij}=\frac{\partial x_i}{\partial \alpha_j}.
$$

### 8.1 Derivatives with respect to $\omega$
Because every component carries the factor $e^{\omega}$,
$$
\frac{\partial x_0}{\partial\omega}=x_0,
\qquad
\frac{\partial x_1}{\partial\omega}=x_1,
\qquad
\frac{\partial x_2}{\partial\omega}=x_2,
\qquad
\frac{\partial x_3}{\partial\omega}=x_3.
$$

### 8.2 Derivatives with respect to $\theta$
$$
\frac{\partial a}{\partial\theta}=-\sin\theta\cos\phi\cos\rho-\cos\theta\sin\phi\sin\rho,
$$
$$
\frac{\partial b}{\partial\theta}=\cos\theta\cos\phi\cos\rho-\sin\theta\sin\phi\sin\rho = a,
$$
$$
\frac{\partial c}{\partial\theta}=-\sin\theta\sin\phi\cos\rho-\cos\theta\cos\phi\sin\rho,
$$
$$
\frac{\partial d}{\partial\theta}=-\sin\theta\cos\phi\sin\rho+\cos\theta\sin\phi\cos\rho.
$$

### 8.3 Derivatives with respect to $\phi$
$$
\frac{\partial a}{\partial\phi}=-\cos\theta\sin\phi\cos\rho-\sin\theta\cos\phi\sin\rho,
$$
$$
\frac{\partial b}{\partial\phi}=-\sin\theta\sin\phi\cos\rho+\cos\theta\cos\phi\sin\rho,
$$
$$
\frac{\partial c}{\partial\phi}=\cos\theta\cos\phi\cos\rho+\sin\theta\sin\phi\sin\rho,
$$
$$
\frac{\partial d}{\partial\phi}=-\cos\theta\sin\phi\sin\rho+\sin\theta\cos\phi\cos\rho.
$$

### 8.4 Derivatives with respect to $\rho$
$$
\frac{\partial a}{\partial\rho}=-\cos\theta\cos\phi\sin\rho-\sin\theta\sin\phi\cos\rho,
$$
$$
\frac{\partial b}{\partial\rho}=-\sin\theta\cos\phi\sin\rho+\cos\theta\sin\phi\cos\rho,
$$
$$
\frac{\partial c}{\partial\rho}=-\cos\theta\sin\phi\sin\rho-\sin\theta\cos\phi\cos\rho,
$$
$$
\frac{\partial d}{\partial\rho}=\cos\theta\cos\phi\sin\rho+\sin\theta\sin\phi\cos\rho = a.
$$

So for angular directions,
$$
\frac{\partial x_i}{\partial\theta}=e^{\omega}\frac{\partial(a,b,c,d)_i}{\partial\theta},
\qquad
\frac{\partial x_i}{\partial\phi}=e^{\omega}\frac{\partial(a,b,c,d)_i}{\partial\phi},
\qquad
\frac{\partial x_i}{\partial\rho}=e^{\omega}\frac{\partial(a,b,c,d)_i}{\partial\rho}.
$$

---

## 9. Why the Jacobian matters

The Jacobian tells us how sensitively the quaternion state depends on:
- scale changes $\omega$,
- $\theta$-variations,
- $\phi$-variations,
- and $\rho$-variations.

This is exactly why the project now needs to restart from this level.

If $\theta,\phi,\rho$ encode genuinely distinct characteristics, the Jacobian is one of the first places where those differences should be analyzed systematically.

---

## 10. Current methodological caution

The recent structured-object / spin / proto-spectrum work may have over-focused on the $\theta$-channel before $\phi$ and $\rho$ were explored on equal footing.

So the correct next-stage methodology is:
- do **not** assume one angle dominates universally,
- do **not** collapse the three-angle space prematurely,
- and re-analyze the mapping and its consequences with all angular channels treated seriously.

---

## 11. Recommended next steps from this clean foundation

1. Compare the three angular channels $\theta,\phi,\rho$ symmetrically at the classical level.
2. Examine Jacobian structure channel by channel rather than reading everything through one preferred angle.
3. Rebuild any later fluctuation or proto-spectrum story only after that symmetric angular treatment is in place.

---

## 12. Bottom line

**Bottom line:** the clean canonical mapping for Khantraction is the ordered quaternionic state map
$$
Q(\omega,\theta,\phi,\rho)=e^{\omega}e^{\theta i}e^{\phi j}e^{\rho k},
$$
with $\omega$ as scale and $\theta,\phi,\rho$ as distinct internal angles. The explicit component formulas and Jacobian above should now be treated as the active foundation from which the next phase of work restarts.
