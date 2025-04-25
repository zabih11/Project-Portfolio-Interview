import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import pymongo
from scipy.stats import pearsonr
from statsmodels.tsa.seasonal import seasonal_decompose

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
    print(df.tail())
    return df
    
def seasonality_check(df):

    df_new = df[['date', 'close']].copy() # new data frame is made that copies the date and close fields of the database retrieved from mongodb using the data_frame function
    df_new['date'] = pd.to_datetime(df_new["date"]) # dates field turned into date time values
    x = df_new['date'] # new dataframe date field is assigned to a variable
    df_new = df_new.asfreq('b') # frequency of the data in the data frame is set to be for business days using asfreq
    df_new = df_new.fillna(method='ffill').dropna() # forward will is used for values that are missing. In this case this means days that are missing which would be weekedns and american holidays
    df_new.set_index('date', inplace=True) # the date is set as the index of the data frame
    df_new['close'] = pd.to_numeric(df['close'], errors='coerce') # the close values are made in to numeric values, float method was tried but received many errors
    y = df_new['close'] # assigned to veriable y
    decompose_result_mult = seasonal_decompose(y, model="multiplicative", period=126) 
    # seasonal decompose is used using multiplcative model and seasonality period of q26 dys corresponding to business days every 2 quarters
    trend = decompose_result_mult.trend # reults for data trend
    seasonal = decompose_result_mult.seasonal # results for patterns of seasonality
    residual = decompose_result_mult.resid # results of residual data as comoared to the trend

    fig13, axs4 = plt.subplots(4, 1, figsize=(8, 8)) # plot is mad to have 4 subplots, one of the close prices, one of the trend line, one for seasonality and last for resifduals
    axs4[0].plot(x, y, label='Original', color="blue")
    axs4[0].legend(loc='best')
    axs4[0].set_ylabel('Stock Close Price ($)')
    axs4[1].plot(x, trend, label='Trend', color="blue")
    axs4[1].legend(loc='best')
    axs4[1].set_ylabel('Stock Close Price ($)')
    axs4[2].plot(x, seasonal, label='Seasonality', color="blue")
    axs4[2].legend(loc='best')
    axs4[2].set_ylabel('Seasonal Patterns')
    axs4[3].plot(x, residual, label='Residuals', color="blue")
    axs4[3].legend(loc='best')
    axs4[3].set_ylabel('Residuals')
    axs4[3].set_xlabel('Date')
    fig13.tight_layout() # layout is made to ft tighly within the figure size given.
    
    plt.savefig('seasonality_decompose.png')
    plt.show()
    return fig13, axs4



def seasonality(df):
    fig14, ax14 = plt.subplots(1, figsize=(8, 4))
    
    x = df['date']
    y = df['close']
    important_event_dates = ['2019-12-31', '2020-06-30', '2020-12-31', '2021-06-30', '2021-12-31', '2022-06-30']
    
    ax14.plot(x,y, color='purple', label='Stock Close Price')

    ax14.set_title("Close Stock Price Against Date With Special Events")
    ax14.set_xlabel("Date")
    ax14.set_ylabel("Close Stock Price ($)")
    ax14.set_xticks(x[::163])

    
    [ax14.axvline(_x, color='green', linestyle='--', linewidth=1, alpha=0.5) for _x in important_event_dates]

    ax14.legend()

    plt.savefig('Seasonality.png')
    plt.show()

    return fig14, ax14




def scatter_plots(df):
    fig15, ax15 = plt.subplots(1, figsize=(8, 4))
    
    x = df['date']
    y1 = df['volume']
    y2 = df['close']


    ax15.scatter(x, y1, color='red', label="Stock Volume Traded")

    ax15.set_title("Scatter Plot of Close Price and Volume Traded of Microsoft Stocks")
    ax15.set_xlabel("Date")
    ax15.set_ylabel("Volume")
    ax15.set_xticks(x[::163])

    ax16 = ax15.twinx()

    ax16.scatter(x, y2, color='blue', label="Stock Close Price ($)")
    #ax4.legend("Stock Close Price ($)")
    ax15.legend(loc="upper left")
    ax16.set_ylabel("Close Price ($)")
    #ax5.legend("Stock Volume Traded")
    ax16.legend(loc="upper right")

    plt.savefig('Scatter_Volume_Close.png')
    plt.show()
    return fig15, (ax15, ax16)

