import ta
import pandas as pd
import numpy as np
from typing import Dict, Any


def calculate_vietnam_indicators(df: pd.DataFrame) -> Dict[str, Any]:
    """
    Calculate comprehensive technical indicators for Vietnam stock market
    """
    if df.empty or len(df) < 50:
        return get_mock_indicators()
    
    close = df["Close"]
    high = df["High"]
    low = df["Low"]
    volume = df["Volume"]
    
    try:
        # Basic indicators
        rsi = ta.momentum.RSIIndicator(close, window=14).rsi().iloc[-1]
        
        # Moving averages
        ma20 = close.rolling(window=20).mean().iloc[-1]
        ma50 = close.rolling(window=50).mean().iloc[-1]
        ma200 = close.rolling(window=200).mean().iloc[-1]
        
        # MACD
        macd_indicator = ta.trend.MACD(close, window_slow=26, window_fast=12, window_sign=9)
        macd = macd_indicator.macd().iloc[-1]
        signal_line = macd_indicator.macd_signal().iloc[-1]
        macd_histogram = macd_indicator.macd_diff().iloc[-1]
        
        # Bollinger Bands
        bb_indicator = ta.volatility.BollingerBands(close, window=20, window_dev=2)
        bb_upper = bb_indicator.bollinger_hband().iloc[-1]
        bb_middle = bb_indicator.bollinger_mavg().iloc[-1]
        bb_lower = bb_indicator.bollinger_lband().iloc[-1]
        bb_width = (bb_upper - bb_lower) / bb_middle
        
        # Volume indicators
        volume_sma = volume.rolling(window=20).mean().iloc[-1]
        volume_ratio = volume.iloc[-1] / volume_sma if volume_sma > 0 else 1
        
        # Stochastic
        stoch = ta.momentum.StochasticOscillator(high, low, close, window=14, smooth_window=3)
        stoch_k = stoch.stoch().iloc[-1]
        stoch_d = stoch.stoch_signal().iloc[-1]
        
        # ADX (Trend strength)
        adx = ta.trend.ADXIndicator(high, low, close, window=14).adx().iloc[-1]
        
        # Williams %R
        williams_r = ta.momentum.WilliamsRIndicator(high, low, close, lbp=14).williams_r().iloc[-1]
        
        # Commodity Channel Index
        cci = ta.trend.CCIIndicator(high, low, close, window=20).cci().iloc[-1]
        
        # Money Flow Index
        mfi = ta.volume.MFIIndicator(high, low, close, volume, window=14).money_flow_index().iloc[-1]
        
        # Calculate volatility (20-day standard deviation of returns)
        returns = close.pct_change().dropna()
        volatility = returns.rolling(window=20).std().iloc[-1] * np.sqrt(252)  # Annualized
        
        # Price position relative to Bollinger Bands
        bb_position = (close.iloc[-1] - bb_lower) / (bb_upper - bb_lower) if bb_upper != bb_lower else 0.5
        
        return {
            # Basic indicators
            "rsi": round(float(rsi), 2) if not pd.isna(rsi) else 50,
            "macd": round(float(macd), 4) if not pd.isna(macd) else 0,
            "signal_line": round(float(signal_line), 4) if not pd.isna(signal_line) else 0,
            "macd_histogram": round(float(macd_histogram), 4) if not pd.isna(macd_histogram) else 0,
            
            # Moving averages
            "ma20": round(float(ma20), 2) if not pd.isna(ma20) else close.iloc[-1],
            "ma50": round(float(ma50), 2) if not pd.isna(ma50) else close.iloc[-1],
            "ma200": round(float(ma200), 2) if not pd.isna(ma200) else close.iloc[-1],
            
            # Bollinger Bands
            "bollinger_upper": round(float(bb_upper), 2) if not pd.isna(bb_upper) else close.iloc[-1] * 1.1,
            "bollinger_middle": round(float(bb_middle), 2) if not pd.isna(bb_middle) else close.iloc[-1],
            "bollinger_lower": round(float(bb_lower), 2) if not pd.isna(bb_lower) else close.iloc[-1] * 0.9,
            "bb_width": round(float(bb_width), 4) if not pd.isna(bb_width) else 0.1,
            "bb_position": round(float(bb_position), 2) if not pd.isna(bb_position) else 0.5,
            
            # Volume
            "volume_sma": round(float(volume_sma), 0) if not pd.isna(volume_sma) else volume.iloc[-1],
            "volume_ratio": round(float(volume_ratio), 2) if not pd.isna(volume_ratio) else 1,
            
            # Other indicators
            "stoch_k": round(float(stoch_k), 2) if not pd.isna(stoch_k) else 50,
            "stoch_d": round(float(stoch_d), 2) if not pd.isna(stoch_d) else 50,
            "adx": round(float(adx), 2) if not pd.isna(adx) else 25,
            "williams_r": round(float(williams_r), 2) if not pd.isna(williams_r) else -50,
            "cci": round(float(cci), 2) if not pd.isna(cci) else 0,
            "mfi": round(float(mfi), 2) if not pd.isna(mfi) else 50,
            
            # Risk metrics
            "volatility": round(float(volatility), 4) if not pd.isna(volatility) else 0.2,
            "current_price": round(float(close.iloc[-1]), 2),
            
            # Vietnam market specific signals
            "support_level": round(float(close.rolling(window=20).min().iloc[-1]), 2),
            "resistance_level": round(float(close.rolling(window=20).max().iloc[-1]), 2),
        }
        
    except Exception as e:
        print(f"Error calculating indicators: {e}")
        return get_mock_indicators()


def get_mock_indicators() -> Dict[str, Any]:
    """Mock indicators for development"""
    import random
    
    return {
        "rsi": round(random.uniform(20, 80), 2),
        "macd": round(random.uniform(-2, 2), 4),
        "signal_line": round(random.uniform(-2, 2), 4),
        "macd_histogram": round(random.uniform(-1, 1), 4),
        "ma20": round(random.uniform(20000, 100000), 2),
        "ma50": round(random.uniform(20000, 100000), 2),
        "ma200": round(random.uniform(20000, 100000), 2),
        "bollinger_upper": round(random.uniform(20000, 100000), 2),
        "bollinger_middle": round(random.uniform(20000, 100000), 2),
        "bollinger_lower": round(random.uniform(20000, 100000), 2),
        "bb_width": round(random.uniform(0.05, 0.3), 4),
        "bb_position": round(random.uniform(0, 1), 2),
        "volume_sma": round(random.uniform(100000, 2000000), 0),
        "volume_ratio": round(random.uniform(0.5, 2.0), 2),
        "stoch_k": round(random.uniform(20, 80), 2),
        "stoch_d": round(random.uniform(20, 80), 2),
        "adx": round(random.uniform(15, 50), 2),
        "williams_r": round(random.uniform(-80, -20), 2),
        "cci": round(random.uniform(-200, 200), 2),
        "mfi": round(random.uniform(20, 80), 2),
        "volatility": round(random.uniform(0.1, 0.5), 4),
        "current_price": round(random.uniform(20000, 100000), 2),
        "support_level": round(random.uniform(20000, 100000), 2),
        "resistance_level": round(random.uniform(20000, 100000), 2),
    }


def calculate_indicators(df: pd.DataFrame) -> Dict[str, Any]:
    """Legacy function for backward compatibility"""
    return calculate_vietnam_indicators(df)