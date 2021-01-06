import asyncio
from typing import List
from mcipc.rcon.enumerations import Item
from mcwb import Vec3, Direction
from mcipc.rcon.je import Client
from mcwc.helper import Helper
import numpy as np

from mcwc.shapes import default_vehicle


class Vehicle:
    def __init__(
        self,
        client: Client,
        location: Vec3,
        cube: List[List[List[Item]]] = None,
        pause: float = 0.5,
        erase_pause: float = 0.3,
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
        self.helper = Helper(client)

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
        self.move_players(vector)
        await self.render()
        await asyncio.sleep(self.erase_pause)
        await self.unrender(vector)
        await asyncio.sleep(self.pause)

    def move_players(self, vector: Vec3):
        players = []

        names = [p.name for p in self.client.players.players]
        for name in names:
            try:
                pos = self.helper.player_pos(name)
                if self.inside(pos, 2):
                    players.append(name)
            except ValueError:
                pass  # players somtimes are missing temporarily

        for player in players:
            pos = self.helper.player_pos(player)
            pos += vector

            self.client.teleport(targets=player, location=pos)

    def inside(self, pos: Vec3, ytol: int = 0) -> bool:
        return (
            self.location.x <= pos.x <= self.location.x + self.width
            and self.location.y - ytol <= pos.y <= self.location.y + self.height + ytol
            and self.location.z <= pos.z <= self.location.z + self.depth
        )

    def shift(self, arr, vec):
        # this is the fast approach, see 1d Benchmark at
        # https://stackoverflow.com/questions/30399534/shift-elements-in-a-numpy-array
        result: np.ndarray = np.full_like(arr, Item.AIR)  # type: ignore
        if vec.y > 0:
            result[:, : vec.y, :] = Item.AIR
            result[:, vec.y :, :] = arr[:, : -vec.y, :]
        elif vec.y < 0:
            result[:, vec.y :, :] = Item.AIR
            result[:, : vec.y, :] = arr[:, -vec.y :, :]
        if vec.x > 0:
            result[: vec.x, :, :] = Item.AIR
            result[vec.x :, :, :] = arr[: -vec.x, :, :]
        elif vec.x < 0:
            result[vec.x :, :, :] = Item.AIR
            result[: vec.x, :, :] = arr[-vec.x :, :, :]
        if vec.z > 0:
            result[:, :, : vec.z :] = Item.AIR
            result[:, :, vec.z :] = arr[:, :, : -vec.z]
        elif vec.z < 0:
            result[:, :, vec.z :] = Item.AIR
            result[:, :, : vec.z] = arr[:, :, -vec.z :]

        return result


if __name__ == "__main__":
    with Client("localhost", 25901, passwd="spider") as client:
        position = Vec3(36, 26, -90)
        v = Vehicle(client, position, cube=default_vehicle, pause=0.5)

        # asyncio.run(v.render())
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
