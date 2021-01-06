from typing import List
from mcipc.rcon.builder import Vec3
from mcipc.rcon.builder import Anchor, Direction, mktunnel
from mcipc.rcon.builder.item import Item
from mcipc.rcon.builder.types import Profile
from box import Box, Regions
from mcipc.rcon.je import Client
from mcipc.rcon import TargetType
import re

# Minecraft Coordinate System
# plus Y is up
# plus X is East
# plus Z is South

# extract the double coords from a string of the form
#  "DispenserAD11 has the following entity data: \
#   [-2984.3695730161085d, 87.16610926093821d, 54.42824875967167d]"

regex_coord = re.compile(r"\[(-?\d+.?\d*)d, *(-?\d+.?\d*)d, *(-?\d+.?\d*)d\]")


class Helper:
    def __init__(self, client: Client) -> None:
        self.client = client

    def player_pos(self, player_name: str) -> Vec3:
        data = self.client.data.get(TargetType.ENTITY, player_name, "Pos")
        match = regex_coord.search(data)
        if match:
            result = Vec3(
                float(match.group(1)), float(match.group(2)), float(match.group(3))
            )
            return result
        else:
            raise ValueError(f"player {player_name} does not exist")

    def players_in(self, region: Box, ytol: int = 0) -> List[str]:
        # return a list of player names found within a region
        players = []

        names = [p.name for p in self.client.players.players]
        for name in names:
            try:
                pos = self.player_pos(name)
                if region.inside(pos, ytol):
                    players.append(name)
            except ValueError:
                pass  # players somtimes are missing temporarily
        return players

    def render_regions(self, regions: Regions, material: str):
        for box in regions:
            self.client.fill(box.start, box.end, material)

    def clear_blocks(self, mid: Vec3, size: int):
        clear: Profile = [[Item.AIR] * size] * size
        mktunnel(
            self.client,
            clear,
            mid,
            direction=Direction.UP,
            length=size,
            anchor=Anchor.MIDDLE,
        )
