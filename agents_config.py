# agents_config.py
from agents import Agent, ModelSettings, input_guardrail, GuardrailFunctionOutput
from tools import check_inventory, reset_user_password
from models import SupportTicket

@input_guardrail
async def safety_gate(context, agent, user_input):
    forbidden = ["delete database", "drop table"]
    if any(word in user_input.lower() for word in forbidden):
        return GuardrailFunctionOutput(tripwire_triggered=True, output_info="Security violation.")
    return GuardrailFunctionOutput(tripwire_triggered=False, output_info="Safe")

def setup_workforce(model):
    # We lower temperature to 0.0 for maximum structure reliability
    strict_settings = ModelSettings(max_tokens=800, temperature=0.0)

    # ✅ FIX 1: Use underscores in names to avoid naming warnings
    inventory_agent = Agent(
        name="inventory_clerk",
        instructions="You check stock levels. Use the check_inventory tool.",
        tools=[check_inventory],
        model=model,
        model_settings=strict_settings
    )

    it_agent = Agent(
        name="it_admin",
        instructions="You handle password resets using the reset_user_password tool.",
        tools=[reset_user_password],
        model=model,
        model_settings=strict_settings
    )

    manager = Agent(
        name="support_manager",
        # ✅ FIX 2: Explicitly tell the model it MUST finish with the schema
        instructions=(
            "Direct the user to 'inventory_clerk' or 'it_admin'. "
            "Once they provide info, you MUST summarize everything into the final SupportTicket format. "
            "Do not just chat; produce the required structured data."
        ),
        model=model,
        handoffs=[inventory_agent, it_agent],
        input_guardrails=[safety_gate],
        output_type=SupportTicket,
        model_settings=strict_settings
    )
    return manager