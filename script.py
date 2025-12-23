import requests
import random
import time
from datetime import datetime
import os
from bs4 import BeautifulSoup
import historical_fundamental_scores

# Configuration SECOND CODE

STOCKS = [
    "MA", "MSFT", "GOOGL", "SPGI", "PGR", "AXP", "DUOL", "AAPL", "ABBV", "ADBE",
    "ADP", "ADSK", "AME", "AMZN", "ANET", "APH", "APP", "AVGO", "AXON", "AZO",
    "BKNG", "BLK", "BMI", "BRO", "BR", "BRK-B", "BSX", "CB", "CDNS", "CME",
    "CMG", "COST", "CPRT", "CRM", "CSGP", "CTAS", "DHR", "DT", "ECL", "ETN",
    "EW", "FAST", "FICO", "FTNT", "GGG", "GS", "GWW", "HD", "HEI", "HLT",
    "HOLX", "HON", "ICE", "IDXX", "IEX", "INTU", "IR", "ITW", "JPM", "KEYS",
    "LIN", "LMAT", "LOW", "MANH", "MAR", "MCO", "MEDP", "MELI", "META", "MPWR",
    "MS", "MSI", "MKTX", "NFLX", "NDAQ", "NOW", "NVDA", "NVMI", "ONTO", "ORCL",
    "ORLY", "PANW", "PAYC", "PAYX", "PH", "PODD", "PTC", "PWR", "QLYS", "QCOM",
    "REGN", "RMD", "ROP", "ROK", "ROST", "SHW", "SNPS", "SAP", "SYK", "TDG",
    "TDY", "TMO", "TRI", "TRMB", "TSM", "TT", "TXN", "TYL", "V", "VEEV",
    "VRSK", "VRSN", "WDAY", "WST", "WRB", "XYL", "ZTS", "A", "TXRH", "IQV",
    "HUBS", "FISV", "ATKR", "MRVL", "APO", "FDS", "SNA", "CBOE", "ISRG", "IDCC",
    "FIX", "TTD", "SN", "ACGL", "GEV", "MSCI", "MCK", "HIG", "TRV", "MWA",
    "MNST", "VRTX", "UNH", "GEHC", "LLY", "WM", "WSO", "ASML", "VICI", "DPZ",
    "HCA", "KLAC", "AMAT", "MKL", "KNSL", "RLI", "WCN", "AON", "EFX", "JKHY",
    "RYAN", "MORN", "STE", "TSCO", "SSNC", "WAB", "ABT", "LRCX", "GOOG", "PLMR",
    "APPF", "RSG", "MTD", "NDSN", "VRT", "TNET", "ZBRA", "GXO", "AJG", "TECH",
    "ELV", "PNR", "GPN", "FNF", "SEIC", "LPLA", "RNR", "ALLE", "ODFL", "CHDN",
    "NVO", "WING", "EXLS", "EEFT", "AX", "UHS", "EPAM", "ICLR", "GHC", "SAIA",
    "RACE", "WDFC", "CW", "WAT", "CLH", "HCI", "NSSC", "NMIH", "CVCO", "IRMD",
    "AWK", "DXCM", "SPSC", "POOL", "FERG", "CACI", "LDOS", "DDOG", "MNDY", "NET",
    "DECK", "LULU", "CROX", "ERIE", "ULTA", "UBER", "NTES", "ESQ", "CPRX", "EME",
    "KO", "PG", "MCD", "PEP", "CHD", "ROL"
]

def calculate_dividend_score(metrics, sector, stock_symbol):
    """
    Calculate Dividend Safety & Quality Score (0-10)
    
    Components:
    1. Payout Ratio (35%) - Lower is safer, sector-adjusted
    2. Dividend Growth (30%) - Consistent growth = quality
    3. Dividend Yield (20%) - Reasonable yield (not too high/low)
    4. FCF Coverage (15%) - Can company afford dividend?
    
    Returns dict with score, rating, and breakdown
    """
    
    payout_ratio = metrics.get('Payout_Ratio')
    div_growth_3_5y = metrics.get('Dividend_Growth_3_5Y')
    div_ttm = metrics.get('Dividend_TTM')
    div_est = metrics.get('Dividend_Est')
    price = metrics.get('Price')
    fcf_per_share = metrics.get('FCF_per_share')
    
    # IMPROVED: Check if stock pays dividend more defensively
    has_dividend = False
    
    # Check multiple indicators for dividend
    if div_ttm is not None and div_ttm > 0:
        has_dividend = True
    elif div_est is not None and div_est > 0:
        has_dividend = True
        div_ttm = div_est  # Use estimate if TTM not available
    elif payout_ratio is not None and payout_ratio > 0:
        has_dividend = True  # Has payout ratio means it pays dividend
    
    if not has_dividend:
        return {
            'dividend_score': None,
            'dividend_rating': 'No Dividend',
            'dividend_icon': '—',
            'dividend_yield': 0,
            'components': {
                'payout_safety': None,
                'growth_consistency': None,
                'yield_quality': None,
                'fcf_coverage': None
            }
        }
    
    # Calculate current yield (handle None values)
    div_yield = 0
    if div_ttm and price and price > 0:
        div_yield = (div_ttm / price * 100)
    elif div_est and price and price > 0:
        div_yield = (div_est / price * 100)
    
    # If we still don't have a yield but have payout ratio, it's a data issue
    if div_yield == 0 and payout_ratio and payout_ratio > 0:
        # We know they pay dividend but can't calculate yield - return partial data
        return {
            'dividend_score': None,
            'dividend_rating': 'Insufficient Data',
            'dividend_icon': '❓',
            'dividend_yield': 0,
            'components': {
                'payout_safety': None,
                'growth_consistency': None,
                'yield_quality': None,
                'fcf_coverage': None
            }
        }
    
    div_components = []
    
    # ========== 1. PAYOUT RATIO SAFETY (35%) ==========
    payout_score = 5.0
    
    if payout_ratio is not None:
        # Sector-adjusted payout thresholds
        if sector in ['Utilities', 'Real Estate', 'Consumer Defensive']:
            # Mature sectors: Higher payout acceptable
            if payout_ratio < 40:
                payout_score = 10.0
            elif payout_ratio < 55:
                payout_score = 9.0
            elif payout_ratio < 70:
                payout_score = 8.0
            elif payout_ratio < 80:
                payout_score = 6.5
            elif payout_ratio < 90:
                payout_score = 4.0
            else:
                payout_score = 2.0
        
        elif sector in ['Technology', 'Healthcare', 'Communication Services']:
            # Growth sectors: Lower payout preferred
            if payout_ratio < 20:
                payout_score = 10.0
            elif payout_ratio < 35:
                payout_score = 9.0
            elif payout_ratio < 50:
                payout_score = 7.5
            elif payout_ratio < 70:
                payout_score = 5.0
            elif payout_ratio < 85:
                payout_score = 3.0
            else:
                payout_score = 1.5
        
        elif sector == 'Financial':
            # Financials: Different dynamics
            if payout_ratio < 30:
                payout_score = 10.0
            elif payout_ratio < 45:
                payout_score = 9.0
            elif payout_ratio < 60:
                payout_score = 7.5
            elif payout_ratio < 75:
                payout_score = 5.5
            else:
                payout_score = 3.0
        
        else:
            # Standard sectors
            if payout_ratio < 30:
                payout_score = 10.0
            elif payout_ratio < 45:
                payout_score = 9.0
            elif payout_ratio < 60:
                payout_score = 7.5
            elif payout_ratio < 75:
                payout_score = 5.5
            elif payout_ratio < 90:
                payout_score = 3.5
            else:
                payout_score = 2.0
    
    div_components.append(('Payout_Safety', payout_score, 0.35))
    
    # ========== 2. DIVIDEND GROWTH CONSISTENCY (30%) ==========
    growth_score = 5.0
    
    if div_growth_3_5y is not None:
        if div_growth_3_5y >= 15:
            growth_score = 10.0  # Dividend aristocrat territory
        elif div_growth_3_5y >= 12:
            growth_score = 9.5
        elif div_growth_3_5y >= 10:
            growth_score = 9.0
        elif div_growth_3_5y >= 8:
            growth_score = 8.5
        elif div_growth_3_5y >= 6:
            growth_score = 8.0
        elif div_growth_3_5y >= 4:
            growth_score = 7.0
        elif div_growth_3_5y >= 2:
            growth_score = 6.0
        elif div_growth_3_5y >= 0:
            growth_score = 5.0
        elif div_growth_3_5y >= -3:
            growth_score = 3.5  # Declining but stable
        else:
            growth_score = 2.0  # Dividend cuts
    
    div_components.append(('Growth_Consistency', growth_score, 0.30))
    
    # ========== 3. YIELD QUALITY (20%) ==========
    yield_score = 5.0
    
    # Sweet spot: 2-6% for most sectors
    # Too low = token dividend, Too high = unsustainable
    
    if sector in ['Utilities', 'Real Estate']:
        # High-yield sectors
        if 4.0 <= div_yield <= 7.0:
            yield_score = 10.0
        elif 3.0 <= div_yield < 4.0 or 7.0 < div_yield <= 8.5:
            yield_score = 8.5
        elif 2.5 <= div_yield < 3.0 or 8.5 < div_yield <= 10:
            yield_score = 7.0
        elif div_yield < 2.5:
            yield_score = 5.0
        else:  # > 10%
            yield_score = 3.0  # Danger zone
    
    elif sector in ['Technology', 'Healthcare']:
        # Lower-yield growth sectors
        if 1.5 <= div_yield <= 3.5:
            yield_score = 10.0
        elif 1.0 <= div_yield < 1.5 or 3.5 < div_yield <= 5.0:
            yield_score = 8.5
        elif 0.5 <= div_yield < 1.0 or 5.0 < div_yield <= 6.5:
            yield_score = 7.0
        elif div_yield < 0.5:
            yield_score = 4.0  # Token dividend
        else:  # > 6.5%
            yield_score = 4.0  # Unsustainable for growth sector
    
    else:
        # Standard sectors
        if 2.5 <= div_yield <= 5.0:
            yield_score = 10.0
        elif 2.0 <= div_yield < 2.5 or 5.0 < div_yield <= 6.0:
            yield_score = 8.5
        elif 1.5 <= div_yield < 2.0 or 6.0 < div_yield <= 7.5:
            yield_score = 7.0
        elif div_yield < 1.5:
            yield_score = 5.0
        else:  # > 7.5%
            yield_score = 3.5  # Warning territory
    
    div_components.append(('Yield_Quality', yield_score, 0.20))
    
    # ========== 4. FCF COVERAGE (15%) ==========
    fcf_coverage_score = 5.0
    
    if fcf_per_share and fcf_per_share > 0 and div_ttm and div_ttm > 0:
        fcf_coverage_ratio = fcf_per_share / div_ttm
        
        if fcf_coverage_ratio >= 3.0:
            fcf_coverage_score = 10.0  # Very safe
        elif fcf_coverage_ratio >= 2.5:
            fcf_coverage_score = 9.5
        elif fcf_coverage_ratio >= 2.0:
            fcf_coverage_score = 9.0
        elif fcf_coverage_ratio >= 1.5:
            fcf_coverage_score = 8.0
        elif fcf_coverage_ratio >= 1.3:
            fcf_coverage_score = 7.0
        elif fcf_coverage_ratio >= 1.1:
            fcf_coverage_score = 6.0
        elif fcf_coverage_ratio >= 1.0:
            fcf_coverage_score = 4.5  # Barely covered
        elif fcf_coverage_ratio >= 0.8:
            fcf_coverage_score = 3.0  # Warning
        else:
            fcf_coverage_score = 1.5  # Unsustainable
    
    div_components.append(('FCF_Coverage', fcf_coverage_score, 0.15))
    
    # ========== CALCULATE FINAL DIVIDEND SCORE ==========
    dividend_score = sum(score * weight for _, score, weight in div_components)
    dividend_score = min(max(0, dividend_score), 10)
    
    # Dividend rating
    if dividend_score >= 9.0:
        dividend_rating = "Dividend Aristocrat"
        dividend_icon = "👑"
    elif dividend_score >= 8.0:
        dividend_rating = "Excellent"
        dividend_icon = "💎"
    elif dividend_score >= 7.0:
        dividend_rating = "Very Good"
        dividend_icon = "✅"
    elif dividend_score >= 6.0:
        dividend_rating = "Good"
        dividend_icon = "👍"
    elif dividend_score >= 5.0:
        dividend_rating = "Fair"
        dividend_icon = "⚖️"
    elif dividend_score >= 4.0:
        dividend_rating = "Caution"
        dividend_icon = "⚠️"
    else:
        dividend_rating = "At Risk"
        dividend_icon = "🚨"
    
    return {
        'dividend_score': round(dividend_score, 2),
        'dividend_rating': dividend_rating,
        'dividend_icon': dividend_icon,
        'dividend_yield': round(div_yield, 2),
        'components': {
            'payout_safety': round(payout_score, 1),
            'growth_consistency': round(growth_score, 1),
            'yield_quality': round(yield_score, 1),
            'fcf_coverage': round(fcf_coverage_score, 1)
        }
    }

