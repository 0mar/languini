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


@dataclass
class Thread:
    chat_id: int
    lines: list[dict[str, str]]

    def add(self, text: str, from_self: bool = True):
        if from_self:
            name = "user"
        else:
            name = "assistant"
        self.lines.append({"role": name, "content": text})

    def last(self, n: int = 3):
        return self.lines[-n:]


class Settings(BaseSettings):
    openai_key: str
    telegram_token: str
    teacher: Role = Role(
        "teacher",
        "",
        "You are a language teacher that corrects sentences and explains any errors",
        1,
    )
    partner: Role = Role(
        "partner",
        "",
        "You are a conversation partner that responds to the previous sentence, keeping the conversation going",
        3,
    )

    model: str = "gpt-3.5-turbo"

    class Config:
        env_file = ".env"
