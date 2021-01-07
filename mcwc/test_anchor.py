from mcipc.rcon.enumerations import FillMode, Item
from mcwb import Vec3, Direction, mktunnel, Profile, Anchor
from mcipc.rcon.je import Client


def knot(client: Client, mid: Vec3, a: Anchor):
    p: Profile = [
        [Item.RED_CONCRETE, Item.AIR, Item.GREEN_CONCRETE],
        [Item.AIR, Item.AIR, Item.AIR],
        [Item.BLUE_CONCRETE, Item.AIR, Item.YELLOW_CONCRETE],
    ]
    f = FillMode.KEEP
    mktunnel(client, p, mid, direction=Direction.NORTH, length=5, mode=f, anchor=a)
    mktunnel(client, p, mid, direction=Direction.SOUTH, length=5, mode=f, anchor=a)
    mktunnel(client, p, mid, direction=Direction.EAST, length=5, mode=f, anchor=a)
    mktunnel(client, p, mid, direction=Direction.WEST, length=5, mode=f, anchor=a)
    mktunnel(client, p, mid, direction=Direction.UP, length=5, mode=f, anchor=a)
    mktunnel(client, p, mid, direction=Direction.DOWN, length=5, mode=f, anchor=a)


def test_anchor(client: Client, mid: Vec3):
    knot(client, mid, Anchor.TOP_LEFT)  # join at RED
    mid += Direction.EAST.value * 12
    knot(client, mid, Anchor.TOP_RIGHT)  # join at GREEN
    mid += Direction.EAST.value * 12
    knot(client, mid, Anchor.BOTTOM_LEFT)  # join at BLUE
    mid += Direction.EAST.value * 12
    knot(client, mid, Anchor.BOTTOM_RIGHT)  # join at YELLOW
    mid += Direction.EAST.value * 12
    knot(client, mid, Anchor.MIDDLE)  # join in middle
