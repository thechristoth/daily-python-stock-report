import requests
import pandas as pd
import numpy as np
from collections import defaultdict
from datetime import datetime, date

HEADERS = {
    'User-Agent': 'Financial Analysis Tool contact@example.com',
    'Accept': 'application/json'
}

# Very flexible validation ranges for historical data
VALIDATION_RANGES = {
    'revenue': (1e5, 1e15),      # $100K to $1T
    'net_income': (1e4, 1e13),   # $10K to $100B
    'equity': (1e5, 1e15),       # $100K to $1T
    'eps': (0.001, 1000),        # $0.001 to $1000
    'debt': (1e4, 1e13),         # $10K to $100B
    'assets': (1e5, 1e15),       # $100K to $1T
    'current_liabilities': (1e4, 1e13),  # $10K to $100B
    'cash': (1e3, 1e14),         # $1K to $100B
    'operating_cash_flow': (1e5, 1e14),  # $100K to $100B
    'capex': (1e4, 1e13),        # $10K to $100B (usually negative)
    'fcf': (1e4, 1e14)           # $10K to $100B
}

TICKERS = {
    'AWI', 'AAPL', 'MSFT', 'AMZN', 'UL', 'MLI', 'GOOGL', 'SPGI', 'WM', 'KO', 'NVDA', 'TSM', 'BKNG', 'PINS', 'DUOL'
}

# Form priorities for different data types
FORM_PRIORITIES = {
    'annual': ['10-K', '10-K/A', '20-F'],           
    'quarterly': ['10-Q', '10-Q/A'],                
    'balance_sheet': ['10-K', '10-K/A', '10-Q', '10-Q/A', '20-F'],
    'cash_flow': ['10-K', '10-K/A', '10-Q', '10-Q/A', '20-F']  # Cash flow statement data
}

def get_all_cik():
    url = "https://www.sec.gov/files/company_tickers.json"
    headers = {"User-Agent": "YourName Contact@Email.com"}  # SEC requires UA

    resp = requests.get(url, headers=headers)
    data = resp.json()

    return data

def get_cik(ticker, all_cik):
    ticker = ticker.upper()
    for entry in all_cik.values():
        if entry["ticker"] == ticker:
            return str(entry["cik_str"]).zfill(10)  # pad to 10 digits
    return None

