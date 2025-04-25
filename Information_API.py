import requests
import json
import pandas as pd
from datetime import datetime
import time


def income_balance_cash_statement_API(apikey='LLMPRGO977MMGN6I'): # I got an API Key from AlphaVantage
    query_income = f'https://www.alphavantage.co/query?function=INCOME_STATEMENT&symbol=MSFT&apikey={apikey}'
    request_income = requests.get(query_income) 
    data_income = request_income.json() 
    with open("Income_Statement.json", "w") as file: 
        json.dump(data_income, file)
    query_balance = f'https://www.alphavantage.co/query?function=BALANCE_SHEET&symbol=MSFT&apikey={apikey}'
    request_balance = requests.get(query_balance) 
    data_balance = request_balance.json() 
    with open("Balance_Sheet.json", "w") as file: 
        json.dump(data_balance, file)
    query_cash_flow = f'https://www.alphavantage.co/query?function=CASH_FLOW&symbol=MSFT&apikey={apikey}'
    request_cash = requests.get(query_cash_flow) 
    data_cash = request_cash.json() 
    with open("Cash_Flow_Statement.json", "w") as file: 
        json.dump(data_cash, file)
    query_eps = f'https://www.alphavantage.co/query?function=EARNINGS&symbol=MSFT&apikey={apikey}'
    request_eps = requests.get(query_eps) 
    data_eps = request_eps.json() 
    with open("Earnings_Statement.json", "w") as file: 
        json.dump(data_eps, file)
    
def filter_data_income_statement(start_date, end_date):
    with open("Income_Statement.json", "r") as file:
        data_income = json.load(file)
    
    annual_report = data_income['annualReports']
    quarterly_report = data_income['quarterlyReports']

    start_date = datetime.strptime(start_date, '%Y-%m-%d').date()
    end_date = datetime.strptime(end_date, '%Y-%m-%d').date()

    dates_needed_income = {}

    for dates in annual_report:

        date_string = dates['fiscalDateEnding']
        date_object = datetime.strptime(date_string, "%Y-%m-%d").date()

        if start_date <= date_object <= end_date:
            dates_needed_income[date_string] = dates

    for dates in quarterly_report:

        date_string = dates['fiscalDateEnding']
        date_object = datetime.strptime(date_string, "%Y-%m-%d").date()

        if start_date <= date_object <= end_date:
            dates_needed_income[date_string] = dates

    reverse_dates_needed_cash = dict(reversed(list(dates_needed_income.items())))
    with open("Income_Statement_Format.json", "w") as file: 
        json.dump(reverse_dates_needed_cash, file, indent=1)

def filter_balance_sheet_statement(start_date, end_date):
    with open("Balance_Sheet.json", "r") as file:
        data_balance = json.load(file)
    
    annual_report = data_balance['annualReports']
    quarterly_report = data_balance['quarterlyReports']

    start_date = datetime.strptime(start_date, '%Y-%m-%d').date()
    end_date = datetime.strptime(end_date, '%Y-%m-%d').date()

    dates_needed_balance = {}

    for dates in annual_report:

        date_string = dates['fiscalDateEnding']
        date_object = datetime.strptime(date_string, "%Y-%m-%d").date()

        if start_date <= date_object <= end_date:
            dates_needed_balance[date_string] = dates

    for dates in quarterly_report:

        date_string = dates['fiscalDateEnding']
        date_object = datetime.strptime(date_string, "%Y-%m-%d").date()

        if start_date <= date_object <= end_date:
            dates_needed_balance[date_string] = dates

    reverse_dates_needed_cash = dict(reversed(list(dates_needed_balance.items())))
    with open("Balance_Sheet_Format.json", "w") as file: 
        json.dump(reverse_dates_needed_cash, file, indent=1)

def filter_cash_flow_statement(start_date, end_date):
    with open("Cash_Flow_Statement.json", "r") as file:
        data_cash = json.load(file)
    
    annual_report = data_cash['annualReports']
    quarterly_report = data_cash['quarterlyReports']

    start_date = datetime.strptime(start_date, '%Y-%m-%d').date()
    end_date = datetime.strptime(end_date, '%Y-%m-%d').date()

    dates_needed_cash = {}

    for dates in annual_report:

        date_string = dates['fiscalDateEnding']
        date_object = datetime.strptime(date_string, "%Y-%m-%d").date()

        if start_date <= date_object <= end_date:
            dates_needed_cash[date_string] = dates

    for dates in quarterly_report:

        date_string = dates['fiscalDateEnding']
        date_object = datetime.strptime(date_string, "%Y-%m-%d").date()

        if start_date <= date_object <= end_date:
            dates_needed_cash[date_string] = dates

    reverse_dates_needed_cash = dict(reversed(list(dates_needed_cash.items())))
    with open("Cash_Flow_Statement_Format.json", "w") as file: 
        json.dump(reverse_dates_needed_cash, file, indent=1)