def calculate_moat_score(metrics, sector, stock_symbol, historical_score):
    """Calculate Long-Term Moat Score (0-10)"""
    
    moat_components = []
    
    # 1. ROIC PERSISTENCE (30%)
    roic = metrics.get('ROIC')
    roe = metrics.get('ROE')
    roic_persistence_score = 5.0
    
    if roic is not None:
        if roic >= 50:      roic_persistence_score = 10.0
        elif roic >= 40:    roic_persistence_score = 9.8
        elif roic >= 35:    roic_persistence_score = 9.5
        elif roic >= 30:    roic_persistence_score = 9.0
        elif roic >= 25:    roic_persistence_score = 8.5
        elif roic >= 22:    roic_persistence_score = 8.0
        elif roic >= 20:    roic_persistence_score = 7.5
        elif roic >= 18:    roic_persistence_score = 7.0
        elif roic >= 15:    roic_persistence_score = 6.5
        elif roic >= 12:    roic_persistence_score = 5.5
        else:               roic_persistence_score = 4.5
        
        if historical_score is not None and historical_score >= 8.0 and roic >= 20:
            roic_persistence_score = min(10, roic_persistence_score + 1.0)
    
    elif roe is not None:
        if roe >= 45:       roic_persistence_score = 8.0
        elif roe >= 30:     roic_persistence_score = 7.0
        elif roe >= 20:     roic_persistence_score = 6.0
        else:               roic_persistence_score = 4.0
    
    moat_components.append(('ROIC_Persistence', roic_persistence_score, 0.30))
    
    # 2. MARGIN STABILITY (25%)
    profit_margin = metrics.get('Profit_Margin')
    gross_margin = metrics.get('Gross_Margin')
    margin_stability_score = 5.0
    
    if profit_margin is not None:
        if profit_margin >= 40:    margin_stability_score = 10.0
        elif profit_margin >= 30:  margin_stability_score = 9.0
        elif profit_margin >= 25:  margin_stability_score = 8.5
        elif profit_margin >= 20:  margin_stability_score = 8.0
        elif profit_margin >= 15:  margin_stability_score = 7.0
        elif profit_margin >= 10:  margin_stability_score = 6.0
        else:                      margin_stability_score = 4.0
        
        if gross_margin and gross_margin >= 80:
            margin_stability_score = min(10, margin_stability_score + 1.5)
    
    moat_components.append(('Margin_Stability', margin_stability_score, 0.25))
    
    # 3. HISTORICAL CONSISTENCY (20%)
    historical_consistency_score = 5.0
    if historical_score is not None:
        if historical_score >= 9.0:     historical_consistency_score = 10.0
        elif historical_score >= 8.0:   historical_consistency_score = 9.0
        elif historical_score >= 7.0:   historical_consistency_score = 8.0
        elif historical_score >= 6.0:   historical_consistency_score = 7.0
        else:                           historical_consistency_score = 5.0
    
    moat_components.append(('Historical_Consistency', historical_consistency_score, 0.20))
    
    # 4. CAPITAL EFFICIENCY (15%)
    fcf_per_share = metrics.get('FCF_per_share')
    eps_ttm = metrics.get('EPS_TTM')
    capital_efficiency_score = 5.0
    
    if fcf_per_share and eps_ttm and eps_ttm > 0:
        fcf_conversion = fcf_per_share / eps_ttm
        if fcf_conversion >= 1.4:       capital_efficiency_score = 10.0
        elif fcf_conversion >= 1.2:     capital_efficiency_score = 9.0
        elif fcf_conversion >= 1.0:     capital_efficiency_score = 8.0
        elif fcf_conversion >= 0.85:    capital_efficiency_score = 7.0
        elif fcf_conversion >= 0.70:    capital_efficiency_score = 6.0
        else:                           capital_efficiency_score = 4.0
    
    moat_components.append(('Capital_Efficiency', capital_efficiency_score, 0.15))
    
    # 5. MARKET POSITION (10%)
    market_cap = metrics.get('Market_Cap')
    market_position_score = 5.0
    
    if market_cap is not None:
        if market_cap >= 500:       market_position_score = 10.0
        elif market_cap >= 200:     market_position_score = 9.0
        elif market_cap >= 100:     market_position_score = 8.0
        elif market_cap >= 50:      market_position_score = 7.5
        elif market_cap >= 20:      market_position_score = 7.0
        else:                       market_position_score = 6.0
    
    moat_components.append(('Market_Position', market_position_score, 0.10))
    
    # CALCULATE FINAL MOAT SCORE
    moat_score = sum(score * weight for _, score, weight in moat_components)
    moat_score = min(max(0, moat_score), 10)
    
    # Moat rating
    if moat_score >= 9.0:
        moat_rating = "Fortress"
        moat_icon = "🏰"
    elif moat_score >= 8.0:
        moat_rating = "Wide Moat"
        moat_icon = "🛡️"
    elif moat_score >= 7.0:
        moat_rating = "Narrow"
        moat_icon = "🔒"
    elif moat_score >= 6.0:
        moat_rating = "Weak"
        moat_icon = "⚠️"
    else:
        moat_rating = "No Moat"
        moat_icon = "❌"
    
    return {
        'moat_score': round(moat_score, 2),
        'moat_rating': moat_rating,
        'moat_icon': moat_icon,
        'moat_components': {
            'roic_persistence': round(roic_persistence_score, 1),
            'margin_stability': round(margin_stability_score, 1),
            'historical_consistency': round(historical_consistency_score, 1),
            'capital_efficiency': round(capital_efficiency_score, 1),
            'market_position': round(market_position_score, 1)
        }
    }

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

def is_investment_phase(metrics):
    """Detect high-growth companies in investment mode"""
    sales_5y = metrics.get('Sales_past_5Y')
    eps_5y = metrics.get('EPS_past_5Y')
    fcf_per_share = metrics.get('FCF_per_share')
    eps_ttm = metrics.get('EPS_TTM')
    
    # High growth + lower FCF conversion = investing for future
    if sales_5y and sales_5y > 15 and eps_5y and eps_5y > 12:
        if fcf_per_share and eps_ttm and eps_ttm > 0:
            conversion = fcf_per_share / eps_ttm
            if 0.40 <= conversion < 0.75:
                return True
    return False

def calculate_peg_score_improved(peg, is_elite=False, actual_growth=None):
    """
    Peter Lynch PEG scoring with research-accurate thresholds
    
    KEY RESEARCH FINDING:
    - PEG = 1.0 is FAIR VALUE (not expensive!)
    - PEG 1.0-2.0 = acceptable range for quality companies
    - PEG > 2.0 = starting to be overvalued
    """
    if peg <= 0:
        return 1.0
    
    # BARGAIN ZONE (PEG < 1.0)
    if peg < 0.5:
        return 10.0 if actual_growth and actual_growth > 25 else 8.5
    elif 0.5 <= peg < 0.75:
        return 10.0
    elif 0.75 <= peg < 1.0:
        return 9.5
    
    # FAIR VALUE ZONE (PEG 1.0-2.0) - CRITICAL CHANGE
    elif 1.0 <= peg < 1.15:
        return 9.0  # ← Was 7.5, now 9.0 (fair value!)
    elif 1.15 <= peg < 1.3:
        return 8.5  # ← New tier
    elif 1.3 <= peg < 1.5:
        return 8.0  # ← Was 6.0, now 8.0
    elif 1.5 <= peg < 1.7:
        return 7.5  # ← Was 4.5, now 7.5 (GOOGL fix)
    elif 1.7 <= peg < 1.9:
        return 7.0
    elif 1.9 <= peg < 2.0:
        return 6.5
    
    # EXPENSIVE ZONE (PEG 2.0-3.0)
    elif 2.0 <= peg < 2.2:
        base_score = 5.5
        if is_elite:
            base_score = min(6.5, base_score + 1.0)
        return base_score
    
    elif 2.2 <= peg < 2.5:
        base_score = 4.5  # ← MSFT 2.30 lands here
        if is_elite:
            base_score = min(5.5, base_score + 1.0)
        return base_score
    
    elif 2.5 <= peg < 3.0:
        base_score = 3.5
        if is_elite:
            base_score = min(4.5, base_score + 1.0)
        return base_score
    
    # BUBBLE ZONE (PEG > 3.0)
    elif 3.0 <= peg < 4.0:
        base_score = 2.5
        if is_elite:
            base_score = min(3.5, base_score + 0.5)
        return base_score
    
    else:  # PEG >= 4.0
        return 1.5


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

def calculate_trust_factor(stock_symbol):
    return historical_fundamental_scores.TRUST_SCORES[stock_symbol]


def calculate_piotroski_fscore(metrics):
    """
    Calculate Piotroski F-Score (0-9)
    
    ⚠️ LIMITATION: Original Piotroski uses year-over-year CHANGES
    Without historical data, we use:
        - Absolute levels (ROA > 0, instead of ΔROA > 0)
        - Proxy metrics (profit margin trend, instead of actual Δmargin)
    
    ACCURACY: ~60-70% of original F-Score predictive power
    
    Profitability (4 points):
    1. ROA > 0
    2. Operating Cash Flow > 0
    3. Change in ROA (proxy: increasing profit margin)
    4. Quality of earnings: CFO > Net Income
    
    Leverage/Liquidity (3 points):
    5. Decreasing leverage (low D/E)
    6. Increasing liquidity (current ratio)
    7. No new shares issued
    
    Operating Efficiency (2 points):
    8. Increasing gross margin
    9. Increasing asset turnover
    """
    score = 0
    
    # 1. Positive ROA
    roa = metrics.get('ROA')
    if roa and roa > 0:
        score += 1
    
    # 2. Positive Operating Cash Flow (proxy: FCF_per_share > 0)
    fcf = metrics.get('FCF_per_share')
    if fcf and fcf > 0:
        score += 1
    
    # 3. Change in ROA (proxy: profit margin + eps growth)
    profit_margin = metrics.get('Profit_Margin')
    eps_yoy = metrics.get('EPS_YoY_TTM')
    if profit_margin and profit_margin > 15 and eps_yoy and eps_yoy > 0:
        score += 1
    
    # 4. Quality of earnings: FCF > Net Income
    eps_ttm = metrics.get('EPS_TTM')
    if fcf and eps_ttm and eps_ttm > 0:
        if (fcf / eps_ttm) > 1.0:
            score += 1
    
    # 5. Decreasing leverage (low debt)
    debt_eq = metrics.get('Debt/Eq')
    if debt_eq is not None and debt_eq < 0.5:
        score += 1
    
    # 6. Increasing liquidity (good current ratio)
    current_ratio = metrics.get('Current_Ratio')
    if current_ratio and current_ratio >= 1.5:
        score += 1
    
    # 7. No new shares (proxy: low debt + high ROE)
    roe = metrics.get('ROE')
    if roe and roe > 20 and debt_eq is not None and debt_eq < 0.5:
        score += 1
    
    # 8. Increasing gross margin (high absolute = proxy)
    gross_margin = metrics.get('Gross_Margin')
    if gross_margin and gross_margin > 40:
        score += 1
    
    # 9. Asset turnover (proxy: high ROA)
    if roa and roa > 10:
        score += 1
    
    return score  # Returns 0-9

