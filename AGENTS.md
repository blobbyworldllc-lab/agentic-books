# Agent instructions (laptop agent, Claude, any AI)

Read `pipeline/AUTOPILOT.md` first: it is the single source of truth for the book pipeline. Book details: `Book_1/pips-christmas-countdown/PROJECT.md`.

Sync rules (so the laptop agent and the scheduled cloud runs never diverge):
1. Start every session with `git pull --rebase --autostash origin main`; end with commit of explicit paths and `git push origin main`. Never force-push. Never commit tokens, logs, or `*_token.json` / `fb_config.json`.
2. The scheduled cloud runs (Fri 6:07pm and 9:07pm ET, Sat 7:07am to 10:07pm ET) own `pipeline/state.json` and book creation. Do not start a competing book cycle; do not edit `state.json` stages by hand.
3. Laptop-owned jobs (Windows Task Scheduler, zero tokens): `AgenticBooks_LaunchWatcher` (every 30 min) and `AgenticBooks_SalesMonitor` (daily is enough; the script self-throttles to one check per 20+ hours). Any change to these scripts goes through git, not only local edits.
4. `pipeline/social/buffer_dispatcher.py` holds the Book 1 payload only; never rerun it for another book. Each book gets its own payload.
5. Hard prohibitions: no ads or spending, no account creation, no passwords or CAPTCHAs, no review incentives, no famous characters or trademarks.
6. Update the status log in `PROJECT.md` and `pipeline/state.json` notes after any change that affects the pipeline.
7. Mandatory Amazon Buy Links on ALL Social Posts (Zero Exceptions): Every promotional post across ALL platforms (including Instagram, Threads, Facebook, X, Pinterest, YouTube, TikTok) for ANY book must contain the prominent direct Amazon purchase link in the post description/caption AND a dedicated comment containing the direct Amazon purchase link.
