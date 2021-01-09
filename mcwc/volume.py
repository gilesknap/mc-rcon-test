from enum import Enum

from mcipc.rcon.enumerations import Item
from mcipc.rcon.je import Client
from mcwb import Anchor, Direction, Vec3, mktunnel


class Anchor3(Enum):
    """Anchor point for cuboids."""

    MIDDLE = "middle"
    BOTTOM_MIDDLE = "bottom_middle"
    TOP_MIDDLE = "top_middle"

    BOTTOM_SW = "bottom_sw"
    BOTTOM_NW = "bottom_nw"
    BOTTOM_NE = "bottom_ne"
    BOTTOM_SE = "bottom_se"

    TOP_SW = "top_sw"
    TOP_NW = "top_nw"
    TOP_NE = "top_ne"
    TOP_SE = "top_se"


class Volume:
    """
    Describes a 3d space in a Minecraft world using a starting point and
    size. The starting point can be any vertex or the middle of one of the
    horizontal faces, using the cardinal terminology defined in Anchor3
    """

    def __init__(
        self,
        pos: Vec3,
        size: Vec3 = None,
        anchor: Anchor3 = Anchor3.BOTTOM_SW,
        end: Vec3 = None,  # oppsoite corner instead of size and anchor
    ):
        if end is not None:
            npos = Vec3(min(pos.x, end.x), min(pos.y, end.y), min(pos.z, end.z))
            end = Vec3(max(pos.x, end.x), max(pos.y, end.y), max(pos.z, end.z))
            pos = npos
            size = end - pos + 1
            anchor = Anchor3.BOTTOM_NW

        if anchor == Anchor3.BOTTOM_NW:
            # start -> start+size from bottom NW already describes the volume
            # because all axes are at a minimum at that corner
            start = pos
        elif anchor == Anchor3.BOTTOM_SW:
            start = pos + Vec3(0, 0, -size.z + 1)
        elif anchor == Anchor3.BOTTOM_SE:
            start = pos + Vec3(-size.x + 1, 0, -size.z + 1)
        elif anchor == Anchor3.BOTTOM_NE:
            start = pos + Vec3(-size.x + 1, 0, 0)
        elif anchor == Anchor3.BOTTOM_MIDDLE:
            start = pos - Vec3(1, 0, 1) * (size / 2).with_ints()
        elif anchor == Anchor3.MIDDLE:
            start = pos - Vec3(1, 1, 1) * (size / 2).with_ints()
        else:
            # TODO support TOP Anchor3
            raise ValueError("unsupported anchor")

        # decrement 1 to include start block
        self.end = start + (size - 0)
        self.start = start
        self.size = size
        self.position = pos
        self.anchor = anchor

    def fill(self, client: Client, block: Item = Item.AIR):
        """ Fill the Volume with a single block type, supports large volumes """
        if self.size.volume < 32768:
            client.fill(self.start, self.end, block.value)
        else:
            profile = [[block.value] * int(self.size.x)] * int(self.size.y)
            mktunnel(
                client,
                profile,
                self.start,
                direction=Direction.UP,
                anchor=Anchor.BOTTOM_LEFT,
                length=int(self.size.dz),
            )

    def inside(self, position: Vec3, ytol: int = 0) -> bool:
        """ determine if position is within the Volume """
        return (
            self.start.x <= position.x <= self.end.x
            and self.start.y - ytol <= position.y <= self.end.y + ytol
            and self.start.z <= position.z <= self.end.z
        )

    def move(self, distance: Vec3) -> None:
        """ move the volume's location in space by distance """
        self.start += distance
        self.position += distance

    def walls(
        self,
        client: Client,
        block: Item,
        top: bool = True,
        bottom: bool = True,
        n: bool = True,
        s: bool = True,
        e: bool = True,
        w: bool = True,
    ) -> None:
        """ renders walls around the volume """
        b = block.value
        if n:
            client.fill(self.start, Vec3(self.end.x, self.end.y, self.start.z), b)
        if s:
            client.fill(self.end, Vec3(self.start.x, self.start.y, self.end.z), b)
        if w:
            client.fill(self.start, Vec3(self.start.x, self.end.y, self.end.z), b)
        if e:
            client.fill(self.end, Vec3(self.end.x, self.start.y, self.start.z), b)
        if top:
            client.fill(self.end, Vec3(self.start.x, self.end.y, self.start.z), b)
        if bottom:
            client.fill(self.start, Vec3(self.end.x, self.start.y, self.end.z), b)
