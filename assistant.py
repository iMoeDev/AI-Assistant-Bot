import requests
import json
from telegram import Update
from telegram.ext import Updater, CommandHandler, MessageHandler, CallbackContext

url = "http://localhost:11434/api/generate"
headers = {'Content-Type': 'application/json'}
conversation_history = []

# Function to generate response using LLM 
def generate_response(prompt):
    conversation_history.append(prompt)
    full_prompt = "\n".join(conversation_history)
    data = {
        "model": "<model name>",
        "stream": False,
        "prompt": full_prompt,
    }
    try:
        response = requests.post(url, headers=headers, data=json.dumps(data))
        response.raise_for_status()  
        data = response.json()
        actual_response = data["response"]
        conversation_history.append(actual_response)
        return actual_response
    except requests.RequestException as e:
        print("Error:", e)
        return "An error occurred while communicating with the server"

# Function to handle start command
def start(update: Update, context: CallbackContext) -> None:
    update.message.reply_text("Hey, I'm your new assistant")

# Function to handle messages
def handle_message(update: Update, context: CallbackContext) -> None:
    user_input = update.message.text
    # check if the message is not a command
    if not user_input.startswith('/'):  
        bot_response = generate_response(user_input)
        update.message.reply_text(bot_response)

def main():
    # Create the Updater and pass it your bot's token.
    updater = Updater("<pass your token here>")

    # Get the dispatcher to register handlers
    dispatcher = updater.dispatcher

    # Register command handlers
    dispatcher.add_handler(CommandHandler("start", start))

    dispatcher.add_handler(MessageHandler(None, handle_message))

    updater.start_polling()

    # Run the bot until you press Ctrl-C
    updater.idle()

if __name__ == '__main__':
    main()
