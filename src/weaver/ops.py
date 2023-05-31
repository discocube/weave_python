"""
This module provides functions for weaving and merging cycles in a 2D zig-zagging pattern.

Functions:
- spin_yarn(radius: int) -> Spool:
    Spin a 2D zig-zagging outwards turning Hamiltonian path
    from the innermost vertex [-1, 1] or [1, 1] to [radius, 1].
- pin_thread_ends(loom: Loom, z: int) -> Pins:
    Add a node one z level up to the end of each thread in the loom.
- chop(tour: Tour, pins: Pins) -> Subtours:
    Chop a tour into subtours using pins as markers for cutting.
- extend_threads(loom: Loom, chopped: Subtours) -> None:
    Extend each thread of the loom with the matching chopped segment.
- mirror_chains(loom: Loom) -> None:
    Mirror the chains in the loom to create a loom of loops.
- merge_cycles(loom: Loom, n: int) -> Solution:
    Merge cycles by finding bridge edges between two loops,
    aligning them, and joining them.

Types:
- Spool: A Hamiltonian chain of 2D vectors representing a yarn.
- ZigZags: A list of 2D displacement vectors for zigzag movements.
- Loom: A collection of threads representing a weaving loom.
- LoomThread: A thread in the loom, represented as a deque of vectors.
- Pins: A set of vectors representing pins or markers for cutting yarn.
- Tour: A list of vectors representing a tour or path.
- Subtours: A list of subtours obtained by cutting a tour using pins.
- Solution: A list of vectors resulting from merging cycles into one cycle.
"""

from collections import deque

import numpy as np

from src.weaver.types import Loom, Pins, Solution, Spool, Subtours, Tour, ZigZags
from src.weaver.utils import LoomThread, Weaver


