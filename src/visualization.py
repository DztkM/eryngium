import matplotlib.pyplot as plt
import numpy as np
import networkx as nx
from matplotlib.animation import FuncAnimation
from typing import List, Dict
import matplotlib.patches as mpatches

COLORS = {
    "S": "lightblue", 
    "E": "orange", 
    "IA": "purple",
    "IS": "red",
    "I": "red", 
    "R": "green", 
    "D": "black"
}

LABELS = {
    "S": "Susceptible",
    "E": "Exposed",
    "IA": "Infectious Asymptomatic",
    "IS": "Infectious Symptomatic",
    "I": "Infectious",
    "R": "Recovered",
    "D": "Dead",
}

def plot_history(history: Dict[str, list[int]], model_type = "SIR"):
    # Plot S(t), I(t), R(t) (and other) curves depending on the model type
    # 
    # Parameters:
    # history   : dict[str, list[int]] (Dictionary with keys 'S', 'I', 'R'...)
    # model_type    : str; ex: "SIR", "SEIR", "SEIRD", "SEIAR", "SEIARD"
    # 
    # Returns:
    # plt.figure.Figure

    fig, ax = plt.subplots(figsize=(8, 5))
    for k, data in history.items():
        plt.plot(data, color=COLORS[k], label=LABELS[k])
    ax.set_xlabel("Day")
    ax.set_ylabel("Individuals")
    ax.set_title(f"ABM {model_type} Time Series")
    ax.legend()
    fig.tight_layout()
    ax.grid(True, linestyle="--", alpha=0.5)
    plt.show()

    return fig


def plot_network(G, agent_states=None, figsize=(6, 6), model_type = "SIR"):
    # Draw contact network using spring-layout

    # Parameters:
    # G : networkx.Graph (Contact graph)
    # agent_states : list[int] | None
    #   if None -> all nodes with the same color

    plt.figure(figsize=figsize)

    # Position nodes using spring (force) layout
    pos = nx.spring_layout(G, seed=42)

    if agent_states is None:
        # all nodes with the same color
        colors = "lightblue"
    elif model_type == "SIR":
        # map S/I/R -> colors
        color_map = {0: "lightblue", 1: "red", 2: "green"}
        colors = [color_map[s] for s in agent_states]
    elif model_type =="SEIRD" or model_type =="SEIR":
        # map S/E/I/R/D -> colors
        color_map = {0: "lightblue", 1: "orange", 2: "red",
            3: "green", 4: "black"}
        colors = [color_map[s] for s in agent_states]
    elif model_type =="SEIARD" or model_type =="SEIAR":
        # map S/E/IA/IS/R/D -> colors
        color_map = {0: "lightblue", 1: "orange", 2: "purple",
            3: "red", 4: "green", 5: "black"}
        colors = [color_map[s] for s in agent_states]
    else:
        raise ValueError(
            "Unknown `model_type`"
        )

    nx.draw(G, pos, node_color=colors, node_size=42, with_labels=False)
    plt.show()


def animate_network_spread(model, interval=150, figsize=(12, 12), model_type="SIR"):
    # Animate infection spread on the model's network.

    if not hasattr(model, "history_states"):
        raise ValueError(
            "Model must store daily node state history in model.history_states. "
            "Modify step() to append `[a.state for a in agents]` each day."
        )

    G = model.G
    history = model.history_states  # list of length T, each entry = list of states per node
    T = len(history)

    pos = nx.spring_layout(G, seed=42, iterations=100)

    fig, ax = plt.subplots(figsize=figsize)
    ax.margins(0.01)
    ax.set_title(f"{model_type} Spread Over Network") 
    
    # Color map
    state_keys = []
    if model_type == "SIRD" or model_type == "SIR":
        state_keys = ["S", "I", "R"]
    elif model_type == "SEIRD" or model_type == "SEIR":
        state_keys = ["S", "E", "I", "R", "D"]
    elif model_type == "SEIARD" or model_type == "SEIAR":
        state_keys = ["S", "E", "IS", "IA", "R", "D"]
    else:
        raise ValueError("Unknown `model_type`")
    
    color_map = {i: COLORS[key] for i, key in enumerate(state_keys) if key in COLORS}

    legend_handles = []
    for key in state_keys:
        if key in COLORS and key in LABELS:
            patch = mpatches.Patch(color=COLORS[key], label=LABELS[key])
            legend_handles.append(patch)
    
    ax.legend(handles=legend_handles, loc="upper right", title="Agent state")
    
    initial_states = history[0]
    node_colors = [color_map[s] for s in initial_states]

    # Edges printing
    edges = nx.draw_networkx_edges(G, pos, ax=ax, width=0.1, alpha=0.5, edge_color="gray")

    # Nodes printing
    nodes = nx.draw_networkx_nodes(G, pos, node_color=node_colors, node_size=35, ax=ax)

    ax.set_axis_off()

    def update(frame):
        # Update node colors for frame t
        states = history[frame]
        node_colors = [color_map[s] for s in states]       
        nodes.set_color(node_colors)             
        ax.set_title(f"{model_type} day {frame}")
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