def calculate_combined_performance_scores(metrics, sector, stock_symbol, 
                                         scores_greenblatt, scores_peter_lynch,
                                         scores_piotroski, scores_fama, scores_buffett):
    """
    Calculate performance-weighted combined scores
    Weights based on historical CAGR:
    - Greenblatt: 30% (30.8% CAGR)
    - Lynch: 28% (29.2% CAGR)
    - Piotroski: 20% (23.0% CAGR)
    - Fama-French: 12% (13.0% CAGR)
    - Buffett: Small adjustment weight
    """
    
    PERFORMANCE_WEIGHTS = {
        'greenblatt': 0.30,   # 30.8% CAGR (1988-2004) - HIGHEST
        'lynch': 0.28,        # 29.2% CAGR (1977-1990) - SECOND
        'piotroski': 0.20,    # 7.5% annual outperformance
        'fama': 0.12,         # Academic validation, but lower absolute returns
        'buffett': 0.10       # Long-term (20%+ CAGR but over 50+ years)
    }
        
    # Check if all component scores exist
    if not all([scores_greenblatt, scores_peter_lynch, scores_piotroski, 
                scores_fama, scores_buffett]):
        return None
    
    # Calculate weighted scores
    combined_valuation = (
        scores_greenblatt['valuation_score'] * PERFORMANCE_WEIGHTS['greenblatt'] +
        scores_peter_lynch['valuation_score'] * PERFORMANCE_WEIGHTS['lynch'] +
        scores_piotroski['valuation_score'] * PERFORMANCE_WEIGHTS['piotroski'] +
        scores_fama['valuation_score'] * PERFORMANCE_WEIGHTS['fama'] +
        scores_buffett['valuation_score'] * PERFORMANCE_WEIGHTS['buffett']
    )
    
    combined_quality = (
        scores_greenblatt['quality_score'] * PERFORMANCE_WEIGHTS['greenblatt'] +
        scores_peter_lynch['quality_score'] * PERFORMANCE_WEIGHTS['lynch'] +
        scores_piotroski['quality_score'] * PERFORMANCE_WEIGHTS['piotroski'] +
        scores_fama['quality_score'] * PERFORMANCE_WEIGHTS['fama'] +
        scores_buffett['quality_score'] * PERFORMANCE_WEIGHTS['buffett']
    )
    
    combined_growth = (
        scores_greenblatt['growth_score'] * PERFORMANCE_WEIGHTS['greenblatt'] +
        scores_peter_lynch['growth_score'] * PERFORMANCE_WEIGHTS['lynch'] +
        scores_piotroski['growth_score'] * PERFORMANCE_WEIGHTS['piotroski'] +
        scores_fama['growth_score'] * PERFORMANCE_WEIGHTS['fama'] +
        scores_buffett['growth_score'] * PERFORMANCE_WEIGHTS['buffett']
    )
    
    combined_historical = None
    if all([s.get('historical_score') for s in [scores_greenblatt, scores_peter_lynch, 
                                                  scores_piotroski, scores_fama, scores_buffett]]):
        combined_historical = (
            scores_greenblatt['historical_score'] * PERFORMANCE_WEIGHTS['greenblatt'] +
            scores_peter_lynch['historical_score'] * PERFORMANCE_WEIGHTS['lynch'] +
            scores_piotroski['historical_score'] * PERFORMANCE_WEIGHTS['piotroski'] +
            scores_fama['historical_score'] * PERFORMANCE_WEIGHTS['fama'] +
            scores_buffett['historical_score'] * PERFORMANCE_WEIGHTS['buffett']
        )

    trust_factor = scores_greenblatt.get('trust_factor')
    
    # Calculate total score using weighted averages
    # Use the base weights from combined_performance profile
    profile = RESEARCH_PROFILES['combined_performance']
    weights = profile['base_weights']
    
    total_score = (
        combined_valuation * weights['valuation'] +
        combined_quality * weights['quality'] +
        combined_growth * weights['growth']
    )
    
    if combined_historical is not None:
        total_score += combined_historical * weights['historical']
    
    return {
        'valuation_score': round(combined_valuation, 2),
        'quality_score': round(combined_quality, 2),
        'stability_score': None,
        'growth_score': round(combined_growth, 2),
        'historical_score': combined_historical,
        'trust_factor': trust_factor,  # ✅ ADD THIS LINE
        'total_score': round(total_score, 2),
        'sector': sector,
        'sector_config_used': scores_greenblatt['sector_config_used'],
        'valuation_components': [],
        'quality_components': [],
        'stability_components': [],
        'growth_components': [],
        'red_flags': [],
        'warnings': [],
        'sector_adjustments': scores_greenblatt['sector_adjustments'],
        'research_insights': {
            'model_version': 'Combined Performance-Weighted v1.0',
            'active_profile': profile['name'],
            'profile_description': profile['description'],
            'methodology': f"Weighted blend: Greenblatt {PERFORMANCE_WEIGHTS['greenblatt']*100:.0f}%, Lynch {PERFORMANCE_WEIGHTS['lynch']*100:.0f}%, Piotroski {PERFORMANCE_WEIGHTS['piotroski']*100:.0f}%, Fama {PERFORMANCE_WEIGHTS['fama']*100:.0f}%, Buffett {PERFORMANCE_WEIGHTS['buffett']*100:.0f}%",
            'weight_breakdown': f"Quality: {weights['quality']*100:.0f}%, Growth: {weights['growth']*100:.0f}%, Valuation: {weights['valuation']*100:.0f}%, Historical: {weights['historical']*100:.0f}%",
            'quality_focus': 'Balanced approach combining value, quality, and growth factors',
            'growth_hierarchy': 'Weighted consensus from top-performing strategies',
            'key_finding': 'Diversified strategy reduces single-model risk',
            'historical_persistence': 'Validation layer from proven long-term performers',
            'valuation_role': 'Strong emphasis from Magic Formula and Lynch PEG approach'
        }
    }

def create_quad_profile_html(stock_data_academic, stock_data_growth, 
                            stock_data_fama,
                            stock_data_magic_piotroski, stock_data_peter_lynch,
                            stock_data_piotroski, stock_data_greenblatt,
                            stock_data_buffett, stock_data_combined):
    """Generate HTML report with ALL 9 research profiles embedded"""
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    
    try:
        with open(HTML_FILE, 'r', encoding='utf-8') as f:
            html_content = f.read()
    except IOError as e:
        print(f"❌ Error reading HTML file: {e}")
        return
    
    print("   📄 HTML file loaded successfully")
    
    # Generate table rows for ALL 9 profiles
    print("\n   🎓 Generating ACADEMIC profile HTML...")
    academic_rows = create_enhanced_html(stock_data_academic, 'academic')
    
    print("   📈 Generating GROWTH-BASED profile HTML...")
    growth_rows = create_enhanced_html(stock_data_growth, 'growth_based')
    
    print("   🏛️ Generating FAMA-FRENCH profile HTML...")
    fama_rows = create_enhanced_html(stock_data_fama, 'fama_french')
    
    print("   🎯 Generating MAGIC+PIOTROSKI profile HTML...")
    magic_piotroski_rows = create_enhanced_html(stock_data_magic_piotroski, 'magic_piotroski')
    
    print("   📊 Generating PETER LYNCH profile HTML...")
    peter_lynch_rows = create_enhanced_html(stock_data_peter_lynch, 'peter_lynch')
    
    print("   ✅ Generating PIOTROSKI profile HTML...")
    piotroski_rows = create_enhanced_html(stock_data_piotroski, 'piotroski')
    
    print("   ⚡ Generating GREENBLATT MAGIC profile HTML...")
    greenblatt_rows = create_enhanced_html(stock_data_greenblatt, 'greenblatt_magic')
    
    print("   🏰 Generating BUFFETT QUALITY profile HTML...")
    buffett_rows = create_enhanced_html(stock_data_buffett, 'buffett_quality')

    print("   🎯 Generating COMBINED PERFORMANCE profile HTML...")
    combined_rows = create_enhanced_html(stock_data_combined, 'combined_performance')
    
    # Create 9-profile table body
    quad_tbody = f'''<tbody id="stockTableBody">
        <!-- ACADEMIC PROFILE ROWS (50% Quality) -->
{academic_rows}
        <!-- GROWTH PROFILE ROWS (40% Growth) -->
{growth_rows}
        <!-- FAMA-FRENCH PROFILE ROWS (40% Quality + 25% Value) -->
{fama_rows}
        <!-- MAGIC+PIOTROSKI PROFILE ROWS (60% Quality + 25% Value) -->
{magic_piotroski_rows}
        <!-- PETER LYNCH PROFILE ROWS (40% Growth + 35% Value) -->
{peter_lynch_rows}
        <!-- PIOTROSKI PROFILE ROWS (70% Quality) -->
{piotroski_rows}
        <!-- GREENBLATT MAGIC PROFILE ROWS (50% Quality + 50% Value) -->
{greenblatt_rows}
        <!-- BUFFETT QUALITY PROFILE ROWS (60% Quality + 25% Historical) -->
{buffett_rows}
    <!-- COMBINED PERFORMANCE PROFILE ROWS (Performance-Weighted Blend) -->
{combined_rows}
    </tbody>'''
    
    import re
    pattern = r'<tbody id="stockTableBody">.*?</tbody>'
    
    if not re.search(pattern, html_content, flags=re.DOTALL):
        print("   ❌ ERROR: Could not find <tbody id='stockTableBody'> in HTML!")
        return
    
    html_content = re.sub(pattern, quad_tbody, html_content, flags=re.DOTALL)
    
    # Update timestamp
    timestamp_pattern = r'<div class="timestamp"[^>]*>.*?</div>'
    timestamp_replacement = f'''<div class="timestamp" style="color: #ffffff; background: rgba(255, 255, 255, 0.15); padding: 10px 15px; border-radius: 8px; text-align: right; margin-top: 20px; backdrop-filter: blur(5px);">
        ⏰ Last updated: {timestamp}<br>
    </div>'''
    
    if re.search(timestamp_pattern, html_content, flags=re.DOTALL):
        html_content = re.sub(timestamp_pattern, timestamp_replacement, html_content, flags=re.DOTALL)
    
    # Write updated HTML
    try:
        with open(HTML_FILE, 'w', encoding='utf-8') as f:
            f.write(html_content)
        print(f"\n✅ Successfully wrote {HTML_FILE}")
        print(f"📊 All 10 research profiles embedded")
        print(f"🔄 Total stocks analyzed: {len(stock_data_academic)}")
    except IOError as e:
        print(f"❌ Error writing HTML file: {e}")


