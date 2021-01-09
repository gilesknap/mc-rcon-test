import asyncio

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


def knot(client: Client, mid: Vec3, a: Anchor):
    p: Profile = [
        [Item.RED_CONCRETE, Item.AIR, Item.GREEN_CONCRETE],
        [Item.AIR, Item.AIR, Item.AIR],
        [Item.BLUE_CONCRETE, Item.AIR, Item.YELLOW_CONCRETE],
    ]
    f = FillMode.KEEP
    mktunnel(client, p, mid, direction=Direction.NORTH, length=5, mode=f, anchor=a)
    mktunnel(client, p, mid, direction=Direction.SOUTH, length=5, mode=f, anchor=a)
    mktunnel(client, p, mid, direction=Direction.EAST, length=5, mode=f, anchor=a)
    mktunnel(client, p, mid, direction=Direction.WEST, length=5, mode=f, anchor=a)
    mktunnel(client, p, mid, direction=Direction.UP, length=5, mode=f, anchor=a)
    mktunnel(client, p, mid, direction=Direction.DOWN, length=5, mode=f, anchor=a)


def test_anchor(client: Client, mid: Vec3):
    knot(client, mid, Anchor.TOP_LEFT)  # join at RED
    mid += Direction.EAST.value * 12
    knot(client, mid, Anchor.TOP_RIGHT)  # join at GREEN
    mid += Direction.EAST.value * 12
    knot(client, mid, Anchor.BOTTOM_LEFT)  # join at BLUE
    mid += Direction.EAST.value * 12
    knot(client, mid, Anchor.BOTTOM_RIGHT)  # join at YELLOW
    mid += Direction.EAST.value * 12
    knot(client, mid, Anchor.MIDDLE)  # join in middle


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
            if switch.id == lever1.id and switch.powered:
                lever2_switched_on.set()
                lever2_switched_on.clear()

        # async task dispatcher
        async def runner(*tasks):
            nonlocal lever2_switched_on
            lever2_switched_on = asyncio.Event()
            await asyncio.gather(*tasks)

        # move the vehicle cuboid through a sequence when lever2 is pulled
        async def move_vehicle(cuboid: Cuboid):
            while True:
                await lever2_switched_on.wait()
                seq = [
                    (1, Direction.UP, 40),
                    (1, Direction.EAST, 80),
                    (1, Direction.SOUTH, 60),
                    (1, Direction.WEST, 80),
                    (1, Direction.NORTH, 60),
                    (-1, Direction.DOWN, 40),
                ]
                for rot, dir, dist in seq:
                    await cuboid.rotate_a(Planes3d.XZ, steps=rot, clear=True)
                    for _ in range(dist):
                        await cuboid.move_a(dir.value)

        # local for sharing between parties intersted in lever2 events
        lever2_switched_on = None

        setup(client)

        pos = Vec3(-5, 5, -38)
        Button(client, pos, changed)
        pos += Direction.NORTH.value
        lever1 = Button(client, pos, changed, True)
        pos += Direction.NORTH.value
        Button(client, pos, changed, True)

        anchor = Anchor3.BOTTOM_MIDDLE
        pos = Vec3(0, 5, -40)
        vehicle = Cuboid(client, pos, cube=airplane2, pause=0, anchor=anchor)

        pos = Vec3(0, 5, 0)
        anchor = Anchor3.BOTTOM_SE
        fun_cube = Cuboid(client, pos, funky_cube(20), anchor=anchor, pause=1.0)

        # middle of last knot from test_anchor
        pos = Vec3(48, 30, -60)
        knot = Volume(pos, Vec3(11, 11, 11), Anchor3.MIDDLE)
        knot_cube = Cuboid.grab(client, knot)
        knot_cube.pause = 30
        knot_cube.move(Vec3(0, -15, 0), clear=False)
        # TODO create a McTask base class which packages up all async stuff
        tasks = [
            spin(fun_cube, clear=False),
            spin(knot_cube),
            move_vehicle(vehicle),
            Button.monitor(client),
        ]

        asyncio.run(runner(*tasks))


if __name__ == "__main__":
    demo()
