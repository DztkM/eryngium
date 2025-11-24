import random
import numpy as np

from agent import Agent
from seird.config_seird import ConfigSEIRD

class AgentSEIRD(Agent):
    # Extended agent with SEIR-D dynamics (inherits from base Agent)

    # States:
    # 0 = Susceptible (S)
    # 1 = Exposed (E)
    # 2 = Infectious (I)
    # 4 = Recovered (R)
    # 5 = Dead (D)

    S, E, I, R, D = range(5)


    def __init__(self, params: ConfigSEIRD, state: int = S):
        self.state: int = state
        self.params = params
        self.days_remaining: int = 0


    def infect(self):
        # Transition from S -> E (exposed)
        if self.state == self.S:
            self.state = self.E
            self.days_remaining = max(1, int(np.random.normal(self.params.inc_period_mean, self.params.inc_period_std)))


    def become_infectious(self) -> None:
        # Transition from E -> I
        
        self.state = self.I
        self.days_remaining = max(
            1, int(np.random.normal(
                self.params.inf_period_mean, self.params.inf_period_std
            ))
        )


    def progress(self) -> None:
        # SEIR-D infection timer and update states
        if self.state in [self.E, self.I]:
            self.days_remaining -= 1
            if self.days_remaining <= 0:
                if self.state == self.E:
                    self.become_infectious()
                elif self.state == self.I:
                    # recovery or death
                    if random.random() < self.params.mortality_rate:
                        self.state = self.D
                    else:
                        self.state = self.R

    @property
    def is_infectious(self) -> bool:
        return self.state == self.I