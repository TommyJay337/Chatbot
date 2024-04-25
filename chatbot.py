from openai import OpenAI
import os
from dotenv import load_dotenv

load_dotenv()

api_key = os.getenv("OPENAI_API_KEY")
if api_key:
    print("API key is loaded.")
else:
    print("API key not found. Please check your environment variables.")

client = OpenAI(api_key=api_key)
if client:
    print("The OpenAI client has been successfully initialized.")
else:
    print("Failed to initialize the OpenAI client.")

chat_completion = client.chat.completions.create(
  model="gpt-3.5-turbo",
  messages=[
    {
      "role": "user",
      "content": "This is a test"
    }
  ],
  temperature=1,
  max_tokens=256,
  top_p=1,
  frequency_penalty=0,
  presence_penalty=0
)


'''
def chat_with_gpt(prompt):
    response = client.chat.completions.create(
        model="gpt-3.5-turbo",
        messages = [{"role": "system", "content": prompt}]
    )

    return response.choices[0].message.content.strip()

if __name__ == "__main__":
    while True:
        user_input = input("You: ")
        if user_input.lower() in ['exit', 'quit', 'q', 'bye']:
            break
        response = chat_with_gpt(user_input)
        print("ChatBot:", response)
'''
        