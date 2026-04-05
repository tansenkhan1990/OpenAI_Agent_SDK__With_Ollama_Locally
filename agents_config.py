from agents import Agent, ModelSettings
from tools import create_record, list_records, update_record, delete_record
from models import AgentResponse

def setup_workforce(model):
    # Temperature 0.0 is best for database operations to prevent 'hallucinated' IDs
    settings = ModelSettings(max_tokens=1000, temperature=0.0)

    db_clerk = Agent(
        name="database_clerk",
        instructions=(
            "You are a database administrator. "
            "1. To ADD: use create_record. "
            "2. To VIEW: use list_records. "
            "3. To CHANGE/UPDATE: use update_record. "
            "4. To REMOVE: use delete_record. "
            "Always confirm the Ticket ID before performing updates or deletes."
        ),
        tools=[create_record, list_records, update_record, delete_record],
        model=model,
        model_settings=settings
    )

    manager = Agent(
        name="support_manager",
        instructions="Triage the user's request and hand off to the database_clerk.",
        model=model,
        handoffs=[db_clerk],
        output_type=AgentResponse,
        model_settings=settings
    )
    return manager