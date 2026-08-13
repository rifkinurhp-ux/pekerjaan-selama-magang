from playwright.sync_api import sync_playwright, expect

def test_beranda_linkedin():
    with sync_playwright() as p:
        # Buka browser secara visual
        browser = p.chromium.launch(headless=False, slow_mo=500)
        
        # SUNTIKKAN FILE SESI YANG DISIMPAN SEBELUMNYA
        # Ini akan melewati proses login sepenuhnya!
        context = browser.new_context(storage_state="linkedin_state.json")
        page = context.new_page()

        print("Mengakses LinkedIn dengan status sudah login...")
        page.goto("https://www.linkedin.com/feed/")

        # --- MULAI PENGUJIAN (ASSERTIONS) ---
        print("Memverifikasi apakah kita berhasil masuk ke beranda...")
        
        # 1. Memastikan elemen navigasi utama terlihat (menandakan halaman termuat)
        navigasi = page.get_by_role("navigation").first
        expect(navigasi).to_be_visible()
        
        # 2. Mengecek apakah URL benar-benar ada di /feed/
        expect(page).to_have_url("https://www.linkedin.com/feed/")
        
        print("Pengujian Berhasil: Otomatis masuk ke Beranda tanpa mengetik password!")

        # Jeda 5 detik agar Anda bisa melihat hasilnya sebelum tertutup otomatis
        page.wait_for_timeout(5000)
        
        browser.close()

if __name__ == "__main__":
    test_beranda_linkedin()