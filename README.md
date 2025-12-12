# Symulacje Dystemów Dyskretnych, AGH, ISI

### [Eryngium](https://en.wikipedia.org/wiki/Eryngium)


This is a university project for the "Symulacje Systemów Dyskretnych 2025/2026" course. The application is an agent-based (ABM) pandemic simulator.

## Authors (Group 1):

- Maksim Dziatkou
- Mateusz Działowski
- Filip Duda

## Sources: 
- (re-check) [ABM of Epidemic Spread](https://ieeexplore.ieee.org/abstract/document/6113095)
- [COVID-19 Case Count by Date (Cambridge Open Data Portal)](https://data.cambridgema.gov/Public-Health/COVID-19-Case-Count-by-Date-3-1-2020-11-24-2022/axxk-jvk8/about_data)

## Current state:

Alpha version of an agent-based (ABM) SIR epidemic simulator.

NOTE: This is a minimal intentionally compact version.
It is designed to be extensible rather than final.


## Planned extensions (TODO): 
- (DONE) Contact graph (networkx)
- (DONE) Create SEIARD ABM
- (DONE) Create classical SEIRD ABM (to compare results)
- (DONE) Add Interventions module and lockdown intervention
- (DONE) Add masks intervention
- Add school closure intervention
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
