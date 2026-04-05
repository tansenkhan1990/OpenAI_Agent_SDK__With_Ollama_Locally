import json
import os

DB_FILE = "tickets_db.json"

def init_db():
    if not os.path.exists(DB_FILE):
        with open(DB_FILE, "w") as f:
            json.dump([], f)

def read_tickets():
    init_db()
    with open(DB_FILE, "r") as f:
        return json.load(f)

def save_tickets(tickets):
    with open(DB_FILE, "w") as f:
        json.dump(tickets, f, indent=4)