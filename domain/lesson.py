import requests
from bs4 import BeautifulSoup
import pandas as pd

from utils.df_utils import pandas_show_all

pandas_show_all()


def fetch_programmes(url: str, headers: dict) -> pd.DataFrame:
    """Fetch tennis programmes from the given URL and return as a DataFrame."""
    response = requests.get(url, headers=headers)
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