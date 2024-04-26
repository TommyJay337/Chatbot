import openai
import os
from dotenv import load_dotenv
from pptx import Presentation

load_dotenv()

def extract_text_from_pptx(pptx_file):
    text_content = []
    prs = Presentation(pptx_file)
    for slide in prs.slides:
        for shape in slide.shapes:
            if shape.has_text_frame:
                text_content.append(' '.join(paragraph.text for paragraph in shape.text_frame.paragraphs))
    return ' '.join(text_content)

# Specify your PowerPoint file path
pptx_file = "Lectures//gbs.pptx"
context_text = extract_text_from_pptx(pptx_file)
#print(context_text)


api_key = os.getenv("OPENAI_API_KEY")
if api_key:
    print("API key is loaded.")
else:
    print("API key not found. Please check your environment variables.")
    exit(1)

client = openai.OpenAI(api_key=api_key)
print("The OpenAI client has been successfully initialized.")

def chat_with_gpt(prompt, context_text, instruction):
    response = client.chat.completions.create(
                model="gpt-3.5-turbo",
                messages=[
                {"role": "system", "content": context_text},  # Providing context
                {"role": "system", "content": instruction},  # Instruction prompt
                {"role": "user", "content": prompt}
                ],
                temperature=1,
                max_tokens=256,
                top_p=1,
                frequency_penalty=0,
                presence_penalty=0
            )
    return response.choices[0].message.content.strip()

if __name__ == "__main__":
    instruction = f"You are a helpful tutor for a physiotherapy neuro physiotherapy based on specific PowerPoint content. It will explain concepts, clarify doubts, and assist in the understanding of topics such as ALS, Alzheimer's disease, cognitive perceptual and behavioural considerations, GBS, and PPS. It provides detailed explanations, generates flashcard-style quizzes with explanations for answers, and helps with note-taking to compare and contrast the various conditions covered in the presentations. In addition to multiple choice questions, the tutor will now include case studies and short answer questions in quizzes to help students apply their knowledge in more practical scenarios. The tutor will ask for clarifications when needed and encourages the user to teach back the learned material to reinforce understanding. All explanations and materials generated will remain within the general scope of the course contents outlined in the attached document."
    while True:
        user_input = input("You: ")
        if user_input.lower() in ['exit', 'quit', 'q', 'bye']:
            break
        response = chat_with_gpt(user_input, context_text, instruction)
        print("ChatBot: ", response)

