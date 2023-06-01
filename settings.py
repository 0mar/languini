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


modes: dict[str, Role] = {
    "sensei": [
        Role(
            "teacher",
            "",
            "You are a language teacher. Respond to every sentence with 1: listing and explaining all errors and 2: a reply to the sentence",
            3,
        )
    ],
    "chaperonne": [
        Role(
            "teacher",
            "Refrain from answering and only provide language corrections to the following sentence: ",
            "You are a language teacher that only focuses on correcting sentences and explaining any errors",
            1,
        ),
        Role(
            "partner",
            "",
            "You are a conversation partner that responds to the previous sentence, keeping the conversation going",
            3,
        ),
    ],
    "intense": [
        Role(
            "teacher",
            "",
            "You are a teacher that analyses the grammar of the sentence extensively",
            1,
        ),
        Role(
            "partner",
            "Provide an answer that rhymes with: ",
            "You are a conversation partner that stimulates the conversation",
            3,
        ),
    ],
}


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
    model: str = "gpt-3.5-turbo"
    mode: str = "chaperonne"  # 'sensei', 'chaperonne', or 'intense'

    class Config:
        env_file = ".env"
