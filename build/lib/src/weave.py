"""
This module provides a function for weaving a Hamiltonian Cycle of a Manhattan Ball of n layers, including the core cube.

Functions:
- weave(n: int) -> Solution:
    Weave a Hamiltonian Cycle of a Manhattan Ball of n layers, including the core cube.

Types:
- Loom: A collection of threads representing a weaving loom.
- Solution: A list of vectors representing the Hamiltonian Cycle.
- Spool: A Hamiltonian chain of 2D vectors representing a yarn.

Module Dependencies:
- from src.weaver.info import get_radius_from_n, get_z_color_size
- from src.weaver.ops import *
- from src.weaver.types import Loom, Solution, Spool

Note: The module depends on other modules from the 'src.weaver' package for additional functionality.

Example Usage:

```
from src.weaver import weave

# Weave a Hamiltonian Cycle for a Manhattan Ball with 5 layers
solution = weave(5)
check_solution(solution)
print(solution)
```
"""

from src.utils import profile
from src.weaver.info import get_order_from_n, get_radius_from_n, get_z_color_size
from src.weaver.ops import *
from src.weaver.types import Loom, Solution, Spool


@profile()
def weave(n: int) -> Solution:
    """Weave a Hamiltonian Cycle of a Manhattan Ball of n layers including the core cube.

    Args:
        n (int): Number of layers around the core and including the core cube.

    Returns:
        Solution: Hamiltonian Cycle of level n of the uncentered octahedral numbers.
    """
    # get order and radius of n with edge-length of 2.
    (order, radius) = (get_order_from_n(n), get_radius_from_n(n))
    # walk tour of xy-floor with the most number of verts, mirror and displace to make red and blue.
    yarns: Spool = spin_yarn(radius=radius)
    # Loom onto which the solution is woven.
    loom: Loom = []
    # Build the solution from the bottom up (-radius to -1 in odd steps) onto the loom.
    for z, color, size in get_z_color_size(n):
        # Extend each thread in the loom:
        extend_threads(
            loom,
            # prepare yarn by getting the color and chop it with pins:
            chop(
                [(*xy, z) for xy in yarns[color][:size]],
                # pin each thread end in loom and get pins for cutting.
                pin_thread_ends(loom, z),
            ),
        )
    # Convert threads in loom into lists:
    loom = [list(thread) for thread in loom]
    # Mirror chains to form subcycles
    mirror_chains(loom)
    # Merge cycles into one cycle and return solution
    return merge_cycles(loom, radius, order)
