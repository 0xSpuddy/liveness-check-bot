import time
import requests
from discordwebhook import Discord

DISCORD_WEBHOOK_URL = "https://discord.com/api/webhooks/<yourwebhookhere>"

def check_status(url, timeout=5):
    try:
        response = requests.get(url, timeout=timeout)
        # Consider the URL functional if the response code is in the 200-299 range
        if 200 <= response.status_code < 300:
            return "up", response.status_code
        else:
            return "down", response.status_code
    except requests.Timeout:
        return "timeout", None
    except requests.ConnectionError:
        return "error", None

def main():
    urls_to_check = [
        "https://url1.com...",
        "https://url2.com..."
    ]

    alert_bot = Discord(url=DISCORD_WEBHOOK_URL)
    while True:
        for url in urls_to_check:
            status, code = check_status(url)
            if status == "up":
                print(f"{url} is up and functional (Status code: {code})")
            elif status == "down":
                print(f"{url} is down (Status code: {code})")
                alert_bot.post(content=f"{url} is down (Status code: {code})")
            elif status == "timeout":
                print(f"{url} is down (Request timed out)")
                alert_bot.post(content=f"{url} is down (Request timed out)")
            elif status == "error":
                print(f"{url} is down (Connection error)")
                alert_bot.post(content=f"{url} is down (Connection error)")
        
        time.sleep(300)  # Wait for 10 seconds before checking again

if __name__ == "__main__":
    main()