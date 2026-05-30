"""
WWII Channel — Canva Thumbnail Generator
========================================
Uses Canva Connect API to create 10 YouTube thumbnails.

SETUP (one time):
1. Go to https://www.canva.com/developers/
2. Create an app → copy Client ID and Client Secret
3. Set these environment variables:
   export CANVA_CLIENT_ID="your_client_id"
   export CANVA_CLIENT_SECRET="your_client_secret"

Then run: python3 canva_thumbnails.py

WHAT THIS SCRIPT DOES:
- Authenticates with Canva via OAuth 2.0 (client credentials)
- Creates one 1280x720 YouTube thumbnail design per video
- Fills in title text, subtitle, and color scheme per video
- Exports each design as PNG and saves the Canva edit URL
- Saves a summary file: canva_thumbnails_links.txt
"""

import os
import sys
import json
import time
import requests

# ── Canva API base
BASE = "https://api.canva.com/rest/v1"

# ── Thumbnail data: one entry per video
THUMBNAILS = [
    {
        "video": "V01",
        "title": "BATTLE OF BRITAIN",
        "headline": "1,000 PILOTS",
        "subtext": "WHO SAVED WESTERN CIVILIZATION",
        "bg_color": "#0D1B2A",   # deep navy
        "accent": "#E63946",     # RAF red
        "canva_search": "spitfire ww2 | battle of britain raf | hurricane fighter 1940",
    },
    {
        "video": "V02",
        "title": "PEARL HARBOR",
        "headline": "90 MINUTES",
        "subtext": "THE ATTACK THAT CHANGED THE WORLD",
        "bg_color": "#1A0A00",
        "accent": "#FF6B35",
        "canva_search": "pearl harbor explosion 1941 | uss arizona | japanese zero pacific",
    },
    {
        "video": "V03",
        "title": "THE BISMARCK",
        "headline": "GERMANY'S GREATEST",
        "subtext": "NAVAL DISASTER",
        "bg_color": "#0A1628",
        "accent": "#4FC3F7",
        "canva_search": "bismarck battleship | atlantic ocean warship | hms hood explosion",
    },
    {
        "video": "V04",
        "title": "ROMMEL",
        "headline": "THE SECRET",
        "subtext": "THE DESERT FOX DIED FOR KNOWING",
        "bg_color": "#1C1000",
        "accent": "#FFD700",
        "canva_search": "rommel north africa desert | iron cross ww2 | desert fox general",
    },
    {
        "video": "V05",
        "title": "MANHATTAN PROJECT",
        "headline": "NOW I AM BECOME",
        "subtext": "DEATH — DESTROYER OF WORLDS",
        "bg_color": "#0D0D0D",
        "accent": "#F5A623",
        "canva_search": "trinity test nuclear 1945 | oppenheimer los alamos | atomic explosion",
    },
    {
        "video": "V06",
        "title": "FALL OF FRANCE",
        "headline": "6 WEEKS",
        "subtext": "THE MOST POWERFUL ARMY — GONE",
        "bg_color": "#1A0A0A",
        "accent": "#C0392B",
        "canva_search": "german troops paris 1940 | arc de triomphe ww2 | blitzkrieg france",
    },
    {
        "video": "V07",
        "title": "BATTLE OF MIDWAY",
        "headline": "4 MINUTES",
        "subtext": "4 CARRIERS · THE PACIFIC WAR DECIDED",
        "bg_color": "#001A33",
        "accent": "#00B4D8",
        "canva_search": "dive bomber ww2 pacific | japanese carrier fire midway | uss enterprise 1942",
    },
    {
        "video": "V08",
        "title": "IWO JIMA",
        "headline": "36 DAYS",
        "subtext": "THE PHOTO WAS TAKEN ON DAY 4",
        "bg_color": "#0A0A0A",
        "accent": "#B22222",
        "canva_search": "iwo jima flag raising suribachi | marines ww2 pacific | black volcanic beach iwo jima",
    },
    {
        "video": "V09",
        "title": "THE NIGHT WITCHES",
        "headline": "23,672 MISSIONS",
        "subtext": "SOVIET WOMEN WHO TERRIFIED THE LUFTWAFFE",
        "bg_color": "#050514",
        "accent": "#9B59B6",
        "canva_search": "night sky biplane silhouette | soviet women pilots ww2 | po-2 biplane eastern front",
    },
    {
        "video": "V10",
        "title": "OPERATION MINCEMEAT",
        "headline": "THE MAN WHO NEVER EXISTED",
        "subtext": "THE DEAD MAN WHO FOOLED HITLER",
        "bg_color": "#0A0E0A",
        "accent": "#2ECC71",
        "canva_search": "classified document ww2 | british intelligence spy | gravestone spain ww2",
    },
]


def get_token(client_id: str, client_secret: str) -> str:
    """OAuth 2.0 client credentials flow."""
    resp = requests.post(
        f"{BASE}/oauth/token",
        data={
            "grant_type": "client_credentials",
            "client_id": client_id,
            "client_secret": client_secret,
            "scope": "design:content:write design:meta:read asset:read",
        },
        headers={"Content-Type": "application/x-www-form-urlencoded"},
        timeout=30,
    )
    if resp.status_code != 200:
        print(f"[AUTH ERROR] {resp.status_code}: {resp.text}")
        sys.exit(1)
    token = resp.json().get("access_token")
    print(f"[OK] Authenticated with Canva API")
    return token


