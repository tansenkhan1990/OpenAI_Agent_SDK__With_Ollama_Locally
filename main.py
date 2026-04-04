import asyncio
import os
from openai import AsyncOpenAI
from dotenv import load_dotenv
from agents import Runner, OpenAIChatCompletionsModel, set_tracing_disabled
from agents_config import setup_workforce

load_dotenv()
set_tracing_disabled(True) # Set to False to see the internal agent 'thoughts'

async def run_local_system():
    # 1. Initialize Local OpenAI-Compatible Client
    client = AsyncOpenAI(
        base_url=os.getenv("OLLAMA_BASE_URL"),
        api_key=os.getenv("OLLAMA_API_KEY"),
    )

    # 2. Define the local model
    local_llama = OpenAIChatCompletionsModel(
        model=os.getenv("LOCAL_MODEL_NAME"),
        openai_client=client
    )

    # 3. Build the workforce
    manager = setup_workforce(local_llama)

    print(f"--- 🛠️ Local Agent System Online ({os.getenv('LOCAL_MODEL_NAME')}) ---")
    user_query = "I can't log in as 'tansenkhan'. Also, do we have any laptops in the warehouse?"

    try:
        # 4. Execute the loop
        result = await Runner.run(manager, user_query)
        ticket = result.final_output
        
        # ✅ FIX 3: Check if 'ticket' is actually the Pydantic object or just text
        if hasattr(ticket, 'ticket_id'):
            print("\n✅ [FINAL SYSTEM REPORT]")
            print(f"Ticket ID: {ticket.ticket_id}")
            print(f"Category:  {ticket.issue_category}")
            print(f"Summary:   {ticket.summary}")
            print(f"Status:    {ticket.status}")
        else:
            # If the model failed to follow the schema, we show the text instead
            print("\n⚠️ [PARTIAL SUCCESS - TEXT ONLY]")
            print(f"The model responded with text instead of a form: \n{ticket}")

    except Exception as e:
        print(f"\n❌ CRITICAL SYSTEM ERROR: {str(e)}")

if __name__ == "__main__":
    asyncio.run(run_local_system())