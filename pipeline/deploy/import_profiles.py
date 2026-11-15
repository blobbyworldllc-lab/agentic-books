"""
Import Browser Profiles Bundle on Google Cloud VM
Extracts authenticated browser sessions directly into pipeline/browser_profiles/
allowing instant headless posting without triggering login gates or CAPTCHAs.
"""
import tarfile
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parent.parent.parent
PROFILES_DIR = REPO_ROOT / "pipeline" / "browser_profiles"
INPUT_BUNDLE = REPO_ROOT / "pipeline" / "deploy" / "browser_sessions_bundle.tar.gz"

def import_profiles():
    if not INPUT_BUNDLE.exists():
        print(f"[ERROR] Bundle not found at {INPUT_BUNDLE}")
        return False
        
    PROFILES_DIR.mkdir(parents=True, exist_ok=True)
    print(f"[START] Extracting browser sessions into {PROFILES_DIR}...")
    with tarfile.open(INPUT_BUNDLE, "r:gz") as tar:
        tar.extractall(path=PROFILES_DIR)
        
    print(f"[SUCCESS] Sessions imported successfully!")
    for p in ["facebook_profile", "pinterest_profile"]:
        status = "EXISTS" if (PROFILES_DIR / p).exists() else "MISSING"
        print(f"  -> {p}: {status}")
    return True

if __name__ == "__main__":
    import_profiles()