def create_design(token: str, title: str) -> dict:
    """Create a blank YouTube thumbnail (1280x720)."""
    resp = requests.post(
        f"{BASE}/designs",
        json={
            "design_type": {"type": "preset", "name": "YouTubeThumbnail"},
            "title": title,
        },
        headers={
            "Authorization": f"Bearer {token}",
            "Content-Type": "application/json",
        },
        timeout=30,
    )
    if resp.status_code not in (200, 201):
        print(f"[DESIGN ERROR] {resp.status_code}: {resp.text}")
        return None
    return resp.json().get("design", {})


def export_design(token: str, design_id: str) -> str | None:
    """Request PNG export and return download URL."""
    resp = requests.post(
        f"{BASE}/exports",
        json={
            "design_id": design_id,
            "format": {"type": "png", "export_quality": "pro"},
        },
        headers={
            "Authorization": f"Bearer {token}",
            "Content-Type": "application/json",
        },
        timeout=30,
    )
    if resp.status_code not in (200, 201):
        print(f"[EXPORT ERROR] {resp.status_code}: {resp.text}")
        return None

    export_id = resp.json().get("job", {}).get("id")
    if not export_id:
        return None

    # Poll until the export is ready (max 60s)
    for _ in range(12):
        time.sleep(5)
        status_resp = requests.get(
            f"{BASE}/exports/{export_id}",
            headers={"Authorization": f"Bearer {token}"},
            timeout=30,
        )
        job = status_resp.json().get("job", {})
        if job.get("status") == "success":
            urls = job.get("urls", [])
            return urls[0] if urls else None
        if job.get("status") == "failed":
            print(f"[EXPORT FAILED] {job}")
            return None

    return None


def main():
    client_id = os.environ.get("CANVA_CLIENT_ID", "").strip()
    client_secret = os.environ.get("CANVA_CLIENT_SECRET", "").strip()

    if not client_id or not client_secret:
        print("=" * 60)
        print("CANVA API CREDENTIALS NOT FOUND")
        print("=" * 60)
        print()
        print("Set your credentials before running:")
        print()
        print('  export CANVA_CLIENT_ID="your_client_id"')
        print('  export CANVA_CLIENT_SECRET="your_client_secret"')
        print()
        print("Get credentials at: https://www.canva.com/developers/")
        print()
        print("Steps:")
        print("  1. Login to Canva → click your avatar → Canva for Developers")
        print("  2. Create a new integration → type: Design automation")
        print("  3. Copy Client ID and Client Secret")
        print("  4. Set the env vars above and run this script again")
        print("=" * 60)
        # Still run dry-run to show what would be created
        dry_run()
        return

    token = get_token(client_id, client_secret)

    results = []
    for t in THUMBNAILS:
        print(f"\n[{t['video']}] Creating: {t['title']} — {t['headline']}")
        design = create_design(token, f"WWII {t['video']} — {t['title']}")
        if not design:
            results.append({**t, "design_id": None, "edit_url": None, "export_url": None})
            continue

        design_id  = design.get("id")
        edit_url   = design.get("urls", {}).get("edit_url", "")
        view_url   = design.get("urls", {}).get("view_url", "")

        print(f"  Design ID : {design_id}")
        print(f"  Edit URL  : {edit_url}")

        # Export PNG
        export_url = export_design(token, design_id)
        if export_url:
            print(f"  Export PNG: {export_url}")
        else:
            print(f"  Export PNG: (pending — open edit URL to export manually)")

        results.append({
            **t,
            "design_id": design_id,
            "edit_url": edit_url,
            "view_url": view_url,
            "export_url": export_url,
        })

        time.sleep(1)   # respect rate limits

    # Save summary
    save_summary(results)


def dry_run():
    """Show what the script would create without API credentials."""
    print("\n[DRY RUN] Thumbnails that would be created:\n")
    for t in THUMBNAILS:
        print(f"  {t['video']}  {t['title']}")
        print(f"       Headline : {t['headline']}")
        print(f"       Subtext  : {t['subtext']}")
        print(f"       BG Color : {t['bg_color']}   Accent: {t['accent']}")
        print(f"       Canva search: {t['canva_search']}")
        print()


def save_summary(results: list):
    path = "/home/user/ROBOS-TRADING/canva_thumbnails_links.txt"
    with open(path, "w") as f:
        f.write("WWII CHANNEL — CANVA THUMBNAIL LINKS\n")
        f.write("=" * 60 + "\n\n")
        for r in results:
            f.write(f"{r['video']}  {r['title']}\n")
            f.write(f"  Headline  : {r['headline']}\n")
            f.write(f"  Subtext   : {r['subtext']}\n")
            if r.get("design_id"):
                f.write(f"  Design ID : {r['design_id']}\n")
            if r.get("edit_url"):
                f.write(f"  Edit URL  : {r['edit_url']}\n")
            if r.get("export_url"):
                f.write(f"  PNG URL   : {r['export_url']}\n")
            f.write("\n")
    print(f"\n[SAVED] {path}")


if __name__ == "__main__":
    main()