def calculate_greenblatt_roic(metrics):
    """
    Greenblatt Magic Formula ROIC approximation
    
    Formula: ROIC = EBIT / Tangible Capital
    
    Since Finviz lacks balance sheet details:
    1. Adjust for financial leverage (debt penalty if high)
    2. Conservative estimate if no ROIC data
    """
    roic = metrics.get('ROIC')
    debt_eq = metrics.get('Debt/Eq')
    oper_margin = metrics.get('Oper_Margin')
    profit_margin = metrics.get('Profit_Margin')
    roe = metrics.get('ROE')
    
    if roic is not None:
        # Greenblatt excludes excess cash and goodwill
        if debt_eq is not None and debt_eq < 0.2:
            adjusted_roic = roic * 1.0  # Low debt = minimal adjustment
        elif debt_eq is not None and debt_eq > 1.0:
            adjusted_roic = roic * 0.95  # High debt = slight downward adjustment
        else:
            adjusted_roic = roic
        
        return adjusted_roic
    
    # Fallback: estimate from ROE and operating margin
    elif roe is not None and oper_margin is not None:
        if debt_eq is not None and debt_eq > 0:
            estimated_roic = roe / (1 + debt_eq) * (oper_margin / profit_margin if profit_margin else 1.0)
        else:
            estimated_roic = roe * 0.8
        
        return estimated_roic
    
    return None


def generate_table_rows(stock_data, profile_name):
    """Generate table rows for a specific profile"""
    # Sort stocks by total score
    sorted_data = sorted(
        [(stock, metrics, scores, sector) for stock, metrics, scores, sector in stock_data if metrics and scores],
        key=lambda x: x[2]['total_score'],
        reverse=True
    )
    
    table_rows = []
    for stock, metrics, scores, sector in sorted_data:
        # Determine CSS classes
        valuation_class = "positive" if scores['valuation_score'] >= 7 else "neutral" if scores['valuation_score'] >= 5 else "negative"
        quality_class = "positive" if scores['quality_score'] >= 7 else "neutral" if scores['quality_score'] >= 5 else "negative"
        growth_class = "positive" if scores['growth_score'] >= 7 else "neutral" if scores['growth_score'] >= 5 else "negative"
        total_class = "positive" if scores['total_score'] >= 7 else "neutral" if scores['total_score'] >= 5.5 else "negative"
        historical_class = "positive" if scores.get('historical_score') and scores['historical_score'] >= 7 else "neutral" if scores.get('historical_score') and scores['historical_score'] >= 5 else "negative" if scores.get('historical_score') else "na"
        
        # Format displays
        pe_display = f"{metrics['PE']:.1f}" if metrics['PE'] is not None else "N/A"
        forward_pe_display = f"{metrics['Forward_PE']:.1f}" if metrics['Forward_PE'] is not None else "N/A"
        peg_display = f"{metrics['PEG']:.2f}" if metrics['PEG'] is not None else "N/A"
        sales_5y = f"{metrics['Sales_past_5Y']:.1f}%" if metrics['Sales_past_5Y'] is not None else "N/A"
        eps_5y = f"{metrics['EPS_past_5Y']:.1f}%" if metrics['EPS_past_5Y'] is not None else "N/A"
        fcf_display = f"${metrics['FCF_per_share']:.2f}" if metrics['FCF_per_share'] is not None else "N/A"
        fcf_yield_display = f"{metrics['FCF_Yield']:.1f}%" if metrics['FCF_Yield'] is not None else "N/A"
        historical_display = f"{scores['historical_score']:.1f}" if scores.get('historical_score') is not None else "N/A"
        
        recent_growth = ""
        if metrics['EPS_YoY_TTM'] is not None and metrics['Sales_YoY_TTM'] is not None:
            recent_growth = f"EPS: {metrics['EPS_YoY_TTM']:+.1f}% | Sales: {metrics['Sales_YoY_TTM']:+.1f}%"
        
        # CRITICAL: Add profile class to EVERY row
        profile_class = f"profile-{profile_name}"
        
        # Create table row with profile-specific class and ID
        table_rows.append(f'''
            <tr class="stock-row {profile_class}" data-profile="{profile_name}" data-sector="{sector}" data-valuation="{scores['valuation_score']:.1f}" data-growth="{scores['growth_score']:.1f}" data-stock="{stock}" onclick="toggleDetails('{stock}', '{profile_name}')">
                <td><strong>{stock}</strong><br><small>${metrics['Price']:.2f}</small><br><small style="color: #666;">{sector}</small></td>
                <td>{pe_display}<br><small>Fwd: {forward_pe_display}</small></td>
                <td>{peg_display}</td>
                <td>{f"{metrics['Debt/Eq']:.2f}" if metrics['Debt/Eq'] is not None else "N/A"}<br>
                    <small>{f"{metrics['Current_Ratio']:.1f}" if metrics['Current_Ratio'] is not None else "N/A"}</small></td>
                <td class="hidden-mobile">{f"{metrics['ROE']:.1f}%" if metrics['ROE'] is not None else "N/A"}<br>
                    <small>{f"{metrics['Profit_Margin']:.1f}%" if metrics['Profit_Margin'] is not None else "N/A"}</small></td>
                <td class="hidden-mobile">{fcf_display}<br><small>{fcf_yield_display}</small></td>
                <td class="hidden-mobile">{sales_5y}</td>
                <td class="hidden-mobile">{eps_5y}</td>
                <td class="hidden-mobile">{recent_growth if recent_growth else "N/A"}</td>
                <td class="{valuation_class}">{scores['valuation_score']:.1f}</td>
                <td class="{quality_class}">{scores['quality_score']:.1f}</td>
                <td class="{growth_class}">{scores['growth_score']:.1f}</td>
                <td class="{historical_class}">{historical_display}</td>
                <td class="{total_class}"><strong>{scores['total_score']:.1f}</strong></td>
            </tr>
        ''')
        
        # Create details row with profile-specific class
        table_rows.append(f'''
            <tr id="details-{stock}-{profile_name}" class="details-row {profile_class}" data-profile="{profile_name}" style="display: none;">
                <td colspan="15">
                    <div class="details-content">
                        <div style="background: linear-gradient(135deg, var(--secondary-blue), var(--accent-blue)); color: white; padding: 15px; border-radius: 8px; margin-bottom: 15px;">
                            <p style="margin: 0; font-size: 1.1rem;"><strong>📊 Active Profile:</strong> {scores['research_insights']['active_profile']}</p>
                            <p style="margin: 5px 0 0 0; font-size: 0.9rem; opacity: 0.9;">{scores['research_insights']['profile_description']}</p>
                        </div>
                        <p style="margin-bottom: 15px; padding: 10px; background: var(--bg-secondary); border-radius: 6px;"><strong>⚖️ Weights:</strong> {scores['research_insights']['weight_breakdown']}</p>
                        
                        <div class="metric-grid">
                            <div class="metric-section">
                                <h4>📊 Valuation Details</h4>
                                <p>P/S: {f"{metrics['P/S']:.2f}" if metrics['P/S'] else "N/A"} | 
                                P/B: {f"{metrics['P/B']:.2f}" if metrics['P/B'] else "N/A"} | 
                                EV/EBITDA: {f"{metrics['EV/EBITDA']:.1f}" if metrics['EV/EBITDA'] else "N/A"}</p>
                            </div>
                            <div class="metric-section">
                                <h4>💪 Quality Metrics</h4>
                                <p>ROA: {f"{metrics['ROA']:.1f}%" if metrics['ROA'] else "N/A"} | 
                                ROIC: {f"{metrics['ROIC']:.1f}%" if metrics['ROIC'] else "N/A"} | 
                                Gross Margin: {f"{metrics['Gross_Margin']:.1f}%" if metrics['Gross_Margin'] else "N/A"}</p>
                            </div>
                            <div class="metric-section">
                                <h4>📈 Growth Trends</h4>
                                <p>5Y Sales CAGR: {sales_5y} | 5Y EPS CAGR: {eps_5y}</p>
                                <p>Recent: {recent_growth if recent_growth else "N/A"}</p>
                            </div>
                        </div>
                    </div>
                </td>
            </tr>
        ''')
    
    return ''.join(table_rows)

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
HTML_FILE = os.path.join(os.getcwd(), 'index.html')
HTML_TEMPLATE_FILE = os.path.join(os.getcwd(), 'template_dual.html')
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
    """Helper function to parse growth values that come as '5.43% 5.54%' or '3Y%/5Y%'"""
    if not value or value == '-' or value == 'N/A':
        return None
    try:
        # Handle format like "5.43% 5.54%" - take the SECOND value (5-year)
        parts = value.split()
        if len(parts) >= 2:
            # Take the last percentage value
            return float(parts[-1].replace('%', ''))
        # Handle single percentage
        return float(value.replace('%', ''))
    except ValueError:
        return None
    
def get_investor_type_classification(risk_score):
    """
    Classify stock by suitable investor type based on risk score
    Returns: dict with investor types and their suitability
    """
    classifications = {
        'conservative': False,
        'balanced': False,
        'aggressive': False,
        'speculative': False
    }
    
    # Conservative: Risk 1-3
    if risk_score <= 3:
        classifications['conservative'] = True
    
    # Balanced: Risk 3-6
    if 3 <= risk_score <= 6:
        classifications['balanced'] = True
    
    # Aggressive: Risk 5-8
    if 5 <= risk_score <= 8:
        classifications['aggressive'] = True
    
    # Speculative: Risk 7-10
    if risk_score >= 7:
        classifications['speculative'] = True
    
    return classifications

