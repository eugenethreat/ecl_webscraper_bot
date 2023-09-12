# Webscraper_Bot

Retrieves all text from a webpage, compares with previous entry.

## Getting Started

### Virtual Environment

Downloading python packages is bloaty, so we use a virtual environment to keep things clean. Run these commands in the terminal.

```bash
python3 -m venv myenv
```

### YAML File

Create a yaml file in the same directory as the python file. The yaml file should look like this:

```yaml
# Email details
sender_email: "email@gmail.com"
sender_password: "app_password"
recipient_email: "hryoo2004@gmail.com"
```

The app password is separate from your normal google account password and is generated like so:

### App Password

Follow this link [here](https://support.google.com/accounts/answer/185833?visit_id=638301564797218479-244567776&p=InvalidSecondFactor&rd=1) to create a password that you can put in your yaml file.

### Run Job

Run the job by typing this in the terminal:

```bash
python3 main.py
```
