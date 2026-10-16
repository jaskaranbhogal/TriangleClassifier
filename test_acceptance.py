import math

from triangle import classify_triangle


def test_stained_glass_customer_acceptance():
    cases = [
        ((4, 4, 4), "Equilateral"),
        ((5, 5, 6), "Isosceles"),
        ((4, 5, 6), "Scalene"),
        ((0, 3, 4), "Invalid"),
        ((1, 2, 3), "Invalid"),
        ((2, 3, 6), "Invalid"),
        ((3, 4, 5), "Right Scalene"),
        ((5, 5, 5 * math.sqrt(2)), "Right Isosceles"),
    ]

    for sides, expected in cases:
        actual = classify_triangle(*sides)
        assert actual == expected, f"Sides {sides}: expected {expected}, got {actual}"
