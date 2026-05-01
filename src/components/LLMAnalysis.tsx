'use client';

import { useState, useEffect } from 'react';
import { apiClient, AnalysisResponse } from '@/lib/api';
import { Card, CardContent, CardHeader, CardTitle } from '@/components/ui/card';
import { Button } from '@/components/ui/button';
import { Brain, RefreshCw, CheckCircle, AlertCircle, XCircle } from 'lucide-react';

interface LLMAnalysisProps {
  ticker: string;
  horizon?: string;
  riskTolerance?: string;
}

export function LLMAnalysis({ ticker, horizon = 'swing', riskTolerance = 'medium' }: LLMAnalysisProps) {
  const [analysis, setAnalysis] = useState<AnalysisResponse | null>(null);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState<string | null>(null);

  useEffect(() => {
    if (ticker) {
      loadDetailedAnalysis();
    }
  }, [ticker, horizon, riskTolerance]);

  const loadDetailedAnalysis = async () => {
    try {
      setLoading(true);
      setError(null);
      const response = await apiClient.analyze({
        ticker,
        horizon,
        risk_tolerance: riskTolerance,
      });
      setAnalysis(response);
    } catch (error) {
      setError('Failed to load LLM analysis');
      console.error('LLM Analysis error:', error);
    } finally {
      setLoading(false);
    }
  };

  const getAgentStatus = (agentName: string, data: any) => {
    if (!data) return 'pending';
    if (data.error) return 'error';
    return 'completed';
  };

  const getAgentIcon = (status: string) => {
    switch (status) {
      case 'completed':
        return <CheckCircle className="h-4 w-4 text-green-600" />;
      case 'error':
        return <XCircle className="h-4 w-4 text-red-600" />;
      default:
        return <AlertCircle className="h-4 w-4 text-yellow-600" />;
    }
  };

  if (loading) {
    return (
      <Card>
        <CardHeader>
          <CardTitle className="flex items-center gap-2">
            <Brain className="h-5 w-5" />
            AI Multi-Agent Analysis
          </CardTitle>
        </CardHeader>
        <CardContent>
          <div className="space-y-4">
            {[...Array(5)].map((_, i) => (
              <div key={i} className="h-16 bg-gray-100 rounded animate-pulse" />
            ))}
          </div>
        </CardContent>
      </Card>
    );
  }

  if (error) {
    return (
      <Card>
        <CardHeader>
          <CardTitle className="flex items-center gap-2">
            <Brain className="h-5 w-5" />
            AI Multi-Agent Analysis
          </CardTitle>
        </CardHeader>
        <CardContent>
          <p className="text-red-600 mb-4">{error}</p>
          <Button onClick={loadDetailedAnalysis} size="sm">
            <RefreshCw className="h-4 w-4 mr-2" />
            Retry Analysis
          </Button>
        </CardContent>
      </Card>
    );
  }

  if (!analysis || !analysis.success) {
    return (
      <Card>
        <CardHeader>
          <CardTitle className="flex items-center gap-2">
            <Brain className="h-5 w-5" />
            AI Multi-Agent Analysis
          </CardTitle>
        </CardHeader>
        <CardContent>
          <p className="text-gray-600">
            {analysis?.error || 'No detailed analysis available'}
          </p>
        </CardContent>
      </Card>
    );
  }

  const { analysis: data } = analysis;

  return (
    <div className="space-y-4">
      {/* Analysis Header */}
      <Card>
        <CardHeader>
          <div className="flex items-center justify-between">
            <CardTitle className="flex items-center gap-2">
              <Brain className="h-5 w-5" />
              AI Multi-Agent Analysis
            </CardTitle>
            <Button onClick={loadDetailedAnalysis} variant="outline" size="sm">
              <RefreshCw className="h-4 w-4 mr-2" />
              Refresh
            </Button>
          </div>
          <div className="text-sm text-gray-500">
            Analysis completed at {new Date(analysis.timestamp).toLocaleString()}
          </div>
        </CardHeader>
      </Card>

      {/* Agent Status */}
      <Card>
        <CardHeader>
          <CardTitle>Agent Status</CardTitle>
        </CardHeader>
        <CardContent>
          <div className="grid grid-cols-2 md:grid-cols-3 gap-4">
            {[
              { name: 'Planner', data: data.plan },
              { name: 'Market', data: data.market_analysis },
              { name: 'Technical', data: data.technical_analysis },
              { name: 'News', data: data.news_analysis },
              { name: 'Risk', data: data.risk_analysis },
              { name: 'Decision', data: data.final_decision },
            ].map((agent) => (
              <div key={agent.name} className="flex items-center gap-2">
                {getAgentIcon(getAgentStatus(agent.name, agent.data))}
                <span className="text-sm font-medium">{agent.name}</span>
              </div>
            ))}
          </div>
        </CardContent>
      </Card>

      {/* Final Decision */}
      {data.final_decision && (
        <Card>
          <CardHeader>
            <CardTitle>Final Decision</CardTitle>
          </CardHeader>
          <CardContent>
            <div className="space-y-4">
              {data.final_decision.recommendation && (
                <div>
                  <h4 className="font-semibold mb-2">Recommendation</h4>
                  <p className="text-gray-700">{data.final_decision.recommendation}</p>
                </div>
              )}
              {data.final_decision.reasoning && (
                <div>
                  <h4 className="font-semibold mb-2">Reasoning</h4>
                  <p className="text-gray-700 whitespace-pre-wrap">{data.final_decision.reasoning}</p>
                </div>
              )}
              {data.final_decision.confidence && (
                <div>
                  <h4 className="font-semibold mb-2">Confidence Level</h4>
                  <div className="flex items-center gap-2">
                    <div className="flex-1 bg-gray-200 rounded-full h-2">
                      <div
                        className="bg-blue-600 h-2 rounded-full"
                        style={{ width: `${data.final_decision.confidence}%` }}
                      />
                    </div>
                    <span className="text-sm font-medium">{data.final_decision.confidence}%</span>
                  </div>
                </div>
              )}
            </div>
          </CardContent>
        </Card>
      )}

      {/* Risk Analysis */}
      {data.risk_analysis && (
        <Card>
          <CardHeader>
            <CardTitle>Risk Analysis</CardTitle>
          </CardHeader>
          <CardContent>
            <div className="space-y-4">
              {data.risk_analysis.risk_level && (
                <div>
                  <h4 className="font-semibold mb-2">Risk Level</h4>
                  <p className="text-gray-700">{data.risk_analysis.risk_level}</p>
                </div>
              )}
              {data.risk_analysis.factors && (
                <div>
                  <h4 className="font-semibold mb-2">Risk Factors</h4>
                  <ul className="list-disc list-inside space-y-1">
                    {data.risk_analysis.factors.map((factor: string, index: number) => (
                      <li key={index} className="text-gray-700">{factor}</li>
                    ))}
                  </ul>
                </div>
              )}
            </div>
          </CardContent>
        </Card>
      )}

      {/* Market Analysis */}
      {data.market_analysis && (
        <Card>
          <CardHeader>
            <CardTitle>Market Analysis</CardTitle>
          </CardHeader>
          <CardContent>
            <div className="space-y-4">
              {data.market_analysis.overview && (
                <div>
                  <h4 className="font-semibold mb-2">Market Overview</h4>
                  <p className="text-gray-700">{data.market_analysis.overview}</p>
                </div>
              )}
              {data.market_analysis.trends && (
                <div>
                  <h4 className="font-semibold mb-2">Market Trends</h4>
                  <p className="text-gray-700">{data.market_analysis.trends}</p>
                </div>
              )}
            </div>
          </CardContent>
        </Card>
      )}

      {/* Technical Analysis */}
      {data.technical_analysis && (
        <Card>
          <CardHeader>
            <CardTitle>Technical Analysis</CardTitle>
          </CardHeader>
          <CardContent>
            <div className="space-y-4">
              {data.technical_analysis.summary && (
                <div>
                  <h4 className="font-semibold mb-2">Technical Summary</h4>
                  <p className="text-gray-700">{data.technical_analysis.summary}</p>
                </div>
              )}
              {data.technical_analysis.signals && (
                <div>
                  <h4 className="font-semibold mb-2">Trading Signals</h4>
                  <p className="text-gray-700">{data.technical_analysis.signals}</p>
                </div>
              )}
            </div>
          </CardContent>
        </Card>
      )}

      {/* News Analysis */}
      {data.news_analysis && (
        <Card>
          <CardHeader>
            <CardTitle>News Analysis</CardTitle>
          </CardHeader>
          <CardContent>
            <div className="space-y-4">
              {data.news_analysis.sentiment && (
                <div>
                  <h4 className="font-semibold mb-2">News Sentiment</h4>
                  <p className="text-gray-700">{data.news_analysis.sentiment}</p>
                </div>
              )}
              {data.news_analysis.key_news && (
                <div>
                  <h4 className="font-semibold mb-2">Key News</h4>
                  <p className="text-gray-700">{data.news_analysis.key_news}</p>
                </div>
              )}
            </div>
          </CardContent>
        </Card>
      )}
    </div>
  );
}
