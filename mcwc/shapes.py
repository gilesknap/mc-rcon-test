from typing import List
from mcipc.rcon.enumerations import Item


def funky_cube(size: int):
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

    return [top] + [square] * (size - 2) + [bottom]


test_cube: List[List[List[Item]]] = [
    [
        [
            Item.GREEN_CONCRETE,
            Item.AIR,
        ],
        [
            Item.AIR,
            Item.GREEN_CONCRETE,
        ],
    ],
    [
        [
            Item.GREEN_CONCRETE,
            Item.GREEN_CONCRETE,
        ],
        [
            Item.GREEN_CONCRETE,
            Item.GREEN_CONCRETE,
        ],
    ],
]


vehicle: List[List[List[Item]]] = [
    [
        [
            Item.GREEN_CONCRETE,
            Item.GREEN_CONCRETE,
            Item.GREEN_CONCRETE,
            Item.GREEN_CONCRETE,
            Item.GREEN_CONCRETE,
        ],
        [
            Item.GREEN_CONCRETE,
            Item.GREEN_CONCRETE,
            Item.GREEN_CONCRETE,
            Item.GREEN_CONCRETE,
            Item.GREEN_CONCRETE,
        ],
        [Item.AIR, Item.AIR, Item.ACACIA_BUTTON, Item.AIR, Item.AIR],
        [Item.AIR, Item.AIR, Item.AIR, Item.AIR, Item.AIR],
    ],
    [
        [
            Item.GREEN_CONCRETE,
            Item.GREEN_CONCRETE,
            Item.GREEN_CONCRETE,
            Item.GREEN_CONCRETE,
            Item.GREEN_CONCRETE,
        ],
        [Item.GREEN_CONCRETE, Item.AIR, Item.AIR, Item.AIR, Item.GREEN_CONCRETE],
        [Item.AIR, Item.AIR, Item.AIR, Item.AIR, Item.AIR],
        [Item.AIR, Item.AIR, Item.AIR, Item.AIR, Item.AIR],
    ],
    [
        [
            Item.GREEN_CONCRETE,
            Item.GREEN_CONCRETE,
            Item.GREEN_CONCRETE,
            Item.GREEN_CONCRETE,
            Item.GREEN_CONCRETE,
        ],
        [Item.GREEN_CONCRETE, Item.AIR, Item.AIR, Item.AIR, Item.GREEN_CONCRETE],
        [Item.ACACIA_BUTTON, Item.AIR, Item.AIR, Item.AIR, Item.ACACIA_BUTTON],
        [Item.AIR, Item.AIR, Item.AIR, Item.AIR, Item.AIR],
    ],
    [
        [
            Item.GREEN_CONCRETE,
            Item.GREEN_CONCRETE,
            Item.GREEN_CONCRETE,
            Item.GREEN_CONCRETE,
            Item.GREEN_CONCRETE,
        ],
        [Item.GREEN_CONCRETE, Item.AIR, Item.AIR, Item.AIR, Item.GREEN_CONCRETE],
        [Item.GREEN_CONCRETE, Item.AIR, Item.AIR, Item.AIR, Item.GREEN_CONCRETE],
        [Item.AIR, Item.AIR, Item.AIR, Item.AIR, Item.AIR],
    ],
    [
        [
            Item.GREEN_CONCRETE,
            Item.GREEN_CONCRETE,
            Item.GREEN_CONCRETE,
            Item.GREEN_CONCRETE,
            Item.GREEN_CONCRETE,
        ],
        [
            Item.GREEN_CONCRETE,
            Item.GREEN_CONCRETE,
            Item.GREEN_CONCRETE,
            Item.GREEN_CONCRETE,
            Item.GREEN_CONCRETE,
        ],
        [Item.GREEN_CONCRETE, Item.AIR, Item.AIR, Item.AIR, Item.GREEN_CONCRETE],
        [Item.GREEN_CONCRETE, Item.AIR, Item.AIR, Item.AIR, Item.GREEN_CONCRETE],
    ],
]