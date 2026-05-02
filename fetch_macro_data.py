#!/usr/bin/env python3
"""
Russia-China Macro Data Fetcher
Fetches latest macro indicators from World Bank API
Run weekly via cronjob
"""
import json
import urllib.request
import urllib.parse
import datetime
import os

DATA_DIR = "/home/qinxi/business/russia-trade-data/data"
os.makedirs(DATA_DIR, exist_ok=True)

INDICATORS = {
    "gdp_usd": "NY.GDP.MKTP.CD",           # GDP (current US$)
    "gdp_growth": "NY.GDP.MKTP.KD.ZG",    # GDP growth (annual %)
    "inflation": "FP.CPI.TOTL.ZG",         # Inflation, consumer prices (annual %)
    "trade_pct_gdp": "TG.VAL.TOTL.GD.ZS", # Merchandise trade (% of GDP)
    "exports_bop": "BX.GSR.GNFS.CD",       # Exports of goods and services (BoP, current US$)
    "imports_bop": "BM.GSR.GNFS.CD",       # Imports of goods and services (BoP, current US$)
    "fdi_inflow": "BX.KLT.DINV.CD.WD",    # Foreign direct investment, inflow (BoP, current US$)
}

COUNTRIES = ["CN", "RU"]

def fetch_indicator(indicator_id, countries, date_range="2020:2025"):
    """Fetch indicator for multiple countries"""
    country_list = ";".join(countries)
    url = (f"https://api.worldbank.org/v2/country/{country_list}"
           f"/indicator/{indicator_id}?format=json&per_page=50&date={date_range}")
    try:
        with urllib.request.urlopen(url, timeout=15) as r:
            return json.loads(r.read())
    except Exception as e:
        return {"error": str(e)}

def format_value(val):
    """Format large numbers nicely"""
    if val is None:
        return "N/A"
    if abs(val) >= 1e12:
        return f"${val/1e12:.2f}T"
    if abs(val) >= 1e9:
        return f"${val/1e9:.1f}B"
    if abs(val) >= 1e6:
        return f"${val/1e6:.1f}M"
    return f"{val:.2f}"

def main():
    today = datetime.date.today().isoformat()
    result = {
        "update_date": today,
        "countries": {},
    }

    for name, indicator_id in INDICATORS.items():
        data = fetch_indicator(indicator_id, COUNTRIES)
        if "error" in data:
            result[name] = {"error": data["error"]}
            continue

        records = data[1] if len(data) > 1 else []
        result[name] = {}
        for rec in records:
            country = rec["countryiso3code"]
            year = rec["date"]
            value = rec["value"]
            if country not in result[name]:
                result[name][country] = {}
            result[name][country][year] = format_value(value) if value is not None else "N/A"

    # Summary text for email/newsletter
    summary_lines = [
        f"# 俄罗斯市场宏观数据更新 | {today}",
        "",
        "## 中国宏观数据",
    ]

    for indicator, countries_data in result.items():
        if indicator in ("update_date", "countries"):
            continue
        if "error" in countries_data:
            continue
        cn_latest = None
        ru_latest = None
        for year in sorted(countries_data.get("CHN", {}).keys(), reverse=True):
            if cn_latest is None:
                cn_latest = countries_data["CHN"][year]
        for year in sorted(countries_data.get("RUS", {}).keys(), reverse=True):
            if ru_latest is None:
                ru_latest = countries_data["RUS"][year]

        indicator_labels = {
            "gdp_usd": "GDP（现价美元）",
            "gdp_growth": "GDP增速（年%）",
            "inflation": "通货膨胀率（年%）",
            "trade_pct_gdp": "商品贸易占GDP比重（%）",
            "exports_bop": "出口（货物与服务，BoP）",
            "imports_bop": "进口（货物与服务，BoP）",
            "fdi_inflow": "外国直接投资流入（BoP）",
        }
        label = indicator_labels.get(indicator, indicator)
        summary_lines.append(f"- **{label}**：中国 {cn_latest} | 俄罗斯 {ru_latest}")

    summary_lines.append("")
    summary_lines.append("*数据来源：World Bank API | 自动更新*")

    summary_text = "\n".join(summary_lines)

    # Save macro data
    macro_path = os.path.join(DATA_DIR, "macro_data.json")
    with open(macro_path, "w", encoding="utf-8") as f:
        json.dump(result, f, indent=2, ensure_ascii=False, default=str)

    # Save summary as markdown for email
    summary_path = os.path.join(DATA_DIR, "macro_update.md")
    with open(summary_path, "w", encoding="utf-8") as f:
        f.write(summary_text)

    print(f"Macro data updated: {today}")
    print(f"Files: {macro_path}, {summary_path}")
    print("\n--- Summary ---")
    print(summary_text)

if __name__ == "__main__":
    main()
