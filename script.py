import requests
import random
import time
from datetime import datetime
import os
from bs4 import BeautifulSoup
import historical_fundamental_scores

# Configuration
STOCKS = ['AWI', 'AAPL', 'ABBV', 'ABNB', 'ABT', 'ACAD', 'ADBE', 'ADP', 'ADSK', 'AMAT', 'AMD', 'AME', 'AMT', 'AMZN', 'ANET', 'APH', 'APP', 'APPF', 'APD', 'ASML', 'ATEN', 'AVGO', 'AXON', 'AXP', 'AZO', 'BABA', 'BMRN', 'BKNG', 'BLK', 'BMI', 'BRO', 'BR', 'BRK-B', 'BSX', 'CARG', 'CAT', 'CB', 'CDNS', 'CELH', 'CINF', 'CHD', 'CHKP', 'CHTR', 'CMCSA', 'CME', 'CMG', 'CMI', 'COF', 'COP', 'COST', 'CPNG', 'CPRT', 'CPRX', 'CRM', 'CSGP', 'CTAS', 'CTSH', 'DAL', 'DASH', 'DDOG', 'DECK', 'DHR', 'DIS', 'DLR', 'DOCS', 'DOCU', 'DPZ', 'DT', 'DUOL', 'DXCM', 'EA', 'ECL', 'ELF', 'EMR', 'ENB', 'ENPH', 'EPAM', 'ETN', 'ETSY', 'EW', 'EXEL', 'EXLS', 'EXR', 'FAST', 'FICO', 'FIS', 'FITB', 'FSLR', 'FTNT', 'GATX', 'GD', 'GGG', 'GDDY', 'GILD', 'GOOGL', 'GS', 'GWW', 'HALO', 'HD', 'HEI', 'HIMS', 'HLT', 'HOLX', 'HON', 'HOOD', 'ICE', 'IDXX', 'IEX', 'ILMN', 'INTU', 'IR', 'ISRG', 'ITW', 'JNJ', 'JKHY', 'JPM', 'KEYS', 'KLAC', 'KMI', 'KO', 'LHX', 'LIN', 'LMAT', 'LMT', 'LOW', 'LRCX', 'LRN', 'LULU', 'MA', 'MANH', 'MAR', 'MCD', 'MCO', 'MDT', 'MEDP', 'MELI', 'META', 'MKC', 'MLI', 'MLM', 'MNST', 'MPWR', 'MS', 'MSFT', 'MSI', 'MTB', 'MKTX', 'NFLX', 'NDAQ', 'NKE', 'NOC', 'NOW', 'NSSC', 'NVDA', 'NVMI', 'O', 'ODD', 'OKTA', 'ON', 'ONTO', 'ORCL', 'ORLY', 'PANW', 'PAYC', 'PAYX', 'PCTY', 'PEP', 'PGR', 'PH', 'PINS', 'PODD', 'POOL', 'PSA', 'PTC', 'PWR', 'PYPL', 'QFIN', 'QLYS', 'QCOM', 'QSR', 'REGN', 'RMD', 'ROL', 'ROP', 'ROK', 'ROST', 'RSG', 'RTX', 'SBAC', 'SBUX', 'SCHW', 'SE', 'SHOP', 'SHW', 'SLB', 'SMCI', 'SNPS', 'SOFI', 'SAP', 'SPGI', 'SQ', 'SYK', 'TDG', 'TDY', 'TMO', 'TJX', 'TRI', 'TRMB', 'TSLA', 'TSM', 'TT', 'TXN', 'TYL', 'UL', 'ULTA', 'UNP', 'UPS', 'USLM', 'V', 'VEEV', 'VICI', 'VMC', 'VRSK', 'VRSN', 'WDAY', 'WM', 'WMT', 'WPM', 'WST', 'WRB', 'XOM', 'XYL', 'YOU', 'ZTS', 'ZM']

def calculate_roic_growth_score(metrics):
    """Calculate ROIC growth score - MOST important growth metric per research"""
    roic = metrics.get('ROIC')
    roe = metrics.get('ROE')
    
    # We don't have historical ROIC, so we'll infer from quality
    # This is a limitation - ideally need 5-year ROIC trend
    if roic is not None and roic > 0:
        # High absolute ROIC suggests it grew to get there
        if roic >= 25:      return 10
        elif roic >= 20:    return 9
        elif roic >= 15:    return 8
        elif roic >= 12:    return 7
        elif roic >= 10:    return 6
        else:               return 4
    elif roe is not None:
        # Fallback to ROE if no ROIC
        if roe >= 25:       return 8
        elif roe >= 20:     return 7
        elif roe >= 15:     return 6
        else:               return 4
    return 5

def calculate_fcf_growth_score(metrics):
    """Calculate FCF growth score"""
    fcf_per_share = metrics.get('FCF_per_share')
    eps_ttm = metrics.get('EPS_TTM')
    sales_5y = metrics.get('Sales_past_5Y')
    
    if fcf_per_share and eps_ttm and eps_ttm > 0:
        fcf_conversion = fcf_per_share / eps_ttm
        
        # High FCF conversion + revenue growth = FCF growing
        if fcf_conversion > 1.2 and sales_5y and sales_5y > 10:
            return 10
        elif fcf_conversion > 1.0 and sales_5y and sales_5y > 5:
            return 8
        elif fcf_conversion > 0.9:
            return 7
        elif fcf_conversion > 0.7:
            return 5
        else:
            return 3
    
    return 5

def calculate_roe_growth_score(metrics):
    """Calculate ROE growth/trend score"""
    roe = metrics.get('ROE')
    eps_5y = metrics.get('EPS_past_5Y')
    
    if roe and eps_5y:
        # High ROE + growing EPS = ROE likely growing
        if roe > 20 and eps_5y > 15:    return 10
        elif roe > 15 and eps_5y > 10:  return 8
        elif roe > 12 and eps_5y > 5:   return 6
        else:                           return 5
    elif roe:
        if roe > 20:    return 7
        elif roe > 15:  return 6
        else:           return 5
    
    return 5

USER_AGENTS = [
    'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36',
    'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36',
    'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:89.0) Gecko/20100101 Firefox/89.0',
    'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/14.1.15 Safari/605.1.15'
]
DELAY_BETWEEN_REQUESTS = 5  # seconds
HTML_FILE = os.path.join(os.getcwd(), 'enhanced_stock_analysis.html')
HTML_TEMPLATE_FILE = os.path.join(os.getcwd(), 'enhanced_stock_analysis.html')
MAX_RETRIES = 3

def calculate_revenue_growth_score(metrics, config):
    """Calculate comprehensive revenue growth score"""
    revenue_score = 5
    
    # Prioritize 5Y revenue CAGR (most predictive)
    sales_5y = metrics.get('Sales_past_5Y')
    sales_yoy = metrics.get('Sales_YoY_TTM')  # ✅ MOVE THIS UP
    
    if sales_5y is not None:
        if config['growth_expectations'] == 'high':
            thresholds = [25, 20, 15, 10, 7]
        elif config['growth_expectations'] == 'low':
            thresholds = [8, 6, 4, 3, 2]
        else:
            thresholds = [18, 15, 12, 8, 5]
        
        for i, threshold in enumerate(thresholds):
            if sales_5y >= threshold:
                revenue_score = 10 - i * 2
                break
        else:
            revenue_score = 2

    # ✅ NOW this will work - sales_yoy is defined
    if sales_5y and sales_yoy:
        growth_volatility = abs(sales_yoy - sales_5y) / sales_5y
        if growth_volatility > 0.5:  # More than 50% deviation
            revenue_score -= 2  # Penalize erratic growth
    
    # Quality adjustment - consistent growth is better
    if sales_5y and sales_yoy and sales_yoy > 0 and sales_5y > 0:
        consistency_ratio = min(sales_yoy / sales_5y, sales_5y / sales_yoy) 
        if consistency_ratio > 0.7:  # Consistent growth pattern
            revenue_score = min(10, revenue_score + 1)
    
    return revenue_score

