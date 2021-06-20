from src.menus.main.keyboard import get_main_keyboard


class MainMenu:
    @staticmethod
    def get_text():
        return "Добро пожаловать! Перед тем как начать рассылку, проверьте ваши аккаунты👇"

    @staticmethod
    def get_keyboard():
        return get_main_keyboard()
