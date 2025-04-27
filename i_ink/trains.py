import requests
from lxml import html
import re
from datetime import datetime, timedelta

def get_next_wkd_trains():
    """
    Scrapes the WKD website for the next scheduled trains at Malichy station.
    Returns a sorted list of (time, train_number) tuples.
    """
    url = "https://www.wkd.com.pl/?tmpl=module&module_id=123"
    headers = {"User-Agent": "Mozilla/5.0"}

    try:
        response = requests.get(url, headers=headers, timeout=10)
        doc = html.fromstring(response.content)

        element = doc.xpath('//*[@id="module-123"]/div[2]/div[2]/div[1]/div[3]/div[1]/ul/li[18]')
        if not element:
            return []

        chunks = element[0].text_content().split()
        results = []
        for chunk in chunks:
            match = re.search(r'(\d{4}).*?(\d{2}:\d{2})', chunk)
            if match:
                train_no, time_str = match.groups()
                time_obj = datetime.strptime(time_str, "%H:%M").time()
                results.append((time_obj, train_no))

        return sorted(results, key=lambda x: x[0])

    except Exception as e:
        print(f"Error fetching WKD data: {e}")
        return []

def filter_trains_for_display(train_list, max_display=3, earliest_minutes_ahead=1):
    """
    Filters trains to include only those departing at least `earliest_minutes_ahead` in the future.
    Returns up to `max_display` upcoming departures.
    """
    now = datetime.now().time()
    results = []

    for train_time, train_no in train_list:
        if train_time > now:
            delta = datetime.combine(datetime.today(), train_time) - datetime.combine(datetime.today(), now)
            if delta >= timedelta(minutes=earliest_minutes_ahead):
                results.append((train_time, train_no))
            if len(results) == max_display:
                break

    return results
