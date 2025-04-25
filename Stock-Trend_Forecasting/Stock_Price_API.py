from datetime import datetime
import requests
import json
import pandas as pd
import csv

# Here, the useful packages are imported to be used to retrieve the information

# The company for which stock prices will be retrieved will be for Microsoft using AlphaVantage where we will get the information from 1st April 2019 - 31rd March 2023

def call_API(apikey='LLMPRGO977MMGN6I'): # I got an API Key from AlphaVantage
    query = f'https://www.alphavantage.co/query?function=TIME_SERIES_DAILY&symbol=MSFT&outputsize=full&apikey={apikey}'
    request = requests.get(query) # The request is done to get the stock information for Apple
    data = request.json() # The data is made into a JSON which is best way to make this data as it is MetaData
    with open("Stock_Data.json", "w") as file: # This is saved in JSON file with file name of Stock_Data
        json.dump(data, file)


def filter_data(start_date, end_date):
    with open("Stock_Data.json", "r") as file:
        data = json.load(file)
    
    data = data['Time Series (Daily)']

    start_date = datetime.strptime(start_date, '%Y-%m-%d').date()
    end_date = datetime.strptime(end_date, '%Y-%m-%d').date()

    # Making dictionary to put it in
    dates_needed = {}

    for date_string, dates in data.items():

        date_object = datetime.strptime(date_string, "%Y-%m-%d").date()

        if start_date <= date_object <= end_date:
            dates_needed[date_string] = dates

    #dates_needed.reverse()
    reverse_dates_needed = dict(reversed(list(dates_needed.items())))
    with open("Stock_Data_Format.json", "w") as file: 
        json.dump(reverse_dates_needed, file)
    return reverse_dates_needed


if __name__ == "__main__":
    #call_API()
    filter_data('2019-04-01','2023-03-31')
    #df = pd.DataFrame.from_dict(dates_not_needed, orient='index')
    #df = df.reset_index()
    #df.to_csv('Stock_Data_PD.csv', index=False)
