

from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from fixture.actions import ActionsHelper

class SessionBroken(Exception):
    def __init__(self, message):
        super(SessionBroken, self).__init__(message)

def assert_session_valid(fn):
    def tmp(self, *args, **kwargs):
        print("Checking session is alive...")
        if not self.app.is_valid():
            raise SessionBroken("Session is broken")
        print("Yep, it's alive.")
        return fn(self, *args, **kwargs)
    return tmp


class SessionHelper(ActionsHelper):

    def __init__(self,app):
        super(SessionHelper,self).__init__(app)
        self.app = app
        self.addressbook_url = self.app.url
        self.username = None
        self.password = None

    def _open_mantisbt(self):
        self.app.wd.get(self.addressbook_url)

    @assert_session_valid
    def login(self, username, password):
        self._open_mantisbt()
        wait = WebDriverWait(self.app.wd, 10)
        print("Login")
        self.username = username
        self.password = password
        wait.until(EC.element_to_be_clickable((By.ID, 'login-form')))
        self.text_input("username", username)
        self.input_click("Login")
        wait.until(EC.element_to_be_clickable((By.ID, "remember-login")))
        self.text_input("password", password)
        self.input_click("Login")


    @assert_session_valid
    def logout(self):
        print("Logout")
        self.link_click(self.username)
        self.link_click("Logout")
        wait = WebDriverWait(self.app.wd, 10)
        wait.until(EC.element_to_be_clickable((By.ID, 'login-form')))

    @assert_session_valid
    def ensure_logout(self):
        wd = self.app.wd
        if self.is_logged_in():
            self.logout()

    @assert_session_valid
    def is_logged_in(self):
        wd = self.app.wd
        return self.app.wd.find_element_by_xpath("//*[contains(text(),'%s')]" % "Logout")

    @assert_session_valid
    def is_logged_in_as(self, username):
        wd = self.app.wd
        return self.get_logged_user() == username

    def get_logged_user(self):
        wd = self.app.wd
        return wd.find_element_by_xpath("//span[@class='user-info']").text

    @assert_session_valid
    def ensure_login(self, username, password):
        wd = self.app.wd
        if self.is_logged_in():
            if self.is_logged_in_as(username):
                return
            else:
                self.logout()
        self.login(username, password)

