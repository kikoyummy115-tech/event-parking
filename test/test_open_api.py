from openai import OpenAI, AuthenticationError
import os

print("start.....")
client = OpenAI(
    api_key=os.getenv("OPENAI_API_KEY")
)


print("Not working")
print(client)