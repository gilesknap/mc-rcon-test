from typing import Callable, List
from mcipc.rcon.builder import Vec3, Item
from mcipc.rcon.enumerations import SetblockMode
from mcipc.rcon.je import Client
import asyncio


class Button:
    buttons: List["Button"] = []
    button_id: int = 0
    button_item = Item.ACACIA_BUTTON.value
    lever_item = Item.LEVER.value
    data_values = "[face={}, facing={}, powered={}]"
    monitoring = False

    def __init__(
        self,
        client: Client,
        location: Vec3,
        callback: Callable[[bool, str, int], None] = None,
        is_lever: bool = False,
        name: str = "",
    ) -> None:
        self.client = client
        self.location = location
        self.callback = callback
        Button.buttons.append(self)
        Button.button_id += 1
        self.powered = False

        if is_lever:
            item = Button.lever_item
            self.name = name if name else f"lever{Button.button_id}"
        else:
            item = Button.button_item
            self.name = name if name else f"button{Button.button_id}"
        self.id = Button.button_id

        self.on = item + "[powered=true]"
        self.off = item + "[powered=false]"

        fullitem = item + self.data_values.format("floor", "north", "false")
        client.setblock(location, fullitem, mode=SetblockMode.REPLACE)

    def remove(self):
        self.buttons.remove(self)
        self.client.setblock(self.location, Item.AIR.value, mode=SetblockMode.REPLACE)

    @classmethod
    async def monitor(cls, client: Client):
        cls.monitoring = True
        while cls.monitoring:
            await asyncio.sleep(0.1)
            for b in cls.buttons:
                if b.powered:
                    if client.execute.if_.block(b.location, b.off).run("seed"):
                        b.powered = False
                        if b.callback:
                            b.callback(False, b.name, b.id)
                else:
                    if client.execute.if_.block(b.location, b.on).run("seed"):
                        b.powered = True
                        if b.callback:
                            b.callback(True, b.name, b.id)
