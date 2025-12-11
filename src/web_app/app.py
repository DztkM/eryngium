import streamlit as st
import networkx as nx
from matplotlib import pyplot as plt
import matplotlib as mpl

from seird.abm_network_seird import ABMNetworkSEIRD

mpl.rcParams["animation.html"] = "jshtml"

from abm_network import ABMNetwork
from intervention.interventions_examples import Lockdown,Masks,Vaccines
from seiard.abm_network_seiard import ABMNetworkSEIARD
from seiard.config_seiard import ConfigSEIARD
from abm import ABM
from config import Config
from seird.config_seird import ConfigSEIRD
from visualization import plot_history, animate_network_spread

import streamlit.components.v1 as components



def init_state():
    if "screen" not in st.session_state:
        st.session_state.screen = "model_select"
    if "selected_models" not in st.session_state:
        st.session_state.selected_models = []
    if "preset_disease" not in st.session_state:
        st.session_state.preset_disease = ("Custom")

def select_models(models):
    st.session_state.selected_models = models
    st.session_state.screen = "config"

def model_selection_screen():
    st.title("Interactive Epidemic Simulation")

    st.markdown(
        "Choose a model to simulate the spread of an infectious disease, "
        "or run all models for comparison."
    )

    spacer1, main_col, spacer2 = st.columns([1, 2, 1])

    with main_col:
        st.subheader("Select model")

        c1, c2, c3 = st.columns(3)
        with c1:
            st.button("SIR", key="sir_btn",
                      on_click=select_models, args=(["SIR"],))
        with c2:
            st.button("SEIR", key="seir_btn",
                      on_click=select_models, args=(["SEIR"],))
        with c3:
            st.button("SEIARD", key="seiard_btn",
                      on_click=select_models, args=(["SEIARD"],))

        st.markdown("---")
        st.button(
            "Run all models (SIR + SEIR + SEIARD)",
            key="all_models_btn",
            on_click=select_models,
            args=(["SIR", "SEIR", "SEIARD"],),
        )

