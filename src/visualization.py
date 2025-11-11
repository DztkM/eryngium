import matplotlib.pyplot as plt
import numpy as np
import networkx as nx
from matplotlib.animation import FuncAnimation


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


def animate_network_spread(model, interval=300, figsize=(6,6)):
    # Animate the SIR spread on the model's network.

    # Parameters:
    # model : ABMNetwork
    #       The network-based model that has already been run() for N days
    #       and contains daily_S, daily_I, daily_R, agents states per day
    # interval : int (Milliseconds per frame)
    # figsize : tuple (Figure size)

    if not hasattr(model, "history_states"):
        raise ValueError(
            "Model must store daily node state history in model.history_states. "
            "Modify step() to append `[a.state for a in agents]` each day."
        )
    
    G = model.G
    history = model.history_states # list of length T, each entry = list of states per node
    T = len(history)

    # Node positions (static layout)
    pos = nx.spring_layout(G, seed=42)

    fig, ax = plt.subplots(figsize=figsize)
    ax.set_title("SIR Spread Over Network")

    # Color map
    color_map = {0: "lightblue",    # susceptible
                 1: "red",          # infected
                 2: "green"}        # recovered
    
    # Initial node color state
    node_colors = [color_map[s] for s in history[0]]

    # Draw initial frame
    nodes = nx.draw_networkx_nodes(G, pos, node_color=node_colors, node_size=60, ax=ax)
    edges = nx.draw_networkx_edges(G, pos, ax=ax)

    ax.set_axis_off()

    def update(frame):
        # Update node colors for frame t
        states = history[frame]
        node_colors = [color_map[s] for s in states]
        nodes.set_color(node_colors)
        ax.set_title(f"Day {frame}")
        return nodes,

    ani = FuncAnimation(
        fig,
        update,
        frames=T,
        interval=interval,
        blit=False,
        repeat=False
    )

    plt.show()
    return ani