from src.views.switcher.keyboards import get_switch_account_keyboard


class SwitchAccountMenu:
    def __init__(self, state):
        self.text = None
        self.state = state

        action = self.state.get('action')

        if action == 'menu_my_accounts':
            self.__set_my_accounts_text()
        elif action == 'menu_distribution':
            self.__set_distribution_text()

    def __set_my_accounts_text(self):
        self.text = 'Выберите нужный вам аккаунт⬇️'

    def __set_distribution_text(self):
        self.text = 'Выберите нужный для рассылки аккаунт⬇️'

    def get_text(self):
        return self.text

    def get_keyboard(self):
        return get_switch_account_keyboard(self.state)
