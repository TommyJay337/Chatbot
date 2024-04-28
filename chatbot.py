from openai import OpenAI
import os
from dotenv import load_dotenv
from pptx import Presentation
import json
from cassandra.cluster import Cluster
from cassandra.auth import PlainTextAuthProvider
from langchain.memory import CassandraChatMessageHistory, ConversationBufferMemory

load_dotenv()

# Open the JSON file for reading
with open("vector_database-token.json") as f:
    secrets = json.load(f)

auth_provider = PlainTextAuthProvider(username=secrets["clientId"], password=secrets["secret"])
cloud_config = {'secure_connect_bundle': 'secure-connect-vector-database.zip'}
cluster = Cluster(cloud=cloud_config, auth_provider=auth_provider)
session = cluster.connect()

ASTRA_DB_KEYSPACE = "search"
message_history = CassandraChatMessageHistory(
    session_id="session_identifier",  # This could be dynamically set per user or conversation
    session=session,
    keyspace=ASTRA_DB_KEYSPACE,
    ttl_seconds=3600  # Adjust as needed
)

cass_buff_memory = ConversationBufferMemory(
    memory_key="chat_history",
    chat_memory=message_history
)

# Optionally clear history if needed at the start of a new conversation
# message_history.clear()

def extract_text_from_multiple_pptx(file_list):
    all_text_content = []
    for pptx_file in file_list:
        prs = Presentation(pptx_file)
        for slide in prs.slides:
            for shape in slide.shapes:
                if shape.has_text_frame:
                    slide_text = ' '.join(paragraph.text for paragraph in shape.text_frame.paragraphs)
                    all_text_content.append(slide_text)
    return ' '.join(all_text_content)

pptx_files = ["Lectures/gbs.pptx", "Lectures/PPS.pptx", "Lectures/Alzheimer's 2024.pptx", "Lectures/ALS part 1.pptx", "Lectures/Cognitive perceptual and behavioural considerations 2024.pptx"  ]

# Extract text from all specified files
context_text = extract_text_from_multiple_pptx(pptx_files)
#print(context_text)

api_key = os.getenv("OPENAI_API_KEY")

'''
if api_key:
    print("API key is loaded.")
else:
    print("API key not found. Please check your environment variables.")
    exit(1)
'''

client = OpenAI(api_key=api_key)
print("The OpenAI client has been successfully initialized.")

# Assuming we maintain our history list
conversation_history = []

conversation_history = []

def chat_with_gpt(prompt, context_text, instruction):
    global conversation_history

    # Append user's prompt to history
    conversation_history.append({"role": "user", "content": prompt})

    # Prepare the chat messages including context and instructions as part of the system messages
    messages = [
        {"role": "system", "content": context_text},
        {"role": "system", "content": instruction}
    ] + conversation_history

    # Use the new interface to create chat completions
    response = client.chat.completions.create(
        model="gpt-3.5-turbo",
        messages=messages,
        temperature=1,
        max_tokens=256,
        top_p=1,
        frequency_penalty=0,
        presence_penalty=0
    )

    # Extract the bot's response and append it to the history
    bot_response = response.choices[0].message.content.strip()
    conversation_history.append({"role": "assistant", "content": bot_response})

    # Return the content of the assistant's message
    return bot_response


if __name__ == "__main__":
    instruction = f"You are a helpful tutor for a physiotherapy student studying neuro physiotherapy based on specific PowerPoint content. You will explain concepts, clarify doubts, and assist in the understanding of topics such as ALS, Alzheimer's disease, cognitive perceptual and behavioural considerations, GBS, and PPS. You will provide detailed explanations, generate flashcard-style quizzes with explanations for answers, and help with note-taking to compare and contrast the various conditions covered in the presentations. In addition to multiple choice questions, the tutor will also include case studies and short answer questions in quizzes to help students apply their knowledge in more practical scenarios. The tutor will ask for clarifications when needed and encourages the user to teach back the learned material to reinforce understanding. All explanations and materials generated will remain within the general scope of the course contents outlined in the attached document."
    while True:
        user_input = input("You: ")
        if user_input.lower() in ['exit', 'quit', 'q', 'bye']:
            break
        response = chat_with_gpt(user_input, context_text, instruction)
        print("ChatBot: ", response)

