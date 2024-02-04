import modelCoal
from Target import Target
from NoAgentPlayers import NoAgentPlayer
import pandas as pd
from domination_heuristics import find_dominating_players
from tqdm import tqdm
import centrality_heuristic as ch
import skillcrit_heuristic as sc
import target_heuristic as th
from utils import make_graph_from_players, make_random_game

if __name__ == "__main__":


    # g = make_graph_from_players(players)
    payoff_list = [['Initial Game', 'Removing by MU/c', 'Removing by MUo',\
                    'Removing by Domination','Eigen','Subgraph','Degree','Betweenness','Closeness','Skill Crit','Top Targets']]
    for i in tqdm(range(100)):
        holder = []
        g, players, targets = make_random_game(70, 12, 8, 2, 1)
        dominators = find_dominating_players(g, players)
        top_eigen = ch.top_eigen_nodes(g)
        top_degree = ch.top_degree_nodes(g)
        top_between = ch.top_betweenness_nodes(g)
        top_closeness = ch.top_closeness_nodes(g)
        top_subgraph = ch.top_subgraph_nodes(g)
        top_skill = sc.players_skill_critical(players,targets)
        top_targets = th.find_target_difficulty(players,targets)
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

        players10 = [player for player in players if player.unique_id not in top_skill[:len(agents)]]

        g10 = make_graph_from_players(players10)
        model10 = modelCoal.Networkmodel(g10, players10, targets)
        for coalition in model10.coalitions:
            players_in = [player.unique_id for player in coalition.players]
        while model10.running:
            model10.step()
        summed_payoffs = 0
        for coalition in model10.coalitions:
            summed_payoffs += coalition.summed_payoff
        holder.append(summed_payoffs)

        for target in targets:
            if target.name in top_targets[:len(agents)]:
                target.payoff=0
        model11 = modelCoal.Networkmodel(g,players,targets)
        for coalition in model11.coalitions:
            players_in = [player.unique_id for player in coalition.players]
        while model11.running:
            model11.step()
        summed_payoffs = 0
        for coalition in model11.coalitions:
            summed_payoffs += coalition.summed_payoff
        holder.append(summed_payoffs)
        payoff_list.append(holder)
    df = pd.DataFrame(payoff_list[1:], columns=payoff_list[0])
    df.to_csv('Payoffs_to_heuristics_3')
    payoff_progression = modelCoal.payoffs
    max_length = max([len(list_len) for list_len in payoff_progression])
    for prog_list in payoff_progression:
        pad = [0] * (max_length - len(prog_list))
        prog_list.extend(pad)
    rounds_header = [f"Round {i}" for i in range(0, max_length)]
    df2 = pd.DataFrame(payoff_progression, columns=rounds_header)
    df2.to_csv('Progression Data_3')
    df.plot()
