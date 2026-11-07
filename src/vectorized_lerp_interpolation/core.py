"""Core linear interpolation functions.

Design decisions:
- ``lerp`` takes scalar t and clamps by default. Extrapolation is opt-in via
  ``clamp=False``. This keeps the common case safe and makes accidental
  extrapolation explicit.
- ``lerp_array`` operates elementwise on sequences. It does not broadcast
  mismatched lengths; that would require a broadcasting rule we do not want to
  invent. All three inputs must have the same length.
- ``lerp_segment`` interpolates along a parametric segment defined by a start
  and end point. Points may be scalars or sequences. It supports a ``steps``
  argument for sampling multiple t values at once.
"""

from __future__ import annotations

from typing import Sequence, Union

Number = Union[int, float]
Point = Union[Number, Sequence[Number]]


def _clamp01(t: float) -> float:
    """Clamp t to [0, 1].

    We use this instead of min/max inline so the intent is obvious and the
    boundary is tested in one place.
    """
    if t < 0.0:
        return 0.0
    if t > 1.0:
        return 1.0
    return t


def lerp(a: Number, b: Number, t: Number, clamp: bool = True) -> float:
    """Linearly interpolate between two scalars.

    Parameters
    ----------
    a : int or float
        Start value.
    b : int or float
        End value.
    t : int or float
        Interpolation parameter. 0 returns ``a``, 1 returns ``b``.
    clamp : bool, optional
        When True (default), ``t`` is clamped to [0, 1]. When False, values
        outside [0, 1] extrapolate linearly.

    Returns
    -------
    float
        The interpolated value.
    """
    tt = _clamp01(float(t)) if clamp else float(t)
    return float(a) + (float(b) - float(a)) * tt


def lerp_array(
    a: Sequence[Number],
    b: Sequence[Number],
    t: Union[Number, Sequence[Number]],
    clamp: bool = True,
) -> list[float]:
    """Elementwise linear interpolation over two sequences.

    Parameters
    ----------
    a : sequence of int or float
        Start values.
    b : sequence of int or float
        End values.
    t : number or sequence of numbers
        Interpolation parameter(s). A scalar applies to every element. A
        sequence must have the same length as ``a`` and ``b``.
    clamp : bool, optional
        When True (default), each ``t`` is clamped to [0, 1]. When False,
        values outside [0, 1] extrapolate linearly.

    Returns
    -------
    list of float
        Interpolated values, same length as ``a``.

    Raises
    ------
    ValueError
        If ``a`` and ``b`` have different lengths, or if ``t`` is a sequence
        whose length does not match.
    """
    if len(a) != len(b):
        raise ValueError(
            f"a and b must have the same length, got {len(a)} and {len(b)}"
        )
    n = len(a)
    if isinstance(t, (int, float)):
        t_seq = [t] * n
    else:
        t_seq = list(t)
        if len(t_seq) != n:
            raise ValueError(
                f"t sequence length {len(t_seq)} does not match a/b length {n}"
            )
    result: list[float] = []
    for ai, bi, ti in zip(a, b, t_seq):
        result.append(lerp(ai, bi, ti, clamp=clamp))
    return result


def _lerp_point(
    p0: Point, p1: Point, t: float, clamp: bool
) -> Union[float, list[float]]:
    """Interpolate between two points, which may be scalars or sequences.

    Returns a float for scalar points and a list of floats for sequence points.
    """
    if isinstance(p0, (int, float)) and isinstance(p1, (int, float)):
        return lerp(p0, p1, t, clamp=clamp)
    if isinstance(p0, (int, float)) or isinstance(p1, (int, float)):
        raise TypeError("p0 and p1 must both be scalars or both be sequences")
    return lerp_array(p0, p1, t, clamp=clamp)


def lerp_segment(
    p0: Point,
    p1: Point,
    t: Union[Number, Sequence[Number]],
    clamp: bool = True,
    steps: int = 1,
) -> Union[float, list[float], list[Union[float, list[float]]]]:
    """Interpolate along a parametric segment.

    This is a convenience wrapper around ``lerp`` and ``lerp_array`` for the
    common case of a segment defined by two endpoints. It supports three
    output shapes:

    - Scalar ``t`` and scalar points: returns a float.
    - Scalar ``t`` and sequence points: returns a list of floats.
    - Sequence ``t`` and scalar points: returns a list of floats.
    - Sequence ``t`` and sequence points: returns a list of lists of floats.

    Parameters
    ----------
    p0 : number or sequence of numbers
        Start point.
    p1 : number or sequence of numbers
        End point.
    t : number or sequence of numbers
        Interpolation parameter(s).
    clamp : bool, optional
        When True (default), ``t`` is clamped to [0, 1]. When False,
        extrapolation is allowed.
    steps : int, optional
        If greater than 1 and ``t`` is a scalar, generate ``steps`` evenly
        spaced t values in [0, 1] instead of a single value. Ignored when
        ``t`` is a sequence.

    Returns
    -------
    float, list of float, or list of lists of float
        Interpolated value(s).

    Raises
    ------
    ValueError
        If ``steps`` is less than 1.
    TypeError
        If ``p0`` and ``p1`` are not both scalars or both sequences.
    """
    if steps < 1:
        raise ValueError("steps must be at least 1")

    if isinstance(t, (int, float)):
        if steps == 1:
            return _lerp_point(p0, p1, float(t), clamp)
        # Generate steps points from 0 to 1 inclusive.
        t_values = [i / (steps - 1) for i in range(steps)] if steps > 1 else [0.0]
        return [_lerp_point(p0, p1, tv, clamp) for tv in t_values]

    t_seq = list(t)
    return [_lerp_point(p0, p1, tv, clamp) for tv in t_seq]
