import math


def is_valid_triangle(a, b, c) -> bool:
    sides = (a, b, c)
    if not all(math.isfinite(side) and side > 0 for side in sides):
        return False

    return a + b > c and a + c > b and b + c > a


def classify_triangle(a, b, c) -> str:
    if not is_valid_triangle(a, b, c):
        return "Invalid"

    if a == b == c:
        triangle_type = "Equilateral"
    elif a == b or a == c or b == c:
        triangle_type = "Isosceles"
    else:
        triangle_type = "Scalene"

    shortest, middle, longest = sorted((a, b, c))
    if math.isclose(
        (shortest / longest) ** 2 + (middle / longest) ** 2,
        1.0,
        rel_tol=1e-9,
    ):
        return f"Right {triangle_type}"

    return triangle_type
