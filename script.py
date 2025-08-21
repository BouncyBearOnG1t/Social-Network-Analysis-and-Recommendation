import pandas as pd
import networkx as nx
import matplotlib.pyplot as plt
from networkx.algorithms.community import greedy_modularity_communities

df = pd.read_csv("facebook_combined.txt", sep=" ", comment="#", header=None)
G = nx.from_pandas_edgelist(df, 0, 1)
print(nx.number_of_edges(G))

degree = nx.degree_centrality(G)

top_influencers = sorted(degree.items(), key=lambda x: x[1], reverse=True)[:10]

nodes, scores = zip(*top_influencers)

# Create bar chart
plt.figure(figsize=(10, 6))
plt.bar(range(len(nodes)), scores, color='skyblue')
plt.xticks(range(len(nodes)), nodes)
plt.xlabel('Node')
plt.ylabel('Degree Centrality Score')
plt.title('Top 10 Influencers by Degree Centrality')
plt.show()

communities = list(greedy_modularity_communities(G))
print(f"Number of communities: {len(communities)}")

shortest = nx.shortest_path(G,source=1,target=40)
print(len(shortest) - 1) 

influencer_nodes = [node for node, score in top_influencers]


color_map = []

for node in G.nodes():
    if node in influencer_nodes:
        color_map.append('red')        # Influencer nodes in red
    else:
        # Assigning community colors (example: blue for community 0, green for community 1 etc.)
        assigned = False
        for i, community in enumerate(communities):
            if node in community:
                community_colors = ['blue','green','orange','purple','cyan','magenta','yellow','brown','pink','lime','teal','gold','navy']
                color_map.append(community_colors[i % len(community_colors)])
                assigned = True
                break
        if not assigned:
            color_map.append('gray')


plt.figure(figsize=(12,12))
pos = nx.spring_layout(G,k=0.5) 
nx.draw_networkx_edges(G, pos, alpha=0.3)

path_edges = list(zip(shortest, shortest[1:]))
nx.draw_networkx_edges(G, pos, edgelist=path_edges, edge_color='red', width=2)
nx.draw(G, pos, node_color=color_map, with_labels=False, node_size=10)

plt.show()

non_edges = list(nx.non_edges(G))
preds = nx.adamic_adar_index(G, non_edges)

top_recommendations = sorted(preds, key=lambda x: x[2], reverse=True)[:10]

print("Top friend recommendations:")
for u, v, score in top_recommendations:
    print(f"Recommend user {u} to connect with user {v} (score: {score:.3f})")

pairs = [f"{u}-{v}" for u,v,s in top_recommendations]
scores = [s for _,_,s in top_recommendations]

plt.figure(figsize=(8,4))
plt.barh(pairs, scores, color='skyblue')
plt.xlabel('Recommendation Score')
plt.title('Top Friend Recommendations')
plt.gca().invert_yaxis()
plt.show()