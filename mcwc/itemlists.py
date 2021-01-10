"""
Functions for manipulating lists of Items
    2d = Profile
    3d = Cuboid
"""

import codecs
import json
import re
from pathlib import Path
from typing import List, Union, cast

import numpy as np
from mcipc.rcon.enumerations import Item
from mcipc.rcon.je import Client
from mcwb import Profile, Row, Vec3
from mcwb.functions import validate

from mcwc.volume import Volume

Cuboid = List[Profile]
Items = Union[Cuboid, Profile, Row]


def validate_cuboid(cuboid: Cuboid):
    ncube = np.array(cuboid)
    if ncube.ndim != 3:
        raise ValueError("wrong dimensions for cuboid")

    xdim = len(ncube[:, 0, 0])
    ydim = len(ncube[0, :, 0])
    zdim = len(ncube[0, 0, :])

    return xdim * ydim * zdim == ncube.size


def save(items: Items, filename: Path) -> None:
    """ save a Profile or Cuboid (or Row) to a json file """

    def json_item(item: Item):
        return {"__Item__": item.value}

    json.dump(
        items,
        codecs.open(str(filename), "w", encoding="utf-8"),
        separators=(",", ":"),
        sort_keys=True,
        indent=4,
        default=json_item,
    )


def load_cuboid(filename: Union[Path, str]):
    """ load a cuboid from a json file """
    cuboid = cast(Cuboid, load(filename))
    if not validate_cuboid(cuboid):
        raise ValueError(f"file {filename} does not contain a cuboid")
    return cuboid


def load_profile(filename: Union[Path, str]) -> Profile:
    """ load a profile from a json file """
    profile = cast(Profile, load(filename))
    if not validate(profile):
        raise ValueError(f"file {filename} does not contain a profile")
    return profile


def load(filename: Union[Path, str]) -> Items:
    """ load a nested list of Item from json file """

    def as_item(d):
        if "__Item__" in d:
            return Item(d["__Item__"])
        else:
            return d

    """ load a previously saved json file - returns a Cuboid or Profile or Row"""
    result = json.load(
        codecs.open(str(filename), "r", encoding="utf-8"), object_hook=as_item
    )
    return result


dump = Vec3(0, 0, 0)
extract_item = re.compile(r".*minecraft\:(?:blocks\/)?(.+)$")


def grab(client: Client, vol: Volume) -> Cuboid:
    """ copy blocks from a Volume in the minecraft world to create a cuboid of items"""
    ncube = np.ndarray(vol.size, dtype=Item)

    for idx, _ in np.ndenumerate(ncube):
        output = client.loot.spawn(dump).mine(vol.start + Vec3(*idx))
        match = extract_item.search(output)
        if not match:
            raise ValueError(f"loot spawn returned: {output}")
        name = match.group(1)
        if name == "empty":
            name = "air"
        ncube[idx] = Item(name)

    result = ncube.tolist()
    return result
