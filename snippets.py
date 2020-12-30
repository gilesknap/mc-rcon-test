# some useful functions
from typing import Tuple
from vector import vector
from mcipc.rcon.types import TargetType, Vec3
from mcipc.rcon.je import Client
import re

# Minecraft Coordinate System
# plus Y is up
# plus X is East
# plus Z is South

# extract the integer coords from a string of the form
#  "DispenserAD11 has the following entity data: \
#   [-2984.3695730161085d, 87.16610926093821d, 54.42824875967167d]"
regex_coord = re.compile(r"\[(-?\d+).?\d*d, *(-?\d+).?\d*d, *(-?\d+).?\d*d\]")


def box_corners(
    center: vector, x_size: int, y_size: int, z_size: int
) -> Tuple[vector, vector]:
    # center describes the bottom centre of a bounding box
    start = center + vector(-int(x_size / 2), 0, -int(z_size / 2))
    end = start + vector(x_size - 1, y_size - 1, z_size - 1)
    return start, end


def make_walls(client: Client, material: str, start: vector, end: vector):
    # north wall uses min z and range of x, y
    client.fill(start.v, Vec3(end.x, end.y, start.z), material)
    # south wall uses max z and range of x,y
    client.fill(end.v, Vec3(start.x, start.y, end.z), material)
    # west wall uses min x and range of x,y
    client.fill(start.v, Vec3(start.x, end.y, end.z), material)
    # east wall uses max x and range of z,y
    client.fill(end.v, Vec3(end.x, start.y, start.z), material)


def player_pos(client: Client, player_name: str) -> vector:
    data = client.data.get(TargetType.ENTITY, player_name, "Pos")
    match = regex_coord.search(data)
    if match:
        result = vector(int(match.group(1)), int(match.group(2)), int(match.group(3)))
        return result
    else:
        raise ValueError(f"player {player_name} does not exist")


def players_in(client: Client, start, end):
    result = []

    names = [p.name for p in client.players.players]
    for name in names:
        pos = player_pos(client, name)
        if pos.inside(start, end):
            result.append(name)

    return result
