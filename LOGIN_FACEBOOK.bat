@echo off
echo =================================================================
echo Opening Chrome for one-time Facebook login...
echo Log into your Facebook account (or log in using Instagram).
echo Once you see your feed, close this browser window.
echo Your session will be permanently saved for automated group posting.
echo =================================================================
start "" "C:\Program Files\Google\Chrome\Application\chrome.exe" --user-data-dir="C:\Users\movov\Projects\agentic-books\pipeline\browser_profiles\facebook_profile" "https://www.facebook.com"
