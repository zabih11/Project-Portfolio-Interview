import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from statsmodels.tsa.arima.model import ARIMA
from sklearn.metrics import mean_squared_error, mean_absolute_error, r2_score
import pymongo
from pmdarima import auto_arima
from statsmodels.tsa.stattools import adfuller
from statsmodels.graphics.tsaplots import plot_acf, plot_pacf
from statsmodels.tsa.statespace.sarimax import SARIMAX
import json
from datetime import datetime
import math

def mongo_connect():
    uri = "mongodb+srv://zabihm11:c51P8iuUJMz3KvRS@cluster0.xe8a23d.mongodb.net/?retryWrites=true&w=majority" 
    # Create a new client and connect to the server
    client = pymongo.MongoClient(uri)
    # Send a ping to confirm a successful connection
    try:
        client.admin.command('ping')
        print("Pinged your deployment. You successfully connected to MongoDB!")
    except Exception as e:
        print(e)
    
    return client

def data_frame(client, stock_name):
    db = client["Stock_Data"]
    collections = db[stock_name]
    values = list(collections.find())
    df = pd.DataFrame(values)
    return df

def filter_data_new_dates(start_date, end_date): # these are the start and end dates for April where the forecasting will occur
    with open("Stock_Data.json", "r") as file:
        data = json.load(file)
    
    data = data['Time Series (Daily)'] # time series data is taken from the stock data of Microsoft

    start_date = datetime.strptime(start_date, '%Y-%m-%d').date() # start and end dates parsed into datetime values using strptime and made into dates
    end_date = datetime.strptime(end_date, '%Y-%m-%d').date()

    # Making dictionary to put it in
    dates_needed = {} # dictionary used to put in the data which is in the same format

    for date_string, dates in data.items(): # for loop going through the data in the time series and makes the date string into datetime object using strptime

        date_object = datetime.strptime(date_string, "%Y-%m-%d").date()

        if start_date <= date_object <= end_date: # each date is checked to be in the conditon of the start and end date
            dates_needed[date_string] = dates # all matching dates added to the dictionary

    #dates_needed.reverse()
    reverse_dates_needed_with_model = dict(reversed(list(dates_needed.items()))) # order reversed to be chronological order
    with open("Stock_Data_Format_with_model.json", "w") as file: 
        json.dump(reverse_dates_needed_with_model, file) # dumped to filtered file
    print("The stock data has been filtered to April 2023")

    df1 = pd.DataFrame.from_dict(reverse_dates_needed_with_model, orient='index') # new dataframe made with adding the dictionary keys as field names and adding index
    df1 = df1.reset_index() # index is reset to be the date
    df1 = df1.rename(columns={'index': 'date'})
    df1 = df1.rename(columns={'4. close': 'close'}) # the close values are named 'close' for easiaer access
    df1['close'] = df1['close'].astype(float) # close values which are str are turned into float values
    df1['date'] = pd.to_datetime(df1["date"]) # date values in index turned into datetime to allow for modelling
    return df1


def pdq(df):
    # Stationary Check
    x = df['close']
    x_1 = df['close'] - df['close'].shift(1) # differencing is used to subtract the next value of close from the current value to make it stationary for the arima model
    x_1 = x_1.dropna() # panda function that drops any of the dates that have at least one missing value
    result_diff = adfuller(x_1) # Augmented Dickey Fuller test is used to hypothesis check whether the differenced data is stationary
    result_og = adfuller(x) # Augmented Dickey Fuller test is used to hypothesis check whether the original data is stationary

    print("Original Data")
    print('ADF Statistic: %f' % result_og[0]) # the more negative this is, the more likely it is to be stationary
    print('p-value: %f' % result_og[1]) # needs to be less than 0.05 to reject h0
    print('Critical Values:')
    for key, value in result_og[4].items():
        print('\t%s: %.20f' % (key, value)) # Different critical values to be compared to adf stat to see what significance level it is stationary

    print("1 Difference on Data")
    print('ADF Statistic: %f' % result_diff[0]) # the more negative this is, the more likely it is to be stationary
    print('p-value: %f' % result_diff[1]) # needs to be less than 0.05 to reject h0
    print('Critical Values:')
    for key, value in result_diff[4].items():
        print('\t%s: %.20f' % (key, value)) # Different critical values to be compared to adf stat to see what significance level it is stationary
    # depending on if the the differeincing makes it stationary, the d value becomes that
    fig26, axs10 = plt.subplots(2, 1, figsize=(8, 4))
    plot_acf(x_1, lags=20, ax=axs10[0]) # autocorrelation is done to get the p value if arima model
    plot_pacf(x_1, lags=20, ax=axs10[1]) # partial autocorrelation is done to get the q value
    # the number lag that goes out of shaded part wil be the respective p and q value
    plt.subplots_adjust(hspace=0.4)
    plt.savefig('ACFxPACF.png')
    plt.show()
    return fig26, axs10
    

