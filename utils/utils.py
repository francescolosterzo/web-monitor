import hashlib
import requests
import os
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

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