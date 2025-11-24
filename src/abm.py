import random
from typing import List, Dict
import numpy as np

from model_config import ModelConfig
from agent import Agent


class ABM:
    # Main agent‑based simulation engine

    # Responsibilities:
    # - Create population of Agent objects
    # - Advance daily infection/recovery dynamics
    # - Track state counts over time

    # Notes:
    # - Uses random mixing (well‑mixed population) by default

    def __init__(self, cfg: ModelConfig):
        self.cfg = cfg
        self._init_rng()

        # Create agents (initially all susceptible)
        self.agents: List[Agent] = [Agent(cfg) for _ in range(cfg.N)]

        # Infect I0 randomly
        initial_I = random.sample(range(cfg.N), cfg.I0)
        for idx in initial_I:
            self.agents[idx].state = Agent.I

        # Time-series tracking (store S/I/R counts per day)
        self.history: Dict[str, list[int]] = {k: [] for k in ["S", "I", "R"]}
        self.day: int = 0
    

    def _init_rng(self) -> None:
        # Initialize random seeds for reproducible runs
        if self.cfg.seed is not None:
            random.seed(self.cfg.seed)
            np.random.seed(self.cfg.seed)


    def step(self) -> None:
        # Unified daily update pipeline
        # DO NOT override this method in subclasses
        # Instead override phase-specific methods below

        # Phase 1: Infectious agents form contacts & mark new infections
        new_infections = self._collect_infections()

        # Phase 2: Apply new infections (batch update for correctness)
        self._apply_infections(new_infections)

        # Phase 3: Update infection timers, recover those who expire
        self._progress_states()
        
        # Phase 4: Log daily summary
        self._log_states()
    
        self.day += 1


    # === PHASE 1 ===
    def _collect_infections(self) -> list[int]:
        # Determine which agents become infected today
        # Default implementation = well-mixed SIR
        # Override for network-based or SEIR/SEIAR logic
        
        newly_exposed: list[int] = []

        # check if anybody is exposed or infected otherwise end simulation
        if not any(a.state in Agent.INF for a in self.agents):
            print(f"Nobody infected or exposed. terminating simulation on day {self.day}")
            return False

        for i, agent in enumerate(self.agents):
            if not agent.is_infectious:
                continue
            # each infectious agent makes K contacts
            for _ in range(self.cfg.contacts_per_day):
                j = random.randrange(self.cfg.N)
                target = self.agents[j]
                # attempt infection
                if target.is_susceptible and random.random() < self.cfg.p_infect:
                    newly_exposed.append(j)

        return newly_exposed


    # === PHASE 2 ===
    def _apply_infections(self, infected_indices: list[int]) -> None:
        # Apply new infections (batch update)
        # Subclasses may override to support exposed/incubation states
        
        for idx in infected_indices:
            self.agents[idx].infect()
    

    # === PHASE 3 ===
    def _progress_states(self) -> None:
        # Update disease progression
        # Subclasses may override for SEIR, SEIAR, waning immunity, vaccination, etc
        
        for ag in self.agents:
            ag.progress()

    # === PHASE 4 ===
    def _log_states(self) -> None:
        # Record S/I/R counts for plotting
        # Subclasses may override to include E, IA, IS, D, V, etc

        states = [a.state for a in self.agents]
        self.history["S"].append(states.count(Agent.S))
        self.history["I"].append(states.count(Agent.I))
        self.history["R"].append(states.count(Agent.R))


    # =================================
    def run(self, days: int = 67):
        # Run simulation for a fixed number of days

        for _ in range(days):
            self.step()
