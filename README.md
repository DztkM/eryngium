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


## Planned extensions (TODO): 
- (DONE) Contact graph (networkx)
- (DONE) Create SEIARD ABM
- (DONE) Create classical SEIRD ABM (to compare results)
- (DONE) Add Interventions module and lockdown intervention
- (25% DONE) Add school closure and masks interventions
- Add Age structure
- Find real medical parameters for models
- Compare results with scientific reports (maybe add module to compare model time_stamps with real data)
- ??? Create classical SIRD ABM (to compare results)
- ??? GUI application

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
