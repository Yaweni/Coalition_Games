import Target
import Player
from typing import List
import itertools
class Coalition:
    def __init__(self, players:List[Player],targets:List[Target]):
        self.players = players
        self.game_targets = targets
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

