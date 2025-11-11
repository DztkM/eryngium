import random

import numpy as np

class Person:
    S, E, IS, IA, R, D = range(6)
    def __init__(self, pid, vaccinated=False, params=None):
        self.id = pid
        self.state = self.R if vaccinated else self.S
        self.symptomatic = False
        self.days_remaining = 0
        self.params = params

        self.incubation_period = max(1, int(np.random.normal(params['inc_period_std'], params['inc_period_std'])))
        self.infectious_period = max(1, int(np.random.normal(params['inf_period_mean_IS'], params['inf_period_std_IS'])))

    def infect(self):
        if self.state == self.S:
            self.state = self.E
            self.days_remaining = max(1, int(np.random.normal(self.params['inc_period_mean'], self.params['inc_period_std'])))

    def progress(self):
        if self.state in [self.E, self.IA, self.IS]:
            self.days_remaining -= 1
            if self.days_remaining <= 0:
                if self.state == self.E:
                    self.become_infectious()
                elif self.state in [self.IA, self.IS]:
                    if random.random() < self.params['mortality_rate']:
                        self.state = self.D
                    else:
                        self.state = self.R

    def become_infectious(self):
        if random.random() < self.params['p_symptomatic']:
            self.state = self.IS
            self.symptomatic = True
            self.days_remaining = max(1, int(np.random.normal(self.params['inf_period_mean_IS'], self.params['inf_period_std_IS'])))
        else:
            self.state = self.IA
            self.symptomatic = False
            self.days_remaining = max(1, int(np.random.normal(self.params['inf_period_mean_IA'], self.params['inf_period_std_IA'])))

    def is_infectious(self):
        return self.state in [self.IA, self.IS]