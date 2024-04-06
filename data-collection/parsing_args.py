import argparse

def parse_arguments():
    """Allows us to retrive data using command limne arguments"""
    parser = argparse.ArgumentParser(description="Fetch financial data for specified tickers.")
    parser.add_argument('--ticker-file', type=str, help='Path to a file containing ticker symbols, one per line', required=True)
    parser.add_argument('--historical_data', action='store_true', help='Fetch historical prices')
    parser.add_argument('--balance_sheets', action='store_true', help='Fetch balance sheets')
    parser.add_argument('--income_statements', action='store_true', help='Fetch income statements')
    parser.add_argument('--actions', action='store_true', help='Fetch actions (dividends, splits etc.)')
    parser.add_argument('--eps', action='store_true', help='Fetch earnings per share data')
    parser.add_argument('--recommendations', action='store_true', help='Fetch recommendations')
    parser.add_argument('--info', action='store_true', help='Fetch ticker info data')

    return parser.parse_args()