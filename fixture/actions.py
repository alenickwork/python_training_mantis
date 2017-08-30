from selenium.webdriver.support.ui import Select
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time

class ActionsHelper:

    def __init__(self,app):
        self.app = app

    def dropdown_select(self, field_name, value):
        print('''   drop-down <{1}> |   value <{0}>'''.format(value, field_name))
        select = Select(self.app.wd.find_element_by_name(field_name))
        start = time.time()
        while True:
            try:
                select.select_by_visible_text(value)
                break
            except:
                assert time.time() - start < 5
                time.sleep(1)

    def file_select(self, field_name, value):
        print("\tfile upload <{1}> |\tvalue <{0}>".format(value, field_name))
        self.app.wd.find_element_by_name(field_name).send_keys(value)

    def text_input(self, field_name, value):
        print('''   text input <{1}> |  value <{0}>'''.format(value, field_name))
        self.app.wd.find_element_by_name(field_name).click()
        self.app.wd.find_element_by_name(field_name).clear()
        self.app.wd.find_element_by_name(field_name).send_keys(value)

    def text_input_by_id(self, field_name, value):
        self.app.wd.find_element_by_id(field_name).click()
        self.app.wd.find_element_by_id(field_name).clear()
        self.app.wd.find_element_by_id(field_name).send_keys(value)


    def button_click(self, button_name):
        self.app.wd.find_element_by_name(button_name).click()

    def input_click(self, input_value):
        self.app.wd.find_element_by_xpath("//input[@value='{0}']".format(input_value)).click()

    def link_click(self, link_text):
        self.app.wd.find_element_by_link_text(link_text).click()
        #self.app.wd.find_elements_by_xpath("//*[contains(text(), '%s')]" % link_text)



    def menu_item_click(self, menu_name):
        print("Menu item name:{0} click".format(menu_name))
        self.app.wd.find_element_by_name(menu_name).click()

    def submit(self):
        self.button_click("submit")

    def update(self):
        self.button_click("update")

    def wait_button_clickable(self, button_name):
        wait = WebDriverWait(self.app.wd, 10)
        wait.until(EC.element_to_be_clickable((By.XPATH, "//input[@value='{0}']".format(button_name))))
