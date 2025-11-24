import random
from typing import List, Dict
import numpy as np
import networkx as nx

from abm_network import ABMNetwork
from seird.config_seird import ConfigSEIRD
from seird.agent_seird import AgentSEIRD

class ABMNetworkSEIRD(ABMNetwork):
    # Network-based SEIAR-D epidemic simulator

    def __init__(self, cfg: ConfigSEIRD, network_type: str = "erdos_renyi", **net_params):
        self.cfg = cfg
        self._init_rng()

         # Create agents (initially all susceptible)
        self.agents: List[AgentSEIRD] = [AgentSEIRD(cfg) for _ in range(cfg.N)]

        # Infect I0 randomly
        initial_I = random.sample(range(cfg.N), cfg.I0)
        for idx in initial_I:
            self.agents[idx].state = AgentSEIRD.E
        
        self.cfg = cfg
        self.network_type = network_type
        self.net_params = net_params
        self.G = self._create_network()

        # Time-series tracking (store S/E/IA/IS/R/D counts per day)
        self.history: Dict[str, list[int]] = {k: [] for k in ["S", "E", "I", "R", "D"]}
        self.history_states: list[list[int]] = [] # stores list of agent states each day
        
        self.day: int = 0
        self.finished = False


    # === PHASE 0 ===
    def _should_continue(self) -> bool:
        # Check if epidemic is still active
        # Default behavior: stop when no infected remain

        any_infected = any(a.state in [AgentSEIRD.E, AgentSEIRD.I] for a in self.agents)
        return any_infected


    # === PHASE 4 ===
    def _log_states(self) -> None:
        # Count all states for logging
        states = [a.state for a in self.agents]
        self.history["S"].append(states.count(AgentSEIRD.S))
        self.history["E"].append(states.count(AgentSEIRD.E))
        self.history["I"].append(states.count(AgentSEIRD.I))
        self.history["R"].append(states.count(AgentSEIRD.R))
        self.history["D"].append(states.count(AgentSEIRD.D))
        self.history_states.append(states)