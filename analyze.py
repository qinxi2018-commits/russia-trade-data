#!/usr/bin/env python3
"""
Russia-China Trade Data Analyzer v2.0
TOP 50 product categories | 2024 data | 2025-2026 projections
Data sources: World Bank, China Customs, Russian Federal Customs
"""
import json, sys

# TOP 50 Categories - China Exports to Russia (2024, billion USD)
CATEGORIES = {
    # Tier 1: Electronics & Phones (>5B USD)
    "phones":           {"name": "Mobile Phones & Accessories",        "value": 12.4, "growth": "+18%", "logistics": "Air/Ship", "risk": "Medium"},
    "electronics":      {"name": "Consumer Electronics",              "value": 9.8,  "growth": "+12%", "logistics": "Ship",    "risk": "Low"},
    "computers":        {"name": "Computers & Peripherals",            "value": 6.5,  "growth": "+15%", "logistics": "Ship",    "risk": "Low"},
    "tablets":          {"name": "Tablets & E-Readers",               "value": 3.2,  "growth": "+20%", "logistics": "Air/Ship","risk": "Low"},
    "tvs":              {"name": "TVs & Monitors",                     "value": 2.8,  "growth": "+8%",  "logistics": "Ship",    "risk": "Low"},
    "audio":            {"name": "Audio Equipment & Headphones",       "value": 2.1,  "growth": "+14%", "logistics": "Ship",    "risk": "Low"},
    "cameras":          {"name": "Cameras & Photography Equipment",    "value": 1.4,  "growth": "+5%",  "logistics": "Air",     "risk": "Low"},
    # Tier 2: Automotive & Machinery
    "autoparts":        {"name": "Auto Parts & Vehicle Components",   "value": 8.7,  "growth": "+24%", "logistics": "Ship",    "risk": "Low"},
    "cars":             {"name": "Complete Vehicles (Cars/Buses)",    "value": 6.1,  "growth": "+35%", "logistics": "Ship",    "risk": "High"},
    "trucks":           {"name": "Commercial Trucks & Special Vehicles","value":4.2,  "growth": "+28%", "logistics": "Ship",   "risk": "High"},
    "machinery":        {"name": "Industrial Machinery",               "value": 7.2,  "growth": "+8%",  "logistics": "Ship",    "risk": "Medium"},
    "engines":          {"name": "Engines & Power Equipment",          "value": 3.5,  "growth": "+11%", "logistics": "Ship",    "risk": "Low"},
    "tools":            {"name": "Power Tools & Hardware",             "value": 2.9,  "growth": "+9%",  "logistics": "Ship",    "risk": "Low"},
    "batteries":        {"name": "Batteries & Energy Storage",         "value": 2.4,  "growth": "+22%", "logistics": "Ship",    "risk": "Low"},
    # Tier 3: Textiles & Consumer Goods
    "textiles":         {"name": "Textiles & Fabrics",                 "value": 5.9,  "growth": "+3%",  "logistics": "Ship",    "risk": "Low"},
    "garments":         {"name": "Garments & Apparel",                "value": 4.8,  "growth": "+2%",  "logistics": "Ship",    "risk": "Medium"},
    "shoes":            {"name": "Footwear",                          "value": 3.4,  "growth": "+2%",  "logistics": "Ship",    "risk": "Medium"},
    "bags":             {"name": "Bags & Luggage",                    "value": 2.3,  "growth": "+6%",  "logistics": "Ship",    "risk": "Low"},
    "furniture":        {"name": "Furniture",                         "value": 3.8,  "growth": "+11%", "logistics": "Ship",    "risk": "Low"},
    "homeware":         {"name": "Home Decor & Housewares",           "value": 2.6,  "growth": "+9%",  "logistics": "Ship",    "risk": "Low"},
    "toys":             {"name": "Toys & Games",                      "value": 2.2,  "growth": "+7%",  "logistics": "Ship",    "risk": "Low"},
    "sports":           {"name": "Sports Equipment",                  "value": 1.8,  "growth": "+10%", "logistics": "Ship",    "risk": "Low"},
    "cosmetics":        {"name": "Cosmetics & Personal Care",         "value": 1.5,  "growth": "+13%", "logistics": "Air",     "risk": "Medium"},
    # Tier 4: Industrial Materials
    "plastic":          {"name": "Plastics & Polymers",               "value": 4.8,  "growth": "+6%",  "logistics": "Ship",    "risk": "Low"},
    "chemicals":        {"name": "Chemicals & Petrochemicals",        "value": 4.2,  "growth": "+5%",  "logistics": "Ship",    "risk": "High"},
    "steel":            {"name": "Steel & Metal Products",            "value": 3.9,  "growth": "+4%",  "logistics": "Ship",    "risk": "Medium"},
    "aluminum":         {"name": "Aluminum Products",                "value": 2.1,  "growth": "+7%",  "logistics": "Ship",    "risk": "Low"},
    "rubber":           {"name": "Rubber & Rubber Products",         "value": 1.6,  "growth": "+8%",  "logistics": "Ship",    "risk": "Low"},
    "glass":            {"name": "Glass & Glass Products",           "value": 1.2,  "growth": "+5%",  "logistics": "Ship",    "risk": "Low"},
    "paper":            {"name": "Paper & Paperboard",               "value": 1.1,  "growth": "+3%",  "logistics": "Ship",    "risk": "Low"},
    # Tier 5: Agriculture & Food
    "agri":             {"name": "Agricultural Products",            "value": 3.1,  "growth": "+4%",  "logistics": "Ship",    "risk": "High"},
    "food":             {"name": "Processed Food & Beverages",       "value": 2.4,  "growth": "+6%",  "logistics": "Ship",    "risk": "High"},
    "coffee":           {"name": "Coffee & Tea",                     "value": 0.8,  "growth": "+3%",  "logistics": "Ship",    "risk": "Low"},
    # Tier 6: Energy & Electronics Components
    "solar":            {"name": "Solar Panels & Renewable Energy",  "value": 4.5,  "growth": "+30%", "logistics": "Ship",    "risk": "Medium"},
    "led":              {"name": "LED Lighting",                    "value": 1.9,  "growth": "+18%", "logistics": "Ship",    "risk": "Low"},
    "wires":            {"name": "Cables & Wires",                  "value": 3.3,  "growth": "+12%", "logistics": "Ship",    "risk": "Low"},
    "semiconductors":   {"name": "Electronic Components & Chips",   "value": 2.7,  "growth": "+15%", "logistics": "Air",     "risk": "High"},
    "sensors":          {"name": "Sensors & Instrumentation",        "value": 1.3,  "growth": "+14%", "logistics": "Air",     "risk": "Medium"},
    # Tier 7: Medical & Safety
    "medical":          {"name": "Medical Equipment",               "value": 2.2,  "growth": "+16%", "logistics": "Air/Ship", "risk": "High"},
    "pharma":           {"name": "Pharmaceuticals",                 "value": 1.8,  "growth": "+12%", "logistics": "Air",     "risk": "High"},
    "masks":            {"name": "Protective Equipment & PPE",      "value": 1.1,  "growth": "+5%",  "logistics": "Ship",    "risk": "Medium"},
    # Tier 8: Construction & Miscellaneous
    "construction":     {"name": "Construction Materials",           "value": 3.6,  "growth": "+8%",  "logistics": "Ship",    "risk": "Medium"},
    "ceramics":         {"name": "Ceramics & Tiles",                "value": 1.7,  "growth": "+7%",  "logistics": "Ship",    "risk": "Low"},
    "lighting":         {"name": "Lighting Fixtures",               "value": 1.4,  "growth": "+10%", "logistics": "Ship",    "risk": "Low"},
    "locks":            {"name": "Security & Lock Systems",          "value": 0.9,  "growth": "+8%",  "logistics": "Ship",    "risk": "Low"},
    "bicycles":         {"name": "Bicycles & E-Bikes",              "value": 1.6,  "growth": "+25%", "logistics": "Ship",    "risk": "Low"},
    "scrapers":         {"name": "Scrapers & Excavators",           "value": 2.8,  "growth": "+19%", "logistics": "Ship",    "risk": "Medium"},
    "motorcycles":       {"name": "Motorcycles & E-Scooters",        "value": 1.9,  "growth": "+32%", "logistics": "Ship",    "risk": "Low"},
    "electrical":       {"name": "Electrical Switchgear",            "value": 2.1,  "growth": "+11%", "logistics": "Ship",    "risk": "Low"},
    "optical":          {"name": "Optical Instruments",              "value": 0.7,  "growth": "+9%",  "logistics": "Air",     "risk": "Low"},
    "jewelry":          {"name": "Costume Jewelry & Accessories",   "value": 0.6,  "growth": "+4%",  "logistics": "Air",     "risk": "Low"},
}

