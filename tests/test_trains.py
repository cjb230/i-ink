from i_ink.trains import get_next_wkd_trains

def test_scraper_runs():
    trains = get_next_wkd_trains()
    assert isinstance(trains, dict), "Expected trains to be a dictionary"
    assert "warsaw" in trains, "Expected 'warsaw' key to be present"
    assert "podkowa_lesna" in trains, "Expected 'podkowa_lesna' key to be present"
    assert "timestamp" in trains, "Expected 'timestamp' key to be present"    
    assert len(trains) == 3, "Expect exactly two destinations for trains"
    assert isinstance(trains["warsaw"], list), "Expected 'warsaw' to be a list"
    assert isinstance(trains["podkowa_lesna"], list), "Expected 'podkowa_lesna' to be a list"
