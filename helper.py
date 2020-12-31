from typing import List
from box import Box, Regions
from mcipc.rcon.je import Client
from mcipc.rcon.types import FillMode, TargetType
from vector import vector
import re

# Minecraft Coordinate System
# plus Y is up
# plus X is East
# plus Z is South

# extract the integer coords from a string of the form
#  "DispenserAD11 has the following entity data: \
#   [-2984.3695730161085d, 87.16610926093821d, 54.42824875967167d]"

regex_coord = re.compile(r"\[(-?\d+).?\d*d, *(-?\d+).?\d*d, *(-?\d+).?\d*d\]")


class Helper:
    def __init__(self, client: Client) -> None:
        self.client = client

    def player_pos(self, player_name: str) -> vector:
        data = self.client.data.get(TargetType.ENTITY, player_name, "Pos")
        match = regex_coord.search(data)
        if match:
            result = vector(
                int(match.group(1)), int(match.group(2)), int(match.group(3))
            )
            return result
        else:
            raise ValueError(f"player {player_name} does not exist")

    def players_in(self, region: Box) -> List[str]:
        # return a list of player names found within a region
        result = []

        names = [p.name for p in self.client.players.players]
        for name in names:
            pos = self.player_pos(name)
            if region.inside(pos):
                result.append(name)

        return result

    def render_regions(self, regions: Regions, material: str):
        for box in regions:
            self.client.fill(box.start, box.end, material, FillMode.REPLACE)  # type: ignore