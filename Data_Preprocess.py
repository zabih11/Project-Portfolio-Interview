import pymongo
import json
import numpy as np
from scipy import stats
import pandas as pd
import matplotlib.pyplot as plt


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


def missing_values(client, stock_name):
    db = client["Stock_Data"]
    collections = db[stock_name]
    found_missing = False
    # Find and delete documents with any null values
    missing_data = {"$or": [{"date": None},{"open": None}, {"high": None}, {"low": None}, {"close": None}, {"volume": None}]}

    days_with_missing_data = collections.find(missing_data)
    # Delete documents with any null values
    for docs in days_with_missing_data:
        found_missing = True
        doc_id = str(docs["_id"])
        date = docs["date"]
        print(f"Deleting Day With ObjectId: {doc_id} and Date: {date} Due to Having an Empty Value(s).")
        collections.delete_one({"_id": docs["_id"]})
    
    if found_missing == False:
        print("There were No Days With Missing Data")
    else:
        print("All Days With Missing Data Were Deleted")

    return stock_name

def outliers(client, stock_name):
    # The outliers of each part of the data will be found using the z-score and if it is more 3 or less than -3 then considered an outlier
    db = client["Stock_Data"]
    collections = db[stock_name]
    values = list(collections.find().sort("date", pymongo.ASCENDING))

    df = pd.DataFrame(values)
    date_values_original = df["date"].copy().to_numpy()
    open_values_original = df["open"].copy().to_numpy().astype(float)
    high_values_original = df["high"].copy().to_numpy().astype(float)
    low_values_original = df["low"].copy().to_numpy().astype(float)
    close_values_original = df["close"].copy().to_numpy().astype(float)
    volume_values_original = df["volume"].copy().to_numpy().astype(int)

    z_open = stats.zscore(open_values_original)
    z_high = stats.zscore(high_values_original)
    z_low = stats.zscore(low_values_original)
    z_close = stats.zscore(close_values_original)
    z_volume = stats.zscore(volume_values_original)

    threshold = 3
    is_outlier_open = abs(z_open) > threshold
    is_outlier_high = abs(z_high) > threshold
    is_outlier_low = abs(z_low) > threshold
    is_outlier_close = abs(z_close) > threshold
    is_outlier_volume = abs(z_volume) > threshold

    outlier_indices_open = np.nonzero(is_outlier_open)
    print("The indices of outliers at open times are:", list(outlier_indices_open[0]))

    outlier_indices_high = np.nonzero(is_outlier_high)
    print("The indices of outliers at high price are:", list(outlier_indices_high[0]))

    outlier_indices_low = np.nonzero(is_outlier_low)
    print("The indices of outliers at low price are:", list(outlier_indices_low[0]))

    outlier_indices_close = np.nonzero(is_outlier_close)
    print("The indices of outliers at close times are:", list(outlier_indices_close[0]))

    outlier_indices_volume = np.nonzero(is_outlier_volume)
    print("The indices of outliers for volume are:", list(outlier_indices_volume[0]))
    outlier_indices = list(outlier_indices_volume[0])
    outlier_value_volume = [volume_values_original[indices] for indices in outlier_indices_volume[0]]
    print("Volume values at desired indices:", outlier_value_volume)

    found_outlier = False
    int_outlier_value_volume = [int(value) for value in outlier_value_volume]
    days_with_volume_outliers = collections.find({"volume": {"$in": int_outlier_value_volume}})

    # Delete documents with outliers
    for docs in days_with_volume_outliers:
        found_outlier = True
        doc_id = str(docs["_id"])
        date = docs["date"]
        volume = docs["volume"]
        print(f"Deleting Day With ObjectId: {doc_id} and Date: {date} Due to Having an Outlier with Volume: {volume}.")
        collections.delete_one({"_id": docs["_id"]})
    
    if found_outlier == False:
        print("There were No Days With Outliers")
    else:
        print("All Days With Outliers Were Deleted")

    collections1 = db[stock_name]
    values1 = list(collections1.find())

    df1 = pd.DataFrame(values1)
    date_values_list = df1["date"].to_numpy().tolist()
    open_values_list = df1["open"].to_numpy().astype(float).tolist()
    high_values_list = df1["high"].to_numpy().astype(float).tolist()
    low_values_list = df1["low"].to_numpy().astype(float).tolist()
    close_values_list = df1["close"].to_numpy().astype(float).tolist()
    volume_values_list = df1["volume"].to_numpy().astype(int).tolist()


    return open_values_list, high_values_list, low_values_list, close_values_list, volume_values_list, date_values_list, open_values_original, high_values_original, low_values_original, close_values_original, volume_values_original, date_values_original, outlier_indices, z_open, z_high, z_low, z_close, z_volume

