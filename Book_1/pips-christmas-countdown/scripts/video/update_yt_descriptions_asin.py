"""
Update YouTube Descriptions for All 25 Shorts (Day 1 through Day 25)
Replaces the old ISBN link with the live Amazon ASIN link:
https://www.amazon.com/dp/B0HPZ647J6
"""
import sys
from google.oauth2.credentials import Credentials
from googleapiclient.discovery import build

TOKEN_PATH = r"C:\Users\movov\Videos\BlobbyWorld\blobby_pipeline\token.json"
OLD_URL = "https://www.amazon.com/dp/9798166809148"
NEW_URL = "https://www.amazon.com/dp/B0HPZ647J6"

ALL_VIDEO_IDS = [
    'SsBNKohRrVQ',  # Day 1
    'Hg896pYbok0',  # Day 2
    'xWBESnLYuvU',  # Day 3
    'mZRKEG0p5eQ',  # Day 4
    '2HX2XnZ4ans',  # Day 5
    'aGb3E-sbsds',  # Day 6
    'sbFLrgFZk1s',  # Day 7
    'SEPwWByfoXo',  # Day 8
    'qCix-WqnfLk',  # Day 9
    'l0P-jFi2bc0',  # Day 10
    '0pdyr_a4zYM',  # Day 11
    'A-uTsCjahTQ',  # Day 12
    '-yN7sHV2gu4',  # Day 13
    'vqs11QGmOpo',  # Day 14
    'gXvoOPQMUWo',  # Day 15
    '05_Z3pqcCbo',  # Day 16
    'c-UbLHKi51w',  # Day 17
    'WJFHdCR2_fA',  # Day 18
    'gTK73CpKuMc',  # Day 19
    'G0KbCJyKAaA',  # Day 20
    '2WFS-d5bYXo',  # Day 21
    '1p2SSdqkVm8',  # Day 22
    'qqW9APJdyqw',  # Day 23
    '9xGed4wuv_o',  # Day 24
    'cgOHoFYgH9k'   # Day 25
]

def update_descriptions():
    creds = Credentials.from_authorized_user_file(TOKEN_PATH, [
        'https://www.googleapis.com/auth/youtube.upload',
        'https://www.googleapis.com/auth/youtube'
    ])
    yt = build('youtube', 'v3', credentials=creds)

    print(f"Fetching details for {len(ALL_VIDEO_IDS)} videos...")
    res = yt.videos().list(part='snippet,status', id=','.join(ALL_VIDEO_IDS)).execute()
    items = res.get('items', [])
    print(f"Retrieved {len(items)} videos from YouTube API.")

    updated_count = 0
    for idx, item in enumerate(items, start=1):
        vid = item['id']
        snippet = item['snippet']
        desc = snippet.get('description', '')

        # Check if old URL is in description or needs update
        if OLD_URL in desc or NEW_URL not in desc:
            new_desc = desc.replace(OLD_URL, NEW_URL)
            if NEW_URL not in new_desc:
                new_desc += f"\n\nFull 110-page paperback on Amazon:\n{NEW_URL}"

            update_body = {
                'id': vid,
                'snippet': {
                    'title': snippet['title'],
                    'description': new_desc,
                    'categoryId': snippet.get('categoryId', '27'),
                    'tags': snippet.get('tags', [])
                }
            }
            yt.videos().update(part='snippet', body=update_body).execute()
            print(f"[{idx}/{len(items)}] Updated video {vid} with ASIN URL.")
            updated_count += 1
        else:
            print(f"[{idx}/{len(items)}] Video {vid} already has ASIN URL.")

    print(f"\n[COMPLETE] Successfully updated {updated_count} video descriptions.")

if __name__ == '__main__':
    update_descriptions()
