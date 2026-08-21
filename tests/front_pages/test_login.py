import os
import pytest
from dotenv import load_dotenv
from pages.front_pages.choose_company_page import ChooseCompanyPage
from pages.front_pages.login_page import LoginPage

load_dotenv()

SAMB_USER = os.getenv("SAMB_USERNAME")
SAMB_PASS = os.getenv("SAMB_PASSWORD")
# Kita ambil juga dari .env agar dinamis, atau langsung ketik "SARANA"
TARGET_COMP = os.getenv("TEST_COMPANY", "SARANA") 

@pytest.mark.parametrize("username, password, target_company", [
    (SAMB_USER, SAMB_PASS, TARGET_COMP) 
])
@pytest.mark.smoke
def test_login_and_select_sarana(username, password, target_company, base_url, driver):
    # Validasi jika data SAMB kosong di .env
    if not username or not password:
        pytest.skip("SAMB_USERNAME atau SAMB_PASSWORD belum diset di .env")

    # 1. Login menggunakan data dari parameterize (akun SAMB)
    login = LoginPage(driver, base_url)
    login.open_login()
    login.login(username, password)
    assert login.wait_for_redirect(), f"Login gagal. URL: {login.driver.current_url}"

    # 2. Pilih company menggunakan data dari parameterize
    company = ChooseCompanyPage(driver, base_url)
    company.wait_until_loaded()
    company.select_company_by_text(target_company)

    assert target_company.lower() in company.selected_text().lower(), (
        f"Company tidak terpilih. Selected: {company.selected_text()}"
    )

    company.click_continue()

    # 3. Berhasil
    print(f"\n[OK] Login + pilih company berhasil. URL: {driver.current_url}")
    driver.save_screenshot("screenshots/after_company_select.png")