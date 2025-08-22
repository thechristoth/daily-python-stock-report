import requests
import random
import time
from datetime import datetime
import os
from bs4 import BeautifulSoup

# Configuration
STOCKS = [
     "MSFT", "AAPL", "NVDA", "GOOGL", "META", "AMZN", "ADBE", "CRM", "NOW", "INTU",
    "ORCL", "CDNS", "SNPS", "ADSK", "SPGI", "MCO", "MSCI", "FICO", "TYL", "VEEV",
    "VRSK", "MA", "V", "ICE", "CME", "PAYX", "ADP", "ASML", "AVGO", "EQIX",
    "PG", "HD", "LOW", "COST", "PEP", "MCD", "SBUX", "JNJ", "ABT", "SYK",
    "BSX", "ZTS", "DHR", "REGN", "PGR", "CB", "WRB", "BRK-B", "SCHW", "ITW",
    "UNP", "GWW", "TT", "IR", "ECL", "NOC", "BKNG", "MAR", "HLT", "LRCX",
    "KLAC", "CSGP", "ABBV", "WST", "POOL", "ISRG", "TMO", "IDXX", "ROP", "AMT",
    "SBAC", "MNST", "YUM", "MKTX", "TDG", "ORLY", "AZO", "FAST", "CTAS", "AME",
    "IEX", "TDY", "KEYS", "CHD", "SHW", "MKC", "DPZ", "CMG", "QSR", "KO",
    "WMT", "ROST", "NDAQ", "TRI", "CTSH", "EPAM", "CHKP", "CINF", "BR",
    "DLR", "PSA", "EXR", "O", "KMI", "ENB", "WM", "RSG", "UPS", "FDX",
    "LHX", "HEI", "XYL", "ETN", "PH", "VMC", "MLM", "SAP", "NVO",
    "UL", "GILD", "MDT", "EW", "HOLX", "ON",
    "WDAY", "DDOG", "PANW", "FTNT", "NFLX", "DXCM", "SQ", "SHOP", "MELI", "ABNB",
    "ETSY", "DASH", "PLTR", "ANET", "OKTA", "DOCU", "DUOL", "LULU", "ULTA", "CELH",
    "PODD", "TOST", "CPRT", "ENPH", "PINS", "APP", "QFIN", "GDDY", "HIMS", "SMCI",
    "PWP", "PYPL", "ILMN", "TRMB", "FSLR", "ZM", "TSM", "TXN", "ADI", "QCOM",
    "JPM", "GS", "BLK", "AXP", "MS", "CAT", "LIN", "APD", "EMR", "HON",
    "XOM", "CVX", "COP", "EOG", "LMT", "RTX", "GD", "NKE", "TJX", "TSLA",
    "SOFI", "HOOD", "BABA", "SE", "DIS",
    "CMCSA", "CHTR", "EA"
]
USER_AGENTS = [
    'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36',
    'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36',
    'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:89.0) Gecko/20100101 Firefox/89.0',
    'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/14.1.15 Safari/605.1.15'
]
DELAY_BETWEEN_REQUESTS = 5  # seconds
HTML_FILE = os.path.join(os.getcwd(), 'index.html')
HTML_TEMPLATE_FILE = os.path.join(os.getcwd(), 'index.html')
MAX_RETRIES = 3

def get_random_user_agent():
    return random.choice(USER_AGENTS)

def parse_growth_value(value):
    """Helper function to parse growth values that come as '3Y%/5Y%'"""
    if not value or value == '-' or value == 'N/A':
        return None
    try:
        # Split the value and take the second part (5Y growth)
        parts = value.split()
        if len(parts) >= 2:
            return float(parts[-1].replace('%', ''))
        return float(value.replace('%', ''))
    except ValueError:
        return None

def parse_percentage(value):
    """Parse percentage values"""
    if not value or value == '-' or value == 'N/A':
        return None
    try:
        return float(value.replace('%', ''))
    except ValueError:
        return None

def parse_float(value):
    """Helper function to parse string values into floats"""
    if not value or value == '-' or value == 'N/A':
        return None
    try:
        # Remove percentage signs, commas, and 'B'/'M' suffixes
        cleaned = value.replace('%', '').replace(',', '').replace('B', '').replace('M', '')
        return float(cleaned)
    except ValueError:
        return None

def calculate_fcf_metrics(metrics):
    """Calculate FCF and FCF yield based on P/FCF and Price"""
    if not metrics or not metrics.get('P/FCF') or not metrics.get('Price'):
        return None, None, None
    
    try:
        p_fcf = metrics['P/FCF']
        price = metrics['Price']
        market_cap = metrics.get('Market_Cap')
        
        # Calculate FCF per share: Price / P/FCF
        fcf_per_share = price / p_fcf if p_fcf != 0 else None
        
        # Calculate total FCF if we have market cap (in billions)
        total_fcf = None
        if market_cap and fcf_per_share:
            # Market cap is in billions, convert to actual value
            shares_outstanding = (market_cap * 1_000_000_000) / price
            total_fcf = fcf_per_share * shares_outstanding / 1_000_000_000  # Back to billions
        
        # Calculate FCF yield: FCF per share / Price
        fcf_yield = (fcf_per_share / price * 100) if fcf_per_share and price else None
        
        return fcf_per_share, total_fcf, fcf_yield
        
    except (ZeroDivisionError, TypeError):
        return None, None, None

