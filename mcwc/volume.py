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
        position: Vec3,
        size: Vec3,
        anchor: Anchor3 = Anchor3.BOTTOM_SW,
    ):
        if anchor == Anchor3.BOTTOM_NW:
            # start -> start+size from bottom NW already describes the volume
            # because all axes are at a minimum at that corner
            start = position
        elif anchor == Anchor3.BOTTOM_SW:
            start = position + Vec3(0, 0, -size.z + 1)
        elif anchor == Anchor3.BOTTOM_SE:
            start = position + Vec3(-size.x + 1, 0, -size.z + 1)
        elif anchor == Anchor3.BOTTOM_NE:
            start = position + Vec3(-size.x + 1, 0, 0)
        elif anchor == Anchor3.BOTTOM_MIDDLE:
            start = position - Vec3(1, 0, 1) * (size / 2).with_ints()
        elif anchor == Anchor3.MIDDLE:
            start = position - Vec3(1, 1, 1) * (size / 2).with_ints()
        else:
            # TODO support TOP Anchor3
            raise ValueError("unsupported anchor")

        # decrement 1 to include start block
        self.end = start + (size - 0)
        self.start = start
        self.size = size
        self.position = position
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

    def inside(self, pos: Vec3, ytol: int = 0) -> bool:
        """ determine if pos is within the Volume """
        return (
            self.start.x <= pos.x <= self.end.x
            and self.start.y - ytol <= pos.y <= self.end.y + ytol
            and self.start.z <= pos.z <= self.end.z
        )
