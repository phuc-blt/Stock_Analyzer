'use client';

import { useState, useEffect } from 'react';
import { useParams, useRouter } from 'next/navigation';
import { apiService, FullAnalysis, Stock } from '../../../services/api';
import AnalysisResult from '../../../components/AnalysisResult';

export default function AnalyzePage() {
  const params = useParams();
  const router = useRouter();
  const ticker = params.ticker as string;

  const [analysis, setAnalysis] = useState<FullAnalysis | null>(null);
  const [stockData, setStockData] = useState<Stock | null>(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);
  const [horizon, setHorizon] = useState('swing');
  const [riskTolerance, setRiskTolerance] = useState('medium');

  useEffect(() => {
    if (ticker) {
      loadAnalysis();
    }
  }, [ticker, horizon, riskTolerance]);

  const loadAnalysis = async () => {
    try {
      setLoading(true);
      setError(null);

      // Load stock data and full analysis in parallel
      const [analysisResult, stockResult] = await Promise.all([
        apiService.fullAnalyze(ticker, horizon, riskTolerance),
        apiService.getStockData(ticker)
      ]);

      setAnalysis(analysisResult);
      
      if (stockResult.success) {
        setStockData(stockResult.data);
      }
    } catch (err) {
      setError(err instanceof Error ? err.message : 'Lỗi khi phân tích');
    } finally {
      setLoading(false);
    }
  };

  const handleBack = () => {
    router.push('/');
  };

  if (loading) {
    return (
      <div className="min-h-screen bg-gray-50 flex items-center justify-center">
        <div className="text-center">
          <div className="animate-spin rounded-full h-12 w-12 border-b-2 border-blue-600 mx-auto mb-4"></div>
          <p className="text-gray-600">Đang phân tích cổ phiếu {ticker?.toUpperCase()}...</p>
          <p className="text-sm text-gray-500 mt-2">Hệ thống multi-agent đang hoạt động</p>
        </div>
      </div>
    );
  }

  if (error) {
    return (
      <div className="min-h-screen bg-gray-50 flex items-center justify-center">
        <div className="bg-red-50 border border-red-200 rounded-lg p-6 max-w-md">
          <h3 className="text-red-800 font-bold mb-2">Lỗi phân tích</h3>
          <p className="text-red-600 mb-4">{error}</p>
          <div className="flex space-x-3">
            <button
              onClick={loadAnalysis}
              className="bg-red-600 text-white px-4 py-2 rounded hover:bg-red-700"
            >
              Thử lại
            </button>
            <button
              onClick={handleBack}
              className="bg-gray-600 text-white px-4 py-2 rounded hover:bg-gray-700"
            >
              Quay lại
            </button>
          </div>
        </div>
      </div>
    );
  }

  return (
    <div className="min-h-screen bg-gray-50">
      {/* Header */}
      <header className="bg-white shadow-sm border-b">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-6">
          <div className="flex justify-between items-center">
            <div className="flex items-center space-x-4">
              <button
                onClick={handleBack}
                className="text-gray-500 hover:text-gray-700 flex items-center space-x-2"
              >
                <svg className="h-5 w-5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                  <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M15 19l-7-7 7-7" />
                </svg>
                <span>Quay lại</span>
              </button>
              <div>
                <h1 className="text-3xl font-bold text-gray-900">
                  {ticker?.toUpperCase()}
                </h1>
                <p className="text-gray-600 mt-1">
                  {stockData?.name || 'Đang tải...'}
                </p>
              </div>
            </div>
            
            {/* Analysis Controls */}
            <div className="flex space-x-4">
              <div>
                <label className="block text-sm font-medium text-gray-700 mb-1">
                  Khung thời gian
                </label>
                <select
                  value={horizon}
                  onChange={(e) => setHorizon(e.target.value)}
                  className="border border-gray-300 rounded px-3 py-2 text-sm focus:ring-2 focus:ring-blue-500"
                >
                  <option value="short_term">Ngắn hạn</option>
                  <option value="swing">Swing trading</option>
                  <option value="long_term">Dài hạn</option>
                </select>
              </div>
              <div>
                <label className="block text-sm font-medium text-gray-700 mb-1">
                  Mức độ rủi ro
                </label>
                <select
                  value={riskTolerance}
                  onChange={(e) => setRiskTolerance(e.target.value)}
                  className="border border-gray-300 rounded px-3 py-2 text-sm focus:ring-2 focus:ring-blue-500"
                >
                  <option value="low">Thấp</option>
                  <option value="medium">Trung bình</option>
                  <option value="high">Cao</option>
                </select>
              </div>
              <button
                onClick={loadAnalysis}
                className="bg-blue-600 text-white px-4 py-2 rounded hover:bg-blue-700 self-end"
              >
                Phân tích lại
              </button>
            </div>
          </div>
        </div>
      </header>

      {/* Stock Info Bar */}
      {stockData && (
        <div className="bg-white border-b">
          <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-4">
            <div className="grid grid-cols-2 md:grid-cols-6 gap-4 text-center">
              <div>
                <p className="text-sm text-gray-500">Giá hiện tại</p>
                <p className="text-lg font-bold text-gray-900">
                  {new Intl.NumberFormat('vi-VN', {
                    style: 'currency',
                    currency: 'VND',
                    minimumFractionDigits: 0,
                  }).format(stockData.price)}
                </p>
              </div>
              <div>
                <p className="text-sm text-gray-500">P/E Ratio</p>
                <p className="text-lg font-bold text-gray-900">{stockData.pe_ratio.toFixed(1)}</p>
              </div>
              <div>
                <p className="text-sm text-gray-500">Vốn hóa</p>
                <p className="text-lg font-bold text-gray-900">
                  {stockData.market_cap >= 1000000 
                    ? `${(stockData.market_cap / 1000000).toFixed(1)}T`
                    : `${(stockData.market_cap / 1000).toFixed(0)}B`
                  } VND
                </p>
              </div>
              <div>
                <p className="text-sm text-gray-500">Khối lượng</p>
                <p className="text-lg font-bold text-gray-900">
                  {stockData.volume.toLocaleString('vi-VN')}
                </p>
              </div>
              <div>
                <p className="text-sm text-gray-500">Sàn</p>
                <p className="text-lg font-bold text-gray-900">{stockData.exchange}</p>
              </div>
              <div>
                <p className="text-sm text-gray-500">Ngành</p>
                <p className="text-lg font-bold text-gray-900">{stockData.industry}</p>
              </div>
            </div>
          </div>
        </div>
      )}

      {/* Analysis Results */}
      <main className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-8">
        {analysis && <AnalysisResult analysis={analysis} />}
      </main>

      {/* Footer */}
      <footer className="bg-white border-t mt-12">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-6">
          <div className="text-center text-sm text-gray-500">
            <p>© 2024 Vietnam Stock Multi-Agent Analyzer</p>
            <p className="mt-1">Powered by LangGraph • FastAPI • Next.js</p>
          </div>
        </div>
      </footer>
    </div>
  );
}
