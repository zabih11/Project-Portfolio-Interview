from datetime import datetime
import requests
import json
import pandas as pd
import pymongo
import time
from bson.objectid import ObjectId
import numpy as np
from scipy import stats
import matplotlib.pyplot as plt
from scipy.stats import pearsonr
from statsmodels.tsa.seasonal import seasonal_decompose
from typing import Any, Dict
from statsmodels.tsa.arima.model import ARIMA
from sklearn.metrics import mean_squared_error, mean_absolute_error, r2_score
from statsmodels.tsa.stattools import adfuller
from statsmodels.graphics.tsaplots import plot_acf, plot_pacf
import math

# All necessary packages for the code are importred

def call_API(apikey='LLMPRGO977MMGN6I'): # I got an API Key from AlphaVantage
    query = f'https://www.alphavantage.co/query?function=TIME_SERIES_DAILY&symbol=MSFT&outputsize=full&apikey={apikey}'
    request = requests.get(query) # The request is done to get the stock information for Microsoft
    data = request.json() # The data is made into a JSON which is best way to make this data as it is MetaData
    with open("Stock_Data.json", "w") as file: # This is saved in JSON file with file name of Stock_Data
        json.dump(data, file)
    print("Stock Data for Microsoft from API Saved on JSON File")


def filter_data(start_date, end_date):
    with open("Stock_Data.json", "r") as file:
        data = json.load(file) # The data is loaded from the JSON file and assigned to a variable
    
    data = data['Time Series (Daily)'] # time series data is assigned to the variable

    start_date = datetime.strptime(start_date, '%Y-%m-%d').date() # strptime is used to parse the start and end date into datetime objects with the y-m-d format
    end_date = datetime.strptime(end_date, '%Y-%m-%d').date()

    # Dictionary is made to put the data within the range inside
    dates_needed = {}

    for date_string, dates in data.items(): # loops through each item and the date string is made to be datetime objects which uses if statement to compare to start and end dates

        date_object = datetime.strptime(date_string, "%Y-%m-%d").date()

        if start_date <= date_object <= end_date: # comparison is done between start and end dates
            dates_needed[date_string] = dates # only dates in the limit are added to dicitonary

    #dates_needed.reverse()
    reverse_dates_needed = dict(reversed(list(dates_needed.items()))) # order of data is reversed to get chronological order
    with open("Stock_Data_Format.json", "w") as file: 
        json.dump(reverse_dates_needed, file) # dumped into format JSON file
    print("Stock Data for Microsoft Filtered Saved on newer JSON File")
    return reverse_dates_needed


def income_balance_cash_statement_API(apikey='LLMPRGO977MMGN6I'): # I got an API Key from AlphaVantage
    query_income = f'https://www.alphavantage.co/query?function=INCOME_STATEMENT&symbol=MSFT&apikey={apikey}'
    request_income = requests.get(query_income) # get method from requests used to to qury
    data_income = request_income.json()  # data turned into JSON type
    with open("Income_Statement.json", "w") as file: 
        json.dump(data_income, file) # The data is dumped to the JSON file
    print("Income Statement for Microsoft from API Saved on JSON File")
    query_balance = f'https://www.alphavantage.co/query?function=BALANCE_SHEET&symbol=MSFT&apikey={apikey}'
    request_balance = requests.get(query_balance) 
    data_balance = request_balance.json() 
    with open("Balance_Sheet.json", "w") as file: 
        json.dump(data_balance, file) # The data is dumped to the JSON file
    print("Balance Sheet for Microsoft from API Saved on JSON File")
    query_cash_flow = f'https://www.alphavantage.co/query?function=CASH_FLOW&symbol=MSFT&apikey={apikey}'
    request_cash = requests.get(query_cash_flow) 
    data_cash = request_cash.json() 
    with open("Cash_Flow_Statement.json", "w") as file: 
        json.dump(data_cash, file) # The data is dumped to the JSON file
    print("Cash Flow Statement for Microsoft from API Saved on JSON File")
    query_eps = f'https://www.alphavantage.co/query?function=EARNINGS&symbol=MSFT&apikey={apikey}'
    request_eps = requests.get(query_eps) 
    data_eps = request_eps.json() 
    with open("Earnings_Statement.json", "w") as file: 
        json.dump(data_eps, file) # The data is dumped to the JSON file
    print("Earnings Report for Microsoft from API Saved on JSON File")
    
def filter_data_income_statement(start_date, end_date):
    with open("Income_Statement.json", "r") as file:
        data_income = json.load(file) # The data is loaded from the JSON file and assigned to a variable
    
    annual_report = data_income['annualReports'] # annual report section assigned to the variable
    quarterly_report = data_income['quarterlyReports'] # quarterly report section assigned to the variable

    start_date = datetime.strptime(start_date, '%Y-%m-%d').date() # end and start date parsed into dataetime values
    end_date = datetime.strptime(end_date, '%Y-%m-%d').date()

    dates_needed_income = {} # dictionary made

    for dates in annual_report: # for loop going through the items in annual report to get the dates

        date_string = dates['fiscalDateEnding'] # due to having quarterly dates, fiscal dates are used for the dates strig to parse to datetime
        date_object = datetime.strptime(date_string, "%Y-%m-%d").date()

        if start_date <= date_object <= end_date: # if statement used to check fiscal date 
            dates_needed_income[date_string] = dates

    for dates in quarterly_report: # exact same thing done for quarterly report

        date_string = dates['fiscalDateEnding']
        date_object = datetime.strptime(date_string, "%Y-%m-%d").date()

        if start_date <= date_object <= end_date:
            dates_needed_income[date_string] = dates

    reverse_dates_needed_income = dict(reversed(list(dates_needed_income.items()))) # items reversed to get the right order chronological
    with open("Income_Statement_Format.json", "w") as file: 
        json.dump(reverse_dates_needed_income, file, indent=1)
    print("Income Statement Data for Microsoft Filtered Saved on newer JSON File")

def filter_balance_sheet_statement(start_date, end_date):
    with open("Balance_Sheet.json", "r") as file:
        data_balance = json.load(file) # The data is loaded from the JSON file and assigned to a variable
    
    annual_report = data_balance['annualReports'] # annual reports assigned to variable
    quarterly_report = data_balance['quarterlyReports'] # quarterly reports assigned to variables

    start_date = datetime.strptime(start_date, '%Y-%m-%d').date() # start and end date parsed into datetime object
    end_date = datetime.strptime(end_date, '%Y-%m-%d').date()

    dates_needed_balance = {}

    for dates in annual_report: # for loop used to find the fiscal dates, date string parsed into datetime and checked between the start and end dates

        date_string = dates['fiscalDateEnding']
        date_object = datetime.strptime(date_string, "%Y-%m-%d").date()

        if start_date <= date_object <= end_date:
            dates_needed_balance[date_string] = dates

    for dates in quarterly_report: # same thing happens for quarterly reports

        date_string = dates['fiscalDateEnding']
        date_object = datetime.strptime(date_string, "%Y-%m-%d").date()

        if start_date <= date_object <= end_date:
            dates_needed_balance[date_string] = dates

    reverse_dates_needed_balance = dict(reversed(list(dates_needed_balance.items()))) # reversed for chronological order
    with open("Balance_Sheet_Format.json", "w") as file: 
        json.dump(reverse_dates_needed_balance, file, indent=1)
    print("Balance Sheet Data for Microsoft Filtered Saved on newer JSON File")

