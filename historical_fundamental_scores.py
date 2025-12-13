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
    "LDOS": "7.2",
    "FERG": "5.9",
    "CACI": "8.4",
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
    "ZBRA": "4.5",
    "CHRW": "5.0",
    "CRWD": "6.3",
    "GXO": "6.5",
    "AJG": "7.3",
    "TECH": "7.8",
    "ELV": "7.9",
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
    "SPSC": "7.7",
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
    "CW": "6.3",
    "WDFC": "5.9",
    "RACE": "0.5",
    "WAT": "1.1",
    "CLH": "6.2",
    "WAB": "7.0",
    "RYAN": "7.9",
    "SAIA": "7.7",
    "GHC": "7.3",
    "AON": "7.0",
    "TYL": "7.5",
    "TSCO": "7.5",
    "CHD": "7.2",
    "ASAN": "5.9",
    "PNR": "5.5",
    "SNOW": "5.5",
    "MKC": "6.5",
    "ALGN": "6.0",
    "TEAM": "8.0",
    "TWLO": "6.2",
    "GPN": "7.9",
    "FNF": "5.3",
    "SEIC": "5.9",
    "LPLA": "8.2",
    "RNR": "5.9",
    "MDT": "4.4",
    "CL": "6.1",
    "ALLE": "6.1",
    "MDB": "5.5",
    "TOST": "5.5",
    "MDLZ": "5.2",

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
    "EEFT": "6.0",
    "KMB": "5.1",
    "TDOC": "5.9",
    "ODFL": "5.2",
    "CLX": "6.0",
    "CAH": "7.0",
    "CHDN": "5.0",
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
    "NKE": "6.5",
    "PEP": "6.4",
    "KR": "5.5",
    "WTRG": "5.2",
    "LSCC": "6.1",
    "CHH": "6.6",
    "CW": "6.3",
    "MTD": "5.9",
    "CVX": "5.0",
    "NDSN": "5.5",
    "PM": "5.8",
    "TNET": "6.9",
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
    "AWK": "4.3",
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

# Stock Quality Scores - CORRECTED REALISTIC DISTRIBUTION
# Formula: (Financial Quality * 0.60) + (Brand Recognition * 0.30) + (Product Popularity * 0.10)
# 
# REALISTIC TIERS:
# 🟢 7.0+ = EXCEPTIONAL (~90 stocks) - Elite financials, strong moats
# 🟡 4.0-6.9 = MIDDLE (~170 stocks) - Decent but not exceptional
# 🔴 0-3.9 = WEAK - Poor financials or highly speculative

