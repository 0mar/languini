from pydantic import BaseSettings
from pydantic.dataclasses import dataclass


@dataclass
class Role:
    name: str
    prompt: str
    context: str
    memory: int

    @property
    def system_prompt(self) -> dict[str, dict]:
        return {"role": "system", "content": self.context}


class Settings(BaseSettings):
    openai_key: str
    telegram_token: str
    teacher: Role = Role(
        "teacher",
        "Correct the following sentence and explain any errors",
        "You are a language teacher",
        1,
    )
    partner: Role = Role(
        "partner",
        "Provide a response to the following sentence",
        "You are a conversation partner",
        2,
    )

    model: str = "gpt-3.5-turbo"

    class Config:
        env_file = ".env"
