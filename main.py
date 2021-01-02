from mcipc.rcon import FillMode
from mcipc.rcon.builder import Item, Vec3, Direction, mktunnel, Profile
from mcipc.rcon.builder.types import Anchor
from box import Box
from helper import Helper
from mcipc.rcon.je import Client
from time import sleep
from saucer import Saucer


def setup(client: Client):
    # don't announce every rcon command
    client.gamerule("sendCommandFeedback", False)
    # clear an area
    center = Vec3(-14112, 100, 4100)
    for y in range(30):

        bounds = Box.centered(center + Direction.UP.value * y, 100, 1, 100)
        client.fill(bounds.start, bounds.end, "air", mode=FillMode.REPLACE)


def test_wall(helper: Helper):
    bounds = Box.centered(middle, 10, 10, 10)
    regions = bounds.walls()
    helper.render_regions(regions, "GLASS")


science = 25701
quest = 25575
flat = 25901

# NOTE checking for a block can be done with
# /loot spawn 10000 10 10000 mine 0 54 0
# but this will spawn the item at 10000 10 10000 s0 best to do entity kill too


def knot(client: Client, mid: Vec3, a: Anchor):
    mktunnel(client, p, mid, direction=Direction.NORTH, length=5, mode=FillMode.KEEP, anchor=a)
    mktunnel(client, p, mid, direction=Direction.SOUTH, length=5, mode=FillMode.KEEP, anchor=a)
    mktunnel(client, p, mid, direction=Direction.EAST, length=5, mode=FillMode.KEEP, anchor=a)
    mktunnel(client, p, mid, direction=Direction.WEST, length=5, mode=FillMode.KEEP, anchor=a)
    mktunnel(client, p, mid, direction=Direction.UP, length=5, mode=FillMode.KEEP, anchor=a)
    mktunnel(client, p, mid, direction=Direction.DOWN, length=5, mode=FillMode.KEEP, anchor=a)


with Client("localhost", flat, passwd="spider") as client:
    helper = Helper(client)
    setup(client)

    middle = Vec3(347, 14, 189)

    saucer = Saucer(client, middle, material="red_concrete")

    while False:
        while not helper.players_in(saucer.bounds, ytol=2):
            sleep(0.1)
        for z in range(100):
            saucer.north(1)
            sleep(0.2)
        for z in range(100):
            saucer.north(-1)
            sleep(0.2)

    p: Profile = [
        [Item.RED_WOOL.value, Item.AIR.value, Item.GREEN_WOOL.value],
        [Item.AIR.value, Item.AIR.value, Item.AIR.value],
        [Item.BLUE_WOOL.value, Item.AIR.value, Item.YELLOW_WOOL.value],
    ]

    # clear 150 * 150 * 100 centred on world_middle
    clear: Profile = [[Item.AIR.value] * 150] * 150
    mktunnel(client, clear, Vec3(75, 5, -75), direction=Direction.UP, length=100)

    mid = Vec3(0, 50, 0)
    mid2 = Vec3(12, 50, 0)
    knot(client, mid, Anchor.TOP_LEFT)
    knot(client, mid2, Anchor.BOTTOM_RIGHT)

