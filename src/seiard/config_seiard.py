from dataclasses import dataclass, field


@dataclass
class ConfigSEIARD:
    # Configuration container for SEIAR-D model parameters
    
    N: int = 1000
    I0: int = 10
    # contacts_per_day: int = 10    # depricated, use contacts_by_group
    seed: int | None = None

    p_infect_IS: float = 0.035
    p_infect_IA: float = 0.017
    p_symptomatic: float = 0.8
    # mortality_rate: float = 0.025 # depricated, use mortality_by_group

    inf_period_mean_IS: float = 7
    inf_period_std_IS: float = 2
    inf_period_mean_IA: float = 5
    inf_period_std_IA: float = 1.5

    inc_period_mean: float = 2
    inc_period_std: float = 1

    # age groups
    age_groups: list[str] = field(
        default_factory=lambda: ["child", "adult", "senior"]
    )
    age_group_dist: dict[str, float] = field(
        default_factory=lambda: {"child": 0.2, "adult": 0.65, "senior": 0.15}
    )
    susceptibility_by_group: dict[str, float] = field(
        default_factory=lambda: {"child": 0.9, "adult": 1.0, "senior": 1.3}
    )
    contacts_by_group: dict[str, int] = field(
        default_factory=lambda: {"child": 18, "adult": 15, "senior": 8}
    )
    mortality_by_group: dict[str, float] = field(
        default_factory=lambda: {"child": 0.001, "adult": 0.025, "senior": 0.05}
    )