import typing


def clamp(source: typing.Set[int]) -> typing.List[int]:
    """Helper for clamping rgb values

    Args:
        source (Set[int]): values to be clamped

    Returns:
        value (List[int]): clamped values
    """
    return [max(0, min(value, 255)) for value in source]


class Figure:
    type = None

    def __init__(self, position: typing.Set[int], uid: int):
        """Class representing a figure

        Args:
            position (int): Position of figure
            uid (int): uid of figure (player id or -1)
        """
        self.position = position
        self.uid = uid

    def move(self, target: typing.List[int]) -> None:
        """Moves figure from current position to start"""
        self.position = target
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

    def __repr__(self) -> str:
        return f"<Figure {self.uid}>"

    def __eq__(self, value) -> bool:
        if isinstance(value, Figure) is False:
            raise TypeError("Figures can only compare to figures")
        return (self.uid == value.uid and self.position == value.position)


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

    def __init__(self, position: typing.Set[int], uid: int, color: typing.List[float]):
        """Player Figure

        Args:
            position (List[int]): Position on board ([-1] for not on board (e.g. after reaching goal))
            uid (int): uid of player
            color (typing.set[int]): rgb color as set (r, g, b)
        """
        super().__init__(position, uid)
        self.color = clamp(color)
        self.hexcolor = f"#{self.color[0]:02x}{self.color[1]:02x}{self.color[2]:02x}"

