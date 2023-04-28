from config import Config
from bot.helpers.translations.tr_en import EN


class Language(object):
    def __init__(self) -> None:
        self.select = EN()


lang = Language()
