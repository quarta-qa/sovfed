from pages import *
from links import Links


class TestSuite:

    driver = webdriver.Chrome("driver\\chromedriver.exe")
    # driver = webdriver.Ie("driver\\IEDriverServer.exe")

    @classmethod
    def setup_class(cls):
        cls.driver.maximize_window()

    @classmethod
    def teardown_class(cls):
        cls.driver.quit()

    def test_incorrect_login_and_password(self):
        page = LoginPage(self.driver)
        page.go_to(Links.login_page)
        page.username("incorrect_login")
        page.password("incorrect_password")
        page.submit()
        page.wait.text_appear("Неверно указан логин или пароль.")
        assert page.get_password() == ""

    def test_correct_login_and_password(self):
        page = LoginPage(self.driver)
        page.go_to(Links.login_page)
        page.username("Литвинцева Ирина Юрьевна")
        page.password("Литвинцева4509")
        page.submit()
        page.wait.text_appear("Здравствуйте, Литвинцева Ирина Юрьевна!")
        MainPage(self.driver).quit()
        assert page.wait.text_appear("Войти")

    def test_registration(self):
        page = LoginPage(self.driver)
        page.go_to(Links.login_page)
        page.click_by_text("Регистрация")
        page.code("4509371236")
        page.next()
        page.new_password("1")
        page.confirm_password("")
        page.finish()
        assert page.get_alert_text() == "Пароли не совпадают"
        page.accept_alert()
        page.clear_new_password()
        page.confirm_password("1")
        page.finish()
        assert page.get_alert_text() == "Не введен пароль"
        page.accept_alert()
        page.new_password("1")
        page.finish()
        assert page.get_alert_text() == "Пароль слишком простой"
        page.accept_alert()
        page.new_password("Литвинцева1")
        page.confirm_password("Литвинцева1")
        page.finish()
        page.submit()
        page.wait.text_appear("Здравствуйте, Литвинцева Ирина Юрьевна!")

    def test_restore_password(self):
        page = LoginPage(self.driver)
        page.go_to(Links.login_page)
        page.click_by_text("Регистрация")
        page.code("4509371236")
        page.next()
        page.new_password("Литвинцева4509")
        page.confirm_password("Литвинцева4509")
        page.finish()
        page.submit()
        page.wait.text_appear("Здравствуйте, Литвинцева Ирина Юрьевна!")
