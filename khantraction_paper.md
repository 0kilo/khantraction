# Khantraction: A Quaternion-Valued Toy Model with a Continuous Scalar-to-Quaternion Branch Family

**Authors:** Khan (primary) + Lumen (assistant)

## Abstract
We propose *Khantraction* as an exploratory toy model in which localized spacetime contractions are sustained by a quaternion-valued glue field. The model is motivated by a rope-and-knot picture in which spacetime threads through a self-bound geometric fold, and by the scalar/vector structure of quaternionic state maps. We formulate a nonlinear Lagrangian coupling the quaternion glue to curvature and electromagnetism, first study a reduced static radial system, and then examine a fuller four-component norm-based quaternion version of the model. The strongest current numerical result is that the full norm-based quaternion model supports a continuous family of regular radial solutions ranging from a real/scalar-dominated regime to a strongly quaternion-rich regime. Along this family, the imaginary quaternion magnitude can grow from negligible levels to roughly two orders of magnitude larger than the real component while the branch remains regular over the sampled integration domain. A new structural result is that these branches are also accurately described by an ordered quaternionic state map,
$$
Q(\omega,\theta,\phi,\rho)=e^{\omega}e^{\theta i}e^{\phi j}e^{\rho k},
$$
with the quaternion-rich family occupying a dominant locked internal-angle sector and providing the best current candidate for a branch-specific proto-excitation structure. The present note is intended as a speculative toy-model research report rather than a completed particle theory.

## 1. Introduction: rope metaphors and toy-model ambition
Khantraction sits at the crossroads of geometry and field theory. The motivating picture is simple: imagine a rope carrying spacetime and a loose knot you hold in one hand while pulling the rope with the other. The knot persists while spacetime slips through, and its tightness influences how much proper-time delay the fold imposes. In the present model, that knot is represented by a quaternion-valued glue field that locally pinches spacetime into a bounded region.

This picture is heuristic rather than derivational. The purpose of the present note is not to claim that known particles have already been recovered from first principles, but to explore whether a quaternion-based toy field theory can support interesting localized contraction regimes and nontrivial branch structure. The emphasis here is on building a mathematically explicit toy model, testing it numerically, and honestly reporting what its present solution landscape appears to contain.

## 2. Quaternion-valued toy field theory
Let the glue field be quaternion-valued,
$$
q(x)=s(x)+\vec v(x)\cdot\vec \tau,
$$
where $\vec \tau$ is an $\mathfrak{su}(2)$-like basis and the norm
$$
|q|^2=s^2+\vec v\cdot\vec v
$$
tracks the local contraction strength. At this stage, the quaternion notation should be understood as a compact parametrization of one scalar degree of freedom and a three-component vector degree of freedom, not yet as a derivation from an established particle-physics symmetry principle.

In natural units with signature $(-+++)$, consider the toy-model Lagrangian
$$
\mathcal L=\sqrt{-g}\left[\tfrac{1}{2}g^{\mu\nu}(\partial_\mu s\partial_\nu s+\partial_\mu\vec v\cdot\partial_\nu\vec v)-U(|q|)+\xi R|q|^2\right]-\sqrt{-g}\left[\tfrac{1}{4}F_{\mu\nu}F^{\mu\nu}+\lambda|q|^2F_{\mu\nu}F^{\mu\nu}\right],
$$
with potential
$$
U(|q|)=\tfrac{m_{\text{glue}}^2}{2}|q|^2+\tfrac{\lambda_q}{4}|q|^4.
$$
The nonminimal term $\xi R|q|^2$ allows the glue amplitude to couple directly to curvature, while the $\lambda|q|^2F^2$ coupling is included as a toy mechanism by which electromagnetism could perturb or reinforce the contraction.

