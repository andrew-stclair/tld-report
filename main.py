import requests, json, time, re, queue, threading

thread_count = 20

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

class Create_Queue(threading.Thread):
    def __init__(self, q, *args, **kwargs):
        self.q = q
        super().__init__(*args, **kwargs)
    def run(self):
        tlds = requests.get("https://tld-list.com/df/tld-list-basic.json").json()
        for tld in tlds:
            if not re.search('[^a-z0-9]+', tld, flags=0):
                q.put(tld)

class Worker(threading.Thread):
    def __init__(self, id, q, list, *args, **kwargs):
        self.id = id
        self.q = q
        self.list = list
        super().__init__(*args, **kwargs)
    def run(self):
        while True:
            try:
                tld = self.q.get(timeout=10)
            except queue.Empty:
                return
            r = requests.get(f"https://www.spamhaus.org/statistics/checktld/{tld}", headers=headers)
            print(f"{self.id:>3}: {tld:<15} = {r.text}")
            if r.text.split(" ")[0] == tld:
                badness = r.text.split(" ")[-1].replace(")", "")
                percent = r.text.split(" ")[2].replace("%", "")
                list[tld] = {"badness":badness,"percent":percent}
            time.sleep(1)
            self.q.task_done()
            

q = queue.Queue(maxsize=thread_count)
list = {}

Create_Queue(q).start()

time.sleep(5)

for i in range(thread_count):
    print(f"Starting worker {i+1} of {thread_count}")
    Worker(i, q, list).start()
q.join()

time.sleep(10)

f = open("results.json", 'w')
f.write(json.dumps(list, indent=2))
f.close()