def minmax_norm(z_open, z_high, z_low, z_close, z_volume):
    z_open = np.array(z_open)
    z_high = np.array(z_high)
    z_low = np.array(z_low)
    z_close = np.array(z_close)
    z_volume = np.array(z_volume)
    
    z_minmax_open = (z_open - np.min(z_open)) / (np.max(z_open) -np. min(z_open))
    z_minmax_high = (z_high - np.min(z_high)) / (np.max(z_high) - np.min(z_high))
    z_minmax_low = (z_low - np.min(z_low)) / (np.max(z_low) - np.min(z_low))
    z_minmax_close = (z_close - np.min(z_close)) / (np.max(z_close) - np.min(z_close))
    z_minmax_volume = (z_volume - np.min(z_volume)) / (np.max(z_volume) - np.min(z_volume))

    return z_minmax_open, z_minmax_high, z_minmax_low, z_minmax_close, z_minmax_volume

def normal_plotting(open_values_original, high_values_original, low_values_original, close_values_original, date_values_original):
    
    fig1, ax1 = plt.subplots(1, figsize=(8, 4))
    
    x = date_values_original
    y1 = open_values_original
    y2 = high_values_original
    y3 = low_values_original
    y4 = close_values_original

    ys = [y1, y2, y3, y4]
    
    for y in ys:
        ax1.plot(x, y)

    ax1.set_title("MSFT - Stock Prices at Open, High, Low and Close from 2019-04-01 to 2023-03-31")
    ax1.set_xlabel("Date")
    ax1.set_ylabel("Stock Price ($)")
    ax1.set_xticks(x[::163])

    # create the names in the legend with the format `<feature_name> [<unit>]`
    ax1.legend(["Stock Open Price ($)", "Stock High Price ($)", "Stock Low Price ($)", "Stock Close Price ($)"])
    plt.savefig('normal_plot.png')
    plt.show()
    return fig1, ax1

def normal_plotting_with_volume(close_values_original, volume_values_original, date_values_original):
    
    fig2, ax2 = plt.subplots(1, figsize=(8, 4))
    
    x = date_values_original
    y1 = close_values_original
    y2 = volume_values_original

    ax2.plot(x, y1, c='green', label="Stock Price ($)")

    # format the axes
    ax2.set_title("MSFT - Close Stock Prices and Volume from 2019-04-01 to 2023-03-31")
    ax2.set_xlabel("Date")
    ax2.set_ylabel("Stock Price ($)")
    ax2.set_xticks(x[::163])

    ax3 = ax2.twinx()

    ax3.plot(x, y2, c='purple', label="Volume Traded")

    ax3.set_ylabel("Volume Traded")

    # create the names in the legend with the format `<feature_name> [<unit>]`
    ax2.legend(loc="upper left")
    ax3.legend(loc="upper right")

    plt.savefig('normal_plot_with_volume.png')
    plt.show()
    return fig2, (ax2, ax3)

