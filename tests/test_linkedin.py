import os
import pytest
from dotenv import load_dotenv
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.keys import Keys

# Load environment variables
load_dotenv()

def test_login_linkedin():
    driver = webdriver.Chrome()
    driver.maximize_window()
    
    try:
        driver.get("https://www.linkedin.com/login")
        wait = WebDriverWait(driver, 20)
        
        # 1. JURUS PAMUNGKAS EMAIL: Cari berdasarkan ID, Name, ATAU Autocomplete
        username_xpath = "//input[@id='username' or @name='session_key' or contains(@autocomplete, 'username')]"
        username_field = wait.until(EC.element_to_be_clickable((By.XPATH, username_xpath)))
        
        # 2. JURUS PAMUNGKAS PASSWORD: Cari berdasarkan Type, ID, ATAU Name
        password_xpath = "//input[@type='password' or @id='password' or @name='session_password']"
        password_field = driver.find_element(By.XPATH, password_xpath)
        
        # 3. Masukkan kredensial
        username_field.send_keys(os.getenv("LINKEDIN_USERNAME"))
        password_field.send_keys(os.getenv("LINKEDIN_PASSWORD") + Keys.RETURN)
        
        # 4. Tunggu sampai masuk ke beranda (feed)
        wait.until(EC.url_contains("feed"))
        print("\n[INFO] Login LinkedIn Berhasil! Selamat datang di Beranda.")
        
    except Exception as e:
        driver.save_screenshot("error_login_linkedin.png")
        print("\n[INFO] Gagal! Cek file 'error_login_linkedin.png'")
        raise e
        
    finally:
        driver.quit()