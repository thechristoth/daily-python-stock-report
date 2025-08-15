import requests
import random
import time
from datetime import datetime

# Configuration
STOCKS = ['AAPL', 'MSFT', 'GOOGL', 'AMZN', 'META', 'TSLA', 'NVDA', 'PYPL', 'ADBE', 'NFLX']
USER_AGENTS = [
    'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36',
    'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36',
    'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:89.0) Gecko/20100101 Firefox/89.0',
    'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/14.1.1 Safari/605.1.15'
]
DELAY_BETWEEN_REQUESTS = 5  # seconds
HTML_FILE = 'index.html'

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
        
        # Simple string search for PEG ratio (faster than BeautifulSoup)
        content = response.text
        peg_index = content.find('PEG</td>')
        if peg_index == -1:
            return None
            
        # Find the next td tag after PEG
        value_start = content.find('<td', peg_index)
        value_start = content.find('>', value_start) + 1
        value_end = content.find('</td>', value_start)
        return content[value_start:value_end].strip()
        
    except Exception as e:
        print(f"Error fetching PEG for {stock}: {e}")
        return None

def update_stock_table():
    # Check if table exists in file
    table_exists = False
    try:
        with open(HTML_FILE, 'r') as f:
            if '<table id="stock-table">' in f.read():
                table_exists = True
    except FileNotFoundError:
        pass
    
    # Get current data
    stock_data = []
    print("Fetching PEG ratios from Finviz...")
    for i, stock in enumerate(STOCKS):
        print(f"Fetching {stock}...")
        peg = fetch_peg_ratio(stock)
        stock_data.append((stock, peg))
        if i < len(STOCKS) - 1:
            time.sleep(DELAY_BETWEEN_REQUESTS + random.uniform(0, 2))
    
    # Update HTML file
    with open(HTML_FILE, 'a' if table_exists else 'w') as f:
        if not table_exists:
            # Create new table
            f.write("""<!DOCTYPE html>
<html>
<head>
    <title>Stock PEG Ratios</title>
    <style>
        table { border-collapse: collapse; width: 300px; }
        th, td { border: 1px solid #ddd; padding: 8px; text-align: left; }
        th { background-color: #f2f2f2; }
    </style>
</head>
<body>
    <h1>Stock PEG Ratios</h1>
    <table id="stock-table">
        <thead>
            <tr><th>Stock</th><th>PEG Ratio</th></tr>
        </thead>
        <tbody>
""")
        
        # Always write current data (will replace existing if table existed)
        f.write("<!-- Stock data updated at: {} -->\n".format(datetime.now().strftime("%Y-%m-%d %H:%M:%S")))
        for stock, peg in stock_data:
            f.write(f'<tr><td>{stock}</td><td>{peg if peg else "N/A"}</td></tr>\n')
        
        if not table_exists:
            f.write("""        </tbody>
    </table>
</body>
</html>""")
        else:
            f.write("<!-- End of stock data -->\n")

if __name__ == '__main__':
    update_stock_table()
    print("Stock table updated successfully")
