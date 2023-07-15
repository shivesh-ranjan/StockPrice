from flask import Flask, render_template
import pandas as pd
import matplotlib.pyplot as plt
from prophet import Prophet
import pickle

app = Flask(__name__)

model_path = 'models/stock_model.pkl'
with open(model_path, 'rb') as f:
    model = pickle.load(f)

@app.route('/')
def home():
    return 'Welcome to the Stock Price Prediction App'

@app.route('/plot')
def plot():
    # Generate future timestamps for prediction
    future_dates = model.make_future_dataframe(periods=30, freq='D')

    # Make predictions
    predictions = model.predict(future_dates)

    # Plot the predictions
    fig, ax = plt.subplots()
    ax.plot(predictions['ds'], predictions['yhat'], label='Predicted Price')
    ax.set_xlabel('Date')
    ax.set_ylabel('Stock Price')
    ax.legend()

    # Save the plot to a file
    plot_path = 'static/plot.png'
    fig.savefig(plot_path)
    plt.close(fig)

    # Render the template with the plot
    return render_template('plot.html', plot_path=plot_path)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
