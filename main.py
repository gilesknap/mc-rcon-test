from mcipc.rcon import Client
from mcipc.rcon.types import FillMode, Vec3
from time import sleep

with Client("86.18.193.64", 25711, passwd="spiderMashTimewarp") as client:
    start = Vec3(-14112, 99, 4100)

    print(client.players)

    client.tell("@a", "Hello - testing testing")

    end = Vec3(int(start.x) + 10, int(start.y) + 10, start.z)
    for i in range(10):
        client.fill(start, end, "iron_block", FillMode.REPLACE)
        sleep(1)
        client.fill(start, end, "air", FillMode.REPLACE)
        sleep(1)

