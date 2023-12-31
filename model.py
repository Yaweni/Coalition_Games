import mesa
import pandas as pd
from mesa.datacollection import DataCollector
from mesa.space import NetworkGrid
from mesa.time import RandomActivation
import networkx as nx
import Player
import main
import Coalition
def total_payoffs(model):
    coalitions = model.coalitions
    payoffs = 0
    for coalition in coalitions:
        payoffs += sum(coalition.values())
    return payoffs

class Networkmodel(mesa.Model):
    """Model containing N terrorist agents connected in a network."""

#   Initializing the model.
    def __init__(self, graph, players, targets):
        self.graph = graph
        self.targets = targets
        self.grid = NetworkGrid(graph)
        self.schedule = RandomActivation(self)
        self.round = 0
        self.running = True
        self.coalitions = []


         # Creating the agents.
        for player in players:
            a = Player.player(player.unique_id, player.skills, player.preferences,  player.neighbors,self)
            self.coalitions.append(Coalition.coalition([a], targets))
            self.grid.place_agent(a, a.unique_id)
            self.schedule.add(a)
        # Creating collector for difference function defined above.
        self.datacollector = DataCollector(model_reporters={"Total Payoff": total_payoffs})

    def step(self):
        #self.datacollector.collect(self)
        initial_coalitions = self.coalitions
        self.schedule.step()
        if not initial_coalitions == self.coalitions:
            self.round += 1
        else:

            self.running = False
            self.datacollector.collect(self)
        return

