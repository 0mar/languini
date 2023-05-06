import openai
from settings import Settings, Role
from telegram import Update
from telegram.ext import (
    Updater,
    CommandHandler,
    MessageHandler,
    Filters,
    CallbackContext,
)
import logging
from collections import defaultdict

logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)


class LanguiniBot:
    def __init__(self, settings: Settings):
        self.settings = settings
        self.conversation_flow = defaultdict(list)

    def start(self, update: Update, context: CallbackContext) -> None:
        """Send a message when the command /start is issued."""
        name = update.message.from_user.first_name
        update.message.reply_text(
            f"Hi {name}! I am an AI-powered bot that helps you learn languages by engaging you in conversation and improving your understanding.\nStart a conversation in your favorite language."
        )

    def get_response(self, chat_id: int, role: Role) -> str:
        """Send text to OpenAI API and get response"""
        past_responses = [
            {"role": "user", "content": f"{role.prompt}: {content}"}
            for content in self.conversation_flow[chat_id][-role.memory :]
        ]
        response = openai.ChatCompletion.create(
            model=self.settings.model,
            messages=[
                role.system_prompt,
                *past_responses,
            ],
        )
        logger.debug(response)
        return response.choices[0].message.content

    def handle_message(self, update: Update, context: CallbackContext) -> None:
        """Handle incoming message"""
        message = update.message
        chat_id = message.chat_id
        text = message.text
        self.conversation_flow[chat_id].append(text)

        # Get response from OpenAI API
        for role in (self.settings.teacher, self.settings.partner):
            response = self.get_response(chat_id, role)
            # Send response to chat
            context.bot.send_message(chat_id=chat_id, text=response)

    def run(self) -> None:
        """Start the bot"""
        updater = Updater(self.settings.telegram_token)
        dispatcher = updater.dispatcher

        # Add handlers
        dispatcher.add_handler(CommandHandler("start", self.start))
        dispatcher.add_handler(
            MessageHandler(Filters.text & ~Filters.command, self.handle_message)
        )

        # Start the bot
        updater.start_polling()
        updater.idle()


if __name__ == "__main__":
    settings = Settings()
    openai.api_key = settings.openai_key
    languini = LanguiniBot(settings)
    languini.run()
