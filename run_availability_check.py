import datetime
from config import headers
from domain.court import fetch_court
from domain.lesson import fetch_programmes


def get_courtside_lessons():
    url = 'https://tennistowerhamlets.com/coaching'
    free_lessons = fetch_programmes(url, headers)
    filters = (free_lessons['status'] == 'Book now') & free_lessons['title'].str.contains('Advanced')
    free_lessons = free_lessons[filters]
    print(free_lessons)


def get_courtside_courts():
    venues = ['Ropemakers Field', 'Victoria Park']
    dates = [datetime.date(2025, 10, 18)]
    start_time = datetime.time(17, 00)
    end_time = datetime.time(21, 00)
    fetch_court(selected_venues=venues, selected_dates=dates, selected_times=start_time)




if __name__ == '__main__':
    # get_courtside_courts()
    get_courtside_lessons()