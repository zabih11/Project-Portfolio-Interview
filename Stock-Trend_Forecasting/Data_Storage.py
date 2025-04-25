import pymongo
import pandas as pd
import json


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


def empty_or_float(number):
    if number == "":
        return None
    else:
        return float(number)

def empty_or_int(number):
    if number == "":
        return None
    else:
        return int(number)

def add_mongo(client, stock_name):
    with open("Stock_Data_Format.json", "r") as file:
        reverse_dates_needed = json.load(file)
    
    db = client["Stock_Data"]
    collections = db[stock_name]
    data_formatted = []
    for date, data_point in reverse_dates_needed.items():
        existing_document = collections.find_one({"date": date})
        if existing_document == None:
            formatted_data_mongo = {
                "date": date, 
                "open": empty_or_float(data_point["1. open"]),
                "high": empty_or_float(data_point["2. high"]),
                "low": empty_or_float(data_point["3. low"]),
                "close": empty_or_float(data_point["4. close"]),
                "volume": empty_or_int(data_point["5. volume"])
            }
            data_formatted.append(formatted_data_mongo)

    if len(data_formatted) > 0:
        collections.insert_many(data_formatted)
        print("Successfully Uploaded Stock Data to MongoDB!")
    else:
        print("All this data already exists!")


def add_mongo_info(client):
    db = client["Stock_Information"]
    
    with open("Balance_Sheet_Format.json", "r") as file: 
        data_balance = json.load(file)

    collections1 = db["Microsoft Balance Sheet"]
    balance_data_formatted = []
    balance_data_formatted.append(data_balance)
    collections1.insert_many(balance_data_formatted)

    with open("Income_Statement_Format.json", "r") as file:
        data_income = json.load(file)
    
    collections2 = db["Microsoft Income Statement"]
    income_statement_formatted = []
    income_statement_formatted.append(data_income)
    collections2.insert_many(income_statement_formatted)

    with open("Cash_Flow_Statement_Format.json", "r") as file:
        data_cash = json.load(file)
    
    collections3 = db["Microsoft Cash Flow Statement"]
    cash_flow_statement_formatted = []
    cash_flow_statement_formatted.append(data_cash)
    collections3.insert_many(cash_flow_statement_formatted)

    with open("Earnings_Statement_Format.json", "r") as file:
        data_eps = json.load(file)
    
    collections4 = db["Microsoft Earnings Statement"]
    eps_statement_formatted = []
    eps_statement_formatted.append(data_eps)
    collections4.insert_many(eps_statement_formatted)

    db1 = client["Microsoft_News"]

    with open("NYT.json", "r") as file:
        data_nyt = json.load(file)

    collections5 = db1["New York Times - First"]
    nyt_formatted = []
    docs_nyt = data_nyt['response']['docs']
    for data_point in docs_nyt:
        formatted_data_nyt = {
            "Abstract": data_point["abstract"],
            "Web URL": data_point["web_url"],
            "Snippet": data_point["snippet"],
            "Lead Paragraph": data_point["lead_paragraph"],
            "Source": data_point["source"]
        }
        nyt_formatted.append(formatted_data_nyt)

    collections5.insert_many(nyt_formatted)

    with open("NYT_out1.json", "r") as file:
        data_nyt_out1 = json.load(file)

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
        data_nyt_out2 = json.load(file)

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
        data_nyt_out3 = json.load(file)

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
        data_nyt_out4 = json.load(file)

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
        data_nyt_before_covid = json.load(file)

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
        data_nyt_biggest_peak = json.load(file)

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
        data_nyt_peak_in_downward = json.load(file)

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


    print("Successfully Uploaded Balance Sheet / Income Statement / Cash-Flow / Earnings / News to MongoDB!")
    






    


if __name__ == "__main__":
    client = mongo_connect()
    stock_name = "Microsoft (MSFT)"
    add_mongo(client, stock_name)
    #add_mongo_info(client)
    client.close()
