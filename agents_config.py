from agents import Agent, ModelSettings
from tools import create_record, list_records, manage_tickets_by_state
from models import AgentResponse

def setup_workforce(model):
    # Temperature 0.0 prevents the AI from 'hallucinating' data
    settings = ModelSettings(max_tokens=1000, temperature=0.0)

    clerk = Agent(
        name="database_clerk",
        instructions=(
            "You are a ticket administrator. Use 'manage_tickets_by_state' for "
            "natural language batch requests like 'delete resolved' or 'set all open to closed'."
        ),
        tools=[create_record, list_records, manage_tickets_by_state],
        model=model,
        model_settings=settings
    )

    manager = Agent(
        name="support_manager",
        instructions="Analyze user intent and hand off to the database_clerk.",
        handoffs=[clerk],
        output_type=AgentResponse,
        model=model,
        model_settings=settings
    )
    return manager