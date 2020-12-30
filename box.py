from vector import vector


class box:
    def __init__(
        self, start: vector = vector(0, 0, 0), end: vector = vector(0, 0, 0)
    ) -> None:
        self.start = start
        self.end = end

    @classmethod
    def centered(cls, center: vector, x_size: int, y_size: int, z_size: int) -> "box":
        # center describes the bottom centre of a bounding box
        start = center + vector(-int(x_size / 2), 0, -int(z_size / 2))
        end = start + vector(x_size - 1, y_size - 1, z_size - 1)
        return box(start, end)

    @property
    def center(self):
        xcenter = self.start.x + int(self.end.x - self.start.x)
        ycenter = self.start.y + int(self.end.y - self.start.y)
        return vector(xcenter, self.start.y, ycenter)

