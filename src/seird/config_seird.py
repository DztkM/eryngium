from dataclasses import dataclass, field


@dataclass
class ConfigSEIRD:
    # Configuration container for SEIAR-D model parameters
    
    N: int = 1000
    I0: int = 10
    starting_total_infections: int = 0
    # contacts_per_day: int = 10    # depricated, use contacts_by_group
    seed: int | None = None

    p_infect: float = 0.041
    # mortality_rate: float = 0.025 # depricated, use mortality_by_group

    inf_period_mean: float = 7
    inf_period_std: float = 2

    inc_period_mean: float = 2
    inc_period_std: float = 1

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
    mortality_by_group: dict[str, float] = field(
        default_factory=lambda: {"child": 0.001, "adult": 0.025, "senior": 0.05}
    )
