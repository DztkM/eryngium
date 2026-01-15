# Symulacje Dystemów Dyskretnych, AGH, ISI

### [Eryngium](https://en.wikipedia.org/wiki/Eryngium)


This is a university project for the "Symulacje Systemów Dyskretnych 2025/2026" course. The application is an agent-based (ABM) pandemic simulator.

## Authors (Group 1):

- Maksim Dziatkou
- Mateusz Działowski
- Filip Duda

## Sources: 
- [ABM of Epidemic Spread](https://ieeexplore.ieee.org/abstract/document/6113095)
- [COVID-19 Case Count by Date (Cambridge Open Data Portal)](https://data.cambridgema.gov/Public-Health/COVID-19-Case-Count-by-Date-3-1-2020-11-24-2022/axxk-jvk8/about_data)

## How To Run:

### UV
[install uv](https://docs.astral.sh/uv/getting-started/installation/)

### Install dependencies
```bash
uv sync
```

### Run main.py in console
```bash
cd /eryngium
uv run ./src/main.py
```

### Run app in streamlit
```bash
cd /eryngium
streamlit run ./src/web_app/app.py
```

### Add package:
```
uv add [package-name]
```
