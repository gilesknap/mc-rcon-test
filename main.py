from vector import vector
from snippets import (
    player_pos,
    make_walls,
    players_in,
)
from box import box
from mcipc.rcon.je import Client
from mcipc.rcon.types import FillMode, Vec3
from time import sleep


def setup(client: Client):
    # don't announce every rcon command
    client.gamerule("sendCommandFeedback", False)
    # clear above top of mountain
    center = vector(-14112, 100, 4100)
    for y in range(30):
        bounds = box.centered(center.up(y), 100, 1, 100)
        client.fill(bounds.start, bounds.end, "air", FillMode.REPLACE)  # type: ignore


def players_pos(client: Client):
    names = [p.name for p in client.players.players]
    for name in names:
        pos = player_pos(client, name)
        print(f"player {name} is at {pos}")


def animate_saucer(client, middle):
    for z in range(200):
        offset = Vec3(0, 0, z)
        flying_saucer(client, middle + offset)
        sleep(0.2)


saucer = box()
old_saucer = box()


def flying_saucer(client: Client, location: vector):
    global saucer, old_saucer
    width: int = 5
    height: int = 1

    # calculate the bounds of the current position
    saucer = box.centered(location, width, 1, width)

    # overwrite the previous location with wool
    client.fill(old_saucer.start, old_saucer.end.up(1), "gray_wool", FillMode.REPLACE)  # type: ignore
    # write the new location with iron_blocks
    client.fill(saucer.start, saucer.end, "iron_block", FillMode.REPLACE)  # type: ignore
    make_walls(client, "iron_block", saucer.start.up(1), saucer.end.up(height))
    # overwrite all old wool with air
    client.fill(
        old_saucer.start,  # type: ignore
        old_saucer.end.up(1),  # type: ignore
        "air",
        FillMode.REPLACE,
        filter="#minecraft:wool",
    )

    for player in players_in(client, saucer.start, saucer.end.up(1)):
        client.teleport(location=location.up(1), targets=player)  # type: ignore
    old_saucer = saucer


science = 25701
quest = 25575

with Client("localhost", science, passwd="spider") as client:
    setup(client)

    middle = vector(-14112, 101, 4100)
    flying_saucer(client, middle)

    while not players_in(client, saucer.start, saucer.end.up(1)):
        sleep(0.1)
    animate_saucer(client, middle)
