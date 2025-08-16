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
    # Create basic HTML if file doesn't exist or is empty
    if not os.path.exists(HTML_FILE) or os.path.getsize(HTML_FILE) == 0:
        with open(HTML_FILE, 'w') as f:
            f.write("""<!DOCTYPE html>
<html>
<head>
    <title>Stock PEG Ratios</title>
    <style>
        body { font-family: Arial, sans-serif; margin: 20px; }
        table { border-collapse: collapse; width: 300px; margin-top: 20px; }
        th, td { border: 1px solid #ddd; padding: 8px; text-align: left; }
        th { background-color: #f2f2f2; }
        tr:nth-child(even) { background-color: #f9f9f9; }
        .timestamp { color: #666; font-size: 0.9em; margin-top: 10px; }
    </style>
</head>
<body>
    <h1>Stock PEG Ratios</h1>
    <table id="stock-data">
        <!-- Table content will be generated -->
    </table>
</body>
</html>""")

    # Read existing HTML
    with open(HTML_FILE, 'r') as f:
        html = f.read()

    # Generate new table content
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    table_content = f"""
        <thead>
            <tr><th>Stock</th><th>PEG Ratio</th></tr>
        </thead>
        <tbody>
"""
    for stock, peg in stock_data:
        table_content += f'            <tr><td>{stock}</td><td>{peg if peg else "N/A"}</td></tr>\n'
    table_content += f"""        </tbody>
        <tfoot>
            <tr><td colspan="2" class="timestamp">Updated: {timestamp}</td></tr>
        </tfoot>
"""

    # Update the table content (replace existing if any)
    if '<table id="stock-data">' in html:
        # If table exists, replace its content
        table_start = html.find('<table id="stock-data">')
        table_end = html.find('</table>', table_start) + len('</table>')
        before_table = html[:table_start]
        after_table = html[table_end:]
        updated_html = before_table + f'<table id="stock-data">{table_content}</table>' + after_table
    else:
        # If no table exists, add it before the closing body tag
        if '</body>' in html:
            updated_html = html.replace('</body>', f'<table id="stock-data">{table_content}</table>\n</body>')
        else:
            # If no body tag exists, append the table at the end
            updated_html = html + f'\n<table id="stock-data">{table_content}</table>'

    # Write updated HTML back to file
    with open(HTML_FILE, 'w') as f:
        f.write(updated_html)

def main():
    # Get stock data
    stock_data = []
    print("Fetching PEG ratios from Finviz...")
    for i, stock in enumerate(STOCKS):
        print(f"Fetching {stock}...")
        peg = fetch_peg_ratio(stock)
        stock_data.append((stock, peg))
        if i < len(STOCKS) - 1:
            time.sleep(DELAY_BETWEEN_REQUESTS + random.uniform(0, 2))

    # Update HTML file
    create_or_update_html(stock_data)
    print(f"\nStock data updated in: {HTML_FILE}")

if __name__ == '__main__':
    main()
