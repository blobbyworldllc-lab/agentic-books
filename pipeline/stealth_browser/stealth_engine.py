"""
Stealth Browser Core Engine
Provides realistic human interaction primitives, persistent profile handling,
and anti-detection evasion for unattended autonomous publishing.
"""
import os
import random
import time
from pathlib import Path
from playwright.sync_api import sync_playwright

REPO_ROOT = Path(__file__).resolve().parent.parent.parent
DEFAULT_PROFILES_DIR = REPO_ROOT / "pipeline" / "browser_profiles"
CHROME_PATH = r"C:\Program Files\Google\Chrome\Application\chrome.exe"

def human_delay(min_s=1.5, max_s=3.5):
    """Sleep with natural Gaussian jitter."""
    mean = (min_s + max_s) / 2.0
    stdev = (max_s - min_s) / 4.0
    delay = random.gauss(mean, stdev)
    delay = max(min_s, min(max_s, delay))
    time.sleep(delay)

def human_type(page, selector, text, min_delay=0.035, max_delay=0.095):
    """
    Type text into selector character-by-character with natural typing rhythms,
    variable inter-keystroke delays, and word boundary pauses.
    """
    loc = page.locator(selector).first
    loc.click()
    human_delay(0.3, 0.7)
    
    for i, ch in enumerate(text):
        page.keyboard.type(ch)
        # Add slight pause at punctuation or spaces
        if ch in " .,!?-":
            time.sleep(random.uniform(0.10, 0.22))
        else:
            time.sleep(random.uniform(min_delay, max_delay))
            
    human_delay(0.4, 0.8)

def human_click(page, selector, pre_delay=(0.4, 0.9), post_delay=(1.2, 2.5)):
    """Hover over target element, pause naturally, click, and settle."""
    loc = page.locator(selector).first
    loc.scroll_into_view_if_needed()
    human_delay(*pre_delay)
    loc.hover()
    human_delay(0.15, 0.35)
    loc.click()
    human_delay(*post_delay)

def human_scroll(page, steps=3, distance=250):
    """Scroll smoothly to mimic human browsing."""
    for _ in range(steps):
        delta = random.randint(distance - 50, distance + 50)
        page.mouse.wheel(0, delta)
        human_delay(0.6, 1.2)


class StealthBrowserEngine:
    def __init__(self, profile_name="default_profile", headless=True, width=1280, height=900):
        self.profile_name = profile_name
        self.profile_dir = DEFAULT_PROFILES_DIR / profile_name
        self.profile_dir.mkdir(parents=True, exist_ok=True)
        self.headless = headless
        self.width = width
        self.height = height
        self._pw = None
        self.context = None
        self.page = None

    def __enter__(self):
        self._pw = sync_playwright().start()
        
        args = [
            "--disable-blink-features=AutomationControlled",
            "--no-sandbox",
            "--disable-dev-shm-usage",
            "--disable-infobars",
            "--lang=en-US,en"
        ]
        
        executable = CHROME_PATH if os.path.exists(CHROME_PATH) else None
        
        self.context = self._pw.chromium.launch_persistent_context(
            user_data_dir=str(self.profile_dir),
            executable_path=executable,
            headless=self.headless,
            args=args,
            viewport={"width": self.width, "height": self.height},
            user_agent="Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/124.0.0.0 Safari/537.36"
        )
        
        self.page = self.context.pages[0] if self.context.pages else self.context.new_page()
        
        # Inject stealth scripts to erase automation signatures
        self.page.add_init_script("""
            Object.defineProperty(navigator, 'webdriver', { get: () => undefined });
            window.chrome = { runtime: {} };
            Object.defineProperty(navigator, 'languages', { get: () => ['en-US', 'en'] });
            Object.defineProperty(navigator, 'plugins', { get: () => [1, 2, 3, 4, 5] });
        """)
        
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        if self.context:
            self.context.close()
        if self._pw:
            self._pw.stop()