def filter_cash_flow_statement(start_date, end_date):
    with open("Cash_Flow_Statement.json", "r") as file:
        data_cash = json.load(file) # The data is loaded from the JSON file and assigned to a variable
    
    annual_report = data_cash['annualReports'] # annual and quarterly reports assigned to variables
    quarterly_report = data_cash['quarterlyReports']

    start_date = datetime.strptime(start_date, '%Y-%m-%d').date() # dates parsed into datetimes
    end_date = datetime.strptime(end_date, '%Y-%m-%d').date()

    dates_needed_cash = {} # dictionary made to get the right dates' information in

    for dates in annual_report: # for loop used to iterate through fiscal dates by using parsed date strings

        date_string = dates['fiscalDateEnding']
        date_object = datetime.strptime(date_string, "%Y-%m-%d").date()

        if start_date <= date_object <= end_date:
            dates_needed_cash[date_string] = dates

    for dates in quarterly_report: # same thing as annual reports is done 

        date_string = dates['fiscalDateEnding']
        date_object = datetime.strptime(date_string, "%Y-%m-%d").date()

        if start_date <= date_object <= end_date:
            dates_needed_cash[date_string] = dates

    reverse_dates_needed_cash = dict(reversed(list(dates_needed_cash.items()))) # order is reversed to get chronological order
    with open("Cash_Flow_Statement_Format.json", "w") as file: 
        json.dump(reverse_dates_needed_cash, file, indent=1)
    print("Cash Flow Statement Data for Microsoft Filtered Saved on newer JSON File")

def filter_eps_statement(start_date, end_date):
    with open("Earnings_Statement.json", "r") as file:
        data_eps = json.load(file) # The data is loaded from the JSON file and assigned to a variable
    
    annual_earning = data_eps['annualEarnings'] # both earnings reports data assigned to respective variables
    quarterly_earning = data_eps['quarterlyEarnings']

    start_date = datetime.strptime(start_date, '%Y-%m-%d').date() # parsed the start and end dates into datetime objects
    end_date = datetime.strptime(end_date, '%Y-%m-%d').date()

    dates_needed_eps = {}

    for dates in annual_earning:

        date_string = dates['fiscalDateEnding']
        date_object = datetime.strptime(date_string, "%Y-%m-%d").date()

        if start_date <= date_object <= end_date:
            dates_needed_eps[date_string] = dates

    for dates in quarterly_earning:

        date_string = dates['fiscalDateEnding']
        date_object = datetime.strptime(date_string, "%Y-%m-%d").date()

        if start_date <= date_object <= end_date:
            dates_needed_eps[date_string] = dates

    reverse_dates_needed_eps = dict(reversed(list(dates_needed_eps.items()))) # order of the data is reversed to get chronological order of dates
    with open("Earnings_Statement_Format.json", "w") as file: 
        json.dump(reverse_dates_needed_eps, file, indent=1) # data is dumped to JSON file
    print("Earnings Report Data for Microsoft Filtered Saved on newer JSON File")    


def nyt_api(): # New York Times API
    api_key = 'gw5RRpLJhzfCX1YlLGAfiYyBAhXUk7HS' # API key for NYT
    base_url = 'https://api.nytimes.com/svc/search/v2/articlesearch.json' # This is the base url for the articles seach where querys are taken in
    # Date ranges are set for times of where data needs explaining inlduding peaks, dips, and times of outliers
    begin_date = '20200220' # Big dip during start of lockdown
    end_date = '20200415'

    begin_date1 = '20200725' # first small peak
    end_date1 = '20200805'

    begin_date2 = '20210125' # outliers 1
    end_date2 = '20210129'

    begin_date3 = '20220120' # outliers 2
    end_date3 = '20220129'

    begin_date4 = '20230315' # Outlier point
    end_date4 = '20230319'

    begin_date5 = '20200125' # sudden drop from smaller peak
    end_date5 = '20200229'

    begin_date6 = '20211005'
    end_date6 = '20220110'

    begin_date7 = '20220825' # outlier period
    end_date7 = '20220915'

    begin_date8 = '20221215' # outliers
    end_date8 = '20230115'

    # Queries are made for each time period and using query keyword of Microsoft to get news articles related to that. this is done for each query and the sort is done by relevance.
    query_params = {
        'q': 'Microsoft',
        'begin_date': begin_date,
        'end_date': end_date,
        'api-key': api_key, # API key used for the query
        'sort': 'relevance'
    }

    query_params1 = {
        'q': 'Microsoft',
        'begin_date': begin_date1,
        'end_date': end_date1,
        'api-key': api_key,
        'sort': 'relevance'
    }

    query_params2 = {
        'q': 'Microsoft',
        'begin_date': begin_date2,
        'end_date': end_date2,
        'api-key': api_key,
        'sort': 'relevance'
    }

    query_params3 = {
        'q': 'Microsoft',
        'begin_date': begin_date3,
        'end_date': end_date3,
        'api-key': api_key,
        'sort': 'relevance'
    }

    query_params4 = {
        'q': 'Microsoft',
        'begin_date': begin_date4,
        'end_date': end_date4,
        'api-key': api_key,
        'sort': 'relevance'
    }

    query_params5 = {
        'q': 'Microsoft',
        'begin_date': begin_date5,
        'end_date': end_date5,
        'api-key': api_key,
        'sort': 'relevance'
    }

    query_params6 = {
        'q': 'Microsoft',
        'begin_date': begin_date6,
        'end_date': end_date6,
        'api-key': api_key,
        'sort': 'relevance'
    }

    query_params7 = {
        'q': 'Microsoft',
        'begin_date': begin_date7,
        'end_date': end_date7,
        'api-key': api_key,
        'sort': 'relevance'
    }

    query_params8 = {
        'q': 'Microsoft',
        'begin_date': begin_date8,
        'end_date': end_date8,
        'api-key': api_key,
        'sort': 'relevance'
    }

    
    response = requests.get(base_url, query_params) # get is used from request to get the information
    data = response.json() # the data is made into JSON format
    with open("NYT.json", "w") as file:
        json.dump(data, file, indent=1) # data is dumped to JSON file
    print("1st News Query about Microsoft from NYT API Saved on JSON File")
    time.sleep(12) # Sleep of 12 seconds is used as there is 5 request per minute limit so 12 secinds ensures max rate matches rate limit

    response1 = requests.get(base_url, query_params1)
    data_out1 = response1.json()
    with open("NYT_out1.json", "w") as file:
        json.dump(data_out1, file, indent=1)
    print("2nd News Query about Microsoft from NYT API Saved on JSON File")
    time.sleep(12)

    response2 = requests.get(base_url, query_params2)
    data_out2 = response2.json()
    with open("NYT_out2.json", "w") as file:
        json.dump(data_out2, file, indent=1)
    print("3rd News Query about Microsoft from NYT API Saved on JSON File")
    time.sleep(12)

    response3 = requests.get(base_url, query_params3)
    data_out3 = response3.json()
    with open("NYT_out3.json", "w") as file:
        json.dump(data_out3, file, indent=1)
    print("4th News Query about Microsoft from NYT API Saved on JSON File")
    time.sleep(12)

    response4 = requests.get(base_url, query_params4)
    data_out4 = response4.json()
    with open("NYT_out4.json", "w") as file:
        json.dump(data_out4, file, indent=1)
    print("5th News Query about Microsoft from NYT API Saved on JSON File")
    time.sleep(12)

    response5 = requests.get(base_url, query_params5)
    data_out5 = response5.json()
    with open("NYT_before_covid.json", "w") as file:
        json.dump(data_out5, file, indent=1)
    print("6th News Query about Microsoft from NYT API Saved on JSON File")
    time.sleep(12)

    response6 = requests.get(base_url, query_params6)
    data_out6 = response6.json()
    with open("NYT_biggest_peak.json", "w") as file:
        json.dump(data_out6, file, indent=1)
    print("7th News Query about Microsoft from NYT API Saved on JSON File")
    time.sleep(12)

    response7 = requests.get(base_url, query_params7)
    data_out7 = response7.json()
    with open("NYT_peak_in_downward.json", "w") as file:
        json.dump(data_out7, file, indent=1)
    print("8th News Query about Microsoft from NYT API Saved on JSON File")
    time.sleep(12)

    response8 = requests.get(base_url, query_params8)
    data_out8 = response8.json()
    with open("NYT_new_upwards.json", "w") as file:
        json.dump(data_out8, file, indent=1)
    print("9th News Query about Microsoft from NYT API Saved on JSON File")


