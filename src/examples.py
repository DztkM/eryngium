from config import Config
from abm import ABM
from abm_network import ABMNetwork
from seird.config_seird import ConfigSEIRD 
from seird.abm_network_seird import ABMNetworkSEIRD
from seiard.config_seiard import ConfigSEIARD
from seiard.abm_network_seiard import ABMNetworkSEIARD
from visualization import plot_history, plot_network, animate_network_spread
from intervention.interventions_examples import Lockdown, Masks, Vaccines


def ex_sir_1():
    cfg = Config(
        seed=42,
    )
    model = ABM(cfg)

    # Run model
    model.run(days=90)
    fig = plot_history(model.history, "SIR")
    fig.savefig("img/sir.png", dpi=300)


def ex_sirnetwork_1():
    cfg = Config(
        seed=42
    )

    model_net = ABMNetwork(cfg, network_type="watts_strogatz", k=10, beta=0.1)
    # Run model
    model_net.run(days=60)

    fig = plot_history(model_net.history, "SIR_network")
    fig.savefig("img/sir_network.png", dpi=300)

    # # Plot final network state
    # agent_states = [a.state for a in model_net.agents]
    # plot_network(model_net.G, agent_states)

    # Animate infection spread:
    ani = animate_network_spread(model_net, interval=200)
    ani.save("img/sir_network_spread.gif", writer="pillow", fps=1)


def ex_seird_1():
    cfg = ConfigSEIRD(
        N=1500,
        I0=50,
        seed=42,
    )
    model_seird = ABMNetworkSEIRD(cfg, network_type="watts_strogatz", k=10, beta=0.1,)

    # Run model
    model_seird.run(days=64)

    fig = plot_history(model_seird.history, "SEIRD")
    fig.savefig("img/seird.png", dpi=300)

    # Animate infection spread:
    ani = animate_network_spread(model_seird, interval=200, model_type="SEIRD")
    ani.save("img/seird_spread.gif", writer="pillow", fps=1)


def ex_seiard_1():
    cfg = ConfigSEIARD(
        N=1500,
        I0=50, 
        seed=42,
    )

    model_seiard = ABMNetworkSEIARD(cfg, network_type="watts_strogatz", k=10, beta=0.1,)
    # Run model
    model_seiard.run(days=64)

    fig = plot_history(model_seiard.history, "SEIARD")
    fig.savefig("img/seiard.png", dpi=300)

    # Animate infection spread:
    ani = animate_network_spread(model_seiard, interval=200, model_type="SEIARD")
    ani.save("img/seiard_spread.gif", writer="pillow", fps=1)


def ex_interventions_sirnetwork_1():
    cfg = Config(
        seed=42
    )
    interventions = [
            Lockdown(start_day=8, end_day=15, reduction_factor=0.5),
        ]

    model_net = ABMNetwork(cfg, interventions=interventions, network_type="watts_strogatz", k=10, beta=0.1)
    # Run model
    model_net.run(days=60)

    fig = plot_history(model_net.history, "SIR_network (+lockdown)")
    fig.savefig("img/lockdown_intervention_sir_network.png", dpi=300)
    
    # Animate infection spread:
    ani = animate_network_spread(model_net, interval=200)
    ani.save("img/lockdown_intervention_sir_network_spread.gif", writer="pillow", fps=1)


def ex_interventions_seird_1():
    cfg = ConfigSEIRD(
        N=1500,
        I0=50,
        seed=42,
    )
    interventions = [
            Lockdown(start_day=8, end_day=15, reduction_factor=0.5),
        ]
    
    model_seird = ABMNetworkSEIRD(cfg, interventions=interventions, network_type="watts_strogatz", k=10, beta=0.1,)
    # Run model
    model_seird.run(days=64)

    fig = plot_history(model_seird.history, "SEIRD (+lockdown)")
    fig.savefig("img/lockdown_intervention_seird.png", dpi=300)

    # Animate infection spread:
    ani = animate_network_spread(model_seird, interval=200, model_type="SEIRD")
    ani.save("img/lockdown_intervention_seird_spread.gif", writer="pillow", fps=1)


