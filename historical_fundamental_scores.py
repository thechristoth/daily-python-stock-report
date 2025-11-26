STOCK_SCORES = {
    # TIER 1: ELITE COMPOUNDERS - Dominant moats, 40%+ ROIC, asset-light models
    "NVDA": "8.9",  # AI revolution leader, 56% ROIC, tech dominance
    "MSFT": "9.1",  # Cloud + AI + productivity monopoly, recurring revenue
    "GOOGL": "8.6",  # Search monopoly, 28% ROIC, advertising duopoly
    "GOOG": "8.6",  # Same as GOOGL
    "META": "8.4",  # Social media dominance, high cash flow margins
    "ASML": "9.1",  # EUV lithography monopoly, semiconductor equipment
    "BKNG": "6.9",  # 96% ROIC (highest), online travel platform leader
    "MA": "6.7",  # Payments network, toll-road business model
    "V": "6.1",  # Payments duopoly with MA, exceptional ROIC
    "AVGO": "7.2",  # Semiconductor + infrastructure software, strong FCF
    
    # TIER 2: QUALITY SOFTWARE/TECH - High switching costs, SaaS models
    "PAYC": "9.8",  # Payroll SaaS, 40%+ ROIC, asset-light
    "SNPS": "9.2",  # EDA duopoly with CDNS, design software moat
    "CDNS": "8.8",  # EDA duopoly, high switching costs
    "ADBE": "9.2",  # Creative software monopoly, subscription model
    "INTU": "8.9",  # Tax software moat, small business ecosystem
    "CRM": "8.7",  # CRM leader, platform lock-in
    "NOW": "7.5",  # IT workflow automation, high NRR
    "PANW": "8.2",  # Cybersecurity platform, network effects
    "FTNT": "9.4",  # Security appliances, integrated platform
    "WDAY": "8.4",  # HR/Finance cloud, enterprise lock-in
    "VEEV": "7.7",  # Life sciences cloud, regulatory moat
    "ADSK": "8.9",  # CAD software, design workflow lock-in
    "FICO": "8.2",  # Credit scoring duopoly, data moat
    "TYL": "7.5",  # Government software, high switching costs
    "PTC": "7.8",  # Industrial IoT software
    "MORN": "8.3",  # Investment research, data moat (mentioned as capital-light)
    
    # TIER 3: NICHE DOMINATORS - Specialized moats, pricing power
    "DECK": "9.5",  # Brand moat (Hoka, UGG), pricing power
    "COST": "8.9",  # Membership model, scale advantages
    "CBOE": "9.4",  # Exchange monopoly, VIX products
    "CME": "5.9",  # Derivatives exchange, network effects
    "ICE": "6.9",  # Exchange operator, data business
    "NDAQ": "5.4",  # Exchange + technology
    "SPGI": "8.3",  # Credit ratings duopoly, data moat
    "MCO": "6.8",  # Credit ratings duopoly with SPGI
    "MKTX": "6.6",  # Bond trading platform, network effects
    
    # TIER 4: INSURANCE - Underwriting discipline, float advantages
    "PGR": "9.4",  # Auto insurance, telematics moat
    "WRB": "7.0",  # Specialty insurance, underwriting discipline
    "BRO": "8.3",  # Insurance broker, fragmented market consolidator
    "CINF": "7.1",  # Regional insurance, conservative underwriting
    "CB": "6.2",  # Commercial insurance leader
    "KNSL": "9.3",  # E&S insurance, underwriting excellence
    "RLI": "8.2",  # Niche insurance specialist
    "PLMR": "8.9",  # Catastrophe insurance
    "ACGL": "7.3",  # Reinsurance, disciplined underwriting
    "ERIE": "7.9",  # Regional auto insurance
    
    # TIER 5: SPECIALTY INDUSTRIALS/SERVICES - Niche leaders
    "CPRT": "7.7",  # Salvage auction platform, network effects (mentioned as capital-light)
    "FAST": "8.5",  # Industrial distribution, vending machines
    "GWW": "7.9",  # MRO distribution, scale advantage (Grainger - wide moat)
    "CTAS": "7.6",  # Uniform rental, route density
    "ROL": "7.4",  # Pest control, route density, 34% ROIC
    "RSG": "6.3",  # Waste management, local monopolies
    "WM": "5.2",  # Waste management scale leader
    
    # TIER 6: SEMICONDUCTOR EQUIPMENT - Oligopoly, high barriers
    "AMAT": "6.9",  # Wafer fab equipment leader (wide moat mentioned)
    "LRCX": "4.9",  # Deposition equipment specialist
    "KLAC": "7.1",  # Inspection equipment monopoly
    "ONTO": "6.3",  # Advanced packaging equipment
    
    # TIER 7: MEDICAL DEVICES/HEALTHCARE - Innovation + switching costs
    "IDXX": "7.7",  # Vet diagnostics monopoly
    "DXCM": "8.8",  # CGM leader, data ecosystem
    "RMD": "9.1",  # Sleep apnea devices, cloud platform
    "PODD": "8.0",  # Insulin pumps, tubeless advantage
    "BSX": "6.1",  # Medical devices, cardiology focus
    "ISRG": "6.0",  # Surgical robotics, razor-blade model
    "ZTS": "7.7",  # Animal health leader
    "REGN": "8.4",  # Biotech, ophthalmology franchise
    
    # TIER 8: SPECIALIZED TECH/COMPONENTS
    "NVMI": "6.2",  # Semiconductor logistics
    "MPWR": "7.4",  # Power management ICs
    "APPF": "9.3",  # AppFolio property management SaaS
    "PCTY": "9.1",  # Paylocity HR/payroll SaaS
    "QLYS": "7.8",  # Cloud security/compliance
    "EXLS": "7.9",  # Business process services
    "MANH": "6.1",  # Supply chain software
    "DOCS": "6.4",  # Physician platform, network effects
    
    # TIER 9: SPECIALTY FINANCE - Capital efficiency
    "RJF": "8.6",  # Wealth management, advisor platform
    "MORN": "8.3",  # Investment research (already listed above)
    "FDS": "7.9",  # Financial data/analytics
    "APO": "5.8",  # Alternative asset manager
    "BLK": "6.3",  # ETF + asset management scale
    "GS": "3.8",  # Investment banking leader (new wide moat)
    "JPM": "5.4",  # Universal bank, scale advantages
    "MS": "3.9",  # Wealth management focus
    
    # TIER 10: PAYMENTS/FINTECH
    "PAYX": "8.1",  # Payroll processing, SMB focus
    "ADP": "7.3",  # Payroll leader, scale moat
    "FISV": "8.0",  # Payment processing, merchant services
    "FIS": "3.9",  # Banking technology (weak - already flagged)
    "AXP": "6.2",  # Closed-loop network, affluent customer base
    "COF": "6.0",  # Credit card issuer
    "PYPL": "8.0",  # Digital wallet, Venmo network
    
    # TIER 11: CONSUMER BRANDS - Pricing power
    "ULTA": "6.9",  # Beauty specialty retail
    "LULU": "7.7",  # Athletic apparel brand
    "CROX": "8.5",  # Footwear brand, comfort niche
    "ELF": "8.2",  # Cosmetics, value positioning
    "WING": "9.4",  # Restaurant, unit economics
    "TXRH": "7.8",  # Casual dining, experience moat
    "CMG": "7.7",  # Fast casual leader, digital integration
    "DPZ": "6.9",  # Pizza delivery, franchise model
    "QSR": "6.0",  # Tim Hortons + Burger King
    "YUM": "5.9",  # QSR franchisor (KFC, Taco Bell)
    "SBUX": "7.3",  # Coffee chain, rewards program
    
    # TIER 12: SEMICONDUCTORS - Design/manufacturing
    "AMD": "8.1",  # CPU/GPU competitor, data center growth
    "QCOM": "5.7",  # Mobile chips, licensing revenue
    "MRVL": "6.5",  # Data infrastructure chips
    "ON": "4.0",  # Power/sensing semiconductors
    "TXN": "3.3",  # Analog chips, diversified
    
    # TIER 13: CLOUD/SOFTWARE GROWTH
    "DDOG": "6.5",  # Observability platform
    "HUBS": "6.8",  # Marketing automation, CRM
    "BILL": "6.4",  # AP automation for SMB
    "WDAY": "8.4",  # Already listed above
    "ZS": "7.5",  # Zero trust security
    "NET": "6.7",  # CDN + security
    "ESTC": "6.3",  # Elastic search/observability
    "CFLT": "5.9",  # Data streaming platform
    "SHOP": "5.9",  # E-commerce platform for SMB
    "DUOL": "7.5",  # Language learning, gamification
    
    # TIER 14: SPECIALTY SMALL CAPS - Niche dominance
    "XPEL": "9.2",  # Paint protection film
    "MEDP": "9.3",  # CRO services, pricing power
    "APPF": "9.3",  # Already listed above
    "FIX": "9.4",  # Comfort Systems HVAC
    "IDCC": "9.0",  # Wireless tech licensing
    "SSD": "8.9",  # Simpson Manufacturing, connector products
    "OSIS": "8.2",  # Eye surgery equipment
    "EME": "8.2",  # Electrical infrastructure
    "IESC": "7.8",  # Infrastructure electrical services
    "UPWK": "8.5",  # Freelancer marketplace
    
    # TIER 15: REGIONAL/SPECIALTY FINANCE
    "EWBC": "8.0",  # East West Bank, US-China corridor
    "OFG": "7.7",  # Oriental Financial Group
    "BSVN": "7.2",  # Bank7 Corp
    "ESQ": "7.3",  # Esquire Financial
    "NMIH": "8.6",  # Mortgage insurance
    "AX": "7.8",  # Axos Financial, digital banking
    "DORM": "8.4",  # Dorman Products, auto parts
    "IPAR": "7.3",  # Inter Parfums
    
    # TIER 16: HOMEBUILDERS
    "DHI": "9.0",  # D.R. Horton, largest homebuilder
    "MHO": "7.8",  # M/I Homes
    "CVCO": "8.2",  # Cavco modular homes
    
    # TIER 17: HEALTHCARE SERVICES/TOOLS
    "ICLR": "7.9",  # Biotech CRO
    "IQV": "6.2",  # IQVIA, healthcare data
    "EXAS": "6.2",  # Cologuard, cancer screening
    "LRN": "4.7",  # Stride K-12 online education
    "CHWY": "6.7",  # Pet e-commerce
    "INMD": "6.6",  # InMode aesthetic devices
    "LNTH": "8.2",  # Lantheus medical imaging
    "UHS": "7.4",  # Universal Health Services
    
    # TIER 18: INDUSTRIAL/B2B SERVICES
    "NSSC": "7.9",  # NAPCO Security
    "STRL": "7.8",  # Sterling Infrastructure
    "HLI": "7.5",  # Houlihan Lokey investment banking
    "PJT": "6.0",  # PJT Partners advisory
    "FN": "8.4",  # Fabrinet optical components
    "TECH": "7.8",  # Bio-Techne life science tools
    "HLNE": "8.8",  # Hamilton Lane private markets
    "GCT": "9.0",  # GigaCloud B2B marketplace
    "NXT": "8.8",  # Nextracker solar trackers
    "AMPH": "9.0",  # Amphastar generic injectables
    "ELMD": "7.3",  # Electromed respiratory
    "CPRX": "6.8",  # Catalyst Pharma
    
    # TIER 19: INDUSTRIAL CONGLOMERATES/MATURE
    "BRK-B": "6.0",  # Berkshire Hathaway
    "HON": "3.9",  # Honeywell
    "ETN": "4.3",  # Eaton electrical
    "EMR": "4.2",  # Emerson automation
    "ITW": "4.1",  # Illinois Tool Works
    "CAT": "4.1",  # Caterpillar construction equipment
    "CMI": "5.5",  # Cummins engines
    "IR": "7.0",  # Ingersoll Rand compressors
    "PH": "6.5",  # Parker Hannifin motion/control
    "ROK": "4.7",  # Rockwell Automation
    
    # TIER 20: AEROSPACE/DEFENSE
    "LMT": "6.2",  # Lockheed Martin
    "RTX": "6.3",  # Raytheon Technologies
    "NOC": "6.0",  # Northrop Grumman
    "GD": "5.8",  # General Dynamics
    "LHX": "6.9",  # L3Harris
    "TDG": "6.3",  # TransDigm aircraft components
    "HEI": "7.2",  # HEICO aerospace components
    "AXON": "4.6",  # Axon body cameras/tasers
    
    # TIER 21: REAL ESTATE/INFRASTRUCTURE
    "AMT": "3.6",  # Cell tower REIT
    "SBAC": "3.4",  # Crown Castle towers
    "DLR": "5.8",  # Digital Realty data centers
    "EXR": "8.3",  # Extra Space Storage
    "PSA": "6.8",  # Public Storage
    "O": "7.9",  # Realty Income monthly dividend REIT
    "VICI": "7.1",  # Gaming properties REIT
    
    # TIER 22: PHARMA/BIOTECH
    "ABBV": "5.8",  # AbbVie (Humira biosimilar risk)
    "JNJ": "5.7",  # Johnson & Johnson diversified
    "BMRN": "4.9",  # BioMarin rare disease
    "UTHR": "4.8",  # United Therapeutics
    "ACAD": "5.7",  # Acadia neuropsych
    "EXEL": "8.2",  # Exelixis oncology
    "INCY": "6.3",  # Incyte oncology/inflammation
    
    # TIER 23: RETAIL/CONSUMER DISCRETIONARY
    "AMZN": "7.1",  # Amazon e-commerce + AWS
    "COST": "8.9",  # Already listed above
    "WMT": "6.8",  # Walmart scale + omnichannel
    "HD": "5.8",  # Home Depot DIY + pro
    "LOW": "5.4",  # Lowe's home improvement
    "TJX": "4.9",  # TJX off-price retail
    "ROST": "5.1",  # Ross Stores off-price
    "DKS": "6.9",  # Dick's Sporting Goods
    "BOOT": "6.5",  # Boot Barn western wear
    "ABNB": "5.1",  # Airbnb (weak - already flagged)
    
    # TIER 24: RESTAURANTS/HOSPITALITY
    "MCD": "5.5",  # McDonald's global franchise
    "MAR": "5.5",  # Marriott hotel franchise
    "HLT": "6.5",  # Hilton hotel franchise
    "BKNG": "6.9",  # Already listed above
    
    # TIER 25: MEDIA/ENTERTAINMENT
    "NFLX": "8.0",  # Netflix streaming leader, content library
    "DIS": "5.2",  # Disney (streaming losses, park cyclicality)
    "EA": "5.0",  # Electronic Arts gaming
    "PINS": "5.9",  # Pinterest visual discovery
    
    # TIER 26: LIFE SCIENCES TOOLS
    "TMO": "6.9",  # Thermo Fisher lab equipment/consumables
    "DHR": "5.5",  # Danaher (mentioned - diagnostic reliability moat)
    "ABT": "6.0",  # Abbott diagnostics/devices
    "WST": "7.0",  # West Pharmaceutical drug delivery
    "SYK": "3.8",  # Stryker medical devices
    "EW": "4.3",  # Edwards Lifesciences heart valves
    "HOLX": "4.6",  # Hologic women's health
    
    # TIER 27: CHEMICALS/MATERIALS
    "LIN": "5.5",  # Linde industrial gases
    "APD": "3.2",  # Air Products gases
    "SHW": "6.5",  # Sherwin-Williams paint
    "ECL": "3.1",  # Ecolab cleaning/sanitation
    "VMC": "6.9",  # Vulcan Materials aggregates
    "MLM": "6.8",  # Martin Marietta aggregates
    
    # TIER 28: ENERGY (Lower quality, commodity exposure)
    "XOM": "3.8",  # ExxonMobil
    "SLB": "3.8",  # Schlumberger
    "COP": "6.1",  # ConocoPhillips
    "NEM": "6.6",  # Newmont Mining gold
    "WPM": "0.5",  # Wheaton Precious Metals (very low score)
    
    # TIER 29: UTILITIES/INFRASTRUCTURE (Low growth)
    "UNP": "2.5",  # Union Pacific railroad
    "ENB": "2.9",  # Enbridge pipelines
    "KMI": "2.8",  # Kinder Morgan pipelines
    
    # TIER 30: INTERNATIONAL/ADRs
    "TSM": "0.5",  # Taiwan Semi (geopolitical risk despite dominance)
    "ASML": "9.1",  # Already listed above
    "SAP": "0.5",  # SAP enterprise software (low score)
    "TRI": "0.5",  # Thomson Reuters (low score)
    "UL": "0.5",  # Unilever (low score)
    
    # TIER 31: SPECULATIVE/LOWER QUALITY (Keep at end)
    "TSLA": "7.5",  # Tesla (execution risk, valuation)
    "PLTR": "6.9",  # Palantir (high growth but unprofitable for years)
    "ATEN": "3.1",  # A10 Networks (already listed - growing well though)
    "MCHP": "2.9",  # Microchip Technology
    "GATX": "4.5",  # GATX railcar leasing (already listed - growing well)
    "ROP": "3.5",  # Roper Technologies
    "AME": "4.9",  # Ametek instrumentation
    "KEYS": "5.8",  # Keysight test equipment
    "TDY": "7.0",  # Teledyne imaging/instrumentation
    "TRMB": "5.6",  # Trimble positioning tech
    "VRSK": "5.0",  # Verisk analytics
    "VRSN": "4.9",  # VeriSign domain registry
    "IEX": "5.0",  # IDEX fluid handling
    "GGG": "6.3",  # Graco fluid handling
    "MSI": "6.3",  # Motorola Solutions
    "FSLR": "4.6",  # First Solar
    "PWR": "7.7",  # Quanta Services utility infrastructure
    "EPAM": "8.2",  # EPAM IT services
    "GDDY": "7.3",  # GoDaddy domains/hosting
    "ODD": "7.9",  # Oddity beauty tech
    "CELH": "6.4",  # Celsius energy drinks
    "APP": "7.6",  # AppLovin mobile advertising
    "TTD": "7.8",  # Trade Desk programmatic ads
    "CSGP": "8.4",  # CoStar Group real estate data
    "VRT": "6.5",  # Vertiv data center infrastructure
    "SN": "7.7",  # SharkNinja appliances
    "BR": "7.1",  # Broadridge financial communications
    "LMAT": "7.3",  # LeMaitre Vascular
    "USLM": "7.0",  # United States Lime & Minerals
    "BMI": "4.7",  # Badger Meter water tech
    "CARG": "5.2",  # CarGurus auto marketplace
    "HALO": "7.0",  # Halozyme drug delivery
    "MLI": "4.5",  # Mueller Industries copper/brass
    "AWI": "6.0",  # Armstrong World ceilings
    "A": "5.7",  # Agilent (mentioned - lab equipment)
    "POOL": "6.3",  # Pool Corp distribution
    "DT": "7.6",  # Dynatrace observability
    "QFIN": "7.4",  # 360 DigiTech China fintech
    "CPNG": "5.7",  # Coupang Korea e-commerce
    "MELI": "8.2",  # MercadoLibre LatAm e-commerce
    "ORCL": "5.9",  # Oracle database/cloud
    "AAPL": "5.3",  # Apple (mature, iPhone-dependent)
    "ANET": "6.6",  # Arista Networks data center
    "APH": "7.2",  # Amphenol connectors
    "BLDR": "6.8",  # Builders FirstSource building materials
    "CPAY": "6.6",  # Corpay B2B payments
    "FROG": "6.5",  # JFrog DevOps platform
    "PMTS": "6.6",  # CPI Card Group payments
    "SNA": "5.8",  # Snap-on tools
    "TPL": "6.0",  # Texas Pacific Land royalties
    "ATKR": "6.1",  # Atkore electrical/mechanical
    "IRMD": "6.5",  # IRadimed MRI devices
    "SFM": "7.2",  # Sprouts Farmers Market
    "HRMY": "6.5",  # Harmony Biosciences
    "CW": "6.3",  # Curtiss-Wright defense
    "FSS": "7.2",  # Federal Signal emergency vehicles
    "INOD": "6.8",  # Innodata AI data services
    "MSA": "6.6",  # MSA Safety protective equipment
    "DAVE": "8.2",  # Dave banking app
}
