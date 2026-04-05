from agents import function_tool
import database as db
import uuid
import json

@function_tool
def create_record(issue: str, priority: str = "Medium") -> str:
    """Create a new support ticket. Use this when the user wants to 'add', 'create', or 'new'."""
    tickets = db.read_tickets()
    new_id = str(uuid.uuid4())[:6]
    new_entry = {"id": new_id, "issue": issue, "priority": priority, "state": "Open"}
    tickets.append(new_entry)
    db.save_tickets(tickets)
    return f"SUCCESS: Created ticket {new_id} for '{issue}'."

@function_tool
def list_records() -> str:
    """Show all tickets. Use this when the user says 'show', 'list', or 'view'."""
    tickets = db.read_tickets()
    if not tickets: return "The database is currently empty."
    return json.dumps(tickets, indent=2)

@function_tool
def update_record(ticket_id: str, new_status: str) -> str:
    """Change the status of a ticket. Use this for 'update', 'fix', or 'resolve'."""
    tickets = db.read_tickets()
    found = False
    for t in tickets:
        if t["id"] == ticket_id:
            t["state"] = new_status
            found = True
            break
    if not found:
        return f"ERROR: Ticket {ticket_id} not found."
    db.save_tickets(tickets)
    return f"SUCCESS: Ticket {ticket_id} updated to {new_status}."

@function_tool
def delete_record(ticket_id: str) -> str:
    """Delete a ticket. Use this for 'delete', 'remove', or 'cancel'."""
    tickets = db.read_tickets()
    updated = [t for t in tickets if t["id"] != ticket_id]
    if len(tickets) == len(updated):
        return f"ERROR: Ticket {ticket_id} not found."
    db.save_tickets(updated)
    return f"SUCCESS: Deleted ticket {ticket_id}."