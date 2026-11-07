@echo off
cd /d "C:\Users\movov\Projects\agentic-books"
python pipeline\stealth_browser\stealth_daemon.py --once >> pipeline\growth\stealth_daemon.log 2>&1
