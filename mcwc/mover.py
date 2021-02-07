""" asynchronous motion """
from mcwb.types import Vec3

from mcwc.blocks import Blocks
from mcwc.enumerations import Planes3d
from mcwc.player import Player


class Mover:
    """ aynchronous motion of objects with synchronous move/rotate """

    def __init__(
        self,
        blocks: Blocks,
        do_teleport: bool = True,
        pause: float = 0,
        erase_pause: float = 0.3,
    ) -> None:
        self.blocks = blocks
        self.do_teleport = do_teleport
        self.pause = pause
        self.erase_pause = erase_pause

    def move(self, vector: Vec3, clear: bool = True) -> None:
        """ sychronous move """
        self.blocks.move(vector, clear)

    def rotate(self, plane: Planes3d, steps: int = 1, clear=True) -> None:
        """ synchronous rotate """
        self.blocks.rotate(plane, steps, clear)

    async def glide(self, new_position: Vec3):
        """ asynchronously move to new location with self.pause secs between steps"""
        #  TODO

    def move_players(self, distance: Vec3) -> None:
        """ moves any players within the cuboid by distance """
        if self.do_teleport:
            players = Player.players_in(self.blocks._client, self.blocks.volume)

            for player in players:
                pos = Player.player_pos(self.blocks._client, player)
                pos += distance

                self.blocks._client.teleport(targets=player, location=pos)
