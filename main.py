import requests
from bs4 import BeautifulSoup
import pandas as pd
from helpers import get_all_info
import concurrent.futures

def scrape_conde():
    # Conde links to scrape
    links = [
        'https://www.cntraveler.com/gallery/best-hotels-in-cape-town',
        'https://www.cntraveler.com/gallery/best-hotels-in-bali',
        'https://www.cntraveler.com/gallery/best-hotels-hong-kong',
        'https://www.cntraveler.com/gallery/best-hotels-in-singapore',
        'https://www.cntraveler.com/gallery/best-hotels-in-tokyo',
        'https://www.cntraveler.com/gallery/best-hotels-in-melbourne',
        'https://www.cntraveler.com/gallery/best-hotels-in-sydney',
        'https://www.cntraveler.com/gallery/best-hotels-in-puerto-rico',
        'https://www.cntraveler.com/gallery/the-best-hotels-in-amsterdam',
        'https://www.cntraveler.com/gallery/best-hotels-in-barcelona',
        'https://www.cntraveler.com/gallery/best-hotels-in-berlin',
        'https://www.cntraveler.com/gallery/best-copenhagen-hotels',
        'https://www.cntraveler.com/gallery/best-hotels-in-dublin',
        'https://www.cntraveler.com/gallery/best-hotels-in-edinburgh',
        'https://www.cntraveler.com/gallery/best-hotels-in-florence',
        'https://www.cntraveler.com/gallery/best-hotels-lisbon',
        'https://www.cntraveler.com/gallery/best-hotels-in-london',
        'https://www.cntraveler.com/gallery/best-hotels-in-madrid',
        'https://www.cntraveler.com/gallery/the-best-hotels-in-paris',
        'https://www.cntraveler.com/gallery/best-hotels-in-rome',
        'https://www.cntraveler.com/gallery/best-hotels-in-venice',
        'https://www.cntraveler.com/gallery/best-hotels-in-abu-dhabi',
        'https://www.cntraveler.com/gallery/best-hotels-in-dubai',
        'https://www.cntraveler.com/gallery/best-hotels-in-boston',
        'https://www.cntraveler.com/gallery/best-hotels-in-charleston',
        'https://www.cntraveler.com/gallery/best-hotels-in-chicago',
        'https://www.cntraveler.com/gallery/best-hotels-in-dallas',
        'https://www.cntraveler.com/gallery/best-hotels-in-denver',
        'https://www.cntraveler.com/gallery/best-hotels-in-houston',
        'https://www.cntraveler.com/gallery/best-hotels-in-key-west',
        'https://www.cntraveler.com/gallery/best-hotels-in-las-vegas',
        'https://www.cntraveler.com/gallery/best-hotels-in-los-angeles',
        'https://www.cntraveler.com/gallery/best-resorts-in-maui',
        'https://www.cntraveler.com/gallery/best-hotels-in-mexico-city',
        'https://www.cntraveler.com/gallery/best-hotels-in-miami',
        'https://www.cntraveler.com/gallery/best-hotels-in-montreal',
        'https://www.cntraveler.com/gallery/best-hotels-in-nashville',
        'https://www.cntraveler.com/gallery/best-hotels-in-new-york-city',
        'https://www.cntraveler.com/gallery/best-hotels-in-orlando-florida',
        'https://www.cntraveler.com/gallery/best-hotels-in-philadelphia',
        'https://www.cntraveler.com/gallery/best-hotels-in-phoenix-and-scottsdale',
        'https://www.cntraveler.com/gallery/best-hotels-portland-maine',
        'https://www.cntraveler.com/gallery/best-hotels-in-portland-oregon',
        'https://www.cntraveler.com/gallery/best-hotels-in-puerto-rico',
        'https://www.cntraveler.com/gallery/best-hotels-in-san-diego',
        'https://www.cntraveler.com/gallery/best-hotels-in-san-francisco',
        'https://www.cntraveler.com/gallery/best-hotels-in-savannah',
        'https://www.cntraveler.com/gallery/the-best-hotels-in-seattle',
        'https://www.cntraveler.com/gallery/best-hotels-in-toronto',
        'https://www.cntraveler.com/gallery/best-hotels-in-vancouver',
        'https://www.cntraveler.com/gallery/the-best-hotels-in-washington-dc',
        'https://www.cntraveler.com/gallery/best-hotels-in-buenos-aires'
    ]

    with concurrent.futures.ThreadPoolExecutor(max_workers=60) as executor:  # Adjust max_workers as needed
        # Scrape hotel data concurrently
        nested_results = list(executor.map(get_all_info, links))

    # Flatten the nested list
    results = [item for sublist in nested_results for item in sublist]

    df = pd.DataFrame(results)
    df.to_csv('hotel_data.csv', index=False)

if __name__ == "__main__":
    scrape_conde()