def spin_yarn(radius: int) -> Spool:
    """Spin a 2d zig-zagging outwards turning Hamiltonian path
    from the innermost vert [-1, 1] or [1, 1] to [radius, 1]

    Args:
        r (int): Radius of Manhattan Ball with an edge-length of 2.

    Returns:
        Spool: A Hamiltonian Chain of 2d vectors where the first item
        is either [-1, 1] or [1, 1] and the last item is [radius, 1]
    """
    # XY Zigzag Displacement Vectors.
    zigzags: ZigZags = [
        [[0, 2], [2, 0]],
        [[0, 2], [-2, 0]],
        [[0, -2], [-2, 0]],
        [[0, -2], [2, 0]],
    ]
    # Start vector and displacement vectors are different for odd and even numbers.
    (spun, dpv) = (
        ([(1, 1)], zigzags)
        if not ((radius + 1) // 2) % 2
        else ([(-1, 1)], zigzags[2:] + zigzags[:2])
    )
    # Return path which is an accumulation starting with the start vector and using
    # collected zigzag vectors as an iterator getting the next step by adding a zigzag vector.
    zigzags = [
        dpv[idx % 4][(idx + isize) % 2]
        for idx, size in enumerate(
            # start from 1 to the radius, odd steps: if r = 5: (1, 3, 5)
            # repeat three times if it is the radius else twice:
            # [[1, 1], [3, 3], [5, 5, 5]] then flatten
            # Aggregating values in generator expressions results in a call for
            #   each item whereas a list comprehension there is one call.
            [
                item
                for nested in [
                    [x] * (2 if x != radius else 3) for x in range(1, radius + 1, 2)
                ]
                for item in nested
            ]
        )
        # size corresponds to the number of xy to take from a particular zigzag:
        # example with 3 will result in yxy, 7: yxyxyxy from a xy zigzag pair.
        for isize in range(size)
    ]
    for idx, (x_val, y_val) in enumerate(zigzags):
        spun += [((prev := spun[idx])[0] + x_val, prev[1] + y_val)]

    return {
        # The original spun is blue
        3: spun,
        # Mirror and displace (one positive step in the y-axis) the original as assign to red
        1: list(np.add(np.dot(np.array(spun), [[-1, 0], [0, -1]]), [0, 2])),
    }


def pin_thread_ends(loom: Loom, z_value: int) -> Pins:
    """Add a node one z level up to the end of each thread in loom.

    Args:
        loom (_type_): Loom with threads for weaving.
    """
    # Collect appended left and right side nodes to each thread.
    pins = set()
    # for each thread in loom append the node that is one step (+2 units) along the z-axis.
    for thread in loom:
        # append-left and assign appended to left
        thread.appendleft(left := (*thread[0][:2], z_value))
        # append-right and assign appended to right
        thread += [right := (*thread[-1][:2], z_value)]
        # Collect pins to use as markers for cutting yarn.
        pins |= {left, right}
    return pins


def chop(tour: Tour, pins: Pins) -> Subtours:
    """Chop tour into subtours using pins

    Args:
    tour: Tour to cut
    pins: Pins used to cut tour into subtours.

    Returns:
    Subtours where each pin is the first index of a subtour in subtours
    """
    # No pins no cutting.
    if not pins:
        # return a reversed tour in a list (expects subtours):
        return [tour[::-1]]
    subtours = []
    # Get a list of indices that are ordered and enumerated, reverse that and iterate:
    for i, j in reversed(list(enumerate([x for x, t in enumerate(tour) if t in pins]))):
        # first instance if first item not in pins:
        if not i and tour[0] not in pins:
            subtours += [tour[: j + 1][::-1]]
            # Does not always result in a tour so we need filter to avoid going through
            # the entire list to check for empties.
            if subtour1 := tour[j + 1 :]:
                subtours += [subtour1]
        else:
            # for every other case other than the first.
            subtours += [tour[j:]]
            # we'll need to delete the last section we just appended (simulates moving items)
            tour[j:] = []
    return subtours


def extend_threads(loom: Loom, subtours: Subtours) -> None:
    """Extend each thread of the loom with the matching chopped segment.

    Args:
        loom (Loom): Container onto which solution is woven.
        chopped (Subtours): Subtours chopped to match the threads.
    """
    # visited list to collect indices which have been incorporated.
    used = set()
    for thread in loom:
        for idx, subtour in enumerate(subtours):
            if idx not in used:
                # if first item in subtour matches the first item in thread.
                if thread[0] == subtour[0]:
                    thread.extendleft(subtour[1:])
                    used |= {idx}
                # if first item in subtour matches the last item in thread.
                elif thread[-1] == subtour[0]:
                    thread += subtour[1:]
                    used |= {idx}
    loom += [deque(ch) for idx, ch in enumerate(subtours) if idx not in used]


def mirror_chains(loom: Loom) -> None:
    """Mirror the chains to create a loom of loops.

    Args:
        loom (Loom): Where solution is woven.
    """
    # Take each thread (chain) and mirror it into a cycle.
    for thread in loom:
        # for each thread in loom, mirror the sequence and reverse the sign of the z-scalar value.
        thread += [(x, y, -z) for x, y, z in thread[::-1]]


def merge_cycles(loom: Loom, radius: int, order: int) -> Solution:
    """Merge cycles by finding bridge edges between two loops, aligning each to edge and joining.

    Args:
        loom (Loom): Container holding the threads to be joined.
        n (int): instance of graph. number of layers if the manhattan ball.

    Returns:
        Solution: A list of vectors resulting from the merging of subcycles into one cycle.
    """
    # separate the first item and convert to weaver and leave others in loom.
    weaver = Weaver(data=loom.pop(0), radius=radius, order=order)
    # Add each thread to the weaver's data:
    for thread in loom:
        # Get edges of current thread and pass in if any cycle has been joined.
        thread_edges = LoomThread.get_edges(thread, weaver.joined)
        # edge belonging to weft that is adjacent to warp_edges.
        weft_bridge = (weaver.edges & LoomThread.get_eadjs(thread_edges)).pop()
        # align weft to bridge so that the lhs and rhs of weft.data matches those of weft_bridge.
        Weaver.align_to(weaver.data, *weft_bridge)
        # align current thread to a reversed bridge edge resulting from the intersection
        # of thread edges and adjacent edge of weft_bridge.
        Weaver.align_to(
            thread, *reversed((thread_edges & Weaver.get_eadj(weft_bridge)).pop())
        )
        # join the current thread to the weaver.
        weaver.join(thread)
    return weaver.data