def normal_plotting_highlight_outliers(open_values_original, high_values_original, low_values_original, close_values_original, date_values_original, outlier_indices):
    
    fig5, ax5 = plt.subplots(1, figsize=(8, 4))
    
    x = date_values_original
    y1 = open_values_original
    y2 = high_values_original
    y3 = low_values_original
    y4 = close_values_original

    x_outlier = date_values_original[outlier_indices]
    y1_outlier = open_values_original[outlier_indices]
    y2_outlier = high_values_original[outlier_indices]
    y3_outlier = low_values_original[outlier_indices]
    y4_outlier = close_values_original[outlier_indices]

    ys = [y1, y2, y3, y4]
    ys_outlier = [y1_outlier, y2_outlier, y3_outlier, y4_outlier]
    
    for y in ys:
        ax5.plot(x, y)
    for y in ys_outlier:
        ax5.scatter(x_outlier, y, c="black", alpha=0.5)

    # format the axes
    ax5.set_title("MSFT - Highlighted Outlier on Stock Prices from 2019-04-01 to 2023-03-31")
    ax5.set_xlabel("Date")
    ax5.set_ylabel("Stock Price ($)")
    ax5.set_xticks(x[::163])

    # create the names in the legend with the format `<feature_name> [<unit>]`
    ax5.legend(["Stock Open Price ($)", "Stock High Price ($)", "Stock Low Price ($)", "Stock Close Price ($)"])

    plt.savefig('normal_plot_highlight_outliers.png')
    plt.show()
    return fig5, ax5


def without_outlier_plotting(open_values_list, high_values_list, low_values_list, close_values_list, date_values_list):
    
    fig6, ax6 = plt.subplots(1, figsize=(8, 4))
    
    x = date_values_list
    y1 = open_values_list
    y2 = high_values_list
    y3 = low_values_list
    y4 = close_values_list

    ys = [y1, y2, y3, y4]
    
    for y in ys:
        ax6.plot(x, y)

    # format the axes
    ax6.set_title("MSFT - Stock Prices With Outliers Removed from 2019-04-01 to 2023-03-31")
    ax6.set_xlabel("Date")
    ax6.set_ylabel("Stock Price ($)")
    ax6.set_xticks(x[::163])

    # create the names in the legend with the format `<feature_name> [<unit>]`
    ax6.legend(["Stock Open Price ($)", "Stock High Price ($)", "Stock Low Price ($)", "Stock Close Price ($)"])

    plt.savefig('without_outlier_plot.png')
    plt.show()
    return fig6, ax6

def volume_plotting(date_values_original, date_values_list, volume_values_original, volume_values_list):
    
    fig4, ax4 = plt.subplots(1, figsize=(8, 4))
    
    x1 = date_values_original
    x2 = date_values_list
    y1 = volume_values_original
    y2 = volume_values_list

    ax4.plot(x1, y1)
    ax4.plot(x2, y2)

    # format the axes
    ax4.set_title("MSFT - Volume of Stocks Traded (With Outliers Vs Without Outliers)")
    ax4.set_xlabel("Date")
    ax4.set_ylabel("Stocks Traded")
    ax4.set_xticks(x1[::163])

    # create the names in the legend with the format `<feature_name> [<unit>]`
    ax4.legend(["With Outliers", "Without Outliers"])
    plt.savefig('volume_plot.png')
    plt.show()
    return fig4, ax4

def normalisation_1(date_values_original, z_minmax_open, z_minmax_high, z_minmax_low, z_minmax_close):
    fig7, ax7 = plt.subplots(1, figsize=(8, 4))
    
    x = date_values_original


    y1_z = z_minmax_open
    y2_z = z_minmax_high
    y3_z = z_minmax_low
    y4_z = z_minmax_close

    ys_z = [y1_z, y2_z, y3_z, y4_z]
    
    for y in ys_z:
        ax7.plot(x, y)

    ax7.set_title("MSFT - Normalised Stock Price Values from 2019-04-01 to 2023-03-31")
    ax7.set_xlabel("Date")
    ax7.set_ylabel("Normalised Stock Price")
    ax7.set_xticks(x[::163])

    # create the names in the legend with the format `<feature_name> [<unit>]`
    ax7.legend(["Stock Open Price ($)", "Stock High Price ($)", "Stock Low Price ($)", "Stock Close Price ($)"], loc="upper left")


    plt.savefig('normal_plot_with_normalised.png')
    plt.show()
    return fig7, ax7