The Euler–Lagrange equations produce coupled PDEs for $s$, $\vec v$, and the electromagnetic sector. In a static, spherically symmetric reduction with hedgehog ansatz $\vec v=v(r)\hat r$, introduce the Misner–Sharp mass function $m(r)$ through
$$
ds^2=-e^{2\Phi(r)}dt^2+e^{2\Lambda(r)}dr^2+r^2d\Omega^2,
\qquad
 e^{-2\Lambda}=1-\frac{2m(r)}{r}.
$$
The reduced glue equations become
$$
s''+\left(\frac{2}{r}+\Phi'-\Lambda'\right)s'-\frac{dU}{ds}+2\xi R s=0,
\qquad
v''+\left(\frac{2}{r}+\Phi'-\Lambda'\right)v'-\frac{dU}{dv}+2\xi R v=0.
$$
With
$$
\frac{\partial U}{\partial q}=(m_{\text{glue}}^2+\lambda_q|q|^2)q,
$$
one obtains a nonlinear radial system whose solutions can be investigated numerically. At present, this setup should be regarded as a classical effective toy model rather than a completed microscopic theory.

## 3. Reduced radial model and early localized profiles
The earliest numerical experiments were carried out in the reduced static radial system above. For representative choices such as
$$
m_{\text{glue}}=0.1,
\qquad
\lambda_q=0.01,
\qquad
\xi=0.002,
$$
with initial data
$$
s(10^{-3})=0.02,
\qquad
s'(10^{-3})=0,
\qquad
v(10^{-3})=0,
\qquad
v'(10^{-3})=0.001,
$$
the RK4 solver reaches $r=20$ without encountering a horizon and yields a regular localized-looking profile with outer values roughly
$$
|q|\approx0.0363,
\qquad
m(r)\approx0.178,
\qquad
R\approx-7.6\times10^{-4}.
$$

This reduced profile remains useful as an existence-style numerical hint: the toy equations can support bounded radial structure. However, later work showed that this reduced scalar/vector-amplitude picture does not exhaust the interesting solution landscape of the fuller quaternion model.

## 4. Full four-component norm-based quaternion model
To go beyond the reduced amplitude picture, one can solve the full radial quaternion field
$$
q(r)=a(r)+b(r)i+c(r)j+d(r)k,
$$
with norm
$$
|q|^2=a^2+b^2+c^2+d^2.
$$
At this level the model is still norm-symmetric: the interaction depends only on $|q|^2$. So it should still be understood as a quaternion-valued toy multiplet rather than a fully noncommutative quaternionic field theory. Nevertheless, this fuller model turns out to have much richer branch structure than the reduced radial system alone suggests.

The most useful branch coordinate is the ratio
$$
\max_r \frac{\theta(r)}{|a(r)|},
\qquad
\theta(r)=\sqrt{b(r)^2+c(r)^2+d(r)^2}.
$$
This measures how strongly the imaginary quaternion sector dominates the real one along a radial profile.

## 5. Branch structure: from scalar-dominated to quaternion-rich regimes
The strongest current numerical result is that the full norm-based quaternion model supports a continuous family of regular radial solutions connecting a scalar-dominated regime to a quaternion-rich regime.

At the scalar end of the family, one finds branches with
$$
\max_r \frac{\theta}{|a|}\sim 5\times10^{-5},
$$
so the imaginary quaternion sector is essentially negligible and the profile is effectively real-led.

At the quaternion-rich end, one finds regular branches with
$$
\max_r \frac{\theta}{|a|}\sim 9.1\times10^1,
$$
meaning that the imaginary quaternion magnitude can exceed the real component by roughly two orders of magnitude while the profile remains regular over the sampled integration domain.

A numerical continuation between these endpoints remains regular across the sampled path. This strongly suggests that the scalar-dominated and quaternion-rich solutions belong to the same connected family rather than to disconnected sectors.

