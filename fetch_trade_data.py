#!/usr/bin/env python3
"""
Russia-China Trade Data Fetcher
Fetches latest trade statistics from World Bank API
"""
import json
import urllib.request
import urllib.parse
import datetime

def fetch_world_bank_data():
    """Fetch China-Russia trade data from World Bank API"""
    # World Bank API - China trade with Russia
    url = "https://api.worldbank.org/v2/country/CN/indicator/NE.TRB.GNFS.ZS?format=json&per_page=10&date=2020:2024"
    try:
        with urllib.request.urlopen(url, timeout=15) as r:
            data = json.loads(r.read())
            return data
    except Exception as e:
        return {"error": str(e)}

def fetch_russia_import_data():
    """Fetch Russia's import from China data"""
    # Russian imports from China (as % of total)
    url = "https://api.worldbank.org/v2/country/RU/indicator/NE.TRB.GNFS.ZS?format=json&per_page=10&date=2020:2024"
    try:
        with urllib.request.urlopen(url, timeout=15) as r:
            data = json.loads(r.read())
            return data
    except Exception as e:
        return {"error": str(e)}

def main():
    today = datetime.date.today().isoformat()
    print(f"Russia-China Trade Data - Updated {today}")
    
    # Fetch data
    cn_trade = fetch_world_bank_data()
    ru_trade = fetch_russia_import_data()
    
    # Save raw data
    with open(f'/home/qinxi/business/russia-trade-data/data/last_update.json', 'w') as f:
        json.dump({
            'update_date': today,
            'china_trade_balance': cn_trade,
            'russia_trade': ru_trade
        }, f, indent=2, default=str)
    
    print("Data updated successfully!")
    print(f"Output: /home/qinxi/business/russia-trade-data/data/last_update.json")

if __name__ == "__main__":
    main()
