@echo off
cd /d "C:\Users\movov\Projects\agentic-books"
python -m pipeline.social.daily_video_syndicator >> "pipeline\social\syndication.log" 2>&1
