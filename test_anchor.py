from mcipc.rcon import FillMode
from mcipc.rcon.builder import Item, Vec3, Direction, mktunnel, Profile
from mcipc.rcon.builder.types import Anchor
from mcipc.rcon.je import Client


def knot(client: Client, mid: Vec3, a: Anchor):
    p: Profile = [
        [Item.RED_CONCRETE, Item.AIR, Item.GREEN_CONCRETE],
        [Item.AIR, Item.AIR, Item.AIR],
        [Item.BLUE_CONCRETE, Item.AIR, Item.YELLOW_CONCRETE],
    ]
    mktunnel(client, p, mid, direction=Direction.NORTH, length=5, mode=FillMode.KEEP, anchor=a)
    mktunnel(client, p, mid, direction=Direction.SOUTH, length=5, mode=FillMode.KEEP, anchor=a)
    mktunnel(client, p, mid, direction=Direction.EAST, length=5, mode=FillMode.KEEP, anchor=a)
    mktunnel(client, p, mid, direction=Direction.WEST, length=5, mode=FillMode.KEEP, anchor=a)
    mktunnel(client, p, mid, direction=Direction.UP, length=5, mode=FillMode.KEEP, anchor=a)
    mktunnel(client, p, mid, direction=Direction.DOWN, length=5, mode=FillMode.KEEP, anchor=a)


def test_anchor(client, location):
    mid = location
    knot(client, mid, Anchor.TOP_LEFT)  # all should join at RED
    mid += Direction.EAST.value * 10
    knot(client, mid, Anchor.TOP_RIGHT)  # all shouls join at GREEN
    mid += Direction.EAST.value * 10
    knot(client, mid, Anchor.BOTTOM_LEFT)  # joins at BLUE
    mid += Direction.EAST.value * 10
    knot(client, mid, Anchor.BOTTOM_RIGHT)  # joins at YELLOW
    mid += Direction.EAST.value * 10
    knot(client, mid, Anchor.MIDDLE)  # joins in center
