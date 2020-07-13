import typing
from math import sqrt, pi

# Base Constats for sizes in 2D room
_constants = {
    "l": 6,
    "k": 3,
    "p": sqrt((25 - 11 * sqrt(5)) / (5 - sqrt(5))),
    "golden": (sqrt(5) + 1) / 2,
    "theta": 18
}

_sizes = {
    "s": 1,
    "c": sqrt(5),
    "j": (9 - 2 * sqrt(5)) / sqrt(5),
    "r": (2 / 5) * sqrt(1570 + 698 * sqrt(5))
}

_sizes["R"] = _sizes["r"] + sqrt(5)
_sizes["outer_circle"] = _sizes["r"] / _sizes["R"] * 0.2
_constants["sizes"] = _sizes
_constants["lineWidth"] = 0.1 / _sizes["R"]
CONSTANTS = _constants


def calc(s: int) -> typing.Dict[str, float]:
    board = dict()
    [board.__setitem__(key, s * val) for key, val in CONSTANTS]

    board["circ"] = board.R * pi
    board["degree"] = board.circ / 360
    return board
