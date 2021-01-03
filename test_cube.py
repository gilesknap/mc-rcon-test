from mcipc.rcon.builder import Item, Vec3
from mcipc.rcon.je import Client
import numpy as np

from helper import Helper


def make_cube(size: int):
    half = int(size / 2)

    left = [Item.RED_CONCRETE] * size
    right = [Item.GREEN_CONCRETE] * size
    row = [Item.BLUE_CONCRETE] + [Item.AIR] * (size - 2) + [Item.YELLOW_CONCRETE]
    square = [left] + [row] * (size - 2) + [right]

    top = [
        [Item.WHITE_CONCRETE, Item.GRAY_CONCRETE] * half,
        [Item.GRAY_CONCRETE, Item.WHITE_CONCRETE] * half,
    ] * half
    bottom = [[Item.BLACK_CONCRETE, Item.GRAY_CONCRETE] * half] * size

    return [top] + [square] * (size - 2) + [bottom]


def render(client, mid, ncube, solid):
    for idx, block in np.ndenumerate(ncube):
        if solid[idx]:  # meh - why doesn't numpy do a filtered enumerate?
            client.setblock(mid + Vec3(*idx), block)


def spin(cube):
    with Client("localhost", 25901, passwd="spider") as client:
        mid = Vec3(-13, 5, 8)
        Helper(client).clear_blocks(mid, 60)

        ncube = np.array(cube, Item)
        planes = [(0, 1), (0, 2), (1, 2)]

        solid = ncube != Item.AIR

        while True:
            for plane in planes:
                for rot in range(9):
                    render(client, mid, ncube, solid)
                    ncube = np.rot90(ncube, axes=plane)


cube = make_cube(50)
spin(cube)
