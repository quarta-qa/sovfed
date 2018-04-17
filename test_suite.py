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

    def te1st_incorrect_login_and_password(self):
        page = LoginPage(self.driver)
        page.go_to(Links.login_page)
        page.username("incorrect_login")
        page.password("incorrect_password")
        page.submit()
        page.wait.text_appear("Неверно указан логин или пароль.")
        assert page.get_password() == ""

    def te1st_correct_login_and_password(self):
        page = LoginPage(self.driver)
        page.go_to(Links.login_page)
        page.username("Литвинцева Ирина Юрьевна")
        page.password("Литвинцева4509")
        page.submit()
        page.wait.text_appear("Здравствуйте, Литвинцева Ирина Юрьевна!")
        MainPage(self.driver).quit()
        assert page.wait.text_appear("Войти")

    def te1st_registration(self):
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

    def te1st_restore_password(self):
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

    def te1st_education_planning(self):
        """
        Планирование обучения
        """
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

    def test_time_sheet(self):
        """
        Табель - Учет рабочего времени
        """
        LoginPage(self.driver).login(username="Литвинцева Ирина Юрьевна", password="Литвинцева4509")

        page = MainPage(self.driver)
        page.show_menu()
        page.menu.click_by_text("Табель")

        page = TimeSheetPage(self.driver)
        page.year("2015")
        page.month("Июнь")
        page.department("Отдел гражданского права")
        assert page.select_reasons("Багмет Лилия Андреевна")

    def test_time_sheet_setting_positions(self):
        """
        Настройка позиций табеля
        """
        day = datetime.datetime.today().day
        if (0 < day < 10) or (15 < day < 24):
            # заходим под администратором и снимаем все чекбоксы
            LoginPage(self.driver).login(username="Литвинцева Ирина Юрьевна", password="Литвинцева4509")

            page = MainPage(self.driver)
            page.show_menu()
            page.menu.click_by_text("Табель")

            page = TimeSheetPage(self.driver)
            page.click_by_text("Настройка позиций табеля")
            page.setting.click_by_text("Настроить позиции табеля")
            page.setting.set_all_positions(False)

            # выходим из текущего сеанса
            MainPage(self.driver).quit()
            # заходим на другого пользователя и проверяем
            LoginPage(self.driver).login(username="Ломакина Ольга Вячеславовна", password="Ломакина4509")

            page = MainPage(self.driver)
            page.show_menu()
            page.menu.click_by_text("Табель")

            page = TimeSheetPage(self.driver)
            # запоминаем результат проверки
            check = page.is_there_any_option("Анохина Марина Николаевна")

            # выходим из текущего сеанса
            MainPage(self.driver).quit()
            # заходим снова под администратором и проставляем чекбоксы обратно
            LoginPage(self.driver).login(username="Литвинцева Ирина Юрьевна", password="Литвинцева4509")

            page = MainPage(self.driver)
            page.show_menu()
            page.menu.click_by_text("Табель")

            page = TimeSheetPage(self.driver)
            page.click_by_text("Настройка позиций табеля")
            page.setting.click_by_text("Настроить позиции табеля")
            page.setting.set_all_positions(True)
            assert check
        else:
            print("Текущая дата не подходит для прохождения данного теста!")

    def test_department_setting(self):
        """
        Настройка курируемых департаментов
        """
        LoginPage(self.driver).login(username="Литвинцева Ирина Юрьевна", password="Литвинцева4509")

        page = MainPage(self.driver)
        page.show_menu()
        page.menu.administration()
        page.menu.click_by_text("Управление пользователями")
        # ищем нужного сотрудника и добавляем департамент
        page = UsersManagementPage(self.driver)
        page.search("Литвинцева Ирина Юрьевна")
        page.personal_card.click_by_text("Курируемые департаменты")
        page.personal_card.departments.click_by_text("Выбор курируемых департаментов")
        selected_department = page.personal_card.departments.select_department()
        page.personal_card.departments.click_by_text("Подтвердить")
        page.personal_card.departments.click_by_text("Сохранить")

        page = MainPage(self.driver)
        page.show_menu()
        page.menu.click_by_text("Табель")
        # запоминаем результат проверки
        check = TimeSheetPage(self.driver).is_option_exist(selected_department)
        # убираем выбранный департамент
        page.show_menu()
        page.menu.administration()
        page.menu.click_by_text("Управление пользователями")
        page = UsersManagementPage(self.driver)
        page.search("Литвинцева Ирина Юрьевна")
        page.personal_card.click_by_text("Курируемые департаменты")
        page.personal_card.departments.click_by_text("Выбор курируемых департаментов")
        page.personal_card.departments.click_by_text("Выбрано")
        page.personal_card.departments.deselect_department(selected_department)
        page.personal_card.departments.click_by_text("Подтвердить")
        page.personal_card.departments.click_by_text("Сохранить")
        assert check
#
        # sss s

    def test_example(self):
        pass
