from mcipc.rcon import FillMode
from mcipc.rcon.builder import Item, Vec3, Direction, mktunnel, Profile
from mcipc.rcon.builder.types import Anchor
from mcipc.rcon.je import Client
import numpy as np
from time import sleep

from helper import Helper

p: Profile = [
    [Item.RED_CONCRETE, Item.AIR, Item.GREEN_CONCRETE],
    [Item.AIR, Item.AIR, Item.AIR],
    [Item.BLUE_CONCRETE, Item.AIR, Item.YELLOW_CONCRETE],
]


def spin():
    with Client("localhost", 25901, passwd="spider") as client:
        mid = Vec3(-13, 5, 8)

        Helper(client).clear_blocks(mid, 20)

        pn = np.array(p)

        for i in range(10):
            sleep(.3)
            mktunnel(
                client,
                pn,
                mid,
                direction=Direction.UP,
                length=3,
                mode=FillMode.REPLACE,
                anchor=Anchor.MIDDLE,
            )
            pn = np.rot90(pn)


spin()
