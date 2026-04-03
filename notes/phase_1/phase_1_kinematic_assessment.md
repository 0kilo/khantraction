# Phase 1 Assessment

## Verdict
Phase 1 is complete.

## What Phase 1 established
- The exact pointwise redundancy structure of the exponential-quaternion ansatz is now on paper.
- The exact Jacobian determinant is now on paper:

```text
det(J)
  = exp(4 a(omega))
    (sin(R)/R)^2
    a'(omega) b'(theta) c'(phi) d'(rho).
```

- The orientation-loss sheets are now explicit:

```text
R = k pi,   k != 0.
```

- The vacuum-equivalent and sign-flip sets are now explicit:

```text
q = 1  <=>  a(omega) = 0 and R = 2pi m
q = -1 <=>  a(omega) = 0 and R = (2m + 1)pi.
```

## What the direct data shows

### Periodic admissible families collapse heavily
On the required full 11-anchor lattice:
- `periodic_simple`
  - total points: `14641`
  - unique quaternion classes: `1080`
  - redundancy ratio: `0.9262345468205724`
  - vacuum-equivalent anchor count: `625`
  - max class multiplicity: `135`
- `periodic_harmonic`
  - total points: `14641`
  - unique quaternion classes: `1080`
  - redundancy ratio: `0.9262345468205724`
  - vacuum-equivalent anchor count: `625`
  - max class multiplicity: `135`

So the periodic angle-respecting class does not preserve raw angle labels as identity data.

### The exponential map itself is still non-injective even without periodic admissibility
The lifted diagnostic family is injective on the required 11-anchor lattice, but it still shows:
- sign-flip hits: `2`
- singular-sheet hits: `22`
- rank-2 anchor points: `22`

So periodicity is not the whole story. The quaternion exponential itself still carries intrinsic sheet redundancy through `R = k pi`.

For the periodic families, the 11-anchor lattice did not land exactly on `R = k pi`, so their anchor-level singular-sheet counts are zero. But the canonical convergence summaries still show:
- `periodic_simple` reaches `R_max = 3.8105117766515306`,
- `periodic_harmonic` reaches `R_max = 3.274503255117253`,

both of which exceed `pi`. So the singular-sheet architecture is present in the continuous domain even when the anchor lattice misses the exact sheet locations.

### Rank loss behaves as predicted
- `periodic_simple`
  - rank-4 anchor points: `2401`
  - rank-3 anchor points: `5488`
  - rank-2 anchor points: `4704`
  - rank-1 anchor points: `1792`
  - rank-0 anchor points: `256`
- `periodic_harmonic`
  - rank-4 anchor points: `9317`
  - rank-3 anchor points: `5324`
- `lifted_chart_linear`
  - rank-4 anchor points: `14619`
  - rank-2 anchor points: `22`

This matches the derivational picture:
- derivative-zero sheets cause additional rank loss in periodic families,
- while the non-periodic lifted family mainly loses rank on the true `R = k pi` orientation-loss sheets.

## Phase 1 decision
The ansatz does retain nontrivial structure:
- the full quaternion `q`,
- the unit-quaternion part `u`,
- the singular-sheet architecture,
- and the vacuum-equivalent/sign-flip sets.

But Phase 1 does **not** support particle-species identity at the pointwise kinematic level.

The correct conclusion is:
- raw angle labels are not identity invariants,
- norm-only structure is already too weak,
- and any serious survival path for Khantraction must come from:
  - non-norm derivative structure,
  - topology,
  - geometry,
  - or the spacetime lift itself.

## Next action
Proceed to Phase 2.

Phase 2 must build direct action families and reject, immediately, any theory that claims angle-defined species while depending only on `|q|`.
