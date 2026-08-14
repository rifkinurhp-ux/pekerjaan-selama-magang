from playwright.sync_api import sync_playwright

def simpan_sesi_full_otomatis():
    with sync_playwright() as p:
        # Membuka browser dalam mode headed dengan slow_mo untuk kestabilan ketikan
        browser = p.chromium.launch(headless=False, slow_mo=1000)
        
        context = browser.new_context()
        page = context.new_page()

        # Membuka halaman login LinkedIn
        print("Membuka halaman login LinkedIn...")
        page.goto("https://www.linkedin.com/login")

        # Mengisi Email menggunakan get_by_role textbox berdasarkan teks labelnya
        print("Mengisi Email atau Telepon...")
        page.get_by_role("textbox", name="Email or phone").fill("isi email")

        # Mengisi Password (Ganti "iiiii" dengan password LinkedIn asli lu)
        print("Mengisi Password...")
        page.get_by_role("textbox", name="Password").fill("isi password lu disini")

        # Klik tombol Sign in
        print("Mengklik tombol Sign in...")
        page.get_by_role("button", name="Sign in", exact=True).click()

        # Menunggu proses masuk ke Beranda dan menyimpan sesi secara otomatis
        print("Menunggu proses masuk ke Beranda...")
        try:
            page.wait_for_url("https://www.linkedin.com/feed/", timeout=30000)
            print("Login Berhasil dan masuk ke Beranda!")
            
            # Menyimpan sesi ke file JSON secara otomatis
            context.storage_state(path="linkedin_state.json")
            print("✅ Sesi berhasil disedot dan disimpan ke 'linkedin_state.json'!")
            
        except Exception:
            print("\n[PERINGATAN] Terdeteksi halaman verifikasi atau CAPTCHA oleh LinkedIn.")
            print("Silakan selesaikan CAPTCHA secara manual di browser, lalu sesi akan disimpan.")
            
            try:
                page.wait_for_url("https://www.linkedin.com/feed/", timeout=60000)
                context.storage_state(path="linkedin_state.json")
                print("✅ Sesi BERHASIL disimpan setelah verifikasi manual!")
            except:
                print("❌ Gagal masuk ke beranda dalam batas waktu yang ditentukan.")

        page.wait_for_timeout(3000)
        browser.close()

if __name__ == "__main__":
    simpan_sesi_full_otomatis()