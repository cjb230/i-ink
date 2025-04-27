from i_ink.trains import get_next_wkd_trains

def test_scraper_runs():
    trains = get_next_wkd_trains()
    assert isinstance(trains, list)
