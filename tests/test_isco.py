import numpy as np

from src.physics.isco import eta, r_isco


def test_schwarzschild_r_isco():
    assert abs(r_isco(0.0, prograde=True) - 6.0) < 1e-12


def test_schwarzschild_eta():
    expected = 1.0 - np.sqrt(8.0 / 9.0)
    assert abs(eta(0.0, prograde=True) - expected) < 1e-6


def test_monotonic_trends():
    a_grid = np.linspace(0.0, 0.99, 200)
    prograde = r_isco(a_grid, prograde=True)
    retrograde = r_isco(a_grid, prograde=False)
    assert np.all(np.diff(prograde) < 0.0)
    assert np.all(np.diff(retrograde) > 0.0)

