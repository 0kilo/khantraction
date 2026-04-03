# Phase A Synthesis — Ordered Quaternion Parameter Foundation

**Date:** 2026-03-28  
**Phase:** A — Parameter foundation  
**Status:** Complete synthesis note; closure handled separately

## 1. Purpose of this synthesis

This note consolidates what Phase A has actually established so far about the ordered quaternion parameter map

$$
Q(\omega,\theta,\phi,\rho)=e^{\omega}e^{\theta i}e^{\phi j}e^{\rho k},
$$

using the active domain convention:
- $\omega>0$
- $\theta,\phi,\rho\in[-2\pi,2\pi]$
- no redundancy quotienting

The aim is to state clearly what now seems robust, what remains interpretive, and what still belongs to later phases.

---

## 2. What Phase A was trying to answer

Phase A asked, at minimum:
1. Is $\omega$ cleanly separable as a scale factor?
2. Are $\theta,\phi,\rho$ genuinely distinct channels in the ordered map?
3. Is there a meaningful asymmetry among the angular variables?
4. Which apparent asymmetries are chart-geometric, and which might later matter physically?

At the start, it was still possible that the three angles were just an arbitrary coordinate packaging with no clear structural distinction.
That no longer looks like the right reading.

---

## 3. Strong results now established

### 3.1 $\omega$ is a pure scale coordinate

This is now the cleanest result of all.

Every component carries the same multiplicative factor $e^{\omega}$, and the angular tangent norms satisfy

$$
\|\partial_\theta Q\|=\|\partial_\phi Q\|=\|\partial_\rho Q\|=e^{\omega}
$$

up to numerical precision across the stress-tested positive-$\omega$ range.

So the current best statement is:

> $\omega$ sets overall scale magnitude and does not alter the internal angular overlap geometry except through uniform rescaling.

---

### 3.2 The three angular channels are locally real, not fake

Away from singular sheets, the map has full local rank and the angular directions are genuinely locally independent.

So $\theta,\phi,\rho$ are not merely redundant names for one local angular degree of freedom.
They define three genuine local tangent directions on the ordered-state manifold wherever the chart is regular.

---

### 3.3 The chart singularity architecture is controlled by $\phi$

A major Phase A result is the determinant law

$$
\det J = e^{4\omega}\cos(2\phi).
$$

Therefore singular sheets occur exactly at

$$
\phi=\frac{\pi}{4}+\frac{n\pi}{2}.
$$

Inside the current working box $[-2\pi,2\pi]$, those are the repeated slices
- $\pm\pi/4$
- $\pm 3\pi/4$
- $\pm 5\pi/4$
- $\pm 7\pi/4$

The wider active angle box does not change the law; it just makes the repeated-sheet structure explicit.

---

### 3.4 $\phi$ is not stronger in norm — it is different in role

This is the conceptual turning point of Phase A.

The angular channels are **equal in norm**, so the distinction is not one of raw channel magnitude.
Instead, the distinction appears in the overlap geometry.

The stress-tested result is:

$$
\cos(\partial_\theta Q,\partial_\phi Q)\approx 0,
\qquad
\cos(\partial_\phi Q,\partial_\rho Q)\approx 0
$$

across the sampled domain to essentially machine precision, while

$$
\cos(\partial_\theta Q,\partial_\rho Q)\in[-1,1].
$$

So $\phi$ stays almost perfectly orthogonal to both $\theta$ and $\rho$, while the relation between $\theta$ and $\rho$ sweeps through the full alignment range.

This supports the mapping-level hypothesis:

> $\phi$ acts as a separator / mixing-control channel for the paired directions $\theta$ and $\rho$, rather than as just one more symmetric peer.

---

### 3.5 The $(\theta,\rho)$ pair is the active relational subsystem

The explicit slice studies made this visible.

- Holding $\phi=0$, the $(\theta,\rho)$-plane remains regular across the sampled box.
- Holding $\phi=\pi/4$, the entire $(\theta,\rho)$-plane becomes singular.
- Varying $\phi$ with $(\theta,\rho)$ fixed exposes repeated singular crossings directly.
- Varying $\theta$ or $\rho$ with regular fixed $\phi$ does not induce singularity by itself.

So the current clean picture is:

> the map contains a paired internal subsystem $(\theta,\rho)$, and $\phi$ determines whether that subsystem remains locally distinct or collapses into local alignment/anti-alignment.

---

## 4. Current best role interpretation

At the purely mapping-geometric level, the strongest current role assignment is:

- **$\omega$** = scale coordinate
- **$\phi$** = separator / mixing-control coordinate
- **$\theta$, $\rho$** = paired internal structural directions

This is the first role assignment in the project that feels both precise and genuinely earned by the calculations.

---

## 5. What Phase A has *not* established

Even now, there are still limits.

### 5.1 Not yet a physical trait proof

Phase A has established a robust **mapping-level structure**.
It has **not yet** proven that the same role structure directly governs classical object observables in the fuller Khantraction model.

So one must still distinguish between:
- parameter-map geometry,
- and classical-object trait structure.

### 5.2 Not yet a full dynamical statement

Nothing here yet says how the field equations weight these channels dynamically.
That belongs to later structured-object analyses and operator-side work.

### 5.3 Not yet a closure of all possible objections

The mapping picture is already strong, but one could still ask whether any hidden alternative parameterization might reorganize the interpretation.
That is an objection Phase A could address only partially.

---

## 6. Why this matters for later phases

Phase A was supposed to prevent premature storytelling.
It has succeeded at that.

Before this work, it was easy to slip into vague claims like:
- one angle seems dominant,
- maybe the rich branch is mainly a theta story,
- maybe the three angles are all just similar.

Now the map itself pushes back against that vagueness.
It says something sharper:
- scale is separate,
- the three angular channels are equally strong in norm,
- but not equal in relational role,
- and $\phi$ is structurally special because it governs the coupling geometry of the $(\theta,\rho)$ pair.

That is exactly the kind of disciplined foundation Phase A was supposed to deliver.

---

## 7. Bottom line

**Bottom line:** Phase A has produced a robust ordered-map foundation in which

$$
Q(\omega,\theta,\phi,\rho)=e^{\omega}e^{\theta i}e^{\phi j}e^{\rho k}
$$

is best read as:
- one pure scale degree of freedom $\omega$,
- plus a three-angle internal geometry in which $\phi$ is an orthogonal separator / mixing controller,
- and $\theta,\rho$ form the paired internal directions whose relative relation is being modulated.

That is not yet the full classical object story.
But it is now a strong and coherent parameter-foundation result.

---

## 8. Closure handoff

This synthesis note captures the final role picture, but it is not the closure note itself.

The audited closure decision and the full claim-to-evidence map are recorded in:

- `summary/2026-03-28_phase_a_closure_summary.md`
