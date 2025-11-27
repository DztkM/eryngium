import random
from typing import List, Dict
import numpy as np
import networkx as nx

from abm_network import ABMNetwork
from seiard.config_seiard import ConfigSEIARD
from seiard.agent_seiard import AgentSEIARD 

from intervention.interventions import InterventionManager

class ABMNetworkSEIARD(ABMNetwork):
    # Network-based SEIAR-D epidemic simulator

    def __init__(self, cfg: ConfigSEIARD, interventions=None, network_type: str = "erdos_renyi", **net_params):
        self.cfg = cfg
        self._init_rng()

         # Create agents (initially all susceptible)
        self.agents: List[AgentSEIARD] = [AgentSEIARD(cfg) for _ in range(cfg.N)]

        # Infect I0 randomly
        initial_I = random.sample(range(cfg.N), cfg.I0)
        for idx in initial_I:
            self.agents[idx].state = AgentSEIARD.E
        
        self.cfg = cfg
        self.network_type = network_type
        self.net_params = net_params
        self.G = self._create_network()

        # Time-series tracking (store S/E/IA/IS/R/D counts per day)
        self.history: Dict[str, list[int]] = {k: [] for k in ["S", "E", "IA", "IS", "R", "D"]}
        self.history_states: list[list[int]] = [] # stores list of agent states each day
        
        self.day: int = 0
        self.finished = False

        # Interventions
        self.interventions = InterventionManager(interventions)

        # Dynamic parameter (modifiable by lockdown etc.)
        self.current_contacts_per_day = cfg.contacts_per_day


    # === PHASE 0 ===
    def _should_continue(self) -> bool:
        # Check if epidemic is still active
        # Default behavior: stop when no infected remain

        any_infected = any(a.state in [AgentSEIARD.E, AgentSEIARD.IA, AgentSEIARD.IS] for a in self.agents)
        return any_infected


    # === PHASE 1 ===
    def _collect_infections(self) -> list[int]:
        # Determine which agents become infected today

        newly_exposed: list[int] = []
        
        for i, agent in enumerate(self.agents):
            if not agent.is_infectious:
                continue

            # Get neighbors of agent i in the network
            neighbors = list(self.G.neighbors(i))
            if not neighbors:
                continue

            # Choose `current_contacts_per_day` random neighbors to attempt contact
            # sampling WITH replacement to simulate repeated daily contacts
            contacts = random.choices(neighbors, k=self.current_contacts_per_day)

            # Attempt infection on each contacted neighbor
            for j in contacts:
                target = self.agents[j]
                # attempt infection
                if target.is_susceptible and not target.vaccinated:
                    p = (self.cfg.p_infect_IS if agent.state == AgentSEIARD.IS
                         else self.cfg.p_infect_IA)
                    p *= (1-agent.mask_eff)
                    if random.random() < p:
                        newly_exposed.append(j)
        
        return newly_exposed


    # === PHASE 4 ===
    def _log_states(self) -> None:
        # Count all states for logging
        states = [a.state for a in self.agents]
        self.history["S"].append(states.count(AgentSEIARD.S))
        self.history["E"].append(states.count(AgentSEIARD.E))
        self.history["IA"].append(states.count(AgentSEIARD.IA))
        self.history["IS"].append(states.count(AgentSEIARD.IS))
        self.history["R"].append(states.count(AgentSEIARD.R))
        self.history["D"].append(states.count(AgentSEIARD.D))
        self.history_states.append(states)