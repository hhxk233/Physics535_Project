"""Generate figures for the ISCO and Kerr shadow project."""

from __future__ import annotations

import argparse
from typing import Iterable

import numpy as np

from src.viz.plots import (
    plot_isco_eta,
    plot_shadow_family_for_a,
    plot_shadow_family_for_i,
)


DEFAULT_A_LIST = [-0.9, -0.5, 0.0, 0.5, 0.9]
DEFAULT_I_LIST = [0.0, 30.0, 60.0, 90.0]


def _parse_float_list(text: str | None, fallback: Iterable[float]) -> list[float]:
    if not text:
        return list(fallback)
    return [float(item.strip()) for item in text.split(",") if item.strip()]


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Create reproducible figures for the project.")
    parser.add_argument(
        "--panels",
        type=str,
        default="all",
        choices=["isco", "shadows_a", "shadows_i", "all"],
        help="Figure panels to generate (default: all).",
    )
    parser.add_argument(
        "--a-list",
        type=str,
        default=None,
        help="Comma-separated spin values for shadow overlays.",
    )
    parser.add_argument(
        "--i-list",
        type=str,
        default=None,
        help="Comma-separated inclination values for shadow overlays.",
    )
    parser.add_argument(
        "--a-grid",
        type=int,
        default=200,
        help="Number of samples for the ISCO/eta grid (default: 200).",
    )
    parser.add_argument(
        "--figdir",
        type=str,
        default="fig",
        help="Output directory for figures (default: fig).",
    )
    return parser.parse_args()


def main() -> None:
    args = parse_args()
    a_list = _parse_float_list(args.a_list, DEFAULT_A_LIST)
    i_list = _parse_float_list(args.i_list, DEFAULT_I_LIST)
    panels = {args.panels} if args.panels != "all" else {"isco", "shadows_a", "shadows_i"}

    if "isco" in panels:
        a_grid = np.linspace(-0.99, 0.99, args.a_grid)
        plot_isco_eta(a_grid, figdir=args.figdir)

    if "shadows_a" in panels:
        inc = float(i_list[-1]) if args.i_list else 60.0
        plot_shadow_family_for_a(a_list, inc_deg=inc, figdir=args.figdir)

    if "shadows_i" in panels:
        a_value = a_list[-1] if a_list else 0.9
        plot_shadow_family_for_i(i_list, a=a_value, figdir=args.figdir)


if __name__ == "__main__":
    main()