def fetch_comprehensive_metrics(stock):
    """Fetch comprehensive stock metrics from Finviz"""
    url = f'https://finviz.com/quote.ashx?t={stock}'
    headers = {
        'User-Agent': get_random_user_agent(),
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
        'Accept-Language': 'en-US,en;q=0.5',
    }
    
    for attempt in range(MAX_RETRIES):
        try:
            response = requests.get(url, headers=headers, timeout=10)
            response.raise_for_status()
            
            if 'Too Many Requests' in response.text:
                raise Exception("Rate limited by Finviz")
            
            soup = BeautifulSoup(response.text, 'html.parser')
            snapshot_table = soup.find('table', class_='snapshot-table2')
            if not snapshot_table:
                print(f"No snapshot table found for {stock}")
                return None, None
                
            # Extract all table cells
            cells = [td.text.strip() for td in snapshot_table.find_all('td')]
            
            # Create a dictionary to map labels to values
            metrics = {}
            for i in range(0, len(cells)-1, 2):
                metrics[cells[i]] = cells[i+1]
            
            # Extract sector information
            sector = None
            try:
                # Try to find sector information in the page
                for key, value in metrics.items():
                    if 'sector' in key.lower():
                        sector = value
                        break
                
                # If not found in metrics, try to find it in the page content
                if not sector:
                    sector_elem = soup.find('a', href=lambda x: x and 'screener.ashx' in x and 'sec' in x)
                    if sector_elem:
                        sector = sector_elem.text.strip()
            except:
                sector = None
            
            # Extract comprehensive metrics
            result = {
                # Valuation Metrics
                'PE': parse_float(metrics.get('P/E', '-')),
                'PEG': parse_float(metrics.get('PEG', '-')),
                'Forward_PE': parse_float(metrics.get('Forward P/E', '-')),
                'P/S': parse_float(metrics.get('P/S', '-')),
                'P/B': parse_float(metrics.get('P/B', '-')),
                'P/FCF': parse_float(metrics.get('P/FCF', '-')),
                'EV/EBITDA': parse_float(metrics.get('EV/EBITDA', '-')),
                'EV/Sales': parse_float(metrics.get('EV/Sales', '-')),
                
                # Growth Metrics
                'EPS_TTM': parse_float(metrics.get('EPS (ttm)', '-')),
                'EPS_next_Y': parse_float(metrics.get('EPS next Y', '-')),
                'EPS_this_Y': parse_percentage(metrics.get('EPS this Y', '-')),
                'EPS_next_Y_growth': parse_percentage(metrics.get('EPS next Y', '-')),  # This is growth %
                'EPS_next_5Y': parse_percentage(metrics.get('EPS next 5Y', '-')),
                'EPS_past_5Y': parse_growth_value(metrics.get('EPS past 3/5Y', '-')),
                'EPS_YoY_TTM': parse_percentage(metrics.get('EPS Y/Y TTM', '-')),
                'EPS_QoQ': parse_percentage(metrics.get('EPS Q/Q', '-')),
                'Sales_past_5Y': parse_growth_value(metrics.get('Sales past 3/5Y', '-')),
                'Sales_YoY_TTM': parse_percentage(metrics.get('Sales Y/Y TTM', '-')),
                'Sales_QoQ': parse_percentage(metrics.get('Sales Q/Q', '-')),
                
                # Stability/Quality Metrics
                'Debt/Eq': parse_float(metrics.get('Debt/Eq', '-')),
                'LT_Debt/Eq': parse_float(metrics.get('LT Debt/Eq', '-')),
                'Current_Ratio': parse_float(metrics.get('Current Ratio', '-')),
                'Quick_Ratio': parse_float(metrics.get('Quick Ratio', '-')),
                'ROE': parse_percentage(metrics.get('ROE', '-')),
                'ROA': parse_percentage(metrics.get('ROA', '-')),
                'ROIC': parse_percentage(metrics.get('ROIC', '-')),
                'Gross_Margin': parse_percentage(metrics.get('Gross Margin', '-')),
                'Oper_Margin': parse_percentage(metrics.get('Oper. Margin', '-')),
                'Profit_Margin': parse_percentage(metrics.get('Profit Margin', '-')),
                'Cash_per_sh': parse_float(metrics.get('Cash/sh', '-')),
                'Book_per_sh': parse_float(metrics.get('Book/sh', '-')),
                
                # Market Metrics
                'Beta': parse_float(metrics.get('Beta', '-')),
                'RSI': parse_float(metrics.get('RSI (14)', '-')),
                'Volatility': parse_float(metrics.get('Volatility', '-')),  # Will take first value
                'Insider_Own': parse_percentage(metrics.get('Insider Own', '-')),
                'Inst_Own': parse_percentage(metrics.get('Inst Own', '-')),
                'Short_Float': parse_percentage(metrics.get('Short Float', '-')),
                
                # Performance
                'Perf_YTD': parse_percentage(metrics.get('Perf YTD', '-')),
                'Perf_Year': parse_percentage(metrics.get('Perf Year', '-')),
                'Perf_3Y': parse_percentage(metrics.get('Perf 3Y', '-')),
                'Perf_5Y': parse_percentage(metrics.get('Perf 5Y', '-')),
                
                # Basic Info
                'Price': parse_float(metrics.get('Price', '-')),
                'Market_Cap': parse_float(metrics.get('Market Cap', '-')),
                'Sales': parse_float(metrics.get('Sales', '-'))
            }
            
            # Calculate FCF metrics
            fcf_per_share, total_fcf, fcf_yield = calculate_fcf_metrics(result)
            result['FCF_per_share'] = fcf_per_share
            result['Total_FCF'] = total_fcf
            result['FCF_Yield'] = fcf_yield
            
            return result, sector
            
        except Exception as e:
            print(f"Attempt {attempt + 1} failed for {stock}: {str(e)}")
            if attempt < MAX_RETRIES - 1:
                wait_time = DELAY_BETWEEN_REQUESTS * (attempt + 1)
                print(f"Waiting {wait_time} seconds before retry...")
                time.sleep(wait_time)
            else:
                print(f"Max retries reached for {stock}")
                return None, None

