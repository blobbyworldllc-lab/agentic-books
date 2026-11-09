# Agent instructions (laptop agent, Claude, Gemini, Antigravity, Cursor, Copilot, any AI)

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

4. **Real Moving 3D Character Animation Only (Zero Static Page Exposures)**:
   - Every promotional video across all channels (YouTube Shorts, Instagram Reels, TikTok, Facebook, Pinterest) MUST feature real moving 3D character animation (e.g. Pip sledding, ice skating, decorating the tree) or active drawing/coloring/printing motion.
   - Never expose raw static book/coloring pages on screen as video slides.
   - Every video must conclude with the festive Amazon call-to-action outro card and voiceover: *"Check the description to buy our book on Amazon!"*.

5. **Mandatory Amazon Buy Links on ALL Social Posts (Zero Exceptions)**:
   - Every promotional post across ALL platforms (including Instagram, Threads, Facebook, X, Pinterest, YouTube, TikTok) for ANY book must contain the prominent direct Amazon purchase link in the post description/caption AND a dedicated comment containing the direct Amazon purchase link (`https://www.amazon.com/dp/B0HPZ647J6`).

6. **Table & Color-Coded Tick Mark Formatting**:
   - Always format explanations, status reports, and execution summaries in structured markdown tables with color-coded tick marks (✅ Green, 🟡 Yellow, ❌ Red) for instant clarity.

7. **Pipeline Ownership & Sync**:
   - The scheduled cloud runs (Fri 6:07pm and 9:07pm ET, Sat 7:07am to 10:07pm ET) own `pipeline/state.json` and book creation. Do not start a competing book cycle; do not edit `state.json` stages by hand.
   - Laptop-owned jobs (Windows Task Scheduler, zero tokens): `AgenticBooks_LaunchWatcher` (every 30 min) and `AgenticBooks_SalesMonitor` (daily is enough; the script self-throttles to one check per 20+ hours). Any change to these scripts goes through git, not only local edits.
   - `pipeline/social/buffer_dispatcher.py` holds the Book 1 payload only; never rerun it for another book. Each book gets its own payload.
   - Hard prohibitions: no ads or spending, no account creation, no passwords or CAPTCHAs, no review incentives, no famous characters or trademarks.
   - Update the status log in `PROJECT.md` and `pipeline/state.json` notes after any change that affects the pipeline.
