import asyncio
from typing import Any

import numpy as np
from mcipc.rcon.enumerations import Item
from mcipc.rcon.je import Client
from mcwb import Vec3

from mcwc.enumerations import Anchor3, Planes3d
from mcwc.functions import shift
from mcwc.itemlists import Cuboid
from mcwc.player import Player
from mcwc.volume import Volume


class Blocks:
    """
    Represents a cubiod of arbitrary blocks in a minecraft world with functions
    for manipulating those blocks
    """

    def __init__(
        self,
        client: Client,
        position: Vec3,
        cube: Cuboid = None,
        ncube: Any = None,
        anchor: Anchor3 = Anchor3.BOTTOM_NW,
        do_teleport: bool = True,
        pause: float = 0,
        erase_pause: float = 0.3,
        render: bool = True,
    ) -> None:
        self._client = client
        self.anchor = anchor
        self.ncube = ncube if ncube is not None else np.array(cube, dtype=Item)

        self.volume = Volume(position, Vec3(*self.ncube.shape), self.anchor)
        self._solid: Any = self.ncube != Item.AIR

        self.do_teleport = do_teleport
        self.pause = pause
        self.erase_pause = erase_pause

        if render:
            asyncio.run(self._render())

    def move(self, vector: Vec3, clear: bool = True) -> None:
        """ sychronous move """
        asyncio.run(self.move_a(vector, clear))

    def rotate(self, plane: Planes3d, steps: int = 1, clear=True) -> None:
        """ synchronous rotate """
        asyncio.run(self.rotate_a(plane, steps, clear))

    async def _render(self) -> None:
        """ render the cuboid's blocks into Minecraft """
        for idx, block in np.ndenumerate(self.ncube):
            if self._solid[idx]:
                # allow for large items to render without blocking
                await asyncio.sleep(0)
                self._client.setblock(self.volume.start + Vec3(*idx), block)

    async def _unrender(self, vector: Vec3, old_start: Vec3) -> None:
        """ clear away exposed blocks from the previous move """
        moved = shift(self.ncube, vector * 1)

        mask: Any = (moved == Item.AIR) & (self.ncube != Item.AIR)

        for idx, block in np.ndenumerate(self.ncube):
            if mask[idx]:
                # allow for large items to unrender without blocking
                await asyncio.sleep(0)
                self._client.setblock(old_start + Vec3(*idx), Item.AIR.value)

    async def rotate_a(self, plane: Planes3d, steps: int = 1, clear=True) -> None:
        """ rotate the blocks in the cuboid in place """
        self.ncube = np.rot90(self.ncube, k=steps, axes=plane.value)

        if clear:  # TODO implement unrender for rotated cuboid (challenging?)
            self.volume.fill(self._client)

        self._solid = self.ncube != Item.AIR
        self.volume = Volume(self.volume.position, Vec3(*self.ncube.shape), self.anchor)

        await self._render()
        await asyncio.sleep(self.pause)

    async def move_a(self, vector: Vec3, clear: bool = True) -> None:
        """ moves the cubiod in the world and redraws it """
        old_start = self.volume.start
        self.volume = Volume(
            self.volume.position + vector, Vec3(*self.ncube.shape), self.anchor
        )

        await self._render()
        self.move_players(vector)

        if clear:
            # this pause can help avoid a flickering appearance
            await asyncio.sleep(self.erase_pause)
            await self._unrender(vector, old_start)
            await asyncio.sleep(self.pause)

    async def glide(self, new_position: Vec3):
        """ asynchronously move to new location with self.pause secs between steps"""
        #  TODO

    def move_players(self, distance: Vec3) -> None:
        """ moves any players within the cuboid by distance """
        if self.do_teleport:
            players = Player.players_in(self._client, self.volume)

            for player in players:
                pos = Player.player_pos(self._client, player)
                pos += distance

                self._client.teleport(targets=player, location=pos)
