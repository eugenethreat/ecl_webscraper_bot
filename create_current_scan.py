import requests
import logging
import json
from bs4 import BeautifulSoup

# Configure the logging module
logging.basicConfig(
    level=logging.INFO,  # Set the desired logging level (INFO, DEBUG, WARNING, ERROR, CRITICAL)
    format="%(asctime)s [%(levelname)s]: %(message)s",
    handlers=[
        logging.FileHandler("my_log_file.log"),  # Log to a file
        logging.StreamHandler()  # Log to the console
    ]
)

CURRENT_SCAN_FILE_NAME = "current_scan.json"
SITES_TO_SCAN_FILE_NAME = "sites_to_scan.txt"

def main():
    url_list = read_sites_to_scan_from_file()
    write_current_scan_entry_to_json(url_list)
    
def read_sites_to_scan_from_file():
    with open(SITES_TO_SCAN_FILE_NAME) as f:
        sites_to_scan = f.readlines()
    sites_to_scan = [x.strip() for x in sites_to_scan]
    return sites_to_scan

def write_current_scan_entry_to_json(url_list):
    current_scan_entry_dict = {}

    for url in url_list:
        text = get_webpage_text(url)
        current_scan_entry_dict[url] = text
    json_data = json.dumps(current_scan_entry_dict)

    with open(CURRENT_SCAN_FILE_NAME, 'w') as f:
        f.write(json_data)
    logging.info(f'Wrote current scan entry to {CURRENT_SCAN_FILE_NAME}.')

def get_webpage_text(url):
    # Send an HTTP GET request to the URL
    response = requests.get(url)

    # Check if the request was successful (status code 200)
    if response.status_code == 200:
        # Parse the HTML content of the webpage using BeautifulSoup
        soup = BeautifulSoup(response.text, 'html.parser')

        # Find all text elements in the HTML
        all_text = soup.get_text()
        all_text = all_text.replace("\n", " ")
        all_text_list = all_text.split(" ")
        all_text_clean = [word.strip() for word in all_text_list if word != ""]

        # Print or process the extracted text
        return all_text_clean
    else:
        logging.error(f"Failed to retrieve the webpage. Status code: {response.status_code}")
        return None

if __name__ == '__main__':
    main()