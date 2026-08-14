from playwright.sync_api import sync_playwright
import time

def jalankan_testing_tanpa_login():
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=False)

        # KUNCI PENTING: Buka browser baru dengan membawa "ingatan" dari JSON
        context = browser.new_context(storage_state="linkedin_state.json")
        page = context.new_page()

        print("Menuju beranda LinkedIn tanpa login...")
        # Langsung tembak ke halaman utama (feed)
        page.goto("https://www.linkedin.com/feed/")

        # Tunggu sebentar biar kita bisa melihat dengan jelas kalau sudah masuk
        time.sleep(5) 
        
        print("✅ Berhasil masuk! Robot siap melakukan testing profil, like, atau scraping.")

        # ---- TULIS SKRIP TESTING/SCRAPING LU DI BAWAH SINI ---- #
        # Contoh: page.click("text=Messaging") 

        browser.close()

if __name__ == "__main__":
    jalankan_testing_tanpa_login()