def mongo_connect(): # connection to mongo is done to mongo using person URI and deployment is pinged
    uri = "mongodb+srv://zabihm11:c51P8iuUJMz3KvRS@cluster0.xe8a23d.mongodb.net/?retryWrites=true&w=majority" 
    # Create a new client and connect to the server
    client = pymongo.MongoClient(uri)
    # Send a ping to confirm a successful connection
    try:
        client.admin.command('ping')
        print("Pinged your deployment. You successfully connected to MongoDB!")
    except Exception as e:
        print(e) # exception is done if connection is done wrong
    
    return client


def empty_or_float(number):
    if number == "": # checks if the data is empty and makes it a null value, else it turns into float
        return None
    else:
        return float(number)

def empty_or_int(number):
    if number == "": # checks if the data is empty and makes it a null value, else it turns into integer
        return None
    else:
        return int(number)

def add_mongo(client, stock_name):
    with open("Stock_Data_Format.json", "r") as file:
        reverse_dates_needed = json.load(file) # The data is loaded from the JSON file and assigned to a variable
    
    db = client["Stock_Data"] # database calles Stock_Data is made
    collections = db[stock_name] # collection within the database is made for Microsoft 
    data_formatted = [] # a list is made to make a list of dictionaries
    for date, data_point in reverse_dates_needed.items(): # iteration through the data points
        existing_document = collections.find_one({"date": date}) # uses find_one function to check if any of the dates within the documents are alredy there
        if existing_document == None: # if not exisiting
            formatted_data_mongo = { # dictionary is made where the data point goes through the key names and gives it a label for the field
                "date": date, 
                "open": empty_or_float(data_point["1. open"]),
                "high": empty_or_float(data_point["2. high"]),
                "low": empty_or_float(data_point["3. low"]),
                "close": empty_or_float(data_point["4. close"]),
                "volume": empty_or_int(data_point["5. volume"])
            }
            data_formatted.append(formatted_data_mongo) # the dictionary os appended to the list

    if len(data_formatted) > 0: # if there is anything in the list, it is inserted using the pymongo function - insert_many
        collections.insert_many(data_formatted)
        print("Successfully Uploaded Stock Data to MongoDB!")
    else:
        print("All this data already exists!")

