# -*- coding=utf-8 -*-
#!/usr/bin/env python3

__doc__ = "Pentagame board as operational networkx graph"

import typing
from heapq import heappop, heappush
from itertools import count
from networkx import bidirectional_dijkstra, Graph  # type: ignore
from networkx.readwrite.json_graph import node_link_data  # type: ignore
from networkx.utils import make_str, to_tuple  # type: ignore
from .figures import Figure, Player, GrayStopper, BlackStopper, FigureType, TYPES


class Board(Graph):
    COLORS: typing.Tuple[typing.Tuple[typing.Tuple[int, int, int], str, str], ...] = (
        ((0, 0, 255), "#0000FF", "blue"),
        ((255, 255, 255), "#FFFFFF", "white"),
        ((0, 128, 0), "#0800", "green"),
        ((255, 255, 0), "#FFFF00", "yellow"),
        ((255, 0, 0), "#FF0000", "red"),
    )  # Websafe colors
    figures_table: typing.Dict[
        str, FigureType
    ]  # Lookup table for figures and their respective positions
    figures: typing.List[FigureType]
    EDGEMAP: typing.Tuple[typing.Tuple[str, str, int], ...] = (
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

    def __init__(
        self,
        figures: typing.List[FigureType] = [],
        generate: bool = False,
    ):
        """Graph representing a pentagame board

        Args:
            figures (typing.List[list[int]], optional): Figures as List[int]. Defaults to [].
            generate (bool, optional): Generate nodes and edges from Board.EDGEMAP. Defaults to False.
        """
        super().__init__()
        self.name = self.__repr__()
        self.figures = figures
        if generate:
            self.gen_simple()

    def gen_simple(self):
        """Generate nodes and edges from Board.EDGEMAP. Can be invoked by Board.__init__"""
        fields: typing.List[str] = []
        for edge in self.EDGEMAP:
            if edge[0] not in fields:
                fields.append(edge[0])
                self.add_node(edge[0], weight=1, is_field=True)
            for stop in range(1, edge[2]):
                self.add_node(
                    f"{edge[0][0]}-{stop}-{edge[1][0]}", weight=1, is_field=False
                )
                self.add_node(
                    f"{edge[0][0]}-{stop + 1}-{edge[1][0]}", weight=1, is_field=False
                )
                self.add_edge(
                    f"{edge[0][0]}-{stop}-{edge[1][0]}",
                    f"{edge[0][0]}-{stop + 1}-{edge[1][0]}",
                )
            self.add_node(
                f"{edge[0][0]}-{edge[2]}-{edge[1][0]}", weight=1, is_field=False
            )
            self.add_node(f"{edge[0][0]}-1-{edge[1][0]}", weight=1, is_field=False)
            self.add_edge(f"{edge[0][0]}-{edge[2]}-{edge[1][0]}", edge[1])
            self.add_edge(f"{edge[0][0]}-1-{edge[1][0]}", edge[0])

    def gen_start_field(
        self, players: typing.Tuple[int, ...], update: bool = True, empty: bool = True
    ):
        """Generate Start Field

        Args:
            players (typing.Set[int]): Player uids. Get placed in order of supplied set.
            update (bool, optional): invoke Board.update for figure_table generation(Recommended). Defaults to True.
            empty (bool, optional): empty Board.figures before adding new figures. Defaults to True.
        """
        if empty:
            self.figures = []

        for i in range(5):
            self.figures.append(GrayStopper((-1, -1, -1), i + 6))
            self.figures.append(BlackStopper((i, 0, 0), i + 11))

        for i in range(len(players)):
            self.figures.append(Player((i + 5, 0, 0), players[i], self.COLORS[i][0]))

        if update:
            self.update()

    def update(self, figure: typing.Union[FigureType, None] = None) -> None:
        """Update internal figure lookup table

        Args:
            figure (typing.Union[FigureType, None], optional): Provide only figure to update. Defaults to None.
        """
        if figure is None:
            self.figures_table = {figure._node: figure for figure in self.figures}
        else:
            self.figures_table[figure._node] = figure

    def verify_path(
        self, source: str, target: str
    ) -> typing.Union[None, typing.Tuple[typing.Union[int, float], typing.List[str]]]:
        """
        Verifies path while respecting figures
        Based on https://github.com/networkx/networkx/blob/master/networkx/algorithms/shortest_paths/weighted.py#L1948
        """

        if source == target:
            return (0, [source])
        push = heappush
        pop = heappop
        # Init:  [Forward, Backward]
        distances: typing.List[typing.Dict[str, int]] = [
            {},
            {},
        ]  # dictionary of final distances
        paths = [{source: [source]}, {target: [target]}]  # dictionary of paths
        # heap of (distance, node) for choosing node to expand
        fringe: typing.List[typing.List[typing.Tuple[int, int, str]]] = [[], []]
        seen = [{source: 0}, {target: 0}]  # dict of distances to seen nodes
        c = count()

        # initialize fringe heap
        push(fringe[0], (0, next(c), source))
        push(fringe[1], (0, next(c), target))

        # neighs for extracting correct neighbor information
        neighs = [self.neighbors, self.neighbors]

        # figures
        table = self.figures_table
        table.pop(source, None)
        table.pop(target, None)

        # variables to hold shortest discovered path
        finaldist = 1e30000
        finalpath: typing.List[str] = []
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
                if finaldist > 99:  # Fallback for stopper
                    return None
                return (finaldist, finalpath)

            for w in neighs[_dir](v):
                if _dir == 0:  # forward
                    pos = self[v][w]
                else:  # back, must remember to change v,w->w,v
                    pos = self[w][v]
                if (w in table or v in table) and pos not in [target, source]:
                    minweight = pos.get("weight", 100)
                else:
                    minweight = pos.get("weight", 1)  # Prevent way
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
        assert False

    def add_figure(self, figure: Figure, update: bool = True):
        """Adds figure to board

        Args:
            figure (Figure): [description]
            update (bool): Invoke Board.update([figure]) (Recommended)
        """
        self.figures.append(figure)
        if update:
            self.update(figure)

    def add_figures(self, figures: typing.List[FigureType], update: bool = True):
        """Add figures to board (invokes Board.add_figure)

        Args:
            figures (typing.List[Figure]): Figures
            update (bool): Invoke Board.update([figures]) (Recommended)
        """
        for figure in figures:
            self.add_figure(figure, update=False)
        if update:
            for figure in figures:
                self.update(figure)

    def move(self, move: list, validate: bool = True):
        """Update field with move (moves are not yet checked on structure)

        Args:
            move (list): Move as described in https://github.com/Penta-Game/denomination
            validate (bool) [True]: Validate move
        """
        print("This function is not yet implemented")

    def jsonify(self, hexcolors: bool = False) -> typing.Dict[str, list]:
        """Saves graph data as dict (suitable for Board.load)

        Returns:
            Dict[str, list]: data (nodes, edges, figures)
        """
        return dict(
            graph=node_link_data(self),
            figures=[figure.jsonify(hexcolors=hexcolors) for figure in self.figures],
        )

    @staticmethod
    def load(json: dict):
        """Loads graph from json (Board.jsonify())

        Args:
            json (dict): [description]

        Returns:
            Board: Board loaded with data
        """
        graph = Board(generate=False)
        graph.figures = [TYPES[entry["type"]](**entry) for entry in json["figures"]]
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


class RawBoard(Board):
    figures: typing.List[typing.List[typing.Union[typing.Set[int], int, typing.Tuple[int, int, int]]]]  # type: ignore [assignment]

    def __init__(
        self,
        figures: typing.List[FigureType] = [],
        raw_figures: typing.List[typing.Set[int]] = [],
        generate=False,  # type: ignore [arg-type]
    ):
        """Graph representing a pentagame board
        Internal data is stored in primitive types. This reduces overhead but also also input validation.

        Args:
            figures: Not supported but kept for mypy linting (will be ignored)
            raw_figures (typing.List[list[int]], optional): Figures as List[int]. Defaults to [].
            generate (bool, optional): Generate nodes and edges from Board.EDGEMAP. Defaults to False.
        """
        super().__init__(generate=generate)

    def gen_start_field(
        self,
        players: typing.Tuple[int, ...] = (),
        update: bool = True,
        empty: bool = True,
    ):
        """Generate Start Field

        Args:
            players (typing.Set[int]): Player uids. Get placed in order of supplied set.
            update (bool, optional): invoke Board.update for figure_table generation(Recommended). Defaults to True.
            empty (bool, optional): empty Board.figures before adding new figures. Defaults to True.
        """
        if empty:
            self.figures = []

        for i in range(5):
            self.figures.append([(-1, -1, -1), i + 6])
            self.figures.append([(i, 0, 0), i + 11])

        for i in range(len(players)):
            self.figures.append([(i + 5, 0, 0), players[i], self.COLORS[i][0]])

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

    def jsonify(self, hexcolors: bool = False) -> typing.Dict[str, list]:
        """Saves graph data as dict (suitable for Board.load)

        Arguments:
            hexcolors [bool]: Return colors as hexcolors instead of set. Default: False

        Returns:
            typing.Dict[str, list]: data (nodes, edges, figures)
        """
        return dict(graph=node_link_data(self), figures=self.figures)
