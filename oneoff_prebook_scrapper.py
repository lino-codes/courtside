import logging
import requests
import urllib3
from bs4 import BeautifulSoup
from config import headers



urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)
logging.basicConfig(format="%(asctime)s - %(name)s - %(levelname)s - %(message)s", level=logging.INFO)
logger = logging.getLogger(__name__)


base_url = "https://tennistowerhamlets.com/book/coaching/"

""" 
Identify a starting id, and find all classes by incrementing the number by 1. 
Ending the loop by giving an ending id. 
"""
start_id = 12447
end_id = 12548
current_id = start_id

while current_id <  end_id:
    response = requests.get(f"{base_url}/{current_id}", headers=headers, verify=False)
    soup = BeautifulSoup(response.text, 'html.parser')
    h1 = soup.find('h1')
    if h1:
        if h1.get_text(strip=True) == 'Out!':
            logger.info(f"{base_url}/{current_id} is an invalid url.")
            break # NOTE: breaking the loop if url becomes invalid
        else:
            raw_class_name = h1.find_next_sibling('p').get_text()
            if 'advanced' in raw_class_name.lower():
                print(raw_class_name) # NOTE: printing the class name
                print(f"{base_url}/{current_id}") # NOTE: printing the url

    current_id += 1


