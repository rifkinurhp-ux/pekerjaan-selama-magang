import time

from pages.front_pages.choose_company_page import ChooseCompanyPage
from pages.front_pages.login_page import LoginPage


def test_inspect_sidebar(login_creds, base_url, test_company, driver):
    username, password = login_creds

    login = LoginPage(driver, base_url)
    login.open_login()
    login.login(username, password)
    login.wait_for_redirect()

    company = ChooseCompanyPage(driver, base_url)
    company.wait_until_loaded()
    company.select_company_by_text(test_company)
    company.click_continue()

    time.sleep(3)

    driver.save_screenshot("screenshots/sidebar.png")

    with open("screenshots/sidebar.html", "w") as f:
        f.write(driver.page_source)

    print(f"\nURL: {driver.current_url}")
