from abc import ABC, abstractmethod
from enum import Enum

class Direction(Enum):
    North = 0
    NorthEast =1
    East = 2
    SouthEast = 3
    South = 4
    SouthWest = 5
    West = 6
    NorthWest = 7

angle_map = {180:[4],135:[3,5],90:[2,6]}



def oppose(direction,angle):
    return [Direction(direction.value + added) for added in angle_map[angle]]


class Track(ABC):

    def __init__(self):
        self.tracks={}

    def connect(self,track,dir):
        self.tracks[dir] = track

    @abstractmethod
    def angle(self):
        pass

class Straight(Track):

    def angle(self):
        return 180


class Curve(Track):

    def next_direction(self, dir):
        pass


class Corner(Track):
    pass

class Crossing(Track):
    pass

