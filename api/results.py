from api.common import get_json_with_retry

def get_results(season=None, limit=None, offset=None):
    if season:
        url = f"https://api.jolpi.ca/ergast/f1/{season}/results.json"
    else:
        url = "https://api.jolpi.ca/ergast/f1/results.json"

    params = {}
    if limit is not None:
        params["limit"] = limit
    if offset is not None:
        params["offset"] = offset

    return get_json_with_retry(url, params=params)
