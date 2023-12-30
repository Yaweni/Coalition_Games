import mesa
import pandas as pd
from mesa.datacollection import DataCollector
from mesa.space import NetworkGrid
from mesa.time import RandomActivation
import networkx as nx
import Player
import main

def total_payoffs(model):
    coalitions = model.coalitions
    payoffs = 0
    for coalition in coalitions:
        coal_players = [player for player in model.players if player.unique_id in coalition]
        payoffs += sum([player.payoff for player in coal_players])
    return payoffs

class Networkmodel(mesa.Model):
    """Model containing N terrorist agents connected in a network."""

#   Initializing the model.
    def __init__(self, Graph,players,targets,skills):
        self.graph = Graph
        self.targets = targets
        self.skills = skills
        self.no_agents = nx.number_of_nodes(Graph)
        self.grid = NetworkGrid(Graph)
        self.schedule = RandomActivation(self)
        self.round = 0
        self.running = True
        self.coalitions_sets = [set([i])for i in range(self.no_agents)]
        self.coalitions = None

         # Creating the agents.
        for player in players:
            a = Player.player(player.unique_id, player.skills,player.preferences,player.neighbors,self)
            self.grid.place_agent(a, a.unique_id)
            self.schedule.add(a)
        # Creating collector for difference function defined above.
        self.datacollector = DataCollector(model_reporters={"Total Payoff": total_payoffs})

    def step(self):
        #self.datacollector.collect(self)
        initial_coalitions=self.coalitions
        self.schedule.step()
        if not initial_coalitions == self.coalitions:
            self.round+=1
        else:

            self.running = False
            self.datacollector.collect(self)
            print(f"{self.round} \n")
            df = pd.DataFrame(main.main_lists[1:],columns=main.main_lists[0])
            df.to_csv('250_0.4.csv')



        return

