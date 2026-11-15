@echo off
cd /d "C:\Users\movov\Projects\agentic-books"
python pipeline\stealth_browser\stealth_daemon.py --min-gap-minutes 5.0 --max-gap-minutes 20.0
