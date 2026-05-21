#!/usr/bin/env python3

"""
Charan's Reminder Bot
Reliable GitHub Actions version
"""

import os
import json
import requests
from datetime import datetime
import pytz

# =========================
# TELEGRAM CONFIG
# =========================

BOT_TOKEN = os.environ["BOT_TOKEN"]
CHAT_ID = os.environ["CHAT_ID"]

IST = pytz.timezone("Asia/Kolkata")

# =========================
# DUPLICATE TRACKING FILE
# =========================

LAST_SENT_FILE = "last_sent.json"

# =========================
# SCHEDULES
# =========================

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
    "Monday": WEEKDAY,
    "Tuesday": WEEKDAY,
    "Wednesday": WEEKDAY,
    "Thursday": WEEKDAY,
    "Friday": WEEKDAY,
    "Saturday": SATURDAY,
    "Sunday": SUNDAY,
}

# =========================
# LOAD LAST SENT
# =========================

def load_last_sent():

    if not os.path.exists(LAST_SENT_FILE):
        return {}

    try:
        with open(LAST_SENT_FILE, "r") as f:
            return json.load(f)

    except:
        return {}

# =========================
# SAVE LAST SENT
# =========================

def save_last_sent(data):

    with open(LAST_SENT_FILE, "w") as f:
        json.dump(data, f)

# =========================
# SEND TELEGRAM MESSAGE
# =========================

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

# =========================
# MAIN LOGIC
# =========================

def main():

    now = datetime.now(IST)

    day = now.strftime("%A")

    print("\n==========================")
    print("Current IST:", now)
    print("Today:", day)

    today_schedule = SCHEDULE.get(day, {})

    last_sent = load_last_sent()

    today_date = now.strftime("%Y-%m-%d")

    for task_time, task_name in today_schedule.items():

        # Convert schedule time
        task_dt = datetime.strptime(task_time, "%H:%M")

        scheduled_dt = now.replace(
            hour=task_dt.hour,
            minute=task_dt.minute,
            second=0,
            microsecond=0
        )

        # Minutes remaining
        minutes_left = (
            scheduled_dt - now
        ).total_seconds() / 60

        print(f"\nChecking task:")
        print(f"Task: {task_name}")
        print(f"Starts at: {task_time}")
        print(f"Minutes left: {minutes_left:.2f}")

        # Send reminder within next 30 mins
        if 0 <= minutes_left <= 30:

            unique_key = f"{today_date}_{task_time}"

            # Prevent duplicate reminders
            if last_sent.get(unique_key):
                print("Already sent.")
                continue

            msg = (
                f"🔔 Upcoming Task Reminder\n\n"
                f"📅 {day}\n"
                f"⏰ Starts at: {task_time} IST\n\n"
                f"{task_name}"
            )

            print("Sending reminder...")

            send(msg)

            last_sent[unique_key] = True

            save_last_sent(last_sent)

            print("Reminder sent successfully.")

            return

    print("\nNo reminder to send now.")

# =========================

if __name__ == "__main__":
    main()
