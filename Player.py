from mesa import Agent
import copy

import modelCoal


class Player(Agent):
    def __init__(self, unique_id, skills : dict, preferences :dict, neighbors : list, model: modelCoal.Networkmodel):
        super().__init__(unique_id, model)
        self.model = model
        self.skills = skills
        self.preferences = preferences
        self.neighbors = neighbors
        self.coalition = self.find_present_coalition()
        self.payoff = self.find_current_payoff()

    def evaluate_utility(self):
        present_payoff = self.payoff
        present_coalition = copy.deepcopy(self.coalition)
        for coalition in self.model.coalitions:
            if coalition.can_player_join(self):
                new_summed_pay, new_pay = coalition.evaluate_join(self)
                if new_summed_pay >= 0 and new_pay >= present_payoff:
                    present_coalition = copy.deepcopy(coalition)
                    present_payoff = new_pay
                if self.coalition is None:
                    new_coal = next((coal for coal in self.model.coalitions if coal.unique_id == \
                                     present_coalition.unique_id), None)
                    self.join_coalition(new_coal)

                    self.payoff = self.find_current_payoff()

                #elif self.coalition.unique_id != present_coalition.unique_id:
                else:
                    self.leave_coalition(self.coalition)
                    new_coal = next((coal for coal in self.model.coalitions if \
                                     coal.unique_id == present_coalition.unique_id),
                                    None)
                    self.join_coalition(new_coal)
                    self.payoff = self.find_current_payoff()

    def find_present_coalition(self):
        for coalition in self.model.coalitions:
            if coalition.is_player_in(self):
                return coalition
        return None

    def find_current_payoff(self):
        if self.coalition is not None:
            return self.coalition.payoffs()[self.unique_id]
        else:
            return 0

    def join_coalition(self, coalition):
        coalition.add_player(self)
        self.coalition = coalition

    def leave_coalition(self, coalition):
        self.coalition = None
        coalition.remove_player(self)

    def step(self):
        self.evaluate_utility()
