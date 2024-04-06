# Some takeaways after writing this:
# 1. For getting the information in `get_info()` consider maintaining consistency with the fetch_data approach for uniformity.
# 2. You can loop through tickers but try this next time: tickers = yf.Tickers('msft aapl goog') -> tickers.tickers['MSFT'].info


import pandas as pd
import yfinance as yf
from parsing_args import parse_arguments

# Generic function to fetch and transform data
def fetch_data(ticker_objs, data_attr, transform_func=None):
    data_to_concatenate = []
    for ticker in ticker_objs:
        # Fetch the data using the specified attribute
        if hasattr(ticker, data_attr):
            data_method = getattr(ticker, data_attr)
            data = data_method() if callable(data_method) else data_method
            # Transform the data if a transformation function is provided
            if transform_func:
                data = transform_func(data, ticker)
            data['Ticker'] = ticker.info.get('symbol')
            data_to_concatenate.append(data)
    return pd.concat(data_to_concatenate, axis='index')

# Transformation function for balance sheets and income statements
def transform_financial_statement(data, ticker):
    data.reset_index(inplace=True)
    data = data.melt(id_vars=['index'])
    data.columns = ['Metric', 'Date', 'Value']
    data['Date'] = pd.to_datetime(data['Date'])
    return data

# Transformation function for actions (and similar structures)
def transform_actions(data, ticker):
    return data.reset_index()

# No transformation required for some datasets
def transform_generic(data, ticker):
    return data

# Same as the notebook implementation for simplicity in readability
def get_info(ticker_objs: list):
    dataframes_to_concatenate = []
    for t in ticker_objs:
        info = t.info
        info_df = pd.DataFrame([i for i in info.items() if i[0] != 'symbol'], columns=['Key', 'Value'])
        info_df['Ticker'] = info.get('symbol')
        dataframes_to_concatenate.append(info_df)
    return pd.concat(dataframes_to_concatenate, axis='index')


def get_historical_data(ticker_string):
    dataset = yf.download(ticker_string)['Close'].reset_index()
    dataset = dataset.melt(id_vars=['Date'], var_name='Ticker', value_name='Close').copy()
    dataset['Date'] = pd.to_datetime(dataset['Date'])
    return dataset


def save_csv(dataset, filename: str):
    """wrapper for pandas dataframe.to_csv() that automatically saves inside the `data` directory with preconfigured index=False"""
    dataset.to_csv(f'./data/{filename}.csv', index=False)


def main():
    # Use the parse_arguments function from argparser_module
    args = parse_arguments()

    # Reading tickers from the provided file
    with open(args.ticker_file, 'r') as file:
        tickers = [line.strip() for line in file.readlines()]
    ticker_list = [yf.Ticker(t) for t in tickers]

    # Fetch and transform data based on arguments
    if args.balance_sheets:
        balance_sheets = fetch_data(ticker_list, 'balance_sheet', transform_financial_statement)
        save_csv(balance_sheets, 'balance_sheet_data')

    if args.income_statements:
        income_statements = fetch_data(ticker_list, 'income_stmt', transform_financial_statement)
        save_csv(income_statements, 'income_statement_data')

    if args.actions:
        actions = fetch_data(ticker_list, 'actions', transform_actions)
        save_csv(actions, 'dividends_and_stock_splits')

    if args.eps:
        eps = fetch_data(ticker_list, 'earnings_dates', transform_actions)
        save_csv(eps, 'earnings_data')

    if args.recommendations:
        # Doesn't exist for Apple and Berkshire!
        recommendations = fetch_data(ticker_list, 'recommendations', transform_generic)
        save_csv(recommendations, 'recommendations_data')

    if args.info:
        info = get_info(ticker_list)
        save_csv(info, 'general_info')
    
    if args.historical_data:
        ticker_string = ' '.join(tickers)
        historical_data = get_historical_data(ticker_string=ticker_string).dropna()
        save_csv(historical_data, 'historical_data')

if __name__ == '__main__':
    main()



