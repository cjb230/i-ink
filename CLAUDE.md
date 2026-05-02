# CLAUDE.md

## What this project is

A Raspberry Pi e-ink dashboard. It runs a loop every 4 minutes: scrape WKD train times, fetch weather from a local proxy, render a composite Pillow image, and push it to a Waveshare 7.5" e-ink display. See README.md for full details.

## Running

```bash
python run.py          # development (uses mock display, saves out.png)
./start.sh             # production Pi deploy (pulls git, activates venv, sets GPIO)
```

## Testing

```bash
pytest                        # runs all tests (requires network)
pytest -m "not integration"   # offline-safe subset
```

- `tests/test_trains.py::test_scraper_runs` is marked `@pytest.mark.integration` — it makes a live HTTP request to wkd.com.pl and will fail offline. Skip it with `-m "not integration"`.
- `tests/test_weather.py` — uses local fixture data but requires the `tesseract` binary (`brew install tesseract` on Mac, `apt-get install tesseract-ocr` on Linux)

## Architecture notes

- `display/__init__.py` auto-detects Raspberry Pi via `platform.uname()` and selects `RealDisplay` or `MockDisplay`. No env var or flag needed.
- Weather data comes from a local proxy at `192.168.1.129:8080`, not directly from OpenWeatherMap. The `.env` variables (`OWM_API_KEY` etc.) are consumed by that proxy, not by this app.
- Times are hardcoded to `Europe/Warsaw` timezone in `transform.py` (`unix_ts_to_str`, `transform_trains`, `transform_weather`).
- The display only refreshes when the image body (top 750px) has changed — `conditional_update_screen` in `main.py` compares raw pixel bytes.
- `render_weather_days` is a stub — it returns a blank white image.

## Key files

| File | Role |
|---|---|
| `i_ink/main.py` | Entry point, main loop, signal handling |
| `i_ink/trains.py` | WKD scraper — XPath-based, fragile to site changes |
| `i_ink/weather.py` | Thin HTTP client for the local weather proxy |
| `i_ink/transform.py` | Converts raw API dicts to display-ready structures |
| `i_ink/render.py` | All Pillow drawing; font loading; SVG weather icons via cairosvg |

## Known issues / rough edges

- `filter_trains_for_display` in `trains.py` is unused — filtering is done in `transform_trains`.
- `pyproject.toml` is missing several runtime dependencies (`cairosvg`, `python-dotenv`, `zoneinfo` backport).
- Weather icon SVGs must be present in `svg/` at the repo root (not tracked in git — source them from OpenWeatherMap).
