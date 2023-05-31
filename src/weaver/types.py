"""
This module provides types for weaving a Hamiltonian Cycle of a Manhattan Ball.

Types:
- XYVects: A list containing two zig-zag displacement XY vectors
- Point: A tuple of three integers representing a point in 3D space.
- Edge: A tuple of two points representing an edge in 3D space.
- Edges: A set of edges.
- Loom: A list of threads representing a weaving loom.
- ZInfo: An iterator providing info about the z-coordinate,
    yarn color and size of each level.
- Solution: A list of points representing the Hamiltonian Cycle.
- Spool: A dictionary mapping colors to lists of zigzag vectors.
- Spun: A list of lists representing spun yarn.
- Tour: A list of points representing a tour.
- Subtours: A list of tours representing subtours.
- Pins: A set of points representing pins used for cutting yarn.
- UonGen: A generator of integers.
- Unpacker: An iterator of integers.
- ZigZags: A list of XYVects representing zigzag vectors.

"""

from typing import (
    Deque,
    Dict,
    Generator,
    Iterator,
    List,
    Set,
    Tuple,
    Union,
)


# A list containing two zig-zag displacement XY vectors
XYVects = List[List[int]]
# A tuple of three integers representing a point in 3D space.
Point = Tuple[int, int, int]
# A tuple of two points representing an edge in 3D space.
Edge = Tuple[Point, Point]
# A set of edges.
Edges = Set[Edge]
# A list of threads representing a weaving loom.
Loom = List[Union[Deque[Point], List[Point]]]
# An iterator providing information about the z-coordinate, the yarn color and size of each layer.
ZInfo = Iterator[Tuple[int, int, int]]
# A list of points representing the Hamiltonian Cycle.
Solution = List[Point]
# A dictionary mapping colors to lists of zigzag vectors.
Spool = Dict[int, List[List[int]]]
# A list of lists representing spun yarn.
Spun = List[List[int]]
# A list of points representing a tour.
Tour = List[Point]
# A list of tours representing subtours.
Subtours = List[Tour]
# A set of points representing pins used for cutting yarn.
Pins = Set[Point]
# A generator of integers.
UonGen = Generator[int, None, None]
# An iterator of integers.
Unpacker = Iterator[int]
# A list of XYVects representing zigzag vectors.
ZigZags = List[XYVects]
