from mesa import Agent


class Player(Agent):
    def __init__(self, unique_id, skills: dict, preferences: dict, neighbors: list, model):
        super().__init__(unique_id, model)
        self.model = model
        self.skills = skills
        self.preferences = preferences
        self.neighbors = neighbors
        self.coalition = self.find_present_coalition()
        self.payoff = self.find_current_payoff()
        self.marginal = 0
        self.gained = 0

    def evaluate_utility(self):
        joined = False
        if self.coalition is None:
            self.coalition = self.find_present_coalition()
            self.payoff = self.find_current_payoff()
        present_payoff = self.payoff
        for coalition in self.model.coalitions:
            if coalition.can_player_join(self):
                new_summed_pay, new_pay = coalition.evaluate_join(self)
                if new_summed_pay > 0 and new_pay >= present_payoff:
                    self.gained = new_pay - present_payoff
                    self.marginal=new_summed_pay
                    present_coalition = coalition
                    present_payoff = new_pay
                    if self.coalition is None:
                        new_coal = next((coal for coal in self.model.coalitions if coal.unique_id == \
                                         present_coalition.unique_id), None)
                        self.join_coalition(new_coal)
                        joined = True
                        self.payoff = self.find_current_payoff()



                    # elif self.coalition.unique_id != present_coalition.unique_id:
                    else:
                        self.leave_coalition(self.coalition)
                        new_coal = next((coal for coal in self.model.coalitions if \
                                         coal.unique_id == present_coalition.unique_id),
                                        None)
                        self.join_coalition(new_coal)
                        self.payoff = self.find_current_payoff()
                        joined = True
                    # print('Player ',self.unique_id, 'has left coalition',prev_coal.unique_id, 'to join Coalition',new_coal.unique_id)
        if not joined:
            _,summed= self.coalition.joined_payoff(self)
            self.marginal=self.coalition.summed_payoff-summed
            self.payoff = self.find_current_payoff()
    def find_present_coalition(self):
        for coalition in self.model.coalitions:
            if coalition.is_player_in(self):
                return coalition
        return None

    def find_current_payoff(self):
        if self.coalition:
            return self.coalition.payoffs[self.unique_id]
        else:
            return 0

    def join_coalition(self, coalition):
        coalition.add_player(self)
        self.coalition = coalition

    def leave_coalition(self, coalition):
        self.coalition = None
        coalition.remove_player(self)

    def step(self):

        #agent_collector.update({self.unique_id:{"Marginal Utility" : self.marginal,"Gained" : self.gained}})
        self.evaluate_utility()
