from agents import function_tool
import database as db
import uuid
import json

@function_tool
def create_record(issue: str, priority: str = "Medium") -> str:
    """Create a new ticket. Use for: 'add', 'new', 'create'."""
    tickets = db.read_tickets()
    new_id = str(uuid.uuid4())[:6]
    tickets.append({"id": new_id, "issue": issue, "priority": priority, "state": "Open"})
    db.save_tickets(tickets)
    return f"Created ticket {new_id}."

@function_tool
def list_records() -> str:
    """List all tickets. Use for: 'show', 'view', 'list'."""
    return json.dumps(db.read_tickets(), indent=2)

@function_tool
def manage_tickets_by_state(action: str, target_state: str, new_state: str = None) -> str:
    """
    Batch actions on tickets. 
    Action: 'delete' or 'update'. 
    Target_state: e.g. 'Resolved', 'Open'.
    """
    tickets = db.read_tickets()
    initial_len = len(tickets)
    
    if action == "delete":
        updated = [t for t in tickets if t["state"].lower() != target_state.lower()]
        db.save_tickets(updated)
        return f"Deleted {initial_len - len(updated)} tickets."
    
    if action == "update" and new_state:
        count = 0
        for t in tickets:
            if t["state"].lower() == target_state.lower():
                t["state"] = new_state
                count += 1
        db.save_tickets(tickets)
        return f"Updated {count} tickets to {new_state}."
    return "No changes made."