def analyze_business_stability(analysis):
    """
    Comprehensive business stability analysis with the following weightings:
    - Revenue Quality & Growth: 60% (6.0 points)
    - Free Cash Flow: 15% (1.5 points)  
    - Debt Management: 12% (1.2 points)
    - ROE & ROIC: 8% (0.8 points)
    - EPS Consistency: 5% (0.5 points)
    
    Total: 100% (10.0 points maximum)
    """
    if not analysis or not analysis.get('financial_metrics'):
        return {"score": 0, "details": "No financial data available"}

    metrics = analysis['financial_metrics']
    ticker = analysis['ticker']

    results = {
        'score': 0,
        'revenue_analysis': {},
        'fcf_analysis': {},
        'debt_analysis': {},
        'roe_roic_analysis': {},
        'eps_analysis': {},
        'disqualifiers': [],
        'warnings': [],
        'details': {}
    }

    # Extract years with data
    years = sorted([m['Year'] for m in metrics])
    recent_years = years[-7:] if len(years) >= 7 else years[-5:] if len(years) >= 5 else years

    # Collect data for recent years
    revenue_data = [(m['Year'], m['Revenue']) for m in metrics if m['Year'] in recent_years and m['Revenue'] is not None]
    fcf_data = [(m['Year'], m['FCF']) for m in metrics if m['Year'] in recent_years and m['FCF'] is not None]
    eps_data = [(m['Year'], m['EPS']) for m in metrics if m['Year'] in recent_years and m['EPS'] is not None]
    debt_data = [(m['Year'], m['TotalDebt']) for m in metrics if m['Year'] in recent_years and m['TotalDebt'] is not None]
    equity_data = [(m['Year'], m['TotalEquity']) for m in metrics if m['Year'] in recent_years and m['TotalEquity'] is not None]
    roe_data = [(m['Year'], m['ROE']) for m in metrics if m['Year'] in recent_years and m['ROE'] is not None]
    roic_data = [(m['Year'], m['ROIC']) for m in metrics if m['Year'] in recent_years and m['ROIC'] is not None]

    # ===== 1. REVENUE ANALYSIS (60% = 6.0 points) =====
    revenue_score = 0
    if len(revenue_data) >= 3:
        # Calculate growth rates
        revenue_growth_rates = []
        for i in range(1, len(revenue_data)):
            prev_rev = revenue_data[i-1][1]
            curr_rev = revenue_data[i][1]
            if prev_rev > 0:
                growth_rate = (curr_rev - prev_rev) / prev_rev * 100
                revenue_growth_rates.append(growth_rate)

        if revenue_growth_rates:
            avg_growth = sum(revenue_growth_rates) / len(revenue_growth_rates)
            declining_years = sum(1 for g in revenue_growth_rates if g < 0)
            
            # 1a. Growth Quality (0-2.5 points)
            if avg_growth >= 20:
                revenue_score += 2.5
            elif avg_growth >= 15:
                revenue_score += 2.2
            elif avg_growth >= 12:
                revenue_score += 2.0
            elif avg_growth >= 10:
                revenue_score += 1.7
            elif avg_growth >= 7:
                revenue_score += 1.4
            elif avg_growth >= 5:
                revenue_score += 1.0
            elif avg_growth >= 3:
                revenue_score += 0.6
            elif avg_growth >= 0:
                revenue_score += 0.2
            # Negative growth gets 0 points

            # 1b. Consistency (0-1.8 points)
            positive_growth_ratio = sum(1 for g in revenue_growth_rates if g > 0) / len(revenue_growth_rates)
            if positive_growth_ratio >= 0.95:
                revenue_score += 1.8
            elif positive_growth_ratio >= 0.85:
                revenue_score += 1.5
            elif positive_growth_ratio >= 0.75:
                revenue_score += 1.2
            elif positive_growth_ratio >= 0.65:
                revenue_score += 0.8
            elif positive_growth_ratio >= 0.5:
                revenue_score += 0.4

            # 1c. Growth Smoothness (0-1.2 points)
            if len(revenue_growth_rates) >= 3:
                std_dev = (sum((g - avg_growth) ** 2 for g in revenue_growth_rates) / len(revenue_growth_rates)) ** 0.5
                if std_dev <= 3:
                    revenue_score += 1.2
                elif std_dev <= 5:
                    revenue_score += 1.0
                elif std_dev <= 8:
                    revenue_score += 0.8
                elif std_dev <= 12:
                    revenue_score += 0.5
                elif std_dev <= 18:
                    revenue_score += 0.2

            # 1d. Long-term Growth Bonus (0-0.5 points)
            if len(revenue_data) >= 5:
                start_rev, end_rev = revenue_data[0][1], revenue_data[-1][1]
                if start_rev > 0:
                    total_growth = (end_rev - start_rev) / start_rev * 100
                    years_span = revenue_data[-1][0] - revenue_data[0][0]
                    if years_span > 0:
                        cagr = (end_rev / start_rev) ** (1/years_span) - 1
                        cagr_pct = cagr * 100
                        if cagr_pct >= 15:
                            revenue_score += 0.5
                        elif cagr_pct >= 12:
                            revenue_score += 0.4
                        elif cagr_pct >= 10:
                            revenue_score += 0.3
                        elif cagr_pct >= 7:
                            revenue_score += 0.2
                        elif cagr_pct >= 5:
                            revenue_score += 0.1

        results['revenue_analysis'] = {
            'avg_growth': avg_growth if revenue_growth_rates else None,
            'consistency_ratio': positive_growth_ratio if revenue_growth_rates else None,
            'declining_years': declining_years if revenue_growth_rates else None,
            'score': revenue_score,
            'data_points': len(revenue_data)
        }
    else:
        results['warnings'].append("Insufficient revenue history for analysis")
        revenue_score = 0.5  # Minimal score for having some revenue data

    # ===== 2. FREE CASH FLOW ANALYSIS (15% = 1.5 points) =====
    fcf_score = 0
    if len(fcf_data) >= 3:
        positive_fcf_years = sum(1 for _, fcf in fcf_data if fcf > 0)
        positive_fcf_ratio = positive_fcf_years / len(fcf_data)
        
        # Recent FCF values
        recent_fcf = [fcf for _, fcf in fcf_data[-3:]]
        avg_recent_fcf = sum(recent_fcf) / len(recent_fcf)
        
        # FCF Consistency (0-0.8 points)
        if positive_fcf_ratio >= 0.9:
            fcf_score += 0.8
        elif positive_fcf_ratio >= 0.8:
            fcf_score += 0.6
        elif positive_fcf_ratio >= 0.7:
            fcf_score += 0.4
        elif positive_fcf_ratio >= 0.6:
            fcf_score += 0.2

        # FCF Growth (0-0.7 points)
        if len(fcf_data) >= 4:
            fcf_growth_rates = []
            for i in range(1, len(fcf_data)):
                prev_fcf = fcf_data[i-1][1]
                curr_fcf = fcf_data[i][1]
                if prev_fcf > 0:
                    growth = (curr_fcf - prev_fcf) / prev_fcf * 100
                    fcf_growth_rates.append(growth)
            
            if fcf_growth_rates:
                avg_fcf_growth = sum(fcf_growth_rates) / len(fcf_growth_rates)
                if avg_fcf_growth >= 15:
                    fcf_score += 0.7
                elif avg_fcf_growth >= 10:
                    fcf_score += 0.5
                elif avg_fcf_growth >= 5:
                    fcf_score += 0.3
                elif avg_fcf_growth >= 0:
                    fcf_score += 0.1

        results['fcf_analysis'] = {
            'positive_fcf_ratio': positive_fcf_ratio,
            'avg_recent_fcf': avg_recent_fcf,
            'score': fcf_score,
            'data_points': len(fcf_data)
        }
    elif len(fcf_data) > 0:
        # Minimal analysis with limited data
        positive_fcf_count = sum(1 for _, fcf in fcf_data if fcf > 0)
        if positive_fcf_count > 0:
            fcf_score = 0.3
        results['fcf_analysis'] = {'score': fcf_score, 'data_points': len(fcf_data)}
    else:
        results['warnings'].append("No FCF data available")

    # ===== 3. DEBT MANAGEMENT (12% = 1.2 points) =====
    debt_score = 0
    if len(debt_data) >= 2 and len(equity_data) >= 2:
        # Calculate debt-to-equity ratios
        debt_equity_ratios = []
        for year in recent_years:
            debt_entry = next((d for d in debt_data if d[0] == year), None)
            equity_entry = next((e for e in equity_data if e[0] == year), None)
            
            if debt_entry and equity_entry and equity_entry[1] != 0:
                de_ratio = debt_entry[1] / equity_entry[1]
                debt_equity_ratios.append(de_ratio)
        
        if debt_equity_ratios:
            avg_de_ratio = sum(debt_equity_ratios) / len(debt_equity_ratios)
            latest_de_ratio = debt_equity_ratios[-1]
            
            # Debt Level Assessment (0-0.7 points)
            if avg_de_ratio <= 0.2:
                debt_score += 0.7  # Very low debt
            elif avg_de_ratio <= 0.4:
                debt_score += 0.6  # Low debt
            elif avg_de_ratio <= 0.7:
                debt_score += 0.4  # Moderate debt
            elif avg_de_ratio <= 1.0:
                debt_score += 0.2  # High debt
            # Very high debt (>1.0) gets 0 points
            
            # Debt Trend (0-0.5 points)
            if len(debt_equity_ratios) >= 3:
                trend_improving = debt_equity_ratios[-1] < debt_equity_ratios[0]
                if trend_improving:
                    debt_score += 0.5
                elif debt_equity_ratios[-1] <= debt_equity_ratios[0] * 1.1:  # Stable
                    debt_score += 0.3

        results['debt_analysis'] = {
            'avg_debt_equity_ratio': avg_de_ratio if debt_equity_ratios else None,
            'latest_debt_equity_ratio': latest_de_ratio if debt_equity_ratios else None,
            'score': debt_score,
            'data_points': len(debt_equity_ratios) if debt_equity_ratios else 0
        }
    else:
        results['warnings'].append("Insufficient debt/equity data")

    # ===== 4. ROE & ROIC ANALYSIS (8% = 0.8 points) =====
    roe_roic_score = 0
    roe_values = [roe for _, roe in roe_data if roe is not None]
    roic_values = [roic for _, roic in roic_data if roic is not None]
    
    # ROE Analysis (0-0.4 points)
    if len(roe_values) >= 2:
        avg_roe = sum(roe_values) / len(roe_values)
        recent_roe = roe_values[-1]
        
        if avg_roe >= 20:
            roe_roic_score += 0.4
        elif avg_roe >= 15:
            roe_roic_score += 0.35
        elif avg_roe >= 12:
            roe_roic_score += 0.25
        elif avg_roe >= 10:
            roe_roic_score += 0.15
        elif avg_roe >= 8:
            roe_roic_score += 0.05
    elif len(roe_values) == 1:
        # Partial credit for single data point
        single_roe = roe_values[0]
        if single_roe >= 15:
            roe_roic_score += 0.2
        elif single_roe >= 10:
            roe_roic_score += 0.1
    
    # ROIC Analysis (0-0.4 points)  
    if len(roic_values) >= 2:
        avg_roic = sum(roic_values) / len(roic_values)
        recent_roic = roic_values[-1]
        
        if avg_roic >= 15:
            roe_roic_score += 0.4
        elif avg_roic >= 12:
            roe_roic_score += 0.35
        elif avg_roic >= 10:
            roe_roic_score += 0.25
        elif avg_roic >= 8:
            roe_roic_score += 0.15
        elif avg_roic >= 6:
            roe_roic_score += 0.05
    elif len(roic_values) == 1:
        # Partial credit for single data point
        single_roic = roic_values[0]
        if single_roic >= 12:
            roe_roic_score += 0.2
        elif single_roic >= 8:
            roe_roic_score += 0.1

    results['roe_roic_analysis'] = {
        'avg_roe': sum(roe_values) / len(roe_values) if roe_values else None,
        'avg_roic': sum(roic_values) / len(roic_values) if roic_values else None,
        'roe_data_points': len(roe_values),
        'roic_data_points': len(roic_values),
        'score': roe_roic_score
    }

    # ===== 5. EPS CONSISTENCY (5% = 0.5 points) =====
    eps_score = 0
    if len(eps_data) >= 3:
        eps_values = [eps for _, eps in eps_data]
        positive_eps_count = sum(1 for eps in eps_values if eps > 0)
        positive_eps_ratio = positive_eps_count / len(eps_values)
        
        # EPS Positivity (0-0.3 points)
        if positive_eps_ratio >= 0.9:
            eps_score += 0.3
        elif positive_eps_ratio >= 0.8:
            eps_score += 0.2
        elif positive_eps_ratio >= 0.7:
            eps_score += 0.1

        # EPS Growth (0-0.2 points)
        if len(eps_data) >= 4:
            eps_growth_rates = []
            for i in range(1, len(eps_data)):
                prev_eps = eps_data[i-1][1]
                curr_eps = eps_data[i][1]
                if prev_eps > 0:
                    growth = (curr_eps - prev_eps) / prev_eps * 100
                    eps_growth_rates.append(growth)
            
            if eps_growth_rates:
                avg_eps_growth = sum(eps_growth_rates) / len(eps_growth_rates)
                if avg_eps_growth >= 10:
                    eps_score += 0.2
                elif avg_eps_growth >= 5:
                    eps_score += 0.1

        results['eps_analysis'] = {
            'positive_eps_ratio': positive_eps_ratio,
            'avg_eps_growth': avg_eps_growth if 'eps_growth_rates' in locals() and eps_growth_rates else None,
            'score': eps_score,
            'data_points': len(eps_data)
        }
    elif len(eps_data) > 0:
        # Minimal scoring for limited EPS data
        recent_eps = eps_data[-1][1]
        if recent_eps > 0:
            eps_score = 0.1
        results['eps_analysis'] = {'score': eps_score, 'data_points': len(eps_data)}

    # ===== FINAL SCORE CALCULATION =====
    total_score = revenue_score + fcf_score + debt_score + roe_roic_score + eps_score
    
    # Quality bonus for companies with comprehensive high-quality metrics
    if (len(revenue_data) >= 5 and len(fcf_data) >= 4 and 
        len(roe_values) >= 3 and len(roic_values) >= 3):
        comprehensive_bonus = 0.2
        total_score += comprehensive_bonus
        results['details']['comprehensive_bonus'] = comprehensive_bonus
    
    # Cap at 10.0
    results['score'] = round(min(10.0, total_score), 2)
    
    # Add component scores to details
    results['details'].update({
        'revenue_score': round(revenue_score, 2),
        'fcf_score': round(fcf_score, 2), 
        'debt_score': round(debt_score, 2),
        'roe_roic_score': round(roe_roic_score, 2),
        'eps_score': round(eps_score, 2),
        'total_weighted_components': round(revenue_score + fcf_score + debt_score + roe_roic_score + eps_score, 2)
    })

    return results

