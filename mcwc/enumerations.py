from enum import Enum


class Planes3d(Enum):
    XY = (0, 1)
    XZ = (0, 2)
    YZ = (1, 2)


class Anchor3(Enum):
    """Anchor point for cuboids."""

    MIDDLE = "middle"
    BOTTOM_MIDDLE = "bottom_middle"
    TOP_MIDDLE = "top_middle"

    BOTTOM_SW = "bottom_sw"
    BOTTOM_NW = "bottom_nw"
    BOTTOM_NE = "bottom_ne"
    BOTTOM_SE = "bottom_se"

    TOP_SW = "top_sw"
    TOP_NW = "top_nw"
    TOP_NE = "top_ne"
    TOP_SE = "top_se"
