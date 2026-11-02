"""Zero-token launch watcher. Run on the laptop every 30 min (Windows Task Scheduler).
For each Book_*/*/launch_manifest.json with live=false: checks whether the book is live on Amazon,
records the ASIN, flips listed YouTube videos to public, commits and pushes the manifest/catalog.
Usage: python launch_watcher.py [--repo PATH] [--token PATH]
"""
import argparse, html, json, re, subprocess, sys, urllib.request
from pathlib import Path

UA = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 Chrome/120 Safari/537.36',
      'Accept-Language': 'en-US,en;q=0.9'}

def get(url):
    try:
        with urllib.request.urlopen(urllib.request.Request(url, headers=UA), timeout=20) as r:
            return html.unescape(r.read().decode('utf-8', 'ignore'))
    except Exception:
        return ''

def find_asin(isbn13, title):
    page = get(f'https://www.amazon.com/s?k={isbn13}')
    if 'captcha' in page.lower() or 'robot check' in page.lower():
        return None
    for m in re.finditer(r'data-asin="([A-Z0-9]{10})"', page):
        asin = m.group(1)
        prod = get(f'https://www.amazon.com/dp/{asin}')
        if title in prod and ('id="productTitle"' in prod or 'add-to-cart-button' in prod):
            return asin
    return None

def youtube_public(ids, token):
    from google.oauth2.credentials import Credentials
    from googleapiclient.discovery import build
    scopes = ['https://www.googleapis.com/auth/youtube.upload', 'https://www.googleapis.com/auth/youtube']
    yt = build('youtube', 'v3', credentials=Credentials.from_authorized_user_file(token, scopes))
    for vid in ids:
        yt.videos().update(part='status', body={'id': vid, 'status': {'privacyStatus': 'public', 'selfDeclaredMadeForKids': True}}).execute()

def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('--repo', default=str(Path(__file__).resolve().parent.parent))
    ap.add_argument('--token', default=r'C:\Users\movov\Videos\BlobbyWorld\blobby_pipeline\token.json')
    a = ap.parse_args()
    repo = Path(a.repo)
    subprocess.run(['git', 'pull', '--rebase', 'origin', 'main'], cwd=repo, capture_output=True)
    changed = []
    for mf in repo.glob('Book_*/*/launch_manifest.json'):
        m = json.loads(mf.read_text(encoding='utf-8'))
        if m.get('live'):
            continue
        asin = find_asin(m['isbn13'], m['title'])
        if not asin:
            print(f"{m['slug']}: not live yet")
            continue
        m['asin'] = asin; m['live'] = True
        ids = m.get('on_live', {}).get('youtube_public', [])
        if ids:
            try:
                youtube_public(ids, a.token)
            except Exception as e:
                print('youtube flip failed:', e); m['live'] = False; m['watcher_error'] = str(e)[:200]
        mf.write_text(json.dumps(m, indent=2), encoding='utf-8')
        if m['live']:
            cat = repo / 'pipeline' / 'catalog.json'
            c = json.loads(cat.read_text(encoding='utf-8'))
            for b in c['books']:
                if b['slug'] == m['slug']:
                    b['asin'] = asin; b['status'] = 'live'
            cat.write_text(json.dumps(c, indent=2), encoding='utf-8')
            changed += [str(mf), str(cat)]
            print(f"{m['slug']}: LIVE, ASIN {asin}")
            try:
                disp_script = repo / 'pipeline' / 'social' / 'buffer_dispatcher.py'
                if disp_script.exists():
                    subprocess.run([sys.executable, str(disp_script)], cwd=repo, capture_output=True, timeout=60)
            except Exception as se:
                print('social dispatch trigger failed:', se)
    if changed:
        subprocess.run(['git', 'add'] + changed, cwd=repo)
        subprocess.run(['git', 'commit', '-m', 'watcher: book is live, ASIN recorded'], cwd=repo)
        subprocess.run(['git', 'push', 'origin', 'main'], cwd=repo)

if __name__ == '__main__':
    sys.exit(main())
