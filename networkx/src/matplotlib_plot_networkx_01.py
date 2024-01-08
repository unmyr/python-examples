"""Plot networkx"""
import matplotlib.pyplot as plt
import networkx
from networkx.drawing.nx_agraph import graphviz_layout


def show(nx_g):
    """Show graph"""
    text_font = "sans-serif"
    node_alpha = 0.4
    pos = graphviz_layout(nx_g, prog="circo")
    networkx.draw_networkx_nodes(nx_g, pos, node_color="pink", alpha=node_alpha + 0.5)
    networkx.draw_networkx_edges(nx_g, pos, edge_color="blue", alpha=node_alpha, arrows=False)
    networkx.draw_networkx_labels(nx_g, pos, font_size=12, font_family=text_font)
    plt.savefig("matplotlib_plot_networkx_01.png")


if __name__ == "__main__":
    G = networkx.Graph()
    G.add_nodes_from(["A", "C", "B", "E", "D", "G", "F", "I", "H"])
    G.add_edges_from(
        [
            ("A", "I"),
            ("A", "C"),
            ("A", "B"),
            ("C", "F"),
            ("B", "D"),
            ("E", "F"),
            ("D", "G"),
            ("G", "H"),
        ]
    )
    show(G)
