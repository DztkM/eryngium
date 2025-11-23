import numpy as np
# from model_config import ModelConfig
from config import Config
from abm import ABM
# from abm_network import ABMNetwork
# from seird.config_seiar import ConfigSEIAR
# from seird.abm_network_seiar import ABMNetworkSEIAR
# from visualization import plot_sir, plot_seiard, plot_network, animate_network_spread 
from visualization import plot_sir

def ex_sir_1():
    cfg = Config(
        seed=42,
    )
    model = ABM(cfg)

    # Run model
    model.run(days=90)
    plot_sir(model.history)

# def ex_sirnetwork_1():
#     cfg = ModelConfig(
#         N=200, 
#         I0=5, 
#         contacts_per_day=8, 
#         p_trans=0.05, 
#         infectious_days=8, 
#         seed=42
#     )

#     model_net = ABMNetwork(cfg, network_type="watts_strogatz", k=10, beta=0.1)
#     # Run model
#     model_net.run(days=50)
#     ts_dict = {
#         "S": np.array(model_net.daily_S),
#         "I": np.array(model_net.daily_I),
#         "R": np.array(model_net.daily_R)
#     }

#     plot_sir(ts_dict)

#     # Plot final network state
#     agent_states = [a.state for a in model_net.agents]
#     plot_network(model_net.G, agent_states)

#     ani = animate_network_spread(model_net, interval=200)
#     ani.save("sir_network_spread.gif", writer="pillow", fps=5)


# def ex_seiard_network_1():
#     cfg = ConfigSEIAR(
#         N=300,
#         I0=5,
#         contacts_per_day=8, 
#         seed=42,
#     )
#     model_seiard = ABMNetworkSEIAR(cfg, network_type="watts_strogatz", k=10, beta=0.1,)
#     # Run model
#     model_seiard.run(days=32)


#     plot_seiard(model_seiard.history)

#     # Plot final network state
#     agent_states = [a.state for a in model_seiard.agents]
#     plot_network(model_seiard.G, agent_states, model_type="SEIARD")

#     ani = animate_network_spread(model_seiard, interval=200, model_type="SEIARD")
#     ani.save("seiard_network_spread.gif", writer="pillow", fps=5)