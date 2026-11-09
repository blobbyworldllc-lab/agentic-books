@echo off
echo =================================================================
echo Opening Chrome for Amazon Author Central session...
echo Profile: pipeline\browser_profiles\amazon_author_profile
echo Target: https://author.amazon.com/
echo =================================================================
start "" "C:\Program Files\Google\Chrome\Application\chrome.exe" --user-data-dir="C:\Users\movov\Projects\agentic-books\pipeline\browser_profiles\amazon_author_profile" "https://author.amazon.com"