A useful set of crossover markers along the family is given by the first points at which
$$
\max_r \frac{\theta}{|a|}\ge 1,
\qquad
\max_r \frac{\theta}{|a|}\ge 10,
\qquad
\max_r \frac{\theta}{|a|}\ge 50.
$$
In the current continuation these occur at approximately
$$
t\approx0.125,
\qquad
t\approx0.600,
\qquad
t\approx0.9375,
$$
respectively, where $t$ parametrizes the interpolation from the scalar seed to the quaternion-rich seed. These are not claimed to be sharp phase transitions, but they do provide a useful branch-family language for weakly imaginary, mixed, and strongly quaternion-dominated regimes.

## 6. Geometric and exponential diagnostics along the family
Several branch observables grow monotonically as the family moves from scalar-dominated to quaternion-rich behavior.

### 6.1 Final mass
The final Misner–Sharp mass increases significantly along the family, from a very small scalar-end value to a substantially larger quaternion-rich value.

### 6.2 Integrated curvature magnitude
Integrated curvature measures such as
$$
\int |R(r)|\,dr
$$
also increase monotonically, suggesting that increasing quaternion richness correlates with a more substantial geometric contraction in the toy-model sense.

### 6.3 Exponential-quaternion vector content
The exponential-quaternion diagnostics
$$
Q_0=e^a\cos\theta,
\qquad
Q_{\mathrm{vec}}=e^a|\sin\theta|
$$
show that the scalar-dominated branch has essentially negligible exponential vector content, while the quaternion-rich branch has a clearly visible nontrivial vector part. In that limited sense, the quaternion exponential is not merely decorative on the quaternion-rich end of the family.

## 7. Ordered quaternionic state map and internal branch structure
A major new structural development is the ordered quaternionic state map
$$
Q(\omega,\theta,\phi,\rho)=e^{\omega}e^{\theta i}e^{\phi j}e^{\rho k}.
$$
This should not be confused with a naive commuting identity for $e^{\omega+\theta i+\phi j+\rho k}$. It is better interpreted as an ordered factorized quaternionic state construction.

Using the quaternion multiplication rules
$$
ij=k,
\qquad
jk=i,
\qquad
ki=j,
$$
one obtains
$$
Q=e^{\omega}(a+bi+cj+dk),
$$
with
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
This gives a nonlinear coordinate map from ordered internal coordinates $(\omega,\theta,\phi,\rho)$ to quaternion components.

Direct numerical fitting shows that this ordered state map describes both scalar and quaternion-rich branch data accurately. More importantly, when tracked across the scalar-to-quaternion family, the fitted coordinates evolve coherently and the quaternion-rich regime settles into a stable ordered-angle pattern.

Across representative branch points, the scalar end sits near trivial internal-angle occupation, while the quaternion-rich end stabilizes near an ordered-angle sector approximately equivalent to
$$
\theta\approx \pi,
\qquad
\phi\approx -\frac{\pi}{2},
\qquad
\rho\approx +\frac{\pi}{2},
$$
up to periodic branch ambiguities.

Neighborhood fits around the promoted quaternion-rich branch show that this pattern is not a one-solution accident: the nearby rich family is strongly angle-locked, especially in $\phi$ and $\rho$, and locked-sector scans reveal one dominant best-fit internal sector together with weaker alternate sectors that are currently best interpreted as residual parameterization degeneracies rather than true species splitting.

This means the quaternion-rich branch is no longer characterized only by large imaginary magnitude. It also appears to occupy a robust internal-state sector in ordered quaternionic coordinates.

## 8. Proto-excitation interpretation of the locked sector
The project still does not possess a full fluctuation spectrum in ordered-state variables. Nevertheless, one can combine the ordered-state analysis with the pre-existing radial-mode proxy results.

Those mode diagnostics show that local fluctuation anisotropy grows strongly along the scalar-to-quaternion family, rising from weak scalar-end values to much larger quaternion-rich values. The ordered-state results now provide an internal-state interpretation of that growth: the strongest mode anisotropy appears precisely where the branch family has settled into its dominant locked ordered-angle sector.

