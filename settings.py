from pydantic import BaseSettings

class Settings(BaseSettings):
    openai_key: str
    telegram_token: str
    roles: dict[str, dict] =  {
            "teacher": {"role": "system", "content": "You are a language teacher"},
            "partner": {"role": "system", "content": "You are a conversation partner"},
        }
    model: str = "gpt-3.5-turbo"

    class Config:
        env_file = ".env"