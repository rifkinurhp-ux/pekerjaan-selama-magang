import os
import time
import pytest
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.action_chains import ActionChains
from datetime import datetime, timedelta

from pages.front_pages.login_page import LoginPage
from pages.front_pages.choose_company_page import ChooseCompanyPage

def _login_and_enter(driver, base_url, username, password, company_name):
    driver.get(base_url)
    time.sleep(2)

    if "login" in driver.current_url.lower():
        print("Sesi kosong, melakukan proses login")
        login = LoginPage(driver, base_url)
        
        login.open_login()
        time.sleep(3) # Memberi waktu ekstra agar form login termuat sempurna
        
        login.login(username, password)
        login.wait_for_redirect()

        company = ChooseCompanyPage(driver, base_url)
        company.wait_until_loaded()
        company.select_company_by_text(company_name)
        company.click_continue()
    else:
        print("Sesi ditemukan! Sudah berada di Dashboard, melewati proses login.")

@pytest.mark.regression
def test_create_customer_purchase_order(login_creds, base_url, test_company, driver):
    username, password = login_creds
    
    # ==========================================
    # 1. Login & Masuk ke Dashboard
    # ==========================================
    _login_and_enter(driver, base_url, username, password, test_company)
    wait = WebDriverWait(driver, 15)

    # ==========================================
    # 2. Buka Sidebar: Sales Order Suites -> Customer PO
    # ==========================================
    time.sleep(3)
    try:
        menu_sales_order = wait.until(EC.presence_of_element_located((By.XPATH, "//div[@role='button' and contains(., 'Sales Order Suites')]")))
        driver.execute_script("arguments[0].click();", menu_sales_order)
        time.sleep(1.5) 
    except Exception:
        pass 
    
    for _ in range(3):
        try:
            submenu_customer_po = wait.until(EC.presence_of_element_located((By.XPATH, "//a[contains(., 'Customer PO')]")))
            driver.execute_script("arguments[0].click();", submenu_customer_po)
            break 
        except Exception as e:
            print(f"Elemen menu bermasalah, mencoba ulang...")
            time.sleep(1.5)

    wait.until(EC.url_contains("customer-purchase-orders"))
    time.sleep(3) 

    # ==========================================
    # 3. Klik tombol "+ CREATE"
    # ==========================================
    btn_create_xpath = "//*[self::button or self::a or @role='button'][contains(., 'CREATE') or contains(., 'Create')]"
    btn_create = wait.until(EC.presence_of_element_located((By.XPATH, btn_create_xpath)))
    driver.execute_script("arguments[0].click();", btn_create)

    # ==========================================
    # 4. Pilih "Create CPO" di Popup Modal
    # ==========================================
    btn_create_cpo = wait.until(EC.element_to_be_clickable((By.XPATH, "//button[contains(., 'Create CPO') and not(contains(., 'Reserve'))]")))
    driver.execute_script("arguments[0].click();", btn_create_cpo) 

    wait.until(EC.url_contains("/create"))
    time.sleep(2) 

  # ==========================================
    # 5. Isi Form di Tab "General"
    # ==========================================
    print("\nMengisi form Tab General...")

    hari_ini = datetime.now()
    lima_hari_kedepan = hari_ini + timedelta(days=10)
    str_hari_ini = hari_ini.strftime("%d%m%Y") 
    str_expiry = lima_hari_kedepan.strftime("%d%m%Y")

    # --- 1. Isi Customer PO No ---
    input_po_no = wait.until(EC.presence_of_element_located((By.XPATH, "(//label[contains(., 'Customer PO No')]/following::input)[1]")))
    input_po_no.send_keys(Keys.CONTROL + "a")
    input_po_no.send_keys(Keys.BACKSPACE)
    input_po_no.send_keys("PO67000006")
    print("-> Customer PO No terisi.")
    time.sleep(1)

    # --- 2. Pilih Sales Code DULUAN ---
    xpath_sales = "(//label[contains(., 'Sales Code')]/following::button[@role='combobox'])[1]"
    dropdown_sales = wait.until(EC.element_to_be_clickable((By.XPATH, xpath_sales)))
    ActionChains(driver).move_to_element(dropdown_sales).click().perform() 
    time.sleep(1) 
    
    ActionChains(driver).send_keys("SAM2010-00650").perform()
    time.sleep(2) 
    
    ActionChains(driver).send_keys(Keys.ARROW_DOWN).perform()
    time.sleep(1)
    ActionChains(driver).send_keys(Keys.ENTER).perform()
    print("-> Sales Code dipilih dan dikunci.")
    time.sleep(2) # Jeda untuk React re-render

    # --- 3. Isi Total Amount (Rp) DULUAN ---
    try:
        xpath_total = "(//label[contains(., 'Total Amount (Rp)')]/following::input)[1]"
        input_total = wait.until(EC.element_to_be_clickable((By.XPATH, xpath_total)))
        input_total.click()
        input_total.send_keys(Keys.CONTROL + "a")
        input_total.send_keys(Keys.BACKSPACE)
        input_total.send_keys("10000000")
        input_total.send_keys(Keys.TAB) 
        print("-> Total Amount (Rp) terisi.")
        time.sleep(2) # Jeda untuk React re-render setelah kalkulasi angka
    except Exception:
        print("-> Field Total Amount tidak ditemukan, melewati langkah ini.")

    # --- 4. Isi Expiry Date PO (Aman dari refresh & tertutup elemen) ---
    input_expiry = wait.until(EC.presence_of_element_located((By.NAME, "expiry_date_po")))
    # GULIR LAYAR: Pastikan elemen berada di tengah agar tidak tertutup header/navbar
    driver.execute_script("arguments[0].scrollIntoView({block: 'center', behavior: 'smooth'});", input_expiry)
    time.sleep(1) 
    
    input_expiry = wait.until(EC.element_to_be_clickable((By.NAME, "expiry_date_po")))
    input_expiry.click() 
    time.sleep(0.5)
    input_expiry.send_keys(Keys.ARROW_LEFT)
    input_expiry.send_keys(Keys.ARROW_LEFT)
    input_expiry.send_keys(Keys.ARROW_LEFT)
    time.sleep(0.5)
    input_expiry.send_keys(str_expiry)
    time.sleep(0.5) 
    input_expiry.send_keys(Keys.TAB) 
    print(f"-> Expiry Date PO diketik dan dikunci: {str_expiry}")
    
    time.sleep(1) 
    label_expiry = driver.find_element(By.XPATH, "//label[contains(., 'Expiry Date PO')]")
    # Gunakan JS Click untuk label agar kebal dari elemen yang menutupi
    driver.execute_script("arguments[0].click();", label_expiry) 
    time.sleep(1)

    # --- 5. Isi Tanggal PO Customer (Aman dari refresh & tertutup elemen) ---
    input_tgl_po = wait.until(EC.presence_of_element_located((By.NAME, "tanggal_cetak")))
    # GULIR LAYAR ke tengah
    driver.execute_script("arguments[0].scrollIntoView({block: 'center', behavior: 'smooth'});", input_tgl_po)
    time.sleep(1)
    
    input_tgl_po = wait.until(EC.element_to_be_clickable((By.NAME, "tanggal_cetak")))
    input_tgl_po.click() 
    time.sleep(0.5)
    input_tgl_po.send_keys(Keys.ARROW_LEFT)
    input_tgl_po.send_keys(Keys.ARROW_LEFT)
    input_tgl_po.send_keys(Keys.ARROW_LEFT)
    time.sleep(0.5)
    input_tgl_po.send_keys(str_hari_ini)
    time.sleep(0.5) 
    input_tgl_po.send_keys(Keys.TAB) 
    print(f"-> Tanggal PO Customer diketik dan dikunci: {str_hari_ini}")
    
    time.sleep(1) 
    label_tgl = driver.find_element(By.XPATH, "//label[contains(., 'Tanggal PO Customer')]")
    # Gunakan JS Click untuk label agar kebal dari elemen yang menutupi
    driver.execute_script("arguments[0].click();", label_tgl) 
    time.sleep(1.5)

    # ==========================================
    # 6. Pindah ke Tab "Ship To" & Pilih Customer 
    # ==========================================
    print("\nMengisi form Tab Ship To...")
    tab_ship_to = wait.until(EC.presence_of_element_located((By.XPATH, "//button[@role='tab' and contains(., 'Ship To')]")))
    driver.execute_script("arguments[0].scrollIntoView({block: 'center', behavior: 'smooth'});", tab_ship_to)
    time.sleep(1)
    ActionChains(driver).move_to_element(tab_ship_to).click().perform() 
    time.sleep(2) 
    
    xpath_ship = "//button[@role='combobox' and (contains(., 'Select Ship To Customer Name') or contains(., 'Ship To Customer Name'))]"
    dropdown_ship_customer = wait.until(EC.presence_of_element_located((By.XPATH, xpath_ship)))
    ActionChains(driver).move_to_element(dropdown_ship_customer).click().perform()
    time.sleep(1.5) 
    
    ActionChains(driver).send_keys("GELAEL HARYONO TEBET").perform() 
    time.sleep(2.5) # Tunggu dropdown muncul
    
    ActionChains(driver).send_keys(Keys.ARROW_DOWN).perform()
    time.sleep(1)
    ActionChains(driver).send_keys(Keys.ENTER).perform()
    print("-> Customer Ship To dipilih.")
    time.sleep(2)

    # ==========================================
    # 7. --- PROSES ADD LINE ITEM ---
    # ==========================================
    btn_add_line = wait.until(EC.presence_of_element_located((By.XPATH, "//button[contains(., 'Add Line Item')]")))
    driver.execute_script("arguments[0].scrollIntoView({block: 'center', behavior: 'smooth'});", btn_add_line)
    time.sleep(1.5) 
    
    driver.execute_script("arguments[0].click();", btn_add_line)
    time.sleep(2) 
    
    xpath_sku = "(//label[contains(., 'SKU SAMB')]/following::input)[1]"
    input_sku = wait.until(EC.element_to_be_clickable((By.XPATH, xpath_sku)))
    
    input_sku.click()
    time.sleep(1) 
    
    input_sku.send_keys("1000027")
    time.sleep(2) # Tunggu dropdown produk muncul
    
    input_sku.send_keys(Keys.ARROW_DOWN)
    time.sleep(1) 
    input_sku.send_keys(Keys.ENTER)
    time.sleep(1.5) 
    
    # Isi QTY
    input_qty = driver.find_element(By.XPATH, "(//label[contains(., 'QTY Dipesan')]/following::input)[1]")
    input_qty.send_keys(Keys.CONTROL + "a")
    input_qty.send_keys(Keys.BACKSPACE)
    input_qty.send_keys("5") 
    time.sleep(2) 
    
    # Klik tombol "Save & Add More"
    btn_save_add_more = driver.find_element(By.XPATH, "//button[contains(., 'Save & Add More')]")
    driver.execute_script("arguments[0].click();", btn_save_add_more)
    time.sleep(3) 

    # --- KLIK TOMBOL CANCEL SETELAH SAVE & ADD MORE ---
    try:
        btn_cancel = wait.until(EC.presence_of_element_located((By.XPATH, "//button[normalize-space()='Cancel']")))
        driver.execute_script("arguments[0].click();", btn_cancel)
        time.sleep(2)
        print("\n[OK] Berhasil mengklik tombol Cancel pada modal.")
    except Exception as e:
        print(f"\n[WARNING] Tombol Cancel tidak ditemukan atau gagal diklik: {e}")

    # ==========================================
    # 8. Lihat Tab "Bill To" (Opsional)
    # ==========================================
    try:
        wait_short = WebDriverWait(driver, 5)
        tab_bill_to = wait_short.until(EC.presence_of_element_located((By.XPATH, "//button[@role='tab' and contains(., 'Bill To')]")))
        driver.execute_script("arguments[0].scrollIntoView({block: 'center', behavior: 'smooth'});", tab_bill_to)
        time.sleep(1)
        ActionChains(driver).move_to_element(tab_bill_to).click().perform() 
        time.sleep(1.5)
    except Exception:
        pass 

    # ==========================================
    # 9. Lihat Tab "SAP Info"
    # ==========================================
    tab_sap_info = wait.until(EC.presence_of_element_located((By.XPATH, "//button[@role='tab' and contains(., 'SAP Info')]")))
    ActionChains(driver).move_to_element(tab_sap_info).click().perform() 
    time.sleep(2)

    # ==========================================
    # 10. Klik Tombol "Save as Draft"
    # ==========================================
    time.sleep(2)
    try:
        btn_draft = wait.until(EC.presence_of_element_located((By.XPATH, "//button[contains(., 'Save as Draft')]")))
        driver.execute_script("arguments[0].scrollIntoView({block: 'center', behavior: 'smooth'});", btn_draft)
        time.sleep(1)
        driver.execute_script("arguments[0].click();", btn_draft)
        print("\n[OK] Berhasil mengklik tombol Save as Draft.")
        time.sleep(3)
    except Exception as e:
        print(f"\n[WARNING] Gagal mengklik Save as Draft: {e}")

    print("\n[OK] Alur Create CPO berhasil dijalankan sampai selesai!")