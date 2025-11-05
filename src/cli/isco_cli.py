"""Command-line demo for ISCO radii and efficiencies."""

from __future__ import annotations

import argparse
import numpy as np

from src.physics.isco import eta, r_isco


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Print ISCO radii and efficiencies.")
    parser.add_argument(
        "--samples",
        type=int,
        default=9,
        help="Number of sample points between a_min and a_max (default: 9).",
    )
    parser.add_argument(
        "--a-min",
        type=float,
        default=-0.99,
        help="Minimum spin value (default: -0.99).",
    )
    parser.add_argument(
        "--a-max",
        type=float,
        default=0.99,
        help="Maximum spin value (default: 0.99).",
    )
    return parser.parse_args()


def format_row(spin: float, r_pro: float, r_retro: float, eta_pro: float, eta_retro: float) -> str:
    return (
        f"{spin:+.3f}"
        f"  {r_pro:8.5f}  {eta_pro:8.6f}"
        f"  {r_retro:8.5f}  {eta_retro:8.6f}"
    )


def main() -> None:
    args = parse_args()
    spins = np.linspace(args.a_min, args.a_max, args.samples)
    header = (
        " a      r_ISCO(pro)   eta(pro)   r_ISCO(ret)   eta(ret)"
    )
    print(header)
    for spin in spins:
        r_pro = r_isco(spin, prograde=True)
        r_retro = r_isco(spin, prograde=False)
        eta_pro = eta(spin, prograde=True)
        eta_retro = eta(spin, prograde=False)
        print(format_row(spin, r_pro, r_retro, eta_pro, eta_retro))


if __name__ == "__main__":
    main()

