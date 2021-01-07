import asyncio
from mcwc.shapes import funky_cube

from mcwb.types import Direction, Vec3
from mcwc.grab import grab
from mcwc.button import Button

# from player import Player
from mcwc.test_anchor import test_anchor

from mcwc.helper import Helper
from mcipc.rcon.je import Client

from mcwc.saucer import Saucer
from mcwc.cuboid import Cuboid

# my server ports
science = 25701
quest = 25575
flat = 25901


async def runloop(*runners):
    await asyncio.gather(*runners)


# callback function for Button activation
def changed(powered: bool, name: str, id: int):
    print(f"button {name}, id {id} powered:{powered}")


def demo():
    with Client("localhost", flat, passwd="spider") as client:
        helper = Helper(client)

        # don't announce every rcon command
        client.gamerule("sendCommandFeedback", False)

        # will give stuff to players
        # player = Player(client, "TransformerScorn")
        # player.give_stop()

        # MIDDLE : helper.clear_blocks(Vec3(0, 5, 0), 200)
        helper.clear_blocks(Vec3(0, 5, 0), 120)
        test_anchor(client, Vec3(0, 30, -40))

        loc = Vec3(0, 5, -49)
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

        start = Vec3(44, 26, -44)
        end = Vec3(52, 34, -36)
        new_cube = grab(client, start, end)

        runners = [
            Saucer(client, Vec3(0, 40, -60), material="red_concrete").run(),
            Saucer(client, Vec3(10, 40, -60), material="green_concrete").run(),
            Saucer(client, Vec3(20, 40, -60), material="blue_concrete").run(),
            Saucer(client, Vec3(30, 40, -60), material="yellow_concrete").run(),
            Saucer(client, Vec3(40, 40, -60), material="pink_concrete").run(),
            Cuboid(client, Vec3(0, 5, 0), funky_cube(20), 1.0).spin(),
            Cuboid(client, Vec3(48, 26, -64), new_cube).spin(),
            Button.monitor(client),
        ]

        asyncio.run(runloop(*runners))


if __name__ == "__main__":
    demo()
