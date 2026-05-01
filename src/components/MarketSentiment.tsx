'use client';

import { useState, useEffect } from 'react';
import { apiClient, MarketSentimentResponse } from '@/lib/api';
import { Card, CardContent, CardHeader, CardTitle } from '@/components/ui/card';
import { Button } from '@/components/ui/button';
import { getSentimentColor } from '@/lib/utils';
import { TrendingUp, TrendingDown, Minus, RefreshCw, Activity } from 'lucide-react';

export function MarketSentiment() {
  const [sentiment, setSentiment] = useState<MarketSentimentResponse | null>(null);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState<string | null>(null);

  useEffect(() => {
    loadSentiment();
  }, []);

  const loadSentiment = async () => {
    try {
      setLoading(true);
      setError(null);
      const response = await apiClient.getMarketSentiment();
      setSentiment(response);
    } catch (error) {
      setError('Failed to load market sentiment');
      console.error('Sentiment error:', error);
    } finally {
      setLoading(false);
    }
  };

  const getSentimentIcon = (sentiment: string) => {
    switch (sentiment.toLowerCase()) {
      case 'positive':
        return <TrendingUp className="h-6 w-6 text-green-600" />;
      case 'negative':
        return <TrendingDown className="h-6 w-6 text-red-600" />;
      default:
        return <Minus className="h-6 w-6 text-yellow-600" />;
    }
  };

  if (loading) {
    return (
      <Card>
        <CardHeader>
          <CardTitle>Market Sentiment</CardTitle>
        </CardHeader>
        <CardContent>
          <div className="h-32 bg-gray-100 rounded animate-pulse" />
        </CardContent>
      </Card>
    );
  }

  if (error) {
    return (
      <Card>
        <CardHeader>
          <CardTitle>Market Sentiment</CardTitle>
        </CardHeader>
        <CardContent>
          <p className="text-red-600">{error}</p>
          <Button onClick={loadSentiment} className="mt-2" size="sm">
            <RefreshCw className="h-4 w-4 mr-2" />
            Retry
          </Button>
        </CardContent>
      </Card>
    );
  }

  if (!sentiment) {
    return null;
  }

  const sentimentData = sentiment.sentiment;
  const overallSentiment = sentimentData.overall || 'NEUTRAL';
  const sentimentScore = sentimentData.score || 0;

  return (
    <Card>
      <CardHeader>
        <div className="flex items-center justify-between">
          <CardTitle className="flex items-center gap-2">
            <Activity className="h-5 w-5" />
            Vietnam Market Sentiment
          </CardTitle>
          <Button onClick={loadSentiment} variant="ghost" size="sm">
            <RefreshCw className="h-4 w-4" />
          </Button>
        </div>
      </CardHeader>
      <CardContent>
        <div className="space-y-4">
          {/* Overall Sentiment */}
          <div className="flex items-center justify-between">
            <div className="flex items-center gap-3">
              {getSentimentIcon(overallSentiment)}
              <div>
                <div className={`inline-flex px-3 py-1 rounded-full ${getSentimentColor(overallSentiment)}`}>
                  <span className="font-semibold">{overallSentiment}</span>
                </div>
                <div className="text-sm text-gray-500 mt-1">
                  Score: {sentimentScore.toFixed(2)}
                </div>
              </div>
            </div>
          </div>

          {/* Market Indicators */}
          {sentimentData.indicators && (
            <div className="grid grid-cols-2 md:grid-cols-4 gap-4">
              {Object.entries(sentimentData.indicators).map(([key, value]) => (
                <div key={key} className="text-center">
                  <div className="text-sm text-gray-500 capitalize">
                    {key.replace('_', ' ')}
                  </div>
                  <div className="text-lg font-semibold">
                    {typeof value === 'number' ? value.toFixed(1) : String(value)}
                  </div>
                </div>
              ))}
            </div>
          )}

          {/* Market Summary */}
          {sentimentData.summary && (
            <div>
              <h4 className="font-semibold mb-2">Market Summary</h4>
              <p className="text-sm text-gray-600">{sentimentData.summary}</p>
            </div>
          )}

          {/* Last Updated */}
          <div className="text-xs text-gray-400 text-right">
            Last updated: {new Date(sentiment.timestamp).toLocaleString()}
          </div>
        </div>
      </CardContent>
    </Card>
  );
}
