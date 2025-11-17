from auto_booker import courtside_booker
from config import coverage


def run_courtside_booker():
    # venue_name = 'Bethnal Green Gardens'
    # venue_name = 'Ropemakers Field'
    venue_name = 'Victoria Park'
    booking_date = '2025-11-18'
    venue_name = coverage.get(venue_name).get('website_name')
    courtside_booker(venue_name, booking_date)


if __name__ == '__main__':
    run_courtside_booker()



