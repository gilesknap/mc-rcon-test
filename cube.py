import asyncio
from typing import List
from mcipc.rcon.builder import Item, Vec3
from mcipc.rcon.je import Client
import numpy as np

from helper import Helper


class CubeRotator:
    def __init__(
        self,
        client: Client,
        location: Vec3,
        cube: List[List[List[Item]]] = None,
        size: int = 5,
        pause=0.5,
    ) -> None:
        self.client = client
        self.helper = Helper(client)
        self.running = False
        self.pause = pause
        self.location = location
        self.cube = cube or self.make_cube(size)

    def make_cube(self, size: int):
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

    async def render(self, client, mid, ncube, solid):
        for idx, block in np.ndenumerate(ncube):
            if solid[idx]:  # meh - why doesn't numpy do a filtered enumerate?
                await asyncio.sleep(0)
                client.setblock(mid + Vec3(*idx), block)

    async def spin(self) -> None:
        self.running = True

        ncube = np.array(self.cube, Item)
        planes = [(0, 1), (0, 2), (1, 2)]

        solid = ncube != Item.AIR

        while self.running:
            for plane in planes:
                for rot in range(9):
                    await asyncio.sleep(self.pause)
                    await self.render(self.client, self.location, ncube, solid)
                    ncube = np.rot90(ncube, axes=plane)
