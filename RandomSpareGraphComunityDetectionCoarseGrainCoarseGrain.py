import networkx as nx
from community import community_louvain
import matplotlib.pyplot as plt
from collections import Counter
import random
# Create an empty graph
G = nx.Graph()

# Add 1001 nodes to the graph
for i in range(1001):
    G.add_node(i)

# Add 10,001 edges to the graph
for i in range(10001):
    node1 = random.randint(0, 999)
    node2 = random.randint(0, 999)
    G.add_edge(node1, node2)

# Convert it to undirected graph for community detection
G_undirected = G.to_undirected()

# Compute the best partition
partition = community_louvain.best_partition(G_undirected)

# Create a new graph to represent the communities
community_graph = nx.Graph()

# Create a node for each community
community_sizes = Counter(partition.values())
for community_id, size in community_sizes.items():
    community_graph.add_node(community_id, size=size)

# Create an edge for each pair of communities if there is an edge between their members in the original graph
for node1 in G_undirected.nodes():
    for node2 in G_undirected.neighbors(node1):
        community1 = partition[node1]
        community2 = partition[node2]
        if community1 != community2:
            if community_graph.has_edge(community1, community2):
                # Increase the weight of the edge if it already exists
                community_graph[community1][community2]['weight'] += 1
            else:
                # Create the edge if it doesn't exist
                community_graph.add_edge(community1, community2, weight=1)

# Visualize the communities
plt.figure(figsize=(8, 8))
pos = nx.spring_layout(community_graph)

# Size of node proportional to the size of the community, multiplied by a factor to make it more visible
node_sizes = [community_graph.nodes[community_id]['size']*50 for community_id in community_graph.nodes()]
nx.draw_networkx_nodes(community_graph, pos, node_size=node_sizes, node_color=list(community_graph.nodes()))
nx.draw_networkx_edges(community_graph, pos, alpha=0.5)
plt.show()
print("done")