import networkx as nx
from community import community_louvain
import matplotlib.pyplot as plt

# Load the graph from the dataset
G = nx.read_edgelist("cit-HepTh.txt",comments="#",delimiter="\t", create_using=nx.DiGraph(), nodetype=int )

# Convert it to undirected graph for community detection
G_undirected = G.to_undirected()

# Compute the best partition
partition = community_louvain.best_partition(G_undirected)

#modularity of communities
modularity = community_louvain.modularity(partition, G_undirected)
print("Modularity: ", modularity)

#Number of communities
num_communities = max(partition.values()) + 1
print("Number of communities: ", num_communities)

#Sizes of communities
from collections import Counter
community_sizes = list(Counter(partition.values()).values())
print("Sizes of communities: ", community_sizes)
# Compute the basic network properties
num_nodes = len(G.nodes())
num_edges = len(G.edges())
avg_degree = sum([val for (node, val) in G.degree()]) / float(num_nodes)
density = nx.density(G)
print(f"Number of nodes: {num_nodes}")
print(f"Number of edges: {num_edges}")
print(f"Average degree: {avg_degree:.2f}")
print(f"Density: {density:.4f}")
#Degree distribution within communities
degree_sequences = []
for community_id in set(partition.values()):
    nodes_in_community = [nodes for nodes in partition.keys() if partition[nodes] == community_id]
    degree_sequence = sorted([d for n, d in G_undirected.degree(nodes_in_community)], reverse=True)
    degree_sequences.append(degree_sequence)
print(f"Density: {degree_sequences}")    
# Now degree_sequences is a list of degree sequences for each community
# Example for betweenness centrality
betweenness_centrality = nx.betweenness_centrality(G_undirected)
print(f"betweenness_centrality: {betweenness_centrality}")   
# Now betweenness_centrality is a dictionary where the keys are nodes and the values are the betweenness centrality of each node


# Visualize the communities
# plt.figure(figsize=(8, 8))
# pos = nx.spring_layout(G_undirected)
# cmap = plt.cm.get_cmap('viridis', max(partition.values()) + 1)
# nx.draw_networkx_nodes(G_undirected, pos, partition.keys(), node_size=40, cmap=cmap, node_color=list(partition.values()))
# nx.draw_networkx_edges(G_undirected, pos, alpha=0.5)
# plt.show()
print("done")