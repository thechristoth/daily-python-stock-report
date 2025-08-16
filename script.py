import requests
import random
import time
from datetime import datetime
import os

# Configuration
STOCKS = ['AAPL', 'MSFT', 'GOOGL', 'AMZN']
USER_AGENTS = [
    'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36',
    'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36',
    'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:89.0) Gecko/20100101 Firefox/89.0',
    'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/14.1.1 Safari/605.1.15'
]
DELAY_BETWEEN_REQUESTS = 5  # seconds
HTML_FILE = os.path.join(os.getcwd(), 'index.html')  # Use current working directory

def get_random_user_agent():
    return random.choice(USER_AGENTS)

def fetch_peg_ratio(stock):
    url = f'https://finviz.com/quote.ashx?t={stock}'
    headers = {
        'User-Agent': get_random_user_agent(),
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
        'Accept-Language': 'en-US,en;q=0.5',
    }
    
    try:
        response = requests.get(url, headers=headers)
        response.raise_for_status()
        
        peg_index = response.text.find('PEG</td>')
        if peg_index == -1:
            return None
            
        value_start = response.text.find('<td', peg_index)
        value_start = response.text.find('>', value_start) + 1
        value_end = response.text.find('</td>', value_start)
        return response.text[value_start:value_end].strip()
        
    except Exception as e:
        print(f"Error fetching PEG for {stock}: {e}")
        return None

def create_or_update_html(stock_data):
    """Generates complete HTML file with styles preserved"""
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    
    # Generate table rows
    table_rows = []
    for stock, peg in stock_data:
        table_rows.append(f'<tr><td>{stock}</td><td>{peg if peg else "N/A"}</td></tr>')
    
    # Complete HTML template
    html_content = f"""<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Stock PEG Ratios</title>
    <style>
        body {{
            font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
            line-height: 1.6;
            color: #333;
            max-width: 800px;
            margin: 0 auto;
            padding: 20px;
            background-color: #f5f5f5;
        }}
        h1 {{
            color: #2c3e50;
            text-align: center;
            margin-bottom: 30px;
        }}
        table {{
            width: 100%;
            border-collapse: collapse;
            margin: 20px 0;
            box-shadow: 0 2px 3px rgba(0,0,0,0.1);
            background-color: white;
        }}
        th, td {{
            padding: 12px 15px;
            text-align: left;
            border-bottom: 1px solid #ddd;
        }}
        th {{
            background-color: #3498db;
            color: white;
            font-weight: bold;
        }}
        tr:nth-child(even) {{
            background-color: #f2f2f2;
        }}
        tr:hover {{
            background-color: #e6f7ff;
        }}
        .timestamp {{
            font-size: 0.85em;
            color: #7f8c8d;
            text-align: right;
            margin-top: 20px;
        }}
        .positive {{
            color: #27ae60;
            font-weight: bold;
        }}
        .negative {{
            color: #e74c3c;
            font-weight: bold;
        }}
    </style>
</head>
<body>
    <h1>Stock PEG Ratios Report</h1>
    <table>
        <thead>
            <tr>
                <th>Stock Symbol</th>
                <th>PEG Ratio</th>
            </tr>
        </thead>
        <tbody>
            {''.join(table_rows)}
        </tbody>
    </table>
    <div class="timestamp">Last updated: {timestamp}</div>
</body>
</html>"""
    
    # Write to file
    try:
        with open(HTML_FILE, 'w', encoding='utf-8') as f:
            f.write(html_content)
        print(f"Successfully updated {HTML_FILE}")
    except IOError as e:
        print(f"Error writing HTML file: {e}")

def main():
    print("Starting stock data collection...")
    stock_data = []
    
    for i, stock in enumerate(STOCKS):
        print(f"Fetching data for {stock}...")
        peg = fetch_peg_ratio(stock)
        stock_data.append((stock, peg))
        
        # Add delay between requests to avoid rate limiting
        if i < len(STOCKS) - 1:
            delay = DELAY_BETWEEN_REQUESTS + random.uniform(0, 2)
            print(f"Waiting {delay:.1f} seconds before next request...")
            time.sleep(delay)
    
    create_or_update_html(stock_data)
    print("Process completed successfully!")

if __name__ == '__main__':
    main()
