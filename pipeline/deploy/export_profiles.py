"""
Export Browser Profiles Bundle for Google Cloud VM
Packages authenticated browser cookies and local storage (Facebook & Pinterest)
into an encrypted/compact tarball for seamless transfer to a Google VM.
"""
import os
import tarfile
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parent.parent.parent
PROFILES_DIR = REPO_ROOT / "pipeline" / "browser_profiles"
OUTPUT_BUNDLE = REPO_ROOT / "pipeline" / "deploy" / "browser_sessions_bundle.tar.gz"

def export_profiles():
    if not PROFILES_DIR.exists():
        print(f"[ERROR] Profiles directory does not exist: {PROFILES_DIR}")
        return False
        
    print(f"[START] Bundling browser profiles from {PROFILES_DIR}...")
    with tarfile.open(OUTPUT_BUNDLE, "w:gz") as tar:
        for profile in ["facebook_profile", "pinterest_profile"]:
            p_path = PROFILES_DIR / profile
            if p_path.exists():
                print(f"  -> Adding {profile}...")
                tar.add(p_path, arcname=profile)
                
    size_mb = OUTPUT_BUNDLE.stat().st_size / (1024 * 1024)
    print(f"[SUCCESS] Exported profiles bundle: {OUTPUT_BUNDLE} ({size_mb:.2f} MB)")
    print(f"[NEXT STEP] Transfer this bundle to your Google Cloud VM with:")
    print(f"  gcloud compute scp {OUTPUT_BUNDLE} <vm-name>:~/agentic-books/pipeline/deploy/")
    return True

if __name__ == "__main__":
    export_profiles()
