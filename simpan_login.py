from playwright.sync_api import sync_playwright

def simpan_sesi_linkedin():
    with sync_playwright() as p:
        # Buka browser secara visual
        browser = p.chromium.launch(headless=False)
        context = browser.new_context()
        page = context.new_page()

        # Buka halaman login
        print("Membuka halaman LinkedIn...")
        page.goto("https://www.linkedin.com/login")

        print("SILAKAN LOGIN SECARA MANUAL DI BROWSER YANG TERBUKA.")
        print("Selesaikan CAPTCHA atau kode OTP jika diminta.")
        print("Menunggu hingga Anda masuk ke halaman utama (Feed)...")

        # Skrip akan menunggu (maksimal 2 menit) sampai URL berubah menjadi /feed/
        page.wait_for_url("https://www.linkedin.com/feed/", timeout=120000)

        # Jika sudah masuk feed, simpan tiket/sesinya ke file JSON
        context.storage_state(path="linkedin_state.json")
        print("Status login berhasil disimpan ke 'linkedin_state.json'!")

        browser.close()

if __name__ == "__main__":
    simpan_sesi_linkedin()