def add_mongo_info(client):
    db = client["Stock_Information"] # new databse is made for stock information
    
    with open("Balance_Sheet_Format.json", "r") as file: 
        data_balance = json.load(file) # The data is loaded from the JSON file and assigned to a variable

    collections1 = db["Microsoft Balance Sheet"] # collection is made for the balance sheet
    balance_data_formatted = [] # list is made
    balance_data_formatted.append(data_balance) # data from JSON is appended to list
    collections1.insert_many(balance_data_formatted) # the list is inserted to the collection
    # the same process is done for all the stock information document types
    with open("Income_Statement_Format.json", "r") as file:
        data_income = json.load(file) # The data is loaded from the JSON file and assigned to a variable
    
    collections2 = db["Microsoft Income Statement"]
    income_statement_formatted = []
    income_statement_formatted.append(data_income)
    collections2.insert_many(income_statement_formatted)

    with open("Cash_Flow_Statement_Format.json", "r") as file:
        data_cash = json.load(file) # The data is loaded from the JSON file and assigned to a variable
    
    collections3 = db["Microsoft Cash Flow Statement"]
    cash_flow_statement_formatted = []
    cash_flow_statement_formatted.append(data_cash)
    collections3.insert_many(cash_flow_statement_formatted)

    with open("Earnings_Statement_Format.json", "r") as file:
        data_eps = json.load(file) # The data is loaded from the JSON file and assigned to a variable
    
    collections4 = db["Microsoft Earnings Statement"]
    eps_statement_formatted = []
    eps_statement_formatted.append(data_eps)
    collections4.insert_many(eps_statement_formatted)

    db1 = client["Microsoft_News"] # a new database is made with the name microsoft news

    with open("NYT.json", "r") as file:
        data_nyt = json.load(file) # The data is loaded from the JSON file and assigned to a variable

    collections5 = db1["New York Times - First"] # collection is made, one for each request of data done
    nyt_formatted = [] # list is made for the data to go inside
    docs_nyt = data_nyt['response']['docs'] # in the file, the docs that are located within the key response is accessed
    for data_point in docs_nyt: # for loop iterates through each part of the file
        formatted_data_nyt = { # dictionary goes through and only saves the important information and disregards the useless data
            "Abstract": data_point["abstract"], # find the key name and saves the value to new field name
            "Web URL": data_point["web_url"],
            "Snippet": data_point["snippet"],
            "Lead Paragraph": data_point["lead_paragraph"],
            "Source": data_point["source"]
        }
        nyt_formatted.append(formatted_data_nyt) # dictionary is appende to the list

    collections5.insert_many(nyt_formatted) # all values of the list are inserted to mongodb

    with open("NYT_out1.json", "r") as file:
        data_nyt_out1 = json.load(file) # The data is loaded from the JSON file and assigned to a variable

    collections6 = db1["New York Times - Outliers 1"]
    nyt_out1_formatted = []
    docs_nyt_out1 = data_nyt_out1['response']['docs']
    for data_point in docs_nyt_out1:
        formatted_data_nyt_out1 = {
            "Abstract": data_point["abstract"],
            "Web URL": data_point["web_url"],
            "Snippet": data_point["snippet"],
            "Lead Paragraph": data_point["lead_paragraph"],
            "Source": data_point["source"]
        }
        nyt_out1_formatted.append(formatted_data_nyt_out1)

    collections6.insert_many(nyt_out1_formatted)

    with open("NYT_out2.json", "r") as file:
        data_nyt_out2 = json.load(file) # The data is loaded from the JSON file and assigned to a variable

    collections7 = db1["New York Times - Outliers 2"]
    nyt_out2_formatted = []
    docs_nyt_out2 = data_nyt_out2['response']['docs']
    for data_point in docs_nyt_out2:
        formatted_data_nyt_out2 = {
            "Abstract": data_point["abstract"],
            "Web URL": data_point["web_url"],
            "Snippet": data_point["snippet"],
            "Lead Paragraph": data_point["lead_paragraph"],
            "Source": data_point["source"]
        }
        nyt_out2_formatted.append(formatted_data_nyt_out2)

    collections7.insert_many(nyt_out2_formatted)

    with open("NYT_out3.json", "r") as file:
        data_nyt_out3 = json.load(file) # The data is loaded from the JSON file and assigned to a variable

    collections8 = db1["New York Times - Outliers 3"]
    nyt_out3_formatted = []
    docs_nyt_out3 = data_nyt_out3['response']['docs']
    for data_point in docs_nyt_out3:
        formatted_data_nyt_out3 = {
            "Abstract": data_point["abstract"],
            "Web URL": data_point["web_url"],
            "Snippet": data_point["snippet"],
            "Lead Paragraph": data_point["lead_paragraph"],
            "Source": data_point["source"]
        }
        nyt_out3_formatted.append(formatted_data_nyt_out3)

    collections8.insert_many(nyt_out3_formatted)

    with open("NYT_out4.json", "r") as file:
        data_nyt_out4 = json.load(file) # The data is loaded from the JSON file and assigned to a variable

    collections9 = db1["New York Times - Outliers 4"]
    nyt_out4_formatted = []
    docs_nyt_out4 = data_nyt_out4['response']['docs']
    for data_point in docs_nyt_out4:
        formatted_data_nyt_out4 = {
            "Abstract": data_point["abstract"],
            "Web URL": data_point["web_url"],
            "Snippet": data_point["snippet"],
            "Lead Paragraph": data_point["lead_paragraph"],
            "Source": data_point["source"]
        }
        nyt_out4_formatted.append(formatted_data_nyt_out4)

    collections9.insert_many(nyt_out4_formatted)

    with open("NYT_before_covid.json", "r") as file:
        data_nyt_before_covid = json.load(file) # The data is loaded from the JSON file and assigned to a variable

    collections10 = db1["New York Times - Before COVID"]
    nyt_formatted_before_covid = []
    docs_nyt_before_covid = data_nyt_before_covid['response']['docs']
    for data_point in docs_nyt_before_covid:
        formatted_data_nyt_before_covid = {
            "Abstract": data_point["abstract"],
            "Web URL": data_point["web_url"],
            "Snippet": data_point["snippet"],
            "Lead Paragraph": data_point["lead_paragraph"],
            "Source": data_point["source"]
        }
        nyt_formatted_before_covid.append(formatted_data_nyt_before_covid)

    collections10.insert_many(nyt_formatted_before_covid)

    with open("NYT_biggest_peak.json", "r") as file:
        data_nyt_biggest_peak = json.load(file) # The data is loaded from the JSON file and assigned to a variable

    collections11 = db1["New York Times - Biggest Peak"]
    nyt_formatted_biggest_peak = []
    docs_nyt_biggest_peak = data_nyt_biggest_peak['response']['docs']
    for data_point in docs_nyt_biggest_peak:
        formatted_data_nyt_biggest_peak = {
            "Abstract": data_point["abstract"],
            "Web URL": data_point["web_url"],
            "Snippet": data_point["snippet"],
            "Lead Paragraph": data_point["lead_paragraph"],
            "Source": data_point["source"]
        }
        nyt_formatted_biggest_peak.append(formatted_data_nyt_biggest_peak)

    collections11.insert_many(nyt_formatted_biggest_peak)

    with open("NYT_peak_in_downward.json", "r") as file:
        data_nyt_peak_in_downward = json.load(file) # The data is loaded from the JSON file and assigned to a variable

    collections12 = db1["New York Times - Peak in Downward Trend"]
    nyt_formatted_peak_in_downward = []
    docs_nyt_peak_in_downward = data_nyt_peak_in_downward['response']['docs']
    for data_point in docs_nyt_peak_in_downward:
        formatted_data_nyt_peak_in_downward = {
            "Abstract": data_point["abstract"],
            "Web URL": data_point["web_url"],
            "Snippet": data_point["snippet"],
            "Lead Paragraph": data_point["lead_paragraph"],
            "Source": data_point["source"]
        }
        nyt_formatted_peak_in_downward.append(formatted_data_nyt_peak_in_downward)

    collections12.insert_many(nyt_formatted_peak_in_downward)

    with open("NYT_new_upwards.json", "r") as file:
        data_nyt_new_upwards = json.load(file) # The data is loaded from the JSON file and assigned to a variable

    collections13 = db1["New York Times - new upwards"]
    nyt_formatted_new_upwards = []
    docs_nyt_new_upwards = data_nyt_new_upwards['response']['docs']
    for data_point in docs_nyt_new_upwards:
        formatted_data_nyt_new_upwards = {
            "Abstract": data_point["abstract"],
            "Web URL": data_point["web_url"],
            "Snippet": data_point["snippet"],
            "Lead Paragraph": data_point["lead_paragraph"],
            "Source": data_point["source"]
        }
        nyt_formatted_new_upwards.append(formatted_data_nyt_new_upwards)

    collections13.insert_many(nyt_formatted_new_upwards)
    print("Successfully Stored All Microsoft Stock Information and News Articles on MongoDB")
    

def create(client, item: Any) -> bool: # uses same signature as in the description of task
    """
    Inserts new item into Microsoft stock data collection in the Stock_Data database stored in MongoDB.

    Parameters:
    client (MongoClient): The MongoDB client connected to the database.
    item (Any): The item that is inserted.

    Returns:
    bool: True if insertion is successful, and returns False if it is not.
    """
    db = client["Stock_Data"] # goes to stock data databse
    collections = db["Microsoft (MSFT)"] # accesses the microssodt stock data collection
    inserted = collections.insert_one(item) # insert_one function is used with item proprties put in as dictionary format
    if inserted.inserted_id: # if ID was made for the item, the item is successfully made
        print("Item was successfully inserted!")
        idee = str(inserted.inserted_id) # gets and print the id as a string
        print(idee)
        return True, idee # returns boolean true and id
    else:
        print("Insertion has failed!")
        return False # returns boolean false
    
