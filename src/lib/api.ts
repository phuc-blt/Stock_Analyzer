const API_BASE_URL = process.env.NEXT_PUBLIC_API_URL || 'http://localhost:8000';

export interface Stock {
  ticker: string;
  name: string;
  sector: string;
  current_price: number;
  pe_ratio: number;
  market_cap: number;
  volume: number;
}

export interface QuickAnalysisRequest {
  ticker: string;
}

export interface QuickAnalysisResponse {
  success: boolean;
  ticker: string;
  company_name: string;
  current_price: number;
  recommendation: string;
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

export interface AnalyzeRequest {
  ticker: string;
  horizon: string;
  risk_tolerance: string;
}

export interface AnalysisResponse {
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
    final_decision: any;
  };
  error?: string;
}

export interface MarketSentimentResponse {
  success: boolean;
  sentiment: any;
  timestamp: string;
}

export interface StockDataResponse {
  success: boolean;
  ticker: string;
  data: any;
  timestamp: string;
  error?: string;
}

class ApiClient {
  private async request<T>(endpoint: string, options?: RequestInit): Promise<T> {
    const url = `${API_BASE_URL}${endpoint}`;
    
    try {
      const response = await fetch(url, {
        headers: {
          'Content-Type': 'application/json',
          ...options?.headers,
        },
        ...options,
      });

      if (!response.ok) {
        throw new Error(`HTTP error! status: ${response.status}`);
      }

      return await response.json();
    } catch (error) {
      console.error('API request failed:', error);
      throw error;
    }
  }

  async getStocks(): Promise<{ success: boolean; stocks: Stock[]; count: number }> {
    return this.request('/api/v1/stocks');
  }

  async quickAnalyze(request: QuickAnalysisRequest): Promise<QuickAnalysisResponse> {
    return this.request('/api/v1/quick-analyze', {
      method: 'POST',
      body: JSON.stringify(request),
    });
  }

  async analyze(request: AnalyzeRequest): Promise<AnalysisResponse> {
    return this.request('/api/v1/analyze', {
      method: 'POST',
      body: JSON.stringify(request),
    });
  }

  async getMarketSentiment(timeframe: string = 'current'): Promise<MarketSentimentResponse> {
    return this.request('/api/v1/market-sentiment', {
      method: 'POST',
      body: JSON.stringify({ timeframe }),
    });
  }

  async getStockData(ticker: string): Promise<StockDataResponse> {
    return this.request(`/api/v1/stock/${ticker}/data`);
  }

  async healthCheck(): Promise<{ status: string; timestamp: string; version: string; graph_status: string }> {
    return this.request('/health');
  }
}

export const apiClient = new ApiClient();
