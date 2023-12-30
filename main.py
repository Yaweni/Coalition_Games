import itertools
import Player
import Coalition
import Target



def find_stable_coalitions(players, targets):
    # Generate all possible coalitions
    all_coalitions = []
    for r in range(1, len(players) + 1):
        combinations = itertools.combinations(players, r)
        all_coalitions.extend([Coalition(list(comb)) for comb in combinations])

    # Identify stable coalitions
    stable_coalitions = []
    for coalition in all_coalitions:
        preference = coalition.calculate_preference()
        payoffs = coalition.calculate_payoffs()

        # Check if no player has an incentive to deviate
        is_stable = True
        for player in coalition.players:
            better_coalitions = [c for c in all_coalitions if c != coalition and player in c.players]
            for bc in better_coalitions:
                better_preference = bc.calculate_preference()
                better_payoffs = bc.calculate_payoffs()
                if payoffs[player.id] < better_payoffs[player.id] or preference != better_preference:
                    is_stable = False
                    break
            if not is_stable:
                break

        if is_stable:
            stable_coalitions.append(coalition)

    return stable_coalitions


if __name__ == "__main__":
    # Example usage
    # Define players, targets, and their attributes
    player1 = Player(1, ['skill1', 'skill2'], {'target1': 0.7, 'target2': 0.3}, [2])
    player2 = Player(2, ['skill2', 'skill3'], {'target1': 0.4, 'target2': 0.6}, [1, 3])
    player3 = Player(3, ['skill1', 'skill3'], {'target1': 0.5, 'target2': 0.5}, [2])

    players = [player1, player2, player3]

    target1 = Target({'skill1':3, 'skill2':2}, 10)
    target2 = Target({'skill2':1, 'skill3':4}, 15)

    targets = [target1, target2]

    # Find stable coalitions
    stable_coalitions = find_stable_coalitions(players, targets)

    # Print the stable coalitions
    for coalition in stable_coalitions:
        print("Coalition:", [player.id for player in coalition.players])
        print("Payoffs:", coalition.calculate_payoffs())
        print()
