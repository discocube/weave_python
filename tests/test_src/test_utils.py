import pytest
from src.utils import *


@pytest.fixture
def solution_fixture():
    # Change the value of solution as needed
    return [(0, 0, 0), (0, 0, 2), (2, 0, 2), (2, 0, 0)]


def test_unpack():
    nested_list = [[1, 2, 3], [4, 5, 6], [7, 8, 9]]
    unpacked = list(unpack(nested_list))
    assert unpacked == [1, 2, 3, 4, 5, 6, 7, 8, 9]


def test_check_solution(solution_fixture):
    check_solution(solution_fixture)


def test_check_solution_invalid_order():
    solution = [(0, 0, 0), (0, 0, 2), (2, 0, 2)]
    with pytest.raises(AssertionError):
        check_solution(solution)


def test_check_solution_duplicate_vertices():
    solution = [(0, 0, 0), (0, 0, 2), (2, 0, 2), (2, 0, 2)]
    with pytest.raises(AssertionError):
        check_solution(solution)


def test_check_solution_invalid_displacement():
    solution = [(0, 0, 0), (0, 0, 2), (2, 0, 3), (2, 0, 0)]
    with pytest.raises(AssertionError):
        check_solution(solution)


def test_check_solution_nonzero_total_displacement():
    solution = [(0, 0, 0), (0, 0, 2), (2, 0, 2), (2, 0, 0), (0, 0, 0)]
    with pytest.raises(AssertionError):
        check_solution(solution)
