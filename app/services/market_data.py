import yfinance as yf
import pandas as pd
import numpy as np
from datetime import datetime, timedelta
import requests


def fetch_vietnam_stock_data(ticker: str):
    """
    Fetch comprehensive Vietnam stock data
    ticker: Vietnam stock symbol (e.g., "VNM", "FPT", "VCB", "HPG", "MWG")
    """
    try:
        # Try to get Vietnam stock data
        # Add .VN suffix for Vietnam stocks if not present
        if not ticker.endswith('.VN'):
            ticker_yahoo = ticker + '.VN'
        else:
            ticker_yahoo = ticker
            
        stock = yf.Ticker(ticker_yahoo)
        hist = stock.history(period="1y")
        info = stock.info
        
        # Get current data
        current_price = info.get("currentPrice") or info.get("regularMarketPrice")
        if not current_price and len(hist) > 0:
            current_price = hist['Close'].iloc[-1]
            
        # Calculate additional metrics
        avg_volume = hist['Volume'].mean() if len(hist) > 0 else 0
        
        # Vietnam market data mapping
        vietnam_stocks = {
            'VNM': {'name': 'Vinamilk', 'industry': 'Thực phẩm & Đồ uống', 'exchange': 'HOSE'},
            'FPT': {'name': 'FPT Corporation', 'industry': 'Công nghệ thông tin', 'exchange': 'HOSE'},
            'VCB': {'name': 'Vietcombank', 'industry': 'Ngân hàng', 'exchange': 'HOSE'},
            'TCB': {'name': 'Techcombank', 'industry': 'Ngân hàng', 'exchange': 'HOSE'},
            'CTG': {'name': 'Vietinbank', 'industry': 'Ngân hàng', 'exchange': 'HOSE'},
            'BID': {'name': 'BIDV', 'industry': 'Ngân hàng', 'exchange': 'HOSE'},
            'HPG': {'name': 'Hòa Phát Group', 'industry': 'Thép', 'exchange': 'HOSE'},
            'HSG': {'name': 'Hoa Sen Group', 'industry': 'Thép', 'exchange': 'HOSE'},
            'MWG': {'name': 'Thế Giới Di Động', 'industry': 'Bán lẻ', 'exchange': 'HOSE'},
            'DGW': {'name': 'Điện Máy Xanh', 'industry': 'Bán lẻ', 'exchange': 'HOSE'},
            'PNJ': {'name': 'Phú Nhuận Jewelry', 'industry': 'Trang sức', 'exchange': 'HOSE'},
            'VRE': {'name': 'Vincom Retail', 'industry': 'Bán lẻ/ bất động sản', 'exchange': 'HOSE'},
            'NVL': {'name': 'Novaland', 'industry': 'Bất động sản', 'exchange': 'HOSE'},
            'VIC': {'name': 'Vingroup', 'industry': 'Tập đoàn đa ngành', 'exchange': 'HOSE'},
            'VHM': {'name': 'Vinhomes', 'industry': 'Bất động sản', 'exchange': 'HOSE'},
            'ACB': {'name': 'Asia Commercial Bank', 'industry': 'Ngân hàng', 'exchange': 'HOSE'},
            'MBB': {'name': 'Military Commercial Bank', 'industry': 'Ngân hàng', 'exchange': 'HOSE'},
            'STB': {'name': 'Sacombank', 'industry': 'Ngân hàng', 'exchange': 'HOSE'},
            'GAS': {'name': 'PetroVietnam Gas', 'industry': 'Năng lượng', 'exchange': 'HOSE'},
            'PLX': {'name': 'PetroVietnam Oil', 'industry': 'Năng lượng', 'exchange': 'HOSE'},
            'POW': {'name': 'Electricity of Vietnam', 'industry': 'Điện lực', 'exchange': 'HOSE'},
            'DHG': {'name': 'Dược Hậu Giang', 'industry': 'Dược phẩm', 'exchange': 'HOSE'},
            'IMP': {'name': 'Imexpharm', 'industry': 'Dược phẩm', 'exchange': 'HOSE'},
            'MSN': {'name': 'Masan Group', 'industry': 'Hàng tiêu dùng', 'exchange': 'HOSE'},
            'VHC': {'name': 'Vinh Hoan Corp', 'industry': 'Thủy sản', 'exchange': 'HOSE'},
            'HDC': {'name': 'Housing Development Bank', 'industry': 'Ngân hàng', 'exchange': 'HOSE'}
        }
        
        # Get stock info from mapping
        stock_info = vietnam_stocks.get(ticker.upper(), {
            'name': ticker,
            'industry': 'Chưa xác định',
            'exchange': 'HOSE'
        })
        
        return {
            "ticker": ticker,
            "company_name": stock_info['name'],
            "price": current_price or 0,
            "pe_ratio": info.get("trailingPE") or 15,
            "pb_ratio": info.get("priceToBook") or 2,
            "market_cap": info.get("marketCap") or 0,
            "beta": info.get("beta") or 1,
            "volume": info.get("volume") or 0,
            "avg_volume": avg_volume,
            "dividend_yield": info.get("dividendYield", 0) * 100 if info.get("dividendYield") else 0,
            "exchange": stock_info['exchange'],
            "industry": stock_info['industry'],
            "history": hist,
            "currency": "VND",
            "last_updated": datetime.now().isoformat()
        }
        
    except Exception as e:
        # Fallback to mock data for development
        print(f"Error fetching data for {ticker}: {e}")
        return get_mock_vietnam_data(ticker)


