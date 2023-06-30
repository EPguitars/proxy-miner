""" This is a scraper for free-proxy-list.net """
import time

from httpx import Client
import pandas as pd


SCRAPING_INTERVAL = 650

def scrape_proxies() -> list:
    """ scraping free-proxy-list.net for current proxies """
    client = Client(headers={
                    "User-Agent": "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/45.0.2454.85 Safari/537.36"})
    URL = "https://free-proxy-list.net/"

    response = client.get(URL)

    table = pd.read_html(response.text)
    table = table[0]

    ips = table["IP Address"]
    ports = table["Port"]
    proxies_list = []

    for ip, port in zip(ips, ports):
        proxies_list.append(f"{ip}:{port}")

    return proxies_list


while True:

    proxies = scrape_proxies()
    with open("applied_proxies.txt", "a", encoding="utf=8") as new_file:
        for data in proxies:
            if data is not None:
                new_file.write(data + "\n")
        print(f"Scraped at {time.ctime()}")
    time.sleep(SCRAPING_INTERVAL)
