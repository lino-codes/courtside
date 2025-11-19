from auto_booker import court_booker, lesson_booker
from config import coverage


def run_court_booker():
    # venue_name = 'Bethnal Green Gardens'
    # venue_name = 'Ropemakers Field'
    venue_name = 'Victoria Park'
    booking_date = '2025-11-19'

    venue_name = coverage.get(venue_name).get('website_name')
    court_booker(venue_name, booking_date)

def run_lesson_booker():
    class_level = 'Advanced'
    lesson_booker(class_level=class_level, exclude_days=[], full_days=['Sat', 'Sun'], start_time=17)



if __name__ == '__main__':
    run_lesson_booker()




