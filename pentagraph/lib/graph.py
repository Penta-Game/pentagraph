# -*- coding=utf-8 -*-
#!/usr/bin/env python3

__doc__ = "Pentagame board as operational networkx graph"

import typing
from heapq import heappop, heappush
from itertools import count

from networkx import bidirectional_dijkstra, empty_graph
from networkx.relabel import relabel_nodes
from networkx.readwrite.json_graph import node_link_data, node_link_graph
from .figures import Figure


class Board:
    """Class representing a pentagame board"""

    board = None
    COLORS = (
        ()
    )
    EDGES = (
        ("0", "1", 3),
        ("0", "4", 3),
        ("0", "5", 6),
        ("0", "6", 6),
        ("1", "2", 3),
        ("1", "6", 6),
        ("1", "7", 6),
        ("2", "3", 3),
        ("2", "8", 6),
        ("2", "7", 6),
        ("3", "4", 3),
        ("3", "8", 6),
        ("3", "9", 6),
        ("4", "5", 6),
        ("4", "9", 6),
        ("5", "9", 3),
        ("5", "6", 3),
        ("6", "7", 3),
        ("7", "8", 3),
        ("8", "9", 3),
    )

    def __init__(self, figures: typing.List[list] = [], generate=True):
        """Represents a game board as graph"""
        self.figures = figures
        if generate:
            self.board = self.gen_simple()

    def produce_figures(self) -> typing.List[Figure]:
        """Returns internal figures to list of Figure class"""
        return [
            Figure() for figure in self.figures
        ]

    def gen_simple(self):
        """Generate complete graph"""
        graph = empty_graph()
        for edge in self.EDGES:
            for stop in range(1, edge[2]):
                graph.add_edge(
                    f"{edge[0]}-{stop}-{edge[1]}", f"{edge[0]}-{stop + 1}-{edge[1]}"
                )
            graph.add_edge(f"{edge[0]}-{edge[2]}-{edge[1]}", edge[1])
            graph.add_edge(f"{edge[0]}-1-{edge[1]}", edge[0])

        def relable(label: int) -> str:
            return f"{label}-0-0"

        mapping = dict()
        [mapping.__setitem__(str(i), relable(i)) for i in range(10)]
        return relabel_nodes(graph, mapping)  # Fix "0" -> "0-0-0"

    def gen_start_field(self, players: typing.List[int], update: bool = True) -> None:
        """Generates figures for start field"""
        for i in range(5):
            self.figures.append([i + 6, "-1", -1, 1])
            self.figures.append([i + 11, f"{i}-0-0", -1, 2])

        [
            [self.figures.append([i, f"{i + 5}-0-0", id, 0]) for i in range(5)]
            for id in players
        ]

        self.update()

    def update(self, figure: list = []) -> None:
        self.figures_table = dict()
        if figure == []:
            [
                self.figures_table.__setitem__(
                    figure[1], (figure[0], figure[2]))
                for figure in self.figures
            ]
        else:
            self.figures_table.__setitem__(figure[1], (figure[0], figure[2]))

    def verify_path(self, source: typing.AnyStr, target: typing.AnyStr) -> typing.Set:
        """
        Verifies path while respecting figures 
        Based on https://networkx.github.io/documentation/stable/_modules/networkx/algorithms/shortest_paths/weighted.html#bidirectional_dijkstra
        """

        if source == target:
            return (0, [source])
        push = heappush
        pop = heappop
        # Init:  [Forward, Backward]
        distances = [{}, {}]  # dictionary of final distances
        paths = [{source: [source]}, {target: [target]}]  # dictionary of paths
        # heap of (distance, node) for choosing node to expand
        fringe = [[], []]
        seen = [{source: 0}, {target: 0}]  # dict of distances to seen nodes
        c = count()
        weight = "weight"

        # initialize fringe heap
        push(fringe[0], (0, next(c), source))
        push(fringe[1], (0, next(c), target))

        # neighs for extracting correct neighbor information
        neighs = [self.board.neighbors, self.board.neighbors]

        # figures
        table = self.figures_table
        table.pop(source, None)
        table.pop(target, None)
        table.pop("-1", None)

        # variables to hold shortest discovered path
        finaldist = 1e30000
        finalpath = []
        _dir = 1

        while fringe[0] and fringe[1]:
            # choose direction
            # dir == 0 is forward direction and dir == 1 is back
            _dir = 1 - _dir
            # extract closest to expand
            (dist, _, v) = pop(fringe[_dir])
            if v in distances[_dir]:
                # Shortest path to v has already been found
                continue
            # update distance
            distances[_dir][v] = dist  # equal to seen[dir][v]
            if v in distances[1 - _dir]:
                # if we have scanned v in both directions we are done
                # we have now discovered the shortest path
                if finaldist > 99:
                    return None
                return (finaldist, finalpath)

            for w in neighs[_dir](v):
                if _dir == 0:  # forward
                    pos = self.board[v][w]
                else:  # back, must remember to change v,w->w,v
                    pos = self.board[w][v]
                if (w in table or v in table) and pos not in [target, source]:
                    minweight = pos.get(weight, 100)
                else:
                    minweight = pos.get(weight, 1)  # Prevent way
                vwLength = distances[_dir][v] + minweight

                if w in distances[_dir]:
                    if vwLength < distances[_dir][w]:
                        raise ValueError(
                            "Contradictory paths found: negative weights?")
                elif w not in seen[_dir] or vwLength < seen[_dir][w]:
                    # relaxing
                    seen[_dir][w] = vwLength
                    push(fringe[_dir], (vwLength, next(c), w))
                    paths[_dir][w] = paths[_dir][v] + [w]
                    if w in seen[0] and w in seen[1]:
                        # see if this path is better than than the already
                        # discovered shortest path
                        totaldist = seen[0][w] + seen[1][w]
                        if finalpath == [] or finaldist > totaldist:
                            finaldist = totaldist
                            revpath = paths[1][w][:]
                            revpath.reverse()
                            finalpath = paths[0][w] + revpath[1:]

    def finds_path(self, start: typing.List[int], end: typing.List[int]) -> bool:
        """Finds path from start to end field"""
        return bidirectional_dijkstra(self.board, start, end)

    def add_figure(self, figure: typing.List[list]):
        """Adds figure to board"""
        self.figures.append(figure)
        self.update(figure)

    def jsonify(self) -> typing.Dict[str, list]:
        """Saves board as dict (json)"""
        if self.board is None:
            self.board = self.gen_simple()
        return dict(edges=node_link_data(self.board), figures=self.figures_table)

    @staticmethod
    def load(json: dict):
        """Loads board from json (from Board.jsonify)"""
        instance = Board(generate=False)
        instance.board = node_link_graph(json["edges"])
        instance.figures = json["figures"]
        return instance