def filter_eps_statement(start_date, end_date):
    with open("Earnings_Statement.json", "r") as file:
        data_eps = json.load(file)
    
    annual_earning = data_eps['annualEarnings']
    quarterly_earning = data_eps['quarterlyEarnings']

    start_date = datetime.strptime(start_date, '%Y-%m-%d').date()
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

    reverse_dates_needed_eps = dict(reversed(list(dates_needed_eps.items())))
    with open("Earnings_Statement_Format.json", "w") as file: 
        json.dump(reverse_dates_needed_eps, file, indent=1)    


def nyt_api():
    api_key = 'gw5RRpLJhzfCX1YlLGAfiYyBAhXUk7HS'
    base_url = 'https://api.nytimes.com/svc/search/v2/articlesearch.json'
    # Define the date range
    begin_date = '20200220'
    end_date = '20200415'

    begin_date1 = '20200725'
    end_date1 = '20200805'

    begin_date2 = '20210125'
    end_date2 = '20210129'

    begin_date3 = '20220120'
    end_date3 = '20220129'

    begin_date4 = '20230315'
    end_date4 = '20230319'

    begin_date5 = '20200125'
    end_date5 = '20200229'

    begin_date6 = '20211005'
    end_date6 = '20220110'

    begin_date7 = '20220825'
    end_date7 = '20220915'

    begin_date8 = '20221215'
    end_date8 = '20230115'

    # Construct the API request URL
    query_params = {
        'q': 'Microsoft',
        'begin_date': begin_date,
        'end_date': end_date,
        'api-key': api_key,
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

    
    response = requests.get(base_url, query_params)
    data = response.json()
    with open("NYT.json", "w") as file:
        json.dump(data, file, indent=1)

    time.sleep(12)

    response1 = requests.get(base_url, query_params1)
    data_out1 = response1.json()
    with open("NYT_out1.json", "w") as file:
        json.dump(data_out1, file, indent=1)

    time.sleep(12)

    response2 = requests.get(base_url, query_params2)
    data_out2 = response2.json()
    with open("NYT_out2.json", "w") as file:
        json.dump(data_out2, file, indent=1)

    time.sleep(12)

    response3 = requests.get(base_url, query_params3)
    data_out3 = response3.json()
    with open("NYT_out3.json", "w") as file:
        json.dump(data_out3, file, indent=1)

    time.sleep(12)

    response4 = requests.get(base_url, query_params4)
    data_out4 = response4.json()
    with open("NYT_out4.json", "w") as file:
        json.dump(data_out4, file, indent=1)

    time.sleep(12)

    response5 = requests.get(base_url, query_params5)
    data_out5 = response5.json()
    with open("NYT_before_covid.json", "w") as file:
        json.dump(data_out5, file, indent=1)

    time.sleep(12)

    response6 = requests.get(base_url, query_params6)
    data_out6 = response6.json()
    with open("NYT_biggest_peak.json", "w") as file:
        json.dump(data_out6, file, indent=1)

    time.sleep(12)

    response7 = requests.get(base_url, query_params7)
    data_out7 = response7.json()
    with open("NYT_peak_in_downward.json", "w") as file:
        json.dump(data_out7, file, indent=1)

    time.sleep(12)

    response8 = requests.get(base_url, query_params8)
    data_out8 = response8.json()
    with open("NYT_new_upwards.json", "w") as file:
        json.dump(data_out8, file, indent=1)


if __name__ == "__main__":
    income_balance_cash_statement_API()
    filter_data_income_statement('2019-03-31','2023-06-30') # Fiscal year is on 30 june each year so need to be higher than 31 march 2023 to get info
    filter_balance_sheet_statement('2019-03-31','2023-06-30')
    filter_cash_flow_statement('2019-03-31','2023-06-30')
    filter_eps_statement('2019-03-31','2023-06-30')
    #nyt_api()
