from mcipc.rcon.enumerations import Item
from mcwb import Vec3
from mcipc.rcon.je import Client
import re

# The only way to discover a block at a location currently is to spawn its
# mined entity. This is a bit naff. e.g.
#
# loot spawn 0 0 0 mine 0 54 0
# 'Dropped 1 [Green Concrete] from loot table minecraft:blocks/green_concrete'
#
# dump spawned items here - they will fall into the void
dump = Vec3(0, 0, 0)

extract_item = re.compile(r".*minecraft\:(?:blocks\/)?(.+)$")
listify = re.compile(r": \'minecraft\:[^\']*\'\>|\<")


def grab(client: Client, start: Vec3, end: Vec3):
    cube = []
    for z in range(int(start.z), int(end.z + 1)):
        profile = []
        for y in range(int(start.y), int(end.y + 1)):
            row = []
            for x in range(int(start.x), int(end.x + 1)):
                loc = Vec3(x, y, z)
                res = client.loot.spawn(dump).mine(loc)
                match = extract_item.search(res)
                name = match.group(1)
                if name == "empty":
                    name = "air"
                row.append(Item(name))
            profile.append(row)
        cube.append(profile)
    return cube


if __name__ == "__main__":
    with Client("localhost", 25901, passwd="spider") as client:
        # middle knot
        start = Vec3(36, 26, -44)
        end = Vec3(44, 34, -36)
        # green saucer
        start = Vec3(8, 40, -62)
        end = Vec3(12, 43, -58)

        concrete = Vec3(39, 29, -43)

        r = client.execute.if_.block(concrete, Item.BLUE_CONCRETE).run("seed")
        print(r)

        cube = grab(client, start, end)
        print(cube)
        print("\n\n")
        # TODO the correct way to do this is to make Item jsonifyable but this is
        # quick and dirty
        cube_list = listify.sub('', str(cube))
        print(cube_list)
