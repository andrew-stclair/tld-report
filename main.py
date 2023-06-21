"""Function for ordering Dictionaries"""
from collections import OrderedDict
import json
import time
import re
import queue
import threading
import requests

THREAD_COUNT = 30

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


class CreateQueue(threading.Thread):
    """Thread that Creates the Queue"""

    def __init__(self, tld_queue, *args, **kwargs):
        self.tld_queue = tld_queue
        super().__init__(*args, **kwargs)

    def run(self):
        tlds = requests.get(
            "https://tld-list.com/df/tld-list-basic.json", timeout=20).json()
        for tld in tlds:
            if not re.search('[^a-z0-9]+', tld, flags=0):
                self.tld_queue.put(tld)


class Worker(threading.Thread):
    """Thread that works on each object in the queue"""

    def __init__(self, thread_id, tld_queue, dict_item, *args, **kwargs):
        self.thread_id = thread_id
        self.tld_queue = tld_queue
        self.dict_item = dict_item
        super().__init__(*args, **kwargs)

    def run(self):
        while True:
            try:
                tld = self.tld_queue.get(timeout=10)
            except queue.Empty:
                return
            request = requests.get(f"https://www.spamhaus.org/statistics/checktld/{tld}",
                                   headers=headers, timeout=20)
            print(f"{self.thread_id:>3}: {tld:<15} = {request.text}")
            if request.text.split(" ")[0] == tld:
                badness = request.text.split(" ")[-1].replace(")", "")
                percent = request.text.split(" ")[2].replace("%", "")
                item_dict[tld] = {"badness": badness, "percent": percent}
            time.sleep(THREAD_COUNT/10)
            self.tld_queue.task_done()


q = queue.Queue(maxsize=THREAD_COUNT)
item_dict = {}

CreateQueue(q).start()

time.sleep(5)

for i in range(THREAD_COUNT):
    print(f"Starting worker {i+1} of {THREAD_COUNT}")
    Worker(i, q, item_dict).start()
q.join()

time.sleep(10)

with open("results.json", 'w', encoding='utf-8') as results_file:
    results_file.write(json.dumps(OrderedDict(
        sorted(item_dict.items())), indent=2))
