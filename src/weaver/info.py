"""
This module contains helper functions to get information for n.
This was once a graph class with adjacency lists etc.,
but has now been reduced to these functions to reduce memory use.
So technically, this is a graph info class.

The module provides the following functions:

- get_z_color_size(n: int) -> ZInfo:
    Get z-scalar value, color, and size for each negative level from -radius to -1.
- get_order_from_radius(radius: int) -> int:
    Get the order from the given radius of a Manhattan ball.
- get_order_from_n(n: int) -> int:
    Get the number of vertices of an n-layer of cubes with the core included.
- get_radius_from_n(n: int) -> int:
    Get the radius for a given number of layers around a central cube.
- get_n_from_radius(radius: int) -> int:
    Get n from radius where the edge-length is 2 units.
"""

from itertools import repeat

from src.weaver.types import ZInfo


def get_z_color_size(n_level: int) -> ZInfo:
    """Get z-scalar value, color and size for each negative level from -radius to -1

    Args:
        n (int): number of layers around a central core with the core included.

    Returns:
        An iterator for z-level, its color and size
    """
    return zip(
        # Odd numbers from -radius to -1: radius for each level:
        range(-(n_level * 2 - 1), 0, 2),
        # Number to access the right yarn for each level:
        # interleave(*((repeat(1), repeat(3)) if not n % 2 else (repeat(3), repeat(1)))),
        [
            n
            for nest in repeat(((1, 3) if not n_level % 2 else (3, 1)), n_level)
            for n in nest
        ],
        # Order for each level:
        map(lambda f: 2 * f * (f + 1), range(1, n_level + 1)),
    )


def get_order_from_radius(radius: int) -> int:
    """Get Order from radius

    Args:
        radius (int): Radius of manhattan ball.

    Returns:
        int: Order from radius.
    """
    # convert radius to n and then get order from radius.
    return get_order_from_n(get_n_from_radius(radius))


def get_n_from_radius(radius: int) -> int:
    """Get n from radius where the edge-length is 2 units.

    Args:
        radius (int): max-scalar value of x, y, or z of all the vertices.

    Returns:
        int: Number of layers in the manhattan cube.
    """
    return (radius + 1) // 2


def get_order_from_n(n_level: int) -> int:
    """get the number of vertices of n layer of cubes with core included.

    Args:
        n (int): number of layers around a central core with the core included.

    Returns:
        int: Uncentered Octahedral Number or the number of vertices at the corners of all cubes.
    """
    return (4 * (n_level + 2) * (n_level + 1) * n_level) // 3


def get_radius_from_n(n_level: int) -> int:
    """Radius is n * edge-length of 2 - 1

    Args:
        n (int): Number of layers around a central cube including the cube.

    Returns:
        int: The location of the furthest vert if the edge-length is 2.
    """
    return n_level * 2 - 1
