from infobip import send_message
from openai import OpenAI
from dotenv import load_dotenv
import os

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

if __name__ == "__main__":
    agent_response =get_response("What is the capital of France?")
    print(agent_response)
    send_message("16462203228", "This is a preregistered test message from Infobip. Enjoy your free trial!")