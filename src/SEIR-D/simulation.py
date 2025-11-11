import random

import numpy as np
import matplotlib.pyplot as plt
import networkx as nx
from person import Person

# Model parameters
T_MAX = 120
params = {
    'p_infect_IA': 0.05,
    'p_infect_IS': 0.4,
    'p_symptomatic': 0.85,
    'mortality_rate': 0.25,

    'inf_period_mean_IS': 7, 'inf_period_std_IS': 3,
    'inf_period_mean_IA': 3, 'inf_period_std_IA': 1.5,
    'inc_period_mean': 3,
    'inc_period_std': 1.5,
}

# Building the network
# ------------------------------
N = 1000          # number of individuals in the population(nodes)
K = 10             # average degree (each node connected to K nearest neighbors)
P_REWIRE = 0.1    # probability of creating a long contact for each node
SEED = 42
np.random.seed(SEED)
G = nx.watts_strogatz_graph(N,K,P_REWIRE, seed=SEED) # Small-world Graph representing a population

#Creating the population
# ------------------------------
people = [
    Person(pid=i, vaccinated = False, params = params)
    for i in range(N)
]
#Injecting the population with randomly placed infected individuals
initial_infected = random.sample(range(N), 10)
for i in initial_infected:
    people[i].infect()
#Tables for tracking data
history = {'S':[], 'E':[], 'IA':[], 'IS':[], 'R':[], 'D':[]}

#Main simulation loop
# ------------------------------
for t in range(T_MAX):
    new_exposed = set()

    #Each infected person tries to infect its neighbors
    for person in people:
        if person.is_infectious():
            for nbr in G.neighbors(person.id):
                neighbor = people[nbr]
                #If neighbor is Susceptible, is infected with the assigned probability
                if neighbor.state == person.S:
                    p = (person.params['p_infect_IS'] if person.state == person.IS
                        else person.params['p_infect_IA'])
                    if random.random() < p:
                        new_exposed.add(neighbor.id)

    for idx in new_exposed:
        people[idx].infect()
    #Progress the simulation 1 day
    for person in people:
        person.progress()

    #Tracking data
    states = [p.state for p in people]
    history['S'].append(states.count(Person.S))
    history['E'].append(states.count(Person.E))
    history['IA'].append(states.count(Person.IA))
    history['IS'].append(states.count(Person.IS))
    history['R'].append(states.count(Person.R))
    history['D'].append(states.count(Person.D))


#Plotting result
# ------------------------------
plt.figure(figsize=(10,6))
for label, color in zip(['S','E','IA','IS','R','D'],
                        ['blue','orange','purple','red','green','black']):
    plt.plot(history[label], label=label, color=color)
plt.xlabel("Days")
plt.ylabel("Individuals")
plt.title("Network-based SEIAR-D Simulation with Individual Attributes")
plt.legend()
plt.grid(True, linestyle="--", alpha=0.5)
plt.show()