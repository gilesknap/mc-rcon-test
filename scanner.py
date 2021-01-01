from mcipc.rcon.je import Client
from vector import vector


class scanner:
    def __init__(self, client: Client, location: vector) -> None:
        self.blocks = {}
        self.edge_blocks = ["air", "grass", "dirt"]
        self.scanblock(location)

    def scanblock(self, location: vector):
        pass