def get_filled_data(data):
    """Get completed data with missing values filled using advanced interpolation"""
    if not data or 'financial_metrics' not in data:
        return data
    
    # Create a copy to avoid modifying original data
    filled_data = data.copy()
    filled_data['financial_metrics'] = complete_missing_data(data['financial_metrics'])
    
    return filled_data

def advanced_time_series_interpolation(years, values):
    """Advanced interpolation that handles all patterns of missing data"""
    if not values or all(v is None for v in values):
        return values
    
    filled_values = list(values)
    n = len(years)
    
    # Pattern 1: Single missing values surrounded by data
    for i in range(1, n-1):
        if filled_values[i] is None and filled_values[i-1] is not None and filled_values[i+1] is not None:
            # Linear interpolation for single missing values
            prev_val = filled_values[i-1]
            next_val = filled_values[i+1]
            year_gap = years[i+1] - years[i-1]
            if year_gap > 0 and prev_val != 0:
                growth_rate = (next_val / prev_val) ** (1/year_gap) - 1
                year_diff = years[i] - years[i-1]
                filled_values[i] = prev_val * (1 + growth_rate) ** year_diff
    
    # Pattern 2: Multiple consecutive missing values at the beginning
    start_index = 0
    while start_index < n and filled_values[start_index] is None:
        start_index += 1
    
    if start_index > 0 and start_index < n:
        # Find the next available value after the gap
        next_index = start_index
        while next_index < n and filled_values[next_index] is None:
            next_index += 1
        
        if next_index < n:
            # Calculate growth rate from available data after the gap
            base_index = next_index
            lookahead = min(3, n - base_index - 1)
            growth_rates = []
            
            for j in range(lookahead):
                if (base_index + j + 1 < n and 
                    filled_values[base_index + j] is not None and 
                    filled_values[base_index + j + 1] is not None):
                    val1 = filled_values[base_index + j]
                    val2 = filled_values[base_index + j + 1]
                    year_diff = years[base_index + j + 1] - years[base_index + j]
                    if year_diff > 0 and val1 != 0:
                        growth_rate = (val2 / val1) ** (1/year_diff) - 1
                        growth_rates.append(growth_rate)
            
            if growth_rates:
                avg_growth = sum(growth_rates) / len(growth_rates)
                # Backfill missing values at the beginning
                for i in range(start_index - 1, -1, -1):
                    year_diff = years[i+1] - years[i]
                    if filled_values[i+1] is not None:
                        filled_values[i] = filled_values[i+1] / ((1 + avg_growth) ** year_diff)
    
    # Pattern 3: Multiple consecutive missing values at the end
    end_index = n - 1
    while end_index >= 0 and filled_values[end_index] is None:
        end_index -= 1
    
    if end_index < n - 1 and end_index >= 0:
        # Find the previous available value before the gap
        prev_index = end_index
        while prev_index >= 0 and filled_values[prev_index] is None:
            prev_index -= 1
        
        if prev_index >= 0:
            # Calculate growth rate from available data before the gap
            base_index = prev_index
            lookback = min(3, base_index)
            growth_rates = []
            
            for j in range(lookback):
                if (base_index - j - 1 >= 0 and 
                    filled_values[base_index - j] is not None and 
                    filled_values[base_index - j - 1] is not None):
                    val1 = filled_values[base_index - j - 1]
                    val2 = filled_values[base_index - j]
                    year_diff = years[base_index - j] - years[base_index - j - 1]
                    if year_diff > 0 and val1 != 0:
                        growth_rate = (val2 / val1) ** (1/year_diff) - 1
                        growth_rates.append(growth_rate)
            
            if growth_rates:
                avg_growth = sum(growth_rates) / len(growth_rates)
                # Forward fill missing values at the end
                for i in range(end_index + 1, n):
                    year_diff = years[i] - years[i-1]
                    if filled_values[i-1] is not None:
                        filled_values[i] = filled_values[i-1] * ((1 + avg_growth) ** year_diff)
    
    # Pattern 4: Multiple consecutive missing values in the middle
    # Find all gaps of consecutive missing values
    gaps = []
    i = 0
    while i < n:
        if filled_values[i] is None:
            gap_start = i
            while i < n and filled_values[i] is None:
                i += 1
            gap_end = i - 1
            if gap_start > 0 and gap_end < n - 1:
                gaps.append((gap_start, gap_end))
        else:
            i += 1
    
    # Fill each gap in the middle
    for gap_start, gap_end in gaps:
        prev_val = filled_values[gap_start - 1]
        next_val = filled_values[gap_end + 1]
        
        if prev_val is not None and next_val is not None and prev_val != 0:
            total_years = years[gap_end + 1] - years[gap_start - 1]
            if total_years > 0:
                growth_rate = (next_val / prev_val) ** (1/total_years) - 1
                
                # Fill each missing value in the gap
                for i in range(gap_start, gap_end + 1):
                    year_diff = years[i] - years[gap_start - 1]
                    filled_values[i] = prev_val * (1 + growth_rate) ** year_diff
    
    # Pattern 5: Sparse data (every other value missing, etc.)
    # Use moving average growth rate for very sparse data
    available_indices = [i for i, v in enumerate(filled_values) if v is not None]
    
    if len(available_indices) >= 2:
        # Calculate growth rates between all available points
        growth_rates = []
        for j in range(1, len(available_indices)):
            i1 = available_indices[j-1]
            i2 = available_indices[j]
            val1 = filled_values[i1]
            val2 = filled_values[i2]
            year_diff = years[i2] - years[i1]
            if year_diff > 0 and val1 != 0:
                growth_rate = (val2 / val1) ** (1/year_diff) - 1
                growth_rates.append(growth_rate)
        
        if growth_rates:
            avg_growth = sum(growth_rates) / len(growth_rates)
            
            # Fill any remaining missing values using average growth
            for i in range(n):
                if filled_values[i] is None:
                    # Find closest available value
                    left_val = None
                    left_dist = float('inf')
                    right_val = None
                    right_dist = float('inf')
                    
                    for j in range(i-1, -1, -1):
                        if filled_values[j] is not None:
                            left_val = filled_values[j]
                            left_dist = years[i] - years[j]
                            break
                    
                    for j in range(i+1, n):
                        if filled_values[j] is not None:
                            right_val = filled_values[j]
                            right_dist = years[j] - years[i]
                            break
                    
                    # Use the closer available value
                    if left_val is not None and (right_val is None or left_dist <= right_dist):
                        year_diff = years[i] - years[i - left_dist]
                        filled_values[i] = left_val * ((1 + avg_growth) ** left_dist)
                    elif right_val is not None:
                        year_diff = right_dist
                        filled_values[i] = right_val / ((1 + avg_growth) ** right_dist)
    
    return filled_values

