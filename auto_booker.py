
from playwright.sync_api import sync_playwright


def courtside_booker(venue, booking_date):
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