def calculate_enhanced_scores_with_sectors(metrics, sector=None):
    """
    Calculate enhanced valuation, quality, stability, and growth scores
    with sector-specific adjustments and value stock considerations
    """
    if not metrics:
        return None
    
    # ================== SECTOR-SPECIFIC CONFIGURATIONS ==================
    SECTOR_CONFIGS = {
        'Technology': {
            'pe_thresholds': [25, 35, 50, 70],  # good, fair, poor, terrible
            'roe_thresholds': [20, 15, 12, 8],
            'roic_thresholds': [25, 20, 15, 10],
            'debt_eq_max': 0.5,
            'growth_expectations': 'high',  # 15%+ expected
            'margin_focus': 'gross',  # Focus on gross margins
            'fcf_yield_min': 2.0,
            'dividend_weight': 0.1  # Low dividend expectation
        },
        'Consumer_Staples': {
            'pe_thresholds': [22, 28, 35, 45],
            'roe_thresholds': [18, 15, 12, 8],
            'roic_thresholds': [20, 15, 12, 8],
            'debt_eq_max': 0.8,
            'growth_expectations': 'moderate',  # 8-15%
            'margin_focus': 'operating',
            'fcf_yield_min': 4.0,
            'dividend_weight': 0.25  # Higher dividend expectation
        },
        'Utilities': {
            'pe_thresholds': [18, 22, 28, 35],
            'roe_thresholds': [12, 10, 8, 6],
            'roic_thresholds': [8, 7, 6, 4],
            'debt_eq_max': 1.5,  # Utilities naturally have more debt
            'growth_expectations': 'low',  # 3-8%
            'margin_focus': 'operating',
            'fcf_yield_min': 6.0,
            'dividend_weight': 0.4  # High dividend expectation
        },
        'Financials': {
            'pe_thresholds': [12, 15, 20, 25],
            'roe_thresholds': [15, 12, 10, 8],
            'roic_thresholds': [12, 10, 8, 6],
            'debt_eq_max': 10.0,  # Banks use leverage differently
            'growth_expectations': 'moderate',
            'margin_focus': 'net_interest',
            'fcf_yield_min': 3.0,
            'dividend_weight': 0.3,
            'use_financial_metrics': True  # Special handling
        },
        'Healthcare': {
            'pe_thresholds': [20, 25, 35, 50],
            'roe_thresholds': [18, 15, 12, 8],
            'roic_thresholds': [20, 15, 12, 8],
            'debt_eq_max': 0.6,
            'growth_expectations': 'moderate',
            'margin_focus': 'gross',
            'fcf_yield_min': 3.0,
            'dividend_weight': 0.2
        },
        'Energy': {
            'pe_thresholds': [15, 20, 30, 40],
            'roe_thresholds': [15, 12, 8, 5],
            'roic_thresholds': [12, 10, 8, 5],
            'debt_eq_max': 1.0,
            'growth_expectations': 'cyclical',
            'margin_focus': 'operating',
            'fcf_yield_min': 8.0,  # High FCF expectation
            'dividend_weight': 0.35,
            'cyclical_adjustment': True
        },
        'Industrials': {
            'pe_thresholds': [20, 25, 35, 45],
            'roe_thresholds': [15, 12, 10, 7],
            'roic_thresholds': [15, 12, 10, 7],
            'debt_eq_max': 0.8,
            'growth_expectations': 'moderate',
            'margin_focus': 'operating',
            'fcf_yield_min': 4.0,
            'dividend_weight': 0.2
        }
    }
    
    # Default configuration for unknown sectors
    DEFAULT_CONFIG = SECTOR_CONFIGS['Technology']  # Use tech as baseline
    
    # Get sector configuration
    if sector and sector in SECTOR_CONFIGS:
        config = SECTOR_CONFIGS[sector]
    else:
        config = DEFAULT_CONFIG
        sector = 'Unknown'
    
    # ================== ENHANCED VALUATION SCORING ==================
    valuation_score = 0
    valuation_components = []
    
    # Adjust PEG weight based on sector (reduce for value-oriented sectors)
    if config['dividend_weight'] > 0.25:  # Value sectors
        peg_weight = 0.25  # Reduced from 0.4
        pe_weight = 0.25   # Increased from 0.2
        div_weight = 0.25  # New dividend component
        ps_weight = 0.15   # Reduced
        ev_ebitda_weight = 0.1
    else:  # Growth sectors
        peg_weight = 0.35  # Slightly reduced from 0.4
        pe_weight = 0.2
        div_weight = config['dividend_weight']
        ps_weight = 0.2 - div_weight
        ev_ebitda_weight = 0.25 - div_weight
    
    # PEG Score with sector-adjusted expectations
    peg_score = 5
    if metrics['PEG'] is not None:
        peg = metrics['PEG']
        
        # Adjust PEG thresholds based on growth expectations
        if config['growth_expectations'] == 'high':
            thresholds = [0.5, 0.8, 1.0, 1.3, 1.7, 2.0, 3.0]
        elif config['growth_expectations'] == 'low':
            thresholds = [0.3, 0.5, 0.8, 1.0, 1.2, 1.5, 2.0]
        else:  # moderate
            thresholds = [0.4, 0.6, 0.9, 1.2, 1.5, 1.8, 2.5]
        
        if peg < thresholds[0]:
            peg_score = 10
        elif peg < thresholds[1]:
            peg_score = 9
        elif peg < thresholds[2]:
            peg_score = 8
        elif peg < thresholds[3]:
            peg_score = 7
        elif peg < thresholds[4]:
            peg_score = 6
        elif peg < thresholds[5]:
            peg_score = 5
        elif peg < thresholds[6]:
            peg_score = 3
        else:
            peg_score = 1
            
        valuation_components.append(('PEG', peg_score, peg_weight))
    
    # Enhanced P/E Analysis with sector-specific thresholds
    pe_score = 5
    if metrics['PE'] is not None:
        pe = metrics['PE']
        forward_pe = metrics.get('Forward_PE')
        
        # Use sector-specific P/E thresholds
        pe_good, pe_fair, pe_poor, pe_terrible = config['pe_thresholds']
        
        if forward_pe is not None:
            target_pe = forward_pe
        else:
            target_pe = pe
        
        if target_pe < pe_good:
            pe_score = 9
        elif target_pe < pe_fair:
            pe_score = 7
        elif target_pe < pe_poor:
            pe_score = 5
        elif target_pe < pe_terrible:
            pe_score = 3
        else:
            pe_score = 1
        
        # Bonus for improving outlook
        if forward_pe and forward_pe < pe * 0.9:
            pe_score = min(10, pe_score + 1)
        
        valuation_components.append(('P/E', pe_score, pe_weight))
    
    # Dividend Yield Score (for value/income sectors)
    if div_weight > 0:
        div_score = 5
        div_yield = metrics.get('Dividend_Yield')
        if div_yield is not None:
            if config['growth_expectations'] == 'low':  # Utilities, REITs
                if div_yield > 6:      div_score = 10
                elif div_yield > 4:    div_score = 8
                elif div_yield > 3:    div_score = 6
                elif div_yield > 2:    div_score = 4
                else:                  div_score = 2
            else:  # Consumer staples, etc.
                if div_yield > 4:      div_score = 9
                elif div_yield > 3:    div_score = 8
                elif div_yield > 2.5:  div_score = 7
                elif div_yield > 2:    div_score = 6
                elif div_yield > 1:    div_score = 4
                else:                  div_score = 2
            
            # Bonus for dividend growth consistency
            div_growth = metrics.get('Dividend_Growth_5Y')
            if div_growth and div_growth > 5:
                div_score = min(10, div_score + 1)
                
            valuation_components.append(('Dividend', div_score, div_weight))
    
    # EV/EBITDA with sector adjustments
    if ev_ebitda_weight > 0:
        ev_ebitda_score = 5
        if metrics['EV/EBITDA'] is not None:
            ev_ebitda = metrics['EV/EBITDA']
            
            # Adjust thresholds for capital-intensive sectors
            if sector in ['Utilities', 'Energy', 'Industrials']:
                if ev_ebitda < 10:    ev_ebitda_score = 10
                elif ev_ebitda < 15:  ev_ebitda_score = 8
                elif ev_ebitda < 20:  ev_ebitda_score = 6
                elif ev_ebitda < 30:  ev_ebitda_score = 4
                else:                 ev_ebitda_score = 2
            else:  # Less capital intensive
                if ev_ebitda < 8:     ev_ebitda_score = 10
                elif ev_ebitda < 12:  ev_ebitda_score = 8
                elif ev_ebitda < 16:  ev_ebitda_score = 6
                elif ev_ebitda < 25:  ev_ebitda_score = 4
                else:                 ev_ebitda_score = 2
                
            valuation_components.append(('EV/EBITDA', ev_ebitda_score, ev_ebitda_weight))
    
    # P/S Score with sector and margin adjustments
    if ps_weight > 0:
        ps_score = 5
        if metrics['P/S'] is not None:
            ps = metrics['P/S']
            profit_margin = metrics.get('Profit_Margin', 10) or 10
            
            # Sector-specific P/S expectations
            if sector == 'Technology':
                if profit_margin > 20:
                    thresholds = [8, 15, 25, 40]
                else:
                    thresholds = [4, 8, 15, 25]
            elif sector in ['Utilities', 'Energy']:
                thresholds = [1.5, 3, 5, 8]
            else:  # Consumer, Healthcare, etc.
                if profit_margin > 15:
                    thresholds = [4, 8, 15, 25]
                else:
                    thresholds = [2, 4, 8, 15]
            
            if ps < thresholds[0]:      ps_score = 9
            elif ps < thresholds[1]:    ps_score = 7
            elif ps < thresholds[2]:    ps_score = 5
            elif ps < thresholds[3]:    ps_score = 3
            else:                       ps_score = 1
                
            valuation_components.append(('P/S', ps_score, ps_weight))
    
    # Calculate weighted valuation score
    if valuation_components:
        valuation_score = sum(score * weight for _, score, weight in valuation_components)
        total_weight = sum(weight for _, _, weight in valuation_components)
        if total_weight > 0:
            valuation_score = valuation_score / total_weight
    
    # ================== SECTOR-ADJUSTED QUALITY SCORE ==================
    quality_components = []
    red_flags = []
    warnings = []
    
    # 1. PROFITABILITY EXCELLENCE (35% weight)
    profitability_score = 0
    prof_factors = []
    
    # ROE Score with sector thresholds
    roe_score = 5
    roe = metrics.get('ROE')
    if roe is not None:
        roe_excellent, roe_good, roe_fair, roe_poor = config['roe_thresholds']
        
        if roe > roe_excellent:     roe_score = 10
        elif roe > roe_good:        roe_score = 8
        elif roe > roe_fair:        roe_score = 6
        elif roe > roe_poor:        roe_score = 4
        elif roe > roe_poor * 0.6:  roe_score = 2
        else:                       roe_score = 1
        prof_factors.append(('ROE', roe_score, 0.4))
    
    # ROIC Score with sector thresholds
    roic_score = 5
    roic = metrics.get('ROIC')
    if roic is not None:
        roic_excellent, roic_good, roic_fair, roic_poor = config['roic_thresholds']
        
        if roic > roic_excellent:     roic_score = 10
        elif roic > roic_good:        roic_score = 8
        elif roic > roic_fair:        roic_score = 6
        elif roic > roic_poor:        roic_score = 4
        elif roic > roic_poor * 0.6:  roic_score = 2
        else:                         roic_score = 1
        prof_factors.append(('ROIC', roic_score, 0.4))
    
    # Sector-specific ROE vs ROIC analysis
    if roe is not None and roic is not None and not config.get('use_financial_metrics', False):
        roe_roic_ratio = roe / roic if roic != 0 else float('inf')
        
        # More lenient for sectors that naturally use more leverage
        if sector in ['Utilities', 'Energy']:
            leverage_tolerance = 2.5
        else:
            leverage_tolerance = 2.0
        
        if roe_roic_ratio > leverage_tolerance:
            red_flags.append(f"ROE ({roe}%) significantly higher than ROIC ({roic}%) for {sector}")
            roe_score = max(1, roe_score - 2)
        elif roe_roic_ratio > 1.8:
            warnings.append(f"ROE ({roe}%) moderately higher than ROIC ({roic}%)")
            roe_score = max(1, roe_score - 1)
    
    # Margin Score (focus on sector-appropriate margin type)
    margin_score = 5
    if config['margin_focus'] == 'gross':
        margin = metrics.get('Gross_Margin')
        if margin is not None:
            if margin > 70:      margin_score = 10
            elif margin > 60:    margin_score = 9
            elif margin > 50:    margin_score = 8
            elif margin > 40:    margin_score = 6
            elif margin > 30:    margin_score = 4
            else:                margin_score = 2
    else:  # operating or profit margin
        margin = metrics.get('Profit_Margin')
        if margin is not None:
            # Sector-adjusted margin expectations
            if sector == 'Technology':
                thresholds = [25, 20, 15, 12, 8]
            elif sector in ['Consumer_Staples', 'Healthcare']:
                thresholds = [15, 12, 10, 8, 5]
            elif sector in ['Utilities', 'Energy']:
                thresholds = [12, 10, 8, 6, 3]
            else:
                thresholds = [20, 15, 12, 8, 5]
            
            if margin > thresholds[0]:      margin_score = 10
            elif margin > thresholds[1]:    margin_score = 8
            elif margin > thresholds[2]:    margin_score = 6
            elif margin > thresholds[3]:    margin_score = 4
            elif margin > thresholds[4]:    margin_score = 2
            else:                           margin_score = 1
    
    if margin_score > 5:  # Only add if we have margin data
        prof_factors.append(('Margins', margin_score, 0.2))
    
    if prof_factors:
        profitability_score = sum(score * weight for _, score, weight in prof_factors)
        total_weight = sum(weight for _, _, weight in prof_factors)
        profitability_score = profitability_score / total_weight if total_weight > 0 else 5
    
    quality_components.append(('Profitability Excellence', profitability_score, 0.35))
    
    # 2. CASH FLOW QUALITY (30% weight)
    cash_flow_score = 0
    cash_factors = []
    
    # FCF Score with sector-adjusted expectations
    fcf_score = 5
    fcf_per_share = metrics.get('FCF_per_share')
    fcf_yield = metrics.get('FCF_Yield')
    
    if fcf_per_share is not None:
        if fcf_per_share > 0:
            if fcf_yield is not None:
                min_yield = config['fcf_yield_min']
                if fcf_yield > min_yield * 1.5:      fcf_score = 10
                elif fcf_yield > min_yield * 1.2:    fcf_score = 9
                elif fcf_yield > min_yield:          fcf_score = 8
                elif fcf_yield > min_yield * 0.7:    fcf_score = 6
                elif fcf_yield > min_yield * 0.4:    fcf_score = 4
                else:                                fcf_score = 3
            else:
                fcf_score = 6
        else:
            fcf_score = 1
            red_flags.append("Negative Free Cash Flow")
        cash_factors.append(('FCF_Generation', fcf_score, 0.6))
    
    # Enhanced cash quality for different sectors
    cash_quality_score = 5
    p_fcf = metrics.get('P/FCF')
    pe = metrics.get('PE')
    
    if p_fcf is not None and pe is not None and pe > 0:
        cash_conversion_ratio = p_fcf / pe
        
        # Adjust expectations by sector
        if sector in ['Utilities', 'Energy']:  # Capital intensive
            if cash_conversion_ratio < 1.2:       cash_quality_score = 10
            elif cash_conversion_ratio < 1.5:     cash_quality_score = 8
            elif cash_conversion_ratio < 2.0:     cash_quality_score = 6
            else:                                  cash_quality_score = 3
        else:  # Less capital intensive
            if cash_conversion_ratio < 1.1:       cash_quality_score = 10
            elif cash_conversion_ratio < 1.3:     cash_quality_score = 8
            elif cash_conversion_ratio < 1.6:     cash_quality_score = 6
            else:                                  cash_quality_score = 3
                
        cash_factors.append(('Cash_Quality', cash_quality_score, 0.4))
    
    if cash_factors:
        cash_flow_score = sum(score * weight for _, score, weight in cash_factors)
        total_weight = sum(weight for _, _, weight in cash_factors)
        cash_flow_score = cash_flow_score / total_weight if total_weight > 0 else 5
    
    quality_components.append(('Cash Flow Quality', cash_flow_score, 0.30))
    
    # 3. FINANCIAL ROBUSTNESS (35% weight)
    financial_score = 0
    financial_factors = []
    
    # Sector-adjusted debt scoring
    debt_score = 5
    debt_eq = metrics.get('Debt/Eq')
    if debt_eq is not None:
        max_debt = config['debt_eq_max']
        
        if sector == 'Financials':
            # Banks use different metrics - this is a simplified approach
            # In reality, you'd want Tier 1 capital ratios, etc.
            if debt_eq < 8:      debt_score = 8
            elif debt_eq < 12:   debt_score = 6
            elif debt_eq < 15:   debt_score = 4
            else:                debt_score = 2
        else:
            if debt_eq < max_debt * 0.2:        debt_score = 10
            elif debt_eq < max_debt * 0.5:      debt_score = 9
            elif debt_eq < max_debt * 0.8:      debt_score = 7
            elif debt_eq < max_debt:            debt_score = 6
            elif debt_eq < max_debt * 1.5:      debt_score = 3
            else:                               debt_score = 1
            
            if debt_eq > max_debt:
                severity = "High" if debt_eq > max_debt * 1.5 else "Elevated"
                red_flags.append(f"{severity} debt for {sector}: D/E = {debt_eq:.2f}")
        
        financial_factors.append(('Debt_Quality', debt_score, 0.4))
    
    # Standard liquidity and cash position scoring (same as before)
    liquidity_score = 5
    current_ratio = metrics.get('Current_Ratio')
    if current_ratio is not None and sector != 'Financials':
        if current_ratio > 2.5:      liquidity_score = 10
        elif current_ratio > 2.0:    liquidity_score = 9
        elif current_ratio > 1.5:    liquidity_score = 7
        elif current_ratio > 1.2:    liquidity_score = 5
        elif current_ratio > 1.0:    liquidity_score = 3
        else:                        liquidity_score = 1
        
        if current_ratio < 1.0:
            red_flags.append(f"Poor liquidity: Current Ratio = {current_ratio:.1f}")
        
        financial_factors.append(('Liquidity', liquidity_score, 0.3))
    
    # Cash position
    cash_score = 5
    cash_per_sh = metrics.get('Cash_per_sh')
    price = metrics.get('Price')
    if cash_per_sh is not None and price is not None and price > 0:
        cash_ratio = cash_per_sh / price
        if cash_ratio > 0.3:        cash_score = 10
        elif cash_ratio > 0.2:      cash_score = 9
        elif cash_ratio > 0.15:     cash_score = 8
        elif cash_ratio > 0.1:      cash_score = 6
        elif cash_ratio > 0.05:     cash_score = 4
        else:                       cash_score = 2
        financial_factors.append(('Cash_Position', cash_score, 0.3))
    
    if financial_factors:
        financial_score = sum(score * weight for _, score, weight in financial_factors)
        total_weight = sum(weight for _, _, weight in financial_factors)
        financial_score = financial_score / total_weight if total_weight > 0 else 5
    
    quality_components.append(('Financial Robustness', financial_score, 0.35))
    
    # Calculate final quality score with red flag penalties
    quality_score = sum(score * weight for _, score, weight in quality_components)
    if red_flags:
        quality_score = max(0, quality_score - len(red_flags) * 0.5)
    
    # ================== ENHANCED STABILITY SCORE ==================
    # (Using similar sector adjustments as quality, keeping the structure similar to original)
    
    stability_components = []
    
    # Business Model Stability with sector context
    business_stability_score = 0
    business_factors = []
    
    # Adjust profit excellence thresholds by sector
    profit_excellence_score = 5
    gross_margin = metrics.get('Gross_Margin')
    oper_margin = metrics.get('Oper_Margin')
    profit_margin = metrics.get('Profit_Margin')
    
    if gross_margin is not None and profit_margin is not None:
        if sector == 'Technology':
            excellence_thresholds = [(55, 18), (50, 15), (40, 12), (30, 8), (20, 5)]
        elif sector in ['Consumer_Staples', 'Healthcare']:
            excellence_thresholds = [(45, 15), (40, 12), (35, 10), (25, 7), (15, 4)]
        elif sector in ['Utilities', 'Energy']:
            excellence_thresholds = [(35, 12), (30, 10), (25, 8), (20, 6), (15, 3)]
        else:
            excellence_thresholds = [(50, 15), (45, 12), (35, 10), (25, 7), (18, 4)]
        
        for i, (gm_thresh, pm_thresh) in enumerate(excellence_thresholds):
            if gross_margin >= gm_thresh and profit_margin >= pm_thresh:
                profit_excellence_score = 10 - i * 2
                break
        else:
            profit_excellence_score = 2
        
        # ROE/ROIC bonuses
        if roe is not None and roe >= config['roe_thresholds'][0]:
            profit_excellence_score = min(10, profit_excellence_score + 1)
        
        business_factors.append(('Profit_Excellence', profit_excellence_score, 0.5))
    
    # Growth consistency (similar to original but with sector context)
    growth_consistency_score = 5
    eps_yoy = metrics.get('EPS_YoY_TTM')
    sales_yoy = metrics.get('Sales_YoY_TTM')
    
    if eps_yoy is not None and sales_yoy is not None:
        if eps_yoy > 0 and sales_yoy > 0:
            base_score = 7
            
            # Sector-specific sustainable growth ranges
            if config['growth_expectations'] == 'high':
                sustainable_eps_range = (10, 40)
                sustainable_sales_range = (8, 35)
            elif config['growth_expectations'] == 'low':
                sustainable_eps_range = (3, 15)
                sustainable_sales_range = (2, 12)
            else:
                sustainable_eps_range = (5, 25)
                sustainable_sales_range = (3, 20)
            
            eps_sustainable = sustainable_eps_range[0] <= eps_yoy <= sustainable_eps_range[1]
            sales_sustainable = sustainable_sales_range[0] <= sales_yoy <= sustainable_sales_range[1]
            
            if eps_sustainable and sales_sustainable:
                growth_consistency_score = 9
            elif eps_yoy > sustainable_eps_range[1] or sales_yoy > sustainable_sales_range[1]:
                growth_consistency_score = 6  # High but potentially unsustainable
            else:
                growth_consistency_score = base_score
        elif eps_yoy > 0 or sales_yoy > 0:
            growth_consistency_score = 5
        else:
            growth_consistency_score = 2
    
    business_factors.append(('Growth_Consistency', growth_consistency_score, 0.5))
    
    if business_factors:
        business_stability_score = sum(score * weight for _, score, weight in business_factors)
    
    stability_components.append(('Business Model Stability', business_stability_score, 0.40))
    
    # Financial Strength (adapted from quality section)
    financial_strength_score = (cash_flow_score * 0.4 + financial_score * 0.6)
    stability_components.append(('Financial Strength', financial_strength_score, 0.35))
    
    # Market Position (similar to original with minor sector adjustments)
    market_position_score = 0
    market_factors = []
    
    # Volatility with sector context
    volatility_score = 5
    beta = metrics.get('Beta')
    if beta is not None:
        if sector in ['Utilities', 'Consumer_Staples']:  # Defensive sectors
            if beta < 0.6:       volatility_score = 10
            elif beta < 0.8:     volatility_score = 9
            elif beta < 1.0:     volatility_score = 8
            elif beta < 1.2:     volatility_score = 6
            else:                volatility_score = 4
        elif sector in ['Technology', 'Energy']:  # Higher volatility expected
            if beta < 0.8:       volatility_score = 9
            elif beta < 1.0:     volatility_score = 8
            elif beta < 1.3:     volatility_score = 7
            elif beta < 1.6:     volatility_score = 5
            else:                volatility_score = 3
        else:  # Moderate expectations
            if beta < 0.7:       volatility_score = 9
            elif beta < 1.0:     volatility_score = 8
            elif beta < 1.2:     volatility_score = 7
            elif beta < 1.4:     volatility_score = 5
            else:                volatility_score = 3
        
        market_factors.append(('Volatility_Risk', volatility_score, 0.4))
    
    # Institutional ownership and short interest (same as original)
    institutional_score = 5
    inst_own = metrics.get('Inst_Own')
    if inst_own is not None:
        if 70 <= inst_own <= 88:     institutional_score = 10
        elif 65 <= inst_own <= 90:   institutional_score = 9
        elif 55 <= inst_own <= 93:   institutional_score = 8
        elif 45 <= inst_own <= 96:   institutional_score = 7
        elif inst_own > 96:          institutional_score = 5
        elif inst_own < 30:          institutional_score = 4
        else:                        institutional_score = 6
        
        market_factors.append(('Institutional_Confidence', institutional_score, 0.35))
    
    # Short Interest Risk
    short_risk_score = 5
    short_float = metrics.get('Short_Float')
    if short_float is not None:
        if short_float < 2:       short_risk_score = 9
        elif short_float < 4:     short_risk_score = 8
        elif short_float < 6:     short_risk_score = 7
        elif short_float < 10:    short_risk_score = 5
        elif short_float < 15:    short_risk_score = 3
        else:                     short_risk_score = 1
        
        market_factors.append(('Short_Risk', short_risk_score, 0.25))
    
    if market_factors:
        market_position_score = sum(score * weight for _, score, weight in market_factors)
        total_weight = sum(weight for _, _, weight in market_factors)
        market_position_score = market_position_score / total_weight if total_weight > 0 else 5
    
    stability_components.append(('Market Position', market_position_score, 0.25))
    
    # Calculate weighted stability score
    stability_score = sum(score * weight for _, score, weight in stability_components)
    
    # ================== SECTOR-ADJUSTED GROWTH SCORE ==================
    growth_components = []
    
    # Recent Growth Momentum with sector expectations
    recent_growth_score = 5
    eps_yoy = metrics.get('EPS_YoY_TTM')
    sales_yoy = metrics.get('Sales_YoY_TTM')
    
    if eps_yoy is not None and sales_yoy is not None:
        avg_recent = (eps_yoy + sales_yoy) / 2
        
        # Sector-specific growth scoring
        if config['growth_expectations'] == 'high':  # Tech
            if avg_recent > 30:      recent_growth_score = 10
            elif avg_recent > 20:    recent_growth_score = 9
            elif avg_recent > 15:    recent_growth_score = 8
            elif avg_recent > 10:    recent_growth_score = 6
            elif avg_recent > 5:     recent_growth_score = 4
            elif avg_recent > 0:     recent_growth_score = 3
            else:                    recent_growth_score = 1
        elif config['growth_expectations'] == 'low':  # Utilities
            if avg_recent > 8:       recent_growth_score = 10
            elif avg_recent > 5:     recent_growth_score = 9
            elif avg_recent > 3:     recent_growth_score = 8
            elif avg_recent > 1:     recent_growth_score = 6
            elif avg_recent > 0:     recent_growth_score = 5
            elif avg_recent > -3:    recent_growth_score = 3
            else:                    recent_growth_score = 1
        else:  # Moderate growth sectors
            if avg_recent > 20:      recent_growth_score = 10
            elif avg_recent > 15:    recent_growth_score = 9
            elif avg_recent > 10:    recent_growth_score = 8
            elif avg_recent > 6:     recent_growth_score = 6
            elif avg_recent > 3:     recent_growth_score = 4
            elif avg_recent > 0:     recent_growth_score = 3
            else:                    recent_growth_score = 1
        
        # Bonus for both metrics being positive
        if eps_yoy > 0 and sales_yoy > 0:
            recent_growth_score = min(10, recent_growth_score + 1)
            
    elif eps_yoy is not None:
        # Fallback to EPS only with sector adjustments
        if config['growth_expectations'] == 'high':
            if eps_yoy > 25:         recent_growth_score = 8
            elif eps_yoy > 15:       recent_growth_score = 6
            elif eps_yoy > 8:        recent_growth_score = 4
            elif eps_yoy > 0:        recent_growth_score = 3
            else:                    recent_growth_score = 1
        elif config['growth_expectations'] == 'low':
            if eps_yoy > 10:         recent_growth_score = 8
            elif eps_yoy > 5:        recent_growth_score = 6
            elif eps_yoy > 2:        recent_growth_score = 4
            elif eps_yoy > 0:        recent_growth_score = 3
            else:                    recent_growth_score = 1
        else:
            if eps_yoy > 20:         recent_growth_score = 8
            elif eps_yoy > 12:       recent_growth_score = 6
            elif eps_yoy > 5:        recent_growth_score = 4
            elif eps_yoy > 0:        recent_growth_score = 3
            else:                    recent_growth_score = 1
    
    growth_components.append(('Recent Growth', recent_growth_score, 0.4))
    
    # Historical Growth with sector context
    historical_score = 5
    eps_5y = metrics.get('EPS_past_5Y')
    sales_5y = metrics.get('Sales_past_5Y')
    
    if eps_5y is not None and sales_5y is not None:
        avg_historical = (eps_5y + sales_5y) / 2
        
        if config['growth_expectations'] == 'high':
            if avg_historical > 25:    historical_score = 10
            elif avg_historical > 20:  historical_score = 9
            elif avg_historical > 15:  historical_score = 8
            elif avg_historical > 12:  historical_score = 6
            elif avg_historical > 8:   historical_score = 4
            else:                      historical_score = 2
        elif config['growth_expectations'] == 'low':
            if avg_historical > 8:     historical_score = 10
            elif avg_historical > 6:   historical_score = 9
            elif avg_historical > 4:   historical_score = 8
            elif avg_historical > 2:   historical_score = 6
            elif avg_historical > 0:   historical_score = 4
            else:                      historical_score = 2
        else:  # Moderate
            if avg_historical > 18:    historical_score = 10
            elif avg_historical > 15:  historical_score = 9
            elif avg_historical > 12:  historical_score = 8
            elif avg_historical > 8:   historical_score = 6
            elif avg_historical > 5:   historical_score = 4
            else:                      historical_score = 2
            
    elif eps_5y is not None:
        if config['growth_expectations'] == 'high':
            if eps_5y > 20:            historical_score = 8
            elif eps_5y > 15:          historical_score = 7
            elif eps_5y > 10:          historical_score = 5
            else:                      historical_score = 3
        elif config['growth_expectations'] == 'low':
            if eps_5y > 8:             historical_score = 8
            elif eps_5y > 5:           historical_score = 7
            elif eps_5y > 3:           historical_score = 5
            else:                      historical_score = 3
        else:
            if eps_5y > 15:            historical_score = 8
            elif eps_5y > 12:          historical_score = 7
            elif eps_5y > 8:           historical_score = 5
            else:                      historical_score = 3
    
    growth_components.append(('Historical Growth', historical_score, 0.3))
    
    # Future Growth Expectations
    future_score = 5
    eps_next_5y = metrics.get('EPS_next_5Y')
    eps_next_y = metrics.get('EPS_next_Y_growth')
    
    if eps_next_5y is not None:
        if config['growth_expectations'] == 'high':
            if eps_next_5y > 20:       future_score = 9
            elif eps_next_5y > 15:     future_score = 8
            elif eps_next_5y > 12:     future_score = 6
            elif eps_next_5y > 8:      future_score = 4
            else:                      future_score = 2
        elif config['growth_expectations'] == 'low':
            if eps_next_5y > 8:        future_score = 9
            elif eps_next_5y > 6:      future_score = 8
            elif eps_next_5y > 4:      future_score = 6
            elif eps_next_5y > 2:      future_score = 4
            else:                      future_score = 2
        else:
            if eps_next_5y > 15:       future_score = 9
            elif eps_next_5y > 12:     future_score = 8
            elif eps_next_5y > 9:      future_score = 6
            elif eps_next_5y > 6:      future_score = 4
            else:                      future_score = 2
            
    elif eps_next_y is not None:
        # Similar scaling for next year growth
        if config['growth_expectations'] == 'high':
            if eps_next_y > 25:        future_score = 8
            elif eps_next_y > 15:      future_score = 6
            elif eps_next_y > 8:       future_score = 4
            else:                      future_score = 2
        elif config['growth_expectations'] == 'low':
            if eps_next_y > 10:        future_score = 8
            elif eps_next_y > 6:       future_score = 6
            elif eps_next_y > 3:       future_score = 4
            else:                      future_score = 2
        else:
            if eps_next_y > 20:        future_score = 8
            elif eps_next_y > 12:      future_score = 6
            elif eps_next_y > 6:       future_score = 4
            else:                      future_score = 2
    
    growth_components.append(('Future Growth', future_score, 0.3))
    
    # Calculate weighted growth score
    growth_score = sum(score * weight for _, score, weight in growth_components)
    
    # ================== FINAL CALCULATIONS WITH SECTOR CONTEXT ==================
    
    # Ensure scores are within bounds
    valuation_score = min(max(0, valuation_score), 10)
    quality_score = min(max(0, quality_score), 10)
    stability_score = min(max(0, stability_score), 10)
    growth_score = min(max(0, growth_score), 10)
    
    # Sector-adjusted weighting - emphasize different aspects for different sectors
    if sector in ['Utilities', 'Consumer_Staples']:  # Value/Income focused
        # Emphasize quality and stability over growth
        total_score = (valuation_score * 0.3 + quality_score * 0.3 + 
                      stability_score * 0.3 + growth_score * 0.1)
    elif sector in ['Technology', 'Healthcare']:  # Growth focused
        # Standard balanced weighting but slight growth emphasis
        total_score = (valuation_score * 0.25 + quality_score * 0.25 + 
                      stability_score * 0.2 + growth_score * 0.3)
    elif sector == 'Energy':  # Cyclical - emphasize valuation and quality
        total_score = (valuation_score * 0.35 + quality_score * 0.3 + 
                      stability_score * 0.25 + growth_score * 0.1)
    elif sector == 'Financials':  # Special case
        # Quality is paramount for financials
        total_score = (valuation_score * 0.2 + quality_score * 0.4 + 
                      stability_score * 0.3 + growth_score * 0.1)
    else:  # Default balanced approach
        total_score = (valuation_score * 0.25 + quality_score * 0.25 + 
                      stability_score * 0.25 + growth_score * 0.25)
    
    # Cyclical adjustment for energy and materials
    if config.get('cyclical_adjustment', False):
        # Add note about cyclical nature
        warnings.append(f"Cyclical sector ({sector}) - consider economic cycle timing")
    
    return {
        'valuation_score': round(valuation_score, 2),
        'quality_score': round(quality_score, 2),
        'stability_score': round(stability_score, 2),
        'growth_score': round(growth_score, 2),
        'total_score': round(total_score, 2),
        'sector': sector,
        'sector_config_used': config,
        'valuation_components': valuation_components,
        'quality_components': quality_components,
        'stability_components': stability_components,
        'growth_components': growth_components,
        'red_flags': red_flags,
        'warnings': warnings,
        'sector_adjustments': {
            'pe_thresholds_used': config['pe_thresholds'],
            'growth_expectations': config['growth_expectations'],
            'dividend_weight': config['dividend_weight'],
            'debt_tolerance': config['debt_eq_max']
        }
    }

