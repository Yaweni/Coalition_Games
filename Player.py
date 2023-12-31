from mesa import Agent
import copy




class Player(Agent):
    def __init__(self, unique_id, skills, preferences, neighbors,model):
        super().__init__(unique_id, model)
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
                new_summed_pay, new_pay= coalition.evaluate_join(self)
                if new_summed_pay > 0 and new_pay > present_payoff:
                    present_coalition = copy.deepcopy(coalition)
                    present_payoff = new_pay
        if not self.coalition.unique_id == present_coalition.unique_id:
            if self.coalition is not None:
                self.coalition.remove_player(self)
                self.leave_coalition()

            self.join_coalition(present_coalition)
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
        self.coalition = coalition

    def leave_coalition(self):
        self.coalition = None
