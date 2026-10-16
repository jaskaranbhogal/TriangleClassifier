import math

import pytest

from triangle import classify_triangle, is_valid_triangle


@pytest.mark.parametrize(
    "sides",
    [
        (0, 3, 4),
        (-1, 3, 4),
        (3, 0, 4),
        (3, 4, -1),
    ],
)
def test_non_positive_sides_are_invalid(sides):
    assert not is_valid_triangle(*sides)
    assert classify_triangle(*sides) == "Invalid"


@pytest.mark.parametrize("sides", [(1, 2, 3), (3, 1, 2), (2, 3, 1)])
def test_degenerate_triangles_are_invalid(sides):
    assert not is_valid_triangle(*sides)
    assert classify_triangle(*sides) == "Invalid"


def test_triangle_inequality_failure_is_invalid():
    assert not is_valid_triangle(2, 3, 6)
    assert classify_triangle(2, 3, 6) == "Invalid"


def test_equilateral_triangle():
    assert is_valid_triangle(4, 4, 4)
    assert classify_triangle(4, 4, 4) == "Equilateral"


@pytest.mark.parametrize("sides", [(5, 5, 6), (5, 6, 5), (6, 5, 5)])
def test_isosceles_triangle(sides):
    assert is_valid_triangle(*sides)
    assert classify_triangle(*sides) == "Isosceles"


def test_scalene_triangle():
    assert is_valid_triangle(4, 5, 6)
    assert classify_triangle(4, 5, 6) == "Scalene"


@pytest.mark.parametrize("sides", [(3, 4, 5), (5, 3, 4), (4, 5, 3)])
def test_right_scalene_triangle(sides):
    assert is_valid_triangle(*sides)
    assert classify_triangle(*sides) == "Right Scalene"


def test_right_isosceles_triangle_with_non_integer_hypotenuse():
    hypotenuse = 5 * math.sqrt(2)
    assert 5**2 + 5**2 != hypotenuse**2
    assert is_valid_triangle(5, 5, hypotenuse)
    assert classify_triangle(5, 5, hypotenuse) == "Right Isosceles"


def test_equilateral_triangle_is_not_right():
    assert classify_triangle(5, 5, 5) == "Equilateral"


def test_non_finite_sides_are_invalid():
    assert not is_valid_triangle(math.inf, 3, 4)
    assert classify_triangle(math.nan, 3, 4) == "Invalid"