def create_enhanced_html(stock_data):
    """Generate comprehensive HTML report with enhanced metrics"""
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    
    # Sort stocks by total score
    sorted_data = sorted(
        [(stock, metrics, scores, sector) for stock, metrics, scores, sector in stock_data if metrics and scores],
        key=lambda x: x[2]['total_score'],
        reverse=True
    )
    
    # Read the existing HTML file
    try:
        with open(HTML_FILE, 'r', encoding='utf-8') as f:
            html_content = f.read()
    except IOError as e:
        print(f"❌ Error reading HTML file: {e}")
        return
    
    # Generate new table rows
    table_rows = []
    for stock, metrics, scores, sector in sorted_data:
        valuation_class = "positive" if scores['valuation_score'] >= 7 else "neutral" if scores['valuation_score'] >= 5 else "negative"
        stability_class = "positive" if scores['stability_score'] >= 7 else "neutral" if scores['stability_score'] >= 5 else "negative"
        growth_class = "positive" if scores['growth_score'] >= 7 else "neutral" if scores['growth_score'] >= 5 else "negative"
        total_class = "positive" if scores['total_score'] >= 7 else "neutral" if scores['total_score'] >= 5.5 else "negative"
        
        # Format growth indicators
        recent_growth = ""
        if metrics['EPS_YoY_TTM'] is not None and metrics['Sales_YoY_TTM'] is not None:
            recent_growth = f"EPS: {metrics['EPS_YoY_TTM']:+.1f}% | Sales: {metrics['Sales_YoY_TTM']:+.1f}%"
        
        # Format key metrics
        pe_display = f"{metrics['PE']:.1f}" if metrics['PE'] is not None else "N/A"
        forward_pe_display = f"{metrics['Forward_PE']:.1f}" if metrics['Forward_PE'] is not None else "N/A"
        peg_display = f"{metrics['PEG']:.2f}" if metrics['PEG'] is not None else "N/A"
        
        # Format 5Y CAGR metrics
        sales_5y_cagr = f"{metrics['Sales_past_5Y']:.1f}%" if metrics['Sales_past_5Y'] is not None else "N/A"
        eps_5y_cagr = f"{metrics['EPS_past_5Y']:.1f}%" if metrics['EPS_past_5Y'] is not None else "N/A"
        
        # Format FCF metrics
        fcf_display = f"${metrics['FCF_per_share']:.2f}" if metrics['FCF_per_share'] is not None else "N/A"
        fcf_yield_display = f"{metrics['FCF_Yield']:.1f}%" if metrics['FCF_Yield'] is not None else "N/A"
        
        # Create the main row
        table_rows.append(f'''
            <tr class="stock-row" data-sector="{sector}" data-valuation="{scores['valuation_score']:.1f}" data-stability="{scores['stability_score']:.1f}" data-growth="{scores['growth_score']:.1f}" onclick="toggleDetails('{stock}')">
                <td><strong>{stock}</strong><br><small>${metrics['Price']:.2f}</small><br><small style="color: #666;">{sector}</small></td>
                <td>{pe_display}<br><small>Fwd: {forward_pe_display}</small></td>
                <td>{peg_display}</td>
                <td>{f"{metrics['Debt/Eq']:.2f}" if metrics['Debt/Eq'] is not None else "N/A"}<br>
                    <small>{f"{metrics['Current_Ratio']:.1f}" if metrics['Current_Ratio'] is not None else "N/A"}</small></td>
                <td class="hidden-mobile">{f"{metrics['ROE']:.1f}%" if metrics['ROE'] is not None else "N/A"}<br>
                    <small>{f"{metrics['Profit_Margin']:.1f}%" if metrics['Profit_Margin'] is not None else "N/A"}</small></td>
                <td class="hidden-mobile">{fcf_display}<br><small>{fcf_yield_display}</small></td>
                <td class="hidden-mobile">{sales_5y_cagr}</td>
                <td class="hidden-mobile">{eps_5y_cagr}</td>
                <td class="hidden-mobile">{recent_growth if recent_growth else "N/A"}</td>
                <td class="{valuation_class}">{scores['valuation_score']:.1f}</td>
                <td class="{stability_class}">{scores['stability_score']:.1f}</td>
                <td class="{growth_class}">{scores['growth_score']:.1f}</td>
                <td class="{total_class}"><strong>{scores['total_score']:.1f}</strong></td>
            </tr>
        ''')
        
        # Create the details row
        table_rows.append(f'''
            <tr id="details-{stock}" class="details-row" style="display: none;">
                <td colspan="13">
                    <div class="details-content">
                        <div class="metric-grid">
                            <div class="metric-section">
                                <h4>📊 Valuation Details</h4>
                                <p>P/S: {f"{metrics['P/S']:.2f}" if metrics['P/S'] else "N/A"} | 
                                   P/B: {f"{metrics['P/B']:.2f}" if metrics['P/B'] else "N/A"} | 
                                   EV/EBITDA: {f"{metrics['EV/EBITDA']:.1f}" if metrics['EV/EBITDA'] else "N/A"}</p>
                                <p>P/FCF: {f"{metrics['P/FCF']:.1f}" if metrics['P/FCF'] else "N/A"} | 
                                   EV/Sales: {f"{metrics['EV/Sales']:.2f}" if metrics['EV/Sales'] else "N/A"}</p>
                            </div>
                            <div class="metric-section">
                                <h4>💪 Quality Metrics</h4>
                                <p>ROA: {f"{metrics['ROA']:.1f}%" if metrics['ROA'] else "N/A"} | 
                                   ROIC: {f"{metrics['ROIC']:.1f}%" if metrics['ROIC'] else "N/A"} | 
                                   Gross Margin: {f"{metrics['Gross_Margin']:.1f}%" if metrics['Gross_Margin'] else "N/A"}</p>
                                <p>Quick Ratio: {f"{metrics['Quick_Ratio']:.2f}" if metrics['Quick_Ratio'] else "N/A"} | 
                                   Cash/sh: ${f"{metrics['Cash_per_sh']:.2f}" if metrics['Cash_per_sh'] else "N/A"}</p>
                            </div>
                            <div class="metric-section">
                                <h4>💰 Free Cash Flow Analysis</h4>
                                <p>FCF per Share: {fcf_display} | FCF Yield: {fcf_yield_display}</p>
                                <p>P/FCF: {f"{metrics['P/FCF']:.1f}" if metrics['P/FCF'] else "N/A"} | 
                                   Total FCF: {f"${metrics['Total_FCF']:.2f}B" if metrics['Total_FCF'] is not None else "N/A"}</p>
                                <p><small>💡 FCF shows actual cash generation ability - crucial for dividends and growth funding</small></p>
                            </div>
                            <div class="metric-section">
                                <h4>📈 Growth Trends</h4>
                                <p>5Y Sales CAGR: {sales_5y_cagr} | 5Y EPS CAGR: {eps_5y_cagr}</p>
                                <p>EPS Growth: TTM {f"{metrics['EPS_YoY_TTM']:+.1f}%" if metrics['EPS_YoY_TTM'] else "N/A"} | 
                                   Q/Q {f"{metrics['EPS_QoQ']:+.1f}%" if metrics['EPS_QoQ'] else "N/A"}</p>
                                <p>Sales Growth: TTM {f"{metrics['Sales_YoY_TTM']:+.1f}%" if metrics['Sales_YoY_TTM'] else "N/A"} | 
                                   Q/Q {f"{metrics['Sales_QoQ']:+.1f}%" if metrics['Sales_QoQ'] else "N/A"}</p>
                            </div>
                            <div class="metric-section">
                                <h4>🎯 Market Position</h4>
                                <p>Beta: {f"{metrics['Beta']:.2f}" if metrics['Beta'] else "N/A"} | 
                                   RSI: {f"{metrics['RSI']:.1f}" if metrics['RSI'] else "N/A"} | 
                                   Short Float: {f"{metrics['Short_Float']:.1f}%" if metrics['Short_Float'] else "N/A"}</p>
                                <p>Insider Own: {f"{metrics['Insider_Own']:.1f}%" if metrics['Insider_Own'] else "N/A"} | 
                                   Inst Own: {f"{metrics['Inst_Own']:.1f}%" if metrics['Inst_Own'] else "N/A"}</p>
                            </div>
                            <div class="metric-section">
                                <h4>🏢 Sector Analysis</h4>
                                <p>Sector: <strong>{sector}</strong></p>
                                <p>Growth Expectations: {scores['sector_adjustments']['growth_expectations'].capitalize()}</p>
                                <p>P/E Thresholds: {scores['sector_adjustments']['pe_thresholds_used']}</p>
                                <p>Debt Tolerance: {scores['sector_adjustments']['debt_tolerance']}</p>
                                <p>Dividend Weight: {scores['sector_adjustments']['dividend_weight']*100:.1f}%</p>
                            </div>
                        </div>
                    </div>
                </td>
            </tr>
        ''')
    
    # Add stocks with missing data
    missing_data = [(stock, metrics, scores, sector) for stock, metrics, scores, sector in stock_data if not metrics or not scores]
    for stock, metrics, scores, sector in missing_data:
        table_rows.append(f'''
            <tr>
                <td><strong>{stock}</strong></td>
                <td colspan="12" class="error">Data not available (may be rate limited)</td>
            </tr>
        ''')
    
    # Find and replace the table body content
    import re
    # Find the table body in the HTML
    pattern = r'<tbody id="stockTableBody">(.*?)</tbody>'
    replacement = f'<tbody id="stockTableBody">{"".join(table_rows)}</tbody>'
    
    # Replace the table body
    html_content = re.sub(pattern, replacement, html_content, flags=re.DOTALL)
    
    # Update the timestamp
    timestamp_pattern = r'<div class="timestamp".*?>⏰ Last updated:.*?</div>'
    timestamp_replacement = f'<div class="timestamp" style="color: #ffffff; background: rgba(255, 255, 255, 0.15); padding: 10px 15px; border-radius: 8px; text-align: right; margin-top: 20px; backdrop-filter: blur(5px);">⏰ Last updated: {timestamp}</div>'
    html_content = re.sub(timestamp_pattern, timestamp_replacement, html_content, flags=re.DOTALL)
    
    # Write the updated HTML back to the file
    try:
        with open(HTML_FILE, 'w', encoding='utf-8') as f:
            f.write(html_content)
        print(f"✅ Successfully updated {HTML_FILE}")
        print(f"📊 Open {HTML_FILE} in your browser to view the enhanced sector-specific report")
    except IOError as e:
        print(f"❌ Error writing HTML file: {e}")

