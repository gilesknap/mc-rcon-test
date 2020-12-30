from vector import vector
from snippets import (
    player_pos,
    box_corners,
    make_walls,
    players_in,
)
from mcipc.rcon.je import Client
from mcipc.rcon.types import FillMode, Vec3
from time import sleep


def setup(client: Client):
    # don't announce every rcon command
    client.gamerule("sendCommandFeedback", False)
    # clear above top of mountain
    center = vector(-14112, 100, 4100)
    for y in range(30):
        start, end = box_corners(center.up(y), 100, 1, 100)
        client.fill(start.v, end.v, "air", FillMode.REPLACE)


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


old_location = vector(0, 0, 0)
saucer_start = vector(0, 0, 0)
saucer_end = vector(0, 0, 0)


def flying_saucer(client: Client, location: vector):
    global old_location, saucer_start, saucer_end
    width: int = 5
    height: int = 1

    # bootstrap old_location
    if old_location is None:
        old_location = location

    # calculate the corners of the current and prev positions
    old_start, old_end = box_corners(old_location, width, height + 1, width)
    saucer_start, saucer_end = box_corners(location, width, 1, width)

    # overwrite the previous location with wool
    client.fill(old_start.v, old_end.v, "gray_wool", FillMode.REPLACE)
    # write the new location with iron_blocks
    client.fill(saucer_start.v, saucer_end.v, "iron_block", FillMode.REPLACE)
    make_walls(client, "iron_block", saucer_start.up(1), saucer_end.up(height))
    # overwrite all old wool with air
    client.fill(
        old_start.v, old_end.v, "air", FillMode.REPLACE, filter="#minecraft:wool"
    )

    for player in players_in(client, saucer_start, saucer_end.up(1)):
        client.teleport(location=location.up(1).v, targets=player)
    old_location = location


science = 25701
quest = 25575

with Client("localhost", science, passwd="spider") as client:
    setup(client)

    middle = vector(-14112, 101, 4100)
    flying_saucer(client, middle)

    while not players_in(client, saucer_start, saucer_end.up(1)):
        sleep(0.1)
    animate_saucer(client, middle)
