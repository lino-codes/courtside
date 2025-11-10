from bs4 import BeautifulSoup
import requests
import pandas as pd
import datetime
from config import headers, coverage
from utils.df_utils import pandas_show_all, split_courts

pandas_show_all()

main_url = 'https://tennistowerhamlets.com'



def fetch_court(selected_venues, selected_dates, selected_times):
    url = 'https://tennistowerhamlets.com/book/courts/'
    select_YDM = [dt.strftime('%Y-%m-%d') for dt in selected_dates]
    venues = {k: coverage[k] for k in selected_venues if k in coverage}

    for venue_name, details in venues.items():
        response = requests.get(f'{url}{details.get("website_name")}#book', headers=headers)
        soup = BeautifulSoup(response.text, "html.parser")
        target_div = soup.find("div", class_="day-picker")
        # get all <a> tags inside it
        links = target_div.find_all("a")
        # extract hrefs
        hrefs = [a["href"] for a in links if a.has_attr("href")]
        venues[venue_name]['booking_links'] = hrefs

    print(venues)
    for venue_name, details in venues.items():
        booking_links = [x for x in details["booking_links"] if any(sub in x for sub in select_YDM)]
        print(booking_links)
        for link in booking_links:
            print('LINK')
            print(link)
            url = f'{main_url}{link}'
            print(f'The url: {url}')
            try:
                tables = pd.read_html(url)  # returns list of DataFrames
                df = tables[0]

                expanded = df[1].apply(split_courts).apply(pd.Series)
                df = pd.concat([df, expanded], axis=1)
            except ValueError as e:
                print(e)
                df = pd.DataFrame()

            print(df)

    return None



