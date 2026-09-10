from openai import OpenAI

client = OpenAI()

def get_bot_response(user_input):
    response = client.chat.completions.create(
        model="gpt-5-nano",
        messages=[
            {"role": "system", "content": "You are a helpful assistant chatbot."},
            {"role": "user", "content": user_input}
        ]
    )

    return response.choices[0].message.content.strip()


# Test it
user_text = input("You: ")
print("Bot:", get_bot_response(user_text))

### CODIO SOLUTION END