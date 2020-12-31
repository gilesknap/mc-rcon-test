from typing import List
from vector import vector

Regions = List["Box"]


class Box:
    def __init__(
        self, start: vector = vector(0, 0, 0), end: vector = vector(0, 0, 0)
    ) -> None:
        self.start = start
        self.end = end

    @classmethod
    def centered(cls, center: vector, x_size: int, y_size: int, z_size: int) -> "Box":
        # center describes the bottom centre of a bounding box
        start = center + vector(-int(x_size / 2), 0, -int(z_size / 2))
        end = start + vector(x_size - 1, y_size - 1, z_size - 1)
        return Box(start, end)

    @property
    def center(self):
        xcenter = self.start.x + int(self.end.x - self.start.x)
        ycenter = self.start.y + int(self.end.y - self.start.y)
        return vector(xcenter, self.start.y, ycenter)

    def inside(self, location: vector) -> bool:
        return (
            self.start.x <= location.x <= self.end.x
            and self.start.y <= location.y <= self.end.y
            and self.start.z <= location.z <= self.end.z
        )

    def up(self, y: int):
        self.start = self.start.up(y)
        self.end = self.end.up(y)

    def north(self, z: int):
        self.start = self.start.north(z)
        self.end = self.end.north(z)

    def east(self, x: int):
        self.start = self.start.east(x)
        self.end = self.end.east(x)

    def walls(
        self,
        top: bool = True,
        bottom: bool = True,
        n: bool = True,
        s: bool = True,
        e: bool = True,
        w: bool = True,
    ) -> Regions:
        result = []

        # north wall uses min z and range of x, y
        if n:
            wall = Box(self.start, vector(self.end.x, self.end.y, self.start.z))
            result.append(wall)
        # south wall uses max z and range of x,y
        if s:
            wall = Box(self.end, vector(self.start.x, self.start.y, self.end.z))
            result.append(wall)
        # west wall uses min x and range of x,y
        if w:
            wall = Box(self.start, vector(self.start.x, self.end.y, self.end.z))
            result.append(wall)
        # east wall uses max x and range of z,y
        if e:
            wall = Box(self.end, vector(self.end.x, self.start.y, self.start.z))
            result.append(wall)
        # top is max y and range of x, z
        if top:
            wall = Box(self.end, vector(self.start.x, self.end.y, self.start.z))
            result.append(wall)
        # bottom is min y and range of x, z
        if bottom:
            wall = Box(self.start, vector(self.end.x, self.start.y, self.end.z))
            result.append(wall)

        return result
