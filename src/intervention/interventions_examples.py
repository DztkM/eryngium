import random
from intervention.interventions import Intervention


class Lockdown(Intervention):
    # Reduces contacts_per_day by a factor during a specific interval

    def __init__(self, start_day, end_day, reduction_factor=0.1):
        self.start_day = start_day
        self.end_day = end_day
        self.reduction_factor = reduction_factor

    def apply(self, model):
        if self.start_day <= model.day <= self.end_day:
            model.current_contacts_by_group = {
                group: int(base_contacts * self.reduction_factor)
                for group, base_contacts in model.cfg.contacts_by_group.items()
            }
        else:
            model.current_contacts_by_group = dict(model.cfg.contacts_by_group)


class Masks(Intervention):
    # Applies mask effectiveness to agents with some probability
    
    def __init__(self, start_day, end_day, compliance=0.8, efficacy=0.5):
        self.start_day = start_day
        self.end_day = end_day
        self.compliance = compliance
        self.efficacy = efficacy

    def apply(self, model):
        if model.day < self.start_day or model.day > self.end_day:
            for a in model.agents:
                a.mask_eff = 0.0
            return

        for a in model.agents:
            if random.random() < self.compliance:
                a.mask_eff = self.efficacy
            else:
                a.mask_eff = 0.0

class Vaccines(Intervention):
    def __init__(self, start_day, end_day, daily_vaccines, compliance, efficacy):
        self.start_day = start_day
        self.end_day = end_day
        self.daily_vaccines = daily_vaccines
        self.compliance = compliance
        self.efficacy = efficacy



    def apply(self, model):
        if self.start_day <= model.day < self.end_day:
            for a in model.agents:
                if a.is_susceptible and not a.vaccinated:
                    if random.random() < self.daily_vaccines and random.random() < self.compliance:
                        if random.random() < self.efficacy:
                            a.vaccinated = True