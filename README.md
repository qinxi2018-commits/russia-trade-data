# Russia-China Trade Data 2024-2026

> 🔥 **TOP 50 categories analyzed** | $162.8B total trade volume | Updated May 2026

Comprehensive Russia-China trade data analysis covering 50 product categories, with historical trends, growth rates, and actionable market intelligence for exporters.

[📊 View Analysis Script](analyze.py) | [📈 Live Data](data/last_update.json) | [📋 Full Report](https://velvety-gecko-b38d75.netlify.app/)

## What's Inside

- **TOP 50 Categories** — Chinese exports to Russia by HS code (2024 data, 50 categories ranked by trade volume)
- **Growth Trends** — Year-over-year comparison, identifying fast-growing opportunities
- **Market Segmentation** — Machinery, Electronics, Textiles, Chemicals, Metals, and more
- **Auto-Update** — Fetches latest World Bank data via `python3 fetch_trade_data.py`

## Quick Start

```bash
# Clone the repo
git clone https://github.com/qinxi2018-commits/russia-trade-data.git
cd russia-trade-data

# Run the analyzer
python3 analyze.py --summary

# Update data from World Bank
python3 fetch_trade_data.py
```

## TOP 10 Categories (2024)

| Rank | Category | Trade Volume |
|------|----------|-------------|
| 1 | Integrated Circuits & Microassemblies | $12.4B |
| 2 | Vehicle Parts & Accessories | $8.7B |
| 3 | Telephone Equipment | $7.2B |
| 4 | Computers & Parts | $6.1B |
| 5 | Display Panels (LCD/LED) | $5.3B |
| 6 | Machine Parts | $4.9B |
| 7 | Insulated Wire & Cable | $4.1B |
| 8 | Excavators & Construction Machinery | $3.8B |
| 9 | Tractors & Agricultural Vehicles | $3.2B |
| 10 | Auto Vehicles (complete units) | $2.9B |

## Data Sources

- **Primary**: China Customs (中国海关总署) via World Bank Global Trade Atlas
- **Supplementary**: UN Comtrade, Russian Federal Customs Service
- **Update Frequency**: Monthly (automated via World Bank API)

## Commercial Reports

For the full Russia Market Report 2026 (EN/ZH/RU), buyer directory, and data packages:

🌐 **http://47.104.69.146/russia-site/**

## License

MIT License — Free to use, attribution required.
