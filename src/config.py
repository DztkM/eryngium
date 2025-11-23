from dataclasses import dataclass


@dataclass
class Config:
    # Container for core model parameters
    # 
    # Attributes:
    # N                 : int, Population size
    # I0                : int, Initial number of infected agents
    # contacts_per_day  : int, Mean daily contact attempts per infectious agent
    # p_infect          : float, Probability of transmission per contact
    # inf_period_mean   : float, Mean infectious period (days)
    # inf_period_std    : float, Standard deviation of infectious period (days)
    # seed              : int | None, Seed for reproducible randomness
    
    N: int = 1000
    I0: int = 10
    contacts_per_day: int = 10

    p_infect: float = 0.08
    inf_period_mean: float = 7
    inf_period_std: float = 3

    seed: int | None = None
