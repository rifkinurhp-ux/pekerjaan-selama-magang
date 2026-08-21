from pages.front_pages.base_page import BasePage
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import Select


class ChooseCompanyPage(BasePage):
    _SELECT   = (By.CSS_SELECTOR, "select")
    _CONTINUE = (By.XPATH, "//button[normalize-space()='Continue']")

    def wait_until_loaded(self) -> "ChooseCompanyPage":
        self.find(*self._SELECT)
        return self

    def select_company_by_text(self, partial_text: str) -> "ChooseCompanyPage":
        el = self.find(*self._SELECT)
        sel = Select(el)
        match = next(
            (opt for opt in sel.options if partial_text.lower() in opt.text.lower()),
            None,
        )
        if match is None:
            available = [o.text for o in sel.options]
            raise ValueError(f"Option '{partial_text}' tidak ditemukan. Tersedia: {available}")
        sel.select_by_visible_text(match.text)
        return self

    def click_continue(self) -> "ChooseCompanyPage":
        btn = self.find_clickable(*self._CONTINUE)
        self.driver.execute_script("arguments[0].click();", btn)
        self.wait.until(lambda d: "/choose-company-org" not in d.current_url)
        return self

    def selected_text(self) -> str:
        el = self.find(*self._SELECT)
        return Select(el).first_selected_option.text
