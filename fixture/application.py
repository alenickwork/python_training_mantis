# -*- coding: utf-8 -*-
__author__ = "Elena Dimchenko"

from selenium import webdriver #.firefox.webdriver import WebDriver
from fixture.session import SessionHelper
from fixture.project import ProjectHelper


class Application:

    def __init__(self, browser, url):
        if browser == "firefox":
            self.wd = webdriver.Firefox()
        elif browser == "chrome":
            self.wd = webdriver.Chrome()
        elif browser == "ie":
            self.wd = webdriver.Ie()
        else:
            raise ValueError("Unrecognized browser %s" % browser)

        # self.wd.implicitly_wait(6)
        self.url = url
        self.session = SessionHelper(self)
        self.project = ProjectHelper(self)



    def destroy(self):
        self.wd.quit()

    def is_valid(self):
        try:
            self.wd.current_url
            return True
        except:
            return False






