from dataclasses import dataclass


@dataclass
class ConfigSEIRD:
    # Configuration container for SEIAR-D model parameters
    
    N: int = 1000
    I0: int = 10
    contacts_per_day: int = 10
    seed: int | None = None

    p_infect: float = 0.035
    mortality_rate: float = 0.025

    inf_period_mean: float = 7
    inf_period_std: float = 2

    inc_period_mean: float = 2
    inc_period_std: float = 1