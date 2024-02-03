import operator

import networkx as nx
import random
from itertools import permutations


def skill_list(players):
    skills_list = []
    for player in players:
        for skill in player.skills:
            skills_list.append(skill)
    skills_list = set(skills_list)
    return skills_list


def find_player_utility(graph: nx.Graph, connected_nodes, total_skills, player, acquired_skills):
    connectivity_utility = len([n for n in graph.neighbors(player) \
                                if n not in connected_nodes]) / graph.number_of_nodes()
    skill_addition = len([skill for skill in graph.nodes[player] \
        ['skills'].keys() if skill not in acquired_skills.keys()]) / len(total_skills.keys())
    skill_density = 0
    for skill in graph.nodes[player]['skills'].keys():
        skill_density += graph.nodes[player]['skills'][skill] / total_skills[skill]
    if len(graph.nodes[player]['skills'].keys()):
        skill_density /= len(graph.nodes[player]['skills'].keys())
    return connectivity_utility + skill_addition + skill_density


def find_skills_total(players, skills):
    '''

    :param players: A list of players in the game
    :param skills:  The name set of skills possesed by players in this game
    :return: A dictionary describing the total amount of every skill
    '''
    skills_dict = {}
    for skill in skills:
        skills_dict[skill] = 0
    for player in players:
        for skill, count in player.skills.items():
            skills_dict[skill] = skills_dict.get(skill, 0) + count
    return skills_dict


def find_dominating_players(graph: nx.Graph, players: list):
    total_skills = find_skills_total(players, skill_list(players))
    dominating_nodes = []
    connected_node_set = []
    acquired_skills = {}
    for id in range(len(list(graph.nodes))):
        player = next((player for player in players if player.unique_id == \
                       id), None)
        graph.nodes[id]['skills'] = player.skills
    order=list(graph.nodes)

    while not all([False for node in list(graph.nodes) if node not in connected_node_set]):

        random.shuffle(order)
        temp_util = {}
        for node in order:
            if node not in dominating_nodes:
                temp_util[node] = find_player_utility(graph, connected_node_set, total_skills, node, acquired_skills)
        top = max(temp_util.items(), key=operator.itemgetter(1))[0]
        dominating_nodes.append(top)
        connected_node_set.extend(list(graph.neighbors(top)))
        connected_node_set.append(top)
        b = set(connected_node_set)  # Dropping duplicates
        connected_node_set = list(b)
        for skill in graph.nodes[top]['skills'].keys():
            acquired_skills[skill] = acquired_skills.get(skill,0)+graph.nodes[top]['skills'][skill]
    return dominating_nodes