def ex_interventions_seiard_1():
    cfg = ConfigSEIARD(
        N=1500,
        I0=50,
        seed=42,
    )
    interventions = [
            Lockdown(start_day=8, end_day=15, reduction_factor=0.5),
        ]
    
    model_seiard = ABMNetworkSEIARD(cfg, interventions=interventions, network_type="watts_strogatz", k=10, beta=0.1,)
    # Run model
    model_seiard.run(days=64)

    # plot_seiard(model_seiard.history)
    fig = plot_history(model_seiard.history, "SEIARD (+lockdown)")
    fig.savefig("img/lockdown_intervention_seiard.png", dpi=300)

    # Animate infection spread:
    ani = animate_network_spread(model_seiard, interval=200, model_type="SEIARD")
    ani.save("img/lockdown_intervention_seiard_spread.gif", writer="pillow", fps=1)


# SIR_network + Masks intervention
def ex_interventions_sirnetwork_2():
    cfg = Config(
        seed=42
    )
    interventions = [
            Masks(start_day=7, end_day=21, compliance=0.8, efficacy=0.5)
        ]

    model_net = ABMNetwork(cfg, interventions=interventions, network_type="watts_strogatz", k=10, beta=0.1)
    # Run model
    model_net.run(days=60)

    fig = plot_history(model_net.history, "SIR_network (+masks)")
    fig.savefig("img/masks_intervention_sir_network.png", dpi=300)
    
    # Animate infection spread:
    ani = animate_network_spread(model_net, interval=200)
    ani.save("img/masks_intervention_sir_network_spread.gif", writer="pillow", fps=1)


# SEIRD + Masks intervention
def ex_interventions_seird_2():
    cfg = ConfigSEIRD(
        N=1500,
        I0=50,
        seed=42,
    )
    interventions = [
            Masks(start_day=7, end_day=21, compliance=0.8, efficacy=0.5)
        ]
    
    model_seird = ABMNetworkSEIRD(cfg, interventions=interventions, network_type="watts_strogatz", k=10, beta=0.1,)
    # Run model
    model_seird.run(days=64)

    # plot_seiard(model_seiard.history)
    fig = plot_history(model_seird.history, "SEIRD (+masks)")
    fig.savefig("img/masks_intervention_seird.png", dpi=300)

    # Animate infection spread:
    ani = animate_network_spread(model_seird, interval=200, model_type="SEIRD")
    ani.save("img/masks_intervention_seird_spread.gif", writer="pillow", fps=1)


# SEIARD + Masks intervention
def ex_interventions_seiard_2():
    cfg = ConfigSEIARD(
        N=1500,
        I0=50,
        seed=42,
    )
    interventions = [
            Masks(start_day=7, end_day=21, compliance=0.8, efficacy=0.5)
        ]
    
    model_seiard = ABMNetworkSEIARD(cfg, interventions=interventions, network_type="watts_strogatz", k=10, beta=0.1,)
    # Run model
    model_seiard.run(days=64)

    # plot_seiard(model_seiard.history)
    fig = plot_history(model_seiard.history, "SEIARD (+masks)")
    fig.savefig("img/masks_intervention_seiard.png", dpi=300)

    # Animate infection spread:
    ani = animate_network_spread(model_seiard, interval=200, model_type="SEIARD")
    ani.save("img/masks_intervention_seiard_spread.gif", writer="pillow", fps=1)


def ex_interventions_vaccines_seiard_2():
    cfg = ConfigSEIARD(
        N=1500,
        I0=50,
        seed=42,
    )
    interventions = [
        Vaccines(start_day=20, end_day=27, daily_vaccines=0.2, compliance=0.8, efficacy=0.93)
    ]

    model_seiard = ABMNetworkSEIARD(cfg, interventions=interventions, network_type="watts_strogatz", k=10, beta=0.1, )
    # Run model
    model_seiard.run(days=64)

    # plot_seiard(model_seiard.history)
    fig = plot_history(model_seiard.history, "SEIARD (+vaccines)")
    fig.savefig("img/vaccines_intervention_seiard.png", dpi=300)

    # Animate infection spread:
    ani = animate_network_spread(model_seiard, interval=200, model_type="SEIARD")
    ani.save("img/vaccines_intervention_seiard_spread.gif", writer="pillow", fps=1)