from mcipc.rcon.enumerations import Item
# from mcwb import Vec3, Direction
# from helper import Helper
from mcipc.rcon.je import Client
# import asyncio


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