def calculate_stock_risk_score(stock_symbol, metrics, sector):
    """
    Calculate risk score (1-10) for a stock with decimal precision
    Based on volatility, sector, growth stage, and business model
    """
    risk_score = 5.0  # Base score (FLOAT)
    
    # Sector risk adjustments (BASE LEVEL)
    sector_risk = {
        'Technology': 6.0,
        'Communication Services': 6.0,
        'Healthcare': 5.0,
        'Consumer Defensive': 3.0,
        'Utilities': 2.0,
        'Financial': 4.0,
        'Consumer Cyclical': 5.0,
        'Industrials': 5.0,
        'Basic Materials': 6.0,
        'Energy': 7.0,
        'Real Estate': 4.0
    }
    
    risk_score = sector_risk.get(sector, 5.0)
    
    # Adjust for volatility/beta (GRANULAR)
    beta = metrics.get('Beta')
    if beta is not None:
        if beta > 2.0:
            risk_score += 2.5      # Very high volatility
        elif beta > 1.8:
            risk_score += 2.0      # High volatility
        elif beta > 1.5:
            risk_score += 1.5
        elif beta > 1.3:
            risk_score += 1.0
        elif beta > 1.2:
            risk_score += 0.5
        elif beta > 1.0:
            risk_score += 0.2      # Slightly above market
        elif beta > 0.8:
            risk_score += 0.0      # Market-like
        elif beta > 0.6:
            risk_score -= 0.3      # Lower volatility
        else:
            risk_score -= 0.8      # Very defensive
    
    # Adjust for profitability/stability (GRANULAR)
    profit_margin = metrics.get('Profit_Margin')
    if profit_margin is not None:
        if profit_margin < 0:
            risk_score += 3.0      # Unprofitable - HIGH RISK
        elif profit_margin < 5:
            risk_score += 1.8      # Barely profitable
        elif profit_margin < 10:
            risk_score += 0.8      # Low margins
        elif profit_margin < 15:
            risk_score += 0.3      # Moderate margins
        elif profit_margin > 30:
            risk_score -= 1.0      # Excellent margins
        elif profit_margin > 25:
            risk_score -= 0.6      # Very good margins
        elif profit_margin > 20:
            risk_score -= 0.3      # Good margins
    
    # Adjust for debt (GRANULAR) - exclude Financials
    debt_eq = metrics.get('Debt/Eq')
    if debt_eq is not None and sector != 'Financial':
        if debt_eq > 3.0:
            risk_score += 2.0      # Dangerously high debt
        elif debt_eq > 2.0:
            risk_score += 1.5      # Very high debt
        elif debt_eq > 1.5:
            risk_score += 1.0      # High debt
        elif debt_eq > 1.0:
            risk_score += 0.5      # Elevated debt
        elif debt_eq > 0.5:
            risk_score += 0.0      # Moderate debt
        elif debt_eq > 0.3:
            risk_score -= 0.3      # Low debt
        elif debt_eq > 0.1:
            risk_score -= 0.6      # Very low debt
        else:
            risk_score -= 1.0      # Nearly debt-free (Visa/MA level)
    
    # Adjust for size (Market Cap) (GRANULAR)
    market_cap = metrics.get('Market_Cap')
    if market_cap is not None:
        if market_cap < 1:          # Micro cap
            risk_score += 2.5
        elif market_cap < 2:        # Small cap
            risk_score += 2.0
        elif market_cap < 5:        # Small-mid cap
            risk_score += 1.2
        elif market_cap < 10:       # Mid cap
            risk_score += 0.6
        elif market_cap < 50:       # Large cap
            risk_score += 0.0
        elif market_cap < 200:      # Mega cap
            risk_score -= 0.5
        else:                       # Super mega cap (AAPL, MSFT level)
            risk_score -= 1.0
    
    # Adjust for growth stage (GRANULAR)
    sales_5y = metrics.get('Sales_past_5Y')
    if sales_5y is not None:
        if sales_5y > 50:
            risk_score += 1.5      # Hyper-growth = execution risk
        elif sales_5y > 30:
            risk_score += 1.0      # Very high growth
        elif sales_5y > 25:
            risk_score += 0.6
        elif sales_5y > 20:
            risk_score += 0.3
        elif sales_5y > 15:
            risk_score += 0.0      # Healthy growth
        elif sales_5y < 5:
            risk_score -= 0.5      # Mature/stable
        elif sales_5y < 2:
            risk_score -= 1.0      # Very mature
    
    # Adjust for ROE/ROIC quality (GRANULAR) - high quality = lower risk
    roic = metrics.get('ROIC')
    roe = metrics.get('ROE')
    
    if roic is not None:
        if roic > 40:
            risk_score -= 1.5      # Elite quality = lower risk
        elif roic > 30:
            risk_score -= 1.0
        elif roic > 25:
            risk_score -= 0.6
        elif roic > 20:
            risk_score -= 0.3
        elif roic < 10:
            risk_score += 0.5      # Poor capital efficiency
        elif roic < 5:
            risk_score += 1.0
    elif roe is not None:
        if roe > 40:
            risk_score -= 1.0
        elif roe > 30:
            risk_score -= 0.6
        elif roe > 20:
            risk_score -= 0.3
        elif roe < 10:
            risk_score += 0.5
    
    # Cap between 1.0-10.0 and round to 1 decimal place
    risk_score = max(1.0, min(10.0, risk_score))
    
    return round(risk_score, 1)

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
        # Handle dividend format: "5.19 (2.52%)" -> extract "5.19"
        if '(' in value:
            value = value.split('(')[0].strip()
        
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
                'Sales': parse_float(metrics.get('Sales', '-')),


                # DIVIDEND FIELDS - IMPROVED PARSING
                'Dividend_Est': parse_float(metrics.get('Dividend Est.', '-')) if metrics.get('Dividend Est.', '-') not in ['-', 'N/A', ''] else None,
                'Dividend_TTM': parse_float(metrics.get('Dividend TTM', '-')) if metrics.get('Dividend TTM', '-') not in ['-', 'N/A', ''] else None,
                'Dividend_Ex_Date': metrics.get('Dividend Ex-Date', 'N/A') if metrics.get('Dividend Ex-Date', '-') not in ['-', 'N/A', ''] else 'N/A',
                'Dividend_Growth_3_5Y': parse_growth_value(metrics.get('Dividend Gr. 3/5Y', '-')) if metrics.get('Dividend Gr. 3/5Y', '-') not in ['-', 'N/A', '', '--'] else None,
                'Payout_Ratio': parse_percentage(metrics.get('Payout', '-')) if metrics.get('Payout', '-') not in ['-', 'N/A', ''] else None,
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

# ============= RESEARCH PROFILES =============
# COMPLETE FIXED RESEARCH_PROFILES - Replace entire RESEARCH_PROFILES dictionary

RESEARCH_PROFILES = {
    'academic': {
        'name': 'Academic Research (McKinsey ROIC Persistence)',
        'description': '50% of ROIC>20% companies maintain it 10yr. Only 13% of 20%+ growers sustain it.',
        'base_weights': {
            'quality': 0.65,      # ✅ INCREASE from 0.50 (ROIC persistence is key)
            'growth': 0.10,       # ✅ DECREASE from 0.20 (only 13% sustain)
            'valuation': 0.05,    # ✅ KEEP (not in McKinsey research)
            'historical': 0.20    # ✅ KEEP (10-year validation critical)
        },
        'quality_breakdown': {
            'roic_absolute': 0.50,        # PRIMARY - 50% persistence
            'roic_stability': 0.30,       # SECONDARY - Duration matters
            'fcf_positivity': 0.10,       # TERTIARY - Cash validation
            'debt_quality': 0.10,         # IMPORTANT - Financial fortress
            'roe_supplementary': 0.02     # MINIMAL - Only when no ROIC
        },
        'growth_breakdown': {
            'roic_growth': 0.50,      # ✅ INCREASE (quality-driven growth only)
            'fcf_growth': 0.25,       # ✅ DECREASE
            'eps_growth': 0.10,       # ✅ DECREASE
            'revenue_growth': 0.10,   # ✅ DECREASE (56% fall to <5%)
            'roe_growth': 0.05
        }
    },
    
    'growth_based': {
        'name': 'Growth Empirical (S&P 500 TSR Decomposition 1987-2005)',
        'description': 'TSR = Revenue (53%) + Margin improvement (16%) + Multiple expansion (26%) + Other (5%)',
        'base_weights': {
            'growth': 0.50,      # ✅ Balanced
            'quality': 0.25,     # ✅ FCF quality matters
            'valuation': 0.15,   
            'historical': 0.10
        },
        'growth_breakdown': {
            'revenue_growth': 0.77,   # 52.6% / 68.4% = 77% of growth weight
            'eps_growth': 0.23,       # 15.8% / 68.4% = 23% of growth weight (margin improvement)
            'fcf_growth': 0.00,       # Not in Image 3
            'roic_growth': 0.00,
            'roe_growth': 0.00
        },
        'quality_breakdown': {
            # Quality weight is 0%, so these don't matter
            'fcf_positivity': 0.50,
            'roic_absolute': 0.30,
            'roic_stability': 0.10,
            'debt_quality': 0.05,
            'roe_supplementary': 0.05
        }
    },
    
    'fama_french': {
        'name': 'Fama-French Five-Factor Model',
        'description': 'RMW (profitability) + CMA (conservative investment) + HML (value)',
        'base_weights': {
            'quality': 0.50,      # RMW factor
            'valuation': 0.25,    # HML factor
            'growth': 0.15,       # CMA factor (inverse - conservative)
            'historical': 0.10
        },
        'quality_breakdown': {
            'roic_absolute': 0.40,
            'roic_stability': 0.25,
            'fcf_positivity': 0.20,
            'debt_quality': 0.10,
            'roe_supplementary': 0.05
        },
        'growth_breakdown': {
            'roic_growth': 0.50,      # Conservative investment pattern
            'fcf_growth': 0.30,
            'revenue_growth': 0.10,
            'eps_growth': 0.05,
            'roe_growth': 0.05
        }
    },
    
    'magic_piotroski': {
        'name': 'Magic Formula + Piotroski Combo',
        'description': 'Greenblatt ROIC/EY (50/50) + Piotroski health screen',
        'base_weights': {
            'quality': 0.60,      # 50% Magic + 10% Piotroski quality filter
            'valuation': 0.25,    # Magic Formula earnings yield
            'growth': 0.10,
            'historical': 0.05
        },
        'quality_breakdown': {
            'roic_absolute': 0.40,    # Magic Formula ROIC
            'roic_stability': 0.15,
            'fcf_positivity': 0.25,   # Piotroski cash flow
            'debt_quality': 0.15,     # Piotroski leverage
            'roe_supplementary': 0.05
        },
        'growth_breakdown': {
            'roic_growth': 0.30,
            'fcf_growth': 0.30,
            'eps_growth': 0.20,
            'revenue_growth': 0.10,
            'roe_growth': 0.10
        }
    },
    
    'peter_lynch': {
        'name': 'Peter Lynch GARP (PEG-Primary)',
        'description': 'PEG ratio is THE core metric. Fair value PEG = 1.0. 29.2% returns (1977-1990)',
        'base_weights': {
            'growth': 0.40,       # ✅ FIX: Restore growth importance
            'valuation': 0.35,    # ✅ FIX: Reduce valuation dominance
            'quality': 0.20,      
            'historical': 0.05
        },
        'quality_breakdown': {
            'fcf_positivity': 0.50,
            'debt_quality': 0.45,
            'roic_absolute': 0.05,
            'roic_stability': 0.00,
            'roe_supplementary': 0.00
        },
        'growth_breakdown': {
            'eps_growth': 0.50,       # ✅ FIX: Re-enable
            'revenue_growth': 0.30,   # ✅ FIX: Re-enable
            'roe_growth': 0.10,       # ✅ FIX: Re-enable
            'roic_growth': 0.05,
            'fcf_growth': 0.05
        }
    },
    
    'piotroski': {
    'name': 'Piotroski F-Score Quality Screen',
        'description': '9 binary signals: 4 profitability, 3 leverage/liquidity, 2 efficiency',
        'base_weights': {
            'quality': 0.80,      # ✅ INCREASE from 0.70 (8/9 signals are quality)
            'valuation': 0.15,    # ✅ DECREASE (applied to value stocks only)
            'growth': 0.00,       # ✅ KEEP (not in original formula)
            'historical': 0.05
        },
        'quality_breakdown': {
            # Piotroski uses 9 EQUAL binary signals (1/9 each)
            'roic_absolute': 0.22,        # ROA positive (1/9)
            'roic_stability': 0.11,       # ROA improvement (1/9)
            'fcf_positivity': 0.33,       # CFO positive + CFO > NI (3/9) ✅ INCREASE
            'debt_quality': 0.33,         # Leverage + Liquidity (3/9) ✅ INCREASE
            'roe_supplementary': 0.12,
        },
        'growth_breakdown': {
            'roic_growth': 0.20,
            'fcf_growth': 0.30,
            'eps_growth': 0.20,
            'revenue_growth': 0.15,
            'roe_growth': 0.15
        }
    },
    
    'greenblatt_magic': {
        'name': 'Greenblatt Magic Formula',
        'description': '50% ROIC + 50% Earnings Yield. 30.8% CAGR (1988-2004)',
        'base_weights': {
            'quality': 0.50,      # ✅ CORRECT: Equal weight
            'valuation': 0.50,    # ✅ CORRECT: Equal weight
            'growth': 0.00,       # ✅ Greenblatt didn't use growth
            'historical': 0.00
        },
        'quality_breakdown': {
            'roic_absolute': 0.80,
            'roic_stability': 0.15,
            'fcf_positivity': 0.00,    # Not in original formula
            'debt_quality': 0.00,      # Not in original formula
            'roe_supplementary': 0.05
        },
        'growth_breakdown': {
            # Not used, but keep structure
            'roic_growth': 0.40,
            'fcf_growth': 0.30,
            'eps_growth': 0.15,
            'revenue_growth': 0.10,
            'roe_growth': 0.05
        }
    },
    
    'buffett_quality': {
        'name': 'Buffett Quality Fortress',
        'description': 'Moat durability (ROIC > 20% for 10yr) + Fair price',
        'base_weights': {
            'quality': 0.55,      # ✅ Slightly reduced
            'historical': 0.25,   
            'valuation': 0.10,    
            'growth': 0.10        # ✅ Organic compounding (increased)
        },
        'quality_breakdown': {
            'roic_absolute': 0.50,    
            'roic_stability': 0.25,   
            'fcf_positivity': 0.15,   # ✅ FIX: Increase
            'debt_quality': 0.08,     
            'roe_supplementary': 0.02 
        },
        'growth_breakdown': {
            'roic_growth': 0.40,
            'roe_growth': 0.30,
            'fcf_growth': 0.15,
            'eps_growth': 0.10,
            'revenue_growth': 0.05
        }
    },
    
    'combined_performance': {
        'name': 'Combined Performance-Weighted Portfolio',
        'description': 'Modern weights: Greenblatt (30%), Lynch (28%), Piotroski (22%), Fama (13%), Buffett (7%)',
        'base_weights': {
            'quality': 0.45,
            'valuation': 0.28,    # 🚨 FIX: Increase (Lynch + Greenblatt heavy)
            'growth': 0.20,       # 🚨 FIX: Decrease
            'historical': 0.07
        },
        'quality_breakdown': {
            'roic_absolute': 0.42,
            'roic_stability': 0.18,
            'fcf_positivity': 0.23,
            'debt_quality': 0.12,
            'roe_supplementary': 0.05
        },
        'growth_breakdown': {
            'eps_growth': 0.35,
            'revenue_growth': 0.25,
            'roic_growth': 0.20,
            'fcf_growth': 0.15,
            'roe_growth': 0.05
        }
    }
}