TRUST_SCORES = {
    # === 🟢 EXCEPTIONAL TIER (7.0+) ===
    
    # ELITE (9.0-10.0) - The Untouchables - Tech monopolies with 100%+ ROIC
    "NVDA": 9.7,     # AI dominance, 113-165% ROIC, 80% GPU share
    "MSFT": 9.5,     # Cloud + Office monopoly, 40%+ ROIC
    "AAPL": 9.4,     # Ecosystem lock-in, services growth, 50%+ ROIC
    "GOOGL": 9.2,    # Search monopoly (90%+ share), 30%+ ROIC
    "GOOG": 9.2,     # Same as GOOGL
    "KO": 9.1,       # Coca-Cola - Ultimate beverage brand, pricing power, 40%+ ROIC
    "META": 9.0,     # Social empire, ad dominance, 25%+ ROIC
    "PG": 8.9,       # Procter & Gamble - Brand portfolio (Tide, Gillette), 25%+ ROIC
    
    # PREMIUM (8.5-8.9) - Payment Networks, Elite Platforms & Compounder
    "COST": 8.9,     # 90% renewal rate, pricing power, member moat
    "SPSC": 8.8,     # SPS Commerce - EDI software, 98 quarters of growth, SaaS model
    "MA": 8.8,       # Payment duopoly, 50%+ ROIC
    "TYL": 8.7,      # Tyler Technologies - Gov software monopoly, high retention
    "V": 8.7,        # Visa network effects, 50%+ ROIC
    "AMZN": 8.6,     # E-commerce + AWS cash cow, scale moat
    "LDOS": 8.6,     # Leidos - Defense IT, gov contracts, recurring revenue
    "CACI": 8.7,     # CACI - Defense intelligence, high barriers
    "ASML": 8.5,     # EUV lithography monopoly (100% share), critical tech
    "LLY": 8.5,      # Eli Lilly - GLP-1 drugs (Mounjaro), strong pipeline
    
    # STRONG (8.0-8.4) - Software Monopolies & Premium Brands
    "INTU": 8.4,     # TurboTax/QuickBooks lock-in, 20%+ ROIC
    "SAIA": 8.3,     # LTL trucking leader, superior network, pricing power
    "ADBE": 8.3,     # Creative Cloud monopoly, subscription model
    "NFLX": 8.2,     # Streaming leader, content moat, improving margins
    "MSCI": 8.2,
    "UNH": 8.2,      # UnitedHealth - Scale in health insurance, Optum growth
    "LULU": 8.1,     # Lululemon - Athleisure cult brand, pricing power
    "BKNG": 8.0,     # Booking.com - Travel booking dominance, network effects
    "RACE": 8.0,     # Ferrari - Ultimate luxury brand, 22% ROIC, scarcity model
    "CAH": 8.0,      # Cardinal Health - Healthcare distribution, scale benefits
    
    # EXCELLENT (7.5-7.9) - Category Leaders with Strong Moats
    "CMG": 7.9,      # Chipotle - QSR leader, unit economics, brand strength
    "NVO": 7.9,      # Novo Nordisk - Ozempic dominance, diabetes/obesity leader
    "VRTX": 7.9,     # Vertex - CF monopoly, strong pipeline, pricing power
    "GHC": 7.9,      # Graham Holdings - Kaplan education, diversified assets
    "RNR": 7.9,      # RenaissanceRe - Elite reinsurance, 23.5% ROE, underwriting discipline
    "CROX": 7.8,     # Crocs - Viral product, pricing power, brand momentum
    "MDB": 7.8,      # MongoDB - Database leader, developer favorite
    "CHD": 7.8,      # Church & Dwight - ARM & HAMMER, consistent compounder
    "MNDY": 7.8,     # Monday.com - Work OS platform, strong growth
    "CRWD": 7.8,     # CrowdStrike - Cybersecurity leader, 80% gross margins
    "PEP": 7.8,      # PepsiCo - Snacks + beverages, brand portfolio, 14% ROIC
    "MKL": 7.8,      # Markel - "Baby Berkshire", insurance + investments
    "PM": 7.8,       # Philip Morris - Tobacco pricing power, IQOS transition
    "WMT": 7.7,      # Walmart - Scale + logistics moat, e-commerce growing
    "LPLA": 7.7,     # LPL Financial - RIA platform, $1.7T assets, capital-light
    "AJG": 7.7,      # Arthur J. Gallagher - Insurance broker, recurring revenue
    "MNST": 7.7,     # Monster Energy - Brand strength, Coke distribution
    "CRM": 7.6,      # Salesforce - Enterprise CRM leader, ecosystem lock-in
    "SEIC": 7.6,     # SEI Investments - $1.6T AUM, 26% op margin, wealth platform
    "NDSN": 7.6,     # Nordson - Industrial adhesives, 61 yrs dividend growth
    "TSCO": 7.6,     # Tractor Supply - Rural retail moat, loyal customers
    "PANW": 7.5,     # Palo Alto Networks - Cybersecurity leader, platform shift
    "MCD": 7.5,      # McDonald's - Global franchise, real estate, brand moat
    "MTD": 7.5,      # Mettler Toledo - Lab equipment, premium pricing, sticky
    "AON": 7.5,      # Aon - Insurance brokerage oligopoly, B2B leader
    "CL": 7.5,       # Colgate - Toothpaste dominance, 27% ROIC, pricing power
    "STE": 7.4,      # STERIS - Medical sterilization, mission-critical
    "AVGO": 7.4,     # Broadcom - Semiconductors + software, diversified
    "FNF": 7.4,      # Fidelity National Financial - Title insurance leader
    "DECK": 7.4,     # Deckers - UGG + Hoka brands, premium positioning
    "MCO": 7.4,      # Moody's - Credit ratings oligopoly
    "KNSL": 7.4,     # Kinsale Capital - Specialty insurance, sub-60 combined ratios
    "MCK": 7.4,      # McKesson - Healthcare distributor, scale advantages
    "WTRG": 7.4,     # Essential Utilities - Water/gas utility, regulated returns
    "TOST": 7.4,     # Toast - Restaurant POS, payments, growing platform
    "TEAM": 7.4,     # Atlassian - Jira/Confluence, developer tools
    "ALLE": 7.4,     # Allegion - Door locks/security, commercial focus
    "DIS": 7.3,      # Disney - IP moat (Marvel, Star Wars), parks + streaming
    "TSM": 7.3,      # TSMC - Chip foundry leader, 30%+ ROIC, manufacturing edge
    "SPGI": 7.3,     # S&P Global - Ratings + data oligopoly
    "ANET": 7.3,     # Arista Networks - Data center networking leader
    "NOW": 7.3,      # ServiceNow - Enterprise IT platform, high retention
    "HCA": 7.3,      # HCA Healthcare - Largest hospital chain, scale benefits
    "PNR": 7.3,      # Pentair - Water tech, 19.7% ROS, strong FCF
    "RYAN": 7.3,     # Ryan Specialty - Insurance MGA, fast growth
    "AZO": 7.2,      # AutoZone - Auto parts, great ROIC, pricing power
    "TXRH": 7.2,     # Texas Roadhouse - Restaurant unit economics, franchising
    "WDAY": 7.2,     # Workday - HR software leader, enterprise focus
    "SNPS": 7.2,     # Synopsys - Chip design software (EDA duopoly)
    "ISRG": 7.2,     # Intuitive Surgical - Da Vinci robot monopoly
    "FICO": 7.2,     # Fair Isaac - Credit score duopoly, essential service
    "HD": 7.2,       # Home Depot - Home improvement moat, PRO focus
    "ULTA": 7.2,     # Ulta Beauty - Beauty retail leader, loyalty program
    "MDLZ": 7.2,     # Mondelez - Snacks (Oreo, Cadbury), global brands
    "HSY": 7.2,      # Hershey - Chocolate leader, 80+ yr dividend history
    "EEFT": 7.2,     # Euronet - ATM/payments, international focus
    "HIMS": 7.2,     # Hims & Hers - Telehealth + pharmacy, consumer brand
    "WCN": 7.2,      # Waste Connections - Waste oligopoly, excellent financials
    "ZBRA": 7.2,     # Zebra Technologies - Barcode scanners, 48% gross margin
    "CHH": 7.2,      # Choice Hotels - Franchise model, asset-light
    "GPN": 7.2,      # Global Payments - Payment processing, 45% op margin
    "ORLY": 7.1,     # O'Reilly Auto - Auto parts oligopoly
    "FTNT": 7.1,     # Fortinet - Security appliances, enterprise focus
    "CDNS": 7.1,     # Cadence - EDA software duopoly with Synopsys
    "YUM": 7.1,      # Yum Brands - KFC, Taco Bell, Pizza Hut franchises
    "DUOL": 7.1,     # Duolingo - Language learning app, freemium model
    "CTAS": 7.1,     # Cintas - Uniform/services moat, recurring revenue
    "CBOE": 7.1,     # CBOE - Options exchange monopoly
    "NBIX": 7.2,     # Neurocrine Biosciences - Neurology focus, growing
    "AMD": 7.1,      # AMD - AI chips, taking Intel share, competitive
    "BRK-B": 7.1,    # Berkshire Hathaway - Diversification, insurance float
    "VEEV": 7.1,     # Veeva - Life sciences cloud software, niche leader
    "SBUX": 7.1,     # Starbucks - Coffee + real estate, global brand
    "CME": 7.1,      # CME Group - Futures exchange, derivatives leader
    "FISV": 7.1,     # Fiserv - Payment processing, bank tech
    "KNSL": 7.1,     # Kinsale Capital - Specialty insurance (duplicate fixed)
    "CPRT": 7.1,     # Copart - Salvage auction duopoly with IAA
    "EFX": 7.1,      # Equifax - Credit bureau oligopoly, essential data
    "ELV": 7.1,      # Elevance Health - Health insurance, large scale
    "MKC": 7.1,      # McCormick - Spices monopoly, 39 yrs dividend growth
    "TNET": 7.1,     # TriNet - PEO model, HR outsourcing
    "NKE": 7.1,      # Nike - Athletic brand leader, but facing margin pressure
    "LOPE": 7.1,     # Grand Canyon Education - Online education niche
    
    # GREAT (7.0-7.4) - High Quality Businesses
    "CHE": 7.0,      # Chemed - Hospice + plumbing (Roto-Rooter), steady
    "CSGP": 7.0,     # CoStar - Real estate data monopoly, sticky customers
    "PGR": 7.0,      # Progressive - Auto insurance, underwriting edge
    "ODFL": 7.0,     # Old Dominion - LTL trucking, best-in-class operations
    "LOW": 7.0,      # Lowe's - Home improvement #2, improving ops
    "DPZ": 7.0,      # Domino's - Pizza franchise, digital leader
    "TJX": 7.0,      # TJX - Off-price retail (TJ Maxx), treasure hunt model
    "DXCM": 7.0,     # Dexcom - CGM device leader, growing diabetes market
    "ADP": 7.0,      # ADP - Payroll processing scale, recurring revenue
    "ROST": 7.0,     # Ross Stores - Off-price retail, value positioning
    "IDXX": 7.0,     # Idexx - Vet diagnostics near-monopoly
    "RMD": 7.0,      # ResMed - Sleep apnea devices, aging demographics
    "PODD": 7.0,     # Insulet - Omnipod insulin pump, innovation leader
    "WING": 7.0,     # Wingstop - Franchise unit economics, brand strength
    "CELH": 7.0,     # Celsius - Energy drink momentum, taking share
    "AXP": 7.0,      # American Express - Premium credit card moat, closed loop
    "JPM": 7.0,      # JPMorgan - Banking scale + quality, Jamie Dimon
    "BLK": 7.0,      # BlackRock - Asset management scale, iShares ETFs
    "TMO": 7.0,      # Thermo Fisher - Life sciences tools, scale leader
    "REGN": 7.0,     # Regeneron - Biotech with blockbusters (Eylea, Dupixent)
    "WM": 7.0,       # Waste Management - Waste oligopoly, largest player
    "SHW": 7.0,      # Sherwin-Williams - Paint + distribution moat
    "ADSK": 7.0,     # Autodesk - CAD software (AutoCAD), subscription model
    "FAST": 7.0,     # Fastenal - Industrial distribution, vending machines
    "BRO": 7.0,      # Brown & Brown - Insurance brokerage, M&A consolidator
    "MORN": 7.0,     # Morningstar - Investment research moat, ratings brand
    "ICE": 7.0,      # Intercontinental Exchange - Exchanges, data business
    "NDAQ": 7.0,     # Nasdaq - Exchange brand, tech listings
    "PAYC": 7.0,     # Paycom - Payroll SaaS, self-service model
    "PAYX": 7.0,     # Paychex - Payroll scale, SMB focus
    "PCTY": 7.0,     # Paylocity - HR software niche, cloud-based
    "EXR": 7.0,      # Extra Space Storage - Self-storage REIT, quality
    "ERIE": 7.0,     # Erie Indemnity - Regional insurance, mutual structure
    "WRB": 7.0,      # W.R. Berkley - Insurance underwriting discipline
    "ACGL": 7.0,     # Arch Capital - Reinsurance quality, consistent
    "ROL": 7.0,      # Rollins - Pest control moat (Orkin), recurring
    "DKS": 7.0,      # Dick's Sporting Goods - Sporting goods leader
    "POOL": 7.0,     # Pool Corp - Pool supplies distribution niche
    "BLDR": 7.0,     # Builders FirstSource - Building materials, scale
    "QSR": 7.0,      # Restaurant Brands - Burger King, Tim Hortons, Popeyes
    "WSO": 7.2,      # Watsco - HVAC distribution, regional monopolies
    "MDT": 7.0,      # Medtronic - Medical devices, but slow growth
    
    # === 🟡 MIDDLE TIER (4.0-6.9) ===
    
    # Upper Middle (6.5-6.9) - Solid but not exceptional
    "TRV": 6.9,      # Travelers - P&C insurance, blue chip but commodity
    "TWLO": 6.9,     # Twilio - Communications platform, newly profitable
    "CHRW": 6.9,     # C.H. Robinson - Freight brokerage, cyclical
    "WAB": 6.9,      # Wabtec - Rail equipment, industrial B2B
    "RLI": 6.9,
    "TSLA": 6.9,     # Tesla - EV leader but execution/quality concerns
    "HIG": 6.8,      # Hartford Financial - Insurance, competitive market
    "MELI": 6.8,     # MercadoLibre - LatAm e-commerce, EM risks
    "GEHC": 6.8,     # GE HealthCare - Medical imaging, post-spin
    "PLMR": 6.8,     # Palomar - Catastrophe insurance specialist
    "PTC": 6.8,      # PTC - CAD/PLM software, slower growth
    "ALGN": 6.8,     # Align Technology - Invisalign, competition rising
    "TECH": 6.8,     # Bio-Techne - Life sciences tools, cyclical exposure
    "SSNC": 6.8,     # SS&C Technologies - Financial software, B2B
    "LSCC": 6.8,     # Lattice Semi - FPGAs, niche but cyclical
    "CVX": 6.8,      # Chevron - Oil major, cyclical commodity
    "JKHY": 6.7,     # Jack Henry - Banking software, slower growth than top SaaS
    "TGLS": 6.7,     # Tecnoglass - Windows/glass, cyclical construction
    "PLTR": 6.7,     # Palantir - Gov software, controversial, high valuation
    "APPF": 6.7,     # AppFolio - Property management SaaS
    "GXO": 6.7,      # GXO Logistics - Contract logistics, margin pressure
    "KR": 6.7,       # Kroger - Grocery, low margins, competitive
    "ABNB": 6.6,     # Airbnb - Travel platform, cyclical, regulatory risks
    "GSHD": 6.6,     # Goosehead Insurance - Fast-growing but small
    "RPM": 6.5,      # RPM International - Specialty coatings
    "MSA": 6.6,      # MSA Safety - Safety equipment
    "KMB": 6.5,      # Kimberly-Clark - Huggies/Kleenex, commodity pressure
    "GEV": 6.5,      # GE Vernova - Energy infrastructure, unproven post-spin
    "GLPI": 6.5,     # Gaming & Leisure Properties - Casino REIT, niche
    "PYPL": 6.5,     # PayPal - Payments, competition from Apple/Block
    "TTD": 6.5,      # The Trade Desk - Adtech leader, programmatic
    "MKTX": 6.5,     # MarketAxess - Bond trading platform
    "CHDN": 6.5,     # Churchill Downs - Horse racing + gaming
    "APO": 6.4,      # Apollo - Asset management, alternatives focus
    "SHOP": 6.3,     # Shopify - E-commerce platform, merchant churn
    "AXON": 6.3,     # Axon - Body cameras/tasers, gov budget dependent
    "PSMT": 6.3,     # PriceSmart - LatAm warehouse clubs, EM risks
    "DHI": 6.2,      # D.R. Horton - Homebuilder, highly cyclical
    "QLYS": 6.2,     # Qualys - Security compliance, mature growth
    "CLX": 6.2,      # Clorox - Bleach/cleaning, commodity inputs
    "BRBR": 6.2,     # BellRing Brands - Protein shakes, commodity costs
    "SNOW": 6.2,     # Snowflake - Data warehouse, high growth but unprofitable
    "HLT": 6.1,      # Hilton - Hotel franchise, cyclical travel
    "XPEL": 6.1,     # XPEL - Paint protection film, niche auto aftermarket
    "MAR": 6.0,      # Marriott - Hotel franchise, cyclical
    "AMAT": 6.0,     # Applied Materials - Semi equipment, very cyclical
    "KLAC": 6.0,     # KLA - Semi inspection equipment, cyclical
    "QCOM": 6.0,     # Qualcomm - Mobile chips, smartphone cycle dependent
    "ORCL": 6.0,     # Oracle - Database legacy, cloud transition
    "EA": 6.0,       # Electronic Arts - Gaming, hit-driven business
    "DHR": 6.0,      # Danaher - Conglomerate, life sciences tools
    "JNJ": 6.0,      # Johnson & Johnson - Healthcare diversified, pharma patent cliffs
    "ABBV": 6.0,     # AbbVie - Pharma, Humira patent cliff passed
    "ABT": 6.0,      # Abbott - Medical devices + diagnostics
    "ZTS": 6.0,      # Zoetis - Animal health, steady but slow
    "SYK": 6.0,      # Stryker - Medical equipment, orthopedics
    "CINF": 6.0,     # Cincinnati Financial - Regional P&C insurance
    "MEDP": 6.0,     # Medpace - Clinical research CRO
    "ODD": 6.0,      # Oddity Tech - Beauty tech (IL MAKIAGE)
    "SKY": 6.0,      # Skyline Champion - Manufactured housing, cyclical
    
    # Mid (5.5-5.9) - Average quality
    "SKWD": 5.9,     # Skyward Specialty - Small insurance, needs scale
    "ASAN": 5.9,     # Asana - Project management, unprofitable
    "LRCX": 5.9,     # Lam Research - Semi equipment, highly cyclical
    "THG": 5.8,      # Hanover Insurance - Regional P&C, commodity
    "MRVL": 5.8,     # Marvell - Chip design, cyclical semi
    "ICLR": 5.8,     # ICON - Clinical research CRO
    "BOOT": 5.8,     # Boot Barn - Western retail, niche but competitive
    "TT": 5.8,       # Trane Technologies - HVAC, cyclical construction
    "TXN": 5.7,      # Texas Instruments - Analog chips, cyclical
    "FINV": 5.7,     # FinVolution - Chinese fintech, regulatory risks
    "BSX": 5.6,      # Boston Scientific - Medical devices, competitive
    "WST": 5.6,      # West Pharmaceutical - Pharma packaging
    "IQV": 5.6,      # IQVIA - Pharma data/CRO services
    "FIX": 5.6,      # Comfort Systems USA - HVAC installation
    "HCI": 5.6,      # HCI Group - Florida insurance, hurricane exposure
    "COF": 5.5,      # Capital One - Credit cards, credit cycle dependent
    "CHKP": 5.5,     # Check Point - Security software, mature
    "PINS": 5.5,     # Pinterest - Social platform, ad revenue cyclical
    "DT": 5.5,       # Dynatrace - Application monitoring
    "SN": 5.5,       # SharkNinja - Small appliances, competitive
    "DDOG": 5.5,     # Datadog - Monitoring software, competition
    "NET": 5.5,      # Cloudflare - CDN services, low margins
    "ZS": 5.5,       # Zscaler - Cloud security, high valuation
    "HUBS": 5.5,     # HubSpot - Marketing automation, SMB focus
    "ESTC": 5.5,     # Elastic - Search software, open source challenges
    "MANH": 5.5,     # Manhattan Associates - Supply chain software
    "CAT": 5.5,      # Caterpillar - Heavy machinery, very cyclical
    "RJF": 5.5,      # Raymond James - Wealth management
    "FDS": 5.5,      # FactSet - Financial data, competition from Bloomberg
    "RSG": 5.5,      # Republic Services - Waste services #2
    "CPNG": 5.5,     # Coupang - Korea e-commerce, competitive
    "EXLS": 5.5,     # ExlService - BPO services, labor arbitrage
    "GWW": 5.5,      # Grainger - MRO distribution
    "EXEL": 5.5,     # Exelixis - Oncology biotech, single drug focus
    "SFM": 5.5,      # Sprouts Farmers Market - Organic grocery niche
    "FELE": 5.5,     # Franklin Electric - Water pumps, cyclical
    "MPWR": 5.4,     # Monolithic Power - Power semis, cyclical
    "HEI": 5.4,      # HEICO - Aerospace parts, niche but cyclical
    "VRT": 5.4,      # Vertiv - Data center infrastructure
    "IPAR": 5.4,     # Inter Parfums - Fragrance licensing
    "MCHP": 5.3,     # Microchip - Microcontrollers, cyclical
    "MSI": 5.3,      # Motorola Solutions - Public safety communications
    "CVCO": 5.3,     # Cavco - Modular homes, cyclical housing
    "FSS": 5.3,      # Federal Signal - Emergency vehicles, gov budget
    "BOW": 5.3,      # Bowman Consulting - Engineering services, project-based
    "ON": 5.2,       # ON Semi - Power semis, cyclical
    "HOLX": 5.2,     # Hologic - Women's health, competitive
    "LHX": 5.2,      # L3Harris - Defense electronics
    "VMC": 5.2,      # Vulcan Materials - Aggregates, construction cycle
    "DAVE": 5.2,     # Dave - Digital banking, niche fintech
    "VCTR": 5.2,     # Victory Capital - Asset manager, market dependent
    "APH": 5.1,      # Amphenol - Connectors, cyclical
    "CPRX": 5.1,     # Catalyst Pharma - Rare disease, single drug
    "TDG": 5.1,      # TransDigm - Aerospace parts, high debt
    "HLI": 5.1,      # Houlihan Lokey - Investment banking, deal cycle
    "MLM": 5.1,      # Martin Marietta - Aggregates, construction cycle
    "MWA": 5.1,      # Mueller Water - Water infrastructure, slow growth
    "CHWY": 5.0,     # Chewy - Pet e-commerce, low margins
    "BILL": 5.0,     # Bill.com - B2B payments, SMB focus
    "GDDY": 5.0,     # GoDaddy - Web hosting, commodity
    "VRSN": 5.0,     # VeriSign - Domain registry, utility-like
    "CFLT": 5.0,     # Confluent - Data streaming, Kafka-based
    "FROG": 5.0,     # JFrog - DevOps tools
    "EPAM": 5.0,     # EPAM - IT outsourcing, labor arbitrage
    "CB": 5.0,       # Chubb - Insurance, large but commodity
    "GS": 5.0,       # Goldman Sachs - Investment banking, cyclical
    "MS": 5.0,       # Morgan Stanley - Wealth + banking
    "FIS": 5.0,      # FIS - Financial services tech
    "BR": 5.0,       # Broadridge - Financial back office
    "LMT": 5.0,      # Lockheed Martin - Defense, gov budget
    "RTX": 5.0,      # RTX - Aerospace/defense
    "NOC": 5.0,      # Northrop Grumman - Defense
    "GD": 5.0,       # General Dynamics - Defense
    "HON": 5.0,      # Honeywell - Industrial conglomerate
    "EMR": 5.0,      # Emerson - Industrial automation
    "ETN": 5.0,      # Eaton - Electrical equipment
    "ITW": 5.0,      # Illinois Tool Works - Industrial tools
    "IR": 5.0,       # Ingersoll Rand - Compressors
    "PH": 5.0,       # Parker-Hannifin - Motion control
    "AME": 5.0,      # AMETEK - Instruments
    "ROP": 5.0,      # Roper Technologies - Diversified tech
    "TDY": 5.0,      # Teledyne - Aerospace imaging/digital
    "AMT": 5.0,      # American Tower - Cell tower REIT
    "DLR": 5.0,      # Digital Realty - Data center REIT
    "PSA": 5.0,      # Public Storage - Self-storage REIT
    "O": 5.0,        # Realty Income - Retail REIT
    "VICI": 5.0,     # VICI Properties - Casino REIT
    "SBAC": 5.0,     # SBA Communications - Tower REIT
    "A": 5.0,        # Agilent - Life sciences tools
    "COP": 5.0,      # ConocoPhillips - Oil & gas
    "DORM": 5.0,     # Dorman Products - Auto parts aftermarket
    "AX": 5.0,       # Axos Financial - Online bank
    "ATAT": 5.0,     # Atour Lifestyle - Chinese hotels, China risks
    
    # Lower Middle (4.5-4.9) - Below average
    "QFIN": 4.9,     # 360 DigiTech - China fintech, regulatory risks
    "FN": 4.9,       # Fabrinet - Optical manufacturing, Thailand-based
    "HLNE": 4.9,     # Hamilton Lane - Private equity fund platform
    "STRL": 4.9,     # Sterling Check - Background checks, commoditized
    "INMD": 4.9,     # InMode - Medical aesthetics devices, cyclical
    "TRMB": 4.9,     # Trimble - GPS/construction tech
    "BRC": 4.9,      # Brady Corp - Industrial ID solutions, mature
    "VRSK": 4.8,     # Verisk - Insurance analytics
    "NXT": 4.8,      # NextEra Energy Partners - Renewable YIELDCO
    "EWBC": 4.8,     # East West Bancorp - Regional bank, China exposure
    "KEYS": 4.8,     # Keysight - Test equipment, cyclical
    "NMIH": 4.8,     # NMI Holdings - Mortgage insurance, housing cycle
    "NSSC": 4.8,     # Napco Security - Security systems, small scale
    "LNTH": 4.8,     # Lantheus - Medical imaging, Alzheimer's exposure
    "XOM": 4.8,      # ExxonMobil - Oil major, commodity cyclical
    "CARG": 4.7,     # CarGurus - Auto marketplace, discretionary
    "SSD": 4.7,      # Simpson Manufacturing - Construction products
    "ATKR": 4.7,     # Atkore - Electrical conduit, construction cycle
    "OSIS": 4.7,     # OSI Systems - Security screening, lumpy gov contracts
    "LMAT": 4.7,     # LeMaitre Vascular - Small vascular devices
    "BMI": 4.7,      # Badger Meter - Flow measurement, utility-dependent
    "MAX": 4.7,      # MediaAlpha - Ad tech, highly competitive
    "PWR": 4.6,      # Quanta Services - Utility construction
    "GATX": 4.6,     # GATX - Railcar leasing, cyclical
    "IEX": 4.6,      # IDEX - Industrial pumps/valves
    "HALO": 4.6,     # Halozyme - Drug delivery tech, single platform
    "GCT": 4.6,      # GigaCloud - B2B marketplace, early stage
    "OFG": 4.6,      # OFG Bancorp - Puerto Rico bank, regional risk
    "HRMY": 4.6,     # Harmony Biosciences - Rare disease, single drug
    "IRMD": 4.6,     # IRadimed - MRI-compatible devices, niche
    "TRI": 4.6,      # Thomson Reuters - Data/media, competition
    "DOCS": 4.5,     # Doximity - Physician network, niche social
    "APP": 4.5,      # AppLovin - Mobile gaming ads, hit-driven
    "UPWK": 4.5,     # Upwork - Freelance marketplace, gig economy
    "CPAY": 4.5,     # Corpay - B2B payments, fuel cards
    "EME": 4.5,      # EMCOR - Construction services
    "IESC": 4.5,     # IES Holdings - Electrical construction
    "MHO": 4.5,      # M/I Homes - Homebuilder, cyclical
    "UL": 4.5,       # Unilever - Consumer goods, slow growth
    "SNA": 4.5,      # Snap-on - Professional tools
    "CMI": 4.5,      # Cummins - Engine manufacturing, cyclical
    "UNP": 4.5,      # Union Pacific - Railroad, regulated utility
    "LIN": 4.5,      # Linde - Industrial gases
    "APD": 4.5,      # Air Products - Industrial gases
    "ECL": 4.5,      # Ecolab - Cleaning chemicals
    "ROK": 4.5,      # Rockwell Automation - Industrial automation
    "NVMI": 4.5,     # Nova - Semi measuring tools
    "ONTO": 4.5,     # Onto Innovation - Semi inspection
    "TPL": 4.5,      # Texas Pacific Land - Land royalties, commodity
    "ELF": 4.5,      # e.l.f. Beauty - Cosmetics, very competitive
    "EW": 4.5,       # Edwards Lifesciences - Heart valves
    "XYL": 4.5,      # Xylem - Water technology
    "GGG": 4.5,      # Graco - Fluid handling equipment
    "UHS": 4.5,      # Universal Health Services - Hospital operator
    "SAP": 4.5,      # SAP - Enterprise software, legacy ERP
    "LRN": 4.5,      # Stride - K-12 online education
    "IDCC": 4.5,     # InterDigital - Wireless IP licensing
    "AWI": 4.5,      # Armstrong World - Ceiling tiles
    "USLM": 4.5,     # U.S. Lime & Minerals - Lime production
    "INOD": 4.5,     # Innodata - AI data services, low margins
    "PMTS": 4.5,     # CPI Card Group - Payment cards manufacturing
    "ESQ": 4.5,      # Esquire Financial - Commercial banking, niche
    "MGIC": 4.5,     # MGIC Investment - Mortgage insurance, housing
    "AMPH": 4.4,     # Amphastar - Generic pharma, low margins
    "MLI": 4.4,      # Mueller Industries - Copper/brass products
    "KMI": 4.3,      # Kinder Morgan - Pipelines, MLP structure
    "ELMD": 4.3,     # Electromed - Respiratory therapy, tiny scale
    "YELP": 4.2,     # Yelp - Local reviews, losing to Google
    "BSVN": 4.2,     # Bank7 Corp - Micro bank, limited scale
    "ENB": 4.2,      # Enbridge - Canadian pipelines
    "WPM": 4.2,      # Wheaton Precious Metals - Gold/silver streaming
    "ACAD": 4.1,     # Acadia Pharma - Biotech, single drug focus
    "PJT": 4.0,      # PJT Partners - M&A advisory, deal cyclical
    
    # === 🔴 WEAK TIER (0-3.9) ===
    
    "ATEN": 3.9,     # A10 Networks - Security appliances, small scale
    "NEM": 3.3,      # Newmont - Gold miner, commodity hell
    "SLB": 3.2,      # Schlumberger - Oilfield services, highly cyclical
    "FSLR": 3.1,     # First Solar - Solar panels, Chinese competition
    "TDOC": 2.1,     # Teladoc - Unprofitable telehealth, $1B loss
    "BMRN": 3.0,     # BioMarin - Biotech, cash burn
    "UTHR": 3.0,     # United Therapeutics - Single drug risk
    "INCY": 3.0,     # Incyte - Biotech struggles
    "EXAS": 3.0,     # Exact Sciences - Cancer screening, losses
    "ABMD": 2.8,     # Abiomed (now owned by J&J) - Heart pumps
    "WDFC": 6.8,     # WD-40 - Single product, good margins but limited
    "CW": 7.8,       # Curtiss-Wright - Defense electronics, strong niche
    "WAT": 7.7,      # Waters Corp - Lab instruments, premium position
    "CLH": 7.6,      # Clean Harbors - Hazmat services, environmental niche
    "AWK": 7.5,      # American Water Works - Water utility, regulated
    "FERG": 8.2,     # Ferguson - Plumbing distribution, scale leader
    "JBHT": 6.9,     # J.B. Hunt - Intermodal transport, cyclical
}
