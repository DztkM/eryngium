# Symulacje Dystemów Dyskretnych, AGH, ISI

### [Eryngium](https://en.wikipedia.org/wiki/Eryngium)


This is a university project for the "Symulacje Systemów Dyskretnych 2025/2026" course. The application is an agent-based (ABM) pandemic simulator.

## Authors (Group 1):

- Maksim Dziatkou
- Mateusz Działowski
- Filip Duda

## (TODO) Sources: 
- https://ieeexplore.ieee.org/abstract/document/6113095

## Current state:

Alpha version of an agent-based (ABM) SIR epidemic simulator.

NOTE: This is a minimal intentionally compact version.
It is designed to be extensible rather than final.


## Planned extensions:
- Add E stage (SEIR)
- Age structure
- Contact graph (networkx)
- Interventions: lockdown, school closure, masks
- Data export utilities
- GUI application?

## How To Run:

### UV
[install uv](https://docs.astral.sh/uv/getting-started/installation/)

### Install dependencies
```bash
uv sync
```

### Run main.py
```bash
cd /eryngium
uv run ./src/main.py
```

### Add package:
```
uv add [package-name]
```