The defensible statement is therefore:

> the dominant locked ordered-angle sector is the best current candidate for a branch-specific proto-excitation sector in Khantraction.

This is still not a true particle spectrum, but it is stronger than a purely geometric re-description. It suggests that the ordered state map is beginning to connect internal branch identity with branch-specific excitation character.

The newest soft-mode analysis sharpens this further: the dominant soft fluctuation of the quaternion-rich locked sector is overwhelmingly a $\theta$-type internal angular mode rather than a breathing-like scale mode, and a first radial $\theta$-channel proxy suggests a small stiff core together with a broadly soft internal region across most of the object.

This makes the richest branches look less like point-particle candidates and more like compact structured spacetime-fold objects with particle-like external behavior and nontrivial internal geometry.

A final major development of this phase is that the soft $\theta$-channel now shows a first refined proto-spectrum. A denser radial shooting scan reveals several resonance-like candidate minima, including one particularly sharp candidate, and the candidate set remains stable under refinement. Even more significantly, the candidate minima shift under both opposite chiral perturbation directions and opposite signed externally induced loading directions. The current proxy-level evidence therefore suggests that the richest structured object does not merely possess internal chirality and loading sensitivity statically; its emerging excitation landscape is also sensitive to both.

The defensible statement is still modest:

> Khantraction has not yet produced a true quantum spectrum, but it now supports a chirality-sensitive and loading-sensitive proto-spectrum in its dominant soft internal channel.

## 9. Limitations
This note has several important limitations.

1. **Toy-model status.** The Lagrangian is phenomenological and exploratory. It has not been derived from a compelling microscopic symmetry principle or from a known extension of general relativity and the Standard Model.
2. **No particle recovery yet.** The model does not yet derive spin, statistics, charge quantization, realistic masses, or experimentally verified couplings.
3. **No full stability proof.** The current numerics concern static radial integration and first robustness probes, not full nonlinear dynamical stability.
4. **Direction still weakly constrained.** The full norm-based model is strongly sensitive to quaternion magnitude, but the current reduced direction-sensitive and transport-based upgrades have not yet shown comparably strong dependence on quaternion direction.
5. **Quaternion link remains partly interpretive.** The connection between the branch family and quaternion exponential / Maurer–Cartan structure is suggestive and partially developed, but not yet a rigorously established dynamical equivalence.

These limitations do not invalidate the toy model, but they define its current epistemic status.

## 10. Future work
1. Strengthen the numerical characterization of the full norm-based branch family through denser continuation, sharper branch observables, and neighborhood searches around the quaternion-rich regime.
2. Develop more systematic stability analysis along representative points of the scalar-to-quaternion family.
3. Compute additional geometric invariants (Ricci, Kretschmann, tidal observables, integrated curvature measures) along the family to sharpen its geometric interpretation.
4. Push the ordered quaternionic state map further by deriving fluctuation equations directly in $(\omega, \theta, \phi, \rho)$ variables and sharpening the current proto-spectrum into a cleaner candidate mode structure.
5. Determine whether the chirality-sensitive and loading-sensitive proto-spectrum shifts survive in improved radial operators and under better boundary conditions.
6. Resolve the weaker alternate ordered-angle sectors more rigorously to determine whether they are exact degeneracies, branch-cut artifacts, or the first hints of deeper internal-state multiplicity.
7. Investigate whether topological, geometric, or transport-based refinements can make quaternion direction—not just quaternion magnitude—dynamically relevant in branch selection.

In short, Khantraction should presently be read as an exploratory geometric toy model with a suggestive quaternion interpretation, numerical evidence for a continuous family of regular radial solutions ranging from scalar-dominated to quaternion-rich behavior, and a newly developed ordered-state description in which the quaternion-rich regime occupies a dominant locked internal sector with the first hints of a chirality-sensitive and loading-sensitive proto-spectrum—not yet as a completed theory of particles.
