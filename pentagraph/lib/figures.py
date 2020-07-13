import typing
from pentagraph.lib.constants import CONSTANTS


class Figure:
    type = None

    def __init__(self, position: int,  uid: int):
        """Class representing a figure

        Args:
            position (int): Position of figure
            uid (int): uid of figure (player id or -1)
        """
        self.position = position
        self.uid = uid

    def draw(self, base: int) -> typing.Union[str, typing.Set[float]]:
        """'Draws' figure by returning dimensions as set

        Args:
            base (int): Base for dimensions

        Returns:
            str: Type of drawing figure (e.g. ellipse, square)
            typing.List[float]: Dimensions (acceseed by PyQt5.QPainter)
        """
        return

    def move(self, target: typing.List[int]) -> None:
        """Moves figure from current position to start"""
        self.position = target
        return


class BlackStopper(Figure):
    type = "black stopper"
    color = (0, 0, 0)

 