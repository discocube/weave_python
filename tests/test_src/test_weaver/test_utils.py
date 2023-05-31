import pytest
from more_itertools import windowed
from src.weaver.utils import *


@pytest.fixture
def weft_fixture():
    # Replace with a sample Weft object for testing
    data = [(0, 0, 0), (0, 0, 2), (2, 0, 2), (2, 0, 0)]
    n = 5
    return Weaver(data, n)


def test_weft_edges(weft_fixture):
    # Replace with appropriate test for edges property of Weft class
    assert isinstance(weft_fixture.edges, Edges)


def test_weft_get_eadj():
    # Replace with appropriate test for get_eadj method of Weft class
    pass


def test_weft_join(weft_fixture):
    # Replace with appropriate test for join method of Weft class
    pass


def test_get_edges():
    # Replace with appropriate test for get_edges function
    pass


def test_get_eadjs():
    # Replace with appropriate test for get_eadjs function
    pass


def test_align_to():
    # Replace with appropriate test for align_to function
    pass


# from src.warps import *


# @pytest.fixture
# def tour_fixture():
#     # Change the value of tour as needed
#     return [(3, 1, '_'), (1, 3, '_'), (3, 1, '_'), (1, 3, '_')]


# @pytest.fixture
# def edges_fixture(tour_fixture):
#     joined = True  # Change the value of joined as needed
#     return get_edges(tour_fixture, joined)


# @pytest.fixture
# def eadjs_fixture(edges_fixture):
#     return get_eadjs(edges_fixture)


# def test_get_edges(edges_fixture):
#     assert isinstance(edges_fixture, set)


# def test_get_eadjs(eadjs_fixture):
#     assert isinstance(eadjs_fixture, set)
