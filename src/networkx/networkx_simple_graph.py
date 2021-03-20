"""Show networks examples."""
import networkx as nx

if __name__ == "__main__":
    G = nx.Graph()
    G.add_node("spam")
    G.add_edge(1, 2)
    print(list(G.nodes()))
    print(list(G.edges()))
