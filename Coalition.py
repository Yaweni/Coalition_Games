import Target
import Player
from typing import List
import itertools


class coalition:
    def __init__(self, unique_id, players: List[Player], targets: List[Target]):
        self.unique_id = unique_id
        self.players = players
        self.game_targets = targets
        self.preference = self.calculate_preference()
        self.targets = self.coalition_targets()
        self.payoffs = self.calculate_payoffs()
        self.summed_payoff = self.calculate_summed_payoff()

    def evaluate_join(self, player):
        initial = self.summed_payoff
        new_payoff = 0
        gained_payoff = -1
        if self.can_player_join(player):
            self.add_player(player)
            _, posterior_summed = self.calculate_minus_one_payoff(player)
            new_payoff = self.payoffs[player.id]
            gained_payoff = posterior_summed - initial
            self.remove_player(player)
        return gained_payoff, new_payoff

    def is_player_in(self, player):
        return player in self.players

    def can_player_join(self, player):
        list_ids = [player.unique_id for player in self.players]
        return any(set(player.neighbors).intersection(list_ids)) and (player.unique_id not in list_ids)

    def add_player(self, player):
        self.players.append(player)
        self.preference = self.calculate_preference()
        self.targets = self.coalition_targets()
        self.payoffs = self.calculate_payoffs()
        self.summed_payoff = self.calculate_summed_payoff()

    def remove_player(self, player):
        self.players.remove(player)
        self.preference = self.calculate_preference()
        self.targets = self.coalition_targets()
        self.payoffs = self.calculate_payoffs()
        self.summed_payoff = self.calculate_summed_payoff()

    def calculate_preference(self):
        preference = {target.name: 0 for target in self.game_targets}
        for player in self.players:
            for target, value in player.preferences.items():
                preference[target] += value
        factor = 1.0 / sum(preference.values())
        for k in preference:
            preference[k] = preference[k] * factor
        preference = {k: v for k, v in sorted(preference.items(), key=lambda item: item[1], reverse=True)}
        return preference

    def coalition_targets(self):
        coalition_resources = {}
        acquired_targets = []
        for player in self.players:
            for skill, count in player.skills.items():
                coalition_resources[skill] = coalition_resources.get(skill, 0) + count
        for target in self.game_targets:
            temp_resources = coalition_resources.copy()
            for k in target.skills:
                temp_resources[k] -= target[k]
            acquire = all([v >= 0 for v in temp_resources.values()])
            if acquire:
                acquired_targets.append(target)
                coalition_resources = temp_resources
        return acquired_targets

    def calculate_payoffs(self):
        payoffs = {player.unique_id: 0 for player in self.players}
        for target in self.targets:
            for player in self.players:
                payoffs[player.unique_id] += target.payoff * player.preferences[target]
        return payoffs

    def calculate_summed_payoff(self):
        payoffs = 0
        payoffs += sum(self.payoffs.values())
        return payoffs

    def calculate_minus_one_payoff(self, player1):
        payoffs = {player.unique_id: 0 for player in self.players if player.unique_id != player1.unique_id}
        for target in self.targets:
            for player in self.players:
                if player.unique_id != player1.unique_id:
                    payoffs[player.unique_id] += target.payoff * player.preferences[target]
        summed_pay = 0
        summed_pay += sum(payoffs.values())
        return payoffs, summed_pay
