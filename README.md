# Triangle Classifier

A Python triangle classifier developed for a Software Engineering testing assignment. Given three side lengths, the program checks whether they form a valid triangle and identifies its shape. It also flags right triangles, which the customer needs to identify for reinforced corners in stained-glass pieces.

## Features

- Rejects non-positive or non-finite side lengths and triangles that fail the triangle inequality.
- Classifies valid triangles as `Equilateral`, `Isosceles`, or `Scalene`.
- Adds the `Right ` prefix for right triangles, such as `Right Scalene` or `Right Isosceles`.
- Uses `math.isclose()` instead of exact floating-point equality for right-angle detection.

## Project Files

| File | Purpose |
| --- | --- |
| `triangle.py` | Triangle validation and classification functions |
| `test_triangle.py` | Pytest unit tests for classifications and boundaries |
| `test_acceptance.py` | End-to-end test of the stained-glass customer's requirements |
| `requirements.txt` | Pytest dependency |
| `README.md` | Project information and testing documentation |

## Setup and Testing

Requires Python 3.9 or newer.

```bash
# Clone the repository
git clone https://github.com/jaskaranbhogal/TriangleClassifier.git
cd TriangleClassifier

# Install the testing dependency
python3 -m pip install -r requirements.txt

# Run every test
python3 -m pytest -v
```

Run the unit and acceptance tests separately if needed:

```bash
python3 -m pytest test_triangle.py -v
python3 -m pytest test_acceptance.py -v
```

The suite contains **19 unit-test cases (some parameterized) and one acceptance test**. The acceptance test evaluates eight customer scenarios in one test function.

### Example Use

```python
from triangle import is_valid_triangle, classify_triangle

print(is_valid_triangle(3, 4, 5))       # True
print(classify_triangle(3, 4, 5))       # Right Scalene
print(classify_triangle(5, 5, 6))       # Isosceles
print(classify_triangle(1, 2, 3))       # Invalid
```

## Equivalence Classes and Boundaries

The following classes were identified from the specification. Each class includes representative test inputs:

| Class | Example sides | Expected result |
| --- | --- | --- |
| Non-positive side | `(0, 3, 4)`, `(-1, 3, 4)` | `Invalid` |
| Triangle inequality fails | `(2, 3, 6)` | `Invalid` |
| Degenerate boundary (sum equals third side) | `(1, 2, 3)` | `Invalid` |
| Equilateral | `(4, 4, 4)` | `Equilateral` |
| Isosceles (exactly two sides equal) | `(5, 5, 6)` | `Isosceles` |
| Scalene (all sides different) | `(4, 5, 6)` | `Scalene` |
| Right scalene | `(3, 4, 5)` | `Right Scalene` |
| Right isosceles with a non-integer side | `(5, 5, 5 * sqrt(2))` | `Right Isosceles` |
| Non-finite side | `(inf, 3, 4)` | `Invalid` |

**Boundary checks:** A side length of zero is rejected, as is a degenerate triangle where the sum of two sides **equals** the third. Permutations of side lengths are tested because classification should not depend on input order. For floating-point right triangles, the tests use `5 * math.sqrt(2)` as a hypotenuse; exact `==` comparisons are unreliable in this case, so `math.isclose()` is used in the classifier.

An **equilateral triangle cannot be right** because its three interior angles are all 60 degrees; a right triangle must contain one 90-degree angle.

## Customer Acceptance Criteria

**Customer scenario:** A stained-glass studio enters three side lengths to determine whether a piece can be built, its shape, and whether its corners need right-angle reinforcement.

1. **Valid shapes:** For three positive, finite lengths that satisfy all strict triangle inequalities, `classify_triangle()` returns the correct shape (`Equilateral`, `Isosceles`, or `Scalene`), with a `Right ` prefix when applicable.
2. **Invalid pieces:** If a side is non-positive or the sum of two sides is less than or equal to the third, `classify_triangle()` returns exactly `Invalid` instead of a shape label.
3. **Right-angle flagging:** For a valid right triangle, including one with a non-integer hypotenuse, the returned string starts with `Right `. For a non-right triangle, it does not.

