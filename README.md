# vectorized_lerp_interpolation

Linear interpolation between scalars, arrays of points, and along parametric segments with clamping and extrapolation control.

## Usage

```python
from vectorized_lerp_interpolation import lerp, lerp_array, lerp_segment

# Scalar interpolation
lerp(0.0, 10.0, 0.5)          # 5.0
lerp(0.0, 10.0, 2.0)          # 10.0 (clamped by default)
lerp(0.0, 10.0, 2.0, clamp=False)  # 20.0 (extrapolated)

# Elementwise array interpolation
lerp_array([0.0, 1.0, 2.0], [10.0, 11.0, 12.0], 0.5)  # [5.0, 6.0, 7.0]

# Parametric segment sampling
lerp_segment(0.0, 10.0, 0.0, steps=3)  # [0.0, 5.0, 10.0]
lerp_segment([0.0, 0.0], [10.0, 20.0], [0.0, 1.0])  # [[0.0, 0.0], [10.0, 20.0]]
```

## Why this exists

The standard formula `a + (b - a) * t` is simple but easy to misuse when `t` falls outside [0, 1]. This library makes clamping the default so that a stray parameter cannot silently produce values outside the segment. Extrapolation is still available by passing `clamp=False`, but it is an explicit choice.

The trade-off is that `lerp` always returns a float, even when both inputs are integers. This avoids surprising type changes and keeps the arithmetic consistent across all functions.

## Edge cases

- Mixed scalar and sequence points in `lerp_segment` raise `TypeError`; there is no implicit broadcasting.
- `lerp_array` requires all three arguments to have the same length (a scalar `t` is broadcast). Mismatched lengths raise `ValueError`.
- `steps` in `lerp_segment` must be at least 1. When `steps > 1` and `t` is a scalar, it generates evenly spaced samples from 0 to 1 inclusive.
