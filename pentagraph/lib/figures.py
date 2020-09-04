import typing


def clamp(source: typing.Tuple[int, int, int]) -> typing.Tuple[int, ...]:
    """Helper for clamping rgb values

    Args:
        source (Tuple[int, int, int]): values to be clamped

    Returns:
        value (Tuple[int, int, int]): clamped values
    """
    return tuple(max(0, min(value, 255)) for value in source)


class Point:
    type: typing.Text

    def __init__(self, postion: typing.Tuple[int, int, int]):
        self.position = postion

    def node_label(self) -> str:
        """Builds node label from Point.position

        Raises:
            ValueError: Position is corrupted or malformed
            TypeError: Type of position was false. Required: List[int]

        Returns:
            str: Node label
        """

        if self.position[0] > self.position[2]:
            return f"{self.position[0]}-{self.position[1]}-{self.position[2]}"
        else:
            return f"{self.position[2]}-{self.position[1]}-{self.position[0]}"


class Corner(Point):
    type = "Corner"


class Junction(Point):
    type = "Junction"


class Stopper:
    type = "Stopper"


class Figure:
    type: typing.Text
    color: typing.Tuple[int, int, int] = (0, 0, 0)
    hexcolor: typing.Text
    position: typing.Tuple[int, int, int]
    _node: str

    def __init__(
        self,
        position: typing.Tuple[int, int, int],
        uid: int,
        **attrs,
    ):
        """Class representing a figure

        Args:
            position (int): Position of figure
            uid (int): uid of figure (player id or -1)
        """
        self.position = position
        self.uid = uid
        self.attrs = attrs
        self.update_node()

    def update_node(self):
        """Updates node label base on positon"""
        self._node = self.node_label()

    def move(self, target: typing.Tuple[int, int, int]) -> None:
        """Moves figure from current position to start"""
        self.position = target
        self.update_node()
        return

    def node_label(self) -> str:
        """Generates node label from position

        Raises:
            ValueError: When position not convertable

        Returns:
            str: node label
        """
        if self.position[0] == -1:
            return "-1"
        elif self.position[1] == 0 and self.position[2] == 0:
            return f"{self.position[0]}-0-0"
        elif self.position[0] > self.position[2]:
            return f"{self.position[0]}-{self.position[1]}-{self.position[2]}"
        elif self.position[2] > self.position[0]:
            return f"{self.position[2]}-{self.position[1]}-{self.position[0]}"
        else:
            raise ValueError(
                f"Position {self.position} isn't convertible, invalid format?"
            )

    def jsonify(self, hexcolors: bool = False) -> dict:
        """Produce dict containing relevant attributes

        Returns:
            dict: relevant attributes of figure
        """
        if hexcolors:
            return dict(
                type=self.type,
                position=self.position,
                uid=self.uid,
                color=self.hexcolor,
            )
        else:
            return dict(
                type=self.type, position=self.position, uid=self.uid, color=self.color
            )

    def __repr__(self) -> str:
        return f"<Figure {self.uid}>"

    def __eq__(self, value) -> bool:
        if isinstance(value, Figure) is False:
            raise TypeError("Figures can only compare to figures")
        return self.uid == value.uid and self.position == value.position


class BlackStopper(Figure):
    type = "black stopper"
    color = (0, 0, 0)
    hexcolor = "#000000"


class GrayStopper(Figure):
    type = "gray stopper"
    color = (44, 44, 44)
    hexcolor = "#2c2c2c"


class Player(Figure):
    type = "player"

    def __init__(
        self,
        position: typing.Tuple[int, int, int],
        uid: int,
        color: typing.Tuple[int, int, int],
        **attrs,
    ):
        """Player Figure

        Args:
            position (List[int]): Position on board ((-1))] for not on board (e.g. after reaching goal))
            uid (int): uid of player
            color (typing.set[int]): rgb color as set (r, g, b)
        """
        super().__init__(position, uid, **attrs)
        self.color = typing.cast(typing.Tuple[int, int, int], clamp(color))
        self.hexcolor = f"#{self.color[0]:02x}{self.color[1]:02x}{self.color[2]:02x}"


TYPES = {
    Player.type: Player,
    GrayStopper.type: GrayStopper,
    BlackStopper.type: BlackStopper,
}

FigureType = typing.Union[Player, GrayStopper, BlackStopper, Figure]
