
import networkx as nx


def top_eigen_nodes(g: nx.Graph):
    eigenvector_centrality = nx.eigenvector_centrality(g, weight='weight')
    tops = {k: v for k, v in sorted(eigenvector_centrality.items(), key=lambda item: item[1], reverse=True)}
    return [key for key in tops.keys()]

def top_subgraph_nodes(g:nx.Graph):
    subgraph_centrality = nx.subgraph_centrality(g)
    tops = {k: v for k, v in sorted(subgraph_centrality.items(), key=lambda item: item[1], reverse=True)}
    return [key for key in tops.keys()]


def top_degree_nodes(g: nx.Graph):
    degree_centrality = nx.degree_centrality(g)
    tops = {k: v for k, v in sorted(degree_centrality.items(), key=lambda item: item[1], reverse=True)}
    return [key for key in tops.keys()]

def top_betweenness_nodes(g:nx.Graph):
    betweenness_centrality = nx.betweenness_centrality(g,weight='weight')
    tops = {k: v for k, v in sorted(betweenness_centrality.items(), key=lambda item: item[1], reverse=True)}
    return [key for key in tops.keys()]


def top_closeness_nodes(g:nx.Graph):
    closeness_centrality = nx.closeness_centrality(g)
    tops = {k: v for k, v in sorted(closeness_centrality.items(), key=lambda item: item[1], reverse=True)}
    return [key for key in tops.keys()]



