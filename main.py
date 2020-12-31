from vector import vector
from box import Box
from helper import Helper
from mcipc.rcon.je import Client
from mcipc.rcon.types import FillMode
from time import sleep
from saucer import Saucer


def setup(client: Client):
    # don't announce every rcon command
    client.gamerule("sendCommandFeedback", False)
    # clear above top of mountain
    center = vector(-14112, 100, 4100)
    for y in range(30):
        bounds = Box.centered(center.up(y), 100, 1, 100)
        client.fill(bounds.start, bounds.end, "air", FillMode.REPLACE)  # type: ignore


def test_wall(helper: Helper):
    bounds = Box.centered(middle, 10, 10, 10)
    regions = bounds.walls()
    helper.render_regions(regions, "red_wool")


science = 25701
quest = 25575

with Client("localhost", science, passwd="spider") as client:
    helper = Helper(client)
    setup(client)

    middle = vector(-14112, 101, 4100)

    saucer = Saucer(client, middle)

    while not helper.players_in(saucer.bounds):
        sleep(0.1)
    for z in range(100):
        saucer.north(1)
        sleep(.5)
