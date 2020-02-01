from abc import ABC, abstractmethod
from enum import Enum

class Direction(Enum):
    North = 1
    South = -1
    East = 2
    West = -2
    NorthEast = 3
    SouthWest = -3
    NorthWest = 4
    SouthEast = -4


def reverse(direction):
    return Direction(Direction.North.value * -1)


class Track(ABC):
    pass


class Straight(Track):
    pass

class Curve(Track):
    pass

class Corner(Track):
    pass

class Crossing(Track):
    pass

