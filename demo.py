from mcipc.rcon.builder import Vec3, Direction
from mcipc.rcon.je import Client
from mcipc.rcon import TargetType
import re

# extract the double coords from a string of the form
#  "DispenserAD11 has the following entity data: \
#   [-2984.3695730161085d, 87.16610926093821d, 54.42824875967167d]"
regex_coord = re.compile(r"\[(-?\d+.?\d*)d, *(-?\d+.?\d*)d, *(-?\d+.?\d*)d\]")


with Client("localhost", 25901, passwd="spider") as client:
    player = "TransformerScorn"
    data = client.data.get(TargetType.ENTITY, player, "Pos")
    match = regex_coord.search(data)
    loc = Vec3(float(match.group(1)), float(match.group(2)), float(match.group(3)))

    loc += Direction.NORTH.value * 2.5

    client.teleport(targets=player, location=loc)
