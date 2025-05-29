import requests

def fetch_high_impact_events_from_api():
    url = "https://cdn-nfs.faireconomy.media/ff_calendar_thisweek.json"
    try:
        response = requests.get(url, timeout=10)
        response.raise_for_status()
        data = response.json()
    except Exception as e:
        return f"Error fetching calendar JSON: {e}"

    events = data.get("events", [])
    output = []

    for event in events:
        # Impact can be "High", "Medium", "Low"
        if event.get("impact") == "High":
            date = event.get("date")
            time = event.get("time")
            currency = event.get("currency")
            event_name = event.get("title")
            output.append(f"{date} {time} - {currency} - {event_name}")

    return "\n".join(output) or "No high-impact events found."

if __name__ == "__main__":
    print("=== High-Impact Forex Events (API) ===")
    print(fetch_high_impact_events_from_api())
