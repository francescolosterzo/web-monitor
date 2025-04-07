from utils.utils import get_page_hash, read_last_hash, write_current_hash
from utils.utils import send_email
import argparse

# URL to monitor
URL = "https://www.ilpost.it/live/da-costa-a-costa/"

# File to store the last hash
HASH_FILE = "hashes/last_page_hash.txt"

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
