"""Unit tests for Brand Gate."""
import pytest


def test_placeholder():
    """Placeholder test to verify test infrastructure works."""
    assert True, "Test infrastructure is working"


def test_calculation():
    """Example test demonstrating pytest usage."""
    result = 2 + 2
    assert result == 4, "Basic arithmetic should work"


@pytest.mark.parametrize("input,expected", [
    (0, 0),
    (1, 1),
    (5, 25),
    (10, 100),
])
def test_square(input, expected):
    """Test square function with parameterized inputs."""
    result = input * input
    assert result == expected, f"Square of {input} should be {expected}"