def get_historical_score(stock_symbol):
    """Get historical fundamental score for a stock"""
    try:
        score_str = historical_fundamental_scores.STOCK_SCORES.get(stock_symbol)
        print(f"Debug: {stock_symbol} -> {score_str}")  # Add this debug line
        if score_str:
            return float(score_str)
        else:
            print(f"Debug: No historical score found for {stock_symbol}")
            return None
    except (ValueError, AttributeError) as e:
        print(f"Debug: Error getting historical score for {stock_symbol}: {e}")
        return None

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

# This is the COMPLETE replacement for calculate_enhanced_scores_with_sectors function
# Copy this entire function to replace your existing one (starts around line 394)

# First, add these at module level (after your existing HISTORICAL_WEIGHTS):

SECTOR_ROIC_BENCHMARKS = {
    'Technology': {
        'median': 18,
        'top_quartile': 35,
        'bottom_quartile': 4,
    },
    'Healthcare': {
        'median': 16,
        'top_quartile': 28,
        'bottom_quartile': 6,
    },
    'Consumer Defensive': {
        'median': 15,
        'top_quartile': 22,
        'bottom_quartile': 8,
    },
    'Utilities': {
        'median': 7,
        'top_quartile': 9,
        'bottom_quartile': 5,
    },
    'Communication Services': {
        'median': 18,
        'top_quartile': 42,
        'bottom_quartile': 11,
    },
    'Basic Materials': {
        'median': 8,
        'top_quartile': 14,
        'bottom_quartile': 3,
    },
    'Financial': {
        'median': 12,
        'top_quartile': 18,
        'bottom_quartile': 7,
    },
    'Industrials': {
        'median': 12,
        'top_quartile': 19,
        'bottom_quartile': 6,
    },
    'Energy': {
        'median': 9,
        'top_quartile': 15,
        'bottom_quartile': 4,
    },
    'Real Estate': {
        'median': 8,
        'top_quartile': 12,
        'bottom_quartile': 5,
    },
    'Consumer Cyclical': {
        'median': 12,
        'top_quartile': 19,
        'bottom_quartile': 6,
    },
}

def get_research_validated_weights(sector):
    """
    Research-validated weights based on:
    - Chart 3: S&P 500 gains decomposition (1987-2005) - 10yr data
    - Chart 2: Metric correlations peak at 8yr mark
    - Chart 1: Revenue > Profit growth for share price gains
    - McKinsey: ROIC persistence across decades
    - Academic: Starting valuation affects terminal multiple
    """
    
    SECTOR_MULTIPLIERS = {
        'Technology': {
            'growth_mult': 1.10,      # Chart 1: Growth matters but not dominant
            'quality_mult': 1.15,     # ROIC moats critical for durability
            'valuation_mult': 0.75,   # Can sustain higher multiples
        },
        'Communication Services': {
            'growth_mult': 1.10,
            'quality_mult': 1.10,
            'valuation_mult': 0.80,
        },
        'Healthcare': {
            'growth_mult': 1.00,
            'quality_mult': 1.25,     # Regulatory moats = ROIC persistence
            'valuation_mult': 0.85,
        },
        'Consumer Defensive': {
            'growth_mult': 0.75,
            'quality_mult': 1.35,     # Brand moats = stable ROIC
            'valuation_mult': 1.10,   # Value-sensitive sector
        },
        'Consumer Cyclical': {
            'growth_mult': 1.05,
            'quality_mult': 1.00,
            'valuation_mult': 1.05,   # Cyclical = valuation timing matters
        },
        'Utilities': {
            'growth_mult': 0.60,
            'quality_mult': 1.40,     # Regulated = ROIC stability
            'valuation_mult': 1.20,   # Yield-focused = valuation critical
        },
        'Energy': {
            'growth_mult': 0.80,
            'quality_mult': 1.15,
            'valuation_mult': 1.15,   # Commodity = buy cheap
        },
        'Industrials': {
            'growth_mult': 1.00,
            'quality_mult': 1.10,
            'valuation_mult': 1.00,
        },
        'Basic Materials': {
            'growth_mult': 0.85,
            'quality_mult': 1.10,
            'valuation_mult': 1.15,   # Commodity = valuation timing
        },
        'Financial': {
            'growth_mult': 0.90,
            'quality_mult': 1.20,     # ROE persistence key
            'valuation_mult': 1.05,
        },
        'Real Estate': {
            'growth_mult': 0.75,
            'quality_mult': 1.30,     # Cash flow stability
            'valuation_mult': 1.15,   # Yield = valuation sensitive
        },
    }
    
    # Chart 3 decomposition at 10yr mark:
    # Revenue ~10% + Margin ~3% + Multiple ~5% + Other ~2% = ~20% total
    # This means: Growth ~50%, Multiple expansion ~25%, Quality ~25%
    # 
    # Chart 2 shows at 8yr: Cash Flow (0.50) ≥ Revenue (0.43)
    # Conclusion: Quality (cash/ROIC) should equal Growth at long horizons
    
    # Research-backed base weights from Document 1
    BASE_WEIGHTS = {
        'quality': 0.50,      # Primary driver per Damodaran
        'growth': 0.20,       # Secondary (only matters with ROIC > WACC)
        'valuation': 0.15,    # Mean-reverting, temporary
        'historical': 0.15    # Validation layer
    }
    
    mult = SECTOR_MULTIPLIERS.get(sector, {
        'growth_mult': 1.0,
        'quality_mult': 1.0,
        'valuation_mult': 1.0
    })
    
    adj_growth = BASE_WEIGHTS['growth'] * mult['growth_mult']
    adj_quality = BASE_WEIGHTS['quality'] * mult['quality_mult']
    adj_valuation = BASE_WEIGHTS['valuation'] * mult['valuation_mult']
    
    total = adj_growth + adj_quality + adj_valuation
    
    return {
        'growth': adj_growth / total,
        'quality': adj_quality / total,
        'valuation': adj_valuation / total,
        'historical': BASE_WEIGHTS['historical'],  # Add this
        'multipliers_used': mult
    }

