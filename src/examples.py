import numpy as np
from model_config import ModelConfig
from abm import ABM
from visualization import plot_sir


def ex1():
    cfg = ModelConfig(
        N=100000,
        I0=100,
        contacts_per_day=12,
        p_trans=0.03,
        infectious_days=10,
        seed=42,
    )
    model = ABM(cfg)
    # Run model
    I_ts = model.run(days=90)
    ts_dict = {
        "S": np.array(model.daily_S),
        "I": np.array(model.daily_I),
        "R": np.array(model.daily_R)
    }

    plot_sir(ts_dict)