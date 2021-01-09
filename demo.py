import asyncio
from datetime import datetime

from mcipc.rcon.enumerations import FillMode
from mcipc.rcon.item import Item
from mcipc.rcon.je import Client
from mcwb import Anchor, Direction, Profile, Vec3, mktunnel

# TODO tidy module exports in __init__
from mcwc.button import Button
from mcwc.cuboid import Cuboid
from mcwc.enumerations import Planes3d
from mcwc.shapes import airplane2, funky_cube
from mcwc.volume import Anchor3, Volume

# my server ports
science = 25701
quest = 25575
flat = 25901


def setup(client):
    # don't announce every rcon command
    client.gamerule("sendCommandFeedback", False)

    # clear an area around the centre
    erase = Volume(Vec3(0, 5, 0), Vec3(150, 150, 150), anchor=Anchor3.BOTTOM_MIDDLE)
    erase.fill(client)

    # make some pretty knots to demo tunnel and anchors
    test_anchor(client, Vec3(0, 30, -60))


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
async def spin(cuboid: Cuboid, clear: bool = True):
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
        async def move_vehicle(cuboid: Cuboid):
            seq = [
                (1, Direction.UP, 40),
                (1, Direction.EAST, 30),
                (1, Direction.SOUTH, 60),
                (1, Direction.WEST, 30),
                (1, Direction.NORTH, 60),
                (-1, Direction.DOWN, 40),
            ]
            while True:
                await lever2_switched_on.wait()
                start = datetime.now()
                for rot, dir, dist in seq:
                    await cuboid.rotate_a(Planes3d.XZ, steps=rot, clear=True)
                    for _ in range(dist):
                        await cuboid.move_a(dir.value)
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
        vehicle = Cuboid(client, pos, cube=airplane2, anchor=anchor, pause=0)

        pos = Vec3(0, 5, 0)
        fun_cube = Cuboid(client, pos, funky_cube(30), anchor=anchor, pause=1.0)

        # middle of first knot from test_anchor
        pos = Vec3(0, 30, -60)
        # copy all 5 knots down by 12 blocks
        for x in range(5):
            knot = Volume(pos, Vec3(11, 11, 11), Anchor3.MIDDLE)
            knot_cube = Cuboid.grab(client, knot)
            knot_cube.pause = 2
            knot_cube.move(Vec3(0, -12, 0), clear=False)
            pos += Vec3(12, 0, 0)

        # TODO create a McTask base class which packages up all async stuff
        tasks = [
            spin(fun_cube, clear=False),
            spin(knot_cube, clear=False),  # type: ignore
            move_vehicle(vehicle),
            Button.monitor(client),
        ]

        asyncio.run(runner(*tasks))


if __name__ == "__main__":
    demo()
