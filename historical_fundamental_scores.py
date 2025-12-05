v# === STOCK RANKING METHODOLOGY ===
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
    "UNH": "7.6",

    # === TIER B+: Profitable Growers + Good Recognition ===
    "TXRH": "7.8",  # Combined: 61.7
    "CTAS": "7.6",  # Combined: 61.1
    "WING": "9.4",  # Combined: 61.1
    "CHWY": "6.7",  # Combined: 61.0
    "AZO": "7.3",  # Combined: 60.7
    "ROL": "7.4",  # Combined: 60.2
    "DUOL": "7.5",  # Combined: 60.0
    "HSY": "6.3",
    "MKL": "7.5",
    "JBHT": "8.0",
    "GLPI": "6.4",
    "KNSL": "9.3",
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
    "GEHC": "6.2",

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
    "WCN": "6.8",
    "STE": "7.8",
    "SSNC": "6.5",
    "EFX": "6.2",
    "WAB": "7.0",
    "RYAN": "7.9",
    "AON": "7.0",
    "TSCO": "7.5",
    "CHD": "7.2",

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
    "KO": "6.3",
    "PG": "6.2",
    "KMB": "5.1",
    "TDOC": "5.9",
    "CLX": "6.0",
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
    "RPM": "6.3",
    "LLY": "7.7",
    "WSO": "7.2",
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
    "WM": "5.2",
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
    "GEV": "6.5",
    "MSCI": "8.5",
    "SKY": "7.5",
    "MCK": "7.2",
    "JKHY": "7.0",
    "THG": "6.9",
    "HCA": "7.5",
    "HIG": "6.5",
    "FINV": "9.1",
    "LOPE": "7.9",
    "TRV": "6.2",
    "NBIX": "7.0",
    "PSMT": "8.1",
    "SKWD": "8.8",
    "MWA": "6.3",
    "VCTR": "6.3",
    "HCI": "6.2",
    "CHE": "7.2",
    "MNST": "7.5",
    "GSHD": "8.2",
    "VRTX": "6.5",
    "MAX": "6.7",
    "BRC": "6.0",
    "BRBR": "8.9",
    "BOW": "8.2",
    "ATAT": "7.8",
    "TGLS": "7.4",
    "FELE": "6.7",
    "YELP": "5.6",
    "MGIC": "9.3",
}

