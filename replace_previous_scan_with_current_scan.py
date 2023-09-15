import logging
import json

# Configure the logging module
logging.basicConfig(
    level=logging.INFO,  # Set the desired logging level (INFO, DEBUG, WARNING, ERROR, CRITICAL)
    format="%(asctime)s [%(levelname)s]: %(message)s",
    handlers=[
        logging.FileHandler("my_log_file.log"),  # Log to a file
        logging.StreamHandler()  # Log to the console
    ]
)

# Define the paths to the source and target JSON files
source_json_file = 'current_scan.json'
target_json_file = 'previous_scan.json'

# Read the content of the source JSON file
with open(source_json_file, 'r') as source_file:
    source_data = json.load(source_file)

# Write the content of the source JSON file into the target JSON file
with open(target_json_file, 'w') as target_file:
    json.dump(source_data, target_file)

logging.info(f'Contents of {source_json_file} have been copied to {target_json_file}.')