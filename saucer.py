from typing import NamedTuple

from mcwb import Vec3, Direction
from box import Box
from helper import Helper
from mcipc.rcon.je import Client
from mcipc.rcon import MaskMode, CloneMode
import asyncio


class x(NamedTuple):
    x: int
    y: int


t = x(1, 1)


class Saucer:
    def __init__(
        self,
        client: Client,
        location: Vec3,
        size: int = 5,
        height: int = 2,
        material: str = "glass",
    ) -> None:
        self.client = client
        self.material = material
        self.bounds = Box.centered(location, size, height, size)
        self.helper = Helper(client)
        self.running = False
        self.render()

    def render(self):
        self.helper.render_regions(self.bounds.walls(top=False), self.material)

    def _interior(self) -> Box:
        s, e = self.bounds.start, self.bounds.end
        interior = Box(
            Vec3(s.x + 1, s.y + 1, s.z + 1), Vec3(e.x - 1, s.y + 1, e.z - 1)
        )
        return interior

    def north(self, z: int, pause: float = 0.3) -> None:
        old_bounds = self.bounds
        self.bounds = self.bounds.north(z)
        self.client.clone(
            old_bounds.start,
            old_bounds.end,
            self.bounds.start,
            mask_mode=MaskMode.REPLACE,
            clone_mode=CloneMode.MOVE,
        )

        for player in self.helper.players_in(self.bounds, ytol=2):
            pos = self.helper.player_pos(player)
            pos += Direction.NORTH.value * z

            self.client.teleport(targets=player, location=pos)

    def east(self, x: int) -> None:
        if abs(x) > 1:
            raise ValueError("move must be only one block maximum")
        self.bounds.east(x)
        self.render()

    async def run(self) -> None:
        self.running = True
        while self.running:
            while not self.helper.players_in(self.bounds, ytol=2):
                await asyncio.sleep(0.1)
            for z in range(100):
                self.north(1)
                await asyncio.sleep(0.2)
            for x in range(500):
                self.east(1)
                await asyncio.sleep(0.2)
            for x in range(500):
                self.north(-1)
                await asyncio.sleep(0.2)
            for x in range(600):
                self.east(-1)
                await asyncio.sleep(0.2)
            for z in range(600):
                self.north(1)
                await asyncio.sleep(0.2)
            for x in range(100):
                self.east(1)
                await asyncio.sleep(0.2)
            for z in range(100):
                self.north(-1)
                await asyncio.sleep(0.2)

    def stop(self) -> None:
        self.running = False
