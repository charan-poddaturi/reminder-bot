#!/usr/bin/env python3
"""
Charan's Schedule Reminder Bot
Deploy on Railway. Set env vars: BOT_TOKEN, CHAT_ID
"""

import os
import time
import requests
from datetime import datetime
import pytz

# ─── CONFIG ───────────────────────────────────────────────────────────────────
BOT_TOKEN = os.environ.get("BOT_TOKEN", "8722143494:AAGe4ODGUQB_nQavOTIuv1w5lGizg5zxE5Y")
CHAT_ID   = os.environ.get("CHAT_ID", "7465929735")   
IST       = pytz.timezone("Asia/Kolkata")

# ─── WEEKLY SCHEDULE (24hr IST) ───────────────────────────────────────────────

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
    "Monday":    WEEKDAY,
    "Tuesday":   WEEKDAY,
    "Wednesday": WEEKDAY,
    "Thursday":  WEEKDAY,
    "Friday":    WEEKDAY,
    "Saturday":  SATURDAY,
    "Sunday":    SUNDAY,
}

# ─── TELEGRAM ─────────────────────────────────────────────────────────────────

def send_message(text):
    url = f"https://api.telegram.org/bot{BOT_TOKEN}/sendMessage"
    try:
        r = requests.post(url, json={"chat_id": CHAT_ID, "text": text}, timeout=10)
        r.raise_for_status()
        print(f"[SENT] {text}")
    except Exception as e:
        print(f"[ERROR] {e}")

# ─── MAIN LOOP ────────────────────────────────────────────────────────────────

def run():
    if not CHAT_ID:
        print("[ERROR] CHAT_ID env variable not set! Check Railway variables.")
        return

    print(f"[BOT] Started. CHAT_ID={CHAT_ID}. Checking every 30s.")
    send_message("🤖 Reminder bot is online! You'll get reminders on schedule.")

    last_sent = None
    while True:
        now     = datetime.now(IST)
        day     = now.strftime("%A")
        hhmm    = now.strftime("%H:%M")
        uid     = f"{day}_{hhmm}"

        task = SCHEDULE.get(day, {}).get(hhmm)
        if task and uid != last_sent:
            send_message(f"🔔 {day} {hhmm}\n\n{task}")
            last_sent = uid

        time.sleep(30)

if __name__ == "__main__":
    run()
