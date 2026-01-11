from dataclasses import dataclass, field

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
    starting_total_infections: int = 0
    # contacts_per_day: int = 10    # depricated, use contacts_by_group

    p_infect: float = 0.08
    inf_period_mean: float = 7
    inf_period_std: float = 3

    seed: int | None = None

    # age groups
    age_groups: list[str] = field(
        default_factory=lambda: ["child", "adult", "senior"]
    )
    age_group_dist: dict[str, float] = field(
        default_factory=lambda: {"child": 0.16,"adult": 0.72,"senior": 0.12}
    )
    susceptibility_by_group: dict[str, float] = field(
        default_factory=lambda: {"child": 0.9, "adult": 1.0, "senior": 1.3}
    )
    contacts_by_group: dict[str, int] = field(
        default_factory=lambda: {"child": 8,"adult": 5,"senior": 4}
    )