The test in `test_acceptance.py` calls `classify_triangle()` directly and checks eight complete input-to-output scenarios: three non-right shapes, three invalid pieces, a right scalene triangle, and a right isosceles triangle. This tests the available application interface, which is a Python function rather than a graphical interface.

## Copilot Review Log

GitHub Copilot suggested a `unittest`-based draft covering triangle validity and classification. The draft checked positive and negative side lengths, degenerate triangles, all three regular shapes, and right triangles. It included the following code (shared from the Copilot suggestion for review):

```python
import unittest
from triangle import is_valid_triangle, classify_triangle

class TestTriangleFunctions(unittest.TestCase):
    def test_is_valid_triangle(self):
        # Valid triangles
        self.assertTrue(is_valid_triangle(3, 4, 5))
        self.assertTrue(is_valid_triangle(5, 5, 5))
        self.assertTrue(is_valid_triangle(7, 10, 5))

        # Invalid triangles
        self.assertFalse(is_valid_triangle(0, 4, 5))
        self.assertFalse(is_valid_triangle(-3, 4, 5))
        self.assertFalse(is_valid_triangle(1, 2, 3))  # Not satisfying triangle inequality
        self.assertFalse(is_valid_triangle(float('inf'), 4, 5))

    def test_classify_triangle(self):
        # Invalid triangles
        self.assertEqual(classify_triangle(0, 4, 5), "Invalid")
        self.assertEqual(classify_triangle(1, 2, 3), "Invalid")

        # Equilateral triangles
        self.assertEqual(classify_triangle(5, 5, 5), "Equilateral")

        # Isosceles triangles
        self.assertEqual(classify_triangle(5, 5, 8), "Isosceles")
        self.assertEqual(classify_triangle(8, 5, 5), "Isosceles")
        self.assertEqual(classify_triangle(5, 8, 5), "Isosceles")

        # Scalene triangles
        self.assertEqual(classify_triangle(7, 10, 5), "Scalene")

        # Right triangles
        self.assertEqual(classify_triangle(3, 4, 5), "Right Scalene")
        self.assertEqual(classify_triangle(5, 12, 13), "Right Scalene")
        self.assertEqual(classify_triangle(1, 1, math.sqrt(2)), "Right Isosceles")


if __name__ == "__main__":
    unittest.main()
```

### Review of Suggestions

| Test | Copilot-suggested? | Kept / edited / rejected | Why |
| --- | --- | --- | --- |
| `test_is_valid_triangle` | Yes | Not adopted verbatim | The suggested tests use `unittest.TestCase`. The assignment requests pytest tests, so the repository uses pytest functions and `@pytest.mark.parametrize` to cover the same validity and boundary categories. |
| `test_classify_triangle` | Yes | Rejected as written | The suggested right-isosceles assertion calls `math.sqrt(2)` without `import math`, which would cause a `NameError`. The repository's tests import `math` and use a non-integer hypotenuse explicitly. |
| Right-triangle floating-point test | Yes, as part of `test_classify_triangle` | Reviewed and supplemented | The suggested example includes a right isosceles triangle with `sqrt(2)`. The pytest suite also checks that exact squared-side equality fails for a floating-point example and that the classifier still returns `Right Isosceles` using tolerance. |

The suggestion was **not copied unchanged**. In particular, the missing `math` import was a concrete error identified while reviewing the proposed test code. Note that pytest can discover `unittest.TestCase` tests, but native pytest functions fit the assignment's requested style better.

## AI-Use Disclosure

- **GitHub Copilot:** Provided the `unittest`-based unit-test suggestion reproduced above. It was reviewed against the specification; the missing `math` import and the difference in test style were identified. The repository's final tests use pytest.
- **ChatGPT (OpenAI):** Assisted in drafting pytest tests and README, and helped check test coverage against the assignment requirements. 
