import asyncio
from openai import OpenAI
from agents.extensions.models.litellm_model import LitellmModel

from agents import Agent, Runner, function_tool, set_tracing_disabled
from dotenv import load_dotenv
import os


set_tracing_disabled(True)

# Load environment variables from .env.local first, then .env as fallback
load_dotenv('.env.local')
load_dotenv()  # Fallback to .env if .env.local doesn't exist

history = [
    {"role": "system", "content": "You are a helpful assistant."},
    {"role": "user", "content": "What is the capital of France?"}
]

client = OpenAI(
    base_url=os.getenv("OLLAMA_BASE_URL"),
    api_key=os.getenv("OLLAMA_API_KEY")
)

def get_response(message: str):
    history.append({"role": "user", "content": message})
    response = client.chat.completions.create(
        model=os.getenv("OLLAMA_MODEL"),
        messages=history
    )
    history.append({"role": "assistant", "content": response.choices[0].message.content})
    return response.choices[0].message.content

@function_tool
def get_weather(city: str):
    print(f"[debug] getting weather for {city}")
    return f"The weather in {city} is sunny."

async def main():
    agent = Agent(
        name="Assistant",
        instructions="You only respond in haikus.",
        model=LitellmModel(model=f"ollama/{os.getenv('OLLAMA_MODEL')}", api_key=os.getenv("OLLAMA_API_KEY")),
        tools=[],
    )
 
    result = await Runner.run(agent, "What's the weather in Tokyo?")
    print(result.final_output)

if __name__ == "__main__":
    asyncio.run(main())