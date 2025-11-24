import matplotlib.pyplot as plt
import numpy as np
import networkx as nx
from matplotlib.animation import FuncAnimation
from typing import List, Dict



def plot_sir(time_series: dict[str, np.ndarray]):
    # Plot S(t), I(t), R(t) curves

    # Parameters:
    # time_series : dict[str, np.ndarray] (Dictionary with keys 'S', 'I', 'R')

    switcher = {
        "S": "Susceptible",
        "I": "Infectious",
        "R": "Recovered"
    }
    fig, ax = plt.subplots(figsize=(8, 5))
    for k, v in time_series.items():
        ax.plot(v, label=switcher[k])
    ax.set_xlabel("Day")
    ax.set_ylabel("Individuals")
    ax.set_title("ABM SIR Time Series")
    ax.legend()
    fig.tight_layout()
    ax.grid(True, linestyle="--", alpha=0.5)
    plt.show()

    return fig


def plot_seird(history: Dict[str, list[int]]):
    # Plot SEIR-D curves

    labels = {
        "S": "Susceptible",
        "E": "Exposed",
        "I": "Infectious",
        "R": "Recovered",
        "D": "Dead",
    }
    plt.figure(figsize=(8, 5))
    colors = {
        "S": "lightblue", "E": "orange", "I": "red", "R": "green", "D": "black"
    }
    for k, data in history.items():
        plt.plot(data, color=colors[k], label=labels[k])
    plt.xlabel("Day")
    plt.ylabel("Individuals")
    plt.title("Network-based SEIR-D ABM Time Series")
    plt.legend()
    plt.grid(True, linestyle="--", alpha=0.5)
    plt.tight_layout()
    plt.show()



def plot_seiard(history: Dict[str, list[int]]):
    # Plot SEIAR-D curves

    labels = {
        "S": "Susceptible",
        "E": "Exposed",
        "IA": "Infectious Asymptomatic",
        "IS": "Infectious Symptomatic",
        "R": "Recovered",
        "D": "Dead",
    }
    plt.figure(figsize=(8, 5))
    colors = {
        "S": "lightblue", "E": "orange", "IA": "purple",
        "IS": "red", "R": "green", "D": "black"
    }
    for k, data in history.items():
        plt.plot(data, color=colors[k], label=labels[k])
    plt.xlabel("Day")
    plt.ylabel("Individuals")
    plt.title("Network-based SEIAR-D ABM Time Series")
    plt.legend()
    plt.grid(True, linestyle="--", alpha=0.5)
    plt.tight_layout()
    plt.show()


def plot_network(G, agent_states=None, figsize=(6, 6), model_type = "SIR"):
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
    elif model_type == "SIR":
        # map S/I/R -> colors
        color_map = {0: "lightblue", 1: "red", 2: "green"}
        colors = [color_map[s] for s in agent_states]
    elif model_type =="SEIRD" or model_type =="SEIR":
        color_map = {0: "lightblue", 1: "orange", 2: "red",
            3: "green", 4: "black"}
        colors = [color_map[s] for s in agent_states]
    elif model_type =="SEIARD" or model_type =="SEIAR":
        color_map = {0: "lightblue", 1: "orange", 2: "purple",
            3: "red", 4: "green", 5: "black"}
        colors = [color_map[s] for s in agent_states]
    else:
        raise ValueError(
            "Unknown `model_type`"
        )

    nx.draw(G, pos, node_color=colors, node_size=50, with_labels=False)
    plt.show()


def animate_network_spread(model, interval=300, figsize=(6,6), model_type = "SIR"):
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
    color_map = {}
    if model_type == "SIRD" or model_type == "SIR":
        # map S/I/R -> colors
        color_map = {0: "lightblue", 1: "red", 2: "green", 3: "black"}
    elif model_type =="SEIRD" or model_type =="SEIR":
        color_map = {0: "lightblue", 1: "orange", 2: "red",
            3: "green", 4: "black"}
    elif model_type =="SEIARD" or model_type =="SEIAR":
        color_map = {0: "lightblue", 1: "orange", 2: "purple",
            3: "red", 4: "green", 5: "black"}
    else:
        raise ValueError(
            "Unknown `model_type`"
        )
    
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