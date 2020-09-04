from ..lib.graph import Board


def test_serialization():
    G = Board(generate=True)
    G.gen_start_field((1, 2, 3, 4, 5))
    data = G.jsonify()

    H = Board.load(data)
    assert H.nodes == G.nodes
    assert H.figures == G.figures
    assert H.figures_table == G.figures_table
    assert H.edges == G.edges
