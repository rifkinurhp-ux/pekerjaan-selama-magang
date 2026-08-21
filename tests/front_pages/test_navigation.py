import json
import os
import time

import pytest
from pages.front_pages.choose_company_page import ChooseCompanyPage
from pages.front_pages.login_page import LoginPage
from pages.front_pages.sidebar_page import SidebarPage

MENUS = [
    "Sales Order Suites",
    "Delivery & Return",
    "NOO",
    "Master Data",
    "Matrix Kecil",
    "Matrix Besar Configuration",
    "Reporting",
    "Configuration",
    "Collection",
    "Supplier Claim",
    "Finance",
    "Administration",
    "Logs",
    "Document Utilities",
    "Inventory",
]

# Progress checkpoint: sub-menu yang sudah pernah OK di run sebelumnya
# di-skip di run berikutnya, jadi test ini tidak mulai dari nol tiap kali
# dijalankan. Item yang gagal (atau belum pernah dicek) selalu dicoba lagi.
# Set RESET_NAV_STATE=true untuk paksa cek ulang semuanya dari awal.
STATE_PATH = "screenshots/navigation/_state.json"
RESET_STATE = os.getenv("RESET_NAV_STATE", "false").lower() == "true"


def _load_state() -> dict:
    if RESET_STATE or not os.path.exists(STATE_PATH):
        return {}
    try:
        with open(STATE_PATH) as f:
            return json.load(f).get("items", {})
    except (json.JSONDecodeError, OSError):
        return {}


def _save_state(items: dict) -> None:
    os.makedirs(os.path.dirname(STATE_PATH), exist_ok=True)
    with open(STATE_PATH, "w") as f:
        json.dump({"items": items}, f, indent=2, ensure_ascii=False)


def _login_and_enter(driver, base_url, username, password, company_name):
    login = LoginPage(driver, base_url)
    login.open_login()
    login.login(username, password)
    login.wait_for_redirect()

    company = ChooseCompanyPage(driver, base_url)
    company.wait_until_loaded()
    company.select_company_by_text(company_name)
    company.click_continue()


@pytest.mark.regression
def test_navigate_all_menus(login_creds, base_url, test_company, driver):
    username, password = login_creds
    _login_and_enter(driver, base_url, username, password, test_company)

    sidebar = SidebarPage(driver, base_url)
    sidebar.wait_until_loaded()

    os.makedirs("screenshots/navigation", exist_ok=True)
    state = _load_state()

    # Phase 1: kumpulin semua sub-menu URL per menu (tanpa navigasi).
    # Kalau satu menu gagal dibuka, dicatat sebagai error tapi menu lain
    # tetap lanjut dikumpulkan — bukan langsung menggagalkan seluruh test.
    menu_map: dict[str, list[dict]] = {}
    collect_errors = []
    for menu_name in MENUS:
        try:
            sidebar.click_menu(menu_name)
            menu_map[menu_name] = sidebar.get_visible_submenus()
            sidebar.click_menu(menu_name)  # collapse kembali
        except Exception as exc:  # noqa: BLE001
            collect_errors.append(f"{menu_name}: gagal buka menu ({exc})")
            menu_map[menu_name] = []

    # Phase 2: navigate ke tiap URL.
    # - Sub-menu yang statusnya "ok" di checkpoint sebelumnya di-skip.
    # - State ditulis ke disk setiap SATU item selesai dicek (bukan cuma
    #   di akhir), jadi kalau test ini crash/di-interrupt di tengah jalan,
    #   run berikutnya lanjut dari sisa yang belum "ok" — tidak mulai dari
    #   menu pertama lagi.
    # - Exception per-item ditangkap supaya satu halaman rusak tidak
    #   menggagalkan seluruh test, cukup menandai item itu "fail".
    failures = list(collect_errors)
    checked = 0
    skipped = 0

    for menu_name, submenus in menu_map.items():
        print(f"\n{'='*50}")
        print(f"[MENU] {menu_name} ({len(submenus)} sub-menu)")

        if not submenus:
            print("  (tidak ada sub-menu)")
            continue

        for sub in submenus:
            href = sub["href"]
            prev = state.get(href)

            if prev and prev.get("status") == "ok":
                print(f"  [SKIP] sudah OK sebelumnya -> [{sub['text']}] {href}")
                skipped += 1
                continue

            print(f"  -> [{sub['text']}] {href}")
            checked += 1
            try:
                sidebar.navigate_to(sub["full_url"])
                sidebar.wait_until_loaded(timeout=8)

                slug = href.strip("/").replace("/", "_")
                driver.save_screenshot(f"screenshots/navigation/{slug}.png")

                if sidebar.current_page_has_error():
                    raise AssertionError("halaman menunjukkan error/404")

                state[href] = {
                    "menu": menu_name,
                    "text": sub["text"],
                    "status": "ok",
                    "checked_at": time.strftime("%Y-%m-%d %H:%M:%S"),
                }
                print(f"  [OK] {driver.current_url}")
            except Exception as exc:  # noqa: BLE001
                msg = f"{menu_name} > {sub['text']} ({href}): {exc}"
                state[href] = {
                    "menu": menu_name,
                    "text": sub["text"],
                    "status": "fail",
                    "error": str(exc),
                    "checked_at": time.strftime("%Y-%m-%d %H:%M:%S"),
                }
                print(f"  [FAIL] {msg}")
                failures.append(msg)
            finally:
                _save_state(state)

    print(f"\n{'='*50}")
    print(f"Selesai: {checked} dicek, {skipped} di-skip (sudah OK), {len(failures)} gagal.")

    if failures:
        pytest.fail(
            f"{len(failures)} halaman bermasalah "
            "(jalankan ulang test ini untuk retry — yang sudah OK otomatis "
            "di-skip, hanya yang gagal yang dicoba lagi):\n" + "\n".join(failures)
        )