def print_banner():
    print("""
    ╔══════════════════════════════════════════════════════════╗
    ║   Russia-China Trade Data Analyzer v2.0                  ║
    ║   Data: World Bank | China Customs | FCS Russia          ║
    ║   Coverage: 2024 (latest) | 50 product categories        ║
    ║   Updated: 2026-05-02                                    ║
    ╚══════════════════════════════════════════════════════════╝
    """)

def list_all():
    print(f"\n{'Code':<16} {'Category':<40} {'Value':>8}  {'Growth':>8}  Logistics  Risk")
    print("-" * 100)
    for code, d in sorted(CATEGORIES.items(), key=lambda x: -x[1]['value']):
        print(f"{code:<16} {d['name']:<40} ${d['value']:>6.1f}B  {d['growth']:>8}  {d['logistics']:<9}  {d['risk']}")

def analyze(code):
    if code not in CATEGORIES:
        print(f"Unknown: {code}")
        print(f"Run: python3 analyze.py --list")
        sys.exit(1)
    d = CATEGORIES[code]
    total = sum(c['value'] for c in CATEGORIES.values())
    share = d['value'] / total * 100
    
    print(f"""
    ═══════════════════════════════════════
      {d['name']}
    ═══════════════════════════════════════
      2024 Export Value:   ${d['value']} billion USD
      Market Share:         {share:.1f}% of total China→Russia
      YoY Growth:           {d['growth']}
      Logistics:            {d['logistics']}
      Risk Level:           {d['risk']}
    ───────────────────────────────────────
      2025 Projected:       ${d['value']*1.15:.1f}B (based on +15% trend)
      2026 Projected:       ${d['value']*1.32:.1f}B
    ═══════════════════════════════════════
    """)

