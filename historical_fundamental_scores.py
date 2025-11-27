# === STOCK RANKING METHODOLOGY ===
# Stocks are ranked by combining business quality (60%) and brand recognition (40%).
# This methodology balances fundamental excellence with market visibility and investor accessibility.
#
# === 60% QUALITY SCORE CRITERIA (In Priority Order) ===
# Quality is determined by position in the fundamentally-ranked list:
# 1. ROIC (Return on Invested Capital) - Higher is better, 40%+ is elite
# 2. Operating/Net Margin Profile - Level and trend (expanding margins prioritized)
# 3. Competitive Moat Strength - Monopolies, duopolies, network effects, switching costs
# 4. Business Model Quality - Asset-light, recurring revenue, scalability
# 5. Free Cash Flow Generation - Conversion rate and consistency
# 6. Revenue Growth Sustainability - Ability to grow while maintaining/expanding margins
# 7. Market Position - Dominance in niche or category leadership
# 8. Capital Efficiency - Low capital requirements for growth
#
# Quality Scoring: Position in fundamental ranking list determines score
# - Position 1-20: 100-90 points (Elite money machines)
# - Position 21-60: 89.5-70 points (Premium quality)
# - Position 61-120: 69.5-40 points (Strong businesses)
# - Position 121-200: 39.5-0 points (Good to acceptable quality)
#
# === 40% BRAND RECOGNITION CRITERIA ===
# Brand recognition measures consumer/investor familiarity and market visibility:
# 1. Consumer Awareness - Household name status and product recognition
# 2. Media Coverage - Frequency and prominence in financial/mainstream media
# 3. Investor Accessibility - Ease of understanding business model for retail investors
# 4. Market Presence - Geographic reach and market penetration visibility
# 5. Cultural Impact - Brand association and mindshare in target markets
#
# Brand Recognition Tiers:
# - Universal (95-100): Globally recognized consumer brands (AAPL, AMZN, GOOGL, META, MSFT, TSLA, NFLX, DIS)
# - Very High (85-94): Major retail/financial brands known to most consumers (COST, SBUX, WMT, HD, V, MA, JPM)
# - High (70-84): Well-known public companies with strong consumer presence (ABNB, SHOP, AMD, LULU, CMG, CROX)
# - Moderate (55-69): Recognized by business professionals and investors (AVGO, PANW, NOW, TMO, ISRG, SPGI)
# - Niche (40-54): Known within specific industries/B2B markets (ASML, SNPS, FTNT, industrial/specialized)
# - Obscure (25-39): Highly specialized companies unknown to general public (PAYC, APPF, MEDP, micro-cap specialists)
#
# === FINAL RANKING FORMULA ===
# Final Score = (Quality Score × 0.60) + (Brand Recognition Score × 0.40)
#
# This weighting ensures:
# - Business fundamentals drive primary ranking (60% weight)
# - Brand recognition provides meaningful differentiation (40% weight)
# - Elite quality + universal brands score highest (90-100 range)
# - Hidden gems with strong fundamentals but low recognition remain visible (60-75 range)
# - Well-known but lower-quality businesses are appropriately weighted (50-65 range)
#
# === TIER CLASSIFICATIONS ===
# Tier S+ (90-100): Elite quality + Universal/Very High brand - The "no-brainer" investments
# Tier S (82-89): Premium quality + High brand - Excellent companies with strong recognition
# Tier A+ (74-81): Strong quality + Good brand - High-quality with moderate visibility
# Tier A (66-73): Quality companies + Moderate brand - Solid fundamentals, less known
# Tier B+ (58-65): Good quality + Niche brand - Hidden quality, specialist recognition
# Tier B (50-57): Profitable + Low brand - Good businesses, minimal public awareness
# Tier C (42-49): Acceptable quality or obscure gems - Trade-offs between quality/recognition
# Tier D (<42): Lower quality or highly specialized - Higher risk/specialized knowledge required
#
# Top tier businesses combine 40%+ ROIC with 25%+ margins, asset-light models, structural moats,
# AND sufficient brand recognition to ensure liquidity, analyst coverage, and investor accessibility.
# Lower tiers may reflect either: (1) fundamental weaknesses (commoditization, cyclicality, margin pressure),
# or (2) low brand recognition despite strong fundamentals (hidden gems requiring specialist knowledge).
# =========================================

