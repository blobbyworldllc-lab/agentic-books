import os
import subprocess
import time
from pathlib import Path
from playwright.sync_api import sync_playwright

def get_env_var(name):
    val = os.environ.get(name)
    if not val:
        try:
            cmd = f'[System.Environment]::GetEnvironmentVariable("{name}", "User")'
            val = subprocess.check_output(["powershell", "-Command", cmd]).decode().strip()
        except Exception:
            pass
    return val

def publish_pin():
    user = get_env_var("PINTEREST_USER")
    password = get_env_var("PINTEREST_PASS")
    
    if not user or not password:
        print("[ERROR] Missing PINTEREST_USER or PINTEREST_PASS in environment.")
        return

    print(f"Logging into Pinterest as {user}...")
    image_path = str(Path(__file__).resolve().parent.parent.parent / "docs" / "pin_1_coloring_pages.png")
    if not os.path.exists(image_path):
        image_path = str(Path(__file__).resolve().parent.parent.parent / "docs" / "cover.jpg")
    print(f"Using image asset: {image_path}")

    title = "Pip's Christmas Countdown Coloring Book"
    desc = "25 daily holiday rhymes and big, bold coloring pages for kids ages 3-6! Follow Pip the puppy as he counts down to Christmas Day. Available now on Amazon Prime!"
    link = "https://www.amazon.com/dp/B0HPZ647J6"

    chrome_path = r"C:\Program Files\Google\Chrome\Application\chrome.exe"

    with sync_playwright() as p:
        browser = p.chromium.launch(
            executable_path=chrome_path,
            headless=True,
            args=["--no-sandbox", "--disable-dev-shm-usage"]
        )
        context = browser.new_context(
            user_agent="Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/122.0.0.0 Safari/537.36",
            viewport={"width": 1280, "height": 800}
        )
        page = context.new_page()

        print("Navigating to Pinterest login...")
        page.goto("https://www.pinterest.com/login/", timeout=30000)
        page.wait_for_timeout(3000)

        # Enter credentials
        page.fill('input[id="email"]', user)
        page.fill('input[id="password"]', password)
        page.wait_for_timeout(1000)
        page.click('button[type="submit"]')
        print("Submitted login form. Waiting for navigation...")

        page.wait_for_timeout(6000)
        print(f"Current URL after login: {page.url}")
        page.screenshot(path=r"C:\Users\movov\.gemini\antigravity\brain\c985265e-3960-48cf-b104-dc69ade68dfa\scratch\pinterest_after_login.png")

        # Navigate to pin creation
        print("Navigating to Pin Creation builder...")
        page.goto("https://www.pinterest.com/pin-creation-tool/", timeout=30000)
        page.wait_for_timeout(4000)
        print(f"Pin builder URL: {page.url}")
        page.screenshot(path=r"C:\Users\movov\.gemini\antigravity\brain\c985265e-3960-48cf-b104-dc69ade68dfa\scratch\pin_builder.png")

        # Upload file
        file_input = page.locator('input[type="file"]')
        if file_input.count() > 0:
            file_input.first.set_input_files(image_path)
            print("[OK] Uploaded pin image file.")
            page.wait_for_timeout(2000)
        else:
            print("File input not found directly, checking dropzone.")

        # Fill Title
        title_box = page.locator('textarea[id*="storyboard-selector-title"], input[placeholder*="Add a title"], [data-test-id*="pin-draft-title"] input, textarea[placeholder*="title"]')
        if title_box.count() > 0:
            title_box.first.fill(title)
            print("[OK] Filled title.")

        # Fill Description
        desc_box = page.locator('div[contenteditable="true"], textarea[placeholder*="description"], [data-test-id*="pin-draft-description"] textarea')
        if desc_box.count() > 0:
            desc_box.first.fill(desc)
            print("[OK] Filled description.")

        # Fill Link
        link_box = page.locator('input[placeholder*="link"], input[id*="WebsiteField"], [data-test-id*="pin-draft-link"] input')
        if link_box.count() > 0:
            link_box.first.fill(link)
            print("[OK] Filled destination link.")

        page.wait_for_timeout(2000)
        page.screenshot(path=r"C:\Users\movov\.gemini\antigravity\brain\c985265e-3960-48cf-b104-dc69ade68dfa\scratch\pin_filled.png")

        # Click Publish / Save
        publish_btn = page.locator('button:has-text("Publish"), button:has-text("Save"), [data-test-id="board-dropdown-save-button"]')
        if publish_btn.count() > 0:
            publish_btn.first.click()
            print("[OK] Clicked Publish/Save button.")
            page.wait_for_timeout(5000)
            page.screenshot(path=r"C:\Users\movov\.gemini\antigravity\brain\c985265e-3960-48cf-b104-dc69ade68dfa\scratch\pin_published.png")
            print("[SUCCESS] Pin published successfully to Pinterest!")
        else:
            print("Publish button not found, saving state.")

        browser.close()

if __name__ == "__main__":
    publish_pin()
