import pytest
from pages.front_pages.base_page import BasePage
from selenium.webdriver.common.by import By


@pytest.mark.smoke
def test_page_title_not_empty(driver, base_url):
    page = BasePage(driver, base_url)
    page.open()
    assert page.title != ""


@pytest.mark.smoke
def test_page_loads_successfully(driver, base_url):
    page = BasePage(driver, base_url)
    page.open()
    assert base_url in page.current_url


@pytest.mark.ui
def test_page_has_body(driver, base_url):
    page = BasePage(driver, base_url)
    page.open()
    assert page.is_visible(By.TAG_NAME, "body")
