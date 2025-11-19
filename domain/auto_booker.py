import requests
import re
import pandas as pd
import logging
from bs4 import BeautifulSoup
from playwright.sync_api import sync_playwright

from config import headers
from domain.utils import parse_time

logging.basicConfig(
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s", level=logging.INFO
)

logger = logging.getLogger(__name__)

def court_booker(venue, booking_date):
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=False)
        page = browser.new_page()
        # Navigate to the booking page
        page.goto(f'https://tennistowerhamlets.com/book/courts/{venue}/{booking_date}#book')

        page.wait_for_selector('input.bookable')
        inputs = page.query_selector_all('input.bookable')
        for input_element in inputs:
            bookable_value = input_element.get_attribute('value')
            print(bookable_value)



def lesson_booker(class_level='Advanced', exclude_days=None, full_days=None, lesson_start=17):
    url = 'https://tennistowerhamlets.com/coaching'
    response = requests.get(url, headers=headers, verify=False)
    response.raise_for_status()

    soup = BeautifulSoup(response.text, "html.parser")
    programmes_div = soup.find("div", class_="programmes")
    cards = programmes_div.find_all("div", class_="card")
    programmes_info = []
    url_link = ''
    for card in cards:
        book_button = card.find("button", class_="primary")
        if book_button is not None: # NOTE: Only includes ones that are available for booking
            title = card.find("div", class_="heading").get_text(strip=True)
            if class_level.lower() in title.lower(): # NOTE: Only includes ones that are advanced
                duration = f"{card.find("div", class_="time").get_text(strip=True)}"
                weekday_match = re.match(r"([A-Za-z]{3})", duration)
                times = re.findall(r"\d{1,2}:\d{2}(?:am|pm)", duration, re.IGNORECASE)
                div = card.find("div", class_="controls")

                if div:
                    url_link = f"https://tennistowerhamlets.com/{div.find('form')['action']}"

                weekday = weekday_match.group(1) if weekday_match else None
                start_time = round(parse_time(times[0] if len(times) > 0 else None) * 2) / 2
                end_time = round(parse_time(times[1] if len(times) > 0 else None) * 2) / 2


                if weekday in exclude_days:
                    continue
                if weekday in full_days:
                    logger.info(f'Class Found: {title}')
                    programme_info = {"title": title,
                                      "location": card.find("div", class_="location").get_text(strip=True),
                                      "day": weekday,
                                      "start_time": start_time,
                                      "end_time": end_time,
                                      'url': url_link,
                                      }
                    programmes_info.append(programme_info)
                elif start_time > lesson_start:
                    logger.info(f'Class Found: {title}')
                    programme_info = {"title": title,
                                      "location": card.find("div", class_="location").get_text(strip=True),
                                      "day": weekday,
                                      "start_time": start_time,
                                      "end_time": end_time,
                                      'url': url_link
                                      }
                    programmes_info.append(programme_info)
    return pd.DataFrame(programmes_info)



