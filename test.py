import requests
import time
import random
import string
url_us = "http://34.63.203.225:8080"
url_europe = "http://34.78.63.195:8080"

def first_test():
    registe_latency_us = 0
    registe_latency_europe = 0
    list_latency_us = 0
    list_latency_europe = 0
    for i in range(10):
        start_time = time.time()
        requests.post(url_us + "/register", json={"username": "test" + str(i)})
        end_time = time.time()
        registe_latency_us += end_time - start_time
    for i in range(10):
        start_time = time.time()
        requests.get(url_us + "/list")
        end_time = time.time()
        list_latency_us += end_time - start_time
    for i in range(10):
        start_time = time.time()
        requests.post(url_europe + "/register", json={"username": "test" + str(i)})
        end_time = time.time()
        registe_latency_europe += end_time - start_time
    for i in range(10):
        start_time = time.time()
        requests.get(url_europe + "/list")
        end_time = time.time()
        list_latency_europe += end_time - start_time
    latency = f"Registe latency US: {registe_latency_us / 10}, List latency US: {list_latency_us / 10}, \
        Registe latency Europe: {registe_latency_europe / 10}, List latency Europe: {list_latency_europe / 10}"
    print(latency)

def second_test():
    time_not_found = 0
    for _ in range(100):
        user_name = ''.join(random.choices(string.ascii_lowercase, k=8))
        requests.post(url_us + "/register", json={"username": user_name})
        resp = requests.get(url_us + "/list")
        users = resp.json().get("users", []) if resp.ok else []
        if user_name not in users:
            print("Error: User not found in list")
            time_not_found += 1
    print(f"time not found: {time_not_found}")

if __name__ == "__main__":
    first_test()
    second_test()