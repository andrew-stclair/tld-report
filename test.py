import requests, re

tlds = requests.get("https://tld-list.com/df/tld-list-basic.json").json()

headers = {
    "Host": "www.spamhaus.org",
    "User-Agent": "Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:109.0) Gecko/20100101 Firefox/113.0",
    "Accept": "*/*",
    "Accept-Language": "en-US,en;q=0.5",
    "Accept-Encoding": "gzip, deflate, br",
    "Alt-Used": "www.spamhaus.org",
    "Connection": "keep-alive",
    "Referer": "https://www.spamhaus.org/statistics/tlds/",
    "Cookie": "",
    "Sec-Fetch-Dest": "empty",
    "Sec-Fetch-Mode": "cors",
    "Sec-Fetch-Site": "same-origin",
    "TE": "trailers"
}

list = []
for tld in tlds:
    if re.search('[^a-z0-9]+', tld, flags=0):
        print(tld, "match")
    else:
        print(tld)
