import json
import os
import firebase_admin
from firebase_admin import credentials, firestore
from datetime import datetime

# Load credentials from secret
cred_json = json.loads(os.environ["FIREBASE_SERVICE_ACCOUNT"])
cred = credentials.Certificate(cred_json)
firebase_admin.initialize_app(cred)

db = firestore.client()

# Get today’s info
today = datetime.utcnow()
weekday_name = today.strftime("%A")  # e.g., "Sunday"
today_str = today.strftime("%Y-%m-%d")  # e.g., "2025-06-29"

# Fetch normal and special events
normal = db.collection("normalEvents").stream()
special = db.collection("specialEvents").stream()

events = []

# Normal events: check if today’s weekday is in 'days'
for doc in normal:
    data = doc.to_dict()
    if weekday_name in data.get("days", []):
        events.append({
            "type": "normal",
            "title": data.get("title", "Untitled"),
            "time": data.get("time", "??:??"),
            "tone": data.get("tone", "-"),
            "delay": data.get("delay", 0)
        })

# Special events: check if date matches today
for doc in special:
    data = doc.to_dict()
    if data.get("date") == today_str:
        events.append({
            "type": "special",
            "description": data.get("description", "Untitled"),
            "time": data.get("time", "??:??"),
            "tone": data.get("tone", "-"),
            "delay": data.get("delay", 0)
        })

with open("events.json", "w") as f:
    json.dump(events, f, indent=2)

print(f"Saved {len(events)} event(s) for {today_str}")
