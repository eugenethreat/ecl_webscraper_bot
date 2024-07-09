import subprocess
import logging
import os

# Configure the logging module
logging.basicConfig(
    level=logging.DEBUG,  # Set the desired logging level (INFO, DEBUG, WARNING, ERROR, CRITICAL)
    format="%(asctime)s [%(levelname)s]: %(message)s",
    handlers=[
        logging.FileHandler("my_log_file.log"),  # Log to a file
        logging.StreamHandler()  # Log to the console
    ]
)

def main():
    virtualenv_path = os.getcwd() + "\my_venv"
    logging.debug(virtualenv_path)
    # List of Python scripts to run
    scripts_to_run = [
        "create_previous_scan.py",
        "create_current_scan.py",
        "compare_previous_to_current_and_generate_report.py",
        "replace_previous_scan_with_current_scan.py"
    ]

    activate_script = os.path.join(virtualenv_path, 'Scripts' if os.name == 'nt' else 'bin', 'activate')
    logging.debug(activate_script)
    subprocess.run([activate_script], shell=True)
    # Command to install packages from requirements.txt
    command = "pip install -r requirements.txt"

    # Run the command using subprocess
    try:
        subprocess.run(command, shell=True, check=True)
    except subprocess.CalledProcessError as e:
        logging.error(f"Error running the command: {e}")
    else:
        logging.info("Packages have been successfully installed from requirements.txt")

    err = False
    # Iterate through the list and run each script
    for script in scripts_to_run:
        try:
            subprocess.run(["python", script], check=True)
        except subprocess.CalledProcessError as e:
            err = True
            logging.error(f"Error running {script}: {e}")
        else:
            logging.info(f"{script} has been successfully executed.")
    if(err):
        logging.info("Execution finished. Some errors occured.")
    else:
        logging.info("All scripts have been successfully executed!")

if __name__ == '__main__':
    main()