def box_plot(df):
    fig17, ax17 = plt.subplots(1, figsize=(8, 4))
    
    #x = df['date']
    y1 = df['open']
    y2 = df['high']   
    y3 = df['low'] 
    y4 = df['close']

    ys = [y1, y2, y3, y4]
    
    ax17.boxplot(ys, labels = ['Open Price', 'High Price', 'Low Price', 'Close Price'], patch_artist=True)

    ax17.set_title("Box Plot of Different Microsoft Stock Prices")
    #ax6.set_xlabel("Date")
    ax17.set_ylabel("Stock Price ($)")
    #ax6.set_xticks(x[::60])
    ax17.grid(alpha=0.5)

    plt.savefig('Boxplot.png')
    plt.show()
    return fig17, ax17


def hypothesis(df):
    x = df['close']
    y = df['volume']
    test = pearsonr(x, y)
    correlation_coefficient = test[0]
    p_value = test[1]

    print(f"The correlation coefficient is {correlation_coefficient}")
    if 0.8 <= correlation_coefficient <= 1:
        print("Strong Positive Correlation")
    elif 0.3 <= correlation_coefficient <= 0.7:
        print("Positive Correlation")
    elif -0.2 <= correlation_coefficient <= 0.2:
        print("Neither Positive or Negative Correlation")
    elif -0.7 <= correlation_coefficient <= -0.3:
        print("Negative Correlation")
    elif -1 <= correlation_coefficient <= -0.8:
        print("Strong Negative Correlation")

    print(f"The P value is {p_value}")
    if p_value < 0.05:
        print("Null Hypothesis is Rejected. There is a statistically significant association between the stock close price and volume of stocks traded.")
    else:
        print("Null Hypothesis is Accepted. There is not a statistically significant association between the stock close price and volume of stocks traded.")



def OBV(df):
    obv = [] # a list to give the on-balance volume of the data
    obv.append(0) # makes the first value of the obv list a 0
    for day in range(1, len(df.close)): 
        if df.close[day] > df.close[day-1]: # compares closing price with closing price of day before
            obv.append(obv[-1] + df.volume[day]) # if bigger, then volume is added to the previous value of obv
        elif df.close[day] < df.close[day-1]: # if lower then subtracts volume from the day before's obv
            obv.append(obv[-1] - df.volume[day])
        else:
            obv.append(obv[-1]) # if they are the same the obv is not changed


    fig18, ax18 = plt.subplots(1, figsize=(8, 4))
    
    x = df['date']
    y1 = df['close']


    ax18.plot(x, obv, color='blue', label='OBV')

    ax19 = ax18.twinx()
    ax19.plot(x,y1, color='red', label='Stock Close Price')
    ax18.set_title("On-balance volume")
    ax18.set_xlabel("Date")
    ax18.set_ylabel("OBV")
    ax18.set_xticks(x[::163])
    ax19.set_ylabel("Stock Close Price ($)")

    # create the names in the legend with the format `<feature_name> [<unit>]`
    ax18.legend(loc="upper left")
    ax19.legend(loc="upper right")

    plt.savefig('OBV.png')
    plt.show()
    return fig18, (ax18, ax19)


def acc_dist(df):
    money_flow_volume = []
    x_close = df['close']
    x_low = df['low']
    x_high = df['high']
    x_volume = df['volume'] 
    money_flow_volume = (((x_close - x_low) - (x_high - x_close)) / (x_high - x_low)) * (x_volume) # money flow (numerator value) is divided by range of stock price on the day and multiplied by volume to get money flow volume
    accum_dist = np.cumsum(money_flow_volume) # cumulative sum is found in form of numpy array

    fig20, ax20 = plt.subplots(1, figsize=(8, 4))
    
    x = df['date']
    #y1 = df['volume']


    ax20.plot(x, accum_dist, color='blue', label='ADL')

    ax21 = ax20.twinx()
    ax21.plot(x,x_close, color='red', label='Stock Close Price')
    ax20.set_title("Accumulation / Distribution Line")
    ax20.set_xlabel("Date")
    ax20.set_ylabel("ADL")
    ax20.set_xticks(x[::163])

    ax21.set_ylabel("Stock Close Price ($)")

    # create the names in the legend with the format `<feature_name> [<unit>]`
    ax20.legend(loc="best")
    ax21.legend(loc="best")


    plt.savefig('Accumulation_Distribution_Line.png')
    plt.show()

    return fig20, (ax20, ax21)


