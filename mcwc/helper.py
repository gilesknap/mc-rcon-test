from typing import List
from mcipc.rcon.enumerations import Item
from mcwb import Vec3, Direction, mktunnel, Profile, Anchor, Anchor3
from mcwc.box import Box, Regions
from mcipc.rcon.je import Client
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
        data = self.client.data.get(entity=player_name, path="Pos")
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

    def fill_blocks(
        self,
        start: Vec3,
        size: Vec3,
        anchor: Anchor3 = Anchor3.BOTTOM_SE,
        block: Item = Item.AIR,
    ):
        """
        fills a 3d region of size from a start point
        """
        if anchor == Anchor3.BOTTOM_SE:
            # size from here is already correct - other clauses are moving
            # start to SE corner from the given corner
            pass
        elif anchor == Anchor3.BOTTOM_MIDDLE:
            start -= Vec3(1, 0, 1) * (size / 2).to_int()
        elif anchor == Anchor3.BOTTOM_NW:
            start += Vec3(0, 0, size.z)
        else:
            # TODO support others
            raise ValueError("unsupported anchor")

        # invert z so that posiitve size is positive North
        size = size * Vec3(1, 1, -1) - 1
        print(self.client.fill(start, start + size, Item.AIR.value))
