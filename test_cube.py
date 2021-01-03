from mcipc.rcon.builder import Item, Vec3
from mcipc.rcon.je import Client
import numpy as np

from helper import Helper

size = 20
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

cube = [top] + [square] * (size - 2) + [bottom]


def spin():
    with Client("localhost", 25901, passwd="spider") as client:
        mid = Vec3(-13, 5, 8)
        Helper(client).clear_blocks(mid, 60)

        ncube = np.array(cube)
        planes = [(0, 1), (0, 2), (1, 2)]

        solid = (ncube != Item.AIR).flatten()

        for plane in planes:
            for rot in range(9):
                for (idx, block), is_solid in zip(np.ndenumerate(ncube), solid):
                    if is_solid:  #  meh - why doesn't numpy do a filtered enumerate?
                        client.setblock(mid + Vec3(*idx), block)

                ncube = np.rot90(ncube, axes=plane)


spin()
