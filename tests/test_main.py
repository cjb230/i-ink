import atexit
from datetime import time
import signal
from unittest.mock import patch, MagicMock
import pytest

import i_ink.main as main


def test_handle_signal_clears_display_once():
    mock_display = MagicMock()
    with patch.object(main, 'DISPLAY', mock_display):
        with pytest.raises(SystemExit):
            main.handle_signal(signal.SIGINT, None)
    mock_display.clear.assert_called_once()


def test_handle_signal_unregisters_atexit():
    with patch('atexit.unregister') as mock_unregister:
        with pytest.raises(SystemExit):
            main.handle_signal(signal.SIGINT, None)
    mock_unregister.assert_called_once_with(main.cleanup)


def reset_source_state():
    main.LATEST_WEATHER = None
    main.LATEST_TRAINS = None
    main.WEATHER_FAILURE_COUNT = 0
    main.TRAINS_FAILURE_COUNT = 0
    main.LAST_WEATHER_ERROR = None
    main.LAST_TRAINS_ERROR = None


def test_weather_failure_uses_last_good_data_until_threshold():
    reset_source_state()
    main.FAILURE_ALERT_THRESHOLD = 3
    main.LATEST_WEATHER = {"update_str": "08:00:00", "hourly": [], "daily": [], "current": {}}

    with patch.object(main, "fetch_forecast", side_effect=RuntimeError("connection refused")):
        result = main.fetch_weather_for_display()

    assert result is main.LATEST_WEATHER
    assert "error" not in result
    assert main.WEATHER_FAILURE_COUNT == 1


def test_weather_failure_displays_error_after_threshold():
    reset_source_state()
    main.FAILURE_ALERT_THRESHOLD = 3
    main.LATEST_WEATHER = {"update_str": "08:00:00", "hourly": [], "daily": [], "current": {}}

    with patch.object(main, "fetch_forecast", side_effect=RuntimeError("connection refused")):
        for _ in range(4):
            result = main.fetch_weather_for_display()

    assert result["update_str"] == "08:00:00"
    assert "Weather source failed 4 times in a row" in result["error"]
    assert "tail /home/cjb/i-ink.log" in result["error"]
    assert "192.168.1.66" in result["error"]


def test_train_failure_displays_error_after_threshold():
    reset_source_state()
    main.FAILURE_ALERT_THRESHOLD = 3
    main.LATEST_TRAINS = {
        "warsaw": [(time(8, 5), "1001")],
        "podkowa_lesna": [(time(8, 10), "2001")],
        "update_str": "08:00:00",
    }

    with patch.object(main, "get_next_wkd_trains", side_effect=RuntimeError("wkd down")):
        for _ in range(4):
            result = main.fetch_trains_for_display()

    assert result["update_str"] == "08:00:00"
    assert result["warsaw"] == []
    assert result["podkowa_lesna"] == []
    assert "Train source failed 4 times in a row" in result["error"]
    assert "tail /home/cjb/i-ink.log" in result["error"]


def test_source_success_resets_failure_count():
    reset_source_state()
    main.WEATHER_FAILURE_COUNT = 2
    weather_payload = {"timestamp": "2025-01-01T08:00:00+00:00", "error": "upstream error"}

    with patch.object(main, "fetch_forecast", return_value=weather_payload):
        result = main.fetch_weather_for_display()

    assert "missing" in result
    assert main.WEATHER_FAILURE_COUNT == 3

    good_weather = {"update_str": "08:00:00", "hourly": [], "daily": [], "current": {}}
    with patch.object(main, "fetch_forecast", return_value={"ok": True}):
        with patch.object(main, "transform_weather", return_value=good_weather):
            result = main.fetch_weather_for_display()

    assert result is good_weather
    assert main.WEATHER_FAILURE_COUNT == 0
