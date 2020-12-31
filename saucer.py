from vector import vector
from box import Box
from helper import Helper
from mcipc.rcon.je import Client


class Saucer:
    def __init__(
        self,
        client: Client,
        location: vector,
        size: int = 5,
        material: str = "glass",
    ) -> None:
        self.client = client
        self.material = material
        self.bounds = Box.centered(location, size, 2, size)
        self.helper = Helper(client)
        self.render()

    def render(self):
        self.helper.render_regions(self.bounds.walls(top=False), self.material)

    def _interior(self) -> Box:
        s, e = self.bounds.start, self.bounds.end
        interior = Box(
            vector(s.x + 1, s.y + 1, s.z + 1), vector(e.x - 1, s.y + 1, e.z - 1)
        )
        return interior

    def north(self, z: int) -> None:
        old_bounds = self.bounds
        self.bounds = self.bounds.north(z)
        self.client.clone(
            old_bounds.start,
            old_bounds.end,
            self.bounds.start,
            mask_mode="replace", # TODO these enumerations not working
            clone_mode="move",
        )

        for player in self.helper.players_in(self.bounds):
            pos = self.helper.player_pos(player).north(z)
            self.client.teleport(targets=player, location=pos)  # type: ignore

    def east(self, x: int) -> None:
        if abs(x) > 1:
            raise ValueError("move must be only one block maximum")
        self.bounds.east(x)
        self.render()