def macd(df):
    long_ema = df['close'].ewm(span = 26, adjust = False).mean() # mean of the exponential moving average is found got a period of 26 days
    short_ema = df['close'].ewm(span = 12, adjust = False).mean() # mean of the exponential moving average is found got a period of 12 days
    macd_values = short_ema - long_ema # different makes the macd values
    signal = macd_values.ewm(span=9, adjust=False).mean() # mean of the exponential moving average is found got a period of 9 days for the signal
    macd_bars = macd_values - signal # difference in macd values and signal calulates how big the bars will be

    fig22, ax22 = plt.subplots(1, figsize=(8, 4))
    
    x = df['date']
    y = df['close']

    ax22.plot(x, macd_values, color='orange')
    ax22.plot(x, signal, color='purple')
    ax22.bar(x, macd_bars, color='green') # bar plot is done that look like financial 'candles'
    ax23 = ax22.twinx()
    ax23.plot(x, y, color='red', label='Stock Close Price', linewidth=0.5, alpha=0.5)
    ax22.set_title("Moving Average Convergence Divergence")
    ax22.set_xlabel("Date")
    ax22.set_ylabel("MACD")
    ax22.set_xticks(x[::163])

    ax22.legend(["MACD Line", "Signal Line", "MACD Bars"], loc="upper left")

    ax23.set_ylabel("Stock Close Price ($)")


    ax23.legend(loc="upper right")

    plt.savefig('MACD.png')
    plt.show()

    return fig22, (ax23, ax23)


def rsi(df):
    delta = df['close'].diff() # difference between consectuive closing prices are found
    period = 14
    gain = delta.copy()
    loss = delta.copy()
    gain[gain < 0] = 0 # gains are set to 0 and are only postive
    loss[loss > 0] = 0 # losses are set to 0 and are only negative   
    avg_gain = gain.rolling(window=period).mean() # mean of the rolling average for the last 14 days is found
    avg_loss = abs(loss.rolling(window=period).mean()) # absolute mean of the rolling average for the last 14 days is found
    relative_strength = avg_gain / avg_loss # ratio is the strength
    rsi = 100 - (100 / (1 + relative_strength)) # rsi formaula is used to get values for the rsi

    
    fig24, ax24 = plt.subplots(1, figsize=(8, 4))
    
    x = df['date']
    y = df['close']


    ax24.plot(x, rsi, color='blue', label='RSI')
    #ax3.plot(x, signal)
    ax25 = ax24.twinx()
    ax25.plot(x, y, color='red', label='Stock Close Price')
    ax24.set_title("Relative Strength Index")
    ax24.set_xlabel("Date")
    ax24.set_ylabel("RSI")
    ax24.set_ylim(0, 100)
    ax24.set_xticks(x[::163])
    ax25.set_ylabel("Stock Close Price ($)")

    # create the names in the legend with the format `<feature_name> [<unit>]`
    ax24.legend(loc="upper left")
    ax25.legend(loc="upper right")
    
    plt.savefig('RSI.png')
    plt.show()

    return fig24, (ax24, ax25)




if __name__ == "__main__":
    client = mongo_connect()
    stock_name = "Microsoft (MSFT)"
    df = data_frame(client, stock_name)
    fig13, axs4 = seasonality_check(df)
    #fig14, ax14 = seasonality(df)
    #fig15, axs5 = scatter_plots(df)
    #fig17, ax17 = box_plot(df)
    #hypothesis(df)
    #fig18, axs6 = OBV(df)
    #fig20, axs7 = acc_dist(df)
    #fig22, axs8 = macd(df)
    #fig24, axs9 = rsi(df)
    client.close()