def read(client, query: str) -> Any:
    """
    Retrieves items from Microsoft stock data collection in the Stock_Data MongoDB database 
    based on a query using the find function.

    Parameters:
    client (MongoClient): The MongoDB client connected to the database.
    query (str): A query string to be found based on the item property and retrieves items in 
    list.

    Returns:
    Any: A list of items matching the query, if no matches are found then an empty list is 
    returned.
    """
    db = client["Stock_Data"]
    collections = db["Microsoft (MSFT)"]
    retrieved = list(collections.find(query)) # find function is used with string query with key and value and a list of results is made
    if not retrieved: # if not found, message is printed
        print("No items matched your query!")
    else:
        print("Matching data to query was retrieved.") # if matched, the item data is printed
        print(retrieved)
    return retrieved


def update(client, item_id: Any, properties: Dict) -> bool:
    """
    Updates an item in the Microsoft stock data collection in the MongoDB database.

    Parameters:
    client (MongoClient): The MongoDB client connected to the database.
    item_id (Any): Item _id of the item is taken in.
    properties (Dict): Dictionary with the properties to be updated is used.

    Returns:
    bool: Returns True if the update is successful and False if it is unsuccessful or 
    if no item with the id is found.
    """
    db = client["Stock_Data"]
    collections = db["Microsoft (MSFT)"]
    existing_db = collections.find({"_id": item_id}) # find function is used to find item using the id
    if len(list(existing_db)) > 0: # if the results has any values then properties in dictionary form are set with the pymongo $set function
        update_parts = {"$set": properties}
        updating = collections.update_one({"_id": item_id}, update_parts) # item with the right id is updates with right properties
        if updating.modified_count: # if modified, success message is sent and boolean true returns
            print("Item was updated in database!")
            return True
        else:
            print("Update was unsuccessful!") # returns false if modifcation did not tally
            return False
    else:
        print("Item with that id was not found!") # if nothing is found by id initially, returns a false
        return False


def delete(client, item_id: str) -> bool:
    """
    Deletes an item from the Microsoft stock data collection in the MongoDB database.

    Parameters:
    client (MongoClient): The MongoDB client connected to the database.
    item_id (str): Item _id of the item to be deleted is taken as string.

    Returns:
    bool: Returns True if the deletion is successful, and returns False if item _id is
    not founf or if deletion was unsuccessful.
    """
    db = client["Stock_Data"]
    collections = db["Microsoft (MSFT)"]
    existing_db = collections.find({"_id":  item_id}) # item is found by its id usinf find function
    if len(list(existing_db)) > 0: # if list has anay values then deletes each one based on the id
        collections.delete_one({"_id":  item_id})
        if len(list(existing_db)) == 0: # list length is checked again to confirm deletion and true is returned
            print("Item was deleted from database!")
            return True
        else:
            print("Deletion was unsuccessful!") # returns false if deletion did not work
            return False
    else:
        print("Item with that id was not found!") # returns false if id was initially not found
        return False

def missing_values(client, stock_name):
    db = client["Stock_Data"]
    collections = db[stock_name] # microsoft stock data collaection is accessed from the database
    found_missing = False
    
    missing_data = {"$or": [{"date": None},{"open": None}, {"high": None}, {"low": None}, {"close": None}, {"volume": None}]}
    # dictionary using the $or function checking if any of the fields have a null value and queries using the find function
    days_with_missing_data = collections.find(missing_data)
    
    for docs in days_with_missing_data: # for loop to go through the documents that have missing values
        found_missing = True
        doc_id = str(docs["_id"]) # id and date of the document are accessed to be printed and made known of their deletion
        date = docs["date"]
        print(f"Deleting Day With ObjectId: {doc_id} and Date: {date} Due to Having an Empty Value(s).")
        collections.delete_one({"_id": docs["_id"]}) # delete_one is used to delete document using its id and then for loop goes again depending on the documents with missing values
    
    if found_missing == False:
        print("There were No Days With Missing Data") # if not missing values were found seen by if found_missing stay false, message is printed
    else:
        print("All Days With Missing Data Were Deleted") # when deletions are done, the message is printed

    return stock_name

def outliers(client, stock_name):
    # The outliers of each part of the data will be found using the z-score and if it is more 3 or less than -3 then considered an outlier
    db = client["Stock_Data"]
    collections = db[stock_name]
    values = list(collections.find().sort("date", pymongo.ASCENDING)) # values of the collection's date are made in asscending order due to accessing the collection twice where an error arised and outliers were psuhed to back. The prevents that and leaves real order

    df = pd.DataFrame(values) # data made into panda dataframe
    date_values_original = df["date"].copy().to_numpy() # each field of the dataframe is accessed and copied, then turned to numpy arrays and corect data type to allow for numpy functions to work
    open_values_original = df["open"].copy().to_numpy().astype(float)
    high_values_original = df["high"].copy().to_numpy().astype(float)
    low_values_original = df["low"].copy().to_numpy().astype(float)
    close_values_original = df["close"].copy().to_numpy().astype(float)
    volume_values_original = df["volume"].copy().to_numpy().astype(int)

    z_open = stats.zscore(open_values_original) # z score function from stats is used to calulate the z score for each value in the numpy array of each numpyt array
    z_high = stats.zscore(high_values_original)
    z_low = stats.zscore(low_values_original)
    z_close = stats.zscore(close_values_original)
    z_volume = stats.zscore(volume_values_original)

    threshold = 3
    is_outlier_open = abs(z_open) > threshold # absolute value of z scored is copared to threshold of 3 for each array
    is_outlier_high = abs(z_high) > threshold
    is_outlier_low = abs(z_low) > threshold
    is_outlier_close = abs(z_close) > threshold
    is_outlier_volume = abs(z_volume) > threshold

    outlier_indices_open = np.nonzero(is_outlier_open) # nonzero is used to get indices of nonzero values in the array, this will shows indices of the outliers
    print("The indices of outliers at open times are:", list(outlier_indices_open[0]))

    outlier_indices_high = np.nonzero(is_outlier_high)
    print("The indices of outliers at high price are:", list(outlier_indices_high[0]))

    outlier_indices_low = np.nonzero(is_outlier_low)
    print("The indices of outliers at low price are:", list(outlier_indices_low[0]))

    outlier_indices_close = np.nonzero(is_outlier_close)
    print("The indices of outliers at close times are:", list(outlier_indices_close[0]))

    outlier_indices_volume = np.nonzero(is_outlier_volume)
    print("The indices of outliers for volume are:", list(outlier_indices_volume[0]))
    outlier_indices = list(outlier_indices_volume[0]) # outliers only lie in the volume array so it is made into list and for loop is used to get actual volume value for each volume indice
    outlier_value_volume = [volume_values_original[indices] for indices in outlier_indices_volume[0]]
    print("Volume values at desired indices:", outlier_value_volume)

    found_outlier = False
    int_outlier_value_volume = [int(value) for value in outlier_value_volume] # makes all the values of the actual volumes of outlier into integers
    days_with_volume_outliers = collections.find({"volume": {"$in": int_outlier_value_volume}}) # $in is usd to chekc all the values of volume on mongodb have the volume of the outliers

    
    for docs in days_with_volume_outliers: # same method as missing values id used to delete the documents by their id
        found_outlier = True
        doc_id = str(docs["_id"])
        date = docs["date"]
        volume = docs["volume"]
        print(f"Deleting Day With ObjectId: {doc_id} and Date: {date} Due to Having an Outlier with Volume: {volume}.") # volume of the outlier is also shown which is not done in the missing values method
        collections.delete_one({"_id": docs["_id"]})
    
    if found_outlier == False:
        print("There were No Days With Outliers")
    else:
        print("All Days With Outliers Were Deleted")

    collections1 = db[stock_name]
    values1 = list(collections1.find()) # collection is accessed again and data without outliers is retirved to be used in plots

    df1 = pd.DataFrame(values1) # data made into data frame and assigned varibles to be used in plotting
    date_values_list = df1["date"].to_numpy().tolist()
    open_values_list = df1["open"].to_numpy().astype(float).tolist()
    high_values_list = df1["high"].to_numpy().astype(float).tolist()
    low_values_list = df1["low"].to_numpy().astype(float).tolist()
    close_values_list = df1["close"].to_numpy().astype(float).tolist()
    volume_values_list = df1["volume"].to_numpy().astype(int).tolist()

    # all lists, arrays, outlier indices and z scores are returned to be used in plotting within other functions
    return open_values_list, high_values_list, low_values_list, close_values_list, volume_values_list, date_values_list, open_values_original, high_values_original, low_values_original, close_values_original, volume_values_original, date_values_original, outlier_indices, z_open, z_high, z_low, z_close, z_volume

