#!/usr/bin/env python3
"""
Charan's Reminder Bot - GitHub Actions version
Runs every 5 min via GitHub Actions cron. Sends message if task matches.
"""

import os
import requests
from datetime import datetime, timedelta
import pytz

BOT_TOKEN = os.environ["BOT_TOKEN"]
CHAT_ID   = os.environ["CHAT_ID"]
IST       = pytz.timezone("Asia/Kolkata")

WEEKDAY = {
    "04:30": "⏰ Wakeup!",
    "05:00": "🏋️ Gym  →  6:15",
    "06:15": "🚿 Getting ready  →  6:45",
    "06:45": "📖 Bagavad Gita  →  7:00",
    "07:00": "🍽️ Meals  →  7:30",
    "07:30": "🏫 College  →  4:30 PM",
    "16:30": "🍴 Freshup & eat  →  5:00 PM",
    "17:00": "😴 Power nap  →  5:15 PM",
    "17:15": "💼 Career  →  8:30 PM",
    "20:30": "🍽️ Dinner & rest  →  9:00 PM",
    "21:00": "📚 College work  →  10:00 PM",
}

SATURDAY = {
    "04:30": "⏰ Wakeup!",
    "05:00": "🏋️ Gym  →  6:15",
    "06:15": "🚿 Getting ready  →  6:45",
    "06:45": "📖 Bagavad Gita  →  7:00",
    "07:00": "🍽️ Meals  →  7:30",
    "07:30": "🏫 College  →  4:30 PM",
    "16:30": "🍴 Freshup & eat  →  5:00 PM",
    "17:00": "😴 Power nap  →  5:15 PM",
    "17:30": "🎵 Samgeetham class  →  7:00 PM",
    "19:00": "💼 Career  →  8:30 PM",
    "20:30": "🍽️ Dinner & rest  →  9:00 PM",
    "21:00": "📚 College work  →  10:00 PM",
}

SUNDAY = {
    "06:00": "⏰ Wakeup! Getting ready  →  6:30",
    "06:30": "🛕 Temple  →  7:00",
    "07:00": "📖 Bagavad Gita  →  7:20",
    "07:20": "🙏 Govinda Koti  →  8:00",
    "08:00": "🍳 Breakfast  →  8:30",
    "08:30": "📋 Plan the day  →  9:00",
    "09:00": "🎵 Samgeetham  →  10:00",
    "10:15": "📈 Upskilling  →  12:30 PM",
    "12:30": "🍽️ Lunch & rest  →  1:30 PM",
    "13:30": "📚 College work  →  3:00 PM",
    "15:00": "💼 Career  →  4:15 PM",
    "16:15": "😴 Power nap  →  4:30 PM",
    "16:30": "🍿 Snacks  →  5:00 PM",
    "17:00": "💼 Career  →  8:30 PM",
    "21:00": "📚 College work  →  10:00 PM",
}

SCHEDULE = {
    "Monday": WEEKDAY, "Tuesday": WEEKDAY,
    "Wednesday": WEEKDAY, "Thursday": WEEKDAY, "Friday": WEEKDAY,
    "Saturday": SATURDAY, "Sunday": SUNDAY,
}

def send(text):
    url = f"https://api.telegram.org/bot{BOT_TOKEN}/sendMessage"

    try:
        response = requests.post(
            url,
            json={
                "chat_id": CHAT_ID,
                "text": text
            },
            timeout=10
        )

        print("STATUS:", response.status_code)
        print("RESPONSE:", response.text)

        response.raise_for_status()

    except Exception as e:
        print("ERROR:", e)

def main():
    now = datetime.now(IST)

    print("Current IST:", now)

    send("✅ TEST MESSAGE FROM GITHUB ACTIONS")
    print("BOT TOKEN LENGTH:", len(BOT_TOKEN))
    print("CHAT ID:", CHAT_ID)


if __name__ == "__main__":
    main()
