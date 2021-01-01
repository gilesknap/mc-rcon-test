from mcipc.rcon.builder.types import Vec3, Direction
from mcipc.rcon import FillMode
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
    helper.render_regions(regions, "red_wool")


science = 25701
quest = 25575
flat = 25901


client = Client("localhost", flat, passwd="spider")
client.__enter__()

helper = Helper(client)
setup(client)

middle = Vec3(347, 14, 189)

saucer = Saucer(client, middle, material="red_concrete")

while True:
    while not helper.players_in(saucer.bounds, ytol=2):
        sleep(0.1)
    for z in range(100):
        saucer.north(1)
        sleep(.2)
    for z in range(100):
        saucer.north(-1)
        sleep(.2)
