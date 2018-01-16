from time import localtime, strftime, sleep
from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as ec
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import Select
from selenium.webdriver.common.keys import Keys
from selenium.common.exceptions import TimeoutException
import datetime
import os
import json


class Browser(object):
    """
    Methods for working with browser
    """
    def __init__(self, driver, timeout=60, log=True):
        self.driver = driver
        self.timeout = timeout
        self.log = log
        self.wait = Wait(self.driver, self.timeout)

    #
    def accept_alert(self):
        try:
            WebDriverWait(self.driver, 3).until(ec.alert_is_present())
            self.driver.switch_to_alert().accept()
        except TimeoutException:
            pass

    #
    def decline_alert(self):
        try:
            WebDriverWait(self.driver, 3).until(ec.alert_is_present())
            self.driver.switch_to_alert().decline()
        except TimeoutException:
            pass

    def get_alert_text(self):
        try:
            WebDriverWait(self.driver, 3).until(ec.alert_is_present())
            return self.driver.switch_to.alert.text
        except TimeoutException:
            return False

    # Click по локатору(Пример: (By.XPATH, "//input[@id='documentNumber']"))
    def click(self, locator, label=None):
        self.wait.loading()
        element = self.wait.element_appear(locator)
        self.move_to_element(element)
        element.click()
        if label and self.log:
            print("[%s] [%s] нажатие на элемент" % (strftime("%H:%M:%S", localtime()), label))

    # Click по тексту для кнопки или ссылки по тексту
    def click_by_text(self, text, order=1, exactly=False):
        self.wait.loading()
        if exactly:
            locator = (By.XPATH, "(//*[self::a or self::button][normalize-space()='%s'])[%s]" % (text, order))
        else:
            locator = (By.XPATH,
                       "(//*[self::a or self::button][contains(normalize-space(), '%s')])[%s]" % (text, order))
        element = self.wait.element_appear(locator)
        self.move_to_element(element)
        element.click()
        if text and self.log:
            print("[%s] [%s] нажатие на элемент" % (strftime("%H:%M:%S", localtime()), text))

    # Click по атрибуту объекта на странице
    def click_by_value(self, value, order=1, exactly=False):
        self.wait.loading()
        if exactly:
            locator = (By.XPATH, "(//input[@value='%s'])[%s]" % (value, order))
        else:
            locator = (By.XPATH, "(//input[contains(@value, '%s')])[%s]" % (value, order))
        element = self.wait.element_appear(locator)
        self.move_to_element(element)
        element.click()
        if value and self.log:
            print("[%s] [%s] нажатие на элемент" % (strftime("%H:%M:%S", localtime()), value))

    # Функция перехода на страницу
    def go_to(self, url):
        while self.driver.current_url != url:
            self.driver.get(url)
            sleep(.1)
        print("Переход по ссылке: %s" % url)

    # Функция скролирования до элемента
    def move_to_element(self, element):
        self.wait.loading()
        webdriver.ActionChains(self.driver).move_to_element(element).perform()

    # Функция скролирования вверх страницы
    def scroll_to_top(self):
        self.wait.loading()
        self.driver.execute_script("window.scrollTo(0, 0);")

    # Функция скролирования вниз
    def scroll_to_bottom(self):
        self.wait.loading()
        self.driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")

    # Функция очистка поисковой строки если выбрано несколько фильтров
    def select2_clear(self, locator):
        self.wait.loading()
        element = self.wait.element_appear(locator)
        while True:
            try:
                element.click()
            except (ec.StaleElementReferenceException, ec.NoSuchElementException):
                break

    # Функция заполнение поля через троеточие(выбор из справочника)
    def set_type(self, locator, value, label=None):
        self.wait.loading()
        self.click(locator)
        self.set_text((By.XPATH, "//div[@class='modal-content']//input[@placeholder='Все поля']"),
                      value + Keys.RETURN, label)
        self.click((By.XPATH, "//tr[contains(., '%s')]" % value))
        self.click_by_text("Выбрать")

    # Функция заполнения текстового поля
    def set_text(self, locator, value, label=None):
        if value:
            self.wait.loading()
            element = self.wait.element_appear(locator)
            element.clear()
            element.send_keys(value)
            if label and self.log:
                print("[%s] [%s] заполнение значением \"%s\"" % (strftime("%H:%M:%S", localtime()), label, value))

    # Функция заполнения текстового поля и проверка содержимого
    def set_text_and_check(self, locator, value, label=None):
        if value:
            self.wait.loading()
            element = self.wait.element_appear(locator)
            element.clear()
            element.send_keys(value)
            self.wait.lamb(lambda x: element.get_attribute("value") == value)
            if label and self.log:
                print("[%s] [%s] заполнение значением \"%s\"" % (strftime("%H:%M:%S", localtime()), label, value))

    # Функция заполнения поля Дата
    def set_date(self, locator, value, label=None):
        if value:
            if value == "=":
                value = Date.get_today_date()
            self.wait.loading()
            element = self.wait.element_appear(locator)
            element.clear()
            element.send_keys(value + Keys.TAB)
            if label and self.log:
                print("[%s] [%s] заполнение значением \"%s\"" % (strftime("%H:%M:%S", localtime()), label, value))

    # Функция заполнения/снятия чек-бокса
    def set_checkbox(self, locator, value=True, label=None):
        element = self.wait.element_appear(locator)
        if element.is_selected() != value:
            element.click()
            if label and self.log:
                print("[%s] [%s] установка флага в положение \"%s\"" % (strftime("%H:%M:%S",
                                                                                 localtime()), label, value))

    # Функция(общая) заполнения/снятия чек-бокса по порядку элемента на страницу
    def set_checkbox_by_order(self, order=1, value=True, label=None):
        element = self.wait.element_appear((By.XPATH, "(//input[@type='checkbox'])[%s]" % order))
        if element.is_selected() != value:
            element.click()
            if label and self.log:
                print("[%s] [%s] установка флага в положение \"%s\"" % (strftime("%H:%M:%S",
                                                                                 localtime()), label, value))

    # Функция заполнения/снятия радио-баттон
    def set_radio(self, locator, label=None):
        element = self.wait.element_appear(locator)
        element.click()
        if label and self.log:
            print("[%s] [%s] выбор опции" % (strftime("%H:%M:%S", localtime()), label))

    # Функция выбора значения из выпадающего списка
    def set_select(self, locator, value, label=None):
        if value:
            self.wait.loading()
            element = self.wait.element_appear(locator)
            Select(element).select_by_visible_text(value)
            if label and self.log:
                print("[%s] [%s] выбор из списка значения \"%s\"" % (strftime("%H:%M:%S", localtime()), label, value))

    # Функция выбора значения из Select2
    def set_select2(self, locator, value, label=None):
        if value:
            self.click(locator)
            self.set_text_and_check((By.XPATH, "//div[@id='select2-drop']//input"), value)
            sleep(1)
            self.click((By.XPATH, "//*[@role='option'][contains(normalize-space(), '%s')]" % value))
            self.wait.element_disappear((By.ID, "select2-drop"))
            if label and self.log:
                print("[%s] [%s] выбор из списка значения \"%s\"" % (strftime("%H:%M:%S", localtime()), label, value))

    # Функция выбора строки в таблице
    def table_select_row(self, order=1, label=None):
        self.wait.loading()
        locator = (By.XPATH, "(//td/input[@type='checkbox'])[%s]" % order)
        self.set_checkbox(locator, True, label)

    # Функция выбора чек-бокса в таблице по порядку
    def table_row_checkbox(self, order=1):
        self.wait.loading()
        sleep(1)
        locator = (By.XPATH, "(//td/input[@type='checkbox'])[%s]" % order)
        self.set_checkbox(locator, True)
        sleep(1)

    # Функция выбора радио-баттон в таблице по порядку
    def table_row_radio(self, order=1):
        self.wait.loading()
        sleep(1)
        locator = (By.XPATH, "(//td/input[@type='radio'])[%s]" % order)
        self.set_radio(locator)
        sleep(1)

    # Функция загрузки файла
    def upload_file(self, value, order=1):
        self.wait.loading()
        # открываем страницу с формой загрузки файла
        element = self.driver.find_element(By.XPATH, "(//input[@type='file'])[%s]" % order)

        element.clear()
        element.send_keys("%s/%s" % (os.getcwd(), value))
        WebDriverWait(self.driver, 60).until(
            ec.visibility_of_element_located((By.XPATH, "//li[@class=' qq-upload-success']")))

    # Функция выбор месяца
    def select_month(self, year, month):
        months = {
            1: "Янв",
            2: "Фев",
            3: "Мар",
            4: "Апр",
            5: "Май",
            6: "Июнь",
            7: "Июль",
            8: "Авг",
            9: "Сен",
            10: "Окт",
            11: "Ноя",
            12: "Дек"
        }
        self.click((By.XPATH, "//a[@class='periods__btn btn seasons dropdown-toggle ng-binding']"))
        sleep(2)
        if year != datetime.date.today().year:
            self.click((By.XPATH, "//span[.='prevLabel']"))
        self.click((By.XPATH, "//span[@class='ui-button-text'][.='%s']" % months[month]))
        self.accept_alert()

    def save_screenshot(self, name, default_folder="", overwrite=True):
        """
        Method making screenshot of current page of driver
        :param name: Name of file. Extension is png by default
        :param default_folder: Folder with script by default. Important: use raw-strings if you using different one
        :param overwrite: Overwite file if True
        :return:
        """
        if self.driver.save_screenshot("%s%s.png" % (default_folder, name)) or overwrite:
            self.driver.save_screenshot("%s%s.png" % (default_folder, name))
        else:
            for i in range(100):
                if not os.path.isfile("%s%s-%s.png" % (default_folder, name, i)):
                    self.driver.save_screenshot("%s%s-%s.png" % (default_folder, name, i))
                    break


