import tkinter.scrolledtext as tks  # creates a scrollable text window
from datetime import datetime
from tkinter import *

# Create the main application window
baseWindow = Tk()
baseWindow.title("The Simple Bot")
baseWindow.geometry("500x250")

# Create the chat window (scrollable text area)
chatWindow = tks.ScrolledText(baseWindow, font="Arial", wrap=WORD)

# Configure tags for message alignment
chatWindow.tag_configure("tag-left", justify="left")   # bot messages
chatWindow.tag_configure("tag-right", justify="right") # user messages

# Disable the chat window so the user can't type directly into it
chatWindow.config(state=DISABLED)

# Create the user entry box
userEntryBox = Text(baseWindow, bd=1, bg="white", width=38, font="Arial")

# Create the send button
# The command is not connected yet — we will attach it to a function next
sendButton = Button(
    baseWindow,
    font=("Verdana", 12, "bold"),
    text="Send",
    bg="#fd94b4",
    activebackground="#ff467e",
    fg="#ffffff",
    # command=send
)

# Place widgets on the window (Tkinter uses x/y coordinates here)
chatWindow.place(x=1, y=1, height=200, width=500)
userEntryBox.place(x=3, y=202, height=27)
sendButton.place(x=430, y=200)

# Start the GUI event loop
# This keeps the window open and listens for user actions (like button clicks)
baseWindow.mainloop()

def create_and_insert_user_frame(user_input):
    userFrame = Frame(chatWindow, bg="#d0ffff")
    Label(
        userFrame,
        text=user_input,
        font=("Arial", 11),
        bg="#d0ffff"
    ).grid(row=0, column=0, sticky="w", padx=5, pady=5)

    Label(
        userFrame,
        text=datetime.now().strftime("%H:%M"),
        font=("Arial", 7),
        bg="#d0ffff"
    ).grid(row=1, column=0, sticky="w")

    chatWindow.insert("end", "\n ", "tag-right")
    chatWindow.window_create("end", window=userFrame)


def create_and_insert_bot_frame(bot_response):
    botFrame = Frame(chatWindow, bg="#ffffd0")
    Label(
        botFrame,
        text=bot_response,
        font=("Arial", 11),
        bg="#ffffd0",
        wraplength=400,
        justify="left"
    ).grid(row=0, column=0, sticky="w", padx=5, pady=5)

    Label(
        botFrame,
        text=datetime.now().strftime("%H:%M"),
        font=("Arial", 7),
        bg="#ffffd0"
    ).grid(row=1, column=0, sticky="w")

    chatWindow.insert("end", "\n ", "tag-left")
    chatWindow.window_create("end", window=botFrame)
    chatWindow.insert(END, "\n\n")

def send(event=None):
    chatWindow.config(state=NORMAL)

    user_input = userEntryBox.get("1.0", "end-2c").strip()
    if not user_input:
        chatWindow.config(state=DISABLED)
        return

    # Show the user's message immediately
    create_and_insert_user_frame(user_input)

    # Clear the input box right away
    userEntryBox.delete("1.0", "end")
    chatWindow.see("end")

    # Insert a temporary typing message and remember where it starts/ends
    typing_start = chatWindow.index("end-1c")
    create_and_insert_bot_frame("Bot is typing...")
    typing_end = chatWindow.index("end-1c")

    chatWindow.config(state=DISABLED)

    # Run the API call in the background so the GUI doesn't freeze
    def worker():
        try:
            bot_response = get_bot_response(user_input)
        except Exception:
            bot_response = "Something went wrong while generating a response."

        # Update the GUI safely from the main Tkinter thread
        def update_ui():
            chatWindow.config(state=NORMAL)

            # Remove the temporary typing message
            chatWindow.delete(typing_start, typing_end)

            # Insert the real response
            create_and_insert_bot_frame(bot_response)

            chatWindow.config(state=DISABLED)
            chatWindow.see("end")

        baseWindow.after(0, update_ui)

    threading.Thread(target=worker, daemon=True).start()

# Pressing Enter will also send the message
baseWindow.bind("<Return>", send)

def get_bot_response(user_input):
    response = client.chat.completions.create(
        model="gpt-5-nano",
        messages=[
            {"role": "system", "content": "You are a helpful assistant chatbot."},
            {"role": "user", "content": user_input}
        ]
    )

    return response.choices[0].message.content.strip()

from openai import OpenAI

client = OpenAI()


