from src.menus.account.switcher.keyboard import get_switch_account_keyboard


class SwitchAccountMenu:
    def __init__(self, initiator):
        self.text = None

        if initiator == 'menu_my_accounts':
            self.__set_my_accounts_text()
        elif initiator == 'menu_distribution':
            self.__set_distribution_text()

    def __set_my_accounts_text(self):
        self.text = 'Выберите нужный вам аккаунт⬇️'

    def __set_distribution_text(self):
        self.text = 'Выберите нужный для рассылки аккаунт⬇️'

    def get_text(self):
        return self.text

    @staticmethod
    def get_keyboard():
        return get_switch_account_keyboard()
