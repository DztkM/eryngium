import matplotlib.pyplot as plt
import numpy as np

def plot_sir(time_series: dict[str, np.ndarray]) -> None:
    # Plot S(t), I(t), R(t) curves

    # Parameters:
    # time_series : dict[str, np.ndarray] (Dictionary with keys 'S', 'I', 'R')

    switcher = {
        "S": "Susceptible",
        "I": "Infectious",
        "R": "Recovered"
    }
    plt.figure(figsize=(8, 5))
    for k, v in time_series.items():
        plt.plot(v, label=switcher[k])
    plt.xlabel("Day")
    plt.ylabel("Population Count")
    plt.title("ABM SIR Time Series")
    plt.legend()
    plt.tight_layout()
    plt.show()
