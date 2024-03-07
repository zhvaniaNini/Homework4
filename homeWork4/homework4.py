import multiprocessing
from concurrent.futures import ThreadPoolExecutor
import requests
import json
import time

base_URL = "https://dummyjson.com/products/"
product_URLs = [f"{base_URL}{i}" for i in range(1, 101)]


def data_from_URL(url):
    response = requests.get(url)
    data = response.json()
    with open("Products.json", 'a') as f:
        json.dump(data, f)
        f.write('\n')
    print(f"Response from {url} added")


def process_task():
    with ThreadPoolExecutor(max_workers=20) as executor:
        for url in product_URLs:
            executor.submit(data_from_URL, url)


if __name__ == "__main__":
    start = time.perf_counter()
    processes = []
    for _ in range(5):
        process = multiprocessing.Process(target=process_task)
        processes.append(process)
        process.start()

    for process in processes:
        process.join()

    end = time.perf_counter()
    elapsed_time = end - start
    print(f"All requests completed in {round(elapsed_time, 2)} seconds")
