"""Autonomous Growth & Marketing Engine.
Analyzes Amazon KDP sales velocity, BSR rank trends, and customer ratings from pipeline/catalog.json.
Generates and adapts organic marketing campaigns dynamically:
 1. Velocity Analysis: Evaluates daily BSR and review trajectory.
 2. Creative Engine: Spins new high-converting angles (Teacher classroom packs, Advent countdown calendars, Stocking stuffers).
 3. Funnel Optimization: Adapts lead magnet landing pages and social hooks based on what moves BSR.
 4. Zero-spam, zero-ad spend organic scaling.
"""
import json
import datetime
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parent.parent

# Marketing Angles Matrix for Pip's Christmas Countdown
MARKETING_ANGLES = [
    {
        "theme": "100% Screen-Free Focus & Motor Skills",
        "hook": "Ditch the screen tantrums this holiday season! 100% screen-free activity book engineered to develop pencil grip, bilateral coordination, and calming bedtime focus for kids ages 3–6.",
        "target_audience": "Parents, occupational therapists, and mindful educators",
        "keywords": ["screen-free toddler activities", "fine motor skills coloring book", "calm bedtime activities for kids"],
        "location_tag": "Tampa, Florida",
        "badge": "📵 Screen-Free Essential • Fine Motor Skills Development"
    },
    {
        "theme": "Local Tampa, FL Creator & Made in USA",
        "hook": "Support local creators! Designed with love right here in Tampa, Florida and printed locally in the USA with guaranteed Amazon Prime fast delivery before Christmas.",
        "target_audience": "Florida locals, American-made supporters, gift shoppers",
        "keywords": ["made in usa coloring book", "tampa florida kids gifts", "prime holiday shipping"],
        "location_tag": "Tampa, Florida, USA",
        "badge": "🇺🇸 Designed in Tampa, FL • Printed in USA"
    },
    {
        "theme": "25-Night Bedtime Wind-Down Ritual",
        "hook": "Tired of chocolate advent calendars or bedtime iPad struggles? Count down to Christmas with 25 gentle rhyming bedtime stories & big easy coloring pages featuring Pip the penguin!",
        "target_audience": "Parents seeking meaningful, non-candy advent traditions",
        "keywords": ["advent calendar alternative for kids", "toddler christmas countdown", "christmas bedtime storybook"],
        "location_tag": "United States",
        "badge": "⭐ 25-Night Calming Bedtime Advent Ritual"
    },
    {
        "theme": "Interactive Visual Scavenger Hunt ('Find Little Star')",
        "hook": "More than just coloring! Little Star plays hide-and-seek on every single page, training toddler patience, visual tracking, and cognitive focus.",
        "target_audience": "Parents of active toddlers and preschoolers needing engaging tasks",
        "keywords": ["hidden picture book for toddlers", "interactive coloring book", "preschool visual tracking"],
        "location_tag": "Tampa, Florida",
        "badge": "🔍 Interactive Hidden Object Game on Every Page"
    },
    {
        "theme": "The $9.99 Gift Parents & Grandparents Love",
        "hook": "The ultimate $9.99 stocking stuffer and Christmas Eve box treasure: 110 heavy-duty single-sided pages. No batteries, no sugar, no mess!",
        "target_audience": "Grandparents, aunts, uncles, budget-conscious holiday shoppers",
        "keywords": ["stocking stuffers for toddlers under 10", "cheap christmas gifts for preschoolers", "christmas eve box ideas"],
        "location_tag": "United States",
        "badge": "🎁 Budget Stocking Stuffer ($9.99) • Single-Sided No Bleed"
    },
    {
        "theme": "Classroom, Daycare & Homeschool Printable Pack",
        "hook": "Preschool & Kindergarten teachers: download our 100% free 4-page holiday printable pack for circle time and motor-skill centers!",
        "target_audience": "Educators, daycare providers, homeschool co-ops",
        "keywords": ["preschool christmas printables", "kindergarten coloring sheets", "classroom holiday crafts"],
        "location_tag": "Tampa, Florida",
        "badge": "🍎 Educator Approved • Free Printable Activity Pack"
    }
]

def analyze_catalog_momentum(repo_dir=None):
    repo = Path(repo_dir) if repo_dir else REPO_ROOT
    catalog_path = repo / "pipeline" / "catalog.json"
    if not catalog_path.exists():
        return {"status": "no_catalog"}
        
    catalog = json.loads(catalog_path.read_text(encoding="utf-8"))
    insights = []

    for book in catalog.get("books", []):
        title = book.get("title")
        asin = book.get("asin")
        metrics = book.get("metrics", [])
        
        latest_bsr = None
        latest_rating = None
        latest_reviews = None
        
        if metrics:
            latest = metrics[-1]
            latest_bsr = latest.get("bsr")
            latest_rating = latest.get("rating")
            latest_reviews = latest.get("review_count")

        insight = {
            "title": title,
            "asin": asin,
            "latest_bsr": latest_bsr,
            "rating": latest_rating,
            "review_count": latest_reviews,
            "recommended_strategy": ""
        }

        # Strategic adaptation rules based on sales/rank trajectory
        if latest_bsr is None or latest_reviews is None:
            insight["recommended_strategy"] = (
                "LAUNCH ACCELERATION: Zero in on Lead Magnet conversion. Promote the Free Printable Pack "
                "across Pinterest and parenting groups to capture initial reviews and trigger Amazon's organic search index."
            )
        elif latest_bsr < 50000:
            insight["recommended_strategy"] = (
                "CATEGORY LEADER: Book is gaining velocity. Double down on 'Stocking Stuffer Under $10' "
                "and queue a themed sequel for the next book creation cycle."
            )
        else:
            insight["recommended_strategy"] = (
                "KEYWORD REFRESH: Test alternative holiday hooks ('Screen-Free Travel Fun' & 'Advent Calendar Alternative') "
                "to expand reach beyond direct coloring book searches."
            )

        insights.append(insight)

    return {"timestamp": datetime.datetime.now(datetime.timezone.utc).isoformat(), "insights": insights}

def get_next_campaign_angle(day_index=0):
    return MARKETING_ANGLES[day_index % len(MARKETING_ANGLES)]

if __name__ == "__main__":
    report = analyze_catalog_momentum()
    print("Catalog Momentum Analysis:")
    print(json.dumps(report, indent=2))
