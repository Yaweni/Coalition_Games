import Target
import Player
from typing import List
import itertools
class coalition:
    def __init__(self, players:List[Player],targets:List[Target]):
        self.players = players
        self.game_targets = targets
        self.preference = self.calculate_preference()
        self.targets = self.coalition_targets()
        self.payoffs = self.calculate_payoffs()

    def evaluate_join(self,player):
        list_ids = [player.id for player in self.players]
        initial = len(self.targets)
        if any(set(player.neighbors).intersection(list_ids)) and (player.id not in list_ids) :
            self.add_player(player)
            posterior = len(self.targets)
            new_payoff = self.payoffs[player.id]
            new_targets = posterior - initial
            self.remove_player(player)
        if not new_targets>0:
            return 0,0
        else:
            return new_targets,new_payoff




    def add_player(self,player):
        self.players.append(player)
        self.preference = self.calculate_preference()
        self.targets = self.coalition_targets()
        self.payoffs = self.calculate_payoffs()

    def remove_player(self,player):
        self.players.remove(player)
        self.preference = self.calculate_preference()
        self.targets = self.coalition_targets()
        self.payoffs = self.calculate_payoffs()


    def calculate_preference(self):
        preference = {target.name: 0 for target in self.game_targets}
        for player in self.players:
            for target, value in player.preferences.items():
                preference[target] += value
        factor = 1.0/sum(preference.values())
        for k in preference:
            preference[k] = preference[k]*factor
        preference={k: v for k, v in sorted(preference.items(), key=lambda item: item[1],reverse=True)}
        return preference

    def coalition_targets(self):
        coalition_resources = {}
        acquired_targets=[]
        for player in self.players:
            for skill, count in player.skills.items():
                coalition_resources[skill] = coalition_resources.get(skill, 0) + count
        for target in self.game_targets:
            temp_resources=coalition_resources.copy()
            for k in target.skills:
                temp_resources[k]-=target[k]
            acquire=all([v>=0 for v in temp_resources.values()])
            if acquire == True:
                acquired_targets.append(target)
                coalition_resources=temp_resources
        return acquired_targets

    def calculate_payoffs(self):
        payoffs = {player.id: 0 for player in self.players}
        for target in self.targets:
            for player in self.players:
                payoffs[player.id] += target.payoff * player.preferences[target]
        return payoffs

