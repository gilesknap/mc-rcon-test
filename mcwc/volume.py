from enum import Enum

from mcipc.rcon.enumerations import Item
from mcipc.rcon.je import Client
from mcwb import Anchor, Direction, Vec3, mktunnel


class Anchor3(Enum):
    """Anchor point for cuboids."""

    MIDDLE = 'middle'
    BOTTOM_MIDDLE = 'bottom_middle'
    TOP_MIDDLE = 'top_middle'

    BOTTOM_SW = 'bottom_sw'
    BOTTOM_NW = 'bottom_nw'
    BOTTOM_NE = 'bottom_ne'
    BOTTOM_SE = 'bottom_se'

    TOP_SW = 'top_sw'
    TOP_NW = 'top_nw'
    TOP_NE = 'top_ne'
    TOP_SE = 'top_se'


class Volume:
    """
    Describes a 3d space in a Minecraft world using a starting point and
    size. The starting point can be any vertex or the middle of one of the
    horizontal faces, using the cardinal terminology defined in Anchor3
    """
    def __init__(self, start: Vec3, size: Vec3, anchor: Anchor3 = Anchor3.BOTTOM_SW):
        if anchor == Anchor3.BOTTOM_SW:
            # start to start+size from bottom SW already describes the volume
            pass
        elif anchor == Anchor3.BOTTOM_NW:
            start += Vec3(0, 0,  + size.z - 1)
        elif anchor == Anchor3.BOTTOM_MIDDLE:
            start -= Vec3(1, 0, 1) * (size / 2).to_int()
        else:
            # TODO support remaining Anchor3
            raise ValueError("unsupported anchor")

        # invert z so posiitve size is positive North, decrement to include start block
        self.end = start + (size - 1) * Vec3(1, 1, -1)
        self.start = start
        self.size = size

    def fill(self, client: Client, block: Item = Item.AIR):
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
                length=int(self.size.dz)
            )