def modelling_without_auxilary(df, df1):
    training_data = df[0:int(len(df))] # the training data is all of the data
    test_data = df[int(len(df)*0.8):] # the last 20% of the data is the test data

    train_model = training_data['close'] # each has the closing price of dataframe picked
    test_model = test_data['close']

    #pdq_summary = auto_arima(train_model, m=5, d=0, test='adf', start_p=1, start_q=1, max_p=3, max_q=5, D=None, seasonal=True, trace=True)
    #pdq_summary = auto_arima(train_model, m=126, d=1, test='adf', start_p=1, start_q=1, max_p=3, max_q=5, seasonal=True, trace=True)
    #print(pdq_summary)  
    
    #stepwise_model = auto_arima(train_model, start_p=1, start_q=1, max_p=3, max_q=3, m=126, start_P=0, seasonal=True, d=1, D=1, trace=True, error_action='ignore', suppress_warnings=True, stepwise=True)
    #print(stepwise_model.aic())  
    
    n = 29 # this is the number of days of april where when 29, foreacsts till 30 april 2023

    history = [x for x in train_model] # for loop goes through each closing price in traininf data

    prediction = [] # list made for forescast prediciton, this will be the plotted data
    for t in range(len(test_model)): # for loop through all the test model
        model = ARIMA(history, order=(2,2,1)) # arima model is used with order of p=2, d=2 and q=1
        #model = SARIMAX(history, order=(1,2,1), seasonal_order=(1,2,1,2))
        model_fit = model.fit() # the model is fitted to the test model data
        yhat = model_fit.forecast(steps=1)[0] # the forecasts happens in steps 1 of oe to include every day
        prediction.append(yhat) # the prediciton of each day in test model is
        obs = test_model.iloc[t] # for the index value of t, the test data gets added to history
        history.append(obs)


    for t in range(0, n+1): # goes till n+1 as is needed by what day it should go until
        model = ARIMA(history, order=(2,2,1)) # same order chosen
        #model = SARIMAX(history, order=(1,2,1), seasonal_order=(1,2,1,2)). 2,2,1
        model_fit = model.fit()
        yhat = model_fit.forecast(steps=1)[0]
        prediction.append(yhat) # prediciton is appened and so is history to still use the precious days of april for prediction
        history.append(yhat)
    print(model_fit.summary()) # sumary is done to see the accuracy of the model
    
    x = df1['date'] # the date and close values are accessed from the dataframe with the april data to evaluate
    y = df1['close']
    
    date_range = pd.date_range('2023-04-01', '2023-04-30').tolist()

    n_days = prediction[len(test_model):] # the prediciton is shown from 1st april onwards as it needs to be shown for those dates
    print(n_days)
    indices = [2, 3, 4, 5, 9, 10, 11, 12, 13, 16, 17, 18, 19, 20, 23, 24, 25, 26, 27] # due to real data being business days, to compare, the indices of the business days of april were selected for comparing
    # The values here are all 1 day less than each day that is available in the real stock market for April
    n_days_selected = [n_days[i] for i in indices] # for loop iteration for the calues at the indices
    mse = mean_squared_error(y, n_days_selected) # different statistical measure are found using sklearn library
    print('MSE: '+str(mse))
    mae = mean_absolute_error(y, n_days_selected)
    print('MAE: '+str(mae))
    rmse = math.sqrt(mean_squared_error(y, n_days_selected))
    print('RMSE: '+str(rmse))
    r2 = r2_score(y, n_days_selected)
    print('R-Squared: '+str(r2))
    mape = np.mean(np.abs((y - n_days_selected)/y))*100
    print('MAPE: '+str(mape))

    fig27, ax27 = plt.subplots(1, figsize=(8, 4)) # plot of forecasted data against real data of april to visualise difference

    ax27.plot(date_range, n_days, label='Forecasted')
    ax27.plot(x, y, label='Real')
    ax27.set_title("Real and Model Forecasted Close Price Stock Movements in April 2023")
    ax27.set_xlabel("Date")
    ax27.set_ylabel("Stock Price ($)")
    ax27.set_xticks(x[::5])
    ax27.legend()
    plt.savefig('Forecast_vs_Real.png')
    plt.show()
    return fig27, ax27
    



if __name__ == "__main__":
    client = mongo_connect()
    stock_name = "Microsoft (MSFT)"
    df = data_frame(client, stock_name)
    fig26, axs10 = pdq(df)
    df1 = filter_data_new_dates('2023-04-01','2023-04-30')
    fig27, ax27 = modelling_without_auxilary(df, df1)
    client.close()


