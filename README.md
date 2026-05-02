# i-ink

A Raspberry Pi e-ink dashboard displaying WKD commuter train times and local weather on a 7.5" Waveshare display (480×800px).

## What it shows

The screen is divided into five vertical sections:

| Section | Content |
|---|---|
| Current weather (top) | Weather icon, temperature, feels-like, UV index, minute-by-minute rain forecast, active alerts |
| Hourly forecast | Icon + temperature for the next 4 hours |
| Daily forecast | *(placeholder — not yet implemented)* |
| Train times | Next departures from Malichy toward Warsaw (left) and Podkowa Leśna (right) |
| Footer | Last-updated timestamps for weather and trains |

The screen only refreshes when the image has actually changed, to preserve e-ink panel lifetime.

## Hardware

- Raspberry Pi (any model with SPI)
- [Waveshare 7.5" e-Paper HAT V2](https://www.waveshare.com/7.5inch-e-paper-hat.htm) (`epd7in5_V2`)

On non-Pi machines the display is replaced by a mock that saves `out.png` and opens it — useful for development.

## Data sources

### Weather
Fetches from a self-hosted proxy at `http://192.168.1.129:8080/data` (expected on the local network). The proxy should return OpenWeatherMap One Call API 3.0 JSON wrapped as:

```json
{
  "timestamp": "<ISO-8601 UTC string>",
  "error": null,
  "result": { /* OWM One Call response */ }
}
```

### Trains
Scrapes the [WKD timetable module](https://www.wkd.com.pl/?tmpl=module&module_id=123) for upcoming departures at Malichy station. Only trains departing ≥1 minute in the future are shown.

## Setup

### Prerequisites

Python 3.13.3, plus system libraries for the e-ink driver on Pi:

```bash
sudo apt-get install python3-dev libgpiod2 pigpio tesseract-ocr
```

### Install

```bash
git clone <repo>
cd i-ink
python -m venv myenv
source myenv/bin/activate
pip install -e .
```

### Environment

Copy `example.env` to `.env` and fill in your values (used by the weather proxy, not directly by this app):

```
LATITUDE=52.0
LONGITUDE=20.9
LOCAL_TIMEZONE="Europe/Warsaw"
OWM_API_KEY=your_key_here
```

### Run

```bash
python run.py
```

On a Pi, use `start.sh` which pulls the latest code, activates the venv, sets the GPIO pin factory, and starts the process with logging to `/home/cjb/i-ink.log`:

```bash
./start.sh
```

To run at boot, add `start.sh` to cron or a systemd service.

## Development

On a non-Pi machine the mock display is used automatically — no hardware required.

```bash
pip install -e ".[dev]"
pytest
```

The train scraper test (`tests/test_trains.py`) makes a live HTTP request to the WKD website. The weather alert tests (`tests/test_weather.py`) use fixture data.

## Project layout

```
i_ink/
  main.py          # Main loop — fetch, transform, render, display
  trains.py        # WKD website scraper
  weather.py       # Weather proxy client
  transform.py     # Raw API data → display-ready dicts
  render.py        # Pillow image composition
  display/
    __init__.py    # Auto-selects real or mock display
    interface.py   # Abstract base class
    real.py        # Waveshare EPD driver wrapper
    mock.py        # Saves out.png for local testing
    epd7in5_V2.py  # Vendor driver (SPI)
    epdconfig.py   # Vendor GPIO/SPI config
```
