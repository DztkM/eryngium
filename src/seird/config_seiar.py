from dataclasses import dataclass


@dataclass
class ConfigSEIAR:
    # Configuration container for SEIAR-D model parameters
    
    N: int = 1000
    I0: int = 10
    contacts_per_day: int = 10
    seed: int | None = None

    p_infect_IS: float = 0.035
    p_infect_IA: float = 0.017
    p_symptomatic: float = 0.8
    mortality_rate: float = 0.025

    inf_period_mean_IS: float = 7
    inf_period_std_IS: float = 2
    inf_period_mean_IA: float = 5
    inf_period_std_IA: float = 1.5

    inc_period_mean: float = 2
    inc_period_std: float = 1