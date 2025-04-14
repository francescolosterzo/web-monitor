from utils.utils import get_page_hash, load_hashes, write_hashes
from utils.utils import send_email
import argparse


## TODO:
## - in order for it to work properly in github actions the hash file should be committed and pushed every time is updated (or just every time?)

# File to store the last hash
HASH_FILE = "hashes/hashes.json"

def main():

    parser = argparse.ArgumentParser(description="Monitor a webpage for changes.")
    parser.add_argument("--send_notification", action="store_true", help="Send notification if the page has changed.")
    parser.add_argument("--url", type=str, default='httpshttps://www.google.com', help="URL to monitor.")
    args = parser.parse_args()

    url = args.url
    send_notification = args.send_notification
    
    current_hash = get_page_hash(url)

    hashes = load_hashes(HASH_FILE)
    last_hash = hashes.get(url, None)

    if last_hash is None:
        print("No previous hash found. Saving current hash.")
        hashes[url] = current_hash
        write_hashes(HASH_FILE, hashes)

        if send_notification:
            send_email(
                subject="New webpage being tracked!",
                body=f"The webpage at {url} has been added to the tracking."
            )

    elif current_hash != last_hash:

        print("🔔 The webpage has changed since the last check!")
        hashes[url] = current_hash
        write_hashes(HASH_FILE, hashes)

        if send_notification:
            send_email(
                subject="Webpage Updated!",
                body=f"The webpage at {url} has been updated."
            )
    else:
        print("✅ The webpage has not changed.")

if __name__ == "__main__":
    main()
