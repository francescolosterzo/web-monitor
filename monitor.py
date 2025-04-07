import hashlib
import requests
import os
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
import argparse

# URL to monitor
URL = "https://www.ilpost.it/live/da-costa-a-costa/"

# File to store the last hash
HASH_FILE = "hashes/last_page_hash.txt"

def get_page_hash(url):

    response = requests.get(url)
    response.raise_for_status()  # Raise error if request failed
    page_content = response.text.encode('utf-8')

    return hashlib.sha256(page_content).hexdigest()

def read_last_hash(file_path):

    if not os.path.exists(file_path):
        return None
    with open(file_path, "r") as file:
        return file.read().strip()

def write_current_hash(file_path, hash_value):

    with open(file_path, "w") as file:
        file.write(hash_value)

def send_email(subject, body):

    smtp_server = "smtp.gmail.com"
    smtp_port = 587
    from_email = os.getenv("SMTP_LOGIN")
    to_email = os.getenv("TO_EMAIL")
    password = os.getenv("SMTP_PASSWORD")

    if from_email is None or to_email is None or password is None:
        print("SMTP credentials are not set in environment variables.")
        return

    msg = MIMEMultipart()
    msg['From'] = from_email
    msg['To'] = to_email
    msg['Subject'] = subject
    msg.attach(MIMEText(body, 'plain'))

    with smtplib.SMTP(smtp_server, smtp_port) as server:
        server.starttls()
        server.login(from_email, password)
        server.send_message(msg)

def main():

    parser = argparse.ArgumentParser(description="Monitor a webpage for changes.")
    parser.add_argument("--send_notification", action="store_true", help="Send notification if the page has changed.")
    parser.add_argument("--url", type=str, default=URL, help="URL to monitor.")
    args = parser.parse_args()

    url = args.url
    send_notification = args.send_notification
    
    current_hash = get_page_hash(url)
    last_hash = read_last_hash(HASH_FILE)

    if last_hash is None:
        print("No previous hash found. Saving current hash.")
        write_current_hash(HASH_FILE, current_hash)

    elif current_hash != last_hash:
        
        print("🔔 The webpage has changed since the last check!")
        write_current_hash(HASH_FILE, current_hash)

        if send_notification:
            send_email(
                subject="Webpage Updated!",
                body=f"The webpage at {url} has been updated."
            )
    else:
        print("✅ The webpage has not changed.")

if __name__ == "__main__":
    main()
