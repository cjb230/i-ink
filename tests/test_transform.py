import pytest
from i_ink.transform import uvi_to_str


@pytest.mark.parametrize("uvi,expected", [
    (0.0,  "Low"),
    (1.9,  "Low"),
    (2.0,  "Moderate"),
    (4.9,  "Moderate"),
    (5.0,  "High"),
    (6.9,  "High"),
    (7.0,  "Very high"),
    (9.9,  "Very high"),
    (10.0, "Extreme"),
    (12.0, "Extreme"),
])
def test_uvi_to_str(uvi, expected):
    assert uvi_to_str(uvi) == expected