def calculate_enhanced_scores_with_sectors(metrics, sector=None, stock_symbol=None):
    """
    Research-validated scoring aligned with:
    - Wharton "Return Dominance" (2023): 75% of 10yr returns from growth
    - McKinsey ROIC persistence study
    - Empirical charts showing revenue > profit growth importance
    """
    if not metrics:
        return None
    
    historical_score_ = get_historical_score(stock_symbol) if stock_symbol else None

    # Keep existing SECTOR_CONFIGS structure
    SECTOR_CONFIGS = {
        'Technology': {
            'pe_thresholds': [25, 35, 50, 70],
            'roe_thresholds': [20, 15, 12, 8],
            'roic_thresholds': [25, 20, 15, 10],
            'debt_eq_max': 0.4,
            'growth_expectations': 'high',
            'margin_focus': 'gross',
            'fcf_yield_min': 2.0,
            'dividend_weight': 0.1,
        },
        'Communication Services': {
            'pe_thresholds': [25, 35, 50, 70],
            'roe_thresholds': [18, 14, 10, 6],
            'roic_thresholds': [20, 15, 12, 8],
            'debt_eq_max': 0.8,
            'growth_expectations': 'high',
            'margin_focus': 'operating',
            'fcf_yield_min': 3.0,
            'dividend_weight': 0.15,
        },
        'Healthcare': {
            'pe_thresholds': [22, 30, 45, 65],
            'roe_thresholds': [18, 15, 12, 8],
            'roic_thresholds': [20, 16, 12, 8],
            'debt_eq_max': 0.6,
            'growth_expectations': 'moderate',
            'margin_focus': 'gross',
            'fcf_yield_min': 3.5,
            'dividend_weight': 0.2,
        },
        'Consumer Defensive': {
            'pe_thresholds': [18, 24, 30, 40],
            'roe_thresholds': [18, 15, 12, 8],
            'roic_thresholds': [20, 15, 12, 8],
            'debt_eq_max': 0.8,
            'growth_expectations': 'low',
            'margin_focus': 'operating',
            'fcf_yield_min': 4.5,
            'dividend_weight': 0.3,
        },
        'Consumer Cyclical': {
            'pe_thresholds': [20, 28, 38, 55],
            'roe_thresholds': [16, 12, 9, 6],
            'roic_thresholds': [18, 14, 10, 7],
            'debt_eq_max': 1.0,
            'growth_expectations': 'moderate',
            'margin_focus': 'operating',
            'fcf_yield_min': 4.0,
            'dividend_weight': 0.2,
            'cyclical_adjustment': True,
        },
        'Utilities': {
            'pe_thresholds': [16, 20, 26, 32],
            'roe_thresholds': [12, 10, 8, 6],
            'roic_thresholds': [8, 7, 6, 4],
            'debt_eq_max': 1.8,
            'growth_expectations': 'low',
            'margin_focus': 'operating',
            'fcf_yield_min': 6.5,
            'dividend_weight': 0.4,
        },
        'Energy': {
            'pe_thresholds': [12, 18, 28, 40],
            'roe_thresholds': [15, 12, 8, 5],
            'roic_thresholds': [12, 10, 8, 5],
            'debt_eq_max': 1.2,
            'growth_expectations': 'cyclical',
            'margin_focus': 'operating',
            'fcf_yield_min': 8.0,
            'dividend_weight': 0.35,
            'cyclical_adjustment': True,
        },
        'Industrials': {
            'pe_thresholds': [18, 24, 32, 45],
            'roe_thresholds': [15, 12, 10, 7],
            'roic_thresholds': [15, 12, 10, 7],
            'debt_eq_max': 0.9,
            'growth_expectations': 'moderate',
            'margin_focus': 'operating',
            'fcf_yield_min': 4.5,
            'dividend_weight': 0.25,
        },
        'Basic Materials': {
            'pe_thresholds': [12, 16, 24, 35],
            'roe_thresholds': [14, 11, 8, 5],
            'roic_thresholds': [12, 10, 8, 5],
            'debt_eq_max': 1.1,
            'growth_expectations': 'cyclical',
            'margin_focus': 'operating',
            'fcf_yield_min': 7.0,
            'dividend_weight': 0.3,
            'cyclical_adjustment': True,
        },
        'Financial': {
            'pe_thresholds': [10, 13, 18, 25],
            'roe_thresholds': [15, 12, 10, 8],
            'roic_thresholds': [12, 10, 8, 6],
            'debt_eq_max': 8.0,
            'growth_expectations': 'moderate',
            'margin_focus': 'net_interest',
            'fcf_yield_min': 4.0,
            'dividend_weight': 0.3,
            'use_financial_metrics': True,
        },
        'Real Estate': {
            'pe_thresholds': [15, 20, 28, 40],
            'roe_thresholds': [12, 10, 8, 6],
            'roic_thresholds': [8, 7, 6, 4],
            'debt_eq_max': 2.0,
            'growth_expectations': 'low',
            'margin_focus': 'operating',
            'fcf_yield_min': 6.0,
            'dividend_weight': 0.45,
        }
    }
    
    DEFAULT_CONFIG = SECTOR_CONFIGS['Technology']
    config = SECTOR_CONFIGS.get(sector, DEFAULT_CONFIG) if sector else DEFAULT_CONFIG
    sector = sector or 'Unknown'
    
    red_flags = []
    warnings = []
    
    # ================== VALUATION SCORING (keep structure, already good) ==================
    valuation_score = 0
    valuation_components = []

    pe = metrics.get('PE')
    forward_pe = metrics.get('Forward_PE')
    target_pe = forward_pe if forward_pe is not None else pe

    peg_score = 5
    if metrics['PEG'] is not None and target_pe is not None:
        peg = metrics['PEG']
        actual_growth = metrics.get('EPS_next_5Y') or metrics.get('EPS_past_5Y') or metrics.get('EPS_YoY_TTM')
        
        # Get quality metrics for context
        roic = metrics.get('ROIC')
        roe = metrics.get('ROE')
        profit_margin = metrics.get('Profit_Margin')
        
        # Determine if this is an elite business
        is_elite = False
        if roic and roic >= 25:
            is_elite = True
        elif roe and roe >= 30:
            is_elite = True
        elif profit_margin and profit_margin >= 25:
            is_elite = True
        
        # Adjust PEG thresholds based on quality
        if is_elite:
            # Elite businesses can sustain higher multiples
            if peg <= 0:
                peg_score = 1
                red_flags.append("Invalid PEG ratio (negative/zero growth)")
            elif peg < 1.0:
                peg_score = 10  # Bargain for elite business
            elif 1.0 <= peg < 2.0:
                peg_score = 9   # Great value
            elif 2.0 <= peg < 3.0:
                peg_score = 7   # Fair value (NOT overvalued!)
            elif 3.0 <= peg < 4.0:
                peg_score = 5   # Slightly expensive but acceptable
            elif 4.0 <= peg < 5.0:
                peg_score = 3
                warnings.append(f"High PEG for elite business: {peg:.2f}")
            else:
                peg_score = 2
                warnings.append(f"Very high PEG even for elite business: {peg:.2f}")
        else:
            # Standard PEG thresholds for average businesses
            if peg <= 0:
                peg_score = 1
                red_flags.append("Invalid PEG ratio (negative/zero growth)")
            elif peg < 0.5:
                if actual_growth and actual_growth > 25:
                    peg_score = 8
                else:
                    peg_score = 6
                    warnings.append(f"Very low PEG ({peg:.2f}) - verify growth sustainability")
            elif 0.5 <= peg < 1.0:
                peg_score = 10  # Bargain
            elif 1.0 <= peg <= 1.5:
                peg_score = 8   # Good value
            elif 1.5 < peg <= 2.0:
                peg_score = 6   # Fair
            elif 2.0 < peg <= 3.0:
                peg_score = 3   # Expensive
                warnings.append(f"High PEG ({peg:.2f}) suggests overvaluation")
            else:
                peg_score = 1   # Very expensive
                red_flags.append(f"Very high PEG ({peg:.2f}) indicates significant overvaluation")

    pe_score = 5
    if metrics['PE'] is not None:
        peg = metrics.get('PEG')
        pe_good, pe_fair, pe_poor, pe_terrible = config['pe_thresholds']
        
        if target_pe < pe_good:
            base_pe_score = 8
        elif target_pe < pe_fair:
            base_pe_score = 6
        elif target_pe < pe_poor:
            base_pe_score = 4
        elif target_pe < pe_terrible:
            base_pe_score = 2
        else:
            base_pe_score = 1
        
        pe_score = base_pe_score
        
        if peg is not None:
            if target_pe < pe_good and peg > 2.0:
                pe_score = max(1, base_pe_score - 2)
                warnings.append(f"Low P/E ({target_pe:.1f}) but high PEG ({peg:.2f}) suggests low growth")
            elif target_pe > pe_fair and peg < 1.5:
                pe_score = min(8, base_pe_score + 2)
            elif target_pe > pe_terrible and peg > 2.0:
                pe_score = 1
                red_flags.append(f"High P/E ({target_pe:.1f}) with high PEG ({peg:.2f}) indicates overvaluation")
        
        if forward_pe and pe and forward_pe < pe * 0.9:
            pe_score = min(10, pe_score + 1)

    ps_score = 5
    if metrics['P/S'] is not None:
        ps = metrics['P/S']
        profit_margin = metrics.get('Profit_Margin', 10) or 10
        
        if sector == 'Technology':
            if profit_margin > 20:
                thresholds = [8, 15, 25, 40]
            else:
                thresholds = [4, 8, 15, 25]
        elif sector in ['Utilities', 'Energy']:
            thresholds = [1.5, 3, 5, 8]
        else:
            if profit_margin > 15:
                thresholds = [4, 8, 15, 25]
            else:
                thresholds = [2, 4, 8, 15]
        
        if ps < thresholds[0]:      ps_score = 9
        elif ps < thresholds[1]:    ps_score = 7
        elif ps < thresholds[2]:    ps_score = 5
        elif ps < thresholds[3]:    ps_score = 3
        else:                       ps_score = 1

    if config['dividend_weight'] > 0.25:
        valuation_components.append(('PEG', peg_score, 0.40))
        valuation_components.append(('P/E_with_Growth_Context', pe_score, 0.30))
        if metrics['P/S'] is not None:
            valuation_components.append(('P/S', ps_score, 0.30))
        else:
            valuation_components = [
                ('PEG', peg_score, 0.57),
                ('P/E_with_Growth_Context', pe_score, 0.43)
            ]
    else:
        valuation_components.append(('PEG', peg_score, 0.60))
        valuation_components.append(('P/E_with_Growth_Context', pe_score, 0.25))
        if metrics['P/S'] is not None:
            valuation_components.append(('P/S', ps_score, 0.15))
        else:
            valuation_components = [
                ('PEG', peg_score, 0.71),
                ('P/E_with_Growth_Context', pe_score, 0.29)
            ]

    if valuation_components:
        valuation_score = sum(score * weight for _, score, weight in valuation_components)
        total_weight = sum(weight for _, _, weight in valuation_components)
        if total_weight > 0:
            valuation_score = valuation_score / total_weight
    # ================== QUALITY SCORE - RESEARCH ALIGNED ==================
    # Research Document 1 Breakdown:
    # - ROIC Absolute: 50% of quality (25% of total score)
    # - ROIC Stability: 25% of quality (12.5% of total score)
    # - FCF Positivity: 10% of quality (5% of total score)
    # - Debt/Equity: 10% of quality (5% of total score)
    # - ROE: 5% of quality (2.5% of total score)

    quality_components = []

    # ========== 1. ROIC ABSOLUTE (50% of quality = 25% of total) ==========
    # "The key number in valuation is return on capital" - Damodaran
    # This is THE most important quality indicator

    roic_absolute_score = 5
    roe = metrics.get('ROE')
    roic = metrics.get('ROIC')
    roa = metrics.get('ROA')

    # Get sector context
    sector_benchmarks = SECTOR_ROIC_BENCHMARKS.get(
        sector,
        {'top_quartile': 20, 'median': 12, 'bottom_quartile': 6}
    )

    if roic is not None:
        # Absolute ROIC scoring (what matters most)
        if roic >= 50:
            # Super-elite (SPGI, V, MA level)
            base_roic = 10
        elif roic >= 40:
            # Elite capital allocators (top 1%)
            base_roic = 9.8
        elif roic >= 35:
            # Exceptional (GOOGL level)
            base_roic = 9.5
        elif roic >= 30:
            # Outstanding (MSFT level)
            base_roic = 9.2
        elif roic >= 25:
            # Excellent competitive advantage
            base_roic = 8.8
        elif roic >= 22:
            # Very strong moat
            base_roic = 8.3
        elif roic >= 20:
            # Strong moat
            base_roic = 8.0
        elif roic >= 18:
            # Good moat
            base_roic = 7.5
        elif roic >= 15:
            # Above average business
            base_roic = 7.0
        elif roic >= 12:
            # Average business
            base_roic = 6.0
        elif roic >= 10:
            # Below average
            base_roic = 5.0
        elif roic >= 8:
            # Weak returns
            base_roic = 4.0
        elif roic >= 6:
            # Poor returns
            base_roic = 3.0
        else:
            # Value destructive
            base_roic = 2.0
        
        # Sector-relative bonus (beating industry significantly)
        sector_median = sector_benchmarks['median']
        sector_top = sector_benchmarks['top_quartile']
        
        if sector_median > 0:
            if roic >= sector_median * 3.0:
                # Crushing the industry
                base_roic = min(10, base_roic + 0.8)
            elif roic >= sector_median * 2.5:
                # Dominating
                base_roic = min(10, base_roic + 0.6)
            elif roic >= sector_median * 2.0:
                # Well above average
                base_roic = min(10, base_roic + 0.4)
            elif roic >= sector_median * 1.5:
                # Above average
                base_roic = min(10, base_roic + 0.2)
            elif roic < sector_benchmarks['bottom_quartile']:
                # Below industry bottom quartile
                base_roic = max(1, base_roic - 1.0)
        
        # Leverage quality check
        if roe is not None and roic > 0:
            leverage_ratio = roe / roic
            
            if leverage_ratio < 1.05:
                # ROE ≈ ROIC = pristine balance sheet (V, MA, GOOGL style)
                # This is EXCEPTIONAL - high returns with no debt
                base_roic = min(10, base_roic + 0.8)
            elif 1.05 <= leverage_ratio <= 1.3:
                # Minimal leverage, still excellent
                base_roic = min(10, base_roic + 0.5)
            elif 1.3 < leverage_ratio <= 2.0:
                # Moderate leverage - acceptable if ROIC is high
                if roic >= sector_top:
                    # High ROIC justifies some leverage
                    base_roic = min(10, base_roic + 0.2)
                # else: no adjustment
            elif 2.0 < leverage_ratio <= 3.0:
                # Elevated leverage - caution
                if roic < sector_median:
                    base_roic = max(2, base_roic - 0.5)
                    warnings.append(f"Moderate leverage with mediocre ROIC: ROE/ROIC = {leverage_ratio:.1f}")
            elif 3.0 < leverage_ratio <= 4.5:
                # High leverage masking weak returns
                base_roic = max(2, base_roic - 1.5)
                warnings.append(f"High financial leverage: ROE/ROIC = {leverage_ratio:.1f}")
            else:
                # Excessive leverage - red flag
                base_roic = max(1, base_roic - 2.5)
                red_flags.append(f"Excessive leverage: ROE/ROIC = {leverage_ratio:.1f}")
        
        roic_absolute_score = base_roic

    elif roe is not None:
        # Fallback to ROE (less reliable, but better than nothing)
        if roe >= 100:      roic_absolute_score = 10.0  # Exceptional (SPGI level)
        elif roe >= 80:     roic_absolute_score = 9.9
        elif roe >= 60:     roic_absolute_score = 9.8
        elif roe >= 45:     roic_absolute_score = 9.5
        elif roe >= 40:     roic_absolute_score = 9.2
        elif roe >= 35:     roic_absolute_score = 9.0
        elif roe >= 30:     roic_absolute_score = 8.5
        elif roe >= 25:     roic_absolute_score = 8.0
        elif roe >= 22:     roic_absolute_score = 7.5
        elif roe >= 20:     roic_absolute_score = 7.0
        elif roe >= 18:     roic_absolute_score = 6.5
        elif roe >= 15:     roic_absolute_score = 6.0
        elif roe >= 12:     roic_absolute_score = 5.0
        elif roe >= 10:     roic_absolute_score = 4.0
        else:               roic_absolute_score = 3.0
        
        # Penalize if high leverage suspected (no ROIC to verify)
        debt_eq = metrics.get('Debt/Eq')
        if debt_eq is not None and sector != 'Financial':
            if debt_eq > 2.0:
                roic_absolute_score = max(2, roic_absolute_score - 2.0)
                warnings.append(f"High ROE may be leverage-driven (D/E={debt_eq:.2f}, no ROIC data)")
            elif debt_eq > 1.5:
                roic_absolute_score = max(3, roic_absolute_score - 1.0)
                warnings.append("ROE may be inflated by leverage (no ROIC data)")
    
    elif roa is not None:
        # Last resort - ROA (weakest proxy for ROIC)
        if roa >= 25:       roic_absolute_score = 8.5
        elif roa >= 20:     roic_absolute_score = 8.0
        elif roa >= 18:     roic_absolute_score = 7.5
        elif roa >= 15:     roic_absolute_score = 7.0
        elif roa >= 12:     roic_absolute_score = 6.0
        elif roa >= 10:     roic_absolute_score = 5.0
        else:               roic_absolute_score = 4.0

    quality_components.append(('ROIC_Absolute', roic_absolute_score, 0.50))

    # DEBUG: Show ROIC calculation
    if stock_symbol in ['MSFT', 'GOOGL', 'SPGI', 'KO']:
        print(f"\n   🔍 ROIC DIAGNOSTIC for {stock_symbol}:")
        print(f"      ROIC: {roic}%")
        print(f"      ROE: {roe}%")
        if roic and roe and roic > 0:
            leverage = roe / roic
            print(f"      Leverage Ratio (ROE/ROIC): {leverage:.2f}")
        print(f"      Sector: {sector}")
        print(f"      Sector Median: {sector_benchmarks['median']}%")
        print(f"      Sector Top Quartile: {sector_benchmarks['top_quartile']}%")
        print(f"      → ROIC Score: {roic_absolute_score:.1f}/10")
            # Show if elite business
            
    profit_margin = metrics.get('Profit_Margin')
    is_elite = (
        (roic and roic >= 25) or 
        (roe and roe >= 30) or 
        (profit_margin and profit_margin >= 25)
    )
    if is_elite:
        print(f"      🏆 ELITE BUSINESS (gets valuation premium)")

    # ========== 2. ROIC STABILITY (25% of quality = 12.5% of total) ==========
    # "Low volatility = durable competitive advantage" - McKinsey
    # High sustained ROIC > volatile high ROIC

    roic_stability_score = 5
    profit_margin = metrics.get('Profit_Margin')
    gross_margin = metrics.get('Gross_Margin')
    oper_margin = metrics.get('Oper_Margin')

    if roic is not None:
        # Without historical volatility data, use cross-sectional indicators
        
        # Base score: High absolute ROIC that persists = proven stability
        if roic >= 40:
            # Elite level sustained = incredible moat
            base_stability = 10
        elif roic >= 35:
            # Exceptional sustained returns
            base_stability = 9.5
        elif roic >= 30:
            # Outstanding stability
            base_stability = 9.0
        elif roic >= 25:
            # Excellent stability
            base_stability = 8.5
        elif roic >= 22:
            # Very good stability
            base_stability = 8.0
        elif roic >= 20:
            # Good stability
            base_stability = 7.5
        elif roic >= 18:
            # Above average
            base_stability = 7.0
        elif roic >= 15:
            # Moderate stability
            base_stability = 6.5
        elif roic >= 12:
            # Average
            base_stability = 6.0
        else:
            # Below average
            base_stability = 5.0
        
        # High profit margins suggest stable business model
        if profit_margin is not None:
            if profit_margin >= 35:
                base_stability = min(10, base_stability + 1.0)
            elif profit_margin >= 30:
                base_stability = min(10, base_stability + 0.7)
            elif profit_margin >= 25:
                base_stability = min(10, base_stability + 0.5)
            elif profit_margin >= 20:
                base_stability = min(10, base_stability + 0.3)
            elif profit_margin < 8:
                # Low margins = commodity-like = unstable
                base_stability = max(2, base_stability - 1.0)
        
        # Gross margin = pricing power = durable advantage
        if gross_margin is not None:
            if gross_margin >= 80:
                # Exceptional pricing power (software, platforms)
                base_stability = min(10, base_stability + 1.5)
            elif gross_margin >= 70:
                # Very strong pricing power
                base_stability = min(10, base_stability + 1.0)
            elif gross_margin >= 60:
                # Strong pricing power
                base_stability = min(10, base_stability + 0.6)
            elif gross_margin >= 50:
                # Good pricing power
                base_stability = min(10, base_stability + 0.3)
            elif gross_margin < 30:
                # Commodity-like = unstable
                base_stability = max(2, base_stability - 0.8)
        
        # Operating leverage stability
        if oper_margin is not None and profit_margin is not None and profit_margin > 0:
            margin_conversion = profit_margin / oper_margin if oper_margin > 0 else 0
            
            if margin_conversion >= 0.85:
                # Efficient conversion = stable model
                base_stability = min(10, base_stability + 0.3)
            elif margin_conversion < 0.6:
                # Inefficient = potential instability
                base_stability = max(3, base_stability - 0.5)
        
        # Sector-specific adjustments
        if sector in ['Utilities', 'Consumer Defensive', 'Healthcare']:
            # These sectors have inherently more stable ROIC
            base_stability = min(10, base_stability + 0.5)
        elif sector in ['Energy', 'Basic Materials']:
            # Commodity sectors = cyclical = less stable
            base_stability = max(3, base_stability - 0.8)
        elif sector in ['Technology', 'Communication Services']:
            # Tech can be stable OR disrupted - margins matter more
            if gross_margin and gross_margin >= 70:
                base_stability = min(10, base_stability + 0.4)
        
        roic_stability_score = base_stability

    elif roe is not None:
        # Fallback to ROE-based stability proxy
        if roe >= 30:
            base_stability = 8.0
        elif roe >= 25:
            base_stability = 7.5
        elif roe >= 20:
            base_stability = 7.0
        elif roe >= 15:
            base_stability = 6.0
        else:
            base_stability = 5.0
        
        # Adjust for margins
        if profit_margin and profit_margin >= 25:
            base_stability = min(10, base_stability + 0.8)
        elif profit_margin and profit_margin < 10:
            base_stability = max(3, base_stability - 0.5)
        
        roic_stability_score = base_stability

    quality_components.append(('ROIC_Stability', roic_stability_score, 0.25))

    # ========== 3. FCF POSITIVITY (10% of quality = 5% of total) ==========
    # "FCF > Net Income = quality earnings" - Research
    # Real cash generation, not accounting artifacts

    fcf_positivity_score = 5
    fcf_per_share = metrics.get('FCF_per_share')
    eps_ttm = metrics.get('EPS_TTM')
    fcf_yield = metrics.get('FCF_Yield')

    if fcf_per_share is not None and eps_ttm is not None and eps_ttm > 0:
        # FCF Conversion Ratio is the key metric
        conversion = fcf_per_share / eps_ttm
        
        # Sector-adjusted conversion thresholds
        # Growth sectors need more lenient thresholds due to high CapEx/R&D
        if sector in ['Technology', 'Communication Services', 'Healthcare']:
            # Growth sectors: more lenient due to high CapEx/R&D/AI infrastructure
            if conversion >= 1.4:
                base_fcf = 10
            elif conversion >= 1.25:
                base_fcf = 9.5
            elif conversion >= 1.1:
                base_fcf = 9.0
            elif conversion >= 1.0:
                base_fcf = 8.5
            elif conversion >= 0.85:
                base_fcf = 8.0
            elif conversion >= 0.75:
                base_fcf = 7.5   # Most mature tech (AAPL, MSFT)
            elif conversion >= 0.65:
                base_fcf = 7.0   # High CapEx tech (still healthy)
            elif conversion >= 0.55:
                base_fcf = 6.5   # ← GOOGL should score here (58.66%)
            elif conversion >= 0.50:
                base_fcf = 6.0   # Growth investment phase
            elif conversion >= 0.40:
                base_fcf = 5.0   # Heavy investment (acceptable)
            elif conversion >= 0.30:
                base_fcf = 4.0
                warnings.append(f"Low FCF conversion for {sector}: {conversion:.2%}")
            else:
                base_fcf = 3.0
                warnings.append(f"Poor FCF conversion for {sector}: {conversion:.2%}")
        
        elif sector in ['Consumer Defensive', 'Utilities', 'Real Estate']:
            # Mature sectors: should have high conversion (stable, low growth CapEx)
            if conversion >= 1.5:
                base_fcf = 10
            elif conversion >= 1.35:
                base_fcf = 9.5
            elif conversion >= 1.2:
                base_fcf = 9.0
            elif conversion >= 1.1:
                base_fcf = 8.5
            elif conversion >= 1.0:
                base_fcf = 8.0
            elif conversion >= 0.90:
                base_fcf = 7.0
            elif conversion >= 0.80:
                base_fcf = 6.0
            elif conversion >= 0.70:
                base_fcf = 5.0
                warnings.append(f"Low FCF conversion for mature {sector}: {conversion:.2%}")
            elif conversion >= 0.60:
                base_fcf = 4.0
                warnings.append(f"Poor FCF conversion for {sector}: {conversion:.2%}")
            else:
                base_fcf = 3.0
                red_flags.append(f"Very low FCF conversion in mature sector: {conversion:.2%}")
        
        elif sector in ['Energy', 'Basic Materials']:
            # Cyclical sectors: moderate expectations
            if conversion >= 1.5:
                base_fcf = 10
            elif conversion >= 1.3:
                base_fcf = 9.3
            elif conversion >= 1.15:
                base_fcf = 8.5
            elif conversion >= 1.0:
                base_fcf = 7.5
            elif conversion >= 0.85:
                base_fcf = 6.5
            elif conversion >= 0.70:
                base_fcf = 5.5
            elif conversion >= 0.60:
                base_fcf = 4.5
            else:
                base_fcf = 3.5
        
        elif sector == 'Financial':
            # Financials: FCF metrics less meaningful (regulatory capital requirements)
            if conversion >= 1.2:
                base_fcf = 9.0
            elif conversion >= 1.0:
                base_fcf = 8.0
            elif conversion >= 0.85:
                base_fcf = 7.0
            elif conversion >= 0.70:
                base_fcf = 6.0
            else:
                base_fcf = 5.0
        
        else:
            # Standard thresholds for other sectors (Industrials, Consumer Cyclical)
            if conversion >= 1.5:
                base_fcf = 10
            elif conversion >= 1.4:
                base_fcf = 9.7
            elif conversion >= 1.3:
                base_fcf = 9.3
            elif conversion >= 1.2:
                base_fcf = 9.0
            elif conversion >= 1.15:
                base_fcf = 8.5
            elif conversion >= 1.1:
                base_fcf = 8.0
            elif conversion >= 1.05:
                base_fcf = 7.5
            elif conversion >= 1.0:
                base_fcf = 7.0
            elif conversion >= 0.95:
                base_fcf = 6.5
            elif conversion >= 0.90:
                base_fcf = 6.0
            elif conversion >= 0.85:
                base_fcf = 5.5
            elif conversion >= 0.80:
                base_fcf = 5.0
            elif conversion >= 0.75:
                base_fcf = 4.0
                warnings.append(f"Low FCF conversion: {conversion:.2%}")
            elif conversion >= 0.60:
                base_fcf = 3.0
                warnings.append(f"Poor FCF conversion: {conversion:.2%}")
            elif conversion >= 0.50:
                base_fcf = 2.0
                red_flags.append(f"Very low FCF conversion: {conversion:.2%}")
            else:
                base_fcf = 1.0
                red_flags.append(f"Critical FCF issue: {conversion:.2%}")
        
        # Absolute FCF yield adjustment (market attractiveness)
        # High FCF yield = attractive regardless of conversion ratio
        if fcf_yield is not None:
            if fcf_yield >= 8:
                base_fcf = min(10, base_fcf + 0.8)
            elif fcf_yield >= 6:
                base_fcf = min(10, base_fcf + 0.5)
            elif fcf_yield >= 5:
                base_fcf = min(10, base_fcf + 0.3)
            elif fcf_yield >= 4:
                base_fcf = min(10, base_fcf + 0.2)
            # Note: Don't penalize low FCF yield for growth stocks
            # Growth companies naturally trade at low FCF yields
        
        # Absolute magnitude bonus (large companies generating massive FCF)
        # Higher absolute FCF = more financial flexibility
        if fcf_per_share >= 20:
            base_fcf = min(10, base_fcf + 0.5)
        elif fcf_per_share >= 15:
            base_fcf = min(10, base_fcf + 0.3)
        elif fcf_per_share >= 10:
            base_fcf = min(10, base_fcf + 0.2)
        elif fcf_per_share >= 5:
            base_fcf = min(10, base_fcf + 0.1)
        
        fcf_positivity_score = base_fcf

    elif fcf_per_share is not None:
        # Have FCF but no EPS for comparison
        if fcf_per_share > 0:
            # Use FCF yield as primary metric
            if fcf_yield and fcf_yield >= 6:
                fcf_positivity_score = 8.5
            elif fcf_yield and fcf_yield >= 5:
                fcf_positivity_score = 8.0
            elif fcf_yield and fcf_yield >= 4:
                fcf_positivity_score = 7.5
            elif fcf_yield and fcf_yield >= 3:
                fcf_positivity_score = 7.0
            elif fcf_yield and fcf_yield >= 2:
                fcf_positivity_score = 6.0
            else:
                fcf_positivity_score = 5.5
            
            # Absolute magnitude bonus
            if fcf_per_share >= 15:
                fcf_positivity_score = min(10, fcf_positivity_score + 0.5)
            elif fcf_per_share >= 10:
                fcf_positivity_score = min(10, fcf_positivity_score + 0.3)
        
        elif fcf_per_share < 0:
            fcf_positivity_score = 2.0
            red_flags.append("Negative Free Cash Flow")
        else:
            fcf_positivity_score = 3.0

    elif eps_ttm is not None and eps_ttm > 0:
        # Have earnings but no FCF data - assume moderate quality
        fcf_positivity_score = 5.5
        warnings.append("No FCF data available")

    else:
        # No data at all
        fcf_positivity_score = 5.0

    quality_components.append(('FCF_Positivity', fcf_positivity_score, 0.10))

    # DEBUG: Show why FCF score is what it is
    if stock_symbol in ['MSFT', 'GOOGL', 'SPGI', 'KO', 'V', 'MA', 'AAPL']:
        print(f"   🔍 FCF DIAGNOSTIC for {stock_symbol}:")
        print(f"      FCF/share: {fcf_per_share}")
        print(f"      EPS (TTM): {eps_ttm}")
        print(f"      FCF Yield: {fcf_yield}%")
        if fcf_per_share and eps_ttm and eps_ttm > 0:
            conversion = fcf_per_share / eps_ttm
            print(f"      FCF/EPS Conversion: {conversion:.2%}")
        print(f"      Sector: {sector}")
        print(f"      → FCF Score: {fcf_positivity_score:.1f}/10")

    # ========== 4. DEBT/EQUITY (10% of quality = 5% of total) ==========
    # Financial fortress vs financial risk

    debt_quality_score = 5
    debt_eq = metrics.get('Debt/Eq')
    lt_debt_eq = metrics.get('LT_Debt/Eq')
    current_ratio = metrics.get('Current_Ratio')

    if debt_eq is not None:
        if sector == 'Financial':
            # Banks/financials use leverage as part of business model
            if debt_eq < 6:
                debt_quality_score = 9.5
            elif debt_eq < 8:
                debt_quality_score = 8.5
            elif debt_eq < 10:
                debt_quality_score = 7.0
            elif debt_eq < 12:
                debt_quality_score = 5.5
            elif debt_eq < 15:
                debt_quality_score = 4.0
            else:
                debt_quality_score = 2.5
                warnings.append(f"High leverage for financial: D/E = {debt_eq:.2f}")
        
        else:
            # Non-financial companies
            max_acceptable = config.get('debt_eq_max', 0.8)
            
            if debt_eq < 0.05:
                # Virtually debt-free (Visa, Mastercard level)
                debt_quality_score = 10
            elif debt_eq < 0.15:
                # Essentially debt-free
                debt_quality_score = 9.8
            elif debt_eq < 0.25:
                # Minimal debt
                debt_quality_score = 9.5
            elif debt_eq < 0.40:
                # Very low debt
                debt_quality_score = 9.0
            elif debt_eq < 0.60:
                # Low debt
                debt_quality_score = 8.5
            elif debt_eq < 0.80:
                # Moderate debt
                debt_quality_score = 7.5
            elif debt_eq < 1.00:
                # Acceptable debt
                debt_quality_score = 6.5
            elif debt_eq < 1.30:
                # Elevated debt
                debt_quality_score = 5.5
            elif debt_eq < 1.60:
                # High debt
                debt_quality_score = 4.5
                warnings.append(f"Elevated debt: D/E = {debt_eq:.2f}")
            elif debt_eq < 2.00:
                # Very high debt
                debt_quality_score = 3.5
                warnings.append(f"High debt: D/E = {debt_eq:.2f}")
            elif debt_eq < 2.50:
                # Dangerous debt levels
                debt_quality_score = 2.5
                red_flags.append(f"Very high debt: D/E = {debt_eq:.2f}")
            else:
                # Critically high debt
                debt_quality_score = 1.5
                red_flags.append(f"Critical debt level: D/E = {debt_eq:.2f}")
            
            # Adjust for sector norms
            if sector in ['Utilities', 'Real Estate']:
                # These sectors tolerate higher debt
                if debt_eq < max_acceptable * 1.5:
                    debt_quality_score = min(10, debt_quality_score + 1.0)
            elif sector in ['Technology', 'Healthcare']:
                # These sectors should have low debt
                if debt_eq > max_acceptable:
                    debt_quality_score = max(2, debt_quality_score - 0.5)

    elif lt_debt_eq is not None:
        # Use long-term debt as proxy
        max_acceptable = config.get('debt_eq_max', 0.8)
        
        if lt_debt_eq < 0.20:
            debt_quality_score = 9.5
        elif lt_debt_eq < 0.40:
            debt_quality_score = 9.0
        elif lt_debt_eq < 0.60:
            debt_quality_score = 8.0
        elif lt_debt_eq < max_acceptable:
            debt_quality_score = 7.0
        elif lt_debt_eq < max_acceptable * 1.3:
            debt_quality_score = 5.5
        else:
            debt_quality_score = 4.0

    quality_components.append(('Debt_Quality', debt_quality_score, 0.10))

    # ========== 5. ROE SUPPLEMENTARY (5% of quality = 2.5% of total) ==========
    # Secondary metric when ROIC unavailable

    roe_supplementary_score = 5
    roe = metrics.get('ROE')

    if roe is not None:
        if roe >= 45:
            roe_supplementary_score = 10
        elif roe >= 40:
            roe_supplementary_score = 9.7
        elif roe >= 35:
            roe_supplementary_score = 9.3
        elif roe >= 30:
            roe_supplementary_score = 9.0
        elif roe >= 27:
            roe_supplementary_score = 8.5
        elif roe >= 25:
            roe_supplementary_score = 8.0
        elif roe >= 22:
            roe_supplementary_score = 7.5
        elif roe >= 20:
            roe_supplementary_score = 7.0
        elif roe >= 18:
            roe_supplementary_score = 6.5
        elif roe >= 15:
            roe_supplementary_score = 6.0
        elif roe >= 12:
            roe_supplementary_score = 5.0
        elif roe >= 10:
            roe_supplementary_score = 4.0
        elif roe >= 8:
            roe_supplementary_score = 3.0
        else:
            roe_supplementary_score = 2.0
        
        # Context check: If ROE is high but we saw high leverage, penalize here
        if roic is not None and roe > 0 and roic > 0:
            leverage_ratio = roe / roic
            if leverage_ratio > 3.0 and roe > 25:
                # High ROE is leverage-driven, not quality
                roe_supplementary_score = max(3, roe_supplementary_score - 2.0)

    quality_components.append(('ROE_Supplementary', roe_supplementary_score, 0.05))

    # ========== CALCULATE FINAL QUALITY SCORE ==========
    quality_score = sum(score * weight for _, score, weight in quality_components)

    # Apply red flag penalties (0.8 per red flag)
    if red_flags:
        penalty = len(red_flags) * 0.8
        quality_score = max(1, quality_score - penalty)

    # Bounds check
    quality_score = min(max(0, quality_score), 10)

    # ================== GROWTH SCORE (Research-aligned) ==================
    # Research: ROIC Growth (20%) > FCF Growth (30%) > EPS Growth (20%) > 
    #           Revenue Growth (15%) > ROE Growth (15%)
    # Key finding: "Growth matters only if ROIC > WACC"

    growth_components = []

    # 1. ROIC Growth (20% - MOST important per research!)
    roic_growth_score = calculate_roic_growth_score(metrics)
    growth_components.append(('ROIC_Growth', roic_growth_score, 0.20))

    # 2. FCF Growth (30%)
    fcf_growth_score = calculate_fcf_growth_score(metrics)
    growth_components.append(('FCF_Growth', fcf_growth_score, 0.30))

    # 3. EPS Growth (20%)
    eps_growth_score = 5
    eps_5y = metrics.get('EPS_past_5Y')
    eps_yoy = metrics.get('EPS_YoY_TTM')

    if eps_5y is not None:
        # Base score from 5-year CAGR
        if config['growth_expectations'] == 'high':
            if eps_5y >= 25:        base_eps_score = 10
            elif eps_5y >= 20:      base_eps_score = 9
            elif eps_5y >= 15:      base_eps_score = 8
            elif eps_5y >= 12:      base_eps_score = 7
            elif eps_5y >= 10:      base_eps_score = 6
            else:                   base_eps_score = 4
        elif config['growth_expectations'] == 'low':
            if eps_5y >= 10:        base_eps_score = 10
            elif eps_5y >= 7:       base_eps_score = 8
            elif eps_5y >= 5:       base_eps_score = 6
            else:                   base_eps_score = 4
        else:  # moderate
            if eps_5y >= 20:        base_eps_score = 10
            elif eps_5y >= 15:      base_eps_score = 9
            elif eps_5y >= 12:      base_eps_score = 8
            elif eps_5y >= 10:      base_eps_score = 7
            else:                   base_eps_score = 5
        
        # Consistency adjustment using YoY growth
        if eps_yoy is not None and eps_5y > 0:
            growth_deviation = abs(eps_yoy - eps_5y) / eps_5y
            
            if growth_deviation <= 0.25:
                # Very consistent growth (within 25%)
                base_eps_score = min(10, base_eps_score + 0.5)
            elif growth_deviation > 2.0:
                # Erratic growth (200%+ deviation)
                base_eps_score = max(2, base_eps_score - 1.5)
                warnings.append(f"Erratic EPS growth: 5Y={eps_5y:.1f}%, YoY={eps_yoy:.1f}%")
            elif growth_deviation > 1.5:
                # High volatility
                base_eps_score = max(3, base_eps_score - 1.0)
        
        eps_growth_score = base_eps_score

    elif eps_yoy is not None:
        # Fallback to YoY if no 5-year data
        if config['growth_expectations'] == 'high':
            if eps_yoy >= 25:       eps_growth_score = 8
            elif eps_yoy >= 20:     eps_growth_score = 7
            elif eps_yoy >= 15:     eps_growth_score = 6
            else:                   eps_growth_score = 4
        elif config['growth_expectations'] == 'low':
            if eps_yoy >= 10:       eps_growth_score = 8
            elif eps_yoy >= 7:      eps_growth_score = 7
            elif eps_yoy >= 5:      eps_growth_score = 6
            else:                   eps_growth_score = 4
        else:  # moderate
            if eps_yoy >= 20:       eps_growth_score = 8
            elif eps_yoy >= 15:     eps_growth_score = 7
            elif eps_yoy >= 12:     eps_growth_score = 6
            else:                   eps_growth_score = 5
        
        warnings.append("Using YoY EPS growth (no 5-year data)")

    growth_components.append(('EPS_Growth', eps_growth_score, 0.20))

    # 4. Revenue Growth (15% - LOWEST weight per research)
    revenue_growth_score = 5
    sales_5y = metrics.get('Sales_past_5Y')

    if sales_5y is not None:
        if config['growth_expectations'] == 'high':
            if sales_5y >= 25:      revenue_growth_score = 10
            elif sales_5y >= 20:    revenue_growth_score = 8
            elif sales_5y >= 15:    revenue_growth_score = 7
            elif sales_5y >= 10:    revenue_growth_score = 6
            else:                   revenue_growth_score = 4
        elif config['growth_expectations'] == 'low':
            if sales_5y >= 8:       revenue_growth_score = 10
            elif sales_5y >= 5:     revenue_growth_score = 8
            elif sales_5y >= 3:     revenue_growth_score = 6
            else:                   revenue_growth_score = 4
        else:  # moderate
            if sales_5y >= 15:      revenue_growth_score = 10
            elif sales_5y >= 12:    revenue_growth_score = 8
            elif sales_5y >= 8:     revenue_growth_score = 6
            else:                   revenue_growth_score = 4

    growth_components.append(('Revenue_Growth', revenue_growth_score, 0.15))

    # 5. ROE Growth (15%)
    roe_growth_score = calculate_roe_growth_score(metrics)
    growth_components.append(('ROE_Growth', roe_growth_score, 0.15))

    # Calculate final growth score
    growth_score = sum(score * weight for _, score, weight in growth_components)
        
    # ================== FINAL SCORE (Research-validated weights) ==================

    
    valuation_score = min(max(0, valuation_score), 10)
    quality_score = min(max(0, quality_score), 10)
    growth_score = min(max(0, growth_score), 10)

   # Get research-validated weights
    weights_info = get_research_validated_weights(sector)

    # Fixed 15% historical weight per research
    HISTORICAL_WEIGHT = 0.15
    historical_weight = HISTORICAL_WEIGHT if historical_score_ is not None else 0.0
    remaining_weight = 1.0 - historical_weight

    # Apply weights to non-historical components
    val_weight = weights_info['valuation'] * remaining_weight
    qual_weight = weights_info['quality'] * remaining_weight  
    growth_weight = weights_info['growth'] * remaining_weight

    # Quality-adjusted valuation context
    roic = metrics.get('ROIC')
    roe = metrics.get('ROE')
    profit_margin = metrics.get('Profit_Margin')

    # Calculate total score
    total_score = (valuation_score * val_weight + 
                quality_score * qual_weight + 
                growth_score * growth_weight)

    if historical_score_ is not None:
        total_score += historical_score_ * historical_weight

    # Add this BEFORE the return statement
    if stock_symbol in ['MSFT', 'GOOGL', 'SPGI', 'KO']:
        print(f"\n{'='*60}")
        print(f"DETAILED SCORING BREAKDOWN for {stock_symbol}")
        print(f"{'='*60}")
        
        # Weight verification
        total_check = qual_weight + growth_weight + val_weight + historical_weight
        print(f"\n📊 CATEGORY WEIGHTS:")
        print(f"   Quality:    {qual_weight*100:>5.1f}% (target: 50.0%)")
        print(f"   Growth:     {growth_weight*100:>5.1f}% (target: 20.0%)")
        print(f"   Valuation:  {val_weight*100:>5.1f}% (target: 15.0%)")
        print(f"   Historical: {historical_weight*100:>5.1f}% (target: 15.0%)")
        print(f"   Total:      {total_check*100:>5.1f}% (must be 100.0%)")
        
        # Quality breakdown
        print(f"\n💎 QUALITY COMPONENTS (50% of total):")
        quality_total = 0
        for name, score, weight in quality_components:
            contribution = score * weight * qual_weight
            quality_total += contribution
            print(f"   {name:.<25} {score:>4.1f}/10 × {weight*100:>4.0f}% = {contribution:>4.2f} pts")
        print(f"   {'QUALITY TOTAL':.<25} {quality_score:>4.1f}/10        = {quality_total:>4.2f} pts")
        
        # Growth breakdown
        print(f"\n📈 GROWTH COMPONENTS (20% of total):")
        growth_total = 0
        for name, score, weight in growth_components:
            contribution = score * weight * growth_weight
            growth_total += contribution
            print(f"   {name:.<25} {score:>4.1f}/10 × {weight*100:>4.0f}% = {contribution:>4.2f} pts")
        print(f"   {'GROWTH TOTAL':.<25} {growth_score:>4.1f}/10        = {growth_total:>4.2f} pts")
        
        # Valuation breakdown
        print(f"\n💰 VALUATION COMPONENTS (15% of total):")
        val_total = valuation_score * val_weight
        for name, score, weight in valuation_components:
            contribution = score * weight * val_weight
            print(f"   {name:.<25} {score:>4.1f}/10 × {weight*100:>4.0f}% = {contribution:>4.2f} pts")
        print(f"   {'VALUATION TOTAL':.<25} {valuation_score:>4.1f}/10        = {val_total:>4.2f} pts")
        
        # Historical
        if historical_score_ is not None:
            hist_contribution = historical_score_ * historical_weight
            print(f"\n📚 HISTORICAL SCORE (15% of total):")
            print(f"   Historical Score:         {historical_score_:>4.1f}/10        = {hist_contribution:>4.2f} pts")
        
        # Final
        print(f"\n{'='*60}")
        print(f"⭐ FINAL TOTAL SCORE: {total_score:.2f}/10")
        print(f"{'='*60}\n")

    if stock_symbol == 'GOOGL':
        print(f"\n   🔍 DETAILED FCF ANALYSIS:")
        print(f"      Raw FCF/share: {fcf_per_share}")
        print(f"      Raw EPS: {eps_ttm}")
        print(f"      Conversion: {fcf_per_share/eps_ttm if eps_ttm else 'N/A':.2%}")
        print(f"      FCF Yield: {fcf_yield}%")
        print(f"      Why score is {fcf_positivity_score}?")

    return {
        'valuation_score': round(valuation_score, 2),
        'quality_score': round(quality_score, 2),
        'stability_score': None,
        'growth_score': round(growth_score, 2),
        'historical_score': historical_score_,
        'total_score': round(total_score, 2),
        'sector': sector,
        'sector_config_used': config,
        'valuation_components': valuation_components,
        'quality_components': quality_components,
        'stability_components': [],
        'growth_components': growth_components,
        'red_flags': red_flags,
        'warnings': warnings,
        'sector_adjustments': {
            'pe_thresholds_used': config['pe_thresholds'],
            'growth_expectations': config['growth_expectations'],
            'dividend_weight': config['dividend_weight'],
            'debt_tolerance': config['debt_eq_max'],
            'historical_weight_used': historical_weight if historical_score_ is not None else 0.0,
            'has_historical_data': historical_score_ is not None
        },
        'research_insights': {
            'model_version': 'Research-Aligned v4.0',
            'methodology': 'Damodaran ROIC-focused + S&P 500 empirical data',
            'weight_breakdown': f'Quality: 50%, Growth: 20%, Valuation: 15%, Historical: 15%',
            'quality_focus': 'ROIC Absolute (25%) + ROIC Stability (12.5%) = 37.5% of total score',
            'growth_hierarchy': 'ROIC Growth (4%) > FCF Growth (6%) > EPS (4%) > Revenue (3%) > ROE (3%)',
            'key_finding': 'Growth only valuable if ROIC > WACC (Damodaran)',
            'historical_persistence': f'{historical_weight*100:.0f}% weight validates moat durability',
            'valuation_role': 'Mean-reverting indicator (15% weight)'
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
        quality_class = "positive" if scores['quality_score'] >= 7 else "neutral" if scores['quality_score'] >= 5 else "negative"
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
        
        # Add this after the growth data and before the scores
       # In create_enhanced_html function, replace the historical display logic:
        historical_display = f"{scores['historical_score']:.1f}" if scores['historical_score'] is not None else "N/A"
        historical_class = "positive" if scores['historical_score'] and scores['historical_score'] >= 7 else "neutral" if scores['historical_score'] and scores['historical_score'] >= 5 else "negative" if scores['historical_score'] else "na"

        # Add debug line to verify what's being used in HTML
        print(f"HTML Debug: {stock} historical score: {scores['historical_score']}")

        # Update the table row to include historical score (adjust colspan in details row accordingly)
        table_rows.append(f'''
            <tr class="stock-row" data-sector="{sector}" data-valuation="{scores['valuation_score']:.1f}" data-growth="{scores['growth_score']:.1f}" onclick="toggleDetails('{stock}')">
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
                <td class="{quality_class}">{scores['quality_score']:.1f}</td>
                <td class="{growth_class}">{scores['growth_score']:.1f}</td>
                <td class="{historical_class}">{historical_display}</td>
                <td class="{total_class}"><strong>{scores['total_score']:.1f}</strong></td>
            </tr>
        ''')
        
        # Update the details row (change colspan from 13 to 14 and add historical section)
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
                                <h4>📚 Historical Fundamentals</h4>
                                <p>Historical Score: <strong>{historical_display}</strong></p>
                                <p>Weight in Total Score: {scores['sector_adjustments']['historical_weight_used']*100:.1f}%</p>
                                <p>Data Available: {'✅ Yes' if scores['sector_adjustments']['has_historical_data'] else '❌ No'}</p>
                                <p><small>💡 Historical score reflects long-term fundamental consistency and quality</small></p>
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
                                <p>Historical Weight: {scores['sector_adjustments']['historical_weight_used']*100:.1f}%</p>
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
                <td colspan="13" class="error">Data not available (may be rate limited)</td>
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
            
            scores = calculate_enhanced_scores_with_sectors(metrics, sector, stock)
            if scores:
                print(f"   🎯 Scores: Val {scores['valuation_score']:.1f} | Qual {scores['quality_score']:.1f} | Growth {scores['growth_score']:.1f} | Total {scores['total_score']:.1f}")
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
