// API service for Vietnam Stock Multi-Agent System
const API_BASE_URL = 'http://localhost:8000';

export interface Stock {
  ticker: string;
  name: string;
  industry: string;
  current_price: number;
  pe_ratio: number;
  market_cap: number;
  volume: number;
}

export interface QuickAnalysis {
  success: boolean;
  ticker: string;
  company_name: string;
  current_price: number;
  recommendation: 'BUY' | 'SELL' | 'HOLD';
  confidence: number;
  key_signals: {
    rsi: number;
    macd: number;
    ma20: number;
    ma50: number;
    sentiment: string;
    sentiment_score: number;
    volume_ratio: number;
    pe_ratio: number;
  };
  error?: string;
}

export interface FullAnalysis {
  success: boolean;
  ticker: string;
  horizon: string;
  timestamp: string;
  analysis: {
    plan: any;
    market_analysis: any;
    technical_analysis: any;
    news_analysis: any;
    risk_analysis: any;
    final_decision: {
      recommendation: string;
      confidence: number;
      reasoning: string[];
      summary: string;
    };
  };
  error?: string;
}

export interface MarketSentiment {
  success: boolean;
  sentiment: {
    market_sentiment: string;
    market_score: number;
    vn30_change: number;
    hnx_change: number;
    upcom_change: number;
    market_volume: number;
    market_topics: string[];
  };
  timestamp: string;
}

class ApiService {
  private async request<T>(endpoint: string, options?: RequestInit): Promise<T> {
    const url = `${API_BASE_URL}${endpoint}`;
    const response = await fetch(url, {
      headers: {
        'Content-Type': 'application/json',
        ...options?.headers,
      },
      ...options,
    });

    if (!response.ok) {
      throw new Error(`API Error: ${response.status} ${response.statusText}`);
    }

    return response.json();
  }

  // Health check
  async healthCheck(): Promise<{ status: string; version: string }> {
    return this.request('/health');
  }

  // Get list of Vietnam stocks
  async getStocks(): Promise<{ success: boolean; stocks: Stock[]; count: number }> {
    return this.request('/api/v1/stocks');
  }

  // Quick analysis
  async quickAnalyze(ticker: string): Promise<QuickAnalysis> {
    return this.request('/api/v1/quick-analyze', {
      method: 'POST',
      body: JSON.stringify({ ticker: ticker.toUpperCase() }),
    });
  }

  // Full analysis
  async fullAnalyze(ticker: string, horizon = 'swing', riskTolerance = 'medium'): Promise<FullAnalysis> {
    return this.request('/api/v1/analyze', {
      method: 'POST',
      body: JSON.stringify({
        ticker: ticker.toUpperCase(),
        horizon,
        risk_tolerance: riskTolerance,
      }),
    });
  }

  // Get stock data
  async getStockData(ticker: string): Promise<any> {
    return this.request(`/api/v1/stock/${ticker.toUpperCase()}/data`);
  }

  // Get market sentiment
  async getMarketSentiment(): Promise<MarketSentiment> {
    return this.request('/api/v1/market-sentiment', {
      method: 'POST',
      body: JSON.stringify({ timeframe: 'current' }),
    });
  }
}

export const apiService = new ApiService();
