import os
import subprocess
import time
from pathlib import Path
from playwright.sync_api import sync_playwright

cmd_u = '[System.Environment]::GetEnvironmentVariable("PINTEREST_USER", "User")'
cmd_p = '[System.Environment]::GetEnvironmentVariable("PINTEREST_PASS", "User")'
u = subprocess.check_output(["powershell", "-Command", cmd_u]).decode().strip()
p = subprocess.check_output(["powershell", "-Command", cmd_p]).decode().strip()

chrome_path = r"C:\Program Files\Google\Chrome\Application\chrome.exe"
image_path = str(Path(__file__).resolve().parent.parent.parent / "docs" / "pin_1_coloring_pages.png")
if not os.path.exists(image_path):
    image_path = str(Path(__file__).resolve().parent.parent.parent / "docs" / "cover.jpg")

title = "Pip's Christmas Countdown Coloring Book"
desc = "25 daily holiday rhymes and big bold coloring pages for kids ages 3-6! Follow Pip the baby penguin as he counts down to Christmas Day. Available now on Amazon Prime!"
link = "https://www.amazon.com/dp/B0HPZ647J6"

with sync_playwright() as pw:
    browser = pw.chromium.launch(executable_path=chrome_path, headless=True)
    context = browser.new_context(
        user_agent="Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/122.0.0.0 Safari/537.36",
        viewport={"width": 1280, "height": 900}
    )
    page = context.new_page()
    
    print("1. Logging into Pinterest...")
    page.goto("https://www.pinterest.com/login/")
    page.wait_for_timeout(2000)
    page.fill('input[id="email"]', u)
    page.fill('input[id="password"]', p)
    page.click('button[type="submit"]')
    page.wait_for_timeout(5000)
    print("Logged in! URL:", page.url)

    print("2. Navigating to Pin Creation Tool...")
    page.goto("https://www.pinterest.com/pin-creation-tool/")
    page.wait_for_timeout(5000)
    print("Builder URL:", page.url)
    page.screenshot(path=r"C:\Users\movov\.gemini\antigravity\brain\c985265e-3960-48cf-b104-dc69ade68dfa\scratch\pin_tool.png")

    # Upload image
    print("3. Uploading image asset...")
    file_input = page.locator('input[type="file"]')
    if file_input.count() > 0:
        file_input.first.set_input_files(image_path)
        print("[OK] Uploaded image!")
        page.wait_for_timeout(3000)

    # Fill Title
    print("4. Filling Title, Description, and Amazon Destination Link...")
    title_loc = page.locator('input[placeholder*="title"], textarea[placeholder*="title"], [data-test-id*="title"] input')
    if title_loc.count() > 0:
        title_loc.first.fill(title)
        print("[OK] Title filled.")

    desc_loc = page.locator('div[contenteditable="true"], textarea[placeholder*="description"]')
    if desc_loc.count() > 0:
        desc_loc.first.fill(desc)
        print("[OK] Description filled.")

    link_loc = page.locator('input[placeholder*="link"], input[id*="WebsiteField"]')
    if link_loc.count() > 0:
        link_loc.first.fill(link)
        print("[OK] Amazon URL filled.")

    page.wait_for_timeout(2000)
    page.screenshot(path=r"C:\Users\movov\.gemini\antigravity\brain\c985265e-3960-48cf-b104-dc69ade68dfa\scratch\pin_ready_to_save.png")

    # Select board if dropdown is present
    board_btn = page.locator('[data-test-id="board-dropdown-select-button"], button:has-text("Choose a board"), button:has-text("Children\'s Books")')
    if board_btn.count() > 0:
        board_btn.first.click()
        page.wait_for_timeout(1000)
        target_board = page.locator('text="Children\'s Books"')
        if target_board.count() > 0:
            target_board.first.click()
            print("[OK] Selected Children's Books board!")
            page.wait_for_timeout(1000)

    # Click Publish / Save
    print("5. Publishing Pin...")
    pub_btn = page.locator('[data-test-id="board-dropdown-save-button"], button:has-text("Publish"), button:has-text("Save")')
    if pub_btn.count() > 0:
        pub_btn.first.click()
        print("[OK] Clicked Publish button!")
        page.wait_for_timeout(5000)
        page.screenshot(path=r"C:\Users\movov\.gemini\antigravity\brain\c985265e-3960-48cf-b104-dc69ade68dfa\scratch\pin_live_result.png")
        print("[SUCCESS] Pin is published live on Pinterest!")

    browser.close()
