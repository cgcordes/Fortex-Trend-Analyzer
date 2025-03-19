# Forex Trend Analyzer

A simple Streamlit application to analyze forex trends for major currency pairs using technical indicators, candlestick charts, and basic trend analysis.

## Overview

This application fetches forex data using the Twelve Data API and displays key information including:

- **Price Chart:** Candlestick chart with moving averages (SMA 20 and SMA 50).
- **Trend Analysis:** Simple trend direction and strength analysis based on recent price changes and a simplified RSI calculation.
- **Trading Insight:** Basic trading recommendations based on trend and RSI values.

## Features

- **Data Fetching:** Retrieves forex data for selected currency pairs with retry logic.
- **Technical Indicators:** Calculates simple moving averages (SMA 20 and SMA 50) and a simplified RSI.
- **Trend Analysis:** Determines if the market is bullish, bearish, or sideways, along with trend strength.
- **Interactive Visualizations:** Uses Plotly for dynamic candlestick charts.
- **User-Friendly Interface:** Streamlit’s sidebar allows for easy selection of currency pairs and time intervals.

## Prerequisites

Before running the app, ensure you have the following installed:

- [Python 3.7+](https://www.python.org/downloads/)
- [pip](https://pip.pypa.io/en/stable/installation/)

## Installation

1. **Clone the Repository:**

   ```bash
   git clone <repository_url>
   cd <repository_folder>

2. **Create & Activate a Virtual Environment (Recommended):**

- On macOS/Linux:

   ```bash
    python3 -m venv venv
    source venv/bin/activate

- On Windows:

    ```bash 
    python -m venv venv
    .\venv\Scripts\activate

3. **Install All Required Dependecies**

    ```bash
    pip install -r requirements.txt

## Running the App

1. Open your terminal in VS Code (or your preferred terminal).
2. Navigate to the repository directory.
3. Run Streamlit script:

    ```bash
    streamlit run ADFM-FortexUi.py 
4. Your default web browser should automatically open a new tab with the running application.

## Configuration
- **API Key:**
The app uses the Twelve Data API. Replace the placeholder API key in the script with your actual API key if needed.
    ```python
    TWELVE_DATA_API_KEY = "YOUR_API_KEY_HERE"

- **Currency Pairs & Intervals:** 
The sidebar in the app lets yuou choose from predefined currency paris and select the data interval (daily or hourly).

## Troubleshooting 
- If the app fails to fetch data, ensure that your internet connection is active and the Twelve Data API key is valid.
- Check that all dependencies are correctly installed.
- For additional help, refer to the [Streamlit documentation](https://docs.streamlit.io/) or the [Twelve Data API documentation](https://twelvedata.com/).

## License
This project is open-source and available under the [MIT License](https://opensource.org/license/mit).

## Acknowledgements
- [Streamlit](https://docs.streamlit.io/)
- [TwelveData](https://twelvedata.com/)
- Various Python libraries for data visualization & analysis.