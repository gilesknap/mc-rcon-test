import asyncio
from mcipc.rcon.builder.types import Direction
from button import Button
from helper import Helper
from mcipc.rcon.je import Client
from mcipc.rcon.builder import Vec3

flat = 25901


client = Client("localhost", flat, passwd="spider")
client.__enter__()

helper = Helper(client)


async def go(client):
    await Button.monitor(client)


def changed(powered: bool, name: str, id: int):
    print(f"button {name}, id {id} powered:{powered}")


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

asyncio.run(go(client))
