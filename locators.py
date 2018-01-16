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
