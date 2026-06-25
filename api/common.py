import random
import time
import requests


def get_json_with_retry(url, params=None, max_retries=6, backoff_factor=1.0, throttle_seconds=1.0):
    """
    Fetch JSON from the API with shared retry and throttling behavior.

    This helper handles HTTP 429 responses by respecting Retry-After if present,
    otherwise falling back to an exponential backoff capped at 60 seconds.
    It also enforces a minimum throttle delay between successful requests.
    """
    attempt = 0
    while attempt < max_retries:
        attempt += 1
        try:
            response = requests.get(url, params=params or {}, timeout=30)
            if response.status_code == 429:
                retry_after = response.headers.get("Retry-After")
                if retry_after:
                    try:
                        wait_seconds = max(1, int(float(retry_after)))
                    except ValueError:
                        wait_seconds = 60
                else:
                    wait_seconds = min(60, backoff_factor * (2 ** (attempt - 1)))
                    if wait_seconds <= 0:
                        wait_seconds = 60
                wait_seconds = min(wait_seconds, 60)
                time.sleep(wait_seconds)
                continue

            response.raise_for_status()
            payload = response.json()

            time.sleep(throttle_seconds + random.uniform(0, 0.5))
            return payload

        except requests.RequestException as err:
            if attempt >= max_retries:
                raise RuntimeError(
                    f"Request failed after {max_retries} retries for {url} params={params}: {err}"
                )

            wait_seconds = min(60, backoff_factor * (2 ** (attempt - 1)))
            if wait_seconds <= 0:
                wait_seconds = 60
            time.sleep(wait_seconds)

    raise RuntimeError(f"Unable to fetch JSON from {url} after {max_retries} attempts.")
