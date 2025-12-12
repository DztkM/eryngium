import random
import numpy as np
from config import Config
class Agent:
    # Represents an individual

    # States:
    # 0 = Susceptible (S)
    # 1 = Infectious (I)
    # 2 = Recovered (R)

    S, I, R = range(3)


    def __init__(self, params: Config, state: int = S, age_group: str = "adult"):
        self.state: int = state
        self.params = params
        self.days_remaining: int = 0
        self.mask_eff = 0
        self.age_group = age_group
        self.vaccinated: bool = False


    @property
    def is_infectious(self) -> bool:
        return self.state == self.I


    @property
    def is_susceptible(self) -> bool:
        return self.state == self.S
    

    def infect(self) -> None:
        # Transition from S -> I
        if self.state == self.S:
            self.state = self.I
            self.days_remaining = max(1, int(np.random.normal(self.params.inf_period_mean, self.params.inf_period_std)))


    def progress(self) -> None:
        # Infection timer
        if self.is_infectious:
            self.days_remaining -= 1
            if self.days_remaining <= 0:
                self.state = self.R    
