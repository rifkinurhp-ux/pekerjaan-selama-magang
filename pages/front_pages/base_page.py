from selenium.webdriver.common.by import By  # noqa: F401
from selenium.webdriver.remote.webdriver import WebDriver
from selenium.webdriver.remote.webelement import WebElement
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait


class BasePage:
    def __init__(self, driver: WebDriver, base_url: str = "") -> None:
        self.driver = driver
        self.base_url = base_url
        self.wait = WebDriverWait(driver, timeout=15)

    def open(self, path: str = "") -> None:
        self.driver.get(self.base_url + path)

    def find(self, by: str, value: str) -> WebElement:
        return self.wait.until(EC.presence_of_element_located((by, value)))

    def find_clickable(self, by: str, value: str) -> WebElement:
        return self.wait.until(EC.element_to_be_clickable((by, value)))

    def click(self, by: str, value: str) -> None:
        self.find_clickable(by, value).click()

    def type(self, by: str, value: str, text: str) -> None:
        el = self.find_clickable(by, value)
        el.clear()
        el.send_keys(text)

    def get_text(self, by: str, value: str) -> str:
        return self.find(by, value).text

    def is_visible(self, by: str, value: str, timeout: int = 5) -> bool:
        try:
            WebDriverWait(self.driver, timeout).until(
                EC.visibility_of_element_located((by, value))
            )
            return True
        except Exception:  # noqa: BLE001
            return False

    @property
    def title(self) -> str:
        return self.driver.title

    @property
    def current_url(self) -> str:
        return self.driver.current_url
