from locators import *
from links import Links


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

    def login(self, username, password):
        self.go_to(Links.login_page)
        self.username(username)
        self.password(password)
        self.submit()
        self.wait.text_appear("Здравствуйте, ")


class MainPage(Browser):

    @property
    def menu(self):
        return self.Menu(self.driver, self.timeout, self.log)

    def quit(self):
        self.click(MainLocators.quit)

    def show_menu(self):
        self.click(MainLocators.menu_button)
        sleep(1)

    class Menu(Browser):

        def administration(self):
            self.click((By.XPATH, "//span[@class='link'][contains(., 'Администрирование')]"))
            sleep(1)


class EducationPlanningPage(Browser):

    @property
    def personal_project(self):
        return self.PersonalProject(self.driver, self.timeout, self.log)

    @property
    def department_project(self):
        return self.DepartmentProject(self.driver, self.timeout, self.log)

    class PersonalProject(Browser):

        def year(self, value):
            self.set_select_alt(EducationPlanningLocators.PersonalProject.year, value, "Выбор года")

        def add(self):
            self.click(EducationPlanningLocators.PersonalProject.add, "Добавить")

        def user(self, value):
            sleep(1)
            self.set_select2(EducationPlanningLocators.PersonalProject.user, value, "Сотрудник")
            sleep(1)

        def education_direction(self, value):
            self.set_select2(EducationPlanningLocators.PersonalProject.education_direction, value,
                             "Направление обучения")

        def content_types(self, value):
            self.set_select2(EducationPlanningLocators.PersonalProject.content_types, value, "Содержание")

        def other_content_type(self, value):
            self.set_text(EducationPlanningLocators.PersonalProject.other_content_type, value, "Иное содержание")

        def rationale(self, value):
            self.set_text(EducationPlanningLocators.PersonalProject.rationale, value, "Обоснование")

        def save(self):
            self.click(EducationPlanningLocators.PersonalProject.save, "Сохранить")

        def select_new_plan(self):
            self.click((By.XPATH, "//input[@ng-model='item.selected']"))

    class DepartmentProject(Browser):

        def year(self, value):
            self.set_select_alt(EducationPlanningLocators.DepartmentProject.year, value, "Выбор года")

        def select_new_plan(self):
            self.click((By.XPATH, "//input[@ng-model='item.selected']"))

        def select_plan_by_order(self, order):
            self.click((By.XPATH, "(//input[@ng-model='item.selected'])[%s]" % order))

        def select_plan_by_user(self, value):
            tr = self.wait.element_appear((By.XPATH, "//tr[contains(., '%s')]" % value))
            checkbox = tr.find_element_by_xpath(".//input[@type='checkbox']")
            self.move_to_element(checkbox)
            checkbox.click()

        def buttons_state(self):
            result = list()
            result.append(self.driver.find_element_by_xpath("//input[@value='Добавить']").is_enabled())
            result.append(self.driver.find_element_by_xpath("//input[@value='Редактировать']").is_enabled())
            result.append(self.driver.find_element_by_xpath("//input[@value='Утвердить']").is_enabled())
            result.append(self.driver.find_element_by_xpath("//input[@value='Удалить']").is_enabled())
            result.append(self.driver.find_element_by_xpath("//input[@value='Печать']").is_enabled())
            return result

        def select_all_plans(self):
            self.driver.find_element_by_xpath("//input[@type='checkbox']")


class UsersManagementPage(Browser):

    @property
    def personal_card(self):
        return self.PersonalCard(self.driver, self.timeout, self.log)

    def search(self, value):
        self.wait.text_appear("ФИО")
        self.set_text_and_check(UsersManagementLocators.search, value, "Поиск")
        sleep(5)
        # из-за анимации поиска и постоянно появляющегося/исчезающего элемента
        # приходится ждать его в течении 5 секунда с помощью данного цикла
        self.click_by_text(value)

    class PersonalCard(Browser):

        @property
        def departments(self):
            return self.Departments(self.driver, self.timeout, self.log)

        def notification_management_rule(self, value):
            self.set_checkbox(UsersManagementLocators.PersonalCard.notification_management_role,
                              value,
                              "Управление уведомлениями")

        def plan_management_rule(self, value):
            self.set_checkbox(UsersManagementLocators.PersonalCard.plan_management_role,
                              value,
                              "Управление уведомлениями")

        class Departments(Browser):

            def select_department(self):
                element = self.wait.element_appear((By.XPATH, "//tr[@class='selectedtr ng-scope']"))
                element.click()
                return element.text

            def deselect_department(self, value):
                element = self.wait.element_appear((By.XPATH, "//tr[contains(., '%s')]//td[@ng-click='onDepartmentUnselect(item)']" % value))
                element.click()


class TimeSheetPage(Browser):

    @property
    def setting(self):
        return self.Setting(self.driver, self.timeout, self.log)

    def year(self, value):
        self.set_select_alt(TimeSheetLocators.year, value, "Выбор года")

    def month(self, value):
        self.set_select_alt(TimeSheetLocators.month, value, "Выбор месяца")

    def department(self, value):
        self.set_select(TimeSheetLocators.department, value, "Выбор подразделения")

    def cross_field_click(self):
        self.click(TimeSheetLocators.cross_field, "Клик на пересечении строки сотрудника и даты")

    def select_reasons(self, employee):
        tr = self.wait.element_appear((By.XPATH,
                                       "//tr[@ng-repeat='user in department.users' and contains(., '%s')]" % employee))
        field = tr.find_element_by_xpath(
            "//td[contains(@ng-class, 'not-employed') and not(contains(@title, 'Выходные и нерабочие'))]")

        for i in range(17):
            field.click()
            sleep(1)
            reason = self.wait.element_appear((By.XPATH, "(//div[@class='item-highlight ng-binding'])[%s]" % (i+1)))
            span = reason.find_element_by_xpath("span[@class='reason-missing ng-binding']").text
            reason.click()
            if span == "Ф" or span == "К":
                self.driver.find_element_by_xpath("(//input[@id='work-time'])[%s]" % (i+1)).send_keys("21:00")
            self.click_by_text("Сохранить")
            sleep(1.5)
            print("Сравнение вывода причины: На ячейке=%s Причина=%s" % (field.text, span))
            if span == "Ф":
                if field.text != "21:00":
                    return False
            elif field.text != span:
                return False
        return True

    def is_there_any_option(self, employee):
        tr = self.wait.element_appear((By.XPATH,
                                       "//tr[@ng-repeat='user in department.users' and contains(., '%s')]" % employee))
        field = tr.find_element_by_xpath(
            "//td[contains(@ng-class, 'not-employed') and not(contains(@title, 'Выходные и нерабочие'))]")

        field.click()
        sleep(1)
        try:
            self.driver.find_element_by_xpath("//li[@ng-click='changeType(type)']")
            return False
        except ec.NoSuchElementException:
            return True
        finally:
            self.click_by_text("Отмена")
            sleep(1)

    def is_option_exist(self, value):
        self.click((By.XPATH, "//select[@id='DepartmentId']"))
        return self.driver.find_element_by_xpath("//select[@id='DepartmentId']//option[contains(., '%s')]"
                                                 % value)

    class Setting(Browser):

        def set_all_positions(self, value):
            for i in range(17):
                locator = (By.XPATH, "//label[@for='typeDays_%s']" % i)
                self.set_checkbox(locator, value)
            self.click_by_text("Подтвердить")
            self.wait.text_disappear("Подтвердить")
            save_button = self.wait.element_appear((By.XPATH, "//button[@ng-click='save()']"))
            if save_button.is_enabled():
                self.click_by_text("Сохранить")
