import matplotlib.pyplot as plt
import networkx as nx
from pentagraph.lib.graph import Board

try:
    import pygraphviz
    from networkx.drawing.nx_agraph import graphviz_layout
except ImportError:
    try:
        import pydot
        from networkx.drawing.nx_pydot import graphviz_layout
    except ImportError:
        raise ImportError(
            "This example needs Graphviz and either " "PyGraphviz or pydot"
        )

G = Board(generate=True)
G.gen_start_field([1, 2, 3, 4])
pos = graphviz_layout(G)
plt.figure(figsize=(16, 16))
nx.draw(G, pos, alpha=0.5, with_labels=True, node_size=100)
nx.draw(
    G,
    pos,
    with_labels=True,
    alpha=0.8,
    node_size=1000,
    nodelist=[
        "0-0-0",
        "1-0-0",
        "2-0-0",
        "3-0-0",
        "4-0-0",
        "5-0-0",
        "6-0-0",
        "7-0-0",
        "8-0-0",
        "9-0-0",
    ],
)

plt.savefig("graph.png")

print("Saved graph image to graph.png")
