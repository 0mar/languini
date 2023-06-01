import openai
from settings import Settings, Role, Thread, modes
from telegram import Update
from telegram.ext import (
    Updater,
    CommandHandler,
    MessageHandler,
    Filters,
    CallbackContext,
)
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class LanguiniBot:
    def __init__(self, settings: Settings):
        self.settings = settings
        self.threads = {}
        self.roles = modes[settings.mode]

    def start(self, update: Update, context: CallbackContext) -> None:
        """Send a message when the command /start is issued."""
        name = update.message.from_user.first_name
        logger.info(f"New user subscribed: {name}")
        update.message.reply_text(
            f"Hi {name}! I am an AI-powered bot that helps you learn languages by engaging you in conversation and improving your understanding.\nStart a conversation in your favorite language."
        )

    def get_response(self, chat_id: int, role: Role) -> str:
        """Send text to OpenAI API and get response using the provided role"""
        messages = [
            role.system_prompt,
            *self.threads[(chat_id, role.name)].last(role.memory),
        ]
        response = openai.ChatCompletion.create(
            model=self.settings.model,
            messages=messages,
        )
        return response.choices[0].message.content

    def handle_message(self, update: Update, context: CallbackContext) -> None:
        """Handle incoming message and reply"""
        message = update.message
        chat_id = message.chat_id
        text = message.text
        logger.info(f"Received new message from {chat_id}")

        # Get response from OpenAI API
        for role in self.roles:
            if (key := (chat_id, role.name)) not in self.threads:
                self.threads[key] = Thread(chat_id, [])
            self.threads[key].add(f"{role.prompt}{text}")
            response = self.get_response(chat_id, role)
            logger.info(f"Received {role.name} reponse from openAI")
            # Send response to chat
            context.bot.send_message(chat_id=chat_id, text=response)
            logger.info(f"Sent {role.name} reponse from openAI")
            self.threads[key].add(response, from_self=False)

    def run(self) -> None:
        """Start the bot"""
        updater = Updater(self.settings.telegram_token)
        dispatcher = updater.dispatcher

        # Add handlers
        dispatcher.add_handler(CommandHandler("start", self.start))
        dispatcher.add_handler(
            MessageHandler(Filters.text & ~Filters.command, self.handle_message)
        )

        updater.start_polling()
        logger.info("Started bot")
        updater.idle()


if __name__ == "__main__":
    settings = Settings()
    openai.api_key = settings.openai_key
    languini = LanguiniBot(settings)
    languini.run()
