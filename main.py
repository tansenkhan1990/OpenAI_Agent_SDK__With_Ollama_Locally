import asyncio
import os
import json
from openai import AsyncOpenAI
from dotenv import load_dotenv
from agents import Runner, OpenAIChatCompletionsModel, set_tracing_disabled
from agents_config import setup_workforce
import database as db

# Load variables from .env
load_dotenv()

# Set to False if you want to see the Agent's internal "thinking" and "handoffs"
set_tracing_disabled(True)

async def main():
    # 1. Initialize the JSON database file immediately
    db.init_db()
    
    # 2. Setup the Ollama Client
    client = AsyncOpenAI(
        base_url=os.getenv("OLLAMA_BASE_URL"), 
        api_key=os.getenv("OLLAMA_API_KEY")
    )
    
    # 3. Initialize the Model
    local_model = OpenAIChatCompletionsModel(
        model=os.getenv("LOCAL_MODEL_NAME"), 
        openai_client=client
    )
    
    # 4. Load the Workforce (Clerk + Researcher + Manager)
    manager = setup_workforce(local_model)

    print("\n--- 🤖 AI Agent: Web Search & Database [ONLINE] ---")
    print("Commands: 'Show tickets', 'Delete ticket 123', 'Search the web for...', 'exit'")
    
    while True:
        query = input("\nUser: ").strip()
        if not query: continue
        if query.lower() in ["exit", "quit"]: break
        
        try:
            # Run the Agentic Loop
            result = await Runner.run(manager, query)
            output = result.final_output
            
            # --- HANDLE RESPONSE ---
            
            # Case A: Structured Output (AgentResponse model)
            if hasattr(output, 'summary'):
                print(f"\n📢 [ASSISTANT]: {output.summary}")
                
                # Check for "Status" if your model provides it
                if hasattr(output, 'status'):
                    print(f"📊 [STATUS]: {output.status}")

                # 💡 AUTO-SHOW: If user did something to the data, show the result
                crud_actions = ["list", "show", "all", "delete", "create", "update", "wipe"]
                if any(word in query.lower() for word in crud_actions):
                    print("\n📋 CURRENT DATABASE:")
                    print(json.dumps(db.read_tickets(), indent=4))
            
            # Case B: Plain Text Output (Common during Web Search/Handoffs)
            else:
                print(f"\n📢 [RESEARCHER]: {output}")

        except Exception as e:
            print(f"⚠️ System Error: {e}")

    print("\n👋 System offline. Goodbye!")

if __name__ == "__main__":
    asyncio.run(main())