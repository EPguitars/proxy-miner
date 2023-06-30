""" Get's list of free proxies and filtering them """
import asyncio
import time

from httpx import AsyncClient

from free_proxies_scraper import scrape_proxies

TESTING_URL = "https://multicity.23met.ru/"
SCRAPING_INTERVAL = 650
TESTING_HEADER = {"User-Agent": "Mozilla/5.0 (X11; Linux x86_64) " +
                                "AppleWebKit/537.36 (KHTML, like Gecko) " +
                                "Ubuntu Chromium/37.0.2062.94" +
                                "Chrome/37.0.2062.94 Safari/537.36"}


async def good_proxy(proxy_attempt: str):
    """ checks connection with current proxy """
    url = TESTING_URL
    current_proxy = f"http://{proxy_attempt}"
    proxies = {"http://": current_proxy, "https://": current_proxy}
    # pylint: disable=E1129
    async with AsyncClient(headers=TESTING_HEADER, proxies=proxies) as test_client:

        try:
            test_response = await test_client.get(url)
        # pylint: disable=W0718
        # Need this block to catch and register unexpected exceptions
        # uncomment to see log in terminal
        except Exception as exception:
            #print(f"Unregistered Exception: {exception.__class__.__name__}")
            return None
        if test_response.status_code == 200:
            return proxy_attempt
        return None


async def filter_proxies(proxies):
    """ filtering free proxies and getting most stable """
    tasks = []

    for element in proxies:
        tasks.append(good_proxy(element))

    checked_proxies = await asyncio.gather(*tasks)
    with open("applied_proxies.txt", "a", encoding="utf=8") as new_file:
        for data in checked_proxies:
            if data is not None:
                new_file.write(data + "\n")
                print(data)


while True:
    PROXIES = scrape_proxies()
    asyncio.run(filter_proxies(PROXIES))
    print(f"Scraped at {time.ctime()}")
    time.sleep(SCRAPING_INTERVAL)