def calculate_growth_rate(prev_value, next_value, year_gap):
    """Calculate annual growth rate between two values with given year gap"""
    if prev_value is None or next_value is None or prev_value == 0:
        return None
    
    # Calculate compound annual growth rate
    if year_gap > 0:
        growth_rate = (next_value / prev_value) ** (1 / year_gap) - 1
        return growth_rate
    return None

def complete_missing_data(financial_metrics):
    """Complete missing data using advanced interpolation for all patterns"""
    if not financial_metrics:
        return financial_metrics
    
    # Get all metric keys that might have missing data
    metric_keys = ['Revenue', 'NetIncome', 'OperatingIncome', 'EPS', 
                  'OperatingCashFlow', 'CapEx', 'FCF', 'TotalDebt', 
                  'TotalEquity', 'Cash']
    
    # Create a copy to avoid modifying original data
    completed_data = [metric.copy() for metric in financial_metrics]
    
    # Track which values were filled
    filled_values = []
    
    for metric_key in metric_keys:
        # Extract the time series for this metric
        years = [metric['Year'] for metric in completed_data]
        values = [metric.get(metric_key) for metric in completed_data]
        
        # Skip if no data at all
        if all(v is None for v in values):
            continue
        
        # Fill missing values using advanced interpolation
        filled_series = advanced_time_series_interpolation(years, values)
        
        # Update the completed data with filled values
        for i, (year, filled_value) in enumerate(zip(years, filled_series)):
            if values[i] is None and filled_value is not None:
                completed_data[i][metric_key] = filled_value
                if '_filled' not in completed_data[i]:
                    completed_data[i]['_filled'] = {}
                completed_data[i]['_filled'][metric_key] = True
                filled_values.append((year, metric_key, filled_value))
    
    # Print filled values
    if filled_values:
        print(f"\n📈 Filled missing values using advanced interpolation:")
        for year, metric, value in filled_values:
            is_currency = metric not in ['EPS', 'ROE', 'ROIC']
            print(f"   ↳ {metric} for {year}: {format_value(value, is_currency=is_currency, is_percent=False)}")
    
    return completed_data

def get_financial_data_direct(ticker, cik):
    if not cik:
        return None, f"Ticker {ticker} not found"
    
    url = f"https://data.sec.gov/api/xbrl/companyfacts/CIK{cik}.json"
    
    try:
        response = requests.get(url, headers=HEADERS, timeout=15)
        response.raise_for_status()
        return response.json(), None
    except Exception as e:
        return None, f"Error: {e}"

def parse_date(date_string):
    """Parse date string into datetime object"""
    if not date_string:
        return None
    try:
        return datetime.fromisoformat(date_string.replace('Z', '+00:00'))
    except:
        try:
            return datetime.strptime(date_string, '%Y-%m-%d')
        except:
            return None

def is_valid_value(value, metric_type):
    """Very flexible value validation"""
    if value is None:
        return False
    
    min_val, max_val = VALIDATION_RANGES.get(metric_type, (0, 1e15))
    return min_val <= abs(value) <= max_val

def get_data_type_for_metric(metric_type):
    """Determine which form types to use for each metric"""
    if metric_type in ['revenue', 'net_income', 'operating_income', 'eps']:
        return 'annual'  # Use annual forms (10-K, 20-F) for income statement items
    elif metric_type in ['equity', 'debt', 'assets', 'current_liabilities', 'cash']:
        return 'balance_sheet'  # Use both annual and quarterly forms for balance sheet items
    elif metric_type in ['operating_cash_flow', 'capex', 'fcf']:
        return 'cash_flow'  # Use annual forms for cash flow statement items
    else:
        return 'annual'

def get_calendar_year_from_fiscal(fiscal_year, end_date_str, ticker):
    """
    Improved fiscal to calendar year conversion with better edge case handling
    """
    if not fiscal_year:
        return None
    
    if not end_date_str:
        return fiscal_year
    
    end_date = parse_date(end_date_str)
    if not end_date:
        return fiscal_year
    
    month = end_date.month
    year = end_date.year
    
    # More sophisticated fiscal year mapping
    if month == 12:
        # December year-end: fiscal year = calendar year
        return year
    elif month in [1, 2, 3]:
        # Jan-Mar: typically previous calendar year (Q1 of fiscal year)
        return year - 1
    elif month in [4, 5, 6]:
        # Apr-Jun: could be either, but typically current calendar year
        # For most companies, this is Q2 of current fiscal year
        return year
    elif month in [7, 8, 9]:
        # Jul-Sep: typically current calendar year (Q3)
        return year
    else:  # month in [10, 11]
        # Oct-Nov: typically current calendar year (Q4)
        return year

