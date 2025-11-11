import matplotlib.pyplot as plt
import numpy as np
import networkx as nx


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


def plot_network(G, agent_states=None, figsize=(6, 6)):
    # Draw contact network using spring-layout

    # Parameters:
    # G : networkx.Graph (Contact graph)
    # agent_states : list[int] | None
    #   Optional list of SIR states to color nodes:
    #   0=SUSC (blue), 1=INF (red), 2=REC (green)
    #   If None → all nodes same color

    plt.figure(figsize=figsize)

    # Position nodes using spring (force) layout
    pos = nx.spring_layout(G, seed=42)

    if agent_states is None:
        # all nodes one color
        colors = "lightblue"
    else:
        # map S/I/R -> colors
        color_map = {0: "lightblue", 1: "red", 2: "green"}
        colors = [color_map[s] for s in agent_states]

    nx.draw(G, pos, node_color=colors, node_size=50, with_labels=False)
    plt.show()