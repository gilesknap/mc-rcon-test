import asyncio
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

# NOTE checking for a block can be done with
# /loot spawn 10000 10 10000 mine 0 54 0
# but this will spawn the item at 10000 10 10000 s0 best to do entity kill too


async def runloop(*runners):
    await asyncio.gather(*runners)


with Client("localhost", flat, passwd="spider") as client:
    helper = Helper(client)
    setup(client)

    player = Player(client, "TransformerScorn")
    player.give_stop()

    helper.clear_blocks(Vec3(0, 5, 0), 200)
    test_anchor(client, Vec3(0, 30, -40))

    runners = [
        Saucer(client, Vec3(0, 40, -60), material="red_concrete").run(),
        Saucer(client, Vec3(10, 40, -60), material="green_concrete").run(),
        Saucer(client, Vec3(20, 40, -60), material="blue_concrete").run(),
        Saucer(client, Vec3(30, 40, -60), material="yellow_concrete").run(),
        Saucer(client, Vec3(40, 40, -60), material="pink_concrete").run(),
        CubeRotator(client, Vec3(0, 5, 0), 10, 1.0).spin(),
    ]

    asyncio.run(runloop(*runners))
