import json
import os

DB_FILE = "tickets_db.json"

def init_db():
    """Create the JSON file if it doesn't exist."""
    if not os.path.exists(DB_FILE):
        with open(DB_FILE, "w") as f:
            json.dump([], f)

def read_tickets():
    """Read all records from the JSON file."""
    init_db()
    with open(DB_FILE, "r") as f:
        return json.load(f)

def save_tickets(tickets):
    """Overwrite the JSON file with new data."""
    with open(DB_FILE, "w") as f:
        json.dump(tickets, f, indent=4)