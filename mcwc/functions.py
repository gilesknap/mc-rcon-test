import numpy as np

from mcipc.rcon.enumerations import Item
from mcwb import Vec3


def shift(arr: np.ndarray, vec: Vec3) -> np.ndarray:
    # this is the fast approach, see 1d Benchmark at
    # https://stackoverflow.com/questions/30399534/shift-elements-in-a-numpy-array
    result: np.ndarray = np.array(np.full_like(arr, Item.AIR), dtype=Item)
    if vec.y > 0:
        result[:, : vec.y, :] = Item.AIR
        result[:, vec.y :, :] = arr[:, : -vec.y, :]
    elif vec.y < 0:
        result[:, vec.y :, :] = Item.AIR
        result[:, : vec.y, :] = arr[:, -vec.y :, :]
    if vec.x > 0:
        result[: vec.x, :, :] = Item.AIR
        result[vec.x :, :, :] = arr[: -vec.x, :, :]
    elif vec.x < 0:
        result[vec.x :, :, :] = Item.AIR
        result[: vec.x, :, :] = arr[-vec.x :, :, :]
    if vec.z > 0:
        result[:, :, : vec.z :] = Item.AIR
        result[:, :, vec.z :] = arr[:, :, : -vec.z]
    elif vec.z < 0:
        result[:, :, vec.z :] = Item.AIR
        result[:, :, : vec.z] = arr[:, :, -vec.z :]

    return result