# Add this helper function for better debugging

def find_best_tag_by_consistency(us_gaap, tag_options, metric_type, years_range, ticker):
    """Find the best tag with improved fallback logic and better data validation"""
    best_tag = None
    best_data = {}
    best_score = -1
    
    data_type = get_data_type_for_metric(metric_type)
    allowed_forms = FORM_PRIORITIES[data_type].copy()
    
    # Expand allowed forms for better coverage
    if data_type in ['annual', 'balance_sheet', 'cash_flow']:
        allowed_forms.extend(['8-K', '8-K/A', '6-K', '40-F'])
    
    # Try each tag option systematically
    for tag in tag_options:
        if tag not in us_gaap:
            continue
            
        metric_data = us_gaap[tag]
        yearly_data = {}
        
        # Check all unit types with more flexible filtering
        unit_types_to_check = metric_data.get('units', {})
        
        for unit_type, data_points in unit_types_to_check.items():
            # More flexible unit validation
            valid_unit = True
            if metric_type != 'eps':
                # Accept various USD denominations and pure numbers
                valid_unit = any(keyword in unit_type.upper() for keyword in 
                               ['USD', 'US$', '$', 'PURE', 'SHARES', ''])
            
            if not valid_unit:
                continue
            
            for point in data_points:
                form = point.get('form', '')
                fiscal_year = point.get('fy')
                fiscal_period = point.get('fp', '')
                value = point.get('val')
                end_date = point.get('end', '')
                filed_date = point.get('filed', '')
                
                # Skip if no fiscal year or value
                if fiscal_year is None or value is None:
                    continue
                
                # More flexible form filtering
                if form and form not in allowed_forms:
                    # Allow some forms as fallback if no better data
                    if form not in ['8-K', '6-K', '40-F']:
                        continue
                
                # Convert to calendar year with better handling
                calendar_year = get_calendar_year_from_fiscal(fiscal_year, end_date, ticker)
                # Skip if calendar year conversion failed
                if calendar_year is None:
                    continue
                
                
                # Use extended range for initial filtering
                extended_range = (years_range[0] - 3, years_range[1] + 3)
                if not (extended_range[0] <= calendar_year <= extended_range[1]):
                    continue
                
                # More flexible value validation
                if metric_type in VALIDATION_RANGES:
                    min_val, max_val = VALIDATION_RANGES[metric_type]
                    # Extend ranges significantly for flexibility
                    extended_min = min_val / 1000
                    extended_max = max_val * 1000
                    
                    # Special handling for EPS
                    if metric_type == 'eps':
                        if not (-10000 <= value <= 10000):  # Very wide EPS range
                            continue
                    elif not (extended_min <= abs(value) <= extended_max):
                        continue
                
                # Parse dates for recency comparison
                end_dt = parse_date(end_date)
                filed_dt = parse_date(filed_date)
                
                data_entry = {
                    'value': value,
                    'form': form,
                    'period': fiscal_period,
                    'fiscal_year': fiscal_year,
                    'calendar_year': calendar_year,
                    'end_date': end_date,
                    'filed_date': filed_date,
                    'end_dt': end_dt,
                    'filed_dt': filed_dt,
                    'unit_type': unit_type,
                    'tag': tag  # Store the actual tag used
                }
                
                # Handle duplicates with improved logic
                if calendar_year in yearly_data:
                    existing = yearly_data[calendar_year]
                    should_replace = False
                    
                    # Priority 1: Form type (10-K > 10-Q > others)
                    form_priority = {'10-K': 10, '10-K/A': 9, '20-F': 8, '10-Q': 7, 
                                   '10-Q/A': 6, '8-K': 5, '6-K': 4, '40-F': 3}
                    
                    current_priority = form_priority.get(form, 1)
                    existing_priority = form_priority.get(existing['form'], 1)
                    
                    if current_priority > existing_priority:
                        should_replace = True
                    elif current_priority == existing_priority:
                        # Priority 2: Period (FY > Q4 > Q3 > Q2 > Q1)
                        period_priority = {'FY': 5, 'Q4': 4, 'Q3': 3, 'Q2': 2, 'Q1': 1, '': 2}
                        current_period_prio = period_priority.get(fiscal_period, 0)
                        existing_period_prio = period_priority.get(existing.get('period'), 0)
                        
                        if current_period_prio > existing_period_prio:
                            should_replace = True
                        elif current_period_prio == existing_period_prio:
                            # Priority 3: More recent filing
                            if (filed_dt and existing.get('filed_dt') and 
                                filed_dt > existing['filed_dt']):
                                should_replace = True
                            # Priority 4: For EPS, prefer diluted
                            elif metric_type == 'eps':
                                current_tag_lower = tag.lower()
                                existing_tag = existing.get('tag', '').lower()
                                if 'diluted' in current_tag_lower and 'basic' in existing_tag:
                                    should_replace = True
                    
                    if should_replace:
                        yearly_data[calendar_year] = data_entry
                else:
                    yearly_data[calendar_year] = data_entry
        
        # Score the data for this tag
        if yearly_data:
            # Filter to target years for scoring
            target_data = {year: data for year, data in yearly_data.items() 
                          if years_range[0] <= year <= years_range[1]}
            
            if not target_data:
                continue
            
            # Calculate completeness score
            target_years = years_range[1] - years_range[0] + 1
            completeness = len(target_data) / target_years
            
            # Calculate continuity bonus
            years_list = sorted(target_data.keys())
            max_consecutive = 0
            current_streak = 0
            for i, year in enumerate(years_list):
                if i == 0 or year == years_list[i-1] + 1:
                    current_streak += 1
                    max_consecutive = max(max_consecutive, current_streak)
                else:
                    current_streak = 1
            
            continuity_bonus = (max_consecutive / target_years) * 0.3
            
            # Form quality bonus
            annual_forms = sum(1 for data in target_data.values() 
                             if data['form'] in ['10-K', '10-K/A', '20-F'])
            form_bonus = (annual_forms / len(target_data)) * 0.2
            
            # Value consistency check
            values = [data['value'] for data in target_data.values()]
            if len(values) > 1:
                # Check for reasonable progression (no extreme jumps)
                value_changes = []
                for i in range(1, len(values)):
                    if abs(values[i-1]) > 0:
                        change_pct = abs(values[i] - values[i-1]) / abs(values[i-1])
                        value_changes.append(change_pct)
                
                if value_changes:
                    avg_change = sum(value_changes) / len(value_changes)
                    # Penalize extreme volatility (more than 100% average change)
                    volatility_penalty = min(0.5, avg_change * 0.1)
                else:
                    volatility_penalty = 0
            else:
                volatility_penalty = 0
            
            total_score = completeness + continuity_bonus + form_bonus - volatility_penalty
            
            if total_score > best_score:
                best_score = total_score
                best_tag = tag
                best_data = target_data
    
    return best_tag, best_data, best_score

