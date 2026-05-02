export interface Stock {
  ticker: string;
  name: string;
  current_price: number;
  change?: number;
  change_percent?: number;
  volume: number;
  market_cap?: number;
  industry?: string;
  pe_ratio?: number;
}

export interface StockAnalysis {
  ticker: string;
  horizon: string;
  timestamp: string;
  analysis: {
    plan?: any;
    market_analysis?: any;
    technical_analysis?: any;
    news_analysis?: any;
    risk_analysis?: any;
    final_decision?: any;
  };
  success: boolean;
  error?: string;
}

export interface QuickAnalysis {
  ticker: string;
  price: number;
  change: number;
  changePercent: number;
  recommendation: "BUY" | "SELL" | "HOLD";
  confidence: number;
  technicalSignal: string;
  sentimentScore: number;
  timestamp: string;
}

export interface ChatMessage {
  id: string;
  role: "user" | "assistant";
  content: string;
  timestamp: string;
  ticker?: string;
  analysis?: any;
}

export interface MarketSentiment {
  overall: "bullish" | "bearish" | "neutral";
  score: number;
  factors: string[];
  timestamp: string;
}
