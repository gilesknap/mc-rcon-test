from typing import NamedTuple


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
