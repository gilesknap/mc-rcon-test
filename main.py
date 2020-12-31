from typing import Tuple, Union
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

#vector = Tuple[Union[int, float, str], Union[int, float, str], Union[int, float, str]]

with Client("localhost", science, passwd="spider") as client:
    helper = Helper(client)
    setup(client)

    middle = vector(-14112, 99, 4100)

    saucer = Saucer(client, middle)

    # for i in range(3):
    #     pos = helper.player_pos("@p")
    #     print(pos)
    #     pos = pos.north(-1)
    #     print(pos)
    #     client.teleport(targets="@p", location=pos)  # type: ignore

    while True:
        while not helper.players_in(saucer.bounds):
            sleep(0.1)
        for z in range(100):
            saucer.north(1)
            sleep(.1)
        for z in range(100):
            saucer.north(-1)
            sleep(.1)