def main():
    print("🔍 Starting enhanced comprehensive stock analysis with sector-specific scoring...")
    print("📈 Fetching detailed metrics from Finviz...")
    
    stock_data = []
    
    for i, stock in enumerate(STOCKS):
        print(f"\n📊 Analyzing {stock} ({i+1}/{len(STOCKS)})...")
        metrics, sector = fetch_comprehensive_metrics(stock)
        
        if metrics:
            print(f"✅ Data fetched successfully")
            print(f"🏢 Sector: {sector if sector else 'Unknown'}")
            # Show key metrics including FCF
            print(f"   💰 Valuation: P/E {metrics['PE']}, PEG {metrics['PEG']}, Forward P/E {metrics['Forward_PE']}")
            print(f"   💪 Quality: ROE {metrics['ROE']}%, Debt/Eq {metrics['Debt/Eq']}, Profit Margin {metrics['Profit_Margin']}%")
            if metrics['FCF_per_share'] is not None and metrics['FCF_Yield'] is not None:
                print(f"   💰 FCF: ${metrics['FCF_per_share']:.2f}/share, Yield {metrics['FCF_Yield']:.1f}%, P/FCF {metrics['P/FCF']}")
            print(f"   📈 Growth: EPS TTM {metrics['EPS_YoY_TTM']}%, Sales TTM {metrics['Sales_YoY_TTM']}%")
            print(f"   📊 5Y CAGR: Sales {metrics['Sales_past_5Y']}%, EPS {metrics['EPS_past_5Y']}%")
            
            scores = calculate_enhanced_scores_with_sectors(metrics, sector)
            if scores:
                print(f"   🎯 Scores: Val {scores['valuation_score']:.1f} | Stab {scores['stability_score']:.1f} | Growth {scores['growth_score']:.1f} | Total {scores['total_score']:.1f}")
        else:
            print(f"❌ Failed to fetch data for {stock}")
            scores = None
        
        stock_data.append((stock, metrics, scores, sector))
        
        # Delay between requests
        if i < len(STOCKS) - 1:
            delay = DELAY_BETWEEN_REQUESTS + random.uniform(0, 2)
            print(f"⏳ Waiting {delay:.1f}s...")
            time.sleep(delay)
    
    print("\n📄 Generating enhanced HTML report with sector-specific scoring...")
    create_enhanced_html(stock_data)
    print("\n🎉 Enhanced sector-specific analysis completed!")
    print("💡 The report now includes sector-specific scoring!")
    print("🏢 Each stock is evaluated using thresholds appropriate for its sector!")

if __name__ == '__main__':
    main()