def minmax_norm(z_open, z_high, z_low, z_close, z_volume):
    z_open = np.array(z_open) # z score values are turned into numpy arrays
    z_high = np.array(z_high)
    z_low = np.array(z_low)
    z_close = np.array(z_close)
    z_volume = np.array(z_volume)
    
    z_minmax_open = (z_open - np.min(z_open)) / (np.max(z_open) -np. min(z_open)) # min max normalisation is done to all the z values of each price and volume using same equation
    z_minmax_high = (z_high - np.min(z_high)) / (np.max(z_high) - np.min(z_high))
    z_minmax_low = (z_low - np.min(z_low)) / (np.max(z_low) - np.min(z_low))
    z_minmax_close = (z_close - np.min(z_close)) / (np.max(z_close) - np.min(z_close))
    z_minmax_volume = (z_volume - np.min(z_volume)) / (np.max(z_volume) - np.min(z_volume))
    # returned values to be used in furutue normalisation plots
    return z_minmax_open, z_minmax_high, z_minmax_low, z_minmax_close, z_minmax_volume

def normal_plotting(open_values_original, high_values_original, low_values_original, close_values_original, date_values_original):
    
    fig1, ax1 = plt.subplots(1, figsize=(8, 4)) # fig and ax are used to make a plot and matplotlib is used with plt to make a sublot of certain size
    # the plotting is all done on the axes which are contained within the figure
    x = date_values_original
    y1 = open_values_original # all variables for data before outliers were removed
    y2 = high_values_original
    y3 = low_values_original
    y4 = close_values_original

    ys = [y1, y2, y3, y4]
    
    for y in ys: # iteration through list to get all lines on same plot
        ax1.plot(x, y)

    ax1.set_title("MSFT - Stock Prices at Open, High, Low and Close from 2019-04-01 to 2023-03-31") # titles and labels are applies as seen fit
    ax1.set_xlabel("Date")
    ax1.set_ylabel("Stock Price ($)")
    ax1.set_xticks(x[::163]) # this allows for skips of 163 days between each date data point, with it being business days, almost shows every date till end of march 2023 with the jumps

    # create the names in the legend with the format `<feature_name> [<unit>]`
    ax1.legend(["Stock Open Price ($)", "Stock High Price ($)", "Stock Low Price ($)", "Stock Close Price ($)"])
    plt.savefig('normal_plot.png') # figure is saved to png file
    return fig1, ax1

def normal_plotting_with_volume(close_values_original, volume_values_original, date_values_original):
    
    fig2, ax2 = plt.subplots(1, figsize=(8, 4)) 
    
    x = date_values_original # plotting close price values before removing outliers and volume befor outliers removes
    y1 = close_values_original
    y2 = volume_values_original

    ax2.plot(x, y1, color='green', label="Stock Price ($)") # colour and label made in the plot part due to having different axis

    # format the axes
    ax2.set_title("MSFT - Close Stock Prices and Volume from 2019-04-01 to 2023-03-31")
    ax2.set_xlabel("Date")
    ax2.set_ylabel("Stock Price ($)")
    ax2.set_xticks(x[::163])

    ax3 = ax2.twinx() # ax3 made opposite of ax2

    ax3.plot(x, y2, color='purple', label="Volume Traded") # volume is plotted using the other axis on the same plot

    ax3.set_ylabel("Volume Traded")

    # create the names in the legend with the format `<feature_name> [<unit>]`
    ax2.legend(loc="upper left")
    ax3.legend(loc="upper right") # legends location are specified

    plt.savefig('normal_plot_with_volume.png') # plot saved
    return fig2, (ax2, ax3)

def normal_plotting_highlight_outliers(open_values_original, high_values_original, low_values_original, close_values_original, date_values_original, outlier_indices):
    
    fig5, ax5 = plt.subplots(1, figsize=(8, 4))
    
    x = date_values_original
    y1 = open_values_original # normal stock price plot but with hihglighted outliers
    y2 = high_values_original
    y3 = low_values_original
    y4 = close_values_original

    x_outlier = date_values_original[outlier_indices] # indices of the data before outlier removal are found
    y1_outlier = open_values_original[outlier_indices]
    y2_outlier = high_values_original[outlier_indices]
    y3_outlier = low_values_original[outlier_indices]
    y4_outlier = close_values_original[outlier_indices]

    ys = [y1, y2, y3, y4]
    ys_outlier = [y1_outlier, y2_outlier, y3_outlier, y4_outlier]
    
    for y in ys:
        ax5.plot(x, y) # normal plot for all stock prices using for loop
    for y in ys_outlier:
        ax5.scatter(x_outlier, y, color="black", alpha=0.5) # scatter of the values with outliers and opacity is reduced

    # format the axes
    ax5.set_title("MSFT - Highlighted Outlier on Stock Prices from 2019-04-01 to 2023-03-31")
    ax5.set_xlabel("Date")
    ax5.set_ylabel("Stock Price ($)")
    ax5.set_xticks(x[::163])

    # create the names in the legend with the format `<feature_name> [<unit>]`
    ax5.legend(["Stock Open Price ($)", "Stock High Price ($)", "Stock Low Price ($)", "Stock Close Price ($)"])

    plt.savefig('normal_plot_highlight_outliers.png')
    return fig5, ax5


