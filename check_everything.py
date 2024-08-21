import time
import requests
from dotenv import load_dotenv
import os
import tracemalloc
import asyncio
from discordwebhook import Discord
from datetime import datetime

load_dotenv()

tracemalloc.start()

DISCORD_HOOK = os.getenv("DISCORD_WEBHOOK_URL")
URL = os.getenv("URL")


async def check_status(url, timeout=5):
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

async def main() -> None:
    alert_bot = Discord(url=DISCORD_HOOK)
    while True:
        url = URL
        status, code = await check_status(url)
        current_time = datetime.now()
        formatted_time = current_time.strftime("%Y-%m-%d %H:%M:%S")
        if status == "up":
            print(f"{url} is up and functional (Status code: {code})")
        elif status == "down":
            print(f"{url} is down (Status code: {code})")
            alert_bot.post(content=f"{url} is down at {formatted_time} (Status code: {code})")
        elif status == "timeout":
            print(f"{url} is down (Request timed out)")
            alert_bot.post(content=f"{url} is down at {formatted_time} (Request timed out)")
        elif status == "error":
            print(f"{url} is down (Connection error)")
            alert_bot.post(content=f"{url} is down at {formatted_time} (Connection error)")
        
        await asyncio.sleep(10)

asyncio.run(main())
