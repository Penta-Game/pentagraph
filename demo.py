from pentagraph.lib.graphic import render
from pentagraph.lib.graph import Board

if __name__ == "__main__":
    G = Board()
    G.gen_start_field([1, 2, 3, 4])
    render(G)   
