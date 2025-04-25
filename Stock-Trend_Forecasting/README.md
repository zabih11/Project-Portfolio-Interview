# Stock Price Analysis and Forecasting

This repository provides a complete pipeline for retrieving, processing, storing, analysing, and forecasting stock price data for any company using the AlphaVantage API and MongoDB. The project covers data acquisition, cleaning, storage, CRUD operations, time series modelling (ARIMA), and visualisations.

---

## Contents

- `Stock_Price_API.py`  
- `Data_Storage.py`  
- `Data_Preprocess.py`  
- `crud_functions.py`  
- `Modelling.py`  
- `requirements.txt`

---

## Overview

This project enables you to:

- Retrieve daily stock price data from AlphaVantage for a specified company (2019-04-01 to 2023-03-31)
- Store and manage the data in MongoDB
- Preprocess the data (handle missing values, remove outliers, normalise)
- Perform CRUD operations on the MongoDB database
- Model and forecast stock prices using ARIMA
- Visualise and evaluate the model's performance

---

## Setup

1.  **Clone the repository**

    ```
    git clone <your-repo-url>
    cd <your-repo-directory>
    ```

2.  **Install dependencies**

    All required packages are listed in `requirements.txt`. Install them with:

    ```
    pip install -r requirements.txt
    ```

---

## File Descriptions

| File                | Purpose                                                                                           |
|---------------------|---------------------------------------------------------------------------------------------------|
| Stock_Price_API.py  | Fetches stock data from AlphaVantage for a specified company and filters it by date range.        |
| Data_Storage.py     | Uploads filtered stock data and financial news/statements to MongoDB.                            |
| Data_Preprocess.py  | Handles missing values, detects/removes outliers, normalises data, and visualises trends.        |
| crud_functions.py   | Provides CRUD (Create, Read, Update, Delete) operations for MongoDB stock data.                   |
| Modelling.py        | Loads data from MongoDB, checks stationarity, fits ARIMA model, forecasts, and visualises.      |
| requirements.txt    | Lists all Python dependencies required for the project.                                           |

---

## Usage

1.  **Retrieve and Save Stock Data**

    Modify `Stock_Price_API.py` to specify the desired company ticker symbol. Run the script to download and save daily stock prices as JSON.

    ```
    python Stock_Price_API.py
    ```

    This will create `Stock_Data.json` and a filtered `Stock_Data_Format.json`.

2.  **Store Data in MongoDB**

    Modify `Data_Storage.py` to specify the stock name. Run `Data_Storage.py` to upload the filtered data to your MongoDB database.

    ```
    python Data_Storage.py
    ```

    This script also supports uploading financial statements and news if the relevant JSON files are present.

3.  **Preprocess Data**

    Modify `Data_Preprocess.py` to specify the stock name. Run `Data_Preprocess.py` to:

    *   Remove days with missing values
    *   Detect and remove outliers
    *   Normalise the data
    *   Generate initial plots

    ```
    python Data_Preprocess.py
    ```

4.  **CRUD Operations**

    Modify `crud_functions.py` to specify the stock name. Use `crud_functions.py` to create, read, update, or delete individual records in the MongoDB stock data collection.

    ```
    python crud_functions.py
    ```

5.  **Modelling and Forecasting**

     Modify `Modelling.py` to specify the stock name. Run `Modelling.py` to:

    *   Load data from MongoDB
    *   Check for stationarity and plot ACF/PACF
    *   Fit an ARIMA model
    *   Forecast stock prices for April 2023
    *   Visualise and evaluate predictions

    ```
    python Modelling.py
    ```

---

## Configuration

*   **MongoDB Connection:**  
    The scripts use a MongoDB Atlas connection string. Update the `uri` variable in each script if you wish to use your own database.
*   **API Key:**  
    The AlphaVantage API key is set by default in `Stock_Price_API.py`. Replace it with your own if needed.
*   **Stock Ticker:**  
    Modify the `symbol` variable in `Stock_Price_API.py` to the desired stock ticker symbol.

---

## Outputs

*   JSON files with stock and financial data
*   Filtered and cleaned data in MongoDB
*   Plots of stock price trends, outliers, and forecast results (saved as PNG)
*   Model evaluation metrics (MSE, MAE, RMSE, R², MAPE) printed to console

---

## Contributing

Pull requests are welcome. For major changes, please open an issue first to discuss what you would like to change.

---

## License

This project is licensed under the MIT License.

---

## Acknowledgements

*   [AlphaVantage](https://www.alphavantage.co/) for stock data API
*   [MongoDB Atlas](https://www.mongodb.com/cloud/atlas) for cloud database hosting

---

## Contact

For questions or suggestions, please open an issue or contact the repository maintainer.
