"""ISCO radius and radiative efficiency utilities for Kerr black holes.

All quantities assume geometric units with G = c = M = 1.
"""

from __future__ import annotations

import numpy as np


def _validate_spin(a: np.ndarray) -> None:
    if np.any(np.abs(a) >= 1.0):
        raise ValueError("Spin parameter must satisfy |a| < 1.")


def z1(a: float) -> float:
    """Intermediate quantity Z1(a) from Bardeen et al. (1972).

    Parameters
    ----------
    a : float
        Dimensionless spin parameter with |a| < 1.
    """

    a_arr = np.asarray(a, dtype=float)
    _validate_spin(a_arr)
    abs_a = np.abs(a_arr)
    term = np.cbrt(1.0 - abs_a * abs_a)
    z1_val = 1.0 + term * (np.cbrt(1.0 + abs_a) + np.cbrt(1.0 - abs_a))
    return float(z1_val)


def z2(a: float) -> float:
    """Intermediate quantity Z2(a) from Bardeen et al. (1972)."""

    z1_val = z1(a)
    a_val = float(a)
    return float(np.sqrt(3.0 * a_val * a_val + z1_val * z1_val))


def r_isco(a: float | np.ndarray, prograde: bool = True) -> np.ndarray | float:
    """Bardeen-Novikov-Thorne ISCO radius for equatorial orbits."""

    a_arr = np.asarray(a, dtype=float)
    _validate_spin(a_arr)
    abs_a = np.abs(a_arr)
    term = np.cbrt(1.0 - abs_a * abs_a)
    z1_val = 1.0 + term * (np.cbrt(1.0 + abs_a) + np.cbrt(1.0 - abs_a))
    z2_val = np.sqrt(3.0 * abs_a * abs_a + z1_val * z1_val)
    root = np.sqrt((3.0 - z1_val) * (3.0 + z1_val + 2.0 * z2_val))
    sigma = -1.0 if prograde else 1.0
    radius = 3.0 + z2_val + sigma * root
    return float(radius) if np.isscalar(a_arr) else radius


def E_equatorial(r: float | np.ndarray, a: float | np.ndarray, prograde: bool = True) -> np.ndarray | float:
    """Specific energy for equatorial circular geodesics."""

    r_arr = np.asarray(r, dtype=float)
    a_arr = np.asarray(a, dtype=float)
    if np.any(r_arr <= 0.0):
        raise ValueError("Radius must be positive.")
    _validate_spin(a_arr)
    abs_a = np.abs(a_arr)
    a_term = abs_a if prograde else -abs_a
    sqrt_r = np.sqrt(r_arr)
    r32 = r_arr * sqrt_r
    numerator = r32 - 2.0 * sqrt_r + a_term
    inner = r32 - 3.0 * sqrt_r + 2.0 * a_term
    if np.any(inner <= 0.0):
        raise ValueError("Geodesic is not stable at the supplied radius.")
    denominator = np.power(r_arr, 0.75) * np.sqrt(inner)
    energy = numerator / denominator
    return float(energy) if np.isscalar(r_arr) and np.isscalar(a_arr) else energy


def eta(a: float | np.ndarray, prograde: bool = True) -> np.ndarray | float:
    """Radiative efficiency eta(a) = 1 - E_ISCO."""

    radii = r_isco(a, prograde=prograde)
    energies = E_equatorial(radii, a, prograde=prograde)
    efficiency = 1.0 - energies
    radii_arr = np.asarray(radii)
    return float(efficiency) if np.isscalar(radii_arr) else efficiency

