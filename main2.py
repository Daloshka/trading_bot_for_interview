import time
from binance.client import Client
import datetime
from main import print_coint

# Enter your API key and secret here
api_key = 'API_KEY'
api_secret = 'API_SECRET'

# Set the base URL and parameters for the API request
base_url = 'https://query1.finance.yahoo.com/v8/finance/chart/'
symbols = ['BTC-USD', 'ETH-USD']
interval = '1m'
range_ = '5m'

# Create a Binance client object
client = Client(api_key, api_secret)

# Initialize the price variable with the current price
price = float(client.futures_mark_price(symbol='ETHUSDT')['markPrice'])
print(f"Start price: {price}$")

# Initialize the time variables for checking price an hour ago
price_hour_ago = price
time_hour_ago = datetime.datetime.now()


# Loop forever
while True:
    # Wait for a few seconds before checking the price again
    print_coint()
    time.sleep(10)
    
    # Get the current price
    current_price = float(client.futures_mark_price(symbol='ETHUSDT')['markPrice'])
    print(f"Current price: {current_price}$")
    
    # Calculate the percentage change in price
    percentage_change = (current_price - price) / price * 100
    print(f"Perentage change: {percentage_change:.4f}%")

    
    if (datetime.datetime.now() > datetime.datetime.now() - datetime.timedelta(hours=1)):
        # Check if the percentage change is greater than 1% over the last 60 minutes
        percentage_change_per_hour = (current_price - price_hour_ago) / price_hour_ago * 100
        if abs(percentage_change_per_hour) > 1:
            print(f"ETHUSDT futures price has increased by {abs(percentage_change):.2f}% over the last 60 minutes.")
            print_coint()
                

        time_hour_ago = datetime.datetime.now()
        price_hour_ago = current_price
    
    # Update the price variable with the current price
    price = current_price