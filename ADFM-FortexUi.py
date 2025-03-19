import streamlit as st
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import yfinance as yf
from datetime import datetime, timedelta
import plotly.graph_objects as go
from sklearn.linear_model import LinearRegression
from statsmodels.tsa.arima.model import ARIMA
import time
import random
from twelvedata import TDClient

# API Configuration
TWELVE_DATA_API_KEY = "86528afdfb424533b083d56107091e52"
td = TDClient(apikey=TWELVE_DATA_API_KEY)

st.set_page_config(
    page_title="Forex Trend Analyzer",
    page_icon="📈",
    layout="wide"
)


@st.cache_data(ttl=3600)  
def get_forex_data(currency_pair, interval='1d', max_retries=3):
    """Fetch forex data using Twelve Data with retry logic"""
    retries = 0
    backoff_time = 2  
    
    while retries < max_retries:
        try:
            response = td.time_series(
                symbol=currency_pair,
                interval=interval,
                outputsize=365, 
                exchange="forex"
            )
            data = response.as_pandas()
            if not data.empty:
                return data
            
            retries += 1
            if retries < max_retries:
                st.warning(f"Attempt {retries}/{max_retries} failed. Retrying...")
                time.sleep(backoff_time)
                backoff_time = backoff_time * 2 + random.uniform(0, 1)
            else:
                st.error(f"Failed to fetch data after {max_retries} attempts.")
                return pd.DataFrame()
        
        except Exception as e:
            st.warning(f"Error on attempt {retries+1}/{max_retries}: {str(e)}")
            retries += 1
            if retries < max_retries:
                st.warning(f"Retrying...")
                time.sleep(backoff_time)
                backoff_time = backoff_time * 2 + random.uniform(0, 1)
            else:
                st.error(f"Failed to fetch data after {max_retries} attempts.")
                return pd.DataFrame()

def calculate_basic_indicators(df):
    """Calculate just the essential technical indicators"""
    if df.empty:
        return df
        
    # Simple Moving Averages
    df['SMA_20'] = df['close'].rolling(window=20).mean()
    df['SMA_50'] = df['close'].rolling(window=50).mean()
    
    # RSI (simplified)
    delta = df['close'].diff()
    gain = delta.where(delta > 0, 0).rolling(window=14).mean()
    loss = -delta.where(delta < 0, 0).rolling(window=14).mean()
    rs = gain / loss
    df['RSI'] = 100 - (100 / (1 + rs))
    
    return df

def analyze_trend(df):
    """Simple trend analysis"""
    if df.empty or len(df) < 21:
        return {"trend": "Unknown", "strength": "Unknown"}
    
    # Determine trend direction (last 20 days)
    current_price = df['close'].iloc[-1]
    price_20_days_ago = df['close'].iloc[-21] if len(df) > 21 else df['close'].iloc[0]
    trend_pct = ((current_price - price_20_days_ago) / price_20_days_ago) * 100
    
    # Determine trend
    if trend_pct > 1:
        trend = "Bullish"
    elif trend_pct < -1:
        trend = "Bearish"
    else:
        trend = "Sideways"
    
    # Simple strength measure
    if abs(trend_pct) > 5:
        strength = "Strong"
    elif abs(trend_pct) > 2:
        strength = "Moderate"
    else:
        strength = "Weak"
    
    return {
        "trend": trend,
        "strength": strength,
        "change_pct": round(trend_pct, 2),
        "rsi": round(df['RSI'].iloc[-1], 2) if 'RSI' in df and not pd.isna(df['RSI'].iloc[-1]) else 0
    }

def main():
    st.title("Simple Forex Trend Analyzer")
    
    # Sidebar for user inputs
    with st.sidebar:
        st.header("Settings")
        
        # Predefined major currency pairs
        currency_pairs = ["EUR/USD", "GBP/USD", "USD/JPY", "AUD/USD", "USD/CAD", "USD/CHF"]
        currency_pair = st.selectbox("Select Currency Pair:", currency_pairs)
        
        # Interval selection
        intervals = {"Daily": "1day", "Hourly": "1h"}
        selected_interval = st.selectbox("Select Interval:", list(intervals.keys()))
        
        # Analyze button
        analyze_button = st.button("Analyze Trends")
    
    # Main area
    if analyze_button:
        with st.spinner(f"Analyzing {currency_pair}..."):
            # Get data
            df = get_forex_data(
                currency_pair, 
                interval=intervals[selected_interval]
            )
            
            if df.empty:
                st.error(f"Unable to retrieve data for {currency_pair}.")
                st.info("Please try again later or select a different currency pair.")
            else:
                # Calculate indicators
                df = calculate_basic_indicators(df)
                
                # Create tabs for different views
                tab1, tab2 = st.tabs(["Price Chart", "Analysis"])
                
                with tab1:
                    st.subheader(f"{currency_pair} Price Chart")
                    
                    # Create price chart with Plotly
                    fig = go.Figure()
                    
                    # Candlestick chart
                    fig.add_trace(
                        go.Candlestick(
                            x=df.index,
                            open=df['open'],
                            high=df['high'],
                            low=df['low'],
                            close=df['close'],
                            name="Price"
                        )
                    )
                    
                    # Add moving averages
                    fig.add_trace(go.Scatter(x=df.index, y=df['SMA_20'], name="SMA 20", line=dict(color='blue')))
                    fig.add_trace(go.Scatter(x=df.index, y=df['SMA_50'], name="SMA 50", line=dict(color='orange')))
                    
                    # Layout
                    fig.update_layout(
                        title=f"{currency_pair} Price Chart",
                        xaxis_title="Date",
                        yaxis_title="Price",
                        height=500,
                        xaxis_rangeslider_visible=False
                    )
                    
                    st.plotly_chart(fig, use_container_width=True)
                    
                    # Display basic price stats
                    col1, col2, col3 = st.columns(3)
                    col1.metric("Current Price", round(df['close'].iloc[-1], 5))
                    col2.metric("Period High", round(df['high'].max(), 5))
                    col3.metric("Period Low", round(df['low'].min(), 5))
                
                with tab2:
                    st.subheader("Trend Analysis")
                    
                    # Simple trend analysis
                    analysis = analyze_trend(df)
                    
                    # Display results
                    col1, col2 = st.columns(2)
                    
                    with col1:
                        st.metric("Trend", analysis["trend"], f"{analysis['change_pct']}%")
                        st.metric("Trend Strength", analysis["strength"])
                    
                    with col2:
                        # RSI Chart
                        rsi_value = analysis["rsi"]
                        st.metric("RSI", rsi_value)
                        
                        # RSI interpretation
                        if rsi_value > 70:
                            st.warning("Overbought condition (RSI > 70)")
                        elif rsi_value < 30:
                            st.warning("Oversold condition (RSI < 30)")
                        else:
                            st.info("RSI in neutral zone")
                    
                    # Simple trading insight
                    st.subheader("Trading Insight")
                    if analysis["trend"] == "Bullish" and analysis["strength"] == "Strong":
                        st.success("Strong bullish trend detected. Consider buying opportunities.")
                    elif analysis["trend"] == "Bearish" and analysis["strength"] == "Strong":
                        st.error("Strong bearish trend detected. Consider selling opportunities.")
                    elif analysis["rsi"] > 70:
                        st.warning("Market may be overbought. Consider taking profits or short entries.")
                    elif analysis["rsi"] < 30:
                        st.warning("Market may be oversold. Consider buying opportunities.")
                    else:
                        st.info("No strong signals detected. Market may be in consolidation phase.")

if __name__ == "__main__":
    main()