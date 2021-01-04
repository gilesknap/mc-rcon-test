import asyncio
from typing import List
from mcipc.rcon.builder import Item, Vec3
from mcipc.rcon.builder.types import Direction
from mcipc.rcon.je import Client
import numpy as np

from shapes import default_vehicle


class Vehicle:
    def __init__(
        self,
        client: Client,
        location: Vec3,
        cube: List[List[List[Item]]] = None,
        pause: float = 0.5,
        erase_pause: float = 0.1,
    ) -> None:
        self.client = client
        self.running = False
        self.pause = pause
        self.location = location
        self.cube = np.array(cube or default_vehicle)
        self.solid = self.cube != Item.AIR
        self.location: Vec3 = location
        self.old_loc: Vec3 = location
        self.erase_pause = erase_pause
        self.width, self.height, self.depth = self.cube.shape

    async def render(self):
        # render all blocks that are not "air"
        for idx, block in np.ndenumerate(self.cube):
            if self.solid[idx]:
                # allow for large items to render without blocking
                await asyncio.sleep(0)
                self.client.setblock(self.location + Vec3(*idx), block)

    async def unrender(self, vector):
        # clear away exposed blocks from the previous move
        moved = self.shift(self.cube, vector * 1)

        mask = moved == Item.AIR
        mask = mask & (self.cube != Item.AIR)

        for idx, block in np.ndenumerate(self.cube):
            if mask[idx]:
                # allow for large items to render without blocking
                await asyncio.sleep(0)
                self.client.setblock(self.old_loc + Vec3(*idx), Item.AIR.value)

    async def move(self, vector: Vec3):
        self.old_loc = self.location
        self.location += vector
        await self.render()
        await asyncio.sleep(self.erase_pause)
        await self.unrender(vector)
        await asyncio.sleep(self.pause)

    def shift(self, arr, vec):
        result = np.full_like(arr, Item.AIR)
        if vec.y > 0:
            result[:, :vec.y, :] = Item.AIR
            result[:, vec.y:, :] = arr[:, :-vec.y, :]
        elif vec.y < 0:
            result[:, vec.y:, :] = Item.AIR
            result[:, :vec.y, :] = arr[:, -vec.y:, :]
        if vec.x > 0:
            result[:vec.x, :, :] = Item.AIR
            result[vec.x:, :, :] = arr[:-vec.x, :, :]
        elif vec.x < 0:
            result[vec.x:, :, :] = Item.AIR
            result[:vec.x, :, :] = arr[-vec.x:, :, :]
        if vec.z > 0:
            result[:, :, :vec.z:] = Item.AIR
            result[:, :, vec.z:] = arr[:, :, :-vec.z]
        elif vec.z < 0:
            result[:, :, vec.z:] = Item.AIR
            result[:, :, :vec.z] = arr[:, :, -vec.z:]

        return result


if __name__ == "__main__":
    with Client("localhost", 25901, passwd="spider") as client:
        position = Vec3(36, 26, -90)
        v = Vehicle(client, position, cube=default_vehicle, pause=0.1)

        #asyncio.run(v.render())
        for i in range(10):
            asyncio.run(v.move(Direction.DOWN.value))
        for i in range(10):
            asyncio.run(v.move(Direction.UP.value))
        for i in range(10):
            asyncio.run(v.move(Direction.EAST.value))
        for i in range(10):
            asyncio.run(v.move(Direction.SOUTH.value))
        for i in range(10):
            asyncio.run(v.move(Direction.WEST.value))
        for i in range(10):
            asyncio.run(v.move(Direction.NORTH.value))
