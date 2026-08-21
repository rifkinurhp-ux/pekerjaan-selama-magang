from pages.front_pages.base_page import BasePage
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC

LOGIN_PATH = "/login"


class LoginPage(BasePage):
    _USERNAME = (By.CSS_SELECTOR, "input[name='username'], input[type='text'], input[placeholder*='sername'], input[id*='username'], input[id*='user']")
    _PASSWORD = (By.CSS_SELECTOR, "input[type='password']")
    _SUBMIT   = (By.CSS_SELECTOR, "button[type='submit'], input[type='submit']")

    def open_login(self) -> "LoginPage":
        self.open(LOGIN_PATH)
        return self

    def login(self, username: str, password: str) -> "LoginPage":
        self.type(*self._USERNAME, username)
        self.type(*self._PASSWORD, password)
        self.click(*self._SUBMIT)
        return self

    def wait_for_redirect(self, timeout: int = 15) -> bool:
        """Wait until URL no longer contains /login."""
        try:
            self.wait.until(EC.url_changes(self.driver.current_url))
            return LOGIN_PATH not in self.driver.current_url
        except TimeoutException:
            return False

    def is_error_visible(self) -> bool:
        return self.is_visible(By.CSS_SELECTOR, "[class*='error'], [class*='alert'], [role='alert']", timeout=5)
