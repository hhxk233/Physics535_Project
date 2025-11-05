"""Spherical photon orbit mapping for Kerr shadow boundaries."""

from __future__ import annotations

import numpy as np


_FACEON_TOL = 1.0e-6


def horizon_radius(a: float) -> float:
    """Outer horizon radius r_plus = 1 + sqrt(1 - a^2)."""

    a_val = float(a)
    if abs(a_val) >= 1.0:
        raise ValueError("Spin parameter must satisfy |a| < 1.")
    return 1.0 + np.sqrt(1.0 - a_val * a_val)


def xi_eta_spherical(r: float, a: float) -> tuple[float, float]:
    """Constants of motion (xi, eta) for spherical photon orbits.

    Parameters
    ----------
    r : float
        Spherical photon-orbit radius with r > r_horizon.
    a : float
        Dimensionless Kerr spin parameter.
    """

    if abs(a) < 1.0e-12:
        raise ValueError("a=0 handled analytically; xi undefined due to division by a.")
    if r <= horizon_radius(a):
        raise ValueError("Radius must exceed the event horizon.")
    Delta = r * r - 2.0 * r + a * a
    Delta_p = 2.0 * r - 2.0
    if abs(Delta_p) < 1.0e-12:
        raise ValueError("Derivative of Delta too small for stable spherical orbit.")
    A = 4.0 * r * Delta / Delta_p
    xi = ((r * r + a * a) * Delta_p - 4.0 * r * Delta) / (a * Delta_p)
    B = (A * A) / Delta
    eta = B - (xi - a) * (xi - a)
    return float(xi), float(eta)


def screen_coords(xi: float, eta: float, a: float, inc_deg: float) -> tuple[float, float]:
    """Project constants of motion to observer screen coordinates (alpha, beta)."""

    i_rad = np.deg2rad(inc_deg)
    sin_i = np.sin(i_rad)
    cos_i = np.cos(i_rad)
    if abs(sin_i) < 1.0e-15:
        sin_i = np.sign(sin_i) * 1.0e-15 if sin_i != 0.0 else 1.0e-15
    alpha = -xi / sin_i
    beta_sq = eta + (a * a) * cos_i * cos_i - (xi * xi) * (cos_i * cos_i) / (sin_i * sin_i)
    if beta_sq < 0.0:
        return float("nan"), float("nan")
    beta = np.sqrt(beta_sq)
    return float(alpha), float(beta)


def _solve_face_on_radius(a: float) -> float:
    r_min = horizon_radius(a) + 1.0e-6
    r_max = 20.0
    grid = np.linspace(r_min, r_max, 2000)
    xi_vals = []
    for r in grid:
        try:
            xi_val, _ = xi_eta_spherical(float(r), a)
        except ValueError:
            xi_vals.append(np.nan)
            continue
        xi_vals.append(xi_val)
    xi_vals = np.asarray(xi_vals)
    valid = ~np.isnan(xi_vals)
    grid = grid[valid]
    xi_vals = xi_vals[valid]
    for idx in range(len(grid) - 1):
        f0 = xi_vals[idx]
        f1 = xi_vals[idx + 1]
        if f0 == 0.0:
            return float(grid[idx])
        if f0 * f1 < 0.0:
            lo = grid[idx]
            hi = grid[idx + 1]
            for _ in range(80):
                mid = 0.5 * (lo + hi)
                f_mid, _ = xi_eta_spherical(float(mid), a)
                if f_mid == 0.0:
                    return float(mid)
                if f0 * f_mid < 0.0:
                    hi = mid
                    f1 = f_mid
                else:
                    lo = mid
                    f0 = f_mid
            return float(0.5 * (lo + hi))
    raise RuntimeError("Unable to locate face-on spherical orbit for the provided spin.")


def _face_on_boundary(a: float, n: int) -> tuple[np.ndarray, np.ndarray]:
    if abs(a) < 1.0e-12:
        radius = np.sqrt(27.0)
    else:
        r_face = _solve_face_on_radius(a)
        xi_val, eta_val = xi_eta_spherical(r_face, a)
        radius = np.sqrt(eta_val + a * a)
        if not np.isfinite(radius):
            raise RuntimeError("Face-on radius computation failed.")
    theta = np.linspace(0.0, 2.0 * np.pi, n, endpoint=False)
    return radius * np.cos(theta), radius * np.sin(theta)


def shadow_boundary(a: float, inc_deg: float, n: int = 4000) -> tuple[np.ndarray, np.ndarray]:
    """Sample the spherical-photon family to trace the Kerr shadow boundary."""

    if n < 100:
        raise ValueError("Number of samples should be >= 100 for stability.")

    if abs(a) < 1.0e-12:
        theta = np.linspace(0.0, 2.0 * np.pi, n, endpoint=False)
        radius = np.sqrt(27.0)
        return radius * np.cos(theta), radius * np.sin(theta)

    if abs(np.sin(np.deg2rad(inc_deg))) < _FACEON_TOL:
        return _face_on_boundary(a, n)

    r_min = horizon_radius(a) + 1.0e-6
    r_max = 20.0
    r_grid = np.linspace(r_min, r_max, n // 2)
    points: list[tuple[float, float]] = []
    for r in r_grid:
        try:
            xi, eta_val = xi_eta_spherical(r, a)
        except ValueError:
            continue
        alpha, beta = screen_coords(xi, eta_val, a, inc_deg)
        if np.isnan(alpha) or np.isnan(beta):
            continue
        points.append((alpha, beta))
        points.append((alpha, -beta))

    if not points:
        return np.array([]), np.array([])

    pts = np.asarray(points)
    angles = np.arctan2(pts[:, 1], pts[:, 0])
    order = np.argsort(angles)
    pts = pts[order]
    return pts[:, 0], pts[:, 1]


def boundary_metrics(alpha: np.ndarray, beta: np.ndarray) -> dict:
    """Return basic diameters and equivalent circular radius for a boundary."""

    if alpha.size == 0 or beta.size == 0:
        return {"D_h": np.nan, "D_v": np.nan, "R_eq": np.nan}
    D_h = float(np.nanmax(alpha) - np.nanmin(alpha))
    D_v = float(np.nanmax(beta) - np.nanmin(beta))
    area = 0.5 * np.abs(np.dot(alpha, np.roll(beta, -1)) - np.dot(beta, np.roll(alpha, -1)))
    R_eq = float(np.sqrt(area / np.pi))
    return {"D_h": D_h, "D_v": D_v, "R_eq": R_eq}