def get_research_validated_weights(sector, research_profile='academic'):
    """
    Get research-validated weights based on selected profile
    
    Args:
        sector: Stock sector
        research_profile: 'academic' or 'growth_based'
    """
    
    profile = RESEARCH_PROFILES.get(research_profile, RESEARCH_PROFILES['academic'])
    
    SECTOR_MULTIPLIERS = {
        'Technology': {
            'growth_mult': 1.10 if research_profile == 'academic' else 1.25,
            'quality_mult': 1.15 if research_profile == 'academic' else 1.05,
            'valuation_mult': 0.75,
        },
        'Communication Services': {
            'growth_mult': 1.10 if research_profile == 'academic' else 1.25,
            'quality_mult': 1.10 if research_profile == 'academic' else 1.00,
            'valuation_mult': 0.80,
        },
        'Healthcare': {
            'growth_mult': 1.00 if research_profile == 'academic' else 1.15,
            'quality_mult': 1.25 if research_profile == 'academic' else 1.10,
            'valuation_mult': 0.85,
        },
        'Consumer Defensive': {
            'growth_mult': 0.75 if research_profile == 'academic' else 0.85,
            'quality_mult': 1.35 if research_profile == 'academic' else 1.25,
            'valuation_mult': 1.10,
        },
        'Consumer Cyclical': {
            'growth_mult': 1.05 if research_profile == 'academic' else 1.20,
            'quality_mult': 1.00,
            'valuation_mult': 1.05,
        },
        'Utilities': {
            'growth_mult': 0.60 if research_profile == 'academic' else 0.70,
            'quality_mult': 1.40 if research_profile == 'academic' else 1.30,
            'valuation_mult': 1.20,
        },
        'Energy': {
            'growth_mult': 0.80 if research_profile == 'academic' else 0.95,
            'quality_mult': 1.15 if research_profile == 'academic' else 1.05,
            'valuation_mult': 1.15,
        },
        'Industrials': {
            'growth_mult': 1.00 if research_profile == 'academic' else 1.10,
            'quality_mult': 1.10 if research_profile == 'academic' else 1.05,
            'valuation_mult': 1.00,
        },
        'Basic Materials': {
            'growth_mult': 0.85 if research_profile == 'academic' else 0.95,
            'quality_mult': 1.10,
            'valuation_mult': 1.15,
        },
        'Financial': {
            'growth_mult': 0.90 if research_profile == 'academic' else 1.00,
            'quality_mult': 1.20 if research_profile == 'academic' else 1.15,
            'valuation_mult': 1.05,
        },
        'Real Estate': {
            'growth_mult': 0.75 if research_profile == 'academic' else 0.85,
            'quality_mult': 1.30 if research_profile == 'academic' else 1.20,
            'valuation_mult': 1.15,
        },
    }
    
    mult = SECTOR_MULTIPLIERS.get(sector, {
        'growth_mult': 1.0,
        'quality_mult': 1.0,
        'valuation_mult': 1.0
    })
    
    # Apply sector multipliers to base weights
    adj_growth = profile['base_weights']['growth'] * mult['growth_mult']
    adj_quality = profile['base_weights']['quality'] * mult['quality_mult']
    adj_valuation = profile['base_weights']['valuation'] * mult['valuation_mult']
    
    total = adj_growth + adj_quality + adj_valuation
    
    return {
        'growth': adj_growth / total,
        'quality': adj_quality / total,
        'valuation': adj_valuation / total,
        'historical': profile['base_weights']['historical'],
        'multipliers_used': mult,
        'profile_name': profile['name'],
        'profile_description': profile['description'],
        'quality_breakdown': profile['quality_breakdown'],
        'growth_breakdown': profile['growth_breakdown']
    }

def calculate_enhanced_scores_with_sectors(metrics, sector=None, stock_symbol=None, research_profile='academic'):
    """
    Research-validated scoring aligned with:
    - Wharton "Return Dominance" (2023): 75% of 10yr returns from growth
    - McKinsey ROIC persistence study
    - Empirical charts showing revenue > profit growth importance
    """
    if not metrics:
        return None
    
    historical_score_ = get_historical_score(stock_symbol) if stock_symbol else None
    trust_factor_ = calculate_trust_factor(stock_symbol) if stock_symbol else None
    risk_score = calculate_stock_risk_score(stock_symbol, metrics, sector)
    investor_types = get_investor_type_classification(risk_score)

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
    peg = metrics.get('PEG')
    
    # ========== 1. PEG RATIO (60% weight) - PRIMARY VALUATION METRIC ==========
    peg_score = 5
    
    if peg is not None and peg > 0:
        actual_growth = metrics.get('EPS_next_5Y') or metrics.get('EPS_past_5Y') or metrics.get('EPS_YoY_TTM')
        
        # Get quality context (for diagnostics only, not scoring adjustment)
        
        # UNIVERSAL PEG THRESHOLDS (same for all companies)
        # Peter Lynch: "Fair value PEG = 1.0"
        # Academic research: PEG > 2.0 = significantly overvalued
        
        peg_score = calculate_peg_score_improved(peg, actual_growth, pe)
    
    valuation_components.append(('PEG_Ratio', peg_score, 0.60))
    
    
    # ========== 2. P/E RATIO (25% weight) - SECONDARY METRIC ==========
    pe_score = 5
    
    if target_pe is not None:
        pe_good, pe_fair, pe_poor, pe_terrible = config['pe_thresholds']
        
        # Base P/E scoring (sector-adjusted)
        if target_pe < pe_good:
            pe_score = 9.0
        elif target_pe < pe_fair:
            pe_score = 7.5
        elif target_pe < pe_poor:
            pe_score = 5.5
        elif target_pe < pe_terrible:
            pe_score = 3.5
        else:
            pe_score = 2.0
        
        # Cross-check with PEG
        # Low P/E but high PEG = low growth (value trap risk)
        # High P/E but low PEG = high growth justifies multiple
        if peg is not None:
            if target_pe < pe_good and peg > 2.0:
                pe_score = max(3.0, pe_score - 2.0)
                print(f"      P/E Warning: Low P/E ({target_pe:.1f}) but high PEG ({peg:.2f}) suggests low growth")
            
            elif target_pe > pe_fair and peg < 1.0:
                pe_score = min(9.0, pe_score + 1.5)
                print(f"      P/E Insight: High P/E ({target_pe:.1f}) justified by low PEG ({peg:.2f})")
        
        # Forward P/E discount (future earnings cheaper)
        if forward_pe and pe and forward_pe < pe * 0.85:
            pe_score = min(10, pe_score + 0.5)
    
    valuation_components.append(('PE_Ratio', pe_score, 0.25))
    
    
    # ========== 3. P/S RATIO (15% weight) - TERTIARY METRIC ==========
    ps_score = 5
    
    if metrics.get('P/S') is not None:
        ps = metrics['P/S']
        profit_margin = metrics.get('Profit_Margin', 10) or 10
        
        # Sector-adjusted P/S thresholds
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
        
        if ps < thresholds[0]:
            ps_score = 9.0
        elif ps < thresholds[1]:
            ps_score = 7.5
        elif ps < thresholds[2]:
            ps_score = 5.5
        elif ps < thresholds[3]:
            ps_score = 3.5
        else:
            ps_score = 2.0
        
        valuation_components.append(('PS_Ratio', ps_score, 0.15))
    
    
    # ========== CALCULATE FINAL VALUATION SCORE ==========
    if valuation_components:
        valuation_score = sum(score * weight for _, score, weight in valuation_components)
        total_weight = sum(weight for _, _, weight in valuation_components)
        if total_weight > 0:
            valuation_score = valuation_score / total_weight
    
    valuation_score = min(max(0, valuation_score), 10)

    # ================== GET RESEARCH WEIGHTS FIRST ==================
    # Must be called BEFORE quality/growth calculations that use it
    weights_info = get_research_validated_weights(sector, research_profile)
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

     # Use Greenblatt-adjusted ROIC for Magic Formula profiles
    if research_profile in ['greenblatt_magic', 'magic_piotroski']:
        roic = calculate_greenblatt_roic(metrics)
        if roic:
            print(f"   🎯 Using Greenblatt-adjusted ROIC: {roic:.1f}%")
    else:
        roic = metrics.get('ROIC')

    roic_absolute_score = 5
    roe = metrics.get('ROE')
    roa = metrics.get('ROA')

        # ========== CALCULATE NOVY-MARX GROSS PROFITABILITY (if needed) ==========


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
    
    # Get quality breakdown from research profile
    quality_breakdown = weights_info.get('quality_breakdown', {
        'roic_absolute': 0.50,
        'roic_stability': 0.25,
        'fcf_positivity': 0.10,
        'debt_quality': 0.10,
        'roe_supplementary': 0.05
    })

    # ========== PIOTROSKI F-SCORE COMPONENT (if applicable) ==========
    if research_profile == 'piotroski' or research_profile == 'magic_piotroski':
        fscore = calculate_piotroski_fscore(metrics)
        
        # Convert F-Score (0-9) to component score (0-10)
        if fscore >= 8:
            fscore_component_score = 10.0
        elif fscore == 7:
            fscore_component_score = 8.5
        elif fscore == 6:
            fscore_component_score = 7.0
        elif fscore == 5:
            fscore_component_score = 5.5
        elif fscore == 4:
            fscore_component_score = 4.0
        elif fscore >= 2:
            fscore_component_score = 2.5
        else:  # 0-1
            fscore_component_score = 1.0
        
        fscore_weight = quality_breakdown.get('piotroski_fscore', 0)
        
        if fscore_weight > 0:
            quality_components.append(('Piotroski_F-Score', fscore_component_score, fscore_weight))
            print(f"   ✅ Piotroski F-Score: {fscore}/9 → Component Score: {fscore_component_score:.1f}/10")



        # Standard ROIC scoring for other profiles
    quality_components.append(('ROIC_Absolute', roic_absolute_score, quality_breakdown['roic_absolute']))


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

    quality_components.append(('ROIC_Stability', roic_stability_score, quality_breakdown['roic_stability']))

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
                base_fcf = 7.5   # Mature tech (AAPL, MSFT)
            elif conversion >= 0.65:
                base_fcf = 6.5   # ✅ SHARPEN from 7.0
            elif conversion >= 0.60:
                base_fcf = 6.0   # ✅ SHARPEN from 6.5
            elif conversion >= 0.55:
                base_fcf = 5.5   # ✅ NEW TIER (was 6.0)
            elif conversion >= 0.50:
                base_fcf = 5.0   # ✅ SHARPEN from 6.0 (investment phase)
            elif conversion >= 0.40:
                base_fcf = 4.0   # ✅ SHARPEN from 5.0
            elif conversion >= 0.30:
                base_fcf = 3.0   # ✅ SHARPEN from 4.0
                warnings.append(f"Low FCF conversion for {sector}: {conversion:.2%}")
            else:
                base_fcf = 2.0   # ✅ SHARPEN from 3.0
                red_flags.append(f"Poor FCF conversion for {sector}: {conversion:.2%}")
        
        elif sector in ['Consumer Defensive', 'Utilities', 'Real Estate']:
            # Mature sectors: MUST have very high conversion
            if conversion >= 1.5:
                base_fcf = 10.0
            elif conversion >= 1.35:
                base_fcf = 9.5
            elif conversion >= 1.2:
                base_fcf = 9.0
            elif conversion >= 1.1:
                base_fcf = 8.5
            elif conversion >= 1.0:
                base_fcf = 7.5
            elif conversion >= 0.90:
                base_fcf = 5.0  # SHARPEN from 6.0
                warnings.append(f"Below-normal FCF for {sector}: {conversion:.2%}")
            elif conversion >= 0.80:
                base_fcf = 2.5  # SHARPEN from 4.0
                red_flags.append(f"Poor FCF for {sector}: {conversion:.2%}")
            elif conversion >= 0.70:
                base_fcf = 1.5
                red_flags.append(f"Critical FCF issue for {sector}: {conversion:.2%}")
            else:
                base_fcf = 1.0
                red_flags.append(f"Unacceptable FCF for mature sector: {conversion:.2%}")
        
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

        # ✅ NEW: Reward high-growth stocks investing heavily
        sales_5y = metrics.get('Sales_past_5Y')
        if conversion >= 0.40 and conversion < 0.70:
            # Investment-phase companies (CapEx/R&D heavy)
            if sales_5y and sales_5y > 15:
                base_fcf = min(10, base_fcf + 1.5)  # Reward growth

        if is_investment_phase(metrics):
            base_fcf = min(10, base_fcf + 1.5)
            print(f"      High-growth investment phase bonus: +1.5")
        
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

    quality_components.append(('FCF_Positivity', fcf_positivity_score, quality_breakdown['fcf_positivity']))

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

    quality_components.append(('Debt_Quality', debt_quality_score, quality_breakdown['debt_quality']))

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

    quality_components.append(('ROE_Supplementary', roe_supplementary_score, quality_breakdown['roe_supplementary']))

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

    growth_breakdown = weights_info.get('growth_breakdown', {
        'roic_growth': 0.20,
        'fcf_growth': 0.30,
        'eps_growth': 0.20,
        'revenue_growth': 0.15,
        'roe_growth': 0.15
    })

    growth_components = []

    # 1. ROIC Growth (20% - MOST important per research!)
    roic_growth_score = calculate_roic_growth_score(metrics)
    growth_components.append(('ROIC_Growth', roic_growth_score, growth_breakdown['roic_growth']))

    # 2. FCF Growth (30%)
    fcf_growth_score = calculate_fcf_growth_score(metrics)
    growth_components.append(('FCF_Growth', fcf_growth_score, growth_breakdown['fcf_growth']))

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

    growth_components.append(('EPS_Growth', eps_growth_score, growth_breakdown['eps_growth']))

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

    growth_components.append(('Revenue_Growth', revenue_growth_score, growth_breakdown['revenue_growth']))

    # 5. ROE Growth (15%)
    roe_growth_score = calculate_roe_growth_score(metrics)
    growth_components.append(('ROE_Growth', roe_growth_score, growth_breakdown['roe_growth']))

    # Calculate final growth score
    growth_score = sum(score * weight for _, score, weight in growth_components)
        
    # ================== FINAL SCORE (Research-validated weights) ==================

    
    valuation_score = min(max(0, valuation_score), 10)
    quality_score = min(max(0, quality_score), 10)
    growth_score = min(max(0, growth_score), 10)

    # Fixed 15% historical weight per research
        # Historical weight should ONLY apply to profiles that value persistence
    if research_profile in ['buffett_quality', 'academic', 'piotroski', 'combined_performance']:
        # Profiles that USE historical in calculation
        HISTORICAL_WEIGHT = 0.15 if historical_score_ is not None else 0.0
    elif research_profile in ['growth_based', 'fama_french', 'peter_lynch', 'magic_piotroski']:
        # Profiles that SHOW but don't weight heavily
        HISTORICAL_WEIGHT = 0.05 if historical_score_ is not None else 0.0
    elif research_profile == 'greenblatt_magic':
        # CRITICAL: Greenblatt truly ignores it (1988-2004 snapshot methodology)
        HISTORICAL_WEIGHT = 0.0
        historical_score_ = None  # OK to hide for pure snapshot methodology
    else:
        # Default: show with minimal weight
        HISTORICAL_WEIGHT = 0.05 if historical_score_ is not None else 0.0

    historical_weight = HISTORICAL_WEIGHT

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

    moat_data = calculate_moat_score(metrics, sector, stock_symbol, historical_score_)
     # ADD THIS LINE:
    dividend_data = calculate_dividend_score(metrics, sector, stock_symbol)

    return {
        'valuation_score': round(valuation_score, 2),
        'quality_score': round(quality_score, 2),
        'stability_score': None,
        'growth_score': round(growth_score, 2),
        'historical_score': historical_score_,
        'trust_factor': trust_factor_,  # ADD THIS LINE
        'risk_score': risk_score,  # ADD THIS
        'investor_types': investor_types,  # ADD THIS
        'total_score': round(total_score, 2),

        # ✅ ADD THESE MOAT LINES:
        'moat_score': moat_data['moat_score'],
        'moat_rating': moat_data['moat_rating'],
        'moat_icon': moat_data['moat_icon'],
        'moat_components': moat_data['moat_components'],

        # ADD THESE LINES before 'sector':
        'dividend_score': dividend_data['dividend_score'],
        'dividend_rating': dividend_data['dividend_rating'],
        'dividend_icon': dividend_data['dividend_icon'],
        'dividend_yield': dividend_data['dividend_yield'],
        'dividend_components': dividend_data['components'],

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
            'model_version': 'Research-Aligned v4.1 (Multi-Profile)',
            'active_profile': weights_info.get('profile_name', 'Unknown'),
            'profile_description': weights_info.get('profile_description', ''),
            'methodology': 'Configurable research-based weighting',
            'weight_breakdown': f"Quality: {qual_weight*100:.0f}%, Growth: {growth_weight*100:.0f}%, Valuation: {val_weight*100:.0f}%, Historical: {historical_weight*100:.0f}%",
            'quality_focus': 'ROIC Absolute (25%) + ROIC Stability (12.5%) = 37.5% of total score',
            'growth_hierarchy': 'ROIC Growth (4%) > FCF Growth (6%) > EPS (4%) > Revenue (3%) > ROE (3%)',
            'key_finding': 'Growth only valuable if ROIC > WACC (Damodaran)',
            'historical_persistence': f'{historical_weight*100:.0f}% weight validates moat durability',
            'valuation_role': 'Mean-reverting indicator (15% weight)'
        }   
}

