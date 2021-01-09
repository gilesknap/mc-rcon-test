import asyncio
from typing import Callable, List

from mcipc.rcon.enumerations import Item, SetblockMode
from mcipc.rcon.je import Client
from mcwb import Vec3


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
        callback: Callable[["Button"], None] = None,
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

        # TODO pass values for orientation to the constructor
        fullitem = item + self.data_values.format("floor", "north", "false")
        # TODO update Item to a class that can hold and render data values
        client.setblock(location, fullitem, mode=SetblockMode.REPLACE)

    def remove(self):
        self.buttons.remove(self)
        self.client.setblock(self.location, Item.AIR.value, mode=SetblockMode.REPLACE)

    @classmethod
    def stop(cls):
        cls.monitoring = False

    @classmethod
    def check_state(cls, client: Client, location: Vec3, state: str) -> bool:
        res = client.execute.if_.block(location, state).run("seed")
        if "Seed" in res:
            result = True
        elif res == "":
            result = False
        else:
            raise RuntimeError(res)

        return result

    @classmethod
    async def monitor(cls, client: Client):
        cls.monitoring = True
        while cls.monitoring:
            await asyncio.sleep(0.1)
            for button in cls.buttons:
                if button.powered:
                    if cls.check_state(client, button.location, button.off):
                        button.powered = False
                        if button.callback:
                            button.callback(button)
                else:
                    if cls.check_state(client, button.location, button.on):
                        button.powered = True
                        if button.callback:
                            button.callback(button)
