from src.weaver.types import Edge, Edges, Point, Tour

"""
This module contains classes and functions related to merging many subcycles into one.

class Weft: Responsible for merging other cycles into it and incrementing the elevation at which the cycles are joined / merged and getting the edges and adjacent edges of weft.data.
    __init__(self, data: Tour, n: int) -> None: Set data and initialize [order, z_abs_max, zc_abs_sum] using n.
    @property edges(self) -> Edges: Tuple windows from data and filter according to conditions to simplify.
    @staticmethod get_eadj(edge: Edge) -> Edge: Get one parallel edge from given edge based on if joined or not.
    join(self, other: Tour) -> None: Join self with other after it has been aligned. 

class LoomThread: Responsible for getting the edges and adjacent edges of the threads left in the loom.
    @staticmethod get_edges(data: Tour, joined: bool = True) -> Edges: Get edges of thread and filter based on joined.
    @staticmethod get_eadjs(edges: Edges) -> Edges: Get adjacent edges of edges and filter to shorten data. 
"""


class Weaver:
    """
    Weaver is responsible for merging other cycles into it and incrementing the elevation at which the cycles are joined/merged.
    It also provides functions to get the edges and adjacent edges of the weaver's data.
    """

    def __init__(self, data: Tour, radius: int, order: int) -> None:
        """
        Initialize the Weft with the provided data and number of layers.

        Args:
            data (Tour): The data representing the weft.
            n (int): The number of layers around a central core with the core included.
        """
        # Main loop onto which others are incorporated
        self.data: Tour = data
        # Number of vertices in the graph or the corners of all the cubes.
        self.order: int = order
        # Elements are merged at different axes depending on whether it has been joined already, hence the need for a switch.
        self.joined: bool = False
        # The maximum absolute scalar value for z.
        self.z_abs_max: int = radius - 4
        # Initial value used to determine current elevation of the stitch (merge) and incremented to elevate position.
        self.zc_abs_sum: int = self.z_abs_max * 2

    @property
    def edges(self) -> Edges:
        """
        Get the edges of the weaver's data.

        Returns:
            Edges: The edges of the weaver's data.
        """
        return {
            # ensure that the edges are correctly aligned where lhs < rhs.
            (u, v) if u < v else (v, u)
            for u, v in zip(self.data, self.data[1:])
            # VALID: ((1, _, zc_abs_sum), (3, _, zc_abs_sum))
            if ([u[0], v[0]] == [1, 3] and not self.joined)
            # VALID: ((1, _, zc_abs_sum), (1, _, zc_abs_sum))
            or ([u[0], v[0]] == [1, 1] and self.joined)
            and {u[2] + v[2]} & {-self.zc_abs_sum, self.zc_abs_sum}
        }

    @staticmethod
    def get_eadj(edge: Edge) -> Edge:
        """Get an adjacent edge of one edge.

        Args:
            edge (Edge): Edge from which to get the adjacent edge.

        Returns:
            Edge: Adjacent edge of edge. If edge lies along the x axis return the parallel edge one positive step along the y-axis.
            Otherwise return the parallel edge one positive step along the x-axis.
        """
        # unpacked into scalar values to avoid edge[0][0] for x etc...
        ((a, b, c), (x, y, z)) = edge
        return {
            # if edge lies along x-axis: the adjacent parallel edge is one step (2 units) along the y-axis.
            # if edge lies along y- or z-axis: the parallel / adjacent edge is one positive step in the x-axis
            ((a, b + 2, c), (x, y + 2, z))
            if a != x
            else ((a + 2, b, c), (x + 2, y, z))
        }

    @staticmethod
    def align_to(data: Tour, lhs: Point, rhs: Point) -> None:
        """Align data to edge so that ends of data match lhs and rhs..

        Args:
            data (Tour): Data to be aligned.
            lhs (Point): The value to which the left hand side of data should be rotated.
            rhs (Point): The value to which the right hand side of data should be rotated.
        """
        if (lix := data.index(lhs)) < (rix := data.index(rhs)):
            data[:] = data[rix - 1 :: -1] + data[: rix - 1 : -1]
        else:
            data[:] = data[lix:] + data[:lix]

    def join(self, other: Tour) -> None:
        """Join self to other by extending to end.

        Args:
            other (Tour): Subtour to be joined.
        """
        # Extend other to end of self.data
        self.data += other
        if self.joined:
            self.z_abs_max -= 4
        else:
            self.joined = True
            self.z_abs_max -= 2
        self.zc_abs_sum = self.z_abs_max * 2 - 2


class LoomThread:
    """
    General convenience methods for merging the subcycles in the Loom with the Weaver's data.
    """

    @staticmethod
    def get_edges(data: Tour, joined: bool = True) -> Edges:
        """Make edges which is the windowed(seq, size=2) and filtered.

        Or: set(map(lambda e: e if e[0] < e[1] else (e[1], e[0]), filter(lambda mn: [mn[1][1], mn[0][0], mn[0][1]] == ([1, 3, 1] if joined else [3, 1, 3]), windowed(data, 2))))

        Args:
            data (Tour): _description_a
            joined (bool, optional): Flag before or after start of merging. Defaults to True.

        Returns:
            Edges: List of edges.
        """
        return {
            # lhs < rhs to ensure consistent orientation of edges.
            (m, n) if m < n else (n, m)
            # tuple windows of data
            for m, n in zip(data, data[1:])
            # check if it matches this pattern if joined: ((3, 1, _), (_, 1, _)) else ((1, 3, _), (_, 3, _))
            if [n[1], m[0], m[1]] == ([1, 3, 1] if joined else [3, 1, 3])
        }

    @staticmethod
    def get_eadjs(edges: Edges) -> Edges:
        """Get the adjacent edges of edges. One edge per edge and not 4.

        Args:
            edges (Edges): Data as sliding window of size 2.

        Returns:
            Edges: Adjacent edges of edges.
        """
        return {
            # if edge lies along x-axis: get parallel edge one positive step along the y-axis
            ((a, b - 2, c), (x, y - 2, z)) if a != x
            # if edge lies along y-axis: get parallel edge one positive step along the z-axis
            else ((a, b, c + 2), (x, y, z + 2)) if b != y
            # if edge lies along y-axis: get parallel edge one positive step along the z-axis
            else ((a - 2, b, c), (x - 2, y, z))
            for (a, b, c), (x, y, z) in edges
            # (1 or 3, 1 or 3, _)
            if (x == 1 or x == 3) and (y == 1 or y == 3)
        }
