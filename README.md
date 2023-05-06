# LanguiniBot

Repository for a Telegram bot that engages you in conversations and helps you learn a language

## Generative AI Caveat
This project relies on OpenAI's GPT 3.5 model, meaning that there is no guarantee that any generated text is correct, useful or appropriate. Always keep this in mind when using this or any other generative-AI-based product.

## Install

The minimal Python version is 3.10. For other dependencies, refer to `pyproject.toml`.
Dependencies are managed with [poetry](https://python-poetry.org/docs/).

Before installing, ensure a functioning poetry installation. Then, install the project.
```bash
poetry install
```
## Run
To run, you need an [OpenAI API key](https://platform.openai.com/account/api-keys) and an [Telegram bot](https://core.telegram.org/bots/tutorial). Both of these can be obtained for free (OpenAI provides $5 to trial the service) and within less than 5 minutes.
### Set environment variables

Place the API key and the token in a file called `.env` at the root of the repository:

```bash
OPENAI_KEY=<api-key>
TELEGRAM_TOKEN=<bot-token>
```

## Usage

To run the bot, run
```bash
poetry run python main.py
```