def parameters_and_simulation_screen():
    models = st.session_state.selected_models
    model_label = (
        "All models (SIR, SEIR, SEIARD)" if len(models) > 1 else models[0]
    )
    left, right = st.columns([4, 1])
    with left:
        st.title("Simulation Config")
        st.caption(f"Current Selection: **{model_label}**")

    with right:
        with st.popover("Advanced"):
            st.markdown("### Disease presets")
            st.write(
                "Choose a disease to preconfigure model parameters. "
                "You can still adjust them manually afterwards if you want."
            )
            disease_options = ["Custom"] + list(
                # get_disease_presets_for_model(models[0]).keys()
            )
            preset = st.selectbox(
                "Select disease", disease_options,
                index=disease_options.index(st.session_state.preset_disease)
                if st.session_state.preset_disease in disease_options
                else 0,
            )
            if st.button("Apply preset"):
                st.session_state.preset_disease = preset

    st.markdown("---")

    col_main, col_side = st.columns([3, 2])

    # ---- Parameter Selection ----
    with col_main:

        N = st.number_input("Population Size", min_value=1, value=int(5000), key="population")
        I0 = st.number_input("Infected in the beginning", min_value=1, value=int(5), key="initial_infected")
        days_of_sim = st.number_input("Number of days", min_value=1, value=int(50), key="days_of_simulation")
        # p_infect = st.sidebar.slider("Transmission Probability", 0.0, 1.0, 0.05)
        # p_symptomatic = st.sidebar.slider("Probability Symptomatic", 0.0, 1.0, 0.7)
        # inc_mu = st.sidebar.slider("Incubation Mean", 1, 10, 4)
        # inc_sigma = st.sidebar.slider("Incubation Std", 0.1, 5.0, 1.5)
        # inf_mu = st.sidebar.slider("Infectious Mean", 1, 20, 8)
        # inf_sigma = st.sidebar.slider("Infectious Std", 0.1, 5.0, 1.5)
        interventions = []
        intervention = st.selectbox(
            "Intervention",
            ["None", "Lockdown", "Masks", "Vaccines"],
            key = "prevention_methos"
        )

        if intervention == "Lockdown":
            start_day = st.number_input("Start day", 0, days_of_sim, days_of_sim//2)
            end_day = st.number_input("End day", start_day if start_day is not None else 0, days_of_sim, days_of_sim)
            reduction_factor = st.number_input("Reduction factor", 0.1, 1.0, 0.5)
            interventions.append(Lockdown(start_day, end_day, reduction_factor))
        elif intervention == "Masks":
            start_day = st.number_input("Start day", 0, days_of_sim, days_of_sim//2)
            end_day = st.number_input("End day", start_day if start_day is not None else 0, days_of_sim, days_of_sim)
            compliance = st.number_input("Compliance", 0.1, 1.0, 0.5)
            efficacy = st.number_input("Efficacy", 0.1, 1.0, 0.5)
            interventions.append(Masks(start_day, end_day, compliance, efficacy))
        elif intervention == "Vaccines":
            start_day = st.number_input("Start day", 0, days_of_sim, days_of_sim//2)
            end_day = st.number_input("End day", start_day if start_day is not None else 0, days_of_sim, days_of_sim)
            daily_vaccines = st.number_input("Fraction of population treated with vaccine daily", 0.01,1.0, 0.5)
            compliance = st.number_input("Compliance", 0.1, 1.0, 0.5)
            efficacy = st.number_input("Efficacy", 0.1, 1.0, 0.5)
            interventions.append(Vaccines(start_day, end_day,daily_vaccines, compliance, efficacy))
        else:
            interventions = []

    with col_side:
        st.subheader("Run simulation")
        run_button = st.button("START")

    # ---- Run Simulation ----
    if run_button:
        st.write("Running simulation... please wait ⏳")
        if model_label == "SIR":
            cfg_sir = Config(
                N=N,
                I0=I0,
                seed=42
            )
            model_sir = ABMNetwork(cfg_sir,interventions=interventions, network_type="watts_strogatz", k=10, beta=0.1)
            model_sir.run(days=days_of_sim)
            #SHOW RESULTS
            col1, col2 = st.columns(2)

            with col1:
                fig = plot_history(model_sir.history, "SIR")
                st.pyplot(fig, width='stretch')
                plt.close(fig)

            with col2:
                ani = animate_network_spread(model_sir, interval=1000)
                gif_path = f"{model_label}_network.gif"
                ani.save(gif_path, writer="pillow", fps=2)

                st.image(gif_path, width='stretch')

        elif model_label == "SEIR":
            cfg_seird = ConfigSEIRD(
                N=N,
                I0=I0,
                seed=42
            )
            model_seird = ABMNetworkSEIRD(cfg_seird,interventions=interventions, network_type="watts_strogatz", k=10, beta=0.1, )
            model_seird.run(days=days_of_sim)

            col1, col2 = st.columns(2)

            with col1:
                fig = plot_history(model_seird.history, "SEIRD")
                st.pyplot(fig, width='stretch')
                plt.close(fig)

            with col2:
                ani = animate_network_spread(model_seird, interval=1000, model_type="SEIRD")
                gif_path = f"{model_label}_network.gif"
                ani.save(gif_path, writer="pillow", fps=2)

                st.image(gif_path, width='stretch')

        elif model_label == "SEIARD":
            cfg_seiard = ConfigSEIARD(
                N=N,
                I0=I0,
                seed=42
            )
            model_seiard = ABMNetworkSEIARD(cfg_seiard,interventions=interventions, network_type="watts_strogatz", k=10, beta=0.1, )
            model_seiard.run(days=days_of_sim)
            col1, col2 = st.columns(2)

            with col1:
                fig = plot_history(model_seiard.history, "SEIARD")
                st.pyplot(fig, width='stretch')
                plt.close(fig)

            with col2:
                ani = animate_network_spread(model_seiard, interval=1000, model_type="SEIARD")
                gif_path = f"{model_label}_network.gif"
                ani.save(gif_path, writer="pillow", fps=2)

                st.image(gif_path, width='stretch')

        else:
            #SIR
            cfg_sir = Config(
                N=N,
                I0=I0,
                seed=42
            )
            model_sir = ABMNetwork(cfg_sir, interventions=interventions, network_type="watts_strogatz", k=10, beta=0.1)
            model_sir.run(days=days_of_sim)

            #SEIRD
            cfg_seird = ConfigSEIRD(
                N=N,
                I0=I0,
                seed=42
            )
            model_seird = ABMNetworkSEIRD(cfg_seird, interventions=interventions, network_type="watts_strogatz", k=10,
                                          beta=0.1, )
            model_seird.run(days=days_of_sim)

            #SEIARD
            cfg_seiard = ConfigSEIARD(
                N=N,
                I0=I0,
                seed=42
            )
            model_seiard = ABMNetworkSEIARD(cfg_seiard, interventions=interventions, network_type="watts_strogatz",
                                            k=10, beta=0.1, )
            model_seiard.run(days=days_of_sim)

            col_sir, col_seird, col_seiard = st.columns(3)
            with col_sir:
                st.caption("SIR")
                fig = plot_history(model_sir.history, "SIR")
                st.pyplot(fig, width='stretch')
            with col_seird:
                st.caption("SEIRD")
                fig = plot_history(model_seird.history, "SEIRD")
                st.pyplot(fig, width='stretch')
            with col_seiard:
                st.caption("SEIARD")
                fig = plot_history(model_seiard.history, model_type="SEIARD")
                st.pyplot(fig, width='stretch')


def render_top_bar():
    with st.container():
        col1, col2 = st.columns([1, 9])
        with col1:
            if st.button("🏠 Home", key="home_btn"):
                st.session_state.screen = "model_select"

def main():
    st.set_page_config(page_title="INFLUENZA SIMULATION", layout="wide")
    st.markdown(
        """
        <style>
        .stAnchor {
            display: none !important;
        }
        </style>
        """,
        unsafe_allow_html=True
    )
    init_state()
    render_top_bar()

    if st.session_state.screen == "model_select":
        model_selection_screen()
    else:
        parameters_and_simulation_screen()

if __name__ == "__main__":
    main()