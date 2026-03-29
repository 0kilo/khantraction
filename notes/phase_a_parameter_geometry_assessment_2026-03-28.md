# Phase A Assessment — Ordered Quaternion Parameter Geometry

**Date:** 2026-03-28  
**Phase:** A — Parameter foundation  
**Status:** In progress

## Purpose

This note assesses the first active Phase A task:

> analyze the ordered quaternion parameter map and determine what can already be said about the distinct roles of \(\omega,\theta,\phi,\rho\).

The active canonical map is
\[
Q(\omega,\theta,\phi,\rho)=e^{\omega}e^{\theta i}e^{\phi j}e^{\rho k}.
\]

## Questions for this first assessment

1. Is \(\omega\) cleanly separable as a scale factor?
2. Are \(\theta,\phi,\rho\) automatically symmetric in the ordered map, or only superficially so?
3. Where does the parameter map become degenerate or structurally delicate?
4. What should be treated as a coordinate artifact versus a candidate real channel distinction?

## Initial expectations before the scan

The current expectation is:
- \(\omega\) should factor out uniformly.
- The angular variables should live on the normalized quaternion state manifold.
- Because the map is ordered, the three angles may not play identical roles in local coordinates even if they all contribute to the same normalized quaternion geometry.
- Any strong claim that one angle is *the* privileged internal direction should require more than raw coordinate sensitivity.

## Active implementation

The first reusable analysis file for this Phase A step is:
- `analysis/phase_a_parameter_geometry.py`

Its generated outputs are stored under:
- `solutions/phase_a_parameter_geometry/`

## What this assessment is looking for

At minimum, this first pass should tell us:
- whether the Jacobian is generically full rank,
- where rank drops or determinant suppression occur,
- whether the angular tangent directions are usually distinct,
- and whether any angle appears globally privileged or only chart-privileged.

## Provisional stance before reading generated outputs

The most likely outcome is:
- \(\omega\) is indeed a pure overall scale coordinate,
- \(\theta,\phi,\rho\) are distinct ordered angular channels at the coordinate level,
- but some of their asymmetries may reflect the chosen factorization chart rather than deep physical non-equivalence.

So the burden of proof for later interpretation should be:

> local coordinate distinction is not yet the same thing as dynamical or physical distinction.

## First generated-output reading

### Coarse scan headline

The first coarse grid scan (`solutions/phase_a_parameter_geometry/coarse_scan.csv`) sampled 4913 ordered-angle points at fixed \(\omega=0\).

Headline observations:
- the Jacobian is **generically full rank**,
- the named benchmark points all have **rank 4** and \(|\det J|=1\),
- the angular tangent vectors at those benchmark points are all **unit norm** and **mutually orthogonal** to numerical precision,
- but there is a large discrete set of **coarse singular points** where rank drops to 3.

This already supports a clean first conclusion:

> away from singular sets, the ordered map behaves like a well-formed local coordinate chart with one scale direction plus three distinct local angular directions.

### Meaning of the named points

The named-point report is especially informative.

At:
- the origin,
- the single-angle quarter-turn points,
- the all-quarter-turn point,
- and the current rich-sector guess,

the three angular tangent directions remain locally orthogonal and equal in norm.

So the first-pass geometry does **not** support a story in which one angular variable is generically stronger or larger than the others at ordinary regular points.

That matters because it pushes against any premature claim that one angle is inherently the dominant internal degree of freedom at the mapping level alone.

### What the singular set seems to be doing

The coarse singular list shows a repeated pattern:
- rank drops occur when two angular tangent directions become collinear,
- in the coarse data this most visibly appears as
  - \(\cos(\partial_\theta Q,\partial_\rho Q)=\pm 1\),
  - while the \(\phi\)-direction remains transverse.

So the singular behavior is not that the whole angular space collapses. Rather:
- one pair of angular directions can locally merge,
- causing the ordered chart to lose one degree of local distinguishability.

This strongly suggests a **coordinate singularity / chart-degeneracy structure** rather than evidence that one angle is globally unphysical.

### What seems established already

From this first pass, the most defensible statements are:

1. **\(\omega\) is cleanly a scale coordinate.**  
   It multiplies all components uniformly and is separable from the normalized angular geometry.

2. **\(\theta,\phi,\rho\) are locally distinct angular directions on regular regions of the chart.**  
   At generic sampled points and especially at named benchmark points, the map treats them as three independent tangent directions.

3. **The ordered chart has singular loci.**  
   On these loci, at least one pair of angular directions becomes locally indistinguishable.

4. **Local distinction is not yet physical distinction.**  
   The present scan only shows that the ordered map carries three locally independent angular directions away from chart singularities. It does **not yet** prove that all three directions correspond to distinct dynamical object traits.

### Revised provisional Phase A stance

The current best Phase A stance is:

> the mapping itself gives strong support for one scale degree of freedom plus three genuine local angular coordinate directions, but any stronger claim about \(\theta\), \(\phi\), and \(\rho\) encoding different classical traits must come from later geometry/object analyses, not from the parameter map alone.

## Phase A refinement — singular structure (re-done on the active domain)

A re-done singular-structure pass has now been added in:
- `analysis/phase_a_singularity_structure.py`
- `derivations/derivation_72_phase_a_jacobian_singularity_structure.md`
- `solutions/phase_a_singularity_structure/`

This re-run uses the active project convention:
- \(\omega>0\)
- \(\theta,\phi,\rho\in[-2\pi,2\pi]\)
- no redundancy quotienting

### Stronger result on the actual working box

Across 55,539 sampled points on the widened domain, the refined scan supports
\[
\det J = e^{4\omega}\cos(2\phi)
\]
with numerical error at machine precision scale.

So the chart becomes singular exactly when
\[
\cos(2\phi)=0
\quad\iff\quad
\phi = \frac{\pi}{4}+\frac{n\pi}{2}.
\]

Inside the active working box \([-2\pi,2\pi]\), that yields the repeated singular slices
- \(\phi=\pm\pi/4\)
- \(\phi=\pm 3\pi/4\)
- \(\phi=\pm 5\pi/4\)
- \(\phi=\pm 7\pi/4\)

### What changed by redoing it this way

The larger angle domain did **not** change the singular law.
What it changed was the visible structure:
- instead of seeing one principal set of singular slices,
- we now see the same singular architecture repeated across the full explicit working domain.

That matches the active preference for this phase: keep the broader angle box and do not quotient away repeated structure.

### What seems established now

1. **\(\omega\)** is a positive scale coordinate and controls determinant magnitude through \(e^{4\omega}\).
2. **\(\phi\)** controls the singular-sheet architecture of the ordered chart.
3. **\(\theta\)** and **\(\rho\)** remain locally distinct away from those sheets, but the chart can lose one angular degree of local distinguishability on them.
4. The singular structure is systematic and repeated across the full active angle box.

### What this still does *not* prove

Even after the redo, this still does **not** prove that \(\phi\) is the dominant physical channel.
It proves something more precise:

> in the ordered coordinate chart, \(\phi\) controls where local angular-coordinate independence fails.

That is chart geometry.
It is not yet a classical trait hierarchy.

## Next interpretation step

The next correct Phase A move is now even clearer:
- compare \(\theta,\phi,\rho\) using less chart-bound quantities,
- keep the full active box \([-2\pi,2\pi]\) visible,
- and test whether channel differences survive at a geometry/object level rather than only at a coordinate-chart level.
