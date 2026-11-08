@echo off
echo =================================================================
echo Opening Chrome for one-time Reddit login...
echo Log into your Reddit account.
echo Once you see your feed, close this browser window.
echo Your session will be permanently saved for autonomous community distribution.
echo =================================================================
start "" "C:\Program Files\Google\Chrome\Application\chrome.exe" --user-data-dir="C:\Users\movov\Projects\agentic-books\pipeline\browser_profiles\reddit_profile" "https://www.reddit.com/login"
