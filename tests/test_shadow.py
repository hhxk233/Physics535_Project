import itertools

import numpy as np

from src.physics.shadow import boundary_metrics, shadow_boundary


def circle_stats(alpha: np.ndarray, beta: np.ndarray) -> tuple[float, float]:
    x0 = np.mean(alpha)
    y0 = np.mean(beta)
    radii = np.sqrt((alpha - x0) ** 2 + (beta - y0) ** 2)
    return float(np.mean(radii)), float(np.std(radii))


def test_schwarzschild_circle():
    alpha, beta = shadow_boundary(0.0, 45.0, n=2048)
    mean_r, std_r = circle_stats(alpha, beta)
    assert abs(mean_r - np.sqrt(27.0)) < 1e-3
    assert std_r < 1e-3


def test_face_on_symmetry():
    alpha, beta = shadow_boundary(0.9, 0.0, n=4096)
    assert abs(np.nanmax(alpha) + np.nanmin(alpha)) < 1e-3


def test_no_nans_across_grid():
    spins = [0.0, 0.5, 0.9]
    inclinations = [0.0, 30.0, 60.0, 90.0]
    for a, inc in itertools.product(spins, inclinations):
        alpha, beta = shadow_boundary(a, inc, n=1024)
        assert not np.any(np.isnan(alpha))
        assert not np.any(np.isnan(beta))


def test_boundary_metrics_valid():
    alpha, beta = shadow_boundary(0.5, 60.0, n=2048)
    metrics = boundary_metrics(alpha, beta)
    assert metrics["D_h"] > 0.0
    assert metrics["D_v"] > 0.0
    assert metrics["R_eq"] > 0.0