STOCK_SCORES = {
    # === TIER S+: Elite Quality + Universal Recognition ===
    "MSFT": "9.1",  # Combined: 98.8
    "GOOGL": "8.6",  # Combined: 97.9
    "GOOG": "8.6",  # Combined: 97.6
    "META": "8.4",  # Combined: 97.3
    "NVDA": "8.9",  # Combined: 96.5
    "MA": "6.7",  # Combined: 93.7
    "V": "6.1",  # Combined: 93.4
    "COST": "8.9",  # Combined: 92.6
    "BKNG": "6.9",  # Combined: 88.8
    "INTU": "8.9",  # Combined: 86.1

    # === TIER S: Premium Quality + Very High Recognition ===
    "ADBE": "9.2",  # Combined: 85.2
    "CRM": "8.7",  # Combined: 83.7
    "NFLX": "8.0",  # Combined: 82.9
    "PANW": "8.2",  # Combined: 80.0
    "WDAY": "8.4",  # Combined: 79.7
    "NOW": "7.5",  # Combined: 79.1
    "DECK": "9.5",  # Combined: 78.9
    "PGR": "9.4",  # Combined: 78.8
    "ASML": "9.1",  # Combined: 78.6
    "SPGI": "8.3",  # Combined: 78.5
    "MCO": "6.8",  # Combined: 78.2
    "AVGO": "7.2",  # Combined: 78.2
    "DXCM": "8.8",  # Combined: 77.6
    "AMZN": "7.1",  # Combined: 77.5

    # === TIER A+: Strong Quality + High Recognition ===
    "LULU": "7.7",  # Combined: 76.6
    "ADSK": "8.9",  # Combined: 76.3
    "FICO": "8.2",  # Combined: 76.0
    "CMG": "7.7",  # Combined: 76.0
    "ORLY": "8.2",  # Combined: 75.8
    "VEEV": "7.7",  # Combined: 75.4
    "SNPS": "9.2",  # Combined: 75.0
    "FTNT": "9.4",  # Combined: 75.0
    "CROX": "8.5",  # Combined: 74.7
    "CDNS": "8.8",  # Combined: 74.7
    "SBUX": "7.3",  # Combined: 74.6
    "PAYC": "9.8",  # Combined: 74.3
    "ELF": "8.2",  # Combined: 73.2
    "CBOE": "9.4",  # Combined: 72.3
    "REGN": "8.4",  # Combined: 71.8
    "AMD": "8.1",  # Combined: 71.4
    "ZTS": "7.7",  # Combined: 71.3
    "PYPL": "8.0",  # Combined: 71.2
    "ULTA": "6.9",  # Combined: 71.2
    "MORN": "8.3",  # Combined: 71.1

    # === TIER A: Quality Software + Moderate Recognition ===
    "ADP": "7.3",  # Combined: 70.7
    "RMD": "9.1",  # Combined: 70.5
    "IDXX": "7.7",  # Combined: 70.0
    "DPZ": "6.9",  # Combined: 69.7
    "WMT": "6.8",  # Combined: 69.3
    "FISV": "8.0",  # Combined: 69.2
    "PAYX": "8.1",  # Combined: 69.0
    "CSGP": "8.4",  # Combined: 68.7
    "TYL": "7.5",  # Combined: 68.4
    "PTC": "7.8",  # Combined: 68.1
    "PODD": "8.0",  # Combined: 67.3
    "BRO": "8.3",  # Combined: 66.3
    "EXR": "8.3",  # Combined: 65.8
    "FAST": "8.5",  # Combined: 65.4
    "TSLA": "7.5",  # Combined: 65.2
    "CPRT": "7.7",  # Combined: 65.1
    "GWW": "7.9",  # Combined: 65.1
    "KNSL": "9.3",  # Combined: 64.8
    "PCTY": "9.1",  # Combined: 64.7
    "RLI": "8.2",  # Combined: 64.5
    "PLMR": "8.9",  # Combined: 64.2
    "AXP": "6.2",  # Combined: 64.0
    "RJF": "8.6",  # Combined: 63.6
    "FDS": "7.9",  # Combined: 63.3
    "ICE": "6.9",  # Combined: 63.1
    "NET": "6.7",  # Combined: 62.6
    "ZS": "7.5",  # Combined: 62.3
    "TMO": "6.9",  # Combined: 62.3
    "APPF": "9.3",  # Combined: 62.0
    "HUBS": "6.8",  # Combined: 61.7

    # === TIER B+: Profitable Growers + Good Recognition ===
    "TXRH": "7.8",  # Combined: 60.9
    "CHWY": "6.7",  # Combined: 60.6
    "CTAS": "7.6",  # Combined: 60.3
    "WING": "9.4",  # Combined: 60.3
    "AZO": "7.3",  # Combined: 59.9
    "ROL": "7.4",  # Combined: 59.4
    "BRK-B": "6.0",  # Combined: 58.9
    "EXLS": "7.9",  # Combined: 58.8
    "DUOL": "7.5",  # Combined: 58.8
    "QLYS": "7.8",  # Combined: 58.5
    "ISRG": "6.0",  # Combined: 57.5
    "AMAT": "6.9",  # Combined: 57.3
    "WRB": "7.0",  # Combined: 57.3
    "CINF": "7.1",  # Combined: 57.0
    "TT": "7.0",  # Combined: 56.8
    "ACGL": "7.3",  # Combined: 56.7
    "BSX": "6.1",  # Combined: 56.6
    "MKTX": "6.6",  # Combined: 56.4
    "ERIE": "7.9",  # Combined: 56.4
    "SHW": "6.5",  # Combined: 56.4
    "WM": "5.2",  # Combined: 56.3
    "DDOG": "6.5",  # Combined: 56.3
    "CB": "6.2",  # Combined: 56.1
    "CME": "5.9",  # Combined: 56.0
    "KLAC": "7.1",  # Combined: 55.8
    "COF": "6.0",  # Combined: 55.7
    "DKS": "6.9",  # Combined: 54.6
    "RSG": "6.3",  # Combined: 54.6
    "VMC": "6.9",  # Combined: 53.8
    "TTD": "7.8",  # Combined: 53.7
    "MLM": "6.8",  # Combined: 53.5
    "RTX": "6.3",  # Combined: 52.8
    "HLT": "6.5",  # Combined: 52.4
    "LMT": "6.2",  # Combined: 52.2
    "MPWR": "7.4",  # Combined: 52.2
    "NDAQ": "5.4",  # Combined: 51.7
    "MELI": "8.2",  # Combined: 51.3
    "NOC": "6.0",  # Combined: 51.1
    "GD": "5.8",  # Combined: 50.8
    "IR": "7.0",  # Combined: 50.2

    # === TIER B: Solid Businesses + Niche Recognition ===
    "PH": "6.5",  # Combined: 49.9
    "ANET": "6.6",  # Combined: 49.6
    "PLTR": "6.9",  # Combined: 48.5
    "MRVL": "6.5",  # Combined: 47.7
    "DHI": "9.0",  # Combined: 47.1
    "LHX": "6.9",  # Combined: 43.5
    "VRT": "6.5",  # Combined: 43.4
    "HEI": "7.2",  # Combined: 42.6
    "TDG": "6.3",  # Combined: 41.7
    "BOOT": "6.5",  # Combined: 41.3
    "CVCO": "8.2",  # Combined: 38.8
    "ICLR": "7.9",  # Combined: 38.3
    "O": "7.9",  # Combined: 37.9
    "UPWK": "8.5",  # Combined: 37.6
    "EPAM": "8.2",  # Combined: 35.4
    "MEDP": "9.3",  # Combined: 35.0
    "GDDY": "7.3",  # Combined: 34.9
    "XPEL": "9.2",  # Combined: 34.4
    "DAVE": "8.2",  # Combined: 33.8
    "CELH": "6.4",  # Combined: 33.6
    "NXT": "8.8",  # Combined: 33.2
    "FIX": "9.4",  # Combined: 33.1
    "IDCC": "9.0",  # Combined: 32.5
    "NMIH": "8.6",  # Combined: 32.3
    "SSD": "8.9",  # Combined: 32.2
    "DORM": "8.4",  # Combined: 32.0
    "HLNE": "8.8",  # Combined: 31.9
    "GCT": "9.0",  # Combined: 31.3
    "HD": "5.8",  # Combined: 31.2
    "AMPH": "9.0",  # Combined: 31.0
    "YUM": "5.9",  # Combined: 31.0
    "EME": "8.2",  # Combined: 30.8
    "EXEL": "8.2",  # Combined: 30.5
    "SN": "7.7",  # Combined: 30.3
    "FN": "8.4",  # Combined: 30.1
    "PSA": "6.8",  # Combined: 30.1
    "UHS": "7.4",  # Combined: 30.0
    "AAPL": "5.3",  # Combined: 29.8
    "BLK": "6.3",  # Combined: 29.6
    "OSIS": "8.2",  # Combined: 29.5
    "VICI": "7.1",  # Combined: 29.5
    "DIS": "5.2",  # Combined: 29.5
    "ODD": "7.9",  # Combined: 29.0
    "STRL": "7.8",  # Combined: 28.4
    "AX": "7.8",  # Combined: 28.4
    "LNTH": "8.2",  # Combined: 28.3
    "TECH": "7.8",  # Combined: 28.1
    "DT": "7.6",  # Combined: 28.1
    "MCD": "5.5",  # Combined: 27.9
    "NSSC": "7.9",  # Combined: 27.7

    # === TIER C+: Quality with Low Recognition ===
    "ABBV": "5.8",  # Combined: 27.7
    "SHOP": "5.9",  # Combined: 27.6
    "MHO": "7.8",  # Combined: 27.5
    "JNJ": "5.7",  # Combined: 27.1
    "PWR": "7.7",  # Combined: 26.6
    "TDY": "7.0",  # Combined: 26.4
    "IPAR": "7.3",  # Combined: 26.3
    "QFIN": "7.4",  # Combined: 26.3
    "IESC": "7.8",  # Combined: 26.2
    "LOW": "5.4",  # Combined: 26.1
    "APP": "7.6",  # Combined: 26.0
    "ORCL": "5.9",  # Combined: 25.8
    "HLI": "7.5",  # Combined: 25.4
    "OFG": "7.7",  # Combined: 25.3
    "BLDR": "6.8",  # Combined: 25.2
    "APH": "7.2",  # Combined: 25.1
    "SFM": "7.2",  # Combined: 24.5
    "ABT": "6.0",  # Combined: 24.5
    "JPM": "5.4",  # Combined: 24.4
    "COP": "6.1",  # Combined: 23.4
    "PINS": "5.9",  # Combined: 23.3
    "BILL": "6.4",  # Combined: 23.1
    "FROG": "6.5",  # Combined: 22.8
    "LMAT": "7.3",  # Combined: 22.6
    "ROST": "5.1",  # Combined: 22.6
    "QCOM": "5.7",  # Combined: 22.5
    "ESQ": "7.3",  # Combined: 22.0
    "ESTC": "6.3",  # Combined: 21.9
    "BR": "7.1",  # Combined: 21.8
    "ELMD": "7.3",  # Combined: 21.7
    "BSVN": "7.2",  # Combined: 21.4
    "DOCS": "6.4",  # Combined: 21.3
    "QSR": "6.0",  # Combined: 21.3
    "ABNB": "5.1",  # Combined: 21.1
    "XYL": "6.3",  # Combined: 21.0
    "WST": "7.0",  # Combined: 20.9
    "FSS": "7.2",  # Combined: 20.8
    "TJX": "4.9",  # Combined: 20.8
    "MSI": "6.3",  # Combined: 20.7
    "ONTO": "6.3",  # Combined: 20.1
    "GGG": "6.3",  # Combined: 19.8
    "CPRX": "6.8",  # Combined: 19.4
    "POOL": "6.3",  # Combined: 19.2
    "INOD": "6.8",  # Combined: 19.1
    "USLM": "7.0",  # Combined: 19.0
    "CPAY": "6.6",  # Combined: 18.8
    "HALO": "7.0",  # Combined: 18.7
    "APO": "5.8",  # Combined: 18.7
    "CW": "6.3",  # Combined: 18.6
    "NVMI": "6.2",  # Combined: 18.3

    # === TIER C: Decent Businesses + Obscure Brands ===
    "MSA": "6.6",  # Combined: 18.2
    "MAR": "5.5",  # Combined: 17.6
    "DLR": "5.8",  # Combined: 17.2
    "MANH": "6.1",  # Combined: 17.1
    "DHR": "5.5",  # Combined: 17.0
    "INMD": "6.6",  # Combined: 16.9
    "PMTS": "6.6",  # Combined: 16.3
    "INCY": "6.3",  # Combined: 16.1
    "CFLT": "5.9",  # Combined: 15.9
    "IRMD": "6.5",  # Combined: 15.7
    "EA": "5.0",  # Combined: 15.7
    "HRMY": "6.5",  # Combined: 15.4
    "CPNG": "5.7",  # Combined: 15.4
    "IQV": "6.2",  # Combined: 15.2
    "EXAS": "6.2",  # Combined: 14.9
    "MS": "3.9",  # Combined: 14.8
    "GS": "3.8",  # Combined: 14.2
    "SNA": "5.8",  # Combined: 13.8
    "KEYS": "5.8",  # Combined: 12.3
    "A": "5.7",  # Combined: 11.7
    "CAT": "4.1",  # Combined: 11.7
    "ATKR": "6.1",  # Combined: 11.6
    "PJT": "6.0",  # Combined: 11.0
    "AWI": "6.0",  # Combined: 10.7
    "LIN": "5.5",  # Combined: 10.5
    "TPL": "6.0",  # Combined: 10.4
    "TRMB": "5.6",  # Combined: 10.2
    "CMI": "5.5",  # Combined: 9.9
    "HON": "3.9",  # Combined: 9.9
    "XOM": "3.8",  # Combined: 9.6
    "ROK": "4.7",  # Combined: 7.9
    "CARG": "5.2",  # Combined: 7.2
    "CHKP": "5.2",  # Combined: 6.9
    "IEX": "5.0",  # Combined: 6.0
    "ETN": "4.3",  # Combined: 5.8
    "EMR": "4.2",  # Combined: 5.5
    "VRSK": "5.0",  # Combined: 5.4
    "AXON": "4.6",  # Combined: 5.2
    "LRCX": "4.9",  # Combined: 5.1
    "SYK": "3.8",  # Combined: 4.7
    "VRSN": "4.9",  # Combined: 4.5
    "FIS": "3.9",  # Combined: 4.5
    "ACAD": "5.7",  # Combined: 4.0
    "AME": "4.9",  # Combined: 3.9
    "NEM": "6.6",  # Combined: 3.7
    "AMT": "3.6",  # Combined: 2.2
    "UL": "0.5",  # Combined: 1.9
    "FSLR": "4.6",  # Combined: 1.8
    "SLB": "3.8",  # Combined: 1.3
    "ITW": "4.1",  # Combined: 1.2

    # === TIER D+: Lower Quality or Highly Specialized ===
    "TSM": "0.5",  # Combined: 1.1
    "SAP": "0.5",  # Combined: 0.5
    "LRN": "4.7",  # Combined: 0.2
    "ON": "4.0",  # Combined: -0.6
    "SBAC": "3.4",  # Combined: -0.8
    "BMRN": "4.9",  # Combined: -1.0
    "TXN": "3.3",  # Combined: -1.1
    "UTHR": "4.8",  # Combined: -1.6
    "EW": "4.3",  # Combined: -1.9
    "APD": "3.2",  # Combined: -3.0
    "HOLX": "4.6",  # Combined: -3.1
    "ROP": "3.5",  # Combined: -3.3
    "BMI": "4.7",  # Combined: -3.5
    "ECL": "3.1",  # Combined: -3.6
    "UNP": "2.5",  # Combined: -4.8
    "MCHP": "2.9",  # Combined: -5.1
    "GATX": "4.5",  # Combined: -5.3
    "MLI": "4.5",  # Combined: -5.6
    "TRI": "0.5",  # Combined: -7.8
    "ENB": "2.9",  # Combined: -8.2
    "KMI": "2.8",  # Combined: -8.5
    "ATEN": "3.1",  # Combined: -11.3
    "EWBC": "8.0",  # Combined: -11.8
    "WPM": "0.5",  # Combined: -12.4
}
