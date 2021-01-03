from mcipc.rcon.builder import Item, Vec3, Profile
from mcipc.rcon.enumerations import SetblockMode
from mcipc.rcon.je import Client
import numpy as np
from time import sleep

from numpy.lib.function_base import vectorize

from helper import Helper


p = [
    [Item.RED_CONCRETE] * 10,
    [Item.GREEN_CONCRETE] * 10,
    [Item.BLUE_CONCRETE] * 10,
    [Item.YELLOW_CONCRETE] * 10,
    [Item.PINK_CONCRETE] * 10,
    [Item.PURPLE_CONCRETE] * 10,
    [Item.CYAN_CONCRETE] * 10,
    [Item.GRAY_CONCRETE] * 10,
    [Item.BLACK_CONCRETE] * 10,
    [Item.WHITE_CONCRETE] * 10,
]

cube = [p] * 10


def spin():
    with Client("localhost", 25901, passwd="spider") as client:
        mid = Vec3(-13, 5, 8)
        Helper(client).clear_blocks(mid, 50)

        ncube = np.array(cube)
        planes = [(0, 1), (0, 2), (1, 2)]

        for plane in planes:
            for rot in range(9):
                for idx, block in np.ndenumerate(ncube):
                    client.setblock(mid + Vec3(*idx), block)

                ncube = np.rot90(ncube, axes=plane)


spin()
