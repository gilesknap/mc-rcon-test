from mcipc.rcon.builder import Item, Vec3, Profile
from mcipc.rcon.enumerations import SetblockMode
from mcipc.rcon.je import Client
import numpy as np
from time import sleep

from numpy.lib.function_base import vectorize

from helper import Helper

left = [Item.RED_CONCRETE] * 10
right = [Item.GREEN_CONCRETE] * 10
row = [Item.BLUE_CONCRETE] + [Item.AIR] * 8 + [Item.YELLOW_CONCRETE]
square = [left] + [row] * 8 + [right]

top = [[Item.WHITE_CONCRETE, Item.GRAY_CONCRETE] * 5] * 10
bottom = [[Item.BLACK_CONCRETE, Item.GRAY_CONCRETE] * 5] * 10

cube = [top] + [square] * 8 + [bottom]


def spin():
    with Client("localhost", 25901, passwd="spider") as client:
        mid = Vec3(-13, 5, 8)
        Helper(client).clear_blocks(mid, 50)

        ncube = np.array(cube)
        planes = [(0, 1), (0, 2), (1, 2)]

        for plane in planes:
            for rot in range(9):
                sleep(.2)
                for idx, block in np.ndenumerate(ncube):
                    client.setblock(mid + Vec3(*idx), block)

                ncube = np.rot90(ncube, axes=plane)


spin()
