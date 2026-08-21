import time

from bs4 import BeautifulSoup
from pages.front_pages.choose_company_page import ChooseCompanyPage
from pages.front_pages.login_page import LoginPage
from selenium.webdriver.common.by import By

MENUS = [
    "Sales Order Suites", "Delivery & Return", "NOO", "Master Data",
    "Matrix Kecil", "Matrix Besar Configuration", "Reporting", "Configuration",
    "Collection", "Supplier Claim", "Finance", "Administration",
    "Approval V2", "Logs", "Document Utilities", "Inventory",
]


def test_inspect_submenus(login_creds, base_url, test_company, driver):
    username, password = login_creds

    login = LoginPage(driver, base_url)
    login.open_login()
    login.login(username, password)
    login.wait_for_redirect()

    company = ChooseCompanyPage(driver, base_url)
    company.wait_until_loaded()
    company.select_company_by_text(test_company)
    company.click_continue()
    time.sleep(2)

    result = {}

    for menu_name in MENUS:
        # klik menu
        btn = driver.find_element(By.CSS_SELECTOR, f"div[role='button'][aria-label='{menu_name}']")
        driver.execute_script("arguments[0].click();", btn)
        time.sleep(1)

        soup = BeautifulSoup(driver.page_source, "html.parser")
        links = soup.find_all("a")
        submenus = [
            {"text": a.get_text(strip=True), "href": a.get("href", "")}
            for a in links
            if a.get("href") and a.get("href") != "/" and a.get_text(strip=True)
        ]
        result[menu_name] = submenus
        print(f"\n[{menu_name}]")
        for s in submenus:
            print(f"  - {s['text']!r:40} -> {s['href']}")

        # collapse lagi sebelum ke menu berikutnya
        driver.execute_script("arguments[0].click();", btn)
        time.sleep(0.5)

    print("\n\n=== SUMMARY ===")
    for menu, subs in result.items():
        print(f"{menu}: {len(subs)} sub-menus")
