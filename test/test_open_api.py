from openai import OpenAI, AuthenticationError
import os
from dotenv import load_dotenv

load_dotenv()

print("start.....")
client = OpenAI(
    api_key=os.getenv("OPENAI_API_KEY")
)


print(client)