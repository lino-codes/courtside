import requests
from bs4 import BeautifulSoup
import pandas as pd
import re

from config import headers, day_names
from utils.df_utils import pandas_show_all

pandas_show_all()


def fetch_programmes(url: str, headers: dict) -> pd.DataFrame:
    """Fetch tennis programmes from the given URL and return as a DataFrame."""
    response = requests.get(url, headers=headers, verify=False)
    response.raise_for_status()

    soup = BeautifulSoup(response.text, "html.parser")
    programmes_div = soup.find("div", class_="programmes")
    cards = programmes_div.find_all("div", class_="card")

    programmes = []
    for card in cards:
        programme_info = {
            "title": card.find("div", class_="heading").get_text(strip=True),
            "location": card.find("div", class_="location").get_text(strip=True),
            "time": card.find("div", class_="time").get_text(strip=True),
            "coached": card.find("div", class_="coached").get_text(strip=True),
            "description": card.find("div", class_="description").get_text(strip=True),
            "status": card.find("div", class_="controls").get_text(strip=True),
        }
        programmes.append(programme_info)

    df = pd.DataFrame(programmes)
    return df[["title", "location", "time", "coached", "status"]]

def get_class_time_info(url_link):
    class_response = requests.get(url_link, headers=headers, verify=False)
    soup = BeautifulSoup(class_response.text, "html.parser")
    programmes_div = soup.find_all("div", class_="session available")
    programmes_dates = []
    # programmes_times = [] # NOTE: Time are being extracted from somewhere elsen
    pattern = re.compile(r'\b(?:' + '|'.join(day_names) + r')\b', re.IGNORECASE)
    for programme in programmes_div:
        programme_date = programme.find("div", class_="date").get_text(strip=True)
        programme_date = pattern.sub('', programme_date)
        programmes_dates.append(programme_date.strip())
        # programmes_times.append(programme.find('div', class_='time'))
    return programmes_dates
