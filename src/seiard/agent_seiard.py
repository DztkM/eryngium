import random
import numpy as np

from agent import Agent
from seiard.config_seiard import ConfigSEIARD

class AgentSEIARD(Agent):
    # Extended agent with SEIAR-D dynamics (inherits from base Agent)

    # States:
    # 0 = Susceptible (S)
    # 1 = Exposed (E)
    # 2 = Infectious Asymptomatic (IA)
    # 3 = Infectious Symptomatic (IS)
    # 4 = Recovered (R)
    # 5 = Dead (D)

    S, E, IS, IA, R, D = range(6)


    def __init__(self, params: ConfigSEIARD, state: int = S, age_group: str = "adult"):
        self.state: int = state
        self.params = params
        self.days_remaining: int = 0
        self.mask_eff = 0
        self.age_group = age_group


    def infect(self):
        # Transition from S -> E (exposed)
        if self.state == self.S:
            self.state = self.E
            self.days_remaining = max(1, int(np.random.normal(self.params.inc_period_mean, self.params.inc_period_std)))


    def become_infectious(self) -> None:
        # Transition from E -> IA or IS
        if random.random() < self.params.p_symptomatic:
            self.state = self.IS
            self.days_remaining = max(
                1, int(np.random.normal(
                    self.params.inf_period_mean_IS, self.params.inf_period_std_IS
                ))
            )
        else:
            self.state = self.IA
            self.days_remaining = max(
                1, int(np.random.normal(
                    self.params.inf_period_mean_IA, self.params.inf_period_std_IA
                ))
            )


    def progress(self) -> None:
        # SEIAR-D infection timer and update states
        if self.state in [self.E, self.IA, self.IS]:
            self.days_remaining -= 1
            if self.days_remaining <= 0:
                if self.state == self.E:
                    self.become_infectious()
                elif self.state in [self.IA, self.IS]:
                    # recovery or death
                    if random.random() < self.params.mortality_by_group[self.age_group]:
                        self.state = self.D
                    else:
                        self.state = self.R

    @property
    def is_infectious(self) -> bool:
        return self.state in [self.IA, self.IS]