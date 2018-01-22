from framework import *


class LoginLocators(object):
    username = (By.XPATH, "//input[@id='UserName']")
    password = (By.XPATH, "//input[@id='Password']")
    submit = (By.XPATH, "//button[@type='submit']")
    code = (By.XPATH, "//input[@id='KeyWord']")
    next = (By.XPATH, "//button[@id='nextBtn']")
    new_password = (By.XPATH, "//input[@id='NewPassword']")
    confirm_password = (By.XPATH, "//input[@id='ConfirmPassword']")
    finish = (By.XPATH, "//button[@id='finishBtn']")


class MainLocators(object):
    quit = (By.XPATH, "//span[@class='qa-icon-exit']")
    menu_button = (By.XPATH, "//i[@class='qa-header-icon-menu-left-sitebar']")


class EducationPlanningLocators(object):

    class PersonalProject(object):
        year = (By.XPATH, "//div[@class='dropdown year']")
        add = (By.XPATH, "//input[@value='Добавить']")
        user = (By.XPATH, "//div[@ng-model='model.user']")
        education_direction = (By.XPATH, "//div[@ng-model='model.educationDirection']")
        content_types = (By.XPATH, "//div[@ng-model='model.contentTypes']")
        other_content_type = (By.XPATH, "//input[@ng-model='model.otherContentType']")
        rationale = (By.XPATH, "//input[@ng-model='model.rationale']")
        save = (By.XPATH, "//input[@value='Сохранить']")

    class DepartmentProject(object):
        year = (By.XPATH, "//div[@class='dropdown year']")


class UsersManagementLocators(object):
    search = (By.XPATH, "//input[@ng-model='filter.searchText']")

    class PersonalCard(object):
        notification_management_role = (By.XPATH, "//label[@for='Roles_14__IsInRole']")
        plan_management_role = (By.XPATH, "//label[@for='Roles_7__IsInRole']")
