import requests
import urllib.request


HEADERS={
    # "Host": "www.anisearch.com",
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:108.0) Gecko/20100101 Firefox/108.0",
    # "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,*/*;q=0.8",
    # "Accept-Language": "en-US,en;q=0.5",
    # "Accept-Encoding": "gzip, deflate, br",
    # "DNT": "1",
    # "Connection": "keep-alive",
    # "Upgrade-Insecure-Requests": "1",
    # "Sec-Fetch-Dest": "document",
    # "Sec-Fetch-Mode": "navigate",
    # "Sec-Fetch-Site": "none",
    # "Sec-Fetch-User": "?1",
    # "Pragma": "no-cache",
    # "Cache-Control": "no-cache",
}


def load(link) -> bytes:
    return requests.get(link, headers=HEADERS, timeout=0.2).content