def normalisation_2(date_values_original, z_minmax_volume):
    fig9, ax9 = plt.subplots(1, figsize=(8, 4))
    
    x = date_values_original


    y1_z = z_minmax_volume
    
    ax9.plot(x, y1_z)

    ax9.set_title("Normalised Volume of Stocks Traded from 2019-04-01 to 2023-03-31")
    ax9.set_xlabel("Date")
    ax9.set_ylabel("MSFT - Normalised Stocks Traded")
    ax9.set_xticks(x[::163])

    # create the names in the legend with the format `<feature_name> [<unit>]`
    ax9.legend(["Normalised Volume"], loc="upper left")

    plt.savefig('volume_plot_with_normalised.png')
    plt.show()
    return fig9, ax9


def z_score_clamp(x, outlier_indices):
    perc_10 = np.quantile(x, 0.25)
    perc_90 = np.quantile(x, 0.75)

    x = np.copy(x)
    for idx in outlier_indices:
        x[idx] = np.clip(x[idx], perc_10, perc_90)

    return x


def clamp_prices(close_values_original, date_values_original, outlier_indices):
    fig11, ax11 = plt.subplots(1, figsize=(8, 4))
    
    x = date_values_original
    y4 = close_values_original

    y4_clamp = z_score_clamp(close_values_original, outlier_indices) 

    ax11.plot(x, y4)


    ax11.plot(x, y4_clamp)

    ax11.set_title("MSFT - Clamped Stock Close Prices from 2019-04-01 to 2023-03-31")
    ax11.set_xlabel("Date")
    ax11.set_ylabel("Stock Price ($)")
    ax11.set_xticks(x[::163])
    
    ax11.legend(["Clamped", "Other"])
    plt.savefig('normal_plot_clamped.png')
    plt.show()

    return fig11, ax11


def clamp_volume(date_values_original, volume_values_original, outlier_indices):
    fig12, ax12 = plt.subplots(1, figsize=(8, 4))
    
    x = date_values_original
    y1 = volume_values_original

    y1_clamp = z_score_clamp(volume_values_original, outlier_indices)

    ax12.plot(x, y1)

    ax12.plot(x, y1_clamp)

    ax12.set_title("MSFT - Clamped Volume of Stocks Traded from 2019-04-01 to 2023-03-31")
    ax12.set_xlabel("Date")
    ax12.set_ylabel("Stocks Traded")
    ax12.set_xticks(x[::163])

    ax12.legend(["Clamped", "Other"])
    plt.savefig('volume_plot_clamped.png')
    plt.show()

    return fig12, ax12




if __name__ == "__main__":  
    client = mongo_connect()
    stock_name = "Microsoft (MSFT)" 
    missing_values(client, stock_name)   
    open_values_list, high_values_list, low_values_list, close_values_list, volume_values_list, date_values_list, open_values_original, high_values_original, low_values_original, close_values_original, volume_values_original, date_values_original, outlier_indices, z_open, z_high, z_low, z_close, z_volume = outliers(client, stock_name)
    z_minmax_open, z_minmax_high, z_minmax_low, z_minmax_close, z_minmax_volume = minmax_norm(z_open, z_high, z_low, z_close, z_volume)
    fig1, ax1 = normal_plotting(open_values_original, high_values_original, low_values_original, close_values_original, date_values_original)
    fig2, axs1 = normal_plotting_with_volume(close_values_original, volume_values_original, date_values_original)
    fig4, ax4 = volume_plotting(date_values_original, date_values_list, volume_values_original, volume_values_list)
    fig5, ax5 = normal_plotting_highlight_outliers(open_values_original, high_values_original, low_values_original, close_values_original, date_values_original, outlier_indices)
    fig6, ax6 = without_outlier_plotting(open_values_list, high_values_list, low_values_list, close_values_list, date_values_list)
    fig7, ax7 = normalisation_1(date_values_original, z_minmax_open, z_minmax_high, z_minmax_low, z_minmax_close)
    fig9, ax9 = normalisation_2(date_values_original, z_minmax_volume)
    fig11, ax11 = clamp_prices(close_values_original, date_values_original, outlier_indices)
    fig12, ax12 = clamp_volume(date_values_original, volume_values_original, outlier_indices)

    client.close()