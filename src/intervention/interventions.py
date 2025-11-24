class Intervention:
    # Base class for all interventions

    def apply(self, model):
        # Called each simulation day BEFORE phase 1
        raise NotImplementedError
    

class InterventionManager:
    # Maintains and applies all interventions each simulation day

    def __init__(self, interventions=None):
        self.interventions = interventions or []


    def add(self, intervention):
        self.interventions.append(intervention)


    def apply(self, model):
        # Called automatically at the beginning of model.step()

        for itv in self.interventions:
            itv.apply(model)
    