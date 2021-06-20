from src.menus.account.not_exists.keyboard import get_create_account_keyboard


class NotAvailableAccountsMenu:
    @staticmethod
    def get_text():
        return 'Нет доступных аккаунтов.'

    @staticmethod
    def get_keyboard():
        return get_create_account_keyboard()