def get_mock_vietnam_data(ticker: str):
    """Mock data for development when API is unavailable"""
    import random
    
    mock_data = {
        'VNM': {'price': 65000, 'pe': 18, 'pb': 2.5, 'market_cap': 150000, 'volume': 500000},
        'FPT': {'price': 95000, 'pe': 25, 'pb': 4.2, 'market_cap': 120000, 'volume': 800000},
        'VCB': {'price': 45000, 'pe': 12, 'pb': 1.8, 'market_cap': 200000, 'volume': 1200000},
        'HPG': {'price': 28000, 'pe': 8, 'pb': 1.2, 'market_cap': 90000, 'volume': 2000000},
        'MWG': {'price': 75000, 'pe': 20, 'pb': 3.5, 'market_cap': 110000, 'volume': 600000}
    }
    
    data = mock_data.get(ticker.upper(), {
        'price': random.randint(20000, 100000),
        'pe': random.uniform(8, 30),
        'pb': random.uniform(1, 5),
        'market_cap': random.randint(50000, 300000),
        'volume': random.randint(100000, 2000000)
    })
    
    # Generate mock history
    dates = pd.date_range(end=datetime.now(), periods=252, freq='D')
    base_price = data['price']
    prices = [base_price * (1 + np.random.normal(0, 0.02)) for _ in range(252)]
    
    hist = pd.DataFrame({
        'Open': prices,
        'High': [p * 1.02 for p in prices],
        'Low': [p * 0.98 for p in prices],
        'Close': prices,
        'Volume': [random.randint(100000, 2000000) for _ in range(252)]
    }, index=dates)
    
    return {
        "ticker": ticker,
        "company_name": f"Công ty Cổ phần {ticker}",
        "price": data['price'],
        "pe_ratio": round(data['pe'], 2),
        "pb_ratio": round(data['pb'], 2),
        "market_cap": data['market_cap'],
        "beta": round(random.uniform(0.8, 1.5), 2),
        "volume": data['volume'],
        "avg_volume": data['volume'],
        "dividend_yield": round(random.uniform(0, 5), 2),
        "exchange": "HOSE",
        "industry": "Chưa xác định",
        "history": hist,
        "currency": "VND",
        "last_updated": datetime.now().isoformat()
    }


def get_vietnam_stock_list():
    """Get list of popular Vietnam stocks"""
    return [
        {'ticker': 'VNM', 'name': 'Vinamilk', 'industry': 'Thực phẩm & Đồ uống'},
        {'ticker': 'FPT', 'name': 'FPT Corporation', 'industry': 'Công nghệ thông tin'},
        {'ticker': 'VCB', 'name': 'Vietcombank', 'industry': 'Ngân hàng'},
        {'ticker': 'HPG', 'name': 'Hòa Phát Group', 'industry': 'Thép'},
        {'ticker': 'MWG', 'name': 'Thế Giới Di Động', 'industry': 'Bán lẻ'},
        {'ticker': 'PNJ', 'name': 'Phú Nhuận Jewelry', 'industry': 'Trang sức'},
        {'ticker': 'VRE', 'name': 'Vincom Retail', 'industry': 'Bán lẻ'},
        {'ticker': 'VIC', 'name': 'Vingroup', 'industry': 'Tập đoàn đa ngành'},
        {'ticker': 'GAS', 'name': 'PetroVietnam Gas', 'industry': 'Năng lượng'},
        {'ticker': 'MSN', 'name': 'Masan Group', 'industry': 'Hàng tiêu dùng'}
    ]