from asyncj import SyncJson


class LoaderLexicon:
    BASE_PATH = "../src/lexicon/{language}.json"

    def __init__(self, language: str = "ru") -> None:
        self.language = language
        self.js = SyncJson(self.BASE_PATH.format(language=self.language))

    def load_messages(self) -> dict[str, str]:

        return self.js.read()["messages"]

    def load_keyboard(self) -> dict[str, str]:
        return self.js.read()["keyboard"]

    def load_names(self) -> list[str]:
        return self.js.read()["names"]

    def load_prompts(self) -> dict[str, str]:
        return self.js.read()["prompts"]



