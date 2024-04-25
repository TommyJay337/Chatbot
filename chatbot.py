import openai
import os
from dotenv import load_dotenv
import time

load_dotenv()

api_key = os.getenv("OPENAI_API_KEY")
if api_key:
    print("API key is loaded.")
else:
    print("API key not found. Please check your environment variables.")
    exit(1)

client = openai.OpenAI(api_key=api_key)
print("The OpenAI client has been successfully initialized.")

def make_api_call():
    retry_delay = 20  # Initial backoff delay in seconds
    while True:
        try:
            chat_completion = client.chat.completions.create(
                model="gpt-3.5-turbo",
                messages=[{"role": "user", "content": "This is a test"}],
                temperature=1,
                max_tokens=256,
                top_p=1,
                frequency_penalty=0,
                presence_penalty=0
            )
            print("Response:", chat_completion.choices[0].message['content'])
            break
        except openai.RateLimitError as e:
            print("Rate limit exceeded, retrying in", retry_delay, "seconds...")
            print(e)
            time.sleep(retry_delay)
            retry_delay *= 2  # Exponential backoff
        except Exception as e:
            print("An unexpected error occurred:", e)
            break

make_api_call()


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
        