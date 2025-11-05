# ISCO and Kerr Shadow Toolkit

Tools for exploring equatorial ISCO radii, radiative efficiency, and Kerr black hole shadow boundaries in geometric units (G=c=M=1).

## Quickstart

### Makefile workflow

```powershell
make setup   # create .venv and install project in editable mode
make test    # run pytest -q
make figs    # generate publication-quality figures under fig/
make gif     # build spin and inclination sweep GIFs
```

### Manual steps

```powershell
python -m venv .venv
.\.venv\Scripts\Activate.ps1
pip install -e .
pytest -q
python -m src.cli.make_figs --panels all
make gif
```

## Command-line tools

- `python -m src.cli.isco_cli` prints ISCO radii and efficiencies for a grid of spins.
- `python -m src.cli.make_figs --panels all` recreates the standard figure suite.

## Physics checks

- a = 0 should give r_ISCO = 6 and eta about 0.057191.
- The Schwarzschild shadow radius should be close to sqrt(27) ~ 5.196 and circular within 1e-3.
- Face-on inclination (i = 0 deg) keeps the shadow circular and left-right symmetric.

Figures and GIFs are saved to `fig/`. CSV tables, if produced, belong in `data/`.

