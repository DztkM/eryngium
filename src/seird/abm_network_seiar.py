import random
from typing import List, Dict
import numpy as np
import networkx as nx

from abm_network import ABMNetwork
from seird.config_seiar import ConfigSEIAR
from seird.agent_seiar import AgentSEIAR  

class ABMNetworkSEIAR(ABMNetwork):
    # Network-based SEIAR-D epidemic simulator

    def __init__(self, cfg: ConfigSEIAR, network_type: str = "erdos_renyi", **net_params):
        self.cfg = cfg
        self._init_rng()

         # Create agents (initially all susceptible)
        self.agents: List[AgentSEIAR] = [AgentSEIAR(cfg) for _ in range(cfg.N)]

        # Infect I0 randomly
        initial_I = random.sample(range(cfg.N), cfg.I0)
        for idx in initial_I:
            self.agents[idx].state = AgentSEIAR.INF

        self.day: int = 0

        self.cfg = cfg
        self.network_type = network_type
        self.net_params = net_params
        self.G = self._create_network()

        # Initialize agents
        # self.agents: List[AgentSEIAR] = [AgentSEIAR(i, cfg) for i in range(cfg.N)]
        # for i in random.sample(range(cfg.N), cfg.I0):
        #     self.agents[i].infect()

        # Tracking
        self.history: Dict[str, list[int]] = {k: [] for k in ["S", "E", "IA", "IS", "R", "D"]}
        self.history_states: list[list[int]] = [] # stores list of agent states each day
    

    def step(self):
        # Advance simulation by one day

        # new_exposed = set()
        newly_exposed: list[int] = []

        # check if anybody is exposed or infected otherwise end simulation
        if not any(a.state in (AgentSEIAR.IA, AgentSEIAR.IS, AgentSEIAR.E) for a in self.agents):
            print(f"Nobody infected or exposed. terminating simulation on day {self.day}")
            return False

        # phase 1: collect candidates for new infection
        for i, agent in enumerate(self.agents):
            if not agent.is_infectious:
                continue
            neighbors = list(self.G.neighbors(i))
            if not neighbors:
                continue

            contacts = random.choices(neighbors, k=self.cfg.contacts_per_day)

            for j in contacts:
                target = self.agents[j]
                if target.is_susceptible:
                    p = (self.cfg.p_infect_IS if agent.state == AgentSEIAR.IS
                         else self.cfg.p_infect_IA)
                    if random.random() < p:
                        newly_exposed.append(j)

        # phase 2: apply new infections (batch)
        for idx in newly_exposed:
            self.agents[idx].infect()

        # phase 3: progress states
        for agent in self.agents:
            agent.progress()

        # phase 4: log states counts
        self._record_day()
        self.day += 1
        return True


    def _record_day(self):
        # Count all states for logging
        states = [a.state for a in self.agents]
        self.history["S"].append(states.count(AgentSEIAR.S))
        self.history["E"].append(states.count(AgentSEIAR.E))
        self.history["IA"].append(states.count(AgentSEIAR.IA))
        self.history["IS"].append(states.count(AgentSEIAR.IS))
        self.history["R"].append(states.count(AgentSEIAR.R))
        self.history["D"].append(states.count(AgentSEIAR.D))
        self.history_states.append(states)