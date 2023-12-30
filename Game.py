import networkx as nx
from typing import List
import Player


class game_graph:
    def __init__(self):
        self.graph = nx.Graph()

    @classmethod
    def from_players_random(cls, players: int, targets: int, skills: int):



        return cls()


    def construct_graph(self,players):
        edge_list = []
        for player in players:
            for neighbor in player.neighbors:
                edge=[player.id,neighbor]
                edge_list.append(edge)
        self.graph.add_edges_from(edge_list)

