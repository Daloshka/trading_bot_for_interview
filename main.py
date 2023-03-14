import pandas as pd
import requests
from datetime import datetime
from fake_useragent import UserAgent
from statsmodels.tsa.stattools import coint
from time import sleep

# Set the base URL and parameters for the API request
base_url = 'https://query1.finance.yahoo.com/v8/finance/chart/'
symbols = ['BTC-USD', 'ETH-USD']
interval = '1m'
range_ = '60m'

# Define a function to parse the JSON response and return a DataFrame
def parse_response(result):
    data = result['chart']['result'][0]['indicators']['quote'][0]
    timestamp = result['chart']['result'][0]['timestamp']
    df = pd.DataFrame(data)
    df['timestamp'] = timestamp
    df['datetime'] = pd.to_datetime(df['timestamp'], unit='s')
    df.set_index('datetime', inplace=True)
    return df

def print_coint():
    if (__name__ != "__main__"):
        def parse_response_no_main(result):
            data = result['chart']['result'][0]['indicators']['quote'][0]
            timestamp = result['chart']['result'][0]['timestamp']
            df = pd.DataFrame(data)
            df['timestamp'] = timestamp
            df['datetime'] = pd.to_datetime(df['timestamp'], unit='s')
            df.set_index('datetime', inplace=True)
            return df
        
        dfs = []
        for symbol in symbols:
            url = f"{base_url}{symbol}?interval={interval}&range={range_}"
            headers = {'User-Agent': UserAgent().random}
            response = requests.get(url, headers=headers).json()
            df = parse_response_no_main(response)
            df.rename(columns={'close': symbol}, inplace=True)
            dfs.append(df[symbol])
        df = pd.concat(dfs, axis=1)
        filename = f"btc_eth.csv"
        df.to_csv(filename)
            
    # Load BTC-ETH data
    btc_data = pd.read_csv('btc_eth.csv', index_col=0, parse_dates=True)
    btc_data = btc_data.loc['2023', ['BTC-USD','ETH-USD']]
    #print(btc_data)

    # Remove Null values
    btc_data.dropna(inplace=True)

    # Perform cointegration analysis
    result = coint(btc_data['BTC-USD'], btc_data['ETH-USD'])

    if (result[1] <= 0.05):
        print('Movements are caused by its own changes')
        print('Cointegration test p-value:', result[1])
    else:
        print('Movements are caused by general changes')
        print('Cointegration test p-value:', result[1])

# Loop over the symbols and make API requests
dfs = []
for symbol in symbols:
    url = f"{base_url}{symbol}?interval={interval}&range={range_}"
    headers = {'User-Agent': UserAgent().random}
    response = requests.get(url, headers=headers).json()
    df = parse_response(response)
    df.rename(columns={'close': symbol}, inplace=True)
    dfs.append(df[symbol])

# Combine the DataFrames and save to a CSV file
if __name__ == "__main__":
    while True:
        df = pd.concat(dfs, axis=1)
        filename = f"btc_eth.csv"
        df.to_csv(filename)
        print_coint()
        print('Ожидание 60 сек до следующего обновления цен')
        sleep(60)