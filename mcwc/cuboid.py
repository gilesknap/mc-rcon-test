import asyncio
from time import sleep
from typing import List

import numpy as np
from mcipc.rcon.enumerations import Item
from mcipc.rcon.je import Client
from mcwb import Direction, Vec3

from mcwc.enumerations import Planes3d
from mcwc.functions import shift
from mcwc.helper import Helper
from mcwc.shapes import airplane2
from mcwc.volume import Anchor3, Volume


class Cuboid:
    """
    Represents a cubiod of arbitrary blocks in a minecraft world
    """

    def __init__(
        self,
        client: Client,
        location: Vec3,
        cube: List[List[List[Item]]] = None,
        anchor: Anchor3 = Anchor3.BOTTOM_NW,
        pause: float = 0,
        erase_pause: float = 0.05,
    ) -> None:
        self.helper = Helper(client)

        self.client = client
        self.ncube = np.array(cube, dtype=Item)
        self.anchor = anchor
        self.running = False
        self.pause = pause
        self.erase_pause = erase_pause
        self.location = location
        self._update()

        asyncio.run(self.render())

    def _update(self):
        self.solid = self.ncube != Item.AIR
        self.volume = Volume(self.location, Vec3(*self.ncube.shape), self.anchor)

    async def render(self):
        """ render the cuboid's blocks into Minecraft """
        for idx, block in np.ndenumerate(self.ncube):
            if self.solid[idx]:
                # allow for large items to render without blocking
                await asyncio.sleep(0)
                self.client.setblock(self.volume.start + Vec3(*idx), block)

    async def unrender(self, vector: Vec3, old_start: Vec3) -> None:
        """ clear away exposed blocks from the previous move """
        moved = shift(self.ncube, vector * 1)

        mask = moved == Item.AIR
        mask = mask & (self.ncube != Item.AIR)

        for idx, block in np.ndenumerate(self.ncube):
            if mask[idx]:
                # allow for large items to render without blocking
                await asyncio.sleep(0)
                self.client.setblock(old_start + Vec3(*idx), Item.AIR.value)

    async def rotate(self, plane: Planes3d, steps: int = 1, clear=False):
        """ rotate the blocks in the cuboid in place """
        old_shape = self.ncube.shape
        self.ncube = np.rot90(self.ncube, k=steps, axes=plane.value)

        # TODO implement unrender for rotated cuboid (challenging?)
        if clear:
            Volume(self.volume.start, Vec3(*old_shape), self.anchor).fill(
                self.client
            )
        self._update()
        await self.render()

    def stop(self):
        self.running = False

    async def spin(self, clear: bool = False):
        self.running = True
        while self.running:
            for plane in Planes3d:
                for rot in range(9):
                    await self.rotate(plane.value, clear=clear)
                    await asyncio.sleep(self.pause)

    async def move(self, vector: Vec3):
        old_start = self.volume.start
        self.location += vector
        self._update()

        await self.render()
        # this pause can help avoid a flickering appearance
        await asyncio.sleep(self.erase_pause)

        self.move_players(vector)

        await self.unrender(vector, old_start)
        await asyncio.sleep(self.pause)

    def move_players(self, vector: Vec3):
        players = self.players_in()

        for player in players:
            pos = self.helper.player_pos(player)
            pos += vector

            self.client.teleport(targets=player, location=pos)

    def players_in(self):
        """ return a list of player names whose position is inside the volume"""
        players = []

        names = [p.name for p in self.client.players.players]
        for name in names:
            try:
                pos = self.helper.player_pos(name)
                if self.volume.inside(pos, 2):
                    players.append(name)
            except ValueError:
                pass  # players somtimes are missing temporarily
        return players


# standalone demo of this class
if __name__ == "__main__":
    with Client("localhost", 25901, passwd="spider") as client:
        position = Vec3(0, 5, -40)
        v = Cuboid(client, position, cube=airplane2, pause=0)

        while True:
            while len(v.players_in()) == 0:
                sleep(0.5)

            asyncio.run(v.rotate(Planes3d.XZ, steps=1, clear=True))
            for i in range(40):
                asyncio.run(v.move(Direction.UP.value))
            asyncio.run(v.rotate(Planes3d.XZ, steps=1, clear=True))
            for i in range(80):
                asyncio.run(v.move(Direction.EAST.value))
            asyncio.run(v.rotate(Planes3d.XZ, steps=1, clear=True))
            for i in range(60):
                asyncio.run(v.move(Direction.SOUTH.value))
            asyncio.run(v.rotate(Planes3d.XZ, steps=1, clear=True))
            for i in range(80):
                asyncio.run(v.move(Direction.WEST.value))
            asyncio.run(v.rotate(Planes3d.XZ, steps=1, clear=True))
            for i in range(60):
                asyncio.run(v.move(Direction.NORTH.value))
            asyncio.run(v.rotate(Planes3d.XZ, steps=-1, clear=True))
            for i in range(40):
                asyncio.run(v.move(Direction.DOWN.value))
