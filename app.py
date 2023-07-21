from flask import Flask, render_template, request
import pandas as pd
from prophet import Prophet
import pickle
import requests

app = Flask(__name__)
'''
@app.route('/')
def home():
    return 'Welcome to the Stock Price Prediction App'
'''
@app.route('/train')
def train():
    symbol = ['AAPL', 'IBM', 'RELIANCE.BSE']  # Apple IBM Reliance
    api_key = '0VSSNFD1KRGASNV9'  
    for i in symbol:
        url = f'https://www.alphavantage.co/query?function=TIME_SERIES_DAILY&symbol={i}&apikey={api_key}&outputsize=full'
        response = requests.get(url)
        data = response.json()
        print('Api called Successfully!')
        #### JSON to Pandas DataFrame
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
        model = Prophet()
        model.fit(df) # df has to contain 'ds' and 'y'
        #### Saving Model
        with open(f'models/stock_model_{i}.pkl', 'wb') as f:
            pickle.dump(model, f)
    print('Models Saved Suuceesfully!')
    return 'Models trained successfully!'


@app.route('/', methods=['GET', 'POST'])
def plot():
    if request.method == 'POST':
        # Get the selected company and number of days from the form
        selected_company = request.form.get('company')
        selected_days = int(request.form.get('days'))

        model_path = f'models/stock_model_{selected_company}.pkl'
        with open(model_path, 'rb') as f:
            model = pickle.load(f)
        # Generate future timestamps for prediction
        future_dates = model.make_future_dataframe(periods=selected_days)

        # Make predictions
        predictions = model.predict(future_dates)

        # Plot the predictions
        fig1 = model.plot(predictions)
        fig2 = model.plot_components(predictions)

        # Save the plot to a file
        fig1.savefig('static/forecast.png')
        fig2.savefig('static/forecast_components.png')

        # Render the template with both plot paths
    return render_template('plot.html', plot_path1='forecast.png', plot_path2='forecast_components.png')

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