def without_outlier_plotting(open_values_list, high_values_list, low_values_list, close_values_list, date_values_list):
    
    fig6, ax6 = plt.subplots(1, figsize=(8, 4))
    
    x = date_values_list
    y1 = open_values_list # stock price data with the outliers removed is plotted against the date
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
    return fig6, ax6

def volume_plotting(date_values_original, date_values_list, volume_values_original, volume_values_list):
    
    fig4, ax4 = plt.subplots(1, figsize=(8, 4))
    
    x1 = date_values_original
    x2 = date_values_list
    y1 = volume_values_original # data of volume with the outliers is plotted on the same as volume data without outliers
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
    return fig4, ax4

def normalisation_1(date_values_original, z_minmax_open, z_minmax_high, z_minmax_low, z_minmax_close):
    fig7, ax7 = plt.subplots(1, figsize=(8, 4))
    
    x = date_values_original


    y1_z = z_minmax_open # minmax values from minmax funtion created are used to get z score min max normalised data
    y2_z = z_minmax_high
    y3_z = z_minmax_low
    y4_z = z_minmax_close

    ys_z = [y1_z, y2_z, y3_z, y4_z]
    
    for y in ys_z: # plotted in the same way as before
        ax7.plot(x, y)

    ax7.set_title("MSFT - Normalised Stock Price Values from 2019-04-01 to 2023-03-31")
    ax7.set_xlabel("Date")
    ax7.set_ylabel("Normalised Stock Price")
    ax7.set_xticks(x[::163])

    # create the names in the legend with the format `<feature_name> [<unit>]`
    ax7.legend(["Stock Open Price ($)", "Stock High Price ($)", "Stock Low Price ($)", "Stock Close Price ($)"], loc="upper left")
    # location of legend is chosen due to more than normal inteference with th

    plt.savefig('normal_plot_with_normalised.png')
    return fig7, ax7


def normalisation_2(date_values_original, z_minmax_volume):
    fig9, ax9 = plt.subplots(1, figsize=(8, 4))
    
    x = date_values_original # same thing as other normalisation is done but using the minmaxed z score normalisaiton of volume


    y1_z = z_minmax_volume
    
    ax9.plot(x, y1_z)

    ax9.set_title("MSFT - Normalised Volume of Stocks Traded from 2019-04-01 to 2023-03-31")
    ax9.set_xlabel("Date")
    ax9.set_ylabel("Normalised Stocks Traded")
    ax9.set_xticks(x[::163])

    # create the names in the legend with the format `<feature_name> [<unit>]`
    ax9.legend(["Normalised Volume"], loc="upper left")

    plt.savefig('volume_plot_with_normalised.png')
    return fig9, ax9


def z_score_clamp(x, outlier_indices):
    perc_10 = np.quantile(x, 0.25)
    perc_90 = np.quantile(x, 0.75) # there is clamping int eh top 25% and bottom 25% of the vlaues with outliers

    x = np.copy(x) # values are coppied to numpy type
    for idx in outlier_indices: # for loop goes through the argument inout data and clips the data with outliers found using the indices to the right amount
        x[idx] = np.clip(x[idx], perc_10, perc_90)

    return x


def clamp_prices(close_values_original, date_values_original, outlier_indices):
    fig11, ax11 = plt.subplots(1, figsize=(8, 4))
    
    x = date_values_original
    y4 = close_values_original

    y4_clamp = z_score_clamp(close_values_original, outlier_indices)  # clamp is done to the stock closing prices using the function

    ax11.plot(x, y4) # normal data is plotted first then the clamped data to show difference and allow for analysis


    ax11.plot(x, y4_clamp)

    ax11.set_title("MSFT - Clamped Stock Close Prices from 2019-04-01 to 2023-03-31")
    ax11.set_xlabel("Date")
    ax11.set_ylabel("Stock Price ($)")
    ax11.set_xticks(x[::163])
    
    ax11.legend(["Clamped", "Other"])
    plt.savefig('normal_plot_clamped.png')

    return fig11, ax11


def clamp_volume(date_values_original, volume_values_original, outlier_indices):
    fig12, ax12 = plt.subplots(1, figsize=(8, 4))
    
    x = date_values_original # same thing as the last clamp is done but this time for the volume
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

    return fig12, ax12



def data_frame(client, stock_name):
    db = client["Stock_Data"]
    collections = db[stock_name] # function to get the data from the collection with microft stock data
    values = list(collections.find()) # each part of the collection is searched and put to list
    df = pd.DataFrame(values) # values are put into a panda dataframe
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
    axs4[2].legend('Seasonal Patterns')
    axs4[3].plot(x, residual, label='Residuals', color="blue")
    axs4[3].legend(loc='best')
    axs4[3].set_ylabel('Residuals')
    axs4[3].set_xlabel('Date')
    fig13.tight_layout() # layout is made to ft tighly within the figure size given.
    
    plt.savefig('seasonality_decompose.png')
    return fig13, axs4




def seasonality(df):
    fig14, ax14 = plt.subplots(1, figsize=(8, 4))
    
    x = df['date'] # close price and date plot is done
    y = df['close']
    important_event_dates = ['2019-12-31', '2020-06-30', '2020-12-31', '2021-06-30', '2021-12-31', '2022-06-30']
    # some important event dates maybe causing seasonlity are added to list, thse are days where earning reports are released
    ax14.plot(x,y, color='purple', label='Stock Close Price')

    ax14.set_title("Close Stock Price Against Date With Special Events")
    ax14.set_xlabel("Date")
    ax14.set_ylabel("Close Stock Price ($)")
    ax14.set_xticks(x[::163])

    
    [ax14.axvline(_x, color='green', linestyle='--', linewidth=1, alpha=0.5) for _x in important_event_dates]
    # verticle dashed lines are made for each of the ones in the list above so change of trend or pattern can be seen
    ax14.legend()

    plt.savefig('Seasonality.png')

    return fig14, ax14




