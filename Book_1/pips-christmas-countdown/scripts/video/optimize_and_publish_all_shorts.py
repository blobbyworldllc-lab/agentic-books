"""
Optimize All 25 YouTube Shorts:
1. Updates Titles with high-converting, search-rich parenting hooks.
2. Updates Descriptions with direct Amazon Prime ASIN links + Free Printable Starter Pack links.
3. Sets Privacy to PUBLIC across all countdown shorts so they algorithmically index immediately.
"""
import sys
import time
from google.oauth2.credentials import Credentials
from googleapiclient.discovery import build

TOKEN_PATH = r"C:\Users\movov\Videos\BlobbyWorld\blobby_pipeline\token.json"
AMAZON_URL = "https://www.amazon.com/dp/B0HPZ647J6"
FREE_PACK_URL = "https://blobbyworldllc-lab.github.io/agentic-books/"

SHORT_TITLES = {
    1: "Day 1: Can Your Toddler Find the Star? Pip's Christmas Countdown #Shorts",
    2: "Day 2: Pip Goes Ice Skating! Toddler Christmas Activity #Shorts",
    3: "Day 3: Pip Decorates the Tree! Christmas Coloring for Kids #Shorts",
    4: "Day 4: Winter Sledding Adventure! Screen-Free Bedtime Routine #Shorts",
    5: "Day 5: Baking Christmas Cookies! Toddler Coloring Countdown #Shorts",
    6: "Day 6: Snowman Building Fun! Preschool Holiday Activity #Shorts",
    7: "Day 7: Cozy Holiday Bedtime! Seek & Find Christmas Story #Shorts",
    8: "Day 8: Christmas Eve Box Idea! Toddler Holiday Countdown #Shorts",
    9: "Day 9: Pip's Sledding Race! Christmas Coloring Book for Kids #Shorts",
    10: "Day 10: Hot Cocoa & Snowflakes! Quiet Time Activity Hack #Shorts",
    11: "Day 11: Finding Little Star! Preschool Observation Game #Shorts",
    12: "Day 12: Christmas Caroling Fun! Toddler Bedtime Countdown #Shorts",
    13: "Day 13: Building a Snow Fort! 25 Nights to Christmas #Shorts",
    14: "Day 14: Wrapping Holiday Gifts! Screen-Free Toddler Activity #Shorts",
    15: "Day 15: Winter Wonderland Walk! Christmas Coloring Pages #Shorts",
    16: "Day 16: Pip Meets Biscuit the Puppy! Holiday Activity Fun #Shorts",
    17: "Day 17: Hanging the Stockings! Christmas Countdown Book #Shorts",
    18: "Day 18: Ice Skating with Friends! Preschool Coloring Fun #Shorts",
    19: "Day 19: North Pole Mail Delivery! Holiday Story Coloring #Shorts",
    20: "Day 20: Christmas Light Glow! Toddler Quiet Time Coloring #Shorts",
    21: "Day 21: Singing Holiday Songs! Screen-Free Bedtime Routine #Shorts",
    22: "Day 22: The Cozy Fireplace! 25 Nights to Christmas #Shorts",
    23: "Day 23: Almost Christmas Eve! Find Little Star Game #Shorts",
    24: "Day 24: Christmas Eve Magic! Toddler Holiday Bedtime Story #Shorts",
    25: "Day 25: Merry Christmas, Pip! 50 Holiday Coloring Pages #Shorts"
}

DESCRIPTION_TEMPLATE = """Download the Free 4-Page Christmas Countdown Starter PDF:
👉 {free_pack}

Order the Full 110-Page Paperback on Amazon Prime (50 Designs + Seek & Find Game):
👉 {amazon_url}

Make December bedtime magical! 25 countdown nights + 25 bonus winter adventures featuring Pip the baby penguin and Biscuit the puppy. Every single page includes the "Find Little Star" observation game to keep little hands busy and screen-free all holiday season!

#ChristmasColoring #ToddlerActivities #PreschoolChristmas #ColoringBook #Shorts #ScreenFreeKids #AdventCalendar #ChristmasForKids
"""

# Live Video IDs mapped to Day number
DAY_TO_VID = {
    1: 'SsBNKohRrVQ',
    2: 'Hg896pYbok0',
    3: 'xWBESnLYuvU',
    4: 'mZRKEG0p5eQ',
    5: '2HX2XnZ4ans',
    6: '6YfrtBRPVMU',
    7: 'WcDDhIRW1Nc',
    8: '0NKyG6QnqXg',
    9: 'txPH06sWgeM',
    10: '-PPfi_siVEA',
    11: '8X4UzGLkzcE',
    12: 'Thz0j_nOpGI',
    13: '-yN7sHV2gu4',
    14: 'vqs11QGmOpo',
    15: 'gXvoOPQMUWo',
    16: '05_Z3pqcCbo',
    17: 'c-UbLHKi51w',
    18: 'WJFHdCR2_fA',
    19: 'gTK73CpKuMc',
    20: 'G0KbCJyKAaA',
    21: '2WFS-d5bYXo',
    22: '1p2SSdqkVm8',
    23: 'qqW9APJdyqw',
    24: '9xGed4wuv_o',
    25: 'cgOHoFYgH9k'
}

def optimize_all():
    creds = Credentials.from_authorized_user_file(TOKEN_PATH, [
        'https://www.googleapis.com/auth/youtube.upload',
        'https://www.googleapis.com/auth/youtube'
    ])
    yt = build('youtube', 'v3', credentials=creds)

    print(f"Starting metadata optimization & public publishing for {len(DAY_TO_VID)} shorts...", flush=True)
    desc_content = DESCRIPTION_TEMPLATE.format(free_pack=FREE_PACK_URL, amazon_url=AMAZON_URL)

    updated_count = 0
    for day, vid in sorted(DAY_TO_VID.items()):
        new_title = SHORT_TITLES[day]
        print(f"\n[Day {day}] Video ID: {vid}", flush=True)
        try:
            # 1. Update snippet (Title, Description, Tags)
            yt.videos().update(
                part='snippet',
                body={
                    'id': vid,
                    'snippet': {
                        'title': new_title,
                        'description': desc_content,
                        'categoryId': '27',  # Education
                        'tags': [
                            'Christmas Coloring', 'Toddler Activities', 'Preschool Christmas',
                            'Coloring Book for Kids', 'Shorts', 'Screen Free', 'Christmas Countdown',
                            'Find Little Star', 'Advent Calendar for Kids'
                        ]
                    }
                }
            ).execute()
            print(f"  [OK] Updated Title: {new_title}", flush=True)

            # 2. Update status to PUBLIC
            yt.videos().update(
                part='status',
                body={
                    'id': vid,
                    'status': {
                        'privacyStatus': 'public',
                        'selfDeclaredMadeForKids': True
                    }
                }
            ).execute()
            print(f"  [OK] Flipped to PUBLIC", flush=True)
            updated_count += 1
            time.sleep(1.0)
        except Exception as e:
            print(f"  [ERROR] Failed to update Day {day} ({vid}): {e}", flush=True)

    print(f"\n=== Successfully optimized & published {updated_count}/25 YouTube Shorts LIVE! ===", flush=True)

if __name__ == '__main__':
    optimize_all()
