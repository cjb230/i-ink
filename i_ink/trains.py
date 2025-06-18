import requests
from lxml import html
import re
from datetime import datetime, timedelta, timezone

def get_next_wkd_trains() -> dict[str, list]:
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

        to_warsaw_element = doc.xpath('//*[@id="module-123"]/div[2]/div[2]/div[1]/div[3]/div[1]/ul/li[18]')
        to_podkowa_lesna_element = doc.xpath('//*[@id="module-123"]/div[2]/div[2]/div[1]/div[2]/div[2]/ul/li[18]')

        if not to_warsaw_element and not to_podkowa_lesna_element:
            return []

        chunks = to_warsaw_element[0].text_content().split()
        results = []
        for chunk in chunks:
            match = re.search(r'(\d{4}).*?(\d{2}:\d{2})', chunk)
            if match:
                train_no, time_str = match.groups()
                try:
                    time_obj = datetime.strptime(time_str, "%H:%M").time()
                except ValueError as e:
                    time_str = time_str.replace("24","00")
                    time_obj = datetime.strptime(time_str, "%H:%M").time()
                results.append((time_obj, train_no))
        to_warsaw_results = sorted(results, key=lambda x: x[0])
        # print(to_warsaw_results)
        chunks = to_podkowa_lesna_element[0].text_content().split()
        results = []
        for chunk in chunks:
            match = re.search(r'(\d{4}).*?(\d{2}:\d{2})', chunk)
            if match:
                train_no, time_str = match.groups()
                try:
                    time_obj = datetime.strptime(time_str, "%H:%M").time()
                except ValueError as e:
                    time_str = time_str.replace("24","00")
                    time_obj = datetime.strptime(time_str, "%H:%M").time()
                results.append((time_obj, train_no))
        to_podkowa_lesna_results = sorted(results, key=lambda x: x[0])
        kk = {"warsaw": to_warsaw_results,
              "podkowa_lesna": to_podkowa_lesna_results,
              "timestamp": datetime.now(timezone.utc).isoformat()}
        return kk
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
