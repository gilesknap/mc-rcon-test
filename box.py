from typing import List
from mcipc.rcon.builder import Vec3, Direction

Regions = List["Box"]


class Box:
    def __init__(self, start: Vec3 = Vec3(0, 0, 0), end: Vec3 = Vec3(0, 0, 0)) -> None:
        self.start = start
        self.end = end

    @classmethod
    def centered(cls, center: Vec3, x_size: int, y_size: int, z_size: int) -> "Box":
        # center describes the bottom centre of a bounding box
        start = center + Vec3(-int(x_size / 2), 0, -int(z_size / 2))
        end = start + Vec3(x_size - 1, y_size - 1, z_size - 1)
        return Box(start, end)

    @property
    def center(self):
        xcenter = self.start.x + int(self.end.x - self.start.x) / 2
        zcenter = self.start.z + int(self.end.z - self.start.z) / 2
        return Vec3(xcenter, self.start.y, zcenter)

    def inside(self, location: Vec3, ytol: int = 0) -> bool:
        return (
            self.start.x <= location.x <= self.end.x
            and self.start.y - ytol <= location.y <= self.end.y + ytol
            and self.start.z <= location.z <= self.end.z
        )

    def up(self, y: int) -> "Box":
        result = Box(self.start, self.end)
        result.start += Direction.UP.value * y
        result.end += Direction.UP.value * y
        return result

    def north(self, z: int) -> "Box":
        result = Box(self.start, self.end)
        result.start += Direction.NORTH.value * z
        result.end += Direction.NORTH.value * z
        return result

    def east(self, x: int) -> "Box":
        result = Box(self.start, self.end)
        result.start += Direction.EAST.value * x
        result.end += Direction.EAST.value * x
        return result

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
            wall = Box(self.start, Vec3(self.end.x, self.end.y, self.start.z))
            result.append(wall)
        # south wall uses max z and range of x,y
        if s:
            wall = Box(self.end, Vec3(self.start.x, self.start.y, self.end.z))
            result.append(wall)
        # west wall uses min x and range of x,y
        if w:
            wall = Box(self.start, Vec3(self.start.x, self.end.y, self.end.z))
            result.append(wall)
        # east wall uses max x and range of z,y
        if e:
            wall = Box(self.end, Vec3(self.end.x, self.start.y, self.start.z))
            result.append(wall)
        # top is max y and range of x, z
        if top:
            wall = Box(self.end, Vec3(self.start.x, self.end.y, self.start.z))
            result.append(wall)
        # bottom is min y and range of x, z
        if bottom:
            wall = Box(self.start, Vec3(self.end.x, self.start.y, self.end.z))
            result.append(wall)

        return result
