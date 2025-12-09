import csv
from datetime import datetime

def load_data(csv_path: str, population: int = 125_000, inf_period_mean: int = 8):
    dates = []
    cumulative_cases = []
    
    with open(csv_path, newline='', encoding="utf-8") as f:
        reader = csv.DictReader(f, delimiter=';')
        for row in reader:
            dt = datetime.strptime(row["Date"], "%m/%d/%Y")
            dates.append(dt)

            cumulative_cases.append(int(row["Cumulative Total Cases"]))

    I_cumulative = cumulative_cases[:]
    I = estimate_active_from_cumulative(cumulative_cases[:], inf_period_mean)
    S = [population - i for i in I]

    return {
        "dates": dates,
        "S": S,
        "I": I,
        "I_cum": I_cumulative,
    }


def estimate_active_from_cumulative(cumulative, D=8):
    active = []
    for t in range(len(cumulative)):
        if t < D:
            active.append(0)
        else:
            active.append(cumulative[t] - cumulative[t - D])

    for t in range(0, D):
        active[t] = active[D+1]

    return active