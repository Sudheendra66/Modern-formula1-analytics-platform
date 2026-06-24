import requests

def get_races(season=None, limit=None, offset=None):
    if season:
        url = f"https://api.jolpi.ca/ergast/f1/{season}.json"
    else:
        url = "https://api.jolpi.ca/ergast/f1/races.json"

    params = {}
    if limit is not None:
        params["limit"] = limit
    if offset is not None:
        params["offset"] = offset

    response = requests.get(url, params=params, timeout=30)
    response.raise_for_status()

    return response.json()
