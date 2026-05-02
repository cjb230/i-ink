import requests
from lxml import html
import re
from datetime import datetime, timedelta, timezone

def _parse_train_element(element) -> list:
    """
    Parses train departures from a WKD timetable HTML element.

    The element's text content is a mix of SVG icon styling and train data.
    Each whitespace-separated chunk may contain a 4-digit train number and an
    HH:MM departure time, e.g.:
      '6128.a,.b{fill:none;}...20:42.a{fill:#004982;}'
    Returns a sorted list of (datetime.time, train_number) tuples.
    """
    results = []
    for chunk in element.text_content().split():
        match = re.search(r'(\d{4}).*?(\d{2}:\d{2})', chunk)
        if match:
            train_no, time_str = match.groups()
            try:
                time_obj = datetime.strptime(time_str, "%H:%M").time()
            except ValueError:
                time_str = time_str.replace("24", "00")
                time_obj = datetime.strptime(time_str, "%H:%M").time()
            results.append((time_obj, train_no))
    return sorted(results, key=lambda x: x[0])


def get_next_wkd_trains() -> dict[str, list | str]:
    """
    Scrapes the WKD website for the next scheduled trains at Malichy station.
    Returns a sorted list of (time, train_number) tuples.
    """
    url = "https://www.wkd.com.pl/?tmpl=module&module_id=123"
    headers = {"User-Agent": "Mozilla/5.0"}

    try:
        print("Fetching WKD data... ", end="")
        response = requests.get(url, headers=headers, timeout=10)
        doc = html.fromstring(response.content)
        print(f"fetched {len(response.content)} chars")

        xpaths = {
            "warsaw":        '//*[@id="module-123"]/div[2]/div[2]/div[1]/div[3]/div[1]/ul/li[18]',
            "podkowa_lesna": '//*[@id="module-123"]/div[2]/div[2]/div[1]/div[2]/div[2]/ul/li[18]',
        }

        result = {"timestamp": datetime.now(timezone.utc).isoformat()}
        for direction, xpath in xpaths.items():
            elements = doc.xpath(xpath)
            result[direction] = _parse_train_element(elements[0]) if elements else []
        return result
    except Exception as e:
        print(f"Error fetching WKD data: {e}")
        raise e


def filter_trains_for_display(train_dict, max_display=3, earliest_minutes_ahead=1):
    """
    Filters trains to include only those departing at least `earliest_minutes_ahead` in the future.
    Returns up to `max_display` upcoming departures.
    """
    now = datetime.now().time()
    results = {"warsaw": [],  "podkowa_lesna": []}
    results["timestamp"] = train_dict["timestamp"]
    del train_dict["timestamp"]
    #print(train_dict)
    for train_direction, train_list in train_dict.items():
        for train_time, train_no in train_list:
            if train_time > now:
                delta = datetime.combine(datetime.today(), train_time) - datetime.combine(datetime.today(), now)
                if delta >= timedelta(minutes=earliest_minutes_ahead):
                    results[train_direction].append((train_time, train_no))
                if len(results) == max_display:
                    break
    return results