class Date(object):
    """
    Methods for working with date
    """
    # Функция возвращающая текущую дату
    @staticmethod
    def get_today_date():
        return datetime.date.today().strftime("%d.%m.%Y")


class Wait(object):
    """
    Methods for waiting
    """
    def __init__(self, driver, timeout):
        self.driver = driver
        self.timeout = timeout

    # Функция ожидания текста пока не появится
    def text_appear(self, text):
        return WebDriverWait(self.driver, self.timeout).until(
            ec.visibility_of_element_located((By.XPATH, "//*[contains(., '%s')]" % text)))

    # Функция ожидания пока текст не пропадёт
    def text_disappear(self, text):
        return WebDriverWait(self.driver, self.timeout).until(
            ec.visibility_of_element_located((By.XPATH, "//*[contains(., '%s')]" % text)))

    # Функция ожидания элемента пока не появится
    def element_appear(self, locator):
        return WebDriverWait(self.driver, self.timeout).until(ec.visibility_of_element_located(locator))

    # Функция ожидания пока элемент не пропадёт
    def element_disappear(self, locator):
        return WebDriverWait(self.driver, self.timeout).until(ec.invisibility_of_element_located(locator))

    def lamb(self, exe):
        return WebDriverWait(self.driver, self.timeout).until(exe)

    # Функция ожидания окончания закгрузки - пока не пропал лоадер
    def loading(self):
        WebDriverWait(self.driver, self.timeout).until_not(
            ec.visibility_of_element_located((By.XPATH, "//div[@class='loading-spinner']")))
        WebDriverWait(self.driver, self.timeout).until_not(
            ec.visibility_of_element_located((By.XPATH, "//div[@class='windows8']")))
        WebDriverWait(self.driver, self.timeout).until_not(
            ec.visibility_of_element_located((By.XPATH, "//div[@class='w2ui-lock']")))


# Работа с данными
class Data(object):
    """
    Methods for working with data
    """
    @staticmethod
    def load_data(file):
        script_path = os.path.dirname(__file__)
        filename = os.path.join(script_path, '%s.json' % file)
        return json.loads(open(filename, encoding="utf8").read())

    @staticmethod
    def get_data_by_value(data, parent, key, value):
        for i in data[parent]:
            if value == i[key]:
                return i
        return None

    @staticmethod
    def get_data_by_number(data, parent, number=0):
        return data[parent][number]
