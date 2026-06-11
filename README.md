# Space Simulation

A Python 2D orbital simulation focused on measurable physics, not only visuals. The current version models the Sun-Earth system with Newtonian gravity and a leapfrog integrator.

## What This Is

This project is a staged space-simulation portfolio project. The immediate goal is a validated Earth-Sun orbit, then a config-driven multi-planet system, followed by larger N-body simulations and performance benchmarks.

## Simulation Accuracy

To verify the mathematical accuracy of the second-order Leapfrog integration engine, orbital periods were tracked automatically by calculating cumulative angular displacement ($2\pi$ radians) relative to the Sun. 

| Celestial Body | Target Period (Earth Days) | Simulated Period (Earth Days) | Absolute Error (Days) | Accuracy % |
| :--- | :--- | :--- | :--- | :--- |
| **Mercury** | 87.97 | 87.96 | 0.01 | 99.99% |
| **Venus** | 224.70 | 224.12 | 0.58 | 99.74% |
| **Earth** | 365.26 | 364.92 | 0.34 | 99.91% |
| **Mars** | 686.98 | 686.12 | 0.86 | 99.87% |
| **Jupiter** | 4,332.59 | 4,332.12 | 0.47 | 99.99% |
| **Saturn** | 10,759.22 | 10,720.96 | 38.26 | 99.64% |
| **Uranus** | 30,688.50 | 30,277.46 | 411.04 | 98.66% |
| **Neptune** | 60,182.00 | 59,518.08 | 663.92 | 98.90% |

Known values are taken from the NASA Planetary Fact Sheet. More bodies will be added to this table when the config expands beyond the current Sun-Earth setup.

## Features

- Newtonian gravitational force calculation between bodies
- Euler and leapfrog integration implementations
- Config-driven body loading from JSON
- Pygame rendering with orbit trails
- Pytest coverage for gravity and orbital regression behavior
- Benchmark script for measuring simulated orbital period

## Physics Engine

The core simulation uses pairwise Newtonian gravity in SI units. Leapfrog integration is the preferred integrator because orbital energy oscillates around a stable value instead of drifting monotonically like Euler integration.

Current simplifications:

- Bodies are treated as point masses for gravity.
- The Sun starts fixed at the origin but still participates in force calculations.
- Relativity, rotation, collisions, and non-gravitational forces are not modeled yet.
- Rendered body sizes are exaggerated so planets remain visible.

## Architecture

```text
space-sim/
├── src/
│   ├── core/       # Body model, gravity, and integrators
│   ├── io/         # JSON config loading
│   ├── rendering/  # Pygame coordinate conversion and drawing helpers
│   └── utils/      # Vector math and physical constants
├── tests/          # Physics and regression tests
├── benchmarks/     # Measurement and comparison scripts
├── configs/        # Simulation initial conditions
└── DECISIONS.md    # Technical decision log
```

## Design Decisions

The main documented decision so far is the Phase 2 integrator choice: leapfrog over Euler for stable long-term orbital behavior. See `DECISIONS.md` for the evidence and reasoning.

## Running It

```bash
pip install -r requirements.txt
python main.py
```

Run tests:

```bash
pytest tests/ -v
```

Measure the current Earth orbital period:

```bash
python benchmarks/measure_period.py
```