def scatter_plots(df):
    fig15, ax15 = plt.subplots(1, figsize=(8, 4))
    
    x = df['date']
    y1 = df['volume']
    y2 = df['close']


    ax15.scatter(x, y1, color='red', label="Stock Volume Traded") # scatter plot of volume and close prices are done to see any visual relations to one another

    ax15.set_title("Scatter Plot of Close Price and Volume Traded of Microsoft Stocks")
    ax15.set_xlabel("Date")
    ax15.set_ylabel("Volume")
    ax15.set_xticks(x[::163])

    ax16 = ax15.twinx() # opposite axis made for the volume

    ax16.scatter(x, y2, color='blue', label="Stock Close Price ($)")

    ax15.legend(loc="upper left")
    ax16.set_ylabel("Close Price ($)")

    ax16.legend(loc="upper right")

    plt.savefig('Scatter_Volume_Close.png')
    return fig15, (ax15, ax16)

def box_plot(df):
    fig17, ax17 = plt.subplots(1, figsize=(8, 4))
    

    y1 = df['open']
    y2 = df['high']   # values for each point ina day's stock price is take from data ram and assigned
    y3 = df['low'] 
    y4 = df['close']

    ys = [y1, y2, y3, y4]
    
    ax17.boxplot(ys, labels = ['Open Price', 'High Price', 'Low Price', 'Close Price'], patch_artist=True) # patch artist is used to give each box plot a different colour to differentiate

    ax17.set_title("Box Plot of Different Microsoft Stock Prices")

    ax17.set_ylabel("Stock Price ($)")

    ax17.grid(alpha=0.5) # light opacity grid is made due to minor differences between the different stock prices

    plt.savefig('Boxplot.png')
    return fig17, ax17


def hypothesis(df):
    x = df['close']
    y = df['volume'] 
    test = pearsonr(x, y)
    correlation_coefficient = test[0]
    p_value = test[1] # pearson r is used to hypothesis test whether the volume and close price are related, p value is used to decide hypothesis

    print(f"The correlation coefficient is {correlation_coefficient}")
    if 0.8 <= correlation_coefficient <= 1:
        print("Strong Positive Correlation") # shows the level of correlation between the two data values
    elif 0.3 <= correlation_coefficient <= 0.7:
        print("Positive Correlation")
    elif -0.2 <= correlation_coefficient <= 0.2:
        print("Neither Positive or Negative Correlation")
    elif -0.7 <= correlation_coefficient <= -0.3:
        print("Negative Correlation")
    elif -1 <= correlation_coefficient <= -0.8:
        print("Strong Negative Correlation")

    print(f"The P value is {p_value}") # sees whther the p values is low enough to show significant association
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

    return fig24, (ax24, ax25)

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
    return fig26, axs10
    

def modelling_without_auxilary(df, df1):
    training_data = df[0:int(len(df))] # the training data is all of the data
    test_data = df[int(len(df)*0.8):] # the last 20% of the data is the test data

    train_model = training_data['close'] # each has the closing price of dataframe picked
    test_model = test_data['close']
     
    n = 29 # this is the number of days of april where when 29, foreacsts till 30 april 2023

    history = [x for x in train_model] # for loop goes through each closing price in training data

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
    ax27.set_xticks(x[::5]) # spacing of 5 days to show good intervals
    ax27.legend()
    plt.savefig('Forecast_vs_Real.png')
    return fig27, ax27

#End of the different functions used within the main


"""
The main method contains everything that is done throughout the code and 
covers all the tasks to be done seamlessly without the need of stopping 
the running or the need of giving inputs. The only part where the inputs
might be useful is for task 2.2 where the crud function are utilised in a
API fashion. The docstring will got through each part of the functions made
and put into the main method. This will go through mainly what is done and
within each function, there is comments that help understand any parts that
accompany this. The explanation happen in order of where they appear in main.

The workflow of the main method is done by using many different functions

The following tasks are done in order and the task description they fall under 
will be titled above it:
'Acquiring Data'
        1. Microsoft stock data is acquired using API and filtered between 
        2019/04/01 and 2023/03/31.
        2. Microsoft stock information in the form of income statements, balance 
        sheets, cash flow statements and earnings reports are acruired using APIs 
        also and filtered between the right dates.
        3. Microsoft news articles from the New York Times API are collected 
        with many queries covering different instances of peaks, dips and outliers.
'Storing Data'
        4. Stock data, stock information and news are formatted in appropriate 
        way and stored online using MongoDB.
'API Implementation of CRUD Operations'
        5. CRUD operations done on MongoDB data and can be used in simple API.
'Preprocessing'
        6. Handling missing values and outliers by deleting the data that has that.
        7. Visualise the preprocessed data using various plots.
        8. Data is tranformed for better forecasting performance.
'Exploratory Data Analysis'
        9. Exploratory Data Analysis (EDA) done on the stock data by looking at 
        trends, seasonality, box plots, scatter plots and hypothesis testing.
        10. Different financial indicators are made from the data.
'Modeling / Forecasting'
        10. Perform modeling by fitting an ARIMA model.
        11. Do fifferencing, ACF and PACF to get ARIMA order values
        12. Visualize the model and get acciracy results. 

"""

def main():
    # Aqcuire Stock Data
    call_API()
    filter_data('2019-04-01','2023-03-31')

    # Aqcuire Stock Information
    income_balance_cash_statement_API()
    filter_data_income_statement('2019-04-01','2023-06-30') # Fiscal year is on 30 june each year so need to be higher than 31 march 2023 to get info
    filter_balance_sheet_statement('2019-04-01','2023-06-30')
    filter_cash_flow_statement('2019-04-01','2023-06-30')
    filter_eps_statement('2019-04-01','2023-06-30')
    nyt_api()

    # Store Stock Data and Stock Information in MongoDB Atlas 
    client = mongo_connect()
    stock_name = "Microsoft (MSFT)"
    add_mongo(client, stock_name)
    add_mongo_info(client)
    client.close()

    # Crud Functions
    client = mongo_connect()
    item = {"date": "2023-04-01", "open": "284.04", "high": "285.01", "low": "275.03", "close": "283.01", "volume": "20065433"}
    idee = create(client, item)
    query = {"volume" : "20065433"}
    read(client, query)
    #item_id = ObjectId('65a6928ec97968d603431f1d')
    item_id = ObjectId(idee[1])
    properties = {"open": "284.05", "low": "285.02", "volume": "20065434"}
    update(client, item_id, properties)
    delete(client, item_id)
    client.close()

    # Preprocessing
    client = mongo_connect()
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

    # EDA
    client = mongo_connect()
    df = data_frame(client, stock_name)
    fig13, axs4 = seasonality_check(df)
    fig14, ax14 = seasonality(df)
    fig15, axs5 = scatter_plots(df)
    fig17, ax17 = box_plot(df)
    hypothesis(df)
    fig18, axs6 = OBV(df)
    fig20, axs7 = acc_dist(df)
    fig22, axs8 = macd(df)
    fig24, axs9 = rsi(df)
    client.close()

    # Modelling
    client = mongo_connect()
    df = data_frame(client, stock_name)
    fig26, axs10 = pdq(df)
    df1 = filter_data_new_dates('2023-04-01','2023-04-30')
    fig27, ax27 = modelling_without_auxilary(df, df1)
    client.close()

    print("Done! ")



if __name__ == "__main__":
    main()