def calculate_fcf(operating_cash_flow, capex):
    """
    Calculate Free Cash Flow = Operating Cash Flow - Capital Expenditures
    Note: CapEx is often reported as negative, so we handle both conventions
    """
    if operating_cash_flow is None or capex is None:
        return None
    
    # Handle different CapEx conventions
    # If CapEx is positive, make it negative for FCF calculation
    # If CapEx is already negative, use as-is
    capex_adjusted = abs(capex) * -1 if capex > 0 else capex
    
    fcf = operating_cash_flow + capex_adjusted  # Adding negative CapEx
    return fcf

def calculate_roic_from_components(net_income, total_debt, total_equity, operating_income=None, tax_rate=0.25):
    """
    Calculate ROIC (Return on Invested Capital) using available components
    ROIC = NOPAT / Invested Capital
    
    Priority:
    1. Use Operating Income * (1 - Tax Rate) as NOPAT if available
    2. Fall back to Net Income if Operating Income not available
    
    Invested Capital = Total Debt + Total Equity
    """
    if not all([total_debt is not None, total_equity is not None]):
        return None
    
    # Calculate NOPAT - prefer operating income approach
    if operating_income is not None:
        nopat = operating_income * (1 - tax_rate)  # Approximate after-tax operating income
    elif net_income is not None:
        nopat = net_income  # Fallback to net income
    else:
        return None
    
    # Calculate invested capital - standard approach
    invested_capital = total_debt + total_equity
    
    if invested_capital <= 0:
        return None
    
    roic = (nopat / invested_capital) * 100
    return roic, "Operating" if operating_income is not None else "NetIncome"

def calculate_roic_from_roe(roe, total_debt, total_equity):
    """
    Alternative method: Calculate ROIC from ROE using the relationship
    ROIC ≈ ROE * (Equity / (Debt + Equity))
    
    This is an approximation that works when:
    - Net Income ≈ NOPAT (after-tax operating income)
    - The company's capital structure is stable
    """
    if not all([roe is not None, total_debt is not None, total_equity is not None]):
        return None
    
    if total_debt + total_equity <= 0:
        return None
    
    equity_ratio = total_equity / (total_debt + total_equity)
    roic_from_roe = roe * equity_ratio
    
    return roic_from_roe

