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


with Client("localhost", 25901, passwd="spider") as client:
    # clear 150 * 150 * 100 centred on world_middle
    clear: Profile = [[Item.AIR] * 150] * 150
    mktunnel(client, clear, Vec3(75, 5, -75), direction=Direction.UP, length=250)

    mid = Vec3(0, 50, 0)
    knot(client, mid, Anchor.TOP_LEFT)  # all should join at RED
    mid = Vec3(10, 50, 0)
    knot(client, mid, Anchor.TOP_RIGHT)  # all shouls join at GREEN
    mid = Vec3(20, 50, 0)
    knot(client, mid, Anchor.BOTTOM_LEFT)  # joins at BLUE
    mid = Vec3(30, 50, 0)
    knot(client, mid, Anchor.BOTTOM_RIGHT)  # joins at YELLOW
    mid = Vec3(40, 50, 0)
    knot(client, mid, Anchor.MIDDLE)  # joins in center
