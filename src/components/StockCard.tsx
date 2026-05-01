'use client';

import { Stock, QuickAnalysis } from '@/services/api';
import { useState } from 'react';

interface StockCardProps {
  stock: Stock;
  onAnalyze?: (ticker: string) => void;
}

export default function StockCard({ stock, onAnalyze }: StockCardProps) {
  const [analysis, setAnalysis] = useState<QuickAnalysis | null>(null);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState<string | null>(null);

  const handleQuickAnalyze = async () => {
    if (!onAnalyze) return;
    
    setLoading(true);
    setError(null);
    
    try {
      const result = await onAnalyze(stock.ticker);
      setAnalysis(result);
    } catch (err) {
      setError(err instanceof Error ? err.message : 'Analysis failed');
    } finally {
      setLoading(false);
    }
  };

  const getRecommendationColor = (recommendation: string) => {
    switch (recommendation) {
      case 'BUY': return 'text-green-600 bg-green-100';
      case 'SELL': return 'text-red-600 bg-red-100';
      case 'HOLD': return 'text-yellow-600 bg-yellow-100';
      default: return 'text-gray-600 bg-gray-100';
    }
  };

  const formatPrice = (price: number) => {
    return new Intl.NumberFormat('vi-VN', {
      style: 'currency',
      currency: 'VND',
      minimumFractionDigits: 0,
    }).format(price);
  };

  const formatMarketCap = (marketCap: number) => {
    if (marketCap >= 1000000) {
      return `${(marketCap / 1000000).toFixed(1)}T VND`;
    }
    return `${(marketCap / 1000).toFixed(0)}B VND`;
  };

  return (
    <div className="bg-white rounded-lg shadow-md p-6 hover:shadow-lg transition-shadow">
      <div className="flex justify-between items-start mb-4">
        <div>
          <h3 className="text-lg font-bold text-gray-900">{stock.ticker}</h3>
          <p className="text-sm text-gray-600">{stock.name}</p>
          <p className="text-xs text-gray-500 mt-1">{stock.industry}</p>
        </div>
        <div className="text-right">
          <p className="text-2xl font-bold text-gray-900">{formatPrice(stock.current_price)}</p>
          <p className="text-xs text-gray-500">P/E: {stock.pe_ratio.toFixed(1)}</p>
        </div>
      </div>

      <div className="grid grid-cols-2 gap-4 mb-4">
        <div>
          <p className="text-xs text-gray-500">Vốn hóa</p>
          <p className="text-sm font-semibold">{formatMarketCap(stock.market_cap)}</p>
        </div>
        <div>
          <p className="text-xs text-gray-500">Khối lượng</p>
          <p className="text-sm font-semibold">{stock.volume.toLocaleString('vi-VN')}</p>
        </div>
      </div>

      {analysis && (
        <div className="border-t pt-4 mb-4">
          <div className="flex justify-between items-center mb-2">
            <span className="text-sm font-medium">Khuyến nghị:</span>
            <span className={`px-2 py-1 rounded-full text-xs font-bold ${getRecommendationColor(analysis.recommendation)}`}>
              {analysis.recommendation}
            </span>
          </div>
          <div className="flex justify-between items-center mb-2">
            <span className="text-sm font-medium">Độ tin cậy:</span>
            <span className="text-sm font-bold">{analysis.confidence}%</span>
          </div>
          <div className="grid grid-cols-3 gap-2 text-xs">
            <div>
              <span className="text-gray-500">RSI:</span>
              <span className="ml-1 font-medium">{analysis.key_signals.rsi.toFixed(1)}</span>
            </div>
            <div>
              <span className="text-gray-500">MACD:</span>
              <span className="ml-1 font-medium">{analysis.key_signals.macd.toFixed(2)}</span>
            </div>
            <div>
              <span className="text-gray-500">Tâm lý:</span>
              <span className="ml-1 font-medium">{analysis.key_signals.sentiment}</span>
            </div>
          </div>
        </div>
      )}

      {error && (
        <div className="bg-red-50 border border-red-200 text-red-700 px-3 py-2 rounded text-sm mb-4">
          {error}
        </div>
      )}

      <button
        onClick={handleQuickAnalyze}
        disabled={loading || !onAnalyze}
        className="w-full bg-blue-600 text-white py-2 px-4 rounded hover:bg-blue-700 disabled:bg-gray-400 disabled:cursor-not-allowed transition-colors"
      >
        {loading ? 'Đang phân tích...' : 'Phân tích nhanh'}
      </button>
    </div>
  );
}
