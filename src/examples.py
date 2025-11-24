from config import Config
from abm import ABM
from abm_network import ABMNetwork
from seird.config_seird import ConfigSEIRD 
from seird.abm_network_seird import ABMNetworkSEIRD
from seiard.config_seiard import ConfigSEIARD
from seiard.abm_network_seiard import ABMNetworkSEIARD
from visualization import plot_sir, plot_seird, plot_seiard, plot_network, animate_network_spread

def ex_sir_1():
    cfg = Config(
        seed=42,
    )
    model = ABM(cfg)

    # Run model
    model.run(days=90)
    plot_sir(model.history)

def ex_sirnetwork_1():
    cfg = Config(
        seed=42
    )

    model_net = ABMNetwork(cfg, network_type="watts_strogatz", k=10, beta=0.1)
    # Run model
    model_net.run(days=50)

    plot_sir(model_net.history)

    # Plot final network state
    agent_states = [a.state for a in model_net.agents]
    plot_network(model_net.G, agent_states)

    ani = animate_network_spread(model_net, interval=200)
    ani.save("sir_network_spread.gif", writer="pillow", fps=5)


def ex_seird_network_1():
    cfg = ConfigSEIRD(
        N=1500,
        I0=50,
        contacts_per_day=15, 
        seed=42,
    )
    model_seird = ABMNetworkSEIRD(cfg, network_type="watts_strogatz", k=10, beta=0.1,)
    # Run model
    model_seird.run(days=64)

    plot_seird(model_seird.history)

    # Plot final network state
    agent_states = [a.state for a in model_seird.agents]
    plot_network(model_seird.G, agent_states, model_type="SEIRD")

    ani = animate_network_spread(model_seird, interval=200, model_type="SEIRD")
    ani.save("seird_network_spread.gif", writer="pillow", fps=1)


def ex_seiard_network_1():
    cfg = ConfigSEIARD(
        N=1500,
        I0=50,
        contacts_per_day=15, 
        seed=42,
    )
    model_seiard = ABMNetworkSEIARD(cfg, network_type="watts_strogatz", k=10, beta=0.1,)
    # Run model
    model_seiard.run(days=64)


    plot_seiard(model_seiard.history)

    # Plot final network state
    agent_states = [a.state for a in model_seiard.agents]
    plot_network(model_seiard.G, agent_states, model_type="SEIARD")

    ani = animate_network_spread(model_seiard, interval=200, model_type="SEIARD")
    ani.save("seiard_network_spread.gif", writer="pillow", fps=1)