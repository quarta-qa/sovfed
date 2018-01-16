from locators import *


class LoginPage(Browser):

    def username(self, value):
        self.set_text(LoginLocators.username, value, "Логин")

    def password(self, value):
        self.set_text(LoginLocators.password, value, "Пароль")

    def submit(self):
        self.click(LoginLocators.submit, "Войти")

    def get_username(self):
        return self.wait.element_appear(LoginLocators.username).text

    def get_password(self):
        return self.wait.element_appear(LoginLocators.password).text

    def set_focus_on_password(self):
        self.click(LoginLocators.password)

    def code(self, value):
        self.set_text(LoginLocators.code, value, "Временный код")

    def next(self):
        self.click(LoginLocators.next)

    def new_password(self, value):
        self.set_text(LoginLocators.new_password, value, "Новый пароль")

    def clear_new_password(self):
        self.wait.element_appear(LoginLocators.new_password).clear()

    def confirm_password(self, value):
        self.set_text(LoginLocators.confirm_password, value, "Подтверждение пароля")

    def finish(self):
        self.click(LoginLocators.finish)


class MainPage(Browser):

    def quit(self):
        self.click(MainLocators.quit)
