import requests
symbol = 'AAPL'  # Example stock symbol
api_key = 'YOUR_API_KEY'  # Replace with your Alpha Vantage API key
url = f'https://www.alphavantage.co/query?function=TIME_SERIES_DAILY_ADJUSTED&symbol={symbol}&outputsize=full&apikey={api_key}'
response = requests.get(url)
data = response.json()
print('Api called Successfully!')
#### JSON to Pandas DataFrame

import pandas as pd
# Extract data points from the JSON response
time_series_data = data['Time Series (Daily)']
timestamps = list(time_series_data.keys())
close_prices = [float(data_point['4. close']) for data_point in time_series_data.values()]
# Create the DataFrame
df = pd.DataFrame({
    'ds': timestamps,
    'y': close_prices
})

#### Training 
print('started Training')

from prophet import Prophet
model = Prophet()
model.fit(df) # df has to contain 'ds' and 'y'

#### Saving Model
import pickle
with open('models/stock_model.pkl', 'wb') as f:
    pickle.dump(model, f)
print('Model Saved Suuceesfully!')