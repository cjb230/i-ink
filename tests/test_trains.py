from unittest.mock import MagicMock
from i_ink.trains import get_next_wkd_trains, _parse_train_element

def test_parse_train_element_deduplicates_same_train_different_leading_zeros():
    # WKD sometimes lists the same train twice with inconsistent leading zeros
    # e.g. "006134" and "0006134" at the same time — should produce one entry
    element = MagicMock()
    element.text_content.return_value = (
        "006134.a{fill:#004982;}00:12.a{fill:#004982;} "
        "0006134.a{fill:#004982;}00:12.a{fill:#004982;}"
    )
    result = _parse_train_element(element)
    assert len(result) == 1
    assert result[0][0].strftime("%H:%M") == "00:12"


def test_scraper_runs():
    trains = get_next_wkd_trains()
    assert isinstance(trains, dict), "Expected trains to be a dictionary"
    assert "warsaw" in trains, "Expected 'warsaw' key to be present"
    assert "podkowa_lesna" in trains, "Expected 'podkowa_lesna' key to be present"
    assert "timestamp" in trains, "Expected 'timestamp' key to be present"    
    assert len(trains) == 3, "Expect exactly two destinations for trains"
    assert isinstance(trains["warsaw"], list), "Expected 'warsaw' to be a list"
    assert isinstance(trains["podkowa_lesna"], list), "Expected 'podkowa_lesna' to be a list"
