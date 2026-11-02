@echo off
cd /d "C:\Users\movov\Projects\agentic-books"
python pipeline\sales_monitor.py >> sales_monitor.log 2>&1
