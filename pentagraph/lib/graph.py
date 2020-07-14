# -*- coding=utf-8 -*-
#!/usr/bin/env python3

__doc__ = "Pentagame board as operational networkx graph"

import typing
from heapq import heappop, heappush
from itertools import count

from networkx import bidirectional_dijkstra, Graph
from networkx.readwrite.json_graph import node_link_data
from networkx.utils import make_str, to_tuple
from .figures import Figure


class Board(Graph):
    """Class representing a pentagame board"""

    board = None
    COLORS = ()
    EDGEMAP = (
        ("0-0-0", "1-0-0", 3),
        ("0-0-0", "4-0-0", 3),
        ("0-0-0", "5-0-0", 6),
        ("0-0-0", "6-0-0", 6),
        ("1-0-0", "2-0-0", 3),
        ("1-0-0", "6-0-0", 6),
        ("1-0-0", "7-0-0", 6),
        ("2-0-0", "3-0-0", 3),
        ("2-0-0", "8-0-0", 6),
        ("2-0-0", "7-0-0", 6),
        ("3-0-0", "4-0-0", 3),
        ("3-0-0", "8-0-0", 6),
        ("3-0-0", "9-0-0", 6),
        ("4-0-0", "5-0-0", 6),
        ("4-0-0", "9-0-0", 6),
        ("5-0-0", "9-0-0", 3),
        ("5-0-0", "6-0-0", 3),
        ("6-0-0", "7-0-0", 3),
        ("7-0-0", "8-0-0", 3),
        ("8-0-0", "9-0-0", 3),
    )

    def __init__(self, figures: typing.List[list] = [], generate: bool = False):
        """Represents a game board as graph"""
        super().__init__()
        self.figures = figures
        if generate:
            self.gen_simple()

    def produce_figures(self) -> typing.List[Figure]:
        """Returns internal figures to list of Figure class"""
        return [Figure() for figure in self.figures]

    def gen_simple(self):
        """Generate complete graph"""
        for edge in self.EDGEMAP:
            for stop in range(1, edge[2]):
                self.add_edge(
                    f"{edge[0][0]}-{stop}-{edge[1][0]}",
                    f"{edge[0][0]}-{stop + 1}-{edge[1][0]}",
                )
            self.add_edge(f"{edge[0][0]}-{edge[2]}-{edge[1][0]}", edge[1])
            self.add_edge(f"{edge[0][0]}-1-{edge[1][0]}", edge[0])

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
                self.figures_table.__setitem__(figure[1], (figure[0], figure[2]))
                for figure in self.figures
                if figure[0] != "-"
            ]
        else:
            self.figures_table.__setitem__(figure[1], (figure[0], figure[2]))

    def verify_path(self, source: str, target: str) -> typing.Set:
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
        neighs = [self.neighbors, self.neighbors]

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
                    pos = self[v][w]
                else:  # back, must remember to change v,w->w,v
                    pos = self[w][v]
                if (w in table or v in table) and pos not in [target, source]:
                    minweight = pos.get(weight, 100)
                else:
                    minweight = pos.get(weight, 1)  # Prevent way
                vwLength = distances[_dir][v] + minweight

                if w in distances[_dir]:
                    if vwLength < distances[_dir][w]:
                        raise ValueError("Contradictory paths found: negative weights?")
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

    def find_path(self, start: str, end: str) -> set:
        """Finds path from start to end (ignoring figures)

        Args:
            start (str): start node
            end (str): end node

        Returns:
            Path with steps (set): (steps, [start, …, end])
        """
        return bidirectional_dijkstra(self, start, end)

    def add_figure(self, figure: typing.List[list]):
        """Adds figure to board"""
        self.figures.append(figure)
        self.update(figure)

    def move(self, move: list, validate: bool = True) -> None:
        """Update field with move (moves are not yet checked on structure)

        Args:
            move (list): Move as described in https://github.com/Penta-Game/denomination
            validate (bool) [True]: Validate move 
        """
        if move[0]:
            pass
        return

    def jsonify(self) -> typing.Dict[str, list]:
        """Saves board as dict (json)"""
        if self.board is None:
            self.board = self.gen_simple()
        return dict(graph=node_link_data(self), figures=self.figures)

    @staticmethod
    def load(json: dict):
        """Loads graph from json (Board.jsonify())

        Args:
            json (dict): [description]

        Returns:
            [type]: [description]
        """
        graph = Board(generate=False)
        graph.figures = json["figures"]
        print(f"Loaded figures: {json['figures']}")
        graph.update()
        data = json["graph"]
        graph.graph = data.get("graph", {})
        c = count()
        for d in data["nodes"]:
            node = to_tuple(d.get("id", next(c)))
            nodedata = dict((make_str(k), v) for k, v in d.items() if k != "id")
            graph.add_node(node, **nodedata)
        for d in data["links"]:
            src = tuple(d["source"]) if isinstance(d["source"], list) else d["source"]
            tgt = tuple(d["target"]) if isinstance(d["target"], list) else d["target"]
            edgedata = dict(
                (make_str(k), v)
                for k, v in d.items()
                if k != "source" and k != "target"
            )
            graph.add_edge(src, tgt, **edgedata)
        return graph
