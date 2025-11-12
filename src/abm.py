import random
from typing import List
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
    # - Hooks exist for contact-network logic in future

    def __init__(self, cfg: ModelConfig):
        self.cfg = cfg
        self._init_rng()

        # Create agents (initially all susceptible)
        self.agents: List[Agent] = [Agent() for _ in range(cfg.N)]

        # Infect I0 randomly
        initial_I = random.sample(range(cfg.N), cfg.I0)
        for idx in initial_I:
            self.agents[idx].state = Agent.INF

        # Time-series outputs (store S/I/R counts per day)
        self.daily_I: list[int] = []
        self.daily_S: list[int] = []
        self.daily_R: list[int] = []
        self.day: int = 0
    

    def _init_rng(self) -> None:
        # Initialize random seeds for reproducible runs
        if self.cfg.seed is not None:
            random.seed(self.cfg.seed)
            np.random.seed(self.cfg.seed)


    def step(self) -> None:
        # Advance simulation by one day

        # PHASES:
        # 1) Infectious agents form contacts & mark new infections
        # 2) Apply new infections (batch update for correctness)
        # 3) Update infection timers, recover those who expire
        # 4) Log daily summary

        # phase 1: collect candidates for new infection
        newly_exposed: list[int] = []

        for i, agent in enumerate(self.agents):
            if not agent.is_infectious:
                continue

            # each infectious agent makes K contacts
            for _ in range(self.cfg.contacts_per_day):
                j = random.randrange(self.cfg.N)
                target = self.agents[j]

                # attempt infection
                if target.is_susceptible and random.random() < self.cfg.p_trans:
                    newly_exposed.append(j)

        # phase 2: apply new infections (batch)
        for idx in newly_exposed:
            tgt = self.agents[idx]
            if tgt.is_susceptible:  # re-check safety
                tgt.state = Agent.INF
                tgt.days_infected = 0

        # phase 3: update timers & recover
        for ag in self.agents:
            if ag.is_infectious:
                ag.days_infected += 1
                if ag.days_infected >= self.cfg.infectious_days:
                    ag.state = Agent.REC

        # phase 4: log S/I/R counts
        S_count = sum(1 for a in self.agents if a.is_susceptible)
        I_count = sum(1 for a in self.agents if a.is_infectious)
        R_count = sum(1 for a in self.agents if a.state == Agent.REC)
    
        self.daily_S.append(S_count)
        self.daily_I.append(I_count)
        self.daily_R.append(R_count)
        
        self.day += 1


    def run(self, days: int = 67):
        # Run simulation for a fixed number of days
        # Returns Time Series of infectious counts

        for _ in range(days):
            self.step()
