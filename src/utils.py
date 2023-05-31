"""
Utility functions for the weave program.

This module provides utility functions for:
- checking if the solution is a Hamiltonian Cycle
- plotting the solution
- profiling, timing, and counting.

Functions:
- check_solution(solution: Solution) -> None: Check if a solution is a valid Hamiltonian Cycle.
- plot_solution(solution: Solution): Plot a solution using pandas and plotly.
- parametrized(dec): Decorator allows adding parameters to other decorators.
- times(fn, n=10): Run a function multiple times and time it.
- profile(func, dump=None): Decorator that profiles the execution of a function using cProfile.
- tstamp() -> str: Generate a formatted date and timestamp.
- unpack(nested_list: Any) -> Unpacker: Unpack a nested list into a generator.

"""
from typing import Any, Iterable
from datetime import datetime
from functools import wraps

import time
import cProfile
import pstats
import pandas as pd
import plotly.express as px


from src.weaver.info import get_order_from_n, get_order_from_radius
from src.weaver.types import Solution, Unpacker


def check_solution(solution: Solution) -> None:
    """Check solution if it is a Hamiltonian Cycle by:

    - Length of solution is equal to the order based on the
        maximum scalar value of all vertices.
    - The values are unique.
    - The total accumulation of vector displacements is (0, 0, 0)
    - The next step is one edge-length in only the x, y, z axis.
        So point_a - point_b = (0, 0, 2)..

    Args:
        solution (Solution): Solution to be checked.
    """
    # Check if the number of vertices matches the order based on max scalar point value.
    order = get_order_from_radius(max(unpack(solution)))
    assert len(solution) == order
    # Check for duplicates
    assert len(set(solution)) == order
    # accumulate the displacements to this start value.
    total_disps = (0, 0, 0)
    previous = solution[-1]
    for x_val, y_val, z_val in solution:
        (a_val, b_val, c_val) = previous
        # calculate displacement by getting the difference between previous and current vert.
        disp = (a_val - x_val, b_val - y_val, c_val - z_val)
        # add to total displacement to ensure that total is (0, 0, 0)
        total_disps = tuple((total_disps[i] + disp[i] for i in range(3)))
        # check if the displacement is always one step in one axis.
        assert [abs(d) for d in disp if d] == [2]
        # assign (x, y, z) to previous for the next iteration of the loop.
        previous = (x_val, y_val, z_val)
    # Total displacement of a loop is (0, 0, 0)
    assert total_disps == (0, 0, 0)


def plot_solution(solution: Solution):
    """Plot solution using pandas and plotly.

    Parameters:
    -----------
    file_path : str
        The path to the CSV file containing the data to be plotted.

    Returns:
    --------
    None
    """
    # Convert solution to DataFrame
    dataframe = pd.DataFrame(solution + solution[:1], columns=["X", "Y", "Z"])

    # Plot 3D line using plotly.express
    fig = px.line_3d(dataframe, x="X", y="Y", z="Z")
    fig.show()


def parametrized(dec):
    """
    allows adding parameters to decorated decorator
    dec: decorator to which parameters are added
    :return: decorator to be parametrized
    """

    def layer(*args, **kwargs):
        def repl(func):
            return dec(func, *args, **kwargs)

        return repl

    return layer


@parametrized
def times(func, repeats=10):
    """
    Run function n times and timeit.
    """

    @wraps(func)
    def inner(*args, **kwargs):
        start = time.perf_counter()
        res = None
        for _ in range(repeats):
            res = func(*args, **kwargs)
        print(f"x{repeats}: {func.__name__} took {(time.perf_counter() - start)}")
        return res

    return inner


def profile(dump=None):
    """
    cprofile decorated function.
    """

    def decorator(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            profiler = cProfile.Profile()
            profiler.enable()
            order = get_order_from_n(args[0]) if args else None
            try:
                return_value = func(*args, **kwargs)
                order = len(return_value) if return_value else order
            finally:
                profiler.disable()
                stats = pstats.Stats(profiler)
                stats.sort_stats("tottime")
                stats.print_stats()
                prim, total = (
                    stats.__dict__["prim_calls"],
                    stats.__dict__["total_calls"],
                )
                print(
                    f"⭕️ {order}: {prim / total:.2%} primitive of {total} calls \
                        | {total / order} calls / n"
                )
                if dump:
                    stats.dump_stats(dump)
            return return_value

        return wrapper

    return decorator


def tstamp() -> str:
    """
    date- and timestamper
    In this format: 18:21 02/06/22
    """
    return datetime.now().strftime("%H:%M %d/%m/%y")


def unpack(nested_list: Any) -> Unpacker:
    """
    Unpack (completely) a nested list into a generator
    """
    for nested in nested_list:
        # Unpack until nested is not str or bytes.
        if isinstance(nested, Iterable) and not isinstance(nested, (str, bytes)):
            yield from unpack(nested)
        else:
            yield nested
