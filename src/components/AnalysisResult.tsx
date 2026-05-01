'use client';

import { FullAnalysis } from '@/services/api';

interface AnalysisResultProps {
  analysis: FullAnalysis;
}

export default function AnalysisResult({ analysis }: AnalysisResultProps) {
  if (!analysis.success) {
    return (
      <div className="bg-red-50 border border-red-200 rounded-lg p-6">
        <h3 className="text-red-800 font-bold mb-2">Lỗi phân tích</h3>
        <p className="text-red-600">{analysis.error}</p>
      </div>
    );
  }

  const { final_decision } = analysis.analysis;
  const getRecommendationColor = (recommendation: string) => {
    switch (recommendation) {
      case 'BUY': return 'text-green-600 bg-green-100 border-green-200';
      case 'SELL': return 'text-red-600 bg-red-100 border-red-200';
      case 'HOLD': return 'text-yellow-600 bg-yellow-100 border-yellow-200';
      default: return 'text-gray-600 bg-gray-100 border-gray-200';
    }
  };

  const getConfidenceColor = (confidence: number) => {
    if (confidence >= 75) return 'text-green-600';
    if (confidence >= 50) return 'text-yellow-600';
    return 'text-red-600';
  };

  return (
    <div className="space-y-6">
      {/* Final Decision */}
      <div className="bg-white rounded-lg shadow-md p-6">
        <h2 className="text-xl font-bold text-gray-900 mb-4">Kết quả phân tích</h2>
        
        <div className="grid md:grid-cols-2 gap-6">
          <div>
            <div className="flex items-center justify-between mb-4">
              <span className="text-lg font-medium">Khuyến nghị:</span>
              <span className={`px-4 py-2 rounded-full font-bold text-lg border ${getRecommendationColor(final_decision.recommendation)}`}>
                {final_decision.recommendation}
              </span>
            </div>
            
            <div className="flex items-center justify-between mb-4">
              <span className="text-lg font-medium">Độ tin cậy:</span>
              <span className={`text-lg font-bold ${getConfidenceColor(final_decision.confidence)}`}>
                {final_decision.confidence}%
              </span>
            </div>
          </div>
          
          <div>
            <h3 className="text-sm font-medium text-gray-500 mb-2">Lý do quyết định:</h3>
            <ul className="space-y-1">
              {final_decision.reasoning.map((reason, index) => (
                <li key={index} className="text-sm text-gray-700 flex items-start">
                  <span className="text-blue-500 mr-2">•</span>
                  {reason}
                </li>
              ))}
            </ul>
          </div>
        </div>

        <div className="mt-6 p-4 bg-gray-50 rounded-lg">
          <h3 className="text-sm font-medium text-gray-500 mb-2">Tóm tắt phân tích:</h3>
          <p className="text-gray-700">{final_decision.summary}</p>
        </div>
      </div>

      {/* Market Analysis */}
      {analysis.analysis.market_analysis && (
        <div className="bg-white rounded-lg shadow-md p-6">
          <h3 className="text-lg font-bold text-gray-900 mb-4">Phân tích thị trường</h3>
          <div className="prose prose-sm max-w-none">
            <p className="text-gray-700">{analysis.analysis.market_analysis.summary || 'Đang cập nhật...'}</p>
          </div>
        </div>
      )}

      {/* Technical Analysis */}
      {analysis.analysis.technical_analysis && (
        <div className="bg-white rounded-lg shadow-md p-6">
          <h3 className="text-lg font-bold text-gray-900 mb-4">Phân tích kỹ thuật</h3>
          <div className="grid grid-cols-2 md:grid-cols-4 gap-4 mb-4">
            <div className="text-center">
              <p className="text-sm text-gray-500">RSI</p>
              <p className="text-lg font-bold">{analysis.analysis.technical_analysis.rsi?.toFixed(2) || 'N/A'}</p>
            </div>
            <div className="text-center">
              <p className="text-sm text-gray-500">MACD</p>
              <p className="text-lg font-bold">{analysis.analysis.technical_analysis.macd?.toFixed(4) || 'N/A'}</p>
            </div>
            <div className="text-center">
              <p className="text-sm text-gray-500">MA20</p>
              <p className="text-lg font-bold">{analysis.analysis.technical_analysis.ma20?.toFixed(0) || 'N/A'}</p>
            </div>
            <div className="text-center">
              <p className="text-sm text-gray-500">MA50</p>
              <p className="text-lg font-bold">{analysis.analysis.technical_analysis.ma50?.toFixed(0) || 'N/A'}</p>
            </div>
          </div>
          <div className="prose prose-sm max-w-none">
            <p className="text-gray-700">{analysis.analysis.technical_analysis.summary || 'Đang cập nhật...'}</p>
          </div>
        </div>
      )}

      {/* News Analysis */}
      {analysis.analysis.news_analysis && (
        <div className="bg-white rounded-lg shadow-md p-6">
          <h3 className="text-lg font-bold text-gray-900 mb-4">Phân tích tin tức</h3>
          <div className="grid grid-cols-2 gap-4 mb-4">
            <div>
              <p className="text-sm text-gray-500">Tâm lý thị trường</p>
              <p className="font-bold">{analysis.analysis.news_analysis.sentiment || 'N/A'}</p>
            </div>
            <div>
              <p className="text-sm text-gray-500">Điểm tâm lý</p>
              <p className="font-bold">{analysis.analysis.news_analysis.sentiment_score?.toFixed(3) || 'N/A'}</p>
            </div>
          </div>
          <div className="prose prose-sm max-w-none">
            <p className="text-gray-700">{analysis.analysis.news_analysis.summary || 'Đang cập nhật...'}</p>
          </div>
        </div>
      )}

      {/* Risk Analysis */}
      {analysis.analysis.risk_analysis && (
        <div className="bg-white rounded-lg shadow-md p-6">
          <h3 className="text-lg font-bold text-gray-900 mb-4">Phân tích rủi ro</h3>
          <div className="grid grid-cols-2 md:grid-cols-4 gap-4 mb-4">
            <div>
              <p className="text-sm text-gray-500">Mức rủi ro</p>
              <p className="font-bold">{analysis.analysis.risk_analysis.risk || 'N/A'}</p>
            </div>
            <div>
              <p className="text-sm text-gray-500">Điểm rủi ro</p>
              <p className="font-bold">{analysis.analysis.risk_analysis.risk_score || 'N/A'}</p>
            </div>
            <div>
              <p className="text-sm text-gray-500">Beta</p>
              <p className="font-bold">{analysis.analysis.risk_analysis.beta?.toFixed(2) || 'N/A'}</p>
            </div>
            <div>
              <p className="text-sm text-gray-500">Biến động</p>
              <p className="font-bold">{analysis.analysis.risk_analysis.volatility?.toFixed(2) || 'N/A'}</p>
            </div>
          </div>
          <div className="prose prose-sm max-w-none">
            <p className="text-gray-700">{analysis.analysis.risk_analysis.summary || 'Đang cập nhật...'}</p>
          </div>
        </div>
      )}

      {/* Timestamp */}
      <div className="text-center text-sm text-gray-500">
        Phân tích lúc: {new Date(analysis.timestamp).toLocaleString('vi-VN')}
      </div>
    </div>
  );
}
