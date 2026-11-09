# Agent instructions (Gemini, Antigravity, any AI)

Read `pipeline/AUTOPILOT.md` first: it is the single source of truth for the book pipeline. Book details: `Book_1/pips-christmas-countdown/PROJECT.md`.

## Universal Hard Rules & Sync Rules (Zero Exceptions, All AIs)

1. **Mandatory Git Commit & Push (Universal Hard Rule)**:
   - Start every session with `git pull --rebase --autostash origin main`.
   - Before ending any turn or completing any task, **ALWAYS** commit and push all changes immediately to remote GitHub (`git push origin main`). Never force-push. Never leave uncommitted changes or unpushed commits.
   - Never commit tokens, credentials, logs, `*_token.json`, or `fb_config.json`.

2. **Autonomous Human-Style Web Execution & Anti-Bot Interval Pacing (Universal Hard Rule - Never Ask User)**:
   - **Never Ask the User**: Any website interaction (login, posting, claiming, form completion, media upload, account setup) must be handled autonomously by the agent in human style without ever asking or burdening the user.
   - **Strict Human Cadence Simulation**: Always interact using human-style typing cadence (character-by-character with 35–110ms jitter and word boundary/punctuation pauses), realistic mouse hovers and clicks, and smooth scrolling. Automation signatures (`navigator.webdriver`) must always be masked.
   - **Random Non-Uniform Intervals (Anti-Bot Detection)**: All scheduled web routines, community distribution, and API/browser actions MUST run with randomized, non-uniform intervals (e.g. 20–100 minute random deltas or Gaussian jitter) and strict daily caps so zero bot, automation, or rate-limit detection is triggered.

3. **Autonomous Command & Scratch Script Policy**:
   - The user operates in Turbo Mode with full autonomous execution.
   - Agents must never generate ad-hoc multiline `python -c "..."` command-line one-liners, which trigger interactive security confirmations for new strings.
   - Instead, write one-off diagnostic or test code directly into `<appDataDir>\brain\<conversation-id>/scratch/` files or use native file tools (`view_file`, `write_to_file`, `replace_file_content`, `list_dir`, `grep_search`) to ensure completely uninterrupted autonomous execution.

4. **Universal Dynamic Video Standard (Zero Static Page Exposures & Pure Soothing Music)**:
   - Every promotional video across all channels (YouTube Shorts, Instagram Reels, TikTok, Facebook, Pinterest) for ANY book must feature real moving 3D character animation or active drawing/coloring/printing motion. Never expose raw static interior book pages on screen as video slides.
   - The video must seamlessly crossfade (0.5s dissolve) into a dynamic Amazon Call-to-Action Outro card generated dynamically via `pipeline/growth/dynamic_video_engine.py`.
   - The card dynamically binds to the specific book's ASIN (`amazon.com/dp/{asin}`), Title, Subtitle, Bullet Highlights, and Golden "BUY NOW ON AMAZON" button.
   - Audio must remain 100% pure, uninterrupted, soothing background music box chimes with ZERO spoken voiceover intrusion (preserving the calm bedtime atmosphere and preventing viewer sales resistance).

5. **Mandatory Dynamic Amazon Buy Links on ALL Social Posts (Zero Exceptions)**:
   - Every promotional post across ALL platforms (including Instagram, Threads, Facebook, X, Pinterest, YouTube, TikTok) for ANY book must contain the prominent direct Amazon purchase link (`https://www.amazon.com/dp/{asin}`) in the post description/caption AND a dedicated comment containing the direct Amazon purchase link.

6. **Table & Color-Coded Tick Mark Formatting**:
   - Always format explanations, status reports, and execution summaries in structured markdown tables with color-coded tick marks (✅ Green, 🟡 Yellow, ❌ Red) for instant clarity.

7. **Pipeline Ownership & Sync**:
   - The scheduled cloud runs (Fri 6:07pm and 9:07pm ET, Sat 7:07am to 10:07pm ET) own `pipeline/state.json` and book creation. Do not start a competing book cycle; do not edit `state.json` stages by hand.
   - Laptop-owned jobs (Windows Task Scheduler, zero tokens): `AgenticBooks_LaunchWatcher` (every 30 min) and `AgenticBooks_SalesMonitor` (daily is enough; the script self-throttles to one check per 20+ hours). Any change to these scripts goes through git, not only local edits.
   - `pipeline/social/buffer_dispatcher.py` holds the Book 1 payload only; never rerun it for another book. Each book gets its own payload.
   - Hard prohibitions: no ads or spending, no account creation, no passwords or CAPTCHAs, no review incentives, no famous characters or trademarks.
   - Update the status log in `PROJECT.md` and `pipeline/state.json` notes after any change that affects the pipeline.
