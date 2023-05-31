"""
Weave Program

This script implements the Weave program, which performs weaving operations based on command-line arguments. It uses the `weave` function from the `src.weave` module to perform the weaving, and it also utilizes other utility functions from the `src.utils` module.

Command-line Arguments:
  --start START   Start value for weaving (default: 1)
  --end END       End value for weaving (default: start)
  --plot PLOT     Value to plot (default: end)

Description:
  The script performs weaving operations by iterating over a range of values from `start` to `end` (inclusive). For each value, it measures the time taken by the `weave` function, checks the solution, and prints the duration. Additionally, it can plot the solution for a specific value `plot`.

Example Usage:
  # Navigate to main.py under weave_python
  python weave --start 3 --end 7 --plot 5

"""

import argparse
import time

from src.utils import check_solution, plot_solution
from src.weave import weave
from src.weaver.info import get_order_from_n


def main():
    """
    Main function to parse arguments and run weave. Will plot last instance solved.
    """
    # Argument Parsing
    parser = argparse.ArgumentParser(description="Weave Program")
    parser.add_argument("--start", type=int, default=1, help="Start value (default: 1)")
    parser.add_argument("--end", type=int, help="End value (default: start)")
    parser.add_argument("--plot", type=int, help="Value to plot (default: end)")
    args = parser.parse_args()
    # Assigning Arguments
    start = args.start
    end = args.end if args.end else start
    # If n to plot is greater than the end value, plot the end.
    to_plot = args.plot if args.plot is not None else end
    # Make sure that args.plot is within the range being solved.
    plot = end if to_plot > end else to_plot
    # weave the range from start to end inclusive.
    for i in range(start, end + 1):
        # start timer.
        begin = time.perf_counter()
        # find solution then certify, time and plot.
        solution = weave(i)
        stop = time.perf_counter() - begin
        # Certify Solution before plotting.
        check_solution(solution)
        # Display duration of weave().
        print(f"Order {len(solution)} solved and certified: solving took {stop} secs.")
        # Plot last solution if specific n is not specified.
        if i == plot:
            print(f"Plotting n={plot} to web.")
            plot_solution(solution)


if __name__ == "__main__":
    main()

""" 
Pylint: Pylint is a widely used linting tool that checks for programming errors, coding style, 
and potential bugs. It provides detailed reports and supports a wide range of configurable options. 
You can install Pylint using pip (pip install pylint) and then 
run it on your Python files using the command pylint <filename>.

Flake8: Flake8 combines multiple Python linting tools, including PyFlakes, 
pycodestyle (formerly known as Pep8), and McCabe. It checks for coding style issues, syntax errors, 
and common programming mistakes. Install Flake8 using pip (pip install flake8) and run it 
with the command flake8 <filename>.

Black: Black is a Python code formatter that also incorporates linting capabilities. 
It automatically formats your code according to a set of predefined rules, ensuring consistent 
and readable code style. Install Black using pip (pip install black) 
and run it with the command black <filename>.

PyCodeStyle (formerly known as Pep8): PyCodeStyle checks Python code against the PEP 8 style guide. 
It ensures your code adheres to the recommended Python coding style conventions. Install 
PyCodeStyle using pip (pip install pycodestyle) and run it with the command pycodestyle <filename>.
"""