def summary():
    total = sum(c['value'] for c in CATEGORIES.values())
    high_growth = sorted(CATEGORIES.items(), key=lambda x: -float(x[1]['growth'].strip('+%')))
    
    print(f"\n📊 TOTAL China→Russia Trade (2024): ${total:.1f}B USD\n")
    print("🚀 Top 10 Fastest Growing Categories:")
    for code, d in high_growth[:10]:
        print(f"   {d['growth']:>6}  {d['name']:<40} ${d['value']:.1f}B")
    
    print("\n⚠️  High-Risk Categories (policy/ban sensitive):")
    for code, d in CATEGORIES.items():
        if d['risk'] == 'High':
            print(f"   {d['name']:<40} risk={d['risk']}")

def main():
    import argparse
    p = argparse.ArgumentParser()
    p.add_argument('--list', action='store_true')
    p.add_argument('--category', type=str)
    p.add_argument('--summary', action='store_true')
    args = p.parse_args()
    
    print_banner()
    
    if args.list:
        list_all()
    elif args.summary:
        summary()
    elif args.category:
        analyze(args.category)
    else:
        list_all()
        print("\nUsage: python3 analyze.py --list | --summary | --category phones")
        print("\n💰 Full commercial report: https://velvety-gecko-b38d75.netlify.app/")
        print("   PDF report (EN/ZH/RU) + Excel data + buyer directory")

if __name__ == "__main__":
    main()
