

## Installation

To build and install the package (including any requirements listed in the 'install_requires' parameter in the setup.py file), in "editable" mode, run the following command:
```
pip install -e .
```

## Usage

Once the package is installed, you can run it from the command line by using:
```
weave --start 100 --end 100 --plot 100
```
Where `start` is the start range and `end` is the end of the range inclusive and `plot` is the solution to plot.

Please note that most browsers won't be able to handle plotting over 10 million vertices. 