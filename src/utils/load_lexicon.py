import os
from asyncj import SyncJson


class LoaderLexicon:
    BASE_PATH = "../src/lexicon"

    def __init__(self, language: str = "ru") -> None:
        self.language = language.lower()
        self.js = SyncJson(f"{self.BASE_PATH}/{self.language}.json")

    def load_messages(self) -> dict[str, str]:

        return self.js.read()["messages"]

    def load_keyboard(self) -> dict[str, str]:
        return self.js.read()["keyboard"]

    def load_names(self) -> list[str]:
        return self.js.read()["names"]

    def load_prompts(self) -> dict[str, str]:
        return self.js.read()["prompts"]

    @property
    def get_languages(self) -> list[str]:
        return [
            f.replace(".json", "").upper()
            for f in os.listdir(self.BASE_PATH)
            if f.endswith(".json")
        ]
