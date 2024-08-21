import time
import requests
from dotenv import load_dotenv
import os
import tracemalloc
import asyncio
from discordwebhook import Discord
from datetime import datetime
from typing import Tuple
from typing import Optional

load_dotenv()

tracemalloc.start()

async def check_status(url) -> Tuple[Optional[str], Optional[int]]:
    try:
        response = requests.get(url, timeout=15)
        # Consider the URL functional if the response code is in the 200-299 range
        if 200 <= response.status_code < 300:
            return "up", response.status_code
        else:
            return "down", response.status_code
    except requests.Timeout:
        return "down", None
    except requests.ConnectionError:
        return "down", None


DISCORD_HOOK = os.getenv("DISCORD_WEBHOOK_URL")
URL = os.getenv("URL")


async def main() -> None:
    good_sent_previous = False
    bad_sent_previous = False
    while True:
        alert_bot = Discord(url=DISCORD_HOOK)
        url = URL
        current_time = datetime.now()
        formatted_time = current_time.strftime("%Y-%m-%d %H:%M:%S")
        status, code = await check_status(url)
        if status == "up" and not good_sent_previous and not bad_sent_previous:
            print(f"\U00002705{url} is up and functional (Status code: {code})")
            alert_bot.post(content=f"\U00002705 {url} is UP at {formatted_time} \U00002705")
            good_sent_previous = True
            bad_sent_previous = False
        elif status == "up" and good_sent_previous and not bad_sent_previous:
            print(f"{url} is up and functional (Status code: {code})")
            good_sent_previous = True
            bad_sent_previous = False
        elif status == "up" and not good_sent_previous and bad_sent_previous:
            print(f"\U00002705{url} is BACK UP at {formatted_time} \U00002705")
            alert_bot.post(content=f"\U00002705 {url} is BACK UP at {formatted_time}")
            good_sent_previous = True
            bad_sent_previous = False
        elif status == "down" and not good_sent_previous and not bad_sent_previous:
            print(f"\U0001F6A8{url} is down (Status code: {code})")
            alert_bot.post(content=f"\U0001F6A8 {url} is DOWN at {formatted_time} (Status code: {code})")
            good_sent_previous = False
            bad_sent_previous = True
        elif status == "down" and good_sent_previous and not bad_sent_previous:
            print(f"\U0001F6A8{url} is down (Status code: {code})")
            alert_bot.post(content=f"\U0001F6A8 {url} is DOWN at {formatted_time} (Status code: {code})")
            good_sent_previous = False
            bad_sent_previous = True
        elif status == "down" and not good_sent_previous and bad_sent_previous:
            print(f"{url} is down (Status code: {code})")
            good_sent_previous = False
            bad_sent_previous = True
        else:
            print("check bot health (code needs help)")
            alert_bot.post(content="check bot health (code needs help)")
        await asyncio.sleep(35)

asyncio.run(main())
