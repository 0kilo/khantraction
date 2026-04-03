# Phase I Data Assessment — Pullback Scan Results

**Date:** 2026-04-02  
**Phase:** I — First-Principles Derivation of Constants  
**Status:** Completed after audit refresh

## 1. What the scan measures

The refreshed Phase I scan measures only the exact pullback-metric eigenstructure of the ordered map:

$$
\lambda_\phi = e^{2\omega},
\qquad
\lambda_+ = e^{2\omega}(1+\sin(2\phi)),
\qquad
\lambda_- = e^{2\omega}(1-\sin(2\phi)).
$$

The data therefore speaks directly about geometry-level angular stiffness, not about full dynamical stability or observables.

## 2. Key numerical results

At the audited fixed scale `omega = 0.5`:

- `lambda_phi = 2.718281828459045`
- maximum active-scale stiffness = `5.43656365691809`
- maximum regular sampled anisotropy ratio = `101320.51697625456`

At the representative off-sheet point `phi = pi/8`:

- `lambda_plus = 4.640397342538603`
- `lambda_minus = 0.7961663143794869`
- active-scale gap = `3.844231028159116`
- unit-scale gap = `1.414213562373095`

## 3. Slice interpretation

The refreshed slice widths are:

- 1D theta `lambda_minus` width: `0.0`
- 1D phi `lambda_minus` width: `5.43656365691809`
- 1D rho `lambda_minus` width: `0.0`
- 2D phi/rho `lambda_minus` width: `5.43656365691809`
- 2D theta/phi `lambda_minus` width: `5.43656365691809`
- 2D theta/rho `lambda_minus` width at fixed `phi = pi/8`: `0.0`

This means:

- phi is the only active control parameter for the pullback anisotropy,
- theta and rho are spectators unless phi changes,
- and the full-domain 1D / 2D protocol confirms that the anisotropy is not a coordinate-artifact of one slice.

## 4. Singular-sheet interpretation

The exact sheet families are:

- `lambda_plus = 0` on `phi = -pi/4 + n*pi`
- `lambda_minus = 0` on `phi = pi/4 + n*pi`

These are alternating soft-sheet families, not a single universal “lambda_minus wall.”

So the correct interpretation is:

- the geometry partitions the active domain into alternating paired-mode sectors,
- one sheet family softens the symmetric `theta + rho` mode,
- the other softens the antisymmetric `theta - rho` mode.

## 5. Bottom line

**Bottom line:** The Phase I data supports a clean geometric result. The ordered-map pullback metric contains a strong phi-controlled stiffness split and exact alternating soft-sheet families. The data does not yet support stronger claims about solver-level beta replacement or observable constants.
