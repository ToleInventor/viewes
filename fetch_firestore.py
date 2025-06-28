import json
import os
import firebase_admin
from firebase_admin import credentials, firestore

# Load credentials from secret
cred_json = json.loads(os.environ["FIREBASE_SERVICE_ACCOUNT"])
cred = credentials.Certificate(cred_json)
firebase_admin.initialize_app(cred)

db = firestore.client()

# Fetch normal and special events
normal = db.collection("normalEvents").stream()
special = db.collection("specialEvents").stream()

events = []

for doc in normal:
    data = doc.to_dict()
    events.append({
        "type": "normal",
        "title": data.get("title", "Untitled"),
        "time": data.get("time", "??:??"),
        "tone": data.get("tone", "-"),
        "delay": data.get("delay", 0)
    })

for doc in special:
    data = doc.to_dict()
    events.append({
        "type": "special",
        "description": data.get("description", "Untitled"),
        "time": data.get("time", "??:??"),
        "tone": data.get("tone", "-"),
        "delay": data.get("delay", 0)
    })

with open("events.json", "w") as f:
    json.dump(events, f, indent=2)
