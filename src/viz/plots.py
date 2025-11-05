"""Plotting utilities for ISCO trends and Kerr shadow boundaries."""

from __future__ import annotations

from pathlib import Path
from typing import Iterable

import matplotlib

matplotlib.use("Agg", force=True)
import matplotlib.pyplot as plt
import numpy as np

from src.physics.isco import eta as eta_fn
from src.physics.isco import r_isco
from src.physics.shadow import shadow_boundary


def _ensure_dir(figdir: str | Path) -> Path:
    path = Path(figdir)
    path.mkdir(parents=True, exist_ok=True)
    return path


def _save(fig: plt.Figure, base: Path) -> None:
    pdf_path = base.parent / f"{base.name}.pdf"
    png_path = base.parent / f"{base.name}.png"
    fig.savefig(pdf_path, bbox_inches="tight")
    fig.savefig(png_path, dpi=300, bbox_inches="tight")
    plt.close(fig)


def _set_shadow_axes(ax: plt.Axes) -> None:
    ax.set_aspect("equal", adjustable="box")
    ax.set_xlabel(r"$\alpha$ [M]")
    ax.set_ylabel(r"$\beta$ [M]")


def plot_isco_eta(a_grid: np.ndarray, figdir: str = "fig") -> None:
    """Plot ISCO radius and efficiency over a grid of spin values."""

    fig_path = _ensure_dir(figdir)

    r_pro = r_isco(a_grid, prograde=True)
    r_retro = r_isco(a_grid, prograde=False)

    fig, ax = plt.subplots(figsize=(6.5, 4.5))
    ax.plot(a_grid, r_pro, label="prograde")
    ax.plot(a_grid, r_retro, label="retrograde")
    ax.set_xlabel("spin a")
    ax.set_ylabel(r"$r_{\mathrm{ISCO}}$ [M]")
    ax.legend()
    ax.grid(True, which="major", alpha=0.2)
    _save(fig, fig_path / "isco_radius_vs_a")

    fig, ax = plt.subplots(figsize=(6.5, 4.5))
    ax.plot(a_grid, eta_fn(a_grid, prograde=True), label=r"$\eta$ prograde")
    ax.plot(a_grid, eta_fn(a_grid, prograde=False), label=r"$\eta$ retrograde")
    ax.set_xlabel("spin a")
    ax.set_ylabel(r"$\eta$")
    ax.legend()
    ax.grid(True, which="major", alpha=0.2)
    _save(fig, fig_path / "eta_vs_a")


def plot_shadow_family_for_a(a_list: Iterable[float], inc_deg: float, figdir: str = "fig") -> None:
    """Overlay multiple spin values at fixed inclination."""

    fig_path = _ensure_dir(figdir)
    fig, ax = plt.subplots(figsize=(6.0, 6.0))
    for a in a_list:
        alpha, beta = shadow_boundary(a, inc_deg, n=4096)
        ax.plot(alpha, beta, label=f"a={a:+.2f}")
    _set_shadow_axes(ax)
    ax.legend(frameon=False)
    ax.grid(True, which="major", alpha=0.2)
    _save(fig, fig_path / f"shadow_multi_a_i{int(round(inc_deg))}")


def plot_shadow_family_for_i(inc_list: Iterable[float], a: float, figdir: str = "fig") -> None:
    """Overlay multiple inclinations for a fixed spin."""

    fig_path = _ensure_dir(figdir)
    fig, ax = plt.subplots(figsize=(6.0, 6.0))
    for inc in inc_list:
        alpha, beta = shadow_boundary(a, inc, n=4096)
        ax.plot(alpha, beta, label=f"i={inc:.0f} deg")
    _set_shadow_axes(ax)
    ax.legend(frameon=False)
    ax.grid(True, which="major", alpha=0.2)
    _save(fig, fig_path / f"shadow_multi_i_a{a:+.2f}")

