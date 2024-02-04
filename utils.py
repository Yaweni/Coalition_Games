import math
from random import uniform, random, randint

import networkx as nx

from NoAgentPlayers import NoAgentPlayer
from Target import Target

'''
 # Example usage
    # Define players, targets, and their attributes
    player1 = NoAgentPlayer(1, {'skill1': 3, 'skill2': 3}, {'Target 1': 0.7, 'Target 2': 0.3}, [2])
    player2 = NoAgentPlayer(2, {'skill2': 4, 'skill3': 4}, {'Target 1': 0.4, 'Target 2': 0.6}, [1, 3])
    player3 = NoAgentPlayer(3, {'skill1': 2, 'skill3': 2}, {'Target 1': 0.5, 'Target 2': 0.5}, [2])

    players = [player1, player2, player3]

    target1 = Target('Target 1', {'skill1': 3, 'skill2': 2}, 10)
    target2 = Target('Target 2', {'skill2': 1, 'skill3': 4}, 15)

    targets = [target1, target2]
'''
def make_graph_from_players(players):
    edge_list = []
    g = nx.Graph()
    for player in players:
        for neighbor in player.neighbors:
            a = {player.unique_id, neighbor}
            edge_list.append(a)
    g.add_edges_from(edge_list)
    return g


def generate_numbers_summing_to_one(length):
    numbers = [uniform(-1, 1) for _ in range(length - 1)]
    numbers.append(1 - sum(numbers))
    # Normalize the numbers to ensure no value is greater than 1
    max_value = max(numbers) - min(numbers)
    normalized_numbers = [num / max_value for num in numbers]

    return normalized_numbers


def generate_connected_erdos_renyi_graph(n, p):
    while True:
        graph = nx.erdos_renyi_graph(n, p)
        if nx.is_connected(graph):
            return graph
        else:
            # Find all the connected components
            components = list(nx.connected_components(graph))

            # Choose two random components and add an edge between them
            component1 = random.choice(components)
            component2 = random.choice(components)
            node1 = random.choice(list(component1))
            node2 = random.choice(list(component2))
            graph.add_edge(node1, node2)


def generate_connected_barabasi_graph(n, p):
    while True:
        graph = nx.barabasi_albert_graph(n, p)
        if nx.is_connected(graph):
            for (u, v, w) in graph.edges(data=True):
                w['weight'] = 1
            return graph
        else:
            # Find all the connected components
            components = list(nx.connected_components(graph))

            # Choose two random components and add an edge between them
            component1 = random.choice(components)
            component2 = random.choice(components)
            node1 = random.choice(list(component1))
            node2 = random.choice(list(component2))
            graph.add_edge(node1, node2)


def make_random_game(num_players: int, num_targets: int, num_skills, barabasi_neighbors, scale_factor):
    """
    :param num_players: Number of players in the game
    :param num_targets: Number of targets in the game
    :param num_skills: The number of skills distributed in the game
    :param connection_probability: The connection density of the graph of players
    :param scale_factor: Average of how many players could cover a skill requirement,
     should be less than or equal to number of players
    :return: A graph,list of players, list of targets
    """
    assert num_players >= scale_factor
    player_skills_probabilty = [random() for _ in range(num_skills)]
    target_skills_prob = [random() for _ in range(num_skills)]
    # graph = generate_connected_erdos_renyi_graph(num_players, connection_probability)
    graph = generate_connected_barabasi_graph(num_players, barabasi_neighbors)
    targets_list = []
    players_list = []
    for i in range(1, num_targets + 1):
        dict_2 = {}
        for a, prob in zip(range(1, num_skills + 1), target_skills_prob):
            if random() > prob:
                dict_2.setdefault(f'skill{a}', math.ceil(randint(1 * scale_factor, 10 * scale_factor)))
        complexity = len(dict_2.keys())
        if complexity == 0:
            dict_2 = {'skill1': randint(1, 10)}
            complexity = 1
        payoff_target = complexity * randint(complexity, num_skills)
        targets_list.append(Target(f'Target {i}', dict_2, payoff_target))

    for i in range(0, num_players):
        unique_id = i
        skills = {}
        for a, prob in zip(range(1, num_skills + 1), player_skills_probabilty):
            if random() > prob:
                skills.setdefault(f'skill{a}', math.ceil(randint(1, 10)))
        preferences = generate_numbers_summing_to_one(num_targets)
        pref_dict = {}
        for a, prob in zip(range(1, num_targets + 1), preferences):
            pref_dict.setdefault(f'Target {a}', prob)
        players_list.append(NoAgentPlayer(unique_id, skills, pref_dict, list(graph.neighbors(unique_id))))

    return graph, players_list, targets_list
