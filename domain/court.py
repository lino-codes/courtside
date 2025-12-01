from bs4 import BeautifulSoup
import requests
import pandas as pd
import datetime
from config import headers, coverage
from utils.df_utils import pandas_show_all, split_courts
from utils.time_utils import parse_time, time_to_int

pandas_show_all()

main_url = 'https://tennistowerhamlets.com'



def fetch_court(selected_venues, selected_dates, worker_schedule):
    url = 'https://tennistowerhamlets.com/book/courts/'
    select_YDM = [dt.strftime('%Y-%m-%d') for dt in selected_dates]
    venues = {k: coverage[k] for k in selected_venues if k in coverage}
    if worker_schedule:
        work_start = 17
    else:
        work_start = 0
    bookable = {}
    for venue_name, details in venues.items():
        response = requests.get(f'{url}{details.get("website_name")}#book', headers=headers)
        soup = BeautifulSoup(response.text, "html.parser")
        target_div = soup.find("div", class_="day-picker")
        # get all <a> tags inside it
        links = target_div.find_all("a")
        # extract hrefs
        hrefs = [a["href"] for a in links if a.has_attr("href")]
        venues[venue_name]['booking_links'] = hrefs

    for venue_name, details in venues.items():
        latest_court_time = 24
        booking_links = [x for x in details["booking_links"] if any(sub in x for sub in select_YDM)]
        for link in booking_links:
            url = f'{main_url}{link}'
            link_date = datetime.datetime.strptime(link.split('#')[0].rstrip('/').split('/')[-1], '%Y-%m-%d')
            if link_date.weekday() < 5 and latest_court_time < work_start:
                continue
            try:
                print(f'url: {url}')
                tables = pd.read_html(url)  # returns list of DataFrames
                df = tables[0]

                expanded = df[1].apply(split_courts).apply(pd.Series)
                df = pd.concat([df, expanded], axis=1)
            except ValueError as e:
                print(e)
                df = pd.DataFrame()

            df['time'] = df[0].apply(time_to_int)
            df = df.drop(columns=[0, 1])
            latest_court_time = df.time.max()
            if link_date.weekday() < 5 and latest_court_time < work_start:
                continue
            else:
                result_dict = {}
                if link_date.weekday() < 5:
                    df = df[df['time'] > work_start]
                for idx, row in df.iterrows():
                    pound_columns = [col for col in df.columns if col != 'time' and '£' in str(row[col])]
                    if pound_columns:
                        result_dict[row['time']] = pound_columns

                print(venue_name)
                print(result_dict)
                venue_details = {url: result_dict}
                if result_dict:
                    bookable.setdefault(link_date.date(), []).append(venue_details)

    return bookable



