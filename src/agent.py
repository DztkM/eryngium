class Agent:
    # Represents an individual

    # States:
    # 0 = Susceptible (S)
    # 1 = Infectious (I)
    # 2 = Recovered (R)

    SUSC = 0
    INF = 1
    REC = 2


    def __init__(self, state: int = SUSC):
        self.state: int = state
        self.days_infected: int = 0 # counts days in INF state


    @property
    def is_infectious(self) -> bool:
        return self.state == self.INF


    @property
    def is_susceptible(self) -> bool:
        return self.state == self.SUSC