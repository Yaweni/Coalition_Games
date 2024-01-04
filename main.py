from random import sample, random
from itertools import combinations, groupby
import modelCoal
from Target import Target
import Player
from NoAgentPlayers import NoAgentPlayer
import networkx as nx
import importlib
import pandas as pd

agent_collector={}
def make_graph_from_players(players):
    edge_list = []
    g = nx.Graph()
    for player in players:
        for neighbor in player.neighbors:
            a = {player.unique_id, neighbor}
            edge_list.append(a)
    g.add_edges_from(edge_list)
    return g


def gnp_random_connected_graph(n, p):
    """
    Generates a random undirected graph, similarly to an Erdős-Rényi
    graph, but enforcing that the resulting graph is connected """
    edges = combinations(range(n), 2)
    G = nx.Graph()
    G.add_nodes_from(range(n))
    if p <= 0:
        return G
    if p >= 1:
        return nx.complete_graph(n, create_using=G)
    for _, node_edges in groupby(edges, key=lambda x: x[0]):
        node_edges = list(node_edges)
        random_edge = sample(node_edges, 2)
        G.add_edge(*random_edge)
        for e in node_edges:
            if random() < p:
                G.add_edge(*e)
        return G


def make_random_game(num_players: int, num_targets: int, num_skills, connection_probability):
    graph = gnp_random_connected_graph(num_players, connection_probability)
    return



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
    g = make_graph_from_players(players)

    model = modelCoal.Networkmodel(g, players, targets)
    for coalition in model.coalitions:
        players_in = [player.unique_id for player in coalition.players]
        if players_in :
            print(players_in, coalition.summed_payoff)
    while model.running:
        model.step()
    summed_payoffs= 0
    print("Coalitions after first Game")
    for coalition in model.coalitions:
        players_in = [player.unique_id for player in coalition.players]
        if players_in:
            print(players_in, coalition.summed_payoff)
        summed_payoffs+=coalition.summed_payoff
    print("First runtime has payoff ",summed_payoffs)


    data = model.datacollector.get_model_vars_dataframe()
    data.to_csv('Model_data.csv')
    data2 = model.datacollector.get_agent_vars_dataframe()
    data2.to_csv('Agent_data.csv')

    last_step = data2.index.levels[0][-1]
    result=data2.loc[data2.index.get_level_values(0) == last_step].copy()
    result=result.reset_index('Step',drop=True)
    result['AgentID']=result.index
    result=result.reset_index('AgentID',drop=True)
    result = result.loc[result.groupby('Coalition ID')['Marginal Utility'].idxmax()]
    agents=result['AgentID'].to_list()

    players2=[player for player in players if player.unique_id not in agents]
    g2 = make_graph_from_players(players2)

    model2 = modelCoal.Networkmodel(g2, players2, targets)
    for coalition in model2.coalitions:
        players_in = [player.unique_id for player in coalition.players]
        if players_in:
            print(players_in, coalition.summed_payoff)
    while model2.running:
        model2.step()
    summed_payoffs= 0
    print("Coalitions after second game")
    for coalition in model2.coalitions:
        players_in = [player.unique_id for player in coalition.players]
        if players_in:
            print(players_in, coalition.summed_payoff)
        summed_payoffs+=coalition.summed_payoff
    print("Second runtime has payoff ",summed_payoffs)

