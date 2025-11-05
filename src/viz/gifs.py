"""Utilities for synthesising Kerr shadow GIFs."""

from __future__ import annotations

from pathlib import Path

import imageio.v2 as imageio
import matplotlib

matplotlib.use("Agg", force=True)
import matplotlib.pyplot as plt
import numpy as np

from src.physics.shadow import shadow_boundary


def _ensure_dir(path: Path) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)


def _frame(alpha: np.ndarray, beta: np.ndarray, title: str) -> np.ndarray:
    fig, ax = plt.subplots(figsize=(4.0, 4.0), dpi=200)
    ax.plot(alpha, beta, color="black")
    ax.set_aspect("equal", adjustable="box")
    ax.set_xlabel(r"$\alpha$ [M]")
    ax.set_ylabel(r"$\beta$ [M]")
    ax.set_title(title)
    ax.grid(True, which="major", alpha=0.2)
    fig.tight_layout()
    fig.canvas.draw()
    buffer = np.asarray(fig.canvas.buffer_rgba())
    image = buffer[:, :, :3].copy()
    plt.close(fig)
    return image


def spin_sweep_gif(
    a_start: float = 0.0,
    a_end: float = 0.998,
    frames: int = 40,
    i: float = 60.0,
    out: str = "fig/shadow_spin_sweep.gif",
) -> Path:
    """Animate the shadow as the spin parameter varies linearly."""

    spins = np.linspace(a_start, a_end, frames)
    images = []
    for a in spins:
        alpha, beta = shadow_boundary(float(a), i, n=2048)
        images.append(_frame(alpha, beta, title=f"a = {a:+.3f}, i = {i:.1f} deg"))
    output = Path(out)
    _ensure_dir(output)
    imageio.mimsave(output, images, duration=0.1)
    return output


def inclination_sweep_gif(
    a: float = 0.9,
    i_start: float = 0.0,
    i_end: float = 90.0,
    frames: int = 40,
    out: str = "fig/shadow_incl_sweep.gif",
) -> Path:
    """Animate the shadow as the observer inclination varies linearly."""

    inclinations = np.linspace(i_start, i_end, frames)
    images = []
    for inc in inclinations:
        alpha, beta = shadow_boundary(a, float(inc), n=2048)
        images.append(_frame(alpha, beta, title=f"a = {a:+.3f}, i = {inc:.1f} deg"))
    output = Path(out)
    _ensure_dir(output)
    imageio.mimsave(output, images, duration=0.1)
    return output


def main() -> None:
    spin_sweep_gif()
    inclination_sweep_gif()


if __name__ == "__main__":
    main()

