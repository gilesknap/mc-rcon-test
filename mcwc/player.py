import re

from mcipc.rcon.enumerations import Item
from mcipc.rcon.je import Client
from mcwb import Vec3

from mcwc.volume import Volume

regex_coord = re.compile(r"\[(-?\d+.?\d*)d, *(-?\d+.?\d*)d, *(-?\d+.?\d*)d\]")


class Player:
    def __init__(
        self,
        client: Client,
        name: str
    ) -> None:
        self.client = client
        self.running = False
        self.name = name

    def give_stop(self):
        nbt = (
            """{BlockEntityTag:{Text1:'{"text":"STOP Python"}', """
            """Command:'{"test":"1"}'},display:{Name:'{"text":"STOP"}'}}"""
        )
        print(self.client.give(self.name, Item.BIRCH_SIGN.value+nbt))

    @classmethod
    def player_pos(cls, client: Client, player_name: str) -> Vec3:
        data = client.data.get(entity=player_name, path="Pos")
        match = regex_coord.search(data)
        if match:
            result = Vec3(
                float(match.group(1)), float(match.group(2)), float(match.group(3))
            )
            return result
        else:
            raise ValueError(f"player {player_name} does not exist")

    @classmethod
    def players_in(cls, client: Client, volume: Volume):
        """ return a list of player names whose position is inside the volume"""
        players = []

        names = [p.name for p in client.players.players]
        for name in names:
            try:
                pos = cls.player_pos(client, name)
                if volume.inside(pos, 2):
                    players.append(name)
            except ValueError:
                pass  # players are sometimes missing temporarily
        return players
