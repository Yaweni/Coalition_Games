from random import sample, random, randint, uniform
from itertools import combinations, groupby
import modelCoal
from Target import Target
from NoAgentPlayers import NoAgentPlayer
import networkx as nx
import math
import pandas as pd
from domination_heuristics import find_dominating_players
from tqdm import tqdm
import centrality_heuristic as ch


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


if __name__ == "__main__":

    # Example usage
    # Define players, targets, and their attributes
    player1 = NoAgentPlayer(1, {'skill1': 3, 'skill2': 3}, {'Target 1': 0.7, 'Target 2': 0.3}, [2])
    player2 = NoAgentPlayer(2, {'skill2': 4, 'skill3': 4}, {'Target 1': 0.4, 'Target 2': 0.6}, [1, 3])
    player3 = NoAgentPlayer(3, {'skill1': 2, 'skill3': 2}, {'Target 1': 0.5, 'Target 2': 0.5}, [2])

    players = [player1, player2, player3]

    target1 = Target('Target 1', {'skill1': 3, 'skill2': 2}, 10)
    target2 = Target('Target 2', {'skill2': 1, 'skill3': 4}, 15)

    targets = [target1, target2]
    # g = make_graph_from_players(players)
    payoff_list = [['Initial Game', 'Removing by MU/c', 'Removing by MUo',\
                    'Removing by Domination','Eigen','Subgraph','Degree','Betweenness','Closeness']]
    for i in tqdm(range(30)):
        holder = []
        g, players, targets = make_random_game(70, 12, 8, 2, 3)
        dominators = find_dominating_players(g, players)
        top_eigen = ch.top_eigen_nodes(g)
        top_degree = ch.top_degree_nodes(g)
        top_between = ch.top_betweenness_nodes(g)
        top_closeness = ch.top_closeness_nodes(g)
        top_subgraph = ch.top_subgraph_nodes(g)
        model = modelCoal.Networkmodel(g, players, targets)
        for coalition in model.coalitions:
            players_in = [player.unique_id for player in coalition.players]
            # if players_in:
            #  print(players_in, coalition.summed_payoff)
        while model.running:
            model.step()
        summed_payoffs = 0
        for coalition in model.coalitions:
            summed_payoffs += coalition.summed_payoff
        holder.append(summed_payoffs)
        data = model.datacollector.get_model_vars_dataframe()
        data.to_csv('Model_data.csv')
        data2 = model.datacollector.get_agent_vars_dataframe()
        data2.to_csv('Agent_data.csv')

        last_step = data2.index.levels[0][-1]
        result = data2.loc[data2.index.get_level_values(0) == last_step].copy()
        result = result.reset_index('Step', drop=True)
        result['AgentID'] = result.index
        result = result.reset_index('AgentID', drop=True)
        result = result.groupby('Coalition ID')
        grouped_df = result
        # grouped_df=data2.loc[data2['Step']==max(data2['Step'])].groupby(['Coalition ID'])
        filtered_df = grouped_df.filter(lambda x: len(x) > 1)
        result_df = filtered_df.loc[filtered_df.groupby('Coalition ID')['Marginal Utility'].idxmax()]
        agents = result_df['AgentID'].tolist()
        # agents = result['AgentID'].to_list()
        agents.sort()

        players2 = [player for player in players if player.unique_id not in agents]
        g2 = make_graph_from_players(players2)

        model2 = modelCoal.Networkmodel(g2, players2, targets)
        for coalition in model2.coalitions:
            players_in = [player.unique_id for player in coalition.players]
        while model2.running:
            model2.step()
        summed_payoffs = 0
        for coalition in model2.coalitions:
            summed_payoffs += coalition.summed_payoff
        holder.append(summed_payoffs)

        data2 = pd.read_csv("Agent_data.csv")
        list_agents = data2.loc[data2['Step'] == max(data2['Step'])].sort_values(['Marginal Utility'], ascending=False)['AgentID'].to_list()

        players3 = [player for player in players if player.unique_id not in list_agents[:len(agents)]]
        g3 = make_graph_from_players(players3)
        agents_list = list_agents[:len(agents)]
        agents_list.sort()
        # print("Payers removed ", agents_list)

        model3 = modelCoal.Networkmodel(g3, players3, targets)
        for coalition in model3.coalitions:
            players_in = [player.unique_id for player in coalition.players]
        while model3.running:
            model3.step()
        summed_payoffs = 0
        for coalition in model3.coalitions:
            summed_payoffs += coalition.summed_payoff
        holder.append(summed_payoffs)

        players4 = [player for player in players if player.unique_id not in dominators[:len(agents)]]
        g4 = make_graph_from_players(players4)
        dom_list = dominators[:len(agents)]

        model4 = modelCoal.Networkmodel(g4, players4, targets)
        for coalition in model4.coalitions:
            players_in = [player.unique_id for player in coalition.players]
        while model4.running:
            model4.step()
        summed_payoffs = 0
        for coalition in model4.coalitions:
            summed_payoffs += coalition.summed_payoff
        holder.append(summed_payoffs)


        players5 = [player for player in players if player.unique_id not in top_eigen[:len(agents)]]
        g5 = make_graph_from_players(players5)

        model5 = modelCoal.Networkmodel(g5, players5, targets)
        for coalition in model5.coalitions:
            players_in = [player.unique_id for player in coalition.players]
        while model5.running:
            model5.step()
        summed_payoffs = 0
        for coalition in model5.coalitions:
            summed_payoffs += coalition.summed_payoff
        holder.append(summed_payoffs)

        players6 = [player for player in players if player.unique_id not in top_subgraph[:len(agents)]]
        g6 = make_graph_from_players(players6)

        model6 = modelCoal.Networkmodel(g6, players6, targets)
        for coalition in model6.coalitions:
            players_in = [player.unique_id for player in coalition.players]
        while model6.running:
            model6.step()
        summed_payoffs = 0
        for coalition in model6.coalitions:
            summed_payoffs += coalition.summed_payoff
        holder.append(summed_payoffs)

        players7 = [player for player in players if player.unique_id not in top_degree[:len(agents)]]
        g7 = make_graph_from_players(players7)

        model7 = modelCoal.Networkmodel(g7, players7, targets)
        for coalition in model7.coalitions:
            players_in = [player.unique_id for player in coalition.players]
        while model7.running:
            model7.step()
        summed_payoffs = 0
        for coalition in model7.coalitions:
            summed_payoffs += coalition.summed_payoff
        holder.append(summed_payoffs)

        players8 = [player for player in players if player.unique_id not in top_between[:len(agents)]]
        g8 = make_graph_from_players(players8)

        model8 = modelCoal.Networkmodel(g8, players8, targets)
        for coalition in model8.coalitions:
            players_in = [player.unique_id for player in coalition.players]
        while model8.running:
            model8.step()
        summed_payoffs = 0
        for coalition in model8.coalitions:
            summed_payoffs += coalition.summed_payoff
        holder.append(summed_payoffs)

        players9 = [player for player in players if player.unique_id not in top_closeness[:len(agents)]]
        g9 = make_graph_from_players(players9)

        model9 = modelCoal.Networkmodel(g9, players9, targets)
        for coalition in model9.coalitions:
            players_in = [player.unique_id for player in coalition.players]
        while model9.running:
            model9.step()
        summed_payoffs = 0
        for coalition in model9.coalitions:
            summed_payoffs += coalition.summed_payoff
        holder.append(summed_payoffs)
        payoff_list.append(holder)
    df = pd.DataFrame(payoff_list[1:], columns=payoff_list[0])
    df.to_csv('Payoffs_to_heuristics_5')
    payoff_progression = modelCoal.payoffs
    max_length = max([len(list_len) for list_len in payoff_progression])
    for prog_list in payoff_progression:
        pad = [0] * (max_length - len(prog_list))
        prog_list.extend(pad)
    rounds_header = [f"Round {i}" for i in range(0, max_length)]
    df2 = pd.DataFrame(payoff_progression, columns=rounds_header)
    df2.to_csv('Progression Data_5')
    df.plot()
