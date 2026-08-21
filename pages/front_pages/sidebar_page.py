from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait

from pages.front_pages.base_page import BasePage


class SidebarPage(BasePage):

    def wait_until_loaded(self, timeout: int | None = None) -> "SidebarPage":
        """Wait for the sidebar shell to render. Pass a shorter `timeout`
        when probing a page that might be broken (404/error), so a bad
        page fails fast instead of eating the default wait."""
        wait = self.wait if timeout is None else WebDriverWait(self.driver, timeout)
        wait.until(EC.presence_of_element_located(
            (By.CSS_SELECTOR, "div[role='button'][aria-label]")
        ))
        return self

    def click_menu(self, name: str) -> "SidebarPage":
        btn = self.find_clickable(By.CSS_SELECTOR, f"div[role='button'][aria-label='{name}']")
        self.driver.execute_script("arguments[0].click();", btn)
        return self

    def get_visible_submenus(self) -> list[dict]:
        """Return unique sub-menu items currently visible in sidebar."""
        raw = self.driver.execute_script("""
            const links = Array.from(document.querySelectorAll('a[href]'));
            return links.map(a => ({ text: a.innerText.trim(), href: a.getAttribute('href') }));
        """)
        seen = set()
        result = []
        for item in raw:
            path = item["href"] or ""
            text = item["text"]
            if path and path != "/" and text and path not in seen:
                seen.add(path)
                result.append({
                    "text": text,
                    "href": path,
                    "full_url": self.base_url + path,
                })
        return result

    def navigate_to(self, full_url: str) -> "SidebarPage":
        self.driver.get(full_url)
        return self

    def current_page_has_error(self) -> bool:
        title = self.driver.title.lower()
        body = self.driver.find_element(By.TAG_NAME, "body").text.lower()
        return "404" in title or "error" in title or "not found" in body[:200]
