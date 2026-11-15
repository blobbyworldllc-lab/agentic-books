# Google Cloud VM Deployment & Cloud Distribution Engine
**Project:** Agentic Books (Pip's Christmas Countdown)  
**Target:** 24/7 Autonomous Community Seeding & Pinterest Video Pinning  
**Pacing:** Random intervals between **5 to 20 minutes** (up to 20 posts/day) with legitimate community karma warmup.

---

## 1. Google VM Specifications
Any standard small Google Cloud Compute Engine instance works:
* **Machine Type:** `e2-medium` (2 vCPU, 4GB RAM) or `e2-small` (2 vCPU, 2GB RAM with swap).
* **OS:** Ubuntu 22.04 LTS or Debian 12.
* **Disk:** 20 GB standard persistent disk.
* **Firewall / Network:** Default allow outbound HTTPS (443). No inbound public ports required.

---

## 2. Fast 3-Step Setup on Google Cloud VM

### Step 1: Clone Repository & Run Automated Setup
SSH into your Google Cloud VM and run:
```bash
# Clone the repository
git clone https://github.com/blobbyworldllc-lab/agentic-books.git ~/agentic-books
cd ~/agentic-books

# Run automated dependency & Playwright installer
chmod +x pipeline/deploy/setup_google_vm.sh
./pipeline/deploy/setup_google_vm.sh
```

### Step 2: Transfer Authenticated Browser Sessions
To allow the VM to post to your Facebook groups and Pinterest boards without triggering fresh login screens or CAPTCHAs, transfer your session bundle:

**On your laptop (PowerShell):**
```powershell
cd C:\Users\movov\Projects\agentic-books
python pipeline\deploy\export_profiles.py
gcloud compute scp pipeline\deploy\browser_sessions_bundle.tar.gz <YOUR_VM_NAME>:~/agentic-books/pipeline/deploy/ --zone=<YOUR_VM_ZONE>
```

**On the Google VM (SSH):**
```bash
cd ~/agentic-books
source .venv/bin/activate
python pipeline/deploy/import_profiles.py
```

### Step 3: Install & Start Systemd 24/7 Background Service
```bash
# Configure systemd service with your VM user and project path
sed -i "s|%USER%|$(whoami)|g" pipeline/deploy/agentic-books-distribution.service
sed -i "s|%PROJECT_DIR%|$(pwd)|g" pipeline/deploy/agentic-books-distribution.service

# Install and enable the service
sudo cp pipeline/deploy/agentic-books-distribution.service /etc/systemd/system/
sudo systemctl daemon-reload
sudo systemctl enable agentic-books-distribution
sudo systemctl start agentic-books-distribution

# Check live service status and streaming logs
sudo systemctl status agentic-books-distribution
tail -f pipeline/growth/stealth_daemon.log
```

---

## 3. How Posts Are Protected from Removal (Automated Legitimacy Protocol)

Group administrators and auto-moderators remove posts when accounts behave like bots (drop-and-run links). The engine prevents removal using a **3-stage authentic member warmup**:

```
[ Step 1: Screening Questions ]
 └── Automatically answers questions ("Toddler & preschooler mom", "Agree to rules")
               │
               ▼
[ Step 2: Pre-Post Karma Warmup ]
 └── Scrolls feed -> Likes 2-3 existing posts -> Leaves genuine supportive comment on another parent's post
               │
               ▼
[ Step 3: Value Lead Magnet ]
 └── Posts 100% free 4-page printable countdown pack (Zero sales jargon; Amazon $7.99 Prime link in footer)
```

1. **Automated Screening Question Answering:**
   - Detects dialog questionnaires when joining new groups.
   - Fills thoughtful parent/teacher answers (`community_warmup_engine.py`) and checks all rule agreements.
2. **Pre-Post Karma Warmup:**
   - Before opening the post composer, the browser scrolls the feed, likes 2–3 active member posts, and leaves an encouraging comment (*"Such a wonderful holiday idea, saving this for our quiet time!"*).
   - This ensures the account carries an active member engagement history before posting.
3. **Random Non-Uniform Intervals (5 to 20 Minutes):**
   - After each distribution cycle, the engine calculates:
     `gap_minutes = random.uniform(5.0, 20.0)`
   - It pauses for that exact duration (e.g., 6.8m, 14.1m, 19.3m, 8.5m), completely defeating bot pattern detection.

---

## 4. Prompt to Paste into an AI Agent Running Inside the Google VM

If you run an AI agent (Claude Code, Gemini, Antigravity, Cursor) directly on the Google Cloud VM, paste this exact turnkey prompt:

```text
You are the autonomous distribution manager for the Agentic Books project (book: "Pip's Christmas Countdown", ASIN B0HPZ647J6).
Working directory: ~/agentic-books

Your mission:
1. Ensure the Python virtual environment (.venv) has all dependencies and Playwright Chromium installed.
2. Verify that authenticated browser profiles exist in pipeline/browser_profiles/ for Facebook and Pinterest.
3. Manage the background stealth distribution daemon (pipeline/stealth_browser/stealth_daemon.py).
   - Enforce randomized intervals between 5 to 20 minutes (never fixed).
   - Cap total distributions at 20 per day.
   - Strictly enforce the moving 3D video standard (pip_sledding_amazon_short.mp4, etc.) and the free 4-page printable lead magnet (https://blobbyworldllc-lab.github.io/agentic-books/). Never expose raw static interior book pages.
   - Execute the authentic member karma warmup (pipeline/stealth_browser/community_warmup_engine.py) before posting to Facebook groups to protect against post removal.
4. Keep the systemd service (agentic-books-distribution.service) active and verify that pipeline/growth/stealth_daemon.log is recording successful live cycles.
5. Always run pytest tests/ before committing any changes and push all updates to origin main.
```
