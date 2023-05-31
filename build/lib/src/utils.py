import cProfile
import pandas as pd
import plotly.express as px
import pstats

import time

from datetime import datetime
from functools import wraps
from itertools import repeat

from src.weaver.info import get_order_from_n, get_order_from_radius
from src.weaver.types import Any, Iterable, Solution, Unpacker


def check_solution(solution: Solution) -> None:
    """Check solution if it is a Hamiltonian Cycle by:

    - Length of solution is equal to the order based on the maximum scalar value of all the vertices.
    - The values are unique.
    - The total vector displacement (accumulation of displacements) is (0, 0, 0)
    - The next step is one edge-length in only the x, y, z axis. So point_a - point_b = (0, 0, 2)...

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
    for idx, (x, y, z) in enumerate(solution):
        (a, b, c) = previous
        # calculate displacement by getting the difference between previous and current vert.
        displacement = (a - x, b - y, c - z)
        # add to total displacement to ensure that in the end the total is (0, 0, 0)
        total_disps = tuple((total_disps[i] + displacement[i] for i in range(3)))
        # check if the displacement is always one step in one axis.
        assert {abs(d) for d in displacement} == {0, 0, 2}
        # assign (x, y, z) to previous for the next iteration of the loop.
        previous = (x, y, z)
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
    df = pd.DataFrame(solution + solution[:1], columns=["X", "Y", "Z"])

    # Plot 3D line using plotly.express
    fig = px.line_3d(df, x="X", y="Y", z="Z")
    fig.show()


_c = 0


def cp(show=False, spacing=None, label=" №", justify=0) -> int:
    """
    Increments global variable _c consecutively when called during the lifetime of 
    executing a program regardless of scope.
    """

    def count():
        """
        Inner.
        """
        global _c
        _c += 1
        if show:
            if spacing:
                if not _c % spacing:
                    print(f"{_c}_{label}") if label else print(f"{_c}")
            else:
                out = f" {label} {_c}" if label else f"{_c}"
                print(f"{out}".rjust(justify, " "))
        return _c

    return count()


def timed(fn):
    """
    Decorator that times a function and prints a pretty readout
    fn: function to time
    :return: fn + runtime of decorated function.
    """

    @wraps(fn)
    def inner(*args, **kwargs):
        """
        inner function with lots of emojis.
        """
        fn_name = fn.__name__.upper()
        st = time.perf_counter()
        border = "═" + ("══" * ((len(fn.__name__) + 30) // 2))
        print()
        cp(show=True)
        print(border + "╕")
        print(f" 📌 {fn_name} | 🏁 {tstamp()}\n")
        res = fn(*args, **kwargs)
        print("\n", f"🕳 {fn_name} | 🕗 {time.perf_counter() - st:.7f} secs")
        print(border + "╛", "\n")
        return res

    return inner


def parametrized(dec):
    """
    allows adding parameters to decorated decorator
    dec: decorator to which parameters are added
    :return: decorator to be parametrized
    """

    def layer(*args, **kwargs):
        def repl(f):
            return dec(f, *args, **kwargs)

        return repl

    return layer


@parametrized
def times(fn, n=10):
    """
    Run function n times and timeit.
    """

    @wraps(fn)
    def inner(*args, **kwargs):
        start = time.perf_counter()
        res = None
        for i in range(n):
            res = fn(*args, **kwargs)
        print(f"x{n}: {fn.__name__} took {(time.perf_counter() - start)}")
        return res

    return inner


@parametrized
def profile(func, dump=None):
    """
    cprofile decorated function.
    """

    @wraps(func)
    def wrapper(*args, **kwargs):
        profiler = cProfile.Profile()
        profiler.enable()
        order = get_order_from_n(args[0])
        try:
            return_value = func(*args, **kwargs)
            order = len(return_value)
        finally:
            profiler.disable()
            stats = pstats.Stats(profiler)
            stats.sort_stats("tottime")
            stats.print_stats()
            prim, total = stats.__dict__["prim_calls"], stats.__dict__["total_calls"]
            print(
                f"⭕️ {order}: {prim / total:.2%} primitive of {total} calls | {round(total / order, 2)} calls / n"
            )
            if dump:
                stats.dump_stats(dump)
        return return_value

    return wrapper


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
