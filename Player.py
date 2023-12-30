from mesa import Agent
import networkx as nx



class player(Agent):
    def __init__(self, unique_id, skills, preferences, neighbors,model):
        super().__init__(unique_id, model)
        self.skills = skills
        self.preferences = preferences
        self.neighbors = neighbors
        self.coalition = None
        self.payoff = None

    def evaluate_utility(self):
        self.model

    def join_coalition(self, coalition):
        self.coalition = coalition

    def leave_coalition(self):
        self.coalition = None
