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
    "NVDA": "8.9",  # Combined: 99.3
    "MSFT": "9.1",  # Combined: 98.8
    "GOOGL": "8.6",  # Combined: 97.9
    "GOOG": "8.6",  # Combined: 97.6
    "META": "8.4",  # Combined: 97.3
    "MA": "6.7",  # Combined: 94.1
    "COST": "8.9",  # Combined: 93.8
    "V": "6.1",  # Combined: 93.8
    "BKNG": "6.9",  # Combined: 89.2
    "INTU": "8.9",  # Combined: 86.5

    # === TIER S: Premium Quality + Very High Recognition ===
    "ADBE": "9.2",  # Combined: 85.6
    "CRM": "8.7",  # Combined: 84.1
    "NFLX": "8.0",  # Combined: 82.9
    "ASML": "9.1",  # Combined: 81.0
    "PANW": "8.2",  # Combined: 80.8
    "AVGO": "7.2",  # Combined: 80.6
    "WDAY": "8.4",  # Combined: 80.1
    "NOW": "7.5",  # Combined: 79.9
    "DECK": "9.5",  # Combined: 79.7
    "PGR": "9.4",  # Combined: 79.6
    "SPGI": "8.3",  # Combined: 79.3
    "MCO": "6.8",  # Combined: 78.6
    "DXCM": "8.8",  # Combined: 78.4
    "AMZN": "7.1",  # Combined: 77.5

    # === TIER A+: Strong Quality + High Recognition ===
    "ADSK": "8.9",  # Combined: 77.1
    "LULU": "7.7",  # Combined: 77.0
    "FICO": "8.2",  # Combined: 76.8
    "CROX": "8.5",  # Combined: 76.7
    "CMG": "7.7",  # Combined: 76.4
    "SNPS": "9.2",  # Combined: 76.2
    "ORLY": "8.2",  # Combined: 76.2
    "CDNS": "8.8",  # Combined: 75.9
    "FTNT": "9.4",  # Combined: 75.8
    "VEEV": "7.7",  # Combined: 75.8
    "PAYC": "9.8",  # Combined: 75.1
    "SBUX": "7.3",  # Combined: 74.6
    "ELF": "8.2",  # Combined: 74.0
    "AMD": "8.1",  # Combined: 73.4
    "CBOE": "9.4",  # Combined: 73.1
    "REGN": "8.4",  # Combined: 72.2
    "MORN": "8.3",  # Combined: 71.9
    "RMD": "9.1",  # Combined: 71.3
    "ZTS": "7.7",  # Combined: 71.3
    "ADP": "7.3",  # Combined: 71.1

    # === TIER A: Quality Software + Moderate Recognition ===
    "WMT": "6.8",  # Combined: 70.9
    "ULTA": "6.9",  # Combined: 70.8
    "IDXX": "7.7",  # Combined: 70.4
    "PYPL": "8.0",  # Combined: 70.4
    "DPZ": "6.9",  # Combined: 70.1
    "FISV": "8.0",  # Combined: 69.6
    "CSGP": "8.4",  # Combined: 69.5
    "PAYX": "8.1",  # Combined: 69.4
    "TYL": "7.5",  # Combined: 69.2
    "PTC": "7.8",  # Combined: 68.9
    "PODD": "8.0",  # Combined: 67.3
    "BRO": "8.3",  # Combined: 67.1
    "CPRT": "7.7",  # Combined: 66.3
    "EXR": "8.3",  # Combined: 66.2
    "FAST": "8.5",  # Combined: 66.2
    "GWW": "7.9",  # Combined: 65.9
    "KNSL": "9.3",  # Combined: 65.6
    "PCTY": "9.1",  # Combined: 65.5
    "RLI": "8.2",  # Combined: 65.3
    "TSLA": "7.5",  # Combined: 65.2
    "PLMR": "8.9",  # Combined: 65.0
    "RJF": "8.6",  # Combined: 64.4
    "FDS": "7.9",  # Combined: 64.1
    "AXP": "6.2",  # Combined: 64.0
    "ICE": "6.9",  # Combined: 63.5
    "APPF": "9.3",  # Combined: 62.8
    "TMO": "6.9",  # Combined: 62.7
    "NET": "6.7",  # Combined: 62.6
    "HUBS": "6.8",  # Combined: 62.1
    "ZS": "7.5",  # Combined: 61.9

    # === TIER B+: Profitable Growers + Good Recognition ===
    "TXRH": "7.8",  # Combined: 61.7
    "CTAS": "7.6",  # Combined: 61.1
    "WING": "9.4",  # Combined: 61.1
    "CHWY": "6.7",  # Combined: 61.0
    "AZO": "7.3",  # Combined: 60.7
    "ROL": "7.4",  # Combined: 60.2
    "DUOL": "7.5",  # Combined: 60.0
    "EXLS": "7.9",  # Combined: 59.6
    "QLYS": "7.8",  # Combined: 59.3
    "BRK-B": "6.0",  # Combined: 59.3
    "AMAT": "6.9",  # Combined: 58.9
    "ISRG": "6.0",  # Combined: 58.7
    "WRB": "7.0",  # Combined: 58.1
    "CINF": "7.1",  # Combined: 57.8
    "ACGL": "7.3",  # Combined: 57.5
    "KLAC": "7.1",  # Combined: 57.4
    "MKTX": "6.6",  # Combined: 57.2
    "ERIE": "7.9",  # Combined: 57.2
    "TT": "7.0",  # Combined: 57.2
    "SHW": "6.5",  # Combined: 57.2
    "WM": "5.2",  # Combined: 57.1
    "BSX": "6.1",  # Combined: 57.0
    "COF": "6.0",  # Combined: 56.9
    "DDOG": "6.5",  # Combined: 56.7
    "CB": "6.2",  # Combined: 56.5
    "CME": "5.9",  # Combined: 56.4
    "RSG": "6.3",  # Combined: 55.0
    "DKS": "6.9",  # Combined: 55.0
    "TTD": "7.8",  # Combined: 54.9
    "VMC": "6.9",  # Combined: 54.2
    "MLM": "6.8",  # Combined: 53.9
    "MPWR": "7.4",  # Combined: 53.4
    "HLT": "6.5",  # Combined: 53.2
    "NDAQ": "5.4",  # Combined: 52.9
    "MELI": "8.2",  # Combined: 52.5
    "RTX": "6.3",  # Combined: 52.4
    "LMT": "6.2",  # Combined: 52.2
    "ANET": "6.6",  # Combined: 51.2
    "NOC": "6.0",  # Combined: 50.7
    "GD": "5.8",  # Combined: 50.4

    # === TIER B: Solid Businesses + Niche Recognition ===
    "IR": "7.0",  # Combined: 50.2
    "PLTR": "6.9",  # Combined: 50.1
    "PH": "6.5",  # Combined: 49.9
    "MRVL": "6.5",  # Combined: 48.9
    "DHI": "9.0",  # Combined: 47.9
    "LHX": "6.9",  # Combined: 44.3
    "VRT": "6.5",  # Combined: 44.2
    "HEI": "7.2",  # Combined: 43.4
    "TDG": "6.3",  # Combined: 42.5
    "BOOT": "6.5",  # Combined: 42.1
    "CVCO": "8.2",  # Combined: 39.6
    "ICLR": "7.9",  # Combined: 39.1
    "UPWK": "8.5",  # Combined: 38.4
    "O": "7.9",  # Combined: 38.3
    "EPAM": "8.2",  # Combined: 36.2
    "MEDP": "9.3",  # Combined: 35.8
    "GDDY": "7.3",  # Combined: 35.7
    "XPEL": "9.2",  # Combined: 35.2
    "CELH": "6.4",  # Combined: 34.8
    "DAVE": "8.2",  # Combined: 34.6
    "NXT": "8.8",  # Combined: 34.0
    "FIX": "9.4",  # Combined: 33.9
    "IDCC": "9.0",  # Combined: 33.3
    "NMIH": "8.6",  # Combined: 33.1
    "SSD": "8.9",  # Combined: 33.0
    "DORM": "8.4",  # Combined: 32.8
    "HLNE": "8.8",  # Combined: 32.7
    "GCT": "9.0",  # Combined: 32.1
    "AMPH": "9.0",  # Combined: 31.8
    "EME": "8.2",  # Combined: 31.6
    "HD": "5.8",  # Combined: 31.6
    "EXEL": "8.2",  # Combined: 31.3
    "SN": "7.7",  # Combined: 31.1
    "FN": "8.4",  # Combined: 30.9
    "PSA": "6.8",  # Combined: 30.9
    "UHS": "7.4",  # Combined: 30.8
    "BLK": "6.3",  # Combined: 30.8
    "YUM": "5.9",  # Combined: 30.6
    "OSIS": "8.2",  # Combined: 30.3
    "VICI": "7.1",  # Combined: 29.9
    "ODD": "7.9",  # Combined: 29.8
    "AAPL": "5.3",  # Combined: 29.8
    "STRL": "7.8",  # Combined: 29.2
    "AX": "7.8",  # Combined: 29.2
    "LNTH": "8.2",  # Combined: 29.1
    "TECH": "7.8",  # Combined: 28.9
    "DT": "7.6",  # Combined: 28.9
    "DIS": "5.2",  # Combined: 28.7
    "NSSC": "7.9",  # Combined: 28.5
    "MHO": "7.8",  # Combined: 28.3

    # === TIER C+: Quality with Low Recognition ===
    "MCD": "5.5",  # Combined: 28.3
    "SHOP": "5.9",  # Combined: 28.0
    "ABBV": "5.8",  # Combined: 27.7
    "JNJ": "5.7",  # Combined: 27.5
    "PWR": "7.7",  # Combined: 27.4
    "TDY": "7.0",  # Combined: 27.2
    "QFIN": "7.4",  # Combined: 27.1
    "IPAR": "7.3",  # Combined: 27.1
    "IESC": "7.8",  # Combined: 27.0
    "APP": "7.6",  # Combined: 26.8
    "HLI": "7.5",  # Combined: 26.2
    "ORCL": "5.9",  # Combined: 26.2
    "OFG": "7.7",  # Combined: 26.1
    "BLDR": "6.8",  # Combined: 26.0
    "APH": "7.2",  # Combined: 25.9
    "LOW": "5.4",  # Combined: 25.7
    "SFM": "7.2",  # Combined: 25.3
    "ABT": "6.0",  # Combined: 24.9
    "JPM": "5.4",  # Combined: 24.8
    "COP": "6.1",  # Combined: 24.6
    "PINS": "5.9",  # Combined: 24.1
    "BILL": "6.4",  # Combined: 23.9
    "FROG": "6.5",  # Combined: 23.6
    "LMAT": "7.3",  # Combined: 23.4
    "QCOM": "5.7",  # Combined: 22.9
    "ESQ": "7.3",  # Combined: 22.8
    "ESTC": "6.3",  # Combined: 22.7
    "BR": "7.1",  # Combined: 22.6
    "QSR": "6.0",  # Combined: 22.5
    "ELMD": "7.3",  # Combined: 22.5
    "BSVN": "7.2",  # Combined: 22.2
    "DOCS": "6.4",  # Combined: 22.1
    "ROST": "5.1",  # Combined: 21.8
    "XYL": "6.3",  # Combined: 21.8
    "WST": "7.0",  # Combined: 21.7
    "FSS": "7.2",  # Combined: 21.6
    "MSI": "6.3",  # Combined: 21.5
    "ONTO": "6.3",  # Combined: 20.9
    "ABNB": "5.1",  # Combined: 20.7
    "GGG": "6.3",  # Combined: 20.6
    "TJX": "4.9",  # Combined: 20.4
    "CPRX": "6.8",  # Combined: 20.2
    "POOL": "6.3",  # Combined: 20.0
    "INOD": "6.8",  # Combined: 19.9
    "USLM": "7.0",  # Combined: 19.8
    "CPAY": "6.6",  # Combined: 19.6
    "HALO": "7.0",  # Combined: 19.5
    "CW": "6.3",  # Combined: 19.4
    "NVMI": "6.2",  # Combined: 19.1
    "APO": "5.8",  # Combined: 19.1

    # === TIER C: Decent Businesses + Obscure Brands ===
    "MSA": "6.6",  # Combined: 19.0
    "MAR": "5.5",  # Combined: 18.4
    "MANH": "6.1",  # Combined: 17.9
    "INMD": "6.6",  # Combined: 17.7
    "DLR": "5.8",  # Combined: 17.6
    "DHR": "5.5",  # Combined: 17.4
    "PMTS": "6.6",  # Combined: 17.1
    "EA": "5.0",  # Combined: 16.9
    "INCY": "6.3",  # Combined: 16.9
    "CFLT": "5.9",  # Combined: 16.7
    "CPNG": "5.7",  # Combined: 16.6
    "IRMD": "6.5",  # Combined: 16.5
    "HRMY": "6.5",  # Combined: 16.2
    "IQV": "6.2",  # Combined: 16.0
    "EXAS": "6.2",  # Combined: 15.7
    "SNA": "5.8",  # Combined: 14.6
    "MS": "3.9",  # Combined: 14.4
    "GS": "3.8",  # Combined: 13.8
    "KEYS": "5.8",  # Combined: 13.1
    "A": "5.7",  # Combined: 12.5
    "ATKR": "6.1",  # Combined: 12.4
    "PJT": "6.0",  # Combined: 11.8
    "CAT": "4.1",  # Combined: 11.7
    "AWI": "6.0",  # Combined: 11.5
    "LIN": "5.5",  # Combined: 11.3
    "TPL": "6.0",  # Combined: 11.2
    "TRMB": "5.6",  # Combined: 11.0
    "CMI": "5.5",  # Combined: 10.7
    "HON": "3.9",  # Combined: 10.3
    "XOM": "3.8",  # Combined: 10.0
    "CARG": "5.2",  # Combined: 8.4
    "CHKP": "5.2",  # Combined: 8.1
    "ROK": "4.7",  # Combined: 7.9
    "IEX": "5.0",  # Combined: 6.8
    "LRCX": "4.9",  # Combined: 6.7
    "AXON": "4.6",  # Combined: 6.4
    "ETN": "4.3",  # Combined: 6.2
    "VRSK": "5.0",  # Combined: 6.2
    "EMR": "4.2",  # Combined: 5.5
    "VRSN": "4.9",  # Combined: 5.3
    "SYK": "3.8",  # Combined: 5.1
    "FIS": "3.9",  # Combined: 4.9
    "ACAD": "5.7",  # Combined: 4.8
    "AME": "4.9",  # Combined: 4.7
    "TSM": "0.5",  # Combined: 3.9
    "FSLR": "4.6",  # Combined: 3.0
    "AMT": "3.6",  # Combined: 3.0
    "NEM": "6.6",  # Combined: 2.9
    "SLB": "3.8",  # Combined: 2.5
    "UL": "0.5",  # Combined: 2.3

    # === TIER D+: Lower Quality or Highly Specialized ===
    "ITW": "4.1",  # Combined: 2.0
    "SAP": "0.5",  # Combined: 1.7
    "LRN": "4.7",  # Combined: 1.0
    "ON": "4.0",  # Combined: 0.6
    "SBAC": "3.4",  # Combined: 0.4
    "TXN": "3.3",  # Combined: 0.1
    "BMRN": "4.9",  # Combined: -0.2
    "UTHR": "4.8",  # Combined: -0.8
    "EW": "4.3",  # Combined: -1.1
    "APD": "3.2",  # Combined: -2.2
    "HOLX": "4.6",  # Combined: -2.3
    "ROP": "3.5",  # Combined: -2.5
    "BMI": "4.7",  # Combined: -2.7
    "ECL": "3.1",  # Combined: -2.8
    "UNP": "2.5",  # Combined: -3.6
    "MCHP": "2.9",  # Combined: -3.9
    "GATX": "4.5",  # Combined: -4.5
    "MLI": "4.5",  # Combined: -4.8
    "TRI": "0.5",  # Combined: -7.0
    "ENB": "2.9",  # Combined: -7.4
    "KMI": "2.8",  # Combined: -7.7
    "ATEN": "3.1",  # Combined: -10.5
    "EWBC": "8.0",  # Combined: -11.0
    "WPM": "0.5",  # Combined: -11.6
}
