from pages import *
from links import Links


class TestSuite:

    # driver = webdriver.Chrome("driver\\chromedriver.exe")
    driver = webdriver.Ie("driver\\IEDriverServer.exe")

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

    def test_education_planning(self):
        LoginPage(self.driver).login(username="Буслаева Людмила Александровна", password="Буслаева4505")

        page = MainPage(self.driver)
        page.show_menu()
        page.menu.click_by_text("Планирование обучения")

        page = EducationPlanningPage(self.driver)
        page.click_by_text("Личный проект")
        page.personal_project.year("2017")
        # проверка возможности добавления
        page.personal_project.click_by_value("Добавить")
        page.personal_project.education_direction("Государственная бюджетная политика")
        page.personal_project.content_types("Иное")
        page.personal_project.other_content_type("123")
        page.personal_project.rationale("1233444")
        page.personal_project.click_by_value("Сохранить")
        # проверка возможности редактирования/удаления
        page.personal_project.select_new_plan()
        page.personal_project.click_by_value("Редактировать")
        page.personal_project.other_content_type("321")
        page.personal_project.click_by_value("Сохранить")
        page.personal_project.select_new_plan()
        page.personal_project.click_by_value("Удалить")
        # делаем повторно проект и утверждаем его
        page.personal_project.scroll_to_top()
        page.personal_project.click_by_value("Добавить")
        page.personal_project.education_direction("Государственная бюджетная политика")
        page.personal_project.content_types("Иное")
        page.personal_project.other_content_type("123")
        page.personal_project.rationale("1233444")
        page.personal_project.click_by_value("Сохранить")
        page.personal_project.select_new_plan()
        page.personal_project.click_by_value("Утвердить")
        # выходим из текущего сеанса
        MainPage(self.driver).quit()
        # заходим на вторую учетку
        LoginPage(self.driver).login(username="Литвинцева Ирина Юрьевна", password="Литвинцева4509")
        page = MainPage(self.driver)
        page.show_menu()
        page.menu.administration()
        page.menu.click_by_text("Управление пользователями")
        # ищем нужного сотрудника и меняем ему права
        page = UsersManagementPage(self.driver)
        page.search("Буслаева Людмила Александровна")
        page.personal_card.notification_management_rule(True)
        page.personal_card.click_by_text("Сохранить")
        # выходим из текущего сеанса
        MainPage(self.driver).quit()
        # заходим на изначальную учетку
        LoginPage(self.driver).login(username="Буслаева Людмила Александровна", password="Буслаева4505")
        page = MainPage(self.driver)
        page.show_menu()
        page.menu.click_by_text("Планирование обучения")

        page = EducationPlanningPage(self.driver)
        page.department_project.click_by_text("Проект отдела")
        page.department_project.year("2017")
        page.department_project.select_new_plan()
        page.department_project.click_by_value("Редактировать")
        page.personal_project.other_content_type("4444")
        page.personal_project.save()
        page.department_project.select_new_plan()
        page.department_project.click_by_value("Печать")
        # добавляем проект первому сотруднику
        page.department_project.click_by_value("Добавить")
        page.personal_project.user("Азарова Наталия Владимировна")
        page.personal_project.education_direction("Государственная бюджетная политика")
        page.personal_project.content_types("Иное")
        page.personal_project.other_content_type("123")
        page.personal_project.rationale("1233444")
        page.personal_project.click_by_value("Сохранить")
        # добавляем проект второму сотруднику
        page.department_project.click_by_value("Добавить")
        page.personal_project.user("Казберова Дина Сергеевна")
        page.personal_project.education_direction("Государственная конкурентная политика")
        page.personal_project.content_types("Иное")
        page.personal_project.other_content_type("123")
        page.personal_project.rationale("1233444")
        page.personal_project.click_by_value("Сохранить")
        # выбираем несколько записей и проверяем состояние кнопок
        page.department_project.select_plan_by_user("Азарова Наталия Владимировна")
        page.department_project.select_plan_by_user("Казберова Дина Сергеевна")
        page.department_project.scroll_to_top()
        assert page.department_project.buttons_state() == [True, False, True, True, True], \
            "Состояние кнопок отличается от указанных в тесте"
        # выбираем все и отправляем на печать
        page.department_project.select_all_plans()
        page.department_project.click_by_value("Печать")
        # проверяем удаление. закомментировано потому что сценарий плохой, не учитывает все возможные варианты
        # page.department_project.select_new_plan()
        # page.department_project.click_by_value("Удалить")
        # проверяем утверждение
        page.department_project.select_new_plan()
        page.department_project.click_by_value("Утвердить")
        # выходим из текущего сеанса
        MainPage(self.driver).quit()
        # заходим на вторую учетку
        LoginPage(self.driver).login(username="Литвинцева Ирина Юрьевна", password="Литвинцева4509")
        page = MainPage(self.driver)
        page.show_menu()
        page.menu.administration()
        page.menu.click_by_text("Управление пользователями")
        # ищем нужного сотрудника и меняем ему права
        page = UsersManagementPage(self.driver)
        page.search("Буслаева Людмила Александровна")
        page.personal_card.plan_management_rule(True)
        page.personal_card.click_by_text("Сохранить")
