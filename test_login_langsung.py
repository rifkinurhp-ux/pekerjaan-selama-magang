from playwright.sync_api import sync_playwright, expect


def test_login_langsung():
    with sync_playwright() as p:
        # Membuka browser dalam mode headed
        browser = p.chromium.launch(headless=False, slow_mo=1000)
        
        context = browser.new_context()
        page = context.new_page()

        # Membuka halaman login LinkedIn
        print("Membuka halaman login LinkedIn...")
        page.goto("https://www.linkedin.com/login")

        # Mengisi Email menggunakan get_by_role textbox berdasarkan teks labelnya
        print("Mengisi Email atau Telepon...")
        page.get_by_role("textbox", name="Email or phone").fill("rifkinurh.p@gmail.com")

        # Mengisi Password menggunakan get_by_role textbox berdasarkan teks labelnya
        print("Mengisi Password...")
        page.get_by_role("textbox", name="Password").fill("iiiii")

        # Klik tombol Sign in
        print("Mengklik tombol Sign in...")
        page.get_by_role("button", name="Sign in", exact=True).click()

        # Menunggu proses masuk ke Beranda
        print("Menunggu proses masuk ke Beranda...")
        try:
            page.wait_for_url("https://www.linkedin.com/feed/", timeout=15000)
            print("Login Berhasil dan masuk ke Beranda!")
        except Exception:
            print("\n[PERINGATAN] Terdeteksi halaman verifikasi atau CAPTCHA oleh LinkedIn.")

        page.wait_for_timeout(5000)
        browser.close()

if __name__ == "__main__":
    test_login_langsung()