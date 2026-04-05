import asyncio
import os
import json
from openai import AsyncOpenAI
from dotenv import load_dotenv
from agents import Runner, OpenAIChatCompletionsModel, set_tracing_disabled
from agents_config import setup_workforce
import database as db

load_dotenv()
set_tracing_disabled(True)

async def main():
    db.init_db()
    client = AsyncOpenAI(base_url=os.getenv("OLLAMA_BASE_URL"), api_key=os.getenv("OLLAMA_API_KEY"))
    local_model = OpenAIChatCompletionsModel(model=os.getenv("LOCAL_MODEL_NAME"), openai_client=client)
    manager = setup_workforce(local_model)

    print("\n--- 🤖 AI Database Manager Online ---")
    while True:
        query = input("\nUser: ").strip()
        if query.lower() in ["exit", "quit"]: break
        
        try:
            result = await Runner.run(manager, query)
            output = result.final_output
            
            if hasattr(output, 'summary'):
                print(f"\n📢 [ASSISTANT]: {output.summary}")
                if any(x in query.lower() for x in ["list", "show", "all"]):
                    print(json.dumps(db.read_tickets(), indent=4))
            else:
                print(f"\n[TEXT]: {output}")
        except Exception as e:
            print(f"Error: {e}")

if __name__ == "__main__":
    asyncio.run(main())