def extract_historical_data(us_gaap, ticker, years_range):
    """Extract historical data with proper form separation and date validation"""
    results = {}
    
    tag_options = {
        'revenue': [
            # Most common revenue tags
            'RevenueFromContractWithCustomerExcludingAssessedTax',
            'Revenues',
            'SalesRevenueNet',
            'RevenueFromContractWithCustomer',
            'TotalRevenue',
            'Revenue',
            'SalesRevenueGoodsNet',
            'OperatingRevenues',
            'Sales',
            'TotalRevenuesAndOtherIncome',
            'SalesRevenueServicesNet',
            'RevenuesNet',
            'TotalOperatingRevenue',
            'NetSales',
            'GrossRevenue',
            'SalesRevenue',
            'OperatingRevenue',
            # Service-specific tags
            'RevenuesFromExternalCustomers',
            'ServiceRevenue',
            'ProductRevenue',
            'SubscriptionRevenue',
            # Financial services specific
            'InterestAndDividendIncomeOperating',
            'TotalInterestIncomeOperatingActivities',
            'NoninterestIncome',
            'InterestIncomeOperating',
            'InterestAndFeeIncome',
            # Additional variations
            'RevenuesExcludingInterestAndDividends',
            'RevenueNet',
            'NetRevenues',
            'TotalRevenueAndOtherIncome',
            'TotalNetRevenues',
            'ConsolidatedRevenues'
        ],
        'net_income': [
            'NetIncomeLoss',
            'ProfitLoss',
            'NetIncome',
            'IncomeLossFromContinuingOperations',
            'NetIncomeLossAttributableToParent',
            'Profit',
            'NetIncomeLossAttributableToNoncontrollingInterest',
            'IncomeLossFromContinuingOperationsBeforeIncomeTaxesExtraordinaryItemsNoncontrollingInterest',
            'NetIncomeLossAttributableToParentAndNoncontrollingInterest',
            'IncomeLossIncludingPortionAttributableToNoncontrollingInterest',
            'ConsolidatedNetIncome',
            'EarningsLossFromContinuingOperations',
            'IncomeLossBeforeGainOrLossOnSaleOfPropertiesExtraordinaryItemsAndCumulativeEffectsOfAccountingChanges',
            'NetIncomeLossAvailableToCommonStockholdersBasic',
            'NetIncomeLossAllocatedToGeneralPartners',
            'NetIncomeLossAttributableToCommonStockholders',
            # Additional variations
            'NetIncomeLossAttributableToShareholdersOfParent',
            'ComprehensiveIncomeLossNetOfTax',
            'IncomeLossFromOperationsBeforeIncomeTaxExpenseBenefit',
            'NetIncomeLossAttributableToControllingInterest'
        ],
        'operating_income': [
            'OperatingIncomeLoss',
            'IncomeLossFromOperations',
            'OperatingIncome',
            'IncomeFromOperations',
            'IncomeLossFromContinuingOperationsBeforeIncomeTaxesExtraordinaryItemsNoncontrollingInterest',
            'OperatingProfit',
            'EarningsFromOperations',
            'IncomeLossFromOperatingActivities',
            'OperatingEarnings',
            'IncomeLossFromContinuingOperationsBeforeIncomeTaxesMinorityInterestAndIncomeLossFromEquityMethodInvestments',
            # Additional variations
            'IncomeLossFromOperationsBeforeIncomeTaxExpenseBenefit',
            'OperatingIncomeOrLoss',
            'IncomeLossFromContinuingOperationsBeforeIncomeTaxes'
        ],
        'operating_cash_flow': [
            'NetCashProvidedByUsedInOperatingActivities',
            'CashProvidedByUsedInOperatingActivities',
            'NetCashFromOperatingActivities',
            'OperatingActivitiesNetCashProvidedUsed',
            'CashFlowFromOperatingActivities',
            'NetCashFlowFromOperatingActivities',
            'CashProvidedByOperatingActivities',
            'NetCashProvidedByOperatingActivities',
            'CashGeneratedFromOperatedActivities',
            'CashFlowFromOperatingActivitiesDirectMethod',
            # Additional variations
            'NetCashProvidedByOperatingActivitiesContinuingOperations',
            'CashFlowFromOperatingActivitiesContinuingOperations',
            'NetCashProvidedUsedInOperatingActivities'
        ],
        'capex': [
            'PaymentsToAcquirePropertyPlantAndEquipment',
            'PaymentsForCapitalExpenditures',
            'CapitalExpenditures',
            'PaymentsToAcquireProductiveAssets',
            'PaymentsToAcquireOtherPropertyPlantAndEquipment',
            'AcquisitionOfPropertyPlantAndEquipment',
            'PropertyPlantAndEquipmentAdditions',
            'InvestmentsInPropertyPlantAndEquipment',
            'CapitalExpenditure',
            'PaymentsToAcquirePropertyAndEquipment',
            'PurchaseOfPropertyAndEquipment',
            'PaymentsForProceedsFromPropertyPlantAndEquipment',
            'PaymentsToAcquireBuildings',
            'PaymentsToAcquireMachineryAndEquipment',
            # Additional variations
            'PaymentsToAcquirePropertyPlantAndEquipmentAndOtherAssets',
            'InvestmentInPropertyAndEquipment',
            'CapitalExpendituresIncludingAcquisitions',
            'PaymentsForCapitalImprovements'
        ],
        'equity': [
            # Comprehensive equity tags
            'StockholdersEquity',
            'StockholdersEquityIncludingPortionAttributableToNoncontrollingInterest', 
            'ShareholdersEquity',
            'TotalShareholdersEquity',
            'CommonStockholdersEquity',
            'TotalStockholdersEquity',
            'ShareholdersEquityIncludingNoncontrollingInterest',
            'Equity',
            'EquityAttributableToParent',
            'TotalEquity',
            'PartnersCapital',
            'MembersEquity',
            'PartnersCapitalIncludingPortionAttributableToNoncontrollingInterest',
            'TotalPartnersCapital',
            'ShareholdersEquityAttributableToParent',
            'TotalStockholdersDeficit',  # Can be negative
            'StockholdersDeficit',
            'EquityAttributableToNoncontrollingInterest',
            'EquityIncludingPortionAttributableToNoncontrollingInterest',
            # Additional variations
            'StockholdersEquityAttributableToParent',
            'TotalShareholdersEquityIncludingNoncontrollingInterests',
            'ShareholdersEquityCommonStock'
        ],
        'eps': [
            # Comprehensive EPS tags
            'EarningsPerShareBasic',
            'EarningsPerShareDiluted', 
            'EarningsPerShareBasicAndDiluted',
            'EarningsPerShare',
            'BasicEarningsPerShare',
            'DilutedEarningsPerShare',
            'BasicAndDilutedEarningsPerShare',
            'EarningsPerShareContinuingOperations',
            'EarningsPerShareBasicContinuingOperations',
            'EarningsPerShareDilutedContinuingOperations',
            'IncomeLossFromContinuingOperationsPerBasicShare',
            'IncomeLossFromContinuingOperationsPerDilutedShare',
            'IncomeLossFromContinuingOperationsPerBasicAndDilutedShare',
            'NetIncomeLossPerShareBasic',
            'NetIncomeLossPerShareDiluted',
            'BasicEarningsLossPerShare',
            'DilutedEarningsLossPerShare',
            'EarningsPerShareBasicFromContinuingOperations',
            'EarningsPerShareDilutedFromContinuingOperations',
            # Additional variations
            'NetIncomeLossNetOfTaxPerBasicShare',
            'NetIncomeLossNetOfTaxPerDilutedShare',
            'EarningsPerShareBasicIncludingExtraordinaryItems',
            'EarningsPerShareDilutedIncludingExtraordinaryItems'
        ],
        'debt': [
            'LongTermDebt',
            'LongTermDebtAndCapitalLeaseObligations',
            'LongTermDebtNoncurrent',
            'DebtCurrent',
            'ShortTermBorrowings',
            'LongTermDebtCurrent',
            'Debt',
            'TotalDebt',
            'DebtAndCapitalLeaseObligations',
            'LongTermDebtAndCapitalLeaseObligationsCurrent',
            'LiabilitiesSubjectToCompromise',  # For bankruptcy situations
            'NotesPayable',
            'BankLoansAndNotesPayable',
            'LongTermDebtMaturitiesRepaymentsOfPrincipalInNextTwelveMonths',
            'ShortTermDebtAndCurrentPortionOfLongTermDebt',
            'DebtLongtermAndShorttermCombinedAmount',
            # Additional variations
            'LongTermDebtAndCapitalLeaseObligationsIncludingCurrentMaturities',
            'DebtAndCapitalLeaseObligationsTotal',
            'TotalBorrowings',
            'ShortTermDebtAndCurrentMaturitiesOfLongTermDebt'
        ],
        'assets': [
            'Assets',
            'AssetsCurrent',
            'TotalAssets',
            'AssetsNoncurrent',
            'AssetsNet',
            # Additional variations
            'TotalAssetsExcludingGoodwillAndIntangibleAssets',
            'TotalAssetsIncludingDiscontinuedOperations'
        ],
        'current_liabilities': [
            'LiabilitiesCurrent',
            'CurrentLiabilities',
            'LiabilitiesCurrentTotal',
            # Additional variations
            'TotalCurrentLiabilities',
            'LiabilitiesCurrentAndNoncurrent'
        ],
        'cash': [
            'CashAndCashEquivalentsAtCarryingValue',
            'Cash',
            'CashCashEquivalentsRestrictedCashAndRestrictedCashEquivalents',
            'CashAndEquivalents',
            'CashCashEquivalentsAndShortTermInvestments',
            'RestrictedCashAndCashEquivalents',
            'CashAndShortTermInvestments',
            'CashEquivalentsAndShortTermInvestments',
            'CashAndCashEquivalents',
            # Additional variations
            'CashAndMarketableSecurities',
            'CashCashEquivalentsAndMarketableSecurities',
            'UnrestrictedCashAndCashEquivalents'
        ]
    }

    # Add this after tag_options definition

    best_score = -1  # Add this line to initialize best_score

    
    print(f"\nDEBUG - Analyzing {ticker} data extraction...")
    
    # Try multiple strategies for each metric
    for metric_type, tags in tag_options.items():
        print(f"\n🔍 Searching for {metric_type}...")
        
        # Strategy 1: Try primary tags first
        primary_tags = tags[:5]  # First 5 tags are primary
        best_tag, best_data, score = find_best_tag_by_consistency(
            us_gaap, primary_tags, metric_type, years_range, ticker
        )
        
        # Strategy 2: If no good primary tag, try all tags
        if best_score < 0.3:  # Low score threshold
            print(f"   Primary tags failed, trying all {len(tags)} tags...")
            best_tag, best_data, score = find_best_tag_by_consistency(
                us_gaap, tags, metric_type, years_range, ticker
            )
        
        # Strategy 3: If still no data, try relaxed validation
        if not best_data:
            print(f"   Standard search failed, trying relaxed validation...")
            # Create a copy with relaxed validation ranges
            relaxed_ranges = VALIDATION_RANGES.copy()
            for key in relaxed_ranges:
                min_val, max_val = relaxed_ranges[key]
                relaxed_ranges[key] = (min_val / 1000, max_val * 1000)
            
            # Temporarily use relaxed ranges
            original_ranges = VALIDATION_RANGES.copy()
            VALIDATION_RANGES.update(relaxed_ranges)
            
            best_tag, best_data, score = find_best_tag_by_consistency(
                us_gaap, tags, metric_type, years_range, ticker
            )
            
            # Restore original ranges
            VALIDATION_RANGES.update(original_ranges)
        
        if best_tag and best_data:
            print(f"   ✓ Found: '{best_tag}' with {len(best_data)} years (score: {score:.2f})")
            
            # Additional validation for revenue
            if metric_type == 'revenue' and best_data:
                recent_year = max(best_data.keys())
                recent_value = best_data[recent_year]['value']
                if recent_value < 1e6:  # Less than $1M revenue for public company
                    print(f"   ⚠️  Suspicious revenue value: ${recent_value:,.0f}")
                    # Mark for manual review but still use it
                
            results[metric_type] = best_data
        else:
            print(f"   ❌ No data found for {metric_type}")
            results[metric_type] = {}
    
    return results

