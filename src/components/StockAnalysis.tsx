'use client';

import { useState, useEffect } from 'react';
import { apiClient, QuickAnalysisResponse } from '@/lib/api';
import { Card, CardContent, CardHeader, CardTitle } from '@/components/ui/card';
import { Button } from '@/components/ui/button';
import { formatCurrency, formatPercentage, getRecommendationColor, getSentimentColor, getConfidenceColor } from '@/lib/utils';
import { TrendingUp, TrendingDown, Minus, RefreshCw, BarChart3, Newspaper } from 'lucide-react';
import { LineChart, Line, XAxis, YAxis, CartesianGrid, Tooltip, ResponsiveContainer, BarChart, Bar } from 'recharts';
import { LLMAnalysis } from '@/components/LLMAnalysis';
import { Tabs, TabsList, TabsTrigger, TabsContent } from '@/components/ui/tabs';

interface StockAnalysisProps {
  ticker: string;
}

export function StockAnalysis({ ticker }: StockAnalysisProps) {
  const [analysis, setAnalysis] = useState<QuickAnalysisResponse | null>(null);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState<string | null>(null);

  useEffect(() => {
    if (ticker) {
      loadAnalysis();
    }
  }, [ticker]);

  const loadAnalysis = async () => {
    try {
      setLoading(true);
      setError(null);
      const response = await apiClient.quickAnalyze({ ticker });
      setAnalysis(response);
    } catch (error) {
      setError('Failed to load analysis');
      console.error('Analysis error:', error);
    } finally {
      setLoading(false);
    }
  };

  const getRecommendationIcon = (recommendation: string) => {
    switch (recommendation.toLowerCase()) {
      case 'buy':
        return <TrendingUp className="h-5 w-5 text-green-600" />;
      case 'sell':
        return <TrendingDown className="h-5 w-5 text-red-600" />;
      default:
        return <Minus className="h-5 w-5 text-yellow-600" />;
    }
  };

  if (loading) {
    return (
      <div className="space-y-4">
        <Card>
          <CardHeader>
            <CardTitle>Loading Analysis...</CardTitle>
          </CardHeader>
          <CardContent>
            <div className="space-y-4">
              {[...Array(4)].map((_, i) => (
                <div key={i} className="h-20 bg-gray-100 rounded animate-pulse" />
              ))}
            </div>
          </CardContent>
        </Card>
      </div>
    );
  }

  if (error) {
    return (
      <Card>
        <CardHeader>
          <CardTitle>Error</CardTitle>
        </CardHeader>
        <CardContent>
          <p className="text-red-600">{error}</p>
          <Button onClick={loadAnalysis} className="mt-2">
            <RefreshCw className="h-4 w-4 mr-2" />
            Retry
          </Button>
        </CardContent>
      </Card>
    );
  }

  if (!analysis) {
    return null;
  }

  const chartData = [
    { name: 'RSI', value: analysis.key_signals.rsi, max: 100 },
    { name: 'MACD', value: Math.abs(analysis.key_signals.macd) * 100, max: 100 },
    { name: 'Volume Ratio', value: analysis.key_signals.volume_ratio * 50, max: 100 },
    { name: 'Sentiment', value: (analysis.key_signals.sentiment_score + 1) * 50, max: 100 },
  ];

  return (
    <div className="space-y-4">
      {/* Header */}
      <Card>
        <CardHeader>
          <div className="flex items-center justify-between">
            <div>
              <CardTitle className="flex items-center gap-2">
                {analysis.ticker}
                <span className="text-lg font-normal text-gray-500">
                  {analysis.company_name}
                </span>
              </CardTitle>
              <p className="text-2xl font-bold mt-2">
                {formatCurrency(analysis.current_price)}
              </p>
            </div>
            <div className="text-right">
              <div className={`flex items-center gap-2 px-3 py-1 rounded-full ${getRecommendationColor(analysis.recommendation)}`}>
                {getRecommendationIcon(analysis.recommendation)}
                <span className="font-semibold">{analysis.recommendation}</span>
              </div>
              <div className={`mt-2 ${getConfidenceColor(analysis.confidence)}`}>
                Confidence: {analysis.confidence}%
              </div>
            </div>
          </div>
        </CardHeader>
      </Card>

      {/* Tabs */}
      <Tabs defaultValue="quick" className="w-full">
        <TabsList className="grid w-full grid-cols-2">
          <TabsTrigger value="quick">Quick Analysis</TabsTrigger>
          <TabsTrigger value="ai">AI Multi-Agent Analysis</TabsTrigger>
        </TabsList>

        <TabsContent value="quick" className="space-y-4">
          {/* Technical Indicators */}
          <Card>
            <CardHeader>
              <CardTitle className="flex items-center gap-2">
                <BarChart3 className="h-5 w-5" />
                Technical Indicators
              </CardTitle>
            </CardHeader>
            <CardContent>
              <div className="grid grid-cols-2 md:grid-cols-4 gap-4">
                <div>
                  <div className="text-sm text-gray-500">RSI</div>
                  <div className="text-lg font-semibold">{analysis.key_signals.rsi.toFixed(1)}</div>
                </div>
                <div>
                  <div className="text-sm text-gray-500">MACD</div>
                  <div className="text-lg font-semibold">{analysis.key_signals.macd.toFixed(3)}</div>
                </div>
                <div>
                  <div className="text-sm text-gray-500">MA20</div>
                  <div className="text-lg font-semibold">{formatCurrency(analysis.key_signals.ma20)}</div>
                </div>
                <div>
                  <div className="text-sm text-gray-500">MA50</div>
                  <div className="text-lg font-semibold">{formatCurrency(analysis.key_signals.ma50)}</div>
                </div>
              </div>
            </CardContent>
          </Card>

          {/* Sentiment Analysis */}
          <Card>
            <CardHeader>
              <CardTitle className="flex items-center gap-2">
                <Newspaper className="h-5 w-5" />
                Market Sentiment
              </CardTitle>
            </CardHeader>
            <CardContent>
              <div className="flex items-center justify-between">
                <div>
                  <div className={`inline-flex px-3 py-1 rounded-full ${getSentimentColor(analysis.key_signals.sentiment)}`}>
                    {analysis.key_signals.sentiment}
                  </div>
                  <div className="mt-2 text-sm text-gray-500">
                    Sentiment Score: {analysis.key_signals.sentiment_score.toFixed(2)}
                  </div>
                </div>
                <div>
                  <div className="text-sm text-gray-500">Volume Ratio</div>
                  <div className="text-lg font-semibold">{analysis.key_signals.volume_ratio.toFixed(2)}x</div>
                </div>
              </div>
            </CardContent>
          </Card>

          {/* Chart */}
          <Card>
            <CardHeader>
              <CardTitle>Indicator Overview</CardTitle>
            </CardHeader>
            <CardContent>
              <ResponsiveContainer width="100%" height={200}>
                <BarChart data={chartData}>
                  <CartesianGrid strokeDasharray="3 3" />
                  <XAxis dataKey="name" />
                  <YAxis domain={[0, 100]} />
                  <Tooltip />
                  <Bar dataKey="value" fill="#3b82f6" />
                </BarChart>
              </ResponsiveContainer>
            </CardContent>
          </Card>

          {/* Refresh Button */}
          <div className="flex justify-center">
            <Button onClick={loadAnalysis} variant="outline">
              <RefreshCw className="h-4 w-4 mr-2" />
              Refresh Quick Analysis
            </Button>
          </div>
        </TabsContent>

        <TabsContent value="ai">
          <LLMAnalysis ticker={ticker} />
        </TabsContent>
      </Tabs>
    </div>
  );
}
