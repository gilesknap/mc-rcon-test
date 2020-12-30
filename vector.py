from mcipc.rcon.types import Vec3


class vector:
    def __init__(self, x: int, y: int, z: int) -> None:
        self.x = x
        self.y = y
        self.z = z

    @property
    def v(self):
        return Vec3(self.x, self.y, self.z)

    @classmethod
    def from_vec(cls, vec: Vec3):
        return vector(int(vec.x), int(vec.y), int(vec.z))

    def __add__(self, other):
        result = vector(self.x + other.x, self.y + other.y, self.z + other.z)
        return result

    def up(self, y: int) -> "vector":
        return vector(self.x, self.y + y, self.z)

    def north(self, z: int) -> "vector":
        return vector(self.x, self.y, self.z - z)

    def east(self, x: int) -> "vector":
        return vector(self.x + x, self.y, self.z)

    def inside(self, start, end) -> bool:
        return (
            start.x <= self.x <= end.x
            and start.y <= self.y <= end.y
            and start.z <= self.z <= end.z
        )
