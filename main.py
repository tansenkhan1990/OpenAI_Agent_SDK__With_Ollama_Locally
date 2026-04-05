import asyncio
import os
import json
from openai import AsyncOpenAI
from dotenv import load_dotenv
from agents import Runner, OpenAIChatCompletionsModel, set_tracing_disabled
from agents_config import setup_workforce
import database as db  # 1. Import your database helper

load_dotenv()
set_tracing_disabled(True) 

async def main():
    # 2. FORCE INITIALIZE: Create the JSON file immediately on startup
    db.init_db()
    print("📦 Database initialized (tickets_db.json is ready)")

    # Connect to Ollama
    client = AsyncOpenAI(
        base_url=os.getenv("OLLAMA_BASE_URL"),
        api_key=os.getenv("OLLAMA_API_KEY")
    )
    
    local_model = OpenAIChatCompletionsModel(
        model=os.getenv("LOCAL_MODEL_NAME", "llama3.2:3b"),
        openai_client=client
    )

    manager = setup_workforce(local_model)

    print("\n--- 🤖 Natural Language Database System [READY] ---")
    print("Commands: 'Create ticket for...', 'List all', 'Delete ticket [ID]', 'exit'")
    
    while True:
        try:
            query = input("\nUser: ").strip()
            if not query: continue
            if query.lower() in ["exit", "quit"]: break

            # Run the Agent Loop
            result = await Runner.run(manager, query)
            output = result.final_output
            
            # 3. SMART DISPLAY: Show summary and the actual data if listing
            if hasattr(output, 'summary'):
                print(f"\n📢 [ASSISTANT]: {output.summary}")
                print(f"📊 [STATUS]: {output.status}")
                
                # Check if the user asked for a list/show command
                list_keywords = ["show", "list", "all", "tickets", "records"]
                if any(word in query.lower() for word in list_keywords):
                    current_tickets = db.read_tickets()
                    if current_tickets:
                        print("\n📋 --- CURRENT DATABASE RECORDS ---")
                        # Print as a pretty JSON string
                        print(json.dumps(current_tickets, indent=4))
                        print("----------------------------------")
                    else:
                        print("\n📂 Database is currently empty.")
            else:
                # Fallback for plain string responses
                print(f"\n[SYSTEM]: {output}")

        except KeyboardInterrupt:
            break
        except Exception as e:
            print(f"\n⚠️ System Error: {e}")

    print("\n👋 System offline. Goodbye!")

if __name__ == "__main__":
    asyncio.run(main())