# Stock Quality Scores - REALISTIC DISTRIBUTION
# Formula: (Financial Quality * 0.60) + (Brand Recognition * 0.30) + (Product Popularity * 0.10)
# 
# REALISTIC TIERS:
# 🟢 7.0+ = EXCEPTIONAL (~90 stocks) - Elite financials, strong moats
# 🟡 4.0-6.9 = MIDDLE (~170 stocks) - Decent but not exceptional
TRUST_SCORES = {
    
    # ========================================
    # === 🟢 TIER 1: ELITE (9.0-10.0) ===
    # ========================================
    
    "MSFT": 9.6,   # ⬆️ from 9.5 - Azure 34% growth, Cloud $169B, diversified AI
    "NVDA": 9.2,   # ⬇️ from 9.7 - Still great but decelerating, China restrictions
    "GOOGL": 9.3,  # ⬆️ from 9.2 - Search monopoly + AI integration
    "GOOG": 9.3,   # ⬆️ from 9.2 - Same as GOOGL
    "META": 9.1,   # ⬆️ from 9.0 - Ad dominance, Reality Labs improving
    "ASML": 9.0,   # ⬆️ from 8.5 - 100% EUV monopoly, AI chip critical
    
    # ========================================
    # === 🟢 TIER 2: PREMIUM (8.5-8.9) ===
    # ========================================
    
    "MA": 8.9,     # ⬆️ from 8.8 - Payment duopoly, network effects
    "AAPL": 8.9,   # ⬇️ from 9.4 - Growth slowing but Services 13.5% growth
    "V": 8.8,      # ⬆️ from 8.7 - Visa network, digital payments
    "COST": 8.7,   # ⬇️ from 8.9 - Renewal 92.3% (slight pressure), still excellent
    "AMZN": 8.7,   # ⬆️ from 8.6 - AWS + e-commerce + ads
    "LLY": 8.6,    # ⬆️ from 8.5 - GLP-1 mega-trend, Mounjaro/Zepbound
    "INTU": 8.5,   # ⬆️ from 8.4 - Tax software lock-in
    
    # ========================================
    # === 🟢 TIER 3: STRONG (8.0-8.4) ===
    # ========================================
    
    "ADBE": 8.4,   # ⬆️ from 8.3 - Creative Cloud + AI (Firefly)
    "NFLX": 8.2,   # = 8.2 - Streaming leader, ad tier
    "UNH": 8.1,    # ⬇️ from 8.2 - Healthcare scale
    "MSCI": 8.0,   # ⬇️ from 8.2 - Data oligopoly
    
    # ========================================
    # === 🟢 TIER 4: EXCELLENT (7.5-7.9) ===
    # ========================================
    
    "BKNG": 7.9,   # ⬇️ from 8.0 - Travel leader but cyclical
    "VRTX": 7.8,   # ⬇️ from 7.9 - CF monopoly + gene therapy
    "LULU": 7.8,   # ⬇️ from 8.1 - Athleisure but competition rising
    "CMG": 7.8,    # ⬇️ from 7.9 - QSR leader
    "WMT": 7.8,    # ⬆️ from 7.7 - E-commerce + membership growing
    "MKL": 7.7,    # ⬇️ from 7.8 - Baby Berkshire quality
    "CRM": 7.7,    # ⬆️ from 7.6 - CRM platform leader
    "PANW": 7.6,   # ⬆️ from 7.5 - Cybersecurity leader
    "CROX": 7.6,   # ⬇️ from 7.8 - Viral product but fashion risk
    "CHD": 7.6,    # ⬇️ from 7.8 - Church & Dwight brands
    "MCD": 7.6,    # ⬆️ from 7.5 - Franchise model
    "TSCO": 7.5,   # ⬇️ from 7.6 - Rural retail leader
    "AVGO": 7.5,   # ⬆️ from 7.4 - Semi + software
    "BRK-B": 7.5,  # ⬆️ from 7.1 - Diversification + Buffett quality
    "AON": 7.4,    # ⬇️ from 7.5 - Insurance brokerage
    "DECK": 7.4,   # ⬇️ from 7.4 - UGG + Hoka brands
    "MCO": 7.4,    # = 7.4 - Ratings oligopoly
    "STE": 7.4,    # = 7.4 - Medical sterilization
    "KNSL": 7.3,   # ⬇️ from 7.4 - Specialty insurance
    "SPGI": 7.3,   # = 7.3 - S&P ratings
    "ANET": 7.3,   # = 7.3 - Networking leader
    "NOW": 7.3,    # = 7.3 - IT platform
    "DIS": 7.3,    # = 7.3 - IP moat (Marvel, Star Wars)
    "TSM": 7.3,    # = 7.3 - Foundry leader, AI demand
    "RYAN": 7.3,   # = 7.3 - Insurance specialty
    "AMD": 7.3,    # ⬆️ from 7.1 - AI chips, taking Intel share
    "PG": 7.3,     # ⬇️⬇️ from 8.9 - MAJOR: Slow 0.3-2.5% growth
    "HCA": 7.2,    # ⬇️ from 7.3 - Hospital operator
    "AZO": 7.2,    # = 7.2 - Auto parts
    "TXRH": 7.2,   # = 7.2 - Restaurant economics
    "WDAY": 7.2,   # = 7.2 - HR software
    "SNPS": 7.2,   # = 7.2 - Chip design software
    "ISRG": 7.2,   # = 7.2 - Surgical robots
    "HSY": 7.2,    # ⬆️ from 7.1 - Hershey brands
    "WCN": 7.2,    # = 7.2 - Waste oligopoly
    "FICO": 7.2,   # = 7.2 - Credit scores
    "HD": 7.2,     # = 7.2 - Home improvement
    "ULTA": 7.2,   # = 7.2 - Beauty retail
    "WSO": 7.1,    # ⬇️ from 7.2 - Watsco HVAC
    "ORLY": 7.1,   # = 7.1 - Auto parts
    "FTNT": 7.1,   # = 7.1 - Security appliances
    "CDNS": 7.1,   # = 7.1 - EDA software
    "YUM": 7.1,    # = 7.1 - Fast food franchises
    "VEEV": 7.1,   # = 7.1 - Life sciences software
    "DUOL": 7.1,   # = 7.1 - Language learning
    "CTAS": 7.1,   # = 7.1 - Uniform services
    "CBOE": 7.1,   # = 7.1 - Options exchange
    "CME": 7.1,    # = 7.1 - Futures exchange
    "EFX": 7.1,    # = 7.1 - Equifax credit
    "FISV": 7.1,   # = 7.1 - Payment processing
    "SBUX": 7.1,   # = 7.1 - Coffee + real estate
    
    # ========================================
    # === 🟢 TIER 5: GREAT (7.0-7.4) ===
    # ========================================
    
    "MCK": 7.0,    # ⬇️ from 7.4 - Healthcare distributor
    "NBIX": 7.0,   # ⬇️ from 7.2 - Neuroscience biotech
    "CHE": 7.0,    # = 7.0 - Healthcare services
    "KNSL": 7.0,   # ⬇️ from 7.1 - Specialty insurance
    "CPRT": 7.0,   # ⬇️ from 7.1 - Salvage auction
    "CSGP": 7.0,   # = 7.0 - CoStar real estate data
    "PGR": 7.0,    # = 7.0 - Insurance underwriting
    "LOW": 7.0,    # = 7.0 - Home improvement #2
    "DPZ": 7.0,    # = 7.0 - Pizza franchise
    "TJX": 7.0,    # = 7.0 - Off-price retail
    "DXCM": 7.0,   # = 7.0 - CGM devices
    "ADP": 7.0,    # = 7.0 - Payroll processing
    "ROST": 7.0,   # = 7.0 - Off-price retail
    "IDXX": 7.0,   # = 7.0 - Vet diagnostics
    "RMD": 7.0,    # = 7.0 - Sleep devices
    "PODD": 7.0,   # = 7.0 - Insulin pumps
    "WING": 7.0,   # = 7.0 - Wing franchises
    "CELH": 7.0,   # = 7.0 - Energy drinks
    "AXP": 7.0,    # = 7.0 - Premium credit
    "JPM": 7.0,    # = 7.0 - Banking scale
    "BLK": 7.0,    # = 7.0 - Asset management
    "TMO": 7.0,    # = 7.0 - Life sciences tools
    "REGN": 7.0,   # = 7.0 - Biotech blockbusters
    "WM": 7.0,     # = 7.0 - Waste services
    "SHW": 7.0,    # = 7.0 - Paint distribution
    "ADSK": 7.0,   # = 7.0 - CAD software
    "FAST": 7.0,   # = 7.0 - Distribution
    "BRO": 7.0,    # = 7.0 - Insurance brokerage
    "MORN": 7.0,   # = 7.0 - Investment research
    "ICE": 7.0,    # = 7.0 - Exchange network
    "NDAQ": 7.0,   # = 7.0 - Nasdaq
    "PAYC": 7.0,   # = 7.0 - Payroll SaaS
    "PAYX": 7.0,   # = 7.0 - Payroll scale
    "PCTY": 7.0,   # = 7.0 - HR software
    "EXR": 7.0,    # = 7.0 - Storage REIT
    "ERIE": 7.0,   # = 7.0 - Regional insurance
    "WRB": 7.0,    # = 7.0 - Insurance underwriting
    "ACGL": 7.0,   # = 7.0 - Reinsurance
    "ROL": 7.0,    # = 7.0 - Pest control
    "DKS": 7.0,    # = 7.0 - Sporting goods
    "POOL": 7.0,   # = 7.0 - Pool supplies
    "BLDR": 7.0,   # = 7.0 - Building materials
    "QSR": 7.0,    # = 7.0 - International QSR
    "LOPE": 6.9,   # ⬇️ from 7.1 - Education headwinds
    "WAB": 6.9,    # = 6.9 - Rail equipment
    "RLI": 6.9,    # = 6.9 - Specialty insurance
    "TSLA": 6.9,   # = 6.9 - EV leader but quality issues
    "ULTA": 6.9,   # ⬇️ from 7.2 - Beauty competition
    
    # ========================================
    # === 🟡 TIER 6: SOLID (6.5-6.9) ===
    # ========================================
    
    "TRV": 6.9,    # = 6.9 - Insurance commodity
    "MELI": 6.8,   # = 6.8 - LatAm e-commerce
    "GEHC": 6.8,   # = 6.8 - GE Healthcare spin
    "PLMR": 6.8,   # = 6.8 - Catastrophe insurance
    "PTC": 6.8,    # = 6.8 - CAD/PLM software
    "ABMD": 6.8,   # = 6.8 - Heart pumps
    "SSNC": 6.8,   # = 6.8 - Financial software
    "JBHT": 6.8,   # = 6.8 - Intermodal logistics
    "SBUX": 6.8,   # ⬇️ from 7.1 - China weakness
    "HIG": 6.8,    # = 6.8 - Hartford insurance
    "PLTR": 6.7,   # = 6.7 - Gov software
    "APPF": 6.7,   # = 6.7 - Property management
    "JKHY": 6.7,   # = 6.7 - Banking software
    "TGLS": 6.7,   # = 6.7 - Tecnoglass industrial
    "ABNB": 6.6,   # = 6.6 - Travel platform
    "GSHD": 6.6,   # = 6.6 - Goosehead insurance
    "MSA": 6.6,    # = 6.6 - Safety equipment
    "RPM": 6.5,    # = 6.5 - Coatings
    "PYPL": 6.5,   # = 6.5 - Payments competition
    "TTD": 6.5,    # = 6.5 - Adtech
    "MKTX": 6.5,   # = 6.5 - Bond trading
    "GEV": 6.5,    # = 6.5 - GE Vernova energy
    "GLPI": 6.5,   # = 6.5 - Gaming REIT
    
    # ========================================
    # === 🟡 TIER 7: GOOD (6.0-6.4) ===
    # ========================================
    
    "APO": 6.4,    # = 6.4 - Asset management
    "SHOP": 6.3,   # = 6.3 - E-commerce platform
    "AXON": 6.3,   # = 6.3 - Body cameras/tasers
    "PSMT": 6.3,   # = 6.3 - LatAm warehouse
    "DHI": 6.2,    # = 6.2 - Homebuilder
    "QLYS": 6.2,   # = 6.2 - Security compliance
    "BRBR": 6.2,   # = 6.2 - Protein brands
    "CLX": 6.2,    # ⬆️ from 6.2 - Bleach/cleaning
    "TSLA": 6.2,   # ⬇️⬇️ from 6.9 - MAJOR: Quality issues
    "HLT": 6.1,    # = 6.1 - Hotel franchise
    "XPEL": 6.1,   # = 6.1 - Paint protection
    "MAR": 6.0,    # = 6.0 - Hotel franchise
    "AMAT": 6.0,   # = 6.0 - Semi equipment (China risk)
    "KLAC": 6.0,   # = 6.0 - Semi equipment
    "QCOM": 6.0,   # = 6.0 - Mobile chips
    "ORCL": 6.0,   # = 6.0 - Database legacy
    "EA": 6.0,     # = 6.0 - Gaming hit-driven
    "DHR": 6.0,    # = 6.0 - Conglomerate
    "JNJ": 6.0,    # = 6.0 - Healthcare diversified
    "ABBV": 6.0,   # = 6.0 - Pharma patent cliffs
    "ABT": 6.0,    # = 6.0 - Medical devices
    "ZTS": 6.0,    # = 6.0 - Animal health
    "SYK": 6.0,    # = 6.0 - Medical equipment
    "CINF": 6.0,   # = 6.0 - Insurance
    "MEDP": 6.0,   # = 6.0 - Clinical research
    "ODD": 6.0,    # = 6.0 - Beauty tech
    "SKY": 6.0,    # = 6.0 - Manufactured housing
    
    # ========================================
    # === 🟡 TIER 8: MODERATE (5.5-5.9) ===
    # ========================================
    
    "SKWD": 5.9,   # = 5.9 - Small insurance
    "LRCX": 5.9,   # = 5.9 - Semi equipment cyclical
    "MRVL": 5.8,   # = 5.8 - Chip design
    "ICLR": 5.8,   # = 5.8 - Clinical research
    "BOOT": 5.8,   # = 5.8 - Boot Barn western
    "TT": 5.8,     # = 5.8 - HVAC equipment
    "THG": 5.8,    # = 5.8 - Regional insurance
    "TXN": 5.7,    # = 5.7 - Analog chips
    "FINV": 5.7,   # = 5.7 - Chinese fintech
    "BSX": 5.6,    # = 5.6 - Medical devices
    "WST": 5.6,    # = 5.6 - Pharma packaging
    "IQV": 5.6,    # = 5.6 - Pharma data
    "FIX": 5.6,    # = 5.6 - HVAC services
    "HCI": 5.6,    # = 5.6 - Florida insurance
    "COF": 5.5,    # = 5.5 - Credit cards
    "CHKP": 5.5,   # = 5.5 - Security software
    "PINS": 5.5,   # = 5.5 - Social platform
    "DT": 5.5,     # = 5.5 - App monitoring
    "SN": 5.5,     # = 5.5 - Small appliances
    "DDOG": 5.5,   # = 5.5 - Monitoring
    "NET": 5.5,    # = 5.5 - CDN services
    "ZS": 5.5,     # = 5.5 - Security cloud
    "HUBS": 5.5,   # = 5.5 - Marketing automation
    "ESTC": 5.5,   # = 5.5 - Search software
    "MANH": 5.5,   # = 5.5 - Supply chain
    "TYL": 5.5,    # = 5.5 - Gov software
    "CAT": 5.5,    # = 5.5 - Heavy machinery
    "RJF": 5.5,    # = 5.5 - Wealth management
    "FDS": 5.5,    # = 5.5 - Financial data
    "RSG": 5.5,    # = 5.5 - Waste services
    "CPNG": 5.5,   # = 5.5 - Korea e-commerce
    "EXLS": 5.5,   # = 5.5 - BPO services
    "GWW": 5.5,    # = 5.5 - MRO distribution
    "EXEL": 5.5,   # = 5.5 - Oncology biotech
    "SFM": 5.5,    # = 5.5 - Organic grocery
    "FELE": 5.5,   # = 5.5 - Water pumps
    "KO": 5.5,     # ⬇️⬇️⬇️ from 9.1 - MASSIVE: 2-3% growth
    
    # ========================================
    # === 🟡 TIER 9: FAIR (5.0-5.4) ===
    # ========================================
    
    "MPWR": 5.4,   # = 5.4 - Power semis
    "HEI": 5.4,    # = 5.4 - Aerospace parts
    "VRT": 5.4,    # = 5.4 - Data center infra
    "TECH": 5.4,   # = 5.4 - Life sciences tools
    "IPAR": 5.4,   # = 5.4 - Fragrance licensing
    "MCHP": 5.3,   # = 5.3 - Microcontrollers
    "MSI": 5.3,    # = 5.3 - Public safety
    "CVCO": 5.3,   # = 5.3 - Modular homes
    "FSS": 5.3,    # = 5.3 - Emergency vehicles
    "BOW": 5.3,    # = 5.3 - Engineering services
    "ON": 5.2,     # = 5.2 - Power semis
    "HOLX": 5.2,   # = 5.2 - Women's health
    "LHX": 5.2,    # = 5.2 - Defense electronics
    "VMC": 5.2,    # = 5.2 - Aggregates
    "DAVE": 5.2,   # = 5.2 - Digital banking
    "VCTR": 5.2,   # = 5.2 - Asset manager
    "APH": 5.1,    # = 5.1 - Connectors
    "CPRX": 5.1,   # = 5.1 - Catalyst Pharma
    "TDG": 5.1,    # = 5.1 - Aerospace (high debt)
    "HLI": 5.1,    # = 5.1 - Investment banking
    "MLM": 5.1,    # = 5.1 - Aggregates
    "MWA": 5.1,    # = 5.1 - Water infrastructure
    "CHWY": 5.0,   # = 5.0 - Pet e-commerce
    "BILL": 5.0,   # = 5.0 - B2B payments
    "GDDY": 5.0,   # = 5.0 - Web hosting
    "VRSN": 5.0,   # = 5.0 - Domain registry
    "CFLT": 5.0,   # = 5.0 - Data streaming
    "FROG": 5.0,   # = 5.0 - DevOps tools
    "EPAM": 5.0,   # = 5.0 - IT outsourcing
    "CB": 5.0,     # = 5.0 - Insurance commodity
    "GS": 5.0,     # = 5.0 - Investment banking
    "MS": 5.0,     # = 5.0 - Investment banking
    "FIS": 5.0,    # = 5.0 - Financial services
    "BR": 5.0,     # = 5.0 - Back office
    "LMT": 5.0,    # = 5.0 - Defense contractor
    "RTX": 5.0,    # = 5.0 - Aerospace/defense
    "NOC": 5.0,    # = 5.0 - Defense
    "GD": 5.0,     # = 5.0 - Defense
    "HON": 5.0,    # = 5.0 - Industrial conglomerate
    "EMR": 5.0,    # = 5.0 - Industrial automation
    "ETN": 5.0,    # = 5.0 - Electrical equipment
    "ITW": 5.0,    # = 5.0 - Industrial tools
    "IR": 5.0,     # = 5.0 - Compressors
    "PH": 5.0,     # = 5.0 - Motion control
    "AME": 5.0,    # = 5.0 - Instruments
    "ROP": 5.0,    # = 5.0 - Diversified tech
    "TDY": 5.0,    # = 5.0 - Aerospace imaging
    "AMT": 5.0,    # = 5.0 - Cell tower REIT
    "DLR": 5.0,    # = 5.0 - Data center REIT
    "PSA": 5.0,    # = 5.0 - Storage REIT
    "O": 5.0,      # = 5.0 - Retail REIT
    "VICI": 5.0,   # = 5.0 - Casino REIT
    "SBAC": 5.0,   # = 5.0 - Tower REIT
    "A": 5.0,      # = 5.0 - Life sciences tools
    "COP": 5.0,    # = 5.0 - Oil & gas
    "DORM": 5.0,   # = 5.0 - Auto parts aftermarket
    "AX": 5.0,     # = 5.0 - Online bank
    "ATAT": 5.0,   # = 5.0 - Chinese hotels
    
    # ========================================
    # === 🟡 TIER 10: BELOW AVERAGE (4.5-4.9) ===
    # ========================================
    
    "QFIN": 4.9,   # = 4.9 - China fintech
    "FN": 4.9,     # = 4.9 - Optical manufacturing
    "HLNE": 4.9,   # = 4.9 - Private equity
    "STRL": 4.9,   # = 4.9 - Background checks
    "INMD": 4.9,   # = 4.9 - Medical aesthetics
    "TRMB": 4.9,   # = 4.9 - GPS/construction tech
    "BRC": 4.9,    # = 4.9 - Industrial ID
    "VRSK": 4.8,   # = 4.8 - Insurance analytics
    "NXT": 4.8,    # = 4.8 - Renewable energy
    "EWBC": 4.8,   # = 4.8 - Regional bank
    "KEYS": 4.8,   # = 4.8 - Test equipment
    "NMIH": 4.8,   # = 4.8 - Mortgage insurance
    "NSSC": 4.8,   # = 4.8 - Security systems
    "LNTH": 4.8,   # = 4.8 - Medical imaging
    "XOM": 4.8,    # = 4.8 - Oil & gas
    "MAX": 4.7,    # = 4.7 - Ad tech
    "CARG": 4.7,   # = 4.7 - Auto marketplace
    "SSD": 4.7,    # = 4.7 - Construction products
    "ATKR": 4.7,   # = 4.7 - Electrical products
    "OSIS": 4.7,   # = 4.7 - Security screening
    "LMAT": 4.7,   # = 4.7 - Vascular devices
    "BMI": 4.7,    # = 4.7 - Flow measurement
    "PWR": 4.6,    # = 4.6 - Utility construction
    "GATX": 4.6,   # = 4.6 - Railcar leasing
    "IEX": 4.6,    # = 4.6 - Industrial pumps
    "HALO": 4.6,   # = 4.6 - Drug delivery
    "GCT": 4.6,    # = 4.6 - B2B marketplace
    "OFG": 4.6,    # = 4.6 - Puerto Rico bank
    "HRMY": 4.6,   # = 4.6 - Rare disease
    "IRMD": 4.6,   # = 4.6 - MRI devices
    "TRI": 4.6,    # = 4.6 - Data/media
    "DOCS": 4.5,   # = 4.5 - Physician network
    "APP": 4.5,    # = 4.5 - Mobile gaming ads
    "UPWK": 4.5,   # = 4.5 - Freelance marketplace
    "CPAY": 4.5,   # = 4.5 - B2B payments
    "EME": 4.5,    # = 4.5 - Construction services
    "IESC": 4.5,   # = 4.5 - Electrical construction
    "MHO": 4.5,    # = 4.5 - Homebuilder
    "UL": 4.5,     # = 4.5 - Consumer goods slow
    "CW": 4.5,     # = 4.5 - Defense electronics
    "SNA": 4.5,    # = 4.5 - Professional tools
    "CMI": 4.5,    # = 4.5 - Engine manufacturing
    "UNP": 4.5,    # = 4.5 - Railroad regulated
    "LIN": 4.5,    # = 4.5 - Industrial gases
    "APD": 4.5,    # = 4.5 - Industrial gases
    "ECL": 4.5,    # = 4.5 - Chemicals
    "ROK": 4.5,    # = 4.5 - Automation
    "NVMI": 4.5,   # = 4.5 - Semi measuring
    "ONTO": 4.5,   # = 4.5 - Semi inspection
    "TPL": 4.5,    # = 4.5 - Land royalties
    "ELF": 4.5,    # = 4.5 - Beauty competitive
    "EW": 4.5,     # = 4.5 - Heart valves
    "XYL": 4.5,    # = 4.5 - Water technology
    "GGG": 4.5,    # = 4.5 - Fluid handling
    "UHS": 4.5,    # = 4.5 - Hospital operator
    "SAP": 4.5,    # = 4.5 - Enterprise software
    "LRN": 4.5,    # = 4.5 - K-12 online education
    "IDCC": 4.5,   # = 4.5 - Wireless IP
    "AWI": 4.5,    # = 4.5 - Ceilings
    "USLM": 4.5,   # = 4.5 - Lime & Minerals
    "INOD": 4.5,   # = 4.5 - AI data services
    "PMTS": 4.5,   # = 4.5 - Payment cards
    "ESQ": 4.5,    # = 4.5 - Commercial banking
    "MGIC": 4.5,   # = 4.5 - Mortgage insurance
    "AMPH": 4.4,   # = 4.4 - Generic pharma
    "MLI": 4.4,    # = 4.4 - Copper/brass
    "KMI": 4.3,    # = 4.3 - Pipelines
    "ELMD": 4.3,   # = 4.3 - Respiratory therapy
    "BSVN": 4.2,   # = 4.2 - Micro bank
    "ENB": 4.2,    # = 4.2 - Pipelines
    "WPM": 4.2,    # = 4.2 - Precious metals
    "YELP": 4.2,   # = 4.2 - Local reviews
    "ACAD": 4.1,   # = 4.1 - Biotech
    "PJT": 4.0,    # = 4.0 - M&A advisory
    
    # ========================================
    # === 🔴 TIER 11: POOR (<4.0) ===
    # ========================================
    
    "ATEN": 3.9,   # = 3.9 - Security appliances
    "NEM": 3.3,    # = 3.3 - Gold miner
    "SLB": 3.2,    # = 3.2 - Oilfield services
    "FSLR": 3.1,   # = 3.1 - Solar oversupply
    "BMRN": 3.0,   # = 3.0 - Biotech cash burn
    "UTHR": 3.0,   # = 3.0 - Single drug pharma
    "INCY": 3.0,   # = 3.0 - Biotech struggles
    "EXAS": 3.0,   # = 3.0 - Cancer screening losses
    "TDOC": 2.1,   # ⬆️ from 2.0 - Still unprofitable telehealth
}
