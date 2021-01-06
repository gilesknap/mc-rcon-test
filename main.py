import asyncio

from mcipc.rcon.builder.types import Direction
from grab import grab
from button import Button
from player import Player
from test_anchor import test_anchor

from helper import Helper
from mcipc.rcon.je import Client
from mcipc.rcon.builder import Vec3

from saucer import Saucer
from cube import CubeRotator


def setup(client: Client):
    # don't announce every rcon command
    client.gamerule("sendCommandFeedback", False)


# my server ports
science = 25701
quest = 25575
flat = 25901


async def runloop(*runners):
    await asyncio.gather(*runners)


# callback function for Button activation
def changed(powered: bool, name: str, id: int):
    print(f"button {name}, id {id} powered:{powered}")


with Client("localhost", flat, passwd="spider") as client:
    helper = Helper(client)
    setup(client)

    # player = Player(client, "TransformerScorn")
    # player.give_stop()

    helper.clear_blocks(Vec3(0, 5, 0), 200)
    test_anchor(client, Vec3(0, 30, -40))

    loc = Vec3(0, 4, -60)
    Button(client, loc, changed)
    loc += Direction.EAST.value
    Button(client, loc, changed)
    loc += Direction.EAST.value
    Button(client, loc, changed)
    loc += Direction.EAST.value
    Button(client, loc, changed)
    loc += Direction.EAST.value
    Button(client, loc, changed, True)
    loc += Direction.EAST.value
    Button(client, loc, changed, True)

    start = Vec3(36, 26, -44)
    end = Vec3(44, 34, -36)
    new_cube = grab(client, start, end)

    runners = [
        Saucer(client, Vec3(0, 40, -60), material="red_concrete").run(),
        Saucer(client, Vec3(10, 40, -60), material="green_concrete").run(),
        Saucer(client, Vec3(20, 40, -60), material="blue_concrete").run(),
        Saucer(client, Vec3(30, 40, -60), material="yellow_concrete").run(),
        Saucer(client, Vec3(40, 40, -60), material="pink_concrete").run(),
        CubeRotator(client, Vec3(0, 5, 0), None, 10, 1.0).spin(),
        CubeRotator(client, Vec3(36, 26, -64), new_cube).spin(),
        Button.monitor(client)
    ]

    asyncio.run(runloop(*runners))
