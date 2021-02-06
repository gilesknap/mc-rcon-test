import asyncio
from datetime import datetime
from pathlib import Path
from typing import cast

from mcipc.rcon.enumerations import FillMode
from mcipc.rcon.item import Item
from mcipc.rcon.je import Client
from mcwb import Anchor, Anchor3, Cuboid, Direction, Profile, Vec3, Volume, mktunnel
from mcwb.itemlists import grab, load_items, save_items

from mcwc.blocks import Blocks

# TODO tidy module exports in __init__
from mcwc.button import Button
from mcwc.enumerations import Planes3d

shapes_folder = Path(__file__).parent / "mcwc" / "shapes"

# my server ports
science = 25701
quest = 25575
flat = 25901


def setup(client):
    # don't announce every rcon command
    client.gamerule("sendCommandFeedback", False)

    # clear an area around the centre
    erase = Volume.from_anchor(
        Vec3(0, 5, 0), Vec3(150, 180, 180), anchor=Anchor3.BOTTOM_MIDDLE
    )
    erase.fill(client)


corners = (
    Anchor3.BOTTOM_NW,
    Anchor3.BOTTOM_SW,
    Anchor3.BOTTOM_NE,
    Anchor3.BOTTOM_SE,
    Anchor3.TOP_NW,
    Anchor3.TOP_SW,
    Anchor3.TOP_NE,
    Anchor3.TOP_SE,
)
items = (
    Item.BLACK_CONCRETE,
    Item.RED_CONCRETE,
    Item.YELLOW_CONCRETE,
    Item.GREEN_CONCRETE,
    Item.BLUE_CONCRETE,
    Item.ORANGE_CONCRETE,
    Item.PINK_CONCRETE,
    Item.PURPLE_CONCRETE,
)


def funky_cube(size: int) -> Cuboid:
    half = int(size / 2)
    size = 2 * half

    left = [Item.RED_CONCRETE] * size
    right = [Item.GREEN_CONCRETE] * size
    row = [Item.BLUE_CONCRETE] + [Item.AIR] * (size - 2) + [Item.YELLOW_CONCRETE]
    square = [left] + [row] * (size - 2) + [right]

    top = [
        [Item.WHITE_CONCRETE, Item.GRAY_CONCRETE] * half,
        [Item.GRAY_CONCRETE, Item.WHITE_CONCRETE] * half,
    ] * half
    bottom = [[Item.BLACK_CONCRETE, Item.GRAY_CONCRETE] * half] * size

    return cast(Cuboid, [top] + [square] * (size - 2) + [bottom])


def test_anchor(client: Client, mid: Vec3):
    def knot(client: Client, mid: Vec3, a: Anchor):
        p: Profile = [
            [Item.RED_CONCRETE, Item.AIR, Item.GREEN_CONCRETE],
            [Item.AIR, Item.AIR, Item.AIR],
            [Item.BLUE_CONCRETE, Item.AIR, Item.YELLOW_CONCRETE],
        ]
        f = FillMode.KEEP
        for d in Direction:
            mktunnel(client, p, mid, direction=d, length=5, mode=f, anchor=a)

    # join at red, green, blue, yellow, middle
    for a in Anchor:
        knot(client, mid, a)
        mid += Direction.EAST.value * 12


# spin a cuboid asynchronously forever
async def spin(cuboid: Blocks, clear: bool = False):
    while True:
        for plane in Planes3d:
            for _ in range(9):
                await cuboid.rotate_a(plane, clear=clear)


def demo():
    with Client("localhost", flat, passwd="spider") as client:
        # callback function for Button activation
        def changed(switch: Button):
            print(f"button {switch.name}, powered:{switch.powered}")
            if switch.id == button2.id and switch.powered:
                lever2_switched_on.set()
                lever2_switched_on.clear()

        # async task dispatcher
        async def runner(*tasks):
            nonlocal lever2_switched_on
            lever2_switched_on = asyncio.Event()
            await asyncio.gather(*tasks)

        # move the vehicle cuboid through a sequence when lever2 is pulled
        async def move_vehicle(cuboid: Blocks):
            seq = [
                (1, Direction.UP, 40),
                (1, Direction.EAST, 30),
                (1, Direction.SOUTH, 60),
                (1, Direction.WEST, 30),
                (1, Direction.NORTH, 60),
                (-1, Direction.DOWN, 40),
            ]
            speed: int = 1
            while True:
                await lever2_switched_on.wait()
                start = datetime.now()
                for rot, dir, dist in seq:
                    await cuboid.rotate_a(Planes3d.XZ, steps=rot, clear=True)
                    for _ in range(dist):
                        await cuboid.move_a(dir.value * speed)
                elapsed = datetime.now() - start
                print(f"the journey took {elapsed}")

        # local for sharing between parties intersted in lever2 events
        lever2_switched_on = None

        setup(client)

        pos = Vec3(-5, 5, -38)
        Button(client, pos, changed)
        pos += Direction.NORTH.value
        button2 = Button(client, pos, changed)
        pos += Direction.NORTH.value
        Button(client, pos, changed, True)

        anchor = Anchor3.BOTTOM_MIDDLE
        pos = Vec3(0, 5, -40)

        plane_json = load_items(shapes_folder / "airplane.json", 3)
        airplane = Blocks(client, pos, plane_json, anchor=anchor, pause=0)

        pos = Vec3(0, 5, 0)
        fun_cube = Blocks(client, pos, funky_cube(30), anchor=anchor, pause=1.0)

        # copy village
        # village_v = Volume(Vec3(146, 3, -325), end=Vec3(264, 15, -434))
        # village = Cuboid.grab(client, village_v)
        # print("village size:", village.volume.size)
        # village.move(Vec3(260, 4, -200), clear=False)

        # make some pretty knots to demo tunnel and anchors
        pos = Vec3(0, 30, -60)
        test_anchor(client, pos)

        # copy all 5 knots down by 12 blocks
        # do it using files to prove save and load
        for x in range(5):
            knot_vol = Volume.from_anchor(pos, Vec3(11, 11, 11), Anchor3.MIDDLE)
            knot_cuboid = grab(client, knot_vol)
            save_items(knot_cuboid, Path("/tmp") / f"knot{x}.json")

            knot_cuboid_read = load_items(Path("/tmp") / f"knot{x}.json")
            knot_blocks = Blocks(
                client, knot_vol.position, knot_cuboid_read, anchor=Anchor3.MIDDLE
            )
            knot_blocks.pause = 2
            knot_blocks.move(Vec3(0, -12, 0), clear=False)

            pos += Vec3(12, 0, 0)

        for t, (anchor, item) in enumerate(zip(corners, items)):
            v = Volume.from_anchor(Vec3(0, 30, 60), Vec3(20, 20, 20), anchor=anchor)
            v.walls(client, item, thickness=t + 1)

        # TODO create a McTask base class which packages up all async stuff
        tasks = [
            spin(fun_cube),
            spin(knot_blocks),  # type: ignore
            move_vehicle(airplane),
            Button.monitor(client),
        ]

        asyncio.run(runner(*tasks))


if __name__ == "__main__":
    demo()
