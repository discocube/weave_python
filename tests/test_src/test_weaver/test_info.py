import pytest

from itertools import repeat
from more_itertools import interleave
from src.weaver.info import *


@pytest.fixture
def z_info_fixture():
    n = 5  # Change the value of n as needed
    return list(get_z_color_size(n))


@pytest.fixture
def order_fixture():
    radius = 3  # Change the value of radius as needed
    return get_order_from_radius(radius)


@pytest.fixture
def radius_fixture():
    n = 5  # Change the value of n as needed
    return get_radius_from_n(n)


def test_get_z_color_size(z_info_fixture):
    assert isinstance(z_info_fixture, list)
    assert (
        len(z_info_fixture) == 5
    )  # Adjust the expected length based on the value of n


def test_get_order_from_radius(order_fixture):
    assert isinstance(order_fixture, int)


def test_get_radius_from_n(radius_fixture):
    assert isinstance(radius_fixture, int)
