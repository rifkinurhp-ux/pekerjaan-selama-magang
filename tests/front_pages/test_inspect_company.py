from pages.front_pages.login_page import LoginPage


def test_inspect_company_page(login_creds, base_url, driver):
    username, password = login_creds

    page = LoginPage(driver, base_url)
    page.open_login()
    page.login(username, password)
    page.wait_for_redirect()

    driver.save_screenshot("screenshots/company_page.png")

    src = driver.page_source
    with open("screenshots/company_page.html", "w") as f:
        f.write(src)

    print(f"\nURL: {driver.current_url}")
    print(f"Title: {driver.title}")
