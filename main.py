from mcipc.rcon.je import Client
from mcipc.rcon.types import FillMode, TargetType, Vec3
from time import sleep


with Client("localhost", 25701, passwd="spider") as client:
    data = client.data.get(TargetType.ENTITY, "@p", "Pos")

    print(f"data: {data}")

    res = client.run(
        "execute unless block -14116 98 4094 #minecraft:acacia_logs run say yes"
    )
    print(f"result {res}")

    print(client.players)

    # don't announce every rcon command
    res = client.gamerule("sendCommandFeedback", False)
    print(f"result {res}")


    # send a message to ALL players
    res = client.tell("@a", "Hello - testing testing")
    print(f"result {res}")

    # materialize a flashing wall
    start = Vec3(-14112, 99, 4100)
    end = Vec3(int(start.x) + 10, int(start.y) + 10, start.z)
    for i in range(1):
        res = client.fill(start, end, "iron_block", FillMode.REPLACE)
        print(f"result {res}")
        sleep(1)
        client.fill(start, end, "air", FillMode.REPLACE)
        sleep(1)

    res = client.run("say hello world")
    print(f"result {res}")

