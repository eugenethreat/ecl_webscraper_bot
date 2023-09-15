import logging
import json
import csv
import requests
from bs4 import BeautifulSoup
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.application import MIMEApplication
import yaml

# Configure the logging module
logging.basicConfig(
    level=logging.INFO,  # Set the desired logging level (INFO, DEBUG, WARNING, ERROR, CRITICAL)
    format="%(asctime)s [%(levelname)s]: %(message)s",
    handlers=[
        logging.FileHandler("my_log_file.log"),  # Log to a file
        logging.StreamHandler()  # Log to the console
    ]
)

with open('secrets.yaml', 'r') as yaml_file:
    secrets = yaml.safe_load(yaml_file)

SENDER_EMAIL = secrets['sender_email']
SENDER_PASSWORD = secrets['sender_password']
RECIPIENT_EMAIL = secrets['recipient_email']

def main():
    # 1. Read the previous and current scan from json files
    previous_dict, current_dict = read_previous_and_current_scan_from_json()
    # 2a. Compare each corresponding key in the previous and current scan dictionaries, turn words into sets
    # 2b. Whatever the result, tabluate it to the csv file
    is_any_website_changed = write_to_report_file(previous_dict, current_dict)
    # 3. If there are any differences, send an email
    if (is_any_website_changed):
        logging.info('Sending email...')
        send_email(SENDER_EMAIL, SENDER_PASSWORD, RECIPIENT_EMAIL)
    else:
        logging.info('No changes detected.')

def read_previous_and_current_scan_from_json():
    with open('previous_scan.json') as f:
        previous_dict = json.load(f)
    with open('current_scan.json') as f:
        current_dict = json.load(f)
    return previous_dict, current_dict

def write_to_report_file(previous_dict, current_dict):
    with open('report.csv', 'w', newline='') as csvfile:
        fieldnames = ['name', 'url', 'is_changed']
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
        writer.writeheader()
        is_any_website_changed = False
        for url in previous_dict:
            is_website_changed = is_changed(previous_dict[url], current_dict[url])
            title = get_website_title(url)
            if is_website_changed and not is_any_website_changed:
                is_any_website_changed = True
            writer.writerow({'name': title, 'url': url, 'is_changed': is_website_changed})
            logging.info(f'Wrote {title} to report.csv.')
    logging.info('Wrote report to report.csv.')
    return is_any_website_changed

def get_website_title(url):
    response = requests.get(url)

    # Check if the request was successful (status code 200)
    if response.status_code == 200:
        # Parse the HTML content of the webpage using BeautifulSoup
        soup = BeautifulSoup(response.text, 'html.parser')

        # Find the title tag
        title_tag = soup.find('title')

        # Extract the text inside the title tag
        if title_tag:
            logging.debug(f'The title of the webpage is: {title_tag.get_text()}')
            return title_tag.get_text()
        else:
            logging.error('No title found on the webpage.')
            return 'No title'
    else:
        logging.error(f"Failed to retrieve the webpage. Status code: {response.status_code}")
        return 'No title'

def is_changed(previous_dict_entry_list, current_dict_entry_list):
    previous_set = set(previous_dict_entry_list)
    current_set = set(current_dict_entry_list)
    if previous_set == current_set:
        return False
    else:
        return True
    
def send_email(sender_email, sender_password, recipient_email):
    # Create a multipart email message
    message = MIMEMultipart()
    message["From"] = sender_email
    message["To"] = recipient_email
    message["Subject"] = "[Ballet Scout] Website change detected!"

    # Email body text
    body = "Please download file to see changes."
    message.attach(MIMEText(body, "plain"))

    # Attach a file (e.g., a text file)
    file_path = "report.csv"  # Replace with the path to the file you want to attach
    attachment = open(file_path, "rb")
    part = MIMEApplication(attachment.read(), Name="report.csv")
    attachment.close()
    part["Content-Disposition"] = f'attachment; filename="{file_path}"'
    message.attach(part)

    # Connect to the SMTP server (in this case, Gmail's SMTP server)
    with smtplib.SMTP("smtp.gmail.com", 587) as server:
        server.starttls()
        server.login(sender_email, sender_password)

        # Send the email
        server.sendmail(sender_email, recipient_email, message.as_string())

    print("Email with attachments sent successfully.")

if __name__ == '__main__':
    main()