def validate_financial_relationships(revenue, net_income, equity, operating_cash_flow, fcf, year):
    """Very flexible validation that accepts most reasonable data"""
    issues = []
    
    if revenue and net_income and revenue != 0:
        net_margin = abs(net_income) / abs(revenue)
        if net_margin > 5.0:
            issues.append(f"Net margin {net_margin:.1%} appears unrealistic")
    
    if net_income and equity and equity != 0:
        roe = (net_income / equity) * 100
        if abs(roe) > 1000:
            issues.append(f"ROE {roe:.1f}% appears extremely high")
    
    # FCF validation
    if operating_cash_flow and fcf:
        if abs(fcf) > abs(operating_cash_flow) * 2:
            issues.append(f"FCF magnitude seems unusually high vs Operating CF")
    
    return issues

def extract_stock_data(ticker, cik):
    """Extract stock data with proper form filtering and date alignment"""
    print(f"\n📊 Extracting {ticker} data (FCF, ROIC, EPS, Revenue, etc.)...")
    
    data, error = get_financial_data_direct(ticker, cik)
    if error:
        print(f"Error: {error}")
        return None
    
    us_gaap = data.get('facts', {}).get('us-gaap', {})
    years_range = (2014, 2024)
    
    # Extract data with proper form filtering and date alignment
    historical_data = extract_historical_data(us_gaap, ticker, years_range)
    
    # Prepare data structure
    extracted_data = {
        'ticker': ticker,
        'financial_metrics': [],
        'data_summary': {},
        'fiscal_calendar_info': {}
    }
    
    for year in range(years_range[0], years_range[1] + 1):
        # Get data entries (now with metadata)
        revenue_entry = historical_data['revenue'].get(year, {})
        net_income_entry = historical_data['net_income'].get(year, {})
        operating_income_entry = historical_data['operating_income'].get(year, {})
        equity_entry = historical_data['equity'].get(year, {})
        eps_entry = historical_data['eps'].get(year, {})
        debt_entry = historical_data['debt'].get(year, {})
        cash_entry = historical_data['cash'].get(year, {})
        operating_cash_flow_entry = historical_data['operating_cash_flow'].get(year, {})
        capex_entry = historical_data['capex'].get(year, {})
        
        # Extract values
        revenue = revenue_entry.get('value') if revenue_entry else None
        net_income = net_income_entry.get('value') if net_income_entry else None
        operating_income = operating_income_entry.get('value') if operating_income_entry else None
        equity = equity_entry.get('value') if equity_entry else None
        eps = eps_entry.get('value') if eps_entry else None
        debt = debt_entry.get('value') if debt_entry else None
        cash = cash_entry.get('value') if cash_entry else None
        operating_cash_flow = operating_cash_flow_entry.get('value') if operating_cash_flow_entry else None
        capex = capex_entry.get('value') if capex_entry else None
        
        # Calculate Free Cash Flow
        fcf = calculate_fcf(operating_cash_flow, capex)
        
        # Get fiscal year info for transparency
        fiscal_year_info = {}
        if revenue_entry:
            fiscal_year_info['revenue_fiscal'] = revenue_entry.get('fiscal_year')
            fiscal_year_info['revenue_end_date'] = revenue_entry.get('end_date')
        if net_income_entry:
            fiscal_year_info['income_fiscal'] = net_income_entry.get('fiscal_year')
            fiscal_year_info['income_end_date'] = net_income_entry.get('end_date')
        
        # Validation
        validation_issues = validate_financial_relationships(revenue, net_income, equity, operating_cash_flow, fcf, year)
        
        # Calculate ratios
        roe = None
        roic_direct = None
        roic_from_roe = None
        roic_method = None
        
        # Calculate ROE
        if net_income is not None and equity is not None and equity != 0:
            roe = (net_income / equity) * 100
        
        # Calculate ROIC using direct method (preferred)
        roic_method = None
        if debt is not None and equity is not None:
            roic_result = calculate_roic_from_components(net_income, debt, equity, operating_income)
            if roic_result:
                roic_direct, roic_method = roic_result
            else:
                roic_direct = None
        
        # Calculate ROIC from ROE (alternative method)
        if roe is not None and debt is not None and equity is not None:
            roic_from_roe = calculate_roic_from_roe(roe, debt, equity)
        
        # Use direct ROIC if available, otherwise use ROIC from ROE
        roic_final = roic_direct if roic_direct is not None else roic_from_roe
        
        extracted_data['financial_metrics'].append({
            'Year': year,
            'Revenue': revenue,
            'NetIncome': net_income,
            'OperatingIncome': operating_income,
            'EPS': eps,
            'ROE': roe,
            'ROIC': roic_final,
            'ROIC_Direct': roic_direct,
            'ROIC_FromROE': roic_from_roe,
            'ROIC_Method': roic_method,
            'TotalDebt': debt,
            'TotalEquity': equity,
            'Cash': cash,
            'OperatingCashFlow': operating_cash_flow,
            'CapEx': capex,
            'FCF': fcf,
            'ValidationIssues': validation_issues,
            'FiscalInfo': fiscal_year_info
        })
    
    # Data summary
    for metric in ['revenue', 'net_income', 'operating_income', 'equity', 'eps', 'debt', 'cash', 'operating_cash_flow', 'capex']:
        extracted_data['data_summary'][metric] = len(historical_data.get(metric, {}))

    
    return extracted_data


def format_value(value, is_percent=False, is_currency=False):
    if value is None:
        return "N/A"
    
    if is_percent:
        return f"{value:.1f}%"
    elif is_currency:
        abs_value = abs(value)
        if abs_value >= 1e12:
            return f"${value/1e12:.2f}T"
        elif abs_value >= 1e9:
            return f"${value/1e9:.1f}B"
        elif abs_value >= 1e6:
            return f"${value/1e6:.1f}M"
        elif abs_value >= 1e3:
            return f"${value/1e3:.1f}K"
        else:
            return f"${value:,.0f}"
    else:
        return f"{value:,.2f}"

def main():
    all_cik = get_all_cik()
    
    # Build the output string
    output_lines = ["STOCK_SCORES = {"]
    
    for ticker in TICKERS:
        cik = get_cik(ticker, all_cik)
        data = extract_stock_data(ticker, cik)
        if data:
            filled_data = get_filled_data(data)
            stability_analysis = analyze_business_stability(filled_data)
            score = round(stability_analysis['score'], 1)
            output_lines.append(f'    "{ticker}": "{score}",')
    
    output_lines.append("}")
    
    # Write everything to file at once
    with open("historical_fundamental_scores.py", "w") as file:
        file.write("\n".join(output_lines))
                
if __name__ == "__main__":
    main()
