import requests
import time
from math import ceil

base = 'https://api.jolpi.ca/ergast/f1'
seasons = list(range(1970, 2027))

def get_total(url):
    for attempt in range(1, 8):
        r = requests.get(url, params={'limit':1,'offset':0}, timeout=30)
        if r.status_code == 429:
            ra = r.headers.get('Retry-After')
            wait = 60
            if ra:
                try:
                    wait = max(1, int(float(ra)))
                except ValueError:
                    wait = 60
            print('429', url, 'wait', wait, 'attempt', attempt)
            time.sleep(wait)
            continue
        r.raise_for_status()
        return int(r.json().get('MRData', {}).get('total', 0))
    raise RuntimeError('Failed after retries: ' + url)

sum_requests = 0
for year in seasons:
    url = f'{base}/{year}/results.json'
    total = get_total(url)
    pages = ceil(total / 100) if total else 1
    sum_requests += pages
    print(year, total, pages)
    time.sleep(1.5)
print('TOTAL_REQUESTS_RESULTS', sum_requests)
