from agents import function_tool

@function_tool
def check_inventory(item_name: str) -> str:
    """Check if a specific hardware item is in stock."""
    stock = {"laptop": 2, "monitor": 0, "keyboard": 15}
    count = stock.get(item_name.lower(), 0)
    return f"Stock for {item_name}: {count} units available."

@function_tool
def reset_user_password(username: str) -> str:
    """Trigger a secure password reset for a local user account."""
    return f"SUCCESS: A temporary password reset link has been sent to {username}."