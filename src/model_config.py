from dataclasses import dataclass


@dataclass
class ModelConfig:
    # Container for core model parameters

    # Attributes:
    # N : int, Population size
    # I0 : int, Initial number of infected agents
    # contacts_per_day : int, Mean daily contact attempts per infectious agent
    # p_trans : float, Probability of transmission per contact
    # infectious_days : int, Number of days an agent remains infectious before recovery
    # seed : int | None, Seed for reproducible randomness
    
    N: int = 2000
    I0: int = 5
    contacts_per_day: int = 10
    p_trans: float = 0.02
    infectious_days: int = 10
    seed: int | None = None