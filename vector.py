from typing import NamedTuple

from mcipc.rcon.builder import Vec3


class vector(NamedTuple):
    x: int
    y: int
    z: int

    def __add__(self, other):
        result = vector(self.x + other.x, self.y + other.y, self.z + other.z)
        return result

    def up(self, y: int) -> "vector":
        return vector(self.x, int(self.y) + y, self.z)

    def north(self, z: int) -> "vector":
        return vector(self.x, self.y, int(self.z) - z)

    def east(self, x: int) -> "vector":
        return vector(int(self.x) + x, self.y, self.z)

    def inside(self, start, end) -> bool:
        return (
            start.x <= self.x <= end.x
            and start.y <= self.y <= end.y
            and start.z <= self.z <= end.z
        )

    @property
    def v(self):
        return Vec3(self.x, self.y, self.z)


class fvector(NamedTuple):
    x: float
    y: float
    z: float

    def __add__(self, other):
        result = fvector(self.x + other.x, self.y + other.y, self.z + other.z)
        return result

    def up(self, y: int) -> "fvector":
        return fvector(self.x, float(self.y) + y, self.z)

    def north(self, z: int) -> "fvector":
        return fvector(self.x, self.y, float(self.z) - z)

    def east(self, x: int) -> "fvector":
        return fvector(float(self.x) + x, self.y, self.z)

    def inside(self, start, end) -> bool:
        return (
            start.x <= self.x <= end.x
            and start.y <= self.y <= end.y
            and start.z <= self.z <= end.z
        )

    @property
    def v(self):
        return Vec3(int(self.x), int(self.y), int(self.z))
