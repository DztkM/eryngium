from dataclasses import dataclass


@dataclass
class ConfigSEIARD:
    # Configuration container for SEIAR-D model parameters
    
    N: int = 1000
    I0: int = 10
    contacts_per_day: int = 10
    seed: int | None = None

    p_infect_IS: float = 0.4
    p_infect_IA: float = 0.05
    p_symptomatic: float = 0.85
    mortality_rate: float = 0.025

    inf_period_mean_IS: float = 7
    inf_period_std_IS: float = 3
    inf_period_mean_IA: float = 3
    inf_period_std_IA: float = 1.5

    inc_period_mean: float = 3
    inc_period_std: float = 1.5