import mesa
from mesa import Model
import pandas as pd
from mesa.datacollection import DataCollector
from mesa.space import NetworkGrid
from mesa.time import RandomActivation
import networkx as nx
import Player
import Coalition
import copy
from typing import List

import main

payoffs=[]
def total_payoffs(model):
    payoffs = 0
    for coalition in model.coalitions:
        payoffs += coalition.summed_payoff
    return payoffs


class Networkmodel(Model):
    """Model containing N terrorist agents connected in a network."""

    #   Initializing the model.
    def __init__(self, graph, players, targets):
        super().__init__()
        self.graph = graph
        self.targets = targets
        self.grid = NetworkGrid(graph)
        self.schedule = RandomActivation(self)
        self.rounds = 0
        self.running = True
        self.coalitions = []

        # Creating the agents.
        i = 1
        for player in players:
            a = Player.Player(player.unique_id, player.skills, player.preferences, player.neighbors, self)
            self.coalitions.append(Coalition.coalition(i, [a], targets))
            self.grid.place_agent(a, a.unique_id)
            self.schedule.add(a)
            i += 1
        # Creating collector for difference function defined above.
        self.datacollector = DataCollector(model_reporters={"Total Payoff": total_payoffs,"Number Rounds":"rounds"},\
                                           agent_reporters={"Marginal Utility": "marginal",\
                                                            "Coalition ID":"coalition.unique_id",\
                                                            "Gained Payoff":"gained",\
                                                           "Payoff":"payoff"})
        self.payoff_lists=[]
    def compare_coalition_lists(self,list1 : List[Coalition.coalition], list2: List[Coalition.coalition]):
        members1 = []
        members2 = []
        for coalition in list1:
            a = set([player.unique_id for player in coalition.players])
            members1.append(a)
        members1 = [s for s in members1 if s]
        for coalition in list2:
            a = set([player.unique_id for player in coalition.players])
            members2.append(a)
        members2 = [s for s in members2 if s]
        found = []
        for s_coal in members1:
            found.append(s_coal in members2)
        return all(found)
    def step(self):

        initial_coalitions = copy.deepcopy(self.coalitions)
        self.payoff_lists.append(total_payoffs(self))
        self.schedule.step()
        if not self.compare_coalition_lists(initial_coalitions,self.coalitions):
            self.rounds += 1

        else:

            self.running = False
            payoffs.append(self.payoff_lists)
        self.datacollector.collect(self)

        return