def create_enhanced_html(stock_data, profile_name='academic'):
    """Generate comprehensive HTML report with enhanced metrics for a specific profile"""
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    
    # Sort stocks by total score
    sorted_data = sorted(
        [(stock, metrics, scores, sector) for stock, metrics, scores, sector in stock_data if metrics and scores],
        key=lambda x: x[2]['total_score'],
        reverse=True
    )
    
    # Generate new table rows with profile class
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
        
        # Historical display
        historical_display = f"{scores['historical_score']:.1f}" if scores['historical_score'] is not None else "N/A"
        historical_class = "positive" if scores['historical_score'] and scores['historical_score'] >= 7 else "neutral" if scores['historical_score'] and scores['historical_score'] >= 5 else "negative" if scores['historical_score'] else "na"

        trust_display = f"{scores['trust_factor']:.1f}" if scores.get('trust_factor') is not None else "N/A"
        trust_class = "positive" if scores.get('trust_factor') and scores['trust_factor'] >= 7 else "neutral" if scores.get('trust_factor') and scores['trust_factor'] >= 4 else "negative" if scores.get('trust_factor') else "na"
        
        # Safe investor type display (handles missing data)
        
        investor_icons = []
        if scores.get('investor_types'):
            if scores['investor_types'].get('conservative'):
                investor_icons.append("🛡️")
            if scores['investor_types'].get('balanced'):
                investor_icons.append("⚖️")
            if scores['investor_types'].get('aggressive'):
                investor_icons.append("🚀")
            if scores['investor_types'].get('speculative'):
                investor_icons.append("🎲")

        investor_display = "".join(investor_icons) if investor_icons else "—"
        # CRITICAL FIX: Add profile class to every row
        profile_class = f"profile-{profile_name}"

        # ✅ ADD THESE LINES BEFORE THE table_rows.append():
        moat_display = f"{scores['moat_score']:.1f}" if scores.get('moat_score') is not None else "N/A"
        moat_icon = scores.get('moat_icon', '—')
        moat_class = "positive" if scores.get('moat_score') and scores['moat_score'] >= 8.0 else "neutral" if scores.get('moat_score') and scores['moat_score'] >= 6.5 else "negative" if scores.get('moat_score') else "na"

        # Around line 3240-3270, find the dividend HTML section and replace with:

        # Pre-format ALL dividend values FIRST
        div_score = f"{scores['dividend_score']:.1f}" if scores.get('dividend_score') is not None else "N/A"
        div_yield = f"{scores['dividend_yield']:.2f}" if scores.get('dividend_yield') is not None else "0.00"
        div_icon = scores.get('dividend_icon', '—')
        div_rating = scores.get('dividend_rating', 'N/A')

        # Get dividend metrics with safe fallbacks
        annual_div = f"{metrics.get('Dividend_TTM', 0):.2f}" if metrics.get('Dividend_TTM') else "0.00"
        forward_div = f"{metrics.get('Dividend_Est', 0):.2f}" if metrics.get('Dividend_Est') else "0.00"
        ex_date = metrics.get('Dividend_Ex_Date', 'N/A')
        payout = f"{metrics['Payout_Ratio']:.1f}" if metrics.get('Payout_Ratio') else "N/A"
        div_growth = f"{metrics['Dividend_Growth_3_5Y']:+.1f}" if metrics.get('Dividend_Growth_3_5Y') else "N/A"

        # Get component scores with safe fallbacks
        payout_safety = f"{scores['dividend_components']['payout_safety']:.1f}" if scores.get('dividend_components', {}).get('payout_safety') is not None else "N/A"
        growth_consistency = f"{scores['dividend_components']['growth_consistency']:.1f}" if scores.get('dividend_components', {}).get('growth_consistency') is not None else "N/A"
        yield_quality = f"{scores['dividend_components']['yield_quality']:.1f}" if scores.get('dividend_components', {}).get('yield_quality') is not None else "N/A"
        fcf_coverage = f"{scores['dividend_components']['fcf_coverage']:.1f}" if scores.get('dividend_components', {}).get('fcf_coverage') is not None else "N/A"
        
        # Stock row with profile class
        table_rows.append(f'''
            <tr class="stock-row {profile_class}" data-profile="{profile_name}" data-sector="{sector}" data-valuation="{scores['valuation_score']:.1f}" data-growth="{scores['growth_score']:.1f}" data-stock="{stock}" onclick="toggleDetails('{stock}', '{profile_name}')">
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
                <td class="{trust_class}">{trust_display}</td>
                <td class="{moat_class}">{moat_display}<br><small>{moat_icon}</small></td>
                <td data-risk-score="{scores.get('risk_score', 5):.1f}">{investor_display}</td>
                <td class="{total_class}"><strong>{scores['total_score']:.1f}</strong></td>
            </tr>
        ''')
        
        # Details row with profile class
        table_rows.append(f'''
            <tr id="details-{stock}-{profile_name}" class="details-row {profile_class}" data-profile="{profile_name}" style="display: none;">
                <td colspan="15">
                    <div class="details-content">
                        <div style="background: linear-gradient(135deg, var(--secondary-blue), var(--accent-blue)); color: white; padding: 15px; border-radius: 8px; margin-bottom: 15px;">
                            <p style="margin: 0; font-size: 1.1rem;"><strong>📊 Active Profile:</strong> {scores['research_insights']['active_profile']}</p>
                            <p style="margin: 5px 0 0 0; font-size: 0.9rem; opacity: 0.9;">{scores['research_insights']['profile_description']}</p>
                        </div>
                        <p style="margin-bottom: 15px; padding: 10px; background: var(--bg-secondary); border-radius: 6px;"><strong>⚖️ Weights:</strong> {scores['research_insights']['weight_breakdown']}</p>
                        
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
                                <h4>💵 Dividend Analysis & Safety</h4>
                                {f"""
                                <div style="background: var(--light-blue); padding: 12px; border-radius: 8px; margin-bottom: 10px;">
                                    <p style="margin: 0;">
                                        <strong style="font-size: 1.3rem;">{div_score}/10</strong>
                                        <span style="font-size: 1.5rem;">{div_icon}</span> 
                                        <strong>{div_rating}</strong>
                                    </p>
                                    <p style="margin: 5px 0 0 0; font-size: 0.9rem;">Current Yield: <strong>{div_yield}%</strong></p>
                                </div>
                                <p><strong>Dividend Metrics:</strong></p>
                                <p>Annual Dividend (TTM): <strong>${annual_div}</strong></p>
                                <p>Forward Est. Dividend: <strong>${forward_div}</strong></p>
                                <p>Ex-Dividend Date: <strong>{ex_date}</strong></p>
                                <p>Payout Ratio: <strong>{payout}%</strong></p>
                                <p>3-5Y Dividend Growth: <strong>{div_growth}%</strong></p>
                                <p style="margin-top: 10px;"><strong>Safety Breakdown:</strong></p>
                                <p style="margin: 3px 0;">Payout Safety: <strong>{payout_safety}/10</strong> <small>(35%)</small></p>
                                <p style="margin: 3px 0;">Growth Consistency: <strong>{growth_consistency}/10</strong> <small>(30%)</small></p>
                                <p style="margin: 3px 0;">Yield Quality: <strong>{yield_quality}/10</strong> <small>(20%)</small></p>
                                <p style="margin: 3px 0;">FCF Coverage: <strong>{fcf_coverage}/10</strong> <small>(15%)</small></p>
                                <p style="margin-top: 10px;"><small>💡 Dividend score measures sustainability and quality. High score = safe, growing dividend.</small></p>
                                """ if scores.get('dividend_score') is not None else """
                                <p style="padding: 15px; background: var(--bg-secondary); border-radius: 8px; text-align: center;">
                                    <strong>No Dividend</strong><br>
                                    <small>This stock does not currently pay a dividend</small>
                                </p>
                                """}
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
                                <p>Trust Factor: <strong>{trust_display}</strong></p>
                                <p>Weight in Total Score: {scores['sector_adjustments']['historical_weight_used']*100:.1f}%</p>
                                <p>Data Available: {'✅ Yes' if scores['sector_adjustments']['has_historical_data'] else '❌ No'}</p>
                                <p><small>💡 Historical score reflects long-term fundamental consistency and quality</small></p>
                            </div>
                            <div class="metric-section">
                                <h4>🏰 Long-Term Moat Analysis</h4>
                                <div style="background: var(--light-blue); padding: 12px; border-radius: 8px; margin-bottom: 10px;">
                                    <p style="margin: 0;"><strong style="font-size: 1.3rem;">{moat_display}/10</strong> 
                                    <span style="font-size: 1.5rem;">{moat_icon}</span> 
                                    <strong>{scores.get('moat_rating', 'N/A')}</strong></p>
                                </div>
                                <p><strong>Component Scores:</strong></p>
                                <p style="margin: 3px 0;">ROIC Persistence: <strong>{scores.get('moat_components', {}).get('roic_persistence', 'N/A')}/10</strong> <small>(30%)</small></p>
                                <p style="margin: 3px 0;">Margin Stability: <strong>{scores.get('moat_components', {}).get('margin_stability', 'N/A')}/10</strong> <small>(25%)</small></p>
                                <p style="margin: 3px 0;">Historical Consistency: <strong>{scores.get('moat_components', {}).get('historical_consistency', 'N/A')}/10</strong> <small>(20%)</small></p>
                                <p style="margin: 3px 0;">Capital Efficiency: <strong>{scores.get('moat_components', {}).get('capital_efficiency', 'N/A')}/10</strong> <small>(15%)</small></p>
                                <p style="margin: 3px 0;">Market Position: <strong>{scores.get('moat_components', {}).get('market_position', 'N/A')}/10</strong> <small>(10%)</small></p>
                                <p style="margin-top: 10px;"><small>💡 Measures sustainable competitive advantage over 10+ years</small></p>
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
    
    return ''.join(table_rows)

def main():
    """Main function - calculates scores for ALL research profiles"""
    
    print("🔬 Multi-Profile Stock Analysis System")
    print("=" * 70)
    print("📊 Calculating scores using NINE research methodologies:")
    print("   1️⃣  Academic Research (ROIC-focused)")
    print("   2️⃣  Growth-Based Research (S&P 500 Empirical)")
    print("   3️⃣  Novy-Marx Profitability (2023)")
    print("   4️⃣  Fama-French Five-Factor Model")
    print("   5️⃣  Magic Formula + Piotroski Combo")
    print("   6️⃣  Peter Lynch GARP (PEG-focused)")
    print("   7️⃣  Piotroski F-Score Quality Screen")
    print("   8️⃣  Greenblatt Magic Formula")
    print("   9️⃣  Buffett Quality Fortress")
    print("   🔟 Combined Performance-Weighted Portfolio")
    print("=" * 70)
    
    print("\n🔍 Starting enhanced comprehensive stock analysis...")
    print("📈 Fetching detailed metrics from Finviz...\n")
    
    stock_data_academic = []
    stock_data_growth = []
    stock_data_fama = []
    stock_data_magic_piotroski = []      # NEW
    stock_data_peter_lynch = []          # NEW
    stock_data_piotroski = []            # NEW
    stock_data_greenblatt = []           # NEW
    stock_data_buffett = []              # NEW
    stock_data_combined = []
    
    for i, stock in enumerate(STOCKS):
        print(f"\n{'='*70}")
        print(f"📊 Analyzing {stock} ({i+1}/{len(STOCKS)})")
        print(f"{'='*70}")
        
        metrics, sector = fetch_comprehensive_metrics(stock)
        
        if metrics:
            print(f"✅ Data fetched successfully")
            print(f"🏢 Sector: {sector if sector else 'Unknown'}")
            
            # Calculate scores for ALL 9 profiles
            print(f"\n   🎓 Calculating ACADEMIC profile scores...")
            scores_academic = calculate_enhanced_scores_with_sectors(
                metrics, sector, stock, research_profile='academic'
            )
            
            print(f"   📈 Calculating GROWTH-BASED profile scores...")
            scores_growth = calculate_enhanced_scores_with_sectors(
                metrics, sector, stock, research_profile='growth_based'
            )
            
            print(f"   🏛️ Calculating FAMA-FRENCH profile scores...")
            scores_fama = calculate_enhanced_scores_with_sectors(
                metrics, sector, stock, research_profile='fama_french'
            )
            
            print(f"   🎯 Calculating MAGIC+PIOTROSKI profile scores...")
            scores_magic_piotroski = calculate_enhanced_scores_with_sectors(
                metrics, sector, stock, research_profile='magic_piotroski'
            )
            
            print(f"   📊 Calculating PETER LYNCH profile scores...")
            scores_peter_lynch = calculate_enhanced_scores_with_sectors(
                metrics, sector, stock, research_profile='peter_lynch'
            )
            
            print(f"   ✅ Calculating PIOTROSKI profile scores...")
            scores_piotroski = calculate_enhanced_scores_with_sectors(
                metrics, sector, stock, research_profile='piotroski'
            )
            
            print(f"   ⚡ Calculating GREENBLATT MAGIC profile scores...")
            scores_greenblatt = calculate_enhanced_scores_with_sectors(
                metrics, sector, stock, research_profile='greenblatt_magic'
            )
            
            print(f"   🏰 Calculating BUFFETT QUALITY profile scores...")
            scores_buffett = calculate_enhanced_scores_with_sectors(
                metrics, sector, stock, research_profile='buffett_quality'
            )

            # Only calculate combined if all component scores exist
            print(f"   🎯 Calculating COMBINED PERFORMANCE profile scores...")
            if all([scores_greenblatt, scores_peter_lynch, scores_piotroski, 
                    scores_fama, scores_buffett]):
                scores_combined = calculate_combined_performance_scores(
                    metrics, sector, stock,
                    scores_greenblatt, scores_peter_lynch, 
                    scores_piotroski, scores_fama, scores_buffett
                )
            else:
                scores_combined = None
                print("      ⚠️ Combined score calculation skipped (missing component scores)")

            if all([scores_academic, scores_growth, scores_fama, 
                    scores_magic_piotroski, scores_peter_lynch, scores_piotroski,
                    scores_greenblatt, scores_buffett, scores_combined]):  # Added scores_combined check
                print(f"\n   📊 Results:")
                print(f"      Academic:         {scores_academic['total_score']:.1f}")
                print(f"      Growth:           {scores_growth['total_score']:.1f}")
                print(f"      Fama-French:      {scores_fama['total_score']:.1f}")
                print(f"      Magic+Piotroski:  {scores_magic_piotroski['total_score']:.1f}")
                print(f"      Peter Lynch:      {scores_peter_lynch['total_score']:.1f}")
                print(f"      Piotroski:        {scores_piotroski['total_score']:.1f}")
                print(f"      Greenblatt:       {scores_greenblatt['total_score']:.1f}")
                print(f"      Buffett:          {scores_buffett['total_score']:.1f}")
                print(f"      Combined:         {scores_combined['total_score']:.1f}")
        else:
            print(f"❌ Failed to fetch data for {stock}")
            scores_academic = None
            scores_growth = None
            scores_fama = None
            scores_magic_piotroski = None
            scores_peter_lynch = None
            scores_piotroski = None
            scores_greenblatt = None
            scores_buffett = None
            scores_combined = None  # Add this line
        
        # Store all 9 sets of scores
        stock_data_academic.append((stock, metrics, scores_academic, sector))
        stock_data_growth.append((stock, metrics, scores_growth, sector))
        stock_data_fama.append((stock, metrics, scores_fama, sector))
        stock_data_magic_piotroski.append((stock, metrics, scores_magic_piotroski, sector))
        stock_data_peter_lynch.append((stock, metrics, scores_peter_lynch, sector))
        stock_data_piotroski.append((stock, metrics, scores_piotroski, sector))
        stock_data_greenblatt.append((stock, metrics, scores_greenblatt, sector))
        stock_data_buffett.append((stock, metrics, scores_buffett, sector))
        stock_data_combined.append((stock, metrics, scores_combined, sector))
        
        # Delay between requests
        if i < len(STOCKS) - 1:
            delay = DELAY_BETWEEN_REQUESTS + random.uniform(0, 2)
            print(f"\n⏳ Waiting {delay:.1f}s before next stock...")
            time.sleep(delay)
    
    print("\n" + "="*70)
    print("📄 Generating 9-profile HTML report...")
    print("="*70)

    # Generate HTML with all 9 profiles
    create_quad_profile_html(
        stock_data_academic, stock_data_growth, stock_data_fama,
        stock_data_magic_piotroski, stock_data_peter_lynch, stock_data_piotroski,
        stock_data_greenblatt, stock_data_buffett, stock_data_combined
    )

    print("\n🎉 Multi-profile analysis completed!")
    print("💡 Open the HTML file to switch between 9 profiles instantly!")


if __name__ == '__main__':
    main()
