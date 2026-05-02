"use client";

import { useState, useEffect } from "react";
import { Card, CardContent, CardHeader, CardTitle } from "@/components/ui/card";
import { Badge } from "@/components/ui/badge";
import { Tabs, TabsContent, TabsList, TabsTrigger } from "@/components/ui/tabs";
import { TrendingUp, TrendingDown, Brain, Newspaper, Shield, Target } from "lucide-react";
import { StockAnalysis } from "@/types/stock";
import { StockChart } from "@/components/stock-chart";

interface AnalysisDashboardProps {
  ticker: string;
  analysis?: any;
  isLoading?: boolean;
}

export function AnalysisDashboard({ ticker, analysis, isLoading }: AnalysisDashboardProps) {
  if (isLoading) {
    return (
      <div className="space-y-6">
        <div className="animate-pulse">
          <div className="h-8 bg-gray-200 rounded mb-4"></div>
          <div className="h-40 bg-gray-200 rounded mb-4"></div>
          <div className="h-40 bg-gray-200 rounded mb-4"></div>
          <div className="h-40 bg-gray-200 rounded"></div>
        </div>
      </div>
    );
  }

  if (!analysis || !analysis.success) {
    return (
      <Card>
        <CardContent className="p-6 text-center">
          <p className="text-gray-500">
            {analysis?.error || "Chưa có phân tích cho cổ phiếu này"}
          </p>
        </CardContent>
      </Card>
    );
  }

  // Quick-analyze data structure
  const { recommendation, confidence, key_signals } = analysis;

  const getRecommendationColor = (recommendation?: string) => {
    switch (recommendation?.toLowerCase()) {
      case "buy":
        return "bg-green-100 text-green-800 border-green-200";
      case "sell":
        return "bg-red-100 text-red-800 border-red-200";
      default:
        return "bg-gray-100 text-gray-800 border-gray-200";
    }
  };

  const getConfidenceLevel = (confidence?: number) => {
    if (!confidence) return "Không có dữ liệu";
    if (confidence >= 80) return "Rất cao";
    if (confidence >= 60) return "Cao";
    if (confidence >= 40) return "Trung bình";
    return "Thấp";
  };

  return (
    <div className="space-y-6">
      {/* Stock Chart */}
      <StockChart ticker={ticker} isLoading={isLoading} />

      {/* Final Decision Card */}
      {recommendation && (
        <Card className="border-2">
          <CardHeader className="pb-4">
            <CardTitle className="flex items-center space-x-2">
              <Target className="h-5 w-5" />
              <span className="font-semibold">Khuyến Nghị Cuối Cùng</span>
            </CardTitle>
          </CardHeader>
          <CardContent>
            <div className="flex items-center space-x-4 mb-4">
              <Badge className={`text-lg px-4 py-2 ${getRecommendationColor(recommendation)}`}>
                {recommendation?.toUpperCase() || "KHÔNG XÁC ĐỊNH"}
              </Badge>
              <div className="text-sm text-muted-foreground">
                <div>Độ tin cậy: <span className="font-semibold">{getConfidenceLevel(confidence)}</span></div>
                {confidence && (
                  <div className="w-32 bg-gray-200 rounded-full h-2 mt-1">
                    <div
                      className="bg-blue-600 h-2 rounded-full"
                      style={{ width: `${confidence}%` }}
                    ></div>
                  </div>
                )}
              </div>
            </div>
            <div className="bg-muted p-4 rounded-lg">
              <h4 className="font-semibold mb-2">Phân tích nhanh:</h4>
              <p className="text-sm text-muted-foreground">
                Khuyến nghị dựa trên các chỉ báo kỹ thuật và tình cảm thị trường hiện tại.
              </p>
            </div>
          </CardContent>
        </Card>
      )}

      <Tabs defaultValue="technical" className="space-y-4">
        <TabsList className="grid w-full grid-cols-4">
          <TabsTrigger value="technical" className="flex items-center space-x-2">
            <TrendingUp className="h-4 w-4" />
            <span>Kỹ thuật</span>
          </TabsTrigger>
          <TabsTrigger value="market" className="flex items-center space-x-2">
            <Brain className="h-4 w-4" />
            <span>Thị trường</span>
          </TabsTrigger>
          <TabsTrigger value="news" className="flex items-center space-x-2">
            <Newspaper className="h-4 w-4" />
            <span>Tin tức</span>
          </TabsTrigger>
          <TabsTrigger value="risk" className="flex items-center space-x-2">
            <Shield className="h-4 w-4" />
            <span>Rủi ro</span>
          </TabsTrigger>
        </TabsList>

        {/* Technical Analysis */}
        <TabsContent value="technical">
          <Card>
            <CardHeader>
              <CardTitle className="flex items-center space-x-2">
                <TrendingUp className="h-5 w-5" />
                <span>Phân Tích Kỹ Thuật</span>
              </CardTitle>
            </CardHeader>
            <CardContent>
              {key_signals ? (
                <div className="space-y-4">
                  <div>
                    <h4 className="font-semibold mb-2">Chỉ báo quan trọng:</h4>
                    <div className="grid grid-cols-2 gap-4">
                      {Object.entries(key_signals).map(([key, value]) => (
                        <div key={key} className="flex justify-between">
                          <span className="text-sm font-medium">{key}:</span>
                          <span className="text-sm">{String(value)}</span>
                        </div>
                      ))}
                    </div>
                  </div>
                </div>
              ) : (
                <p className="text-gray-500">Chưa có dữ liệu phân tích kỹ thuật</p>
              )}
            </CardContent>
          </Card>
        </TabsContent>

        {/* Market Analysis */}
        <TabsContent value="market">
          <Card>
            <CardHeader>
              <CardTitle className="flex items-center space-x-2">
                <Brain className="h-5 w-5" />
                <span>Phân Tích Thị Trường</span>
              </CardTitle>
            </CardHeader>
            <CardContent>
              {key_signals ? (
                <div className="space-y-4">
                  <div>
                    <h4 className="font-semibold mb-2">Sentiment thị trường:</h4>
                    <div className="flex items-center space-x-2">
                      <Badge className={
                        key_signals.sentiment === "POSITIVE" ? "bg-green-100 text-green-800" :
                        key_signals.sentiment === "NEGATIVE" ? "bg-red-100 text-red-800" :
                        "bg-gray-100 text-gray-800"
                      }>
                        {key_signals.sentiment || "Không xác định"}
                      </Badge>
                      {key_signals.sentiment_score && (
                        <span className="text-sm text-gray-600">
                          (Score: {key_signals.sentiment_score})
                        </span>
                      )}
                    </div>
                  </div>
                  {key_signals.pe_ratio && (
                    <div>
                      <h4 className="font-semibold mb-2">P/E Ratio:</h4>
                      <p className="text-sm text-gray-700">{key_signals.pe_ratio}</p>
                    </div>
                  )}
                </div>
              ) : (
                <p className="text-gray-500">Chưa có dữ liệu phân tích thị trường</p>
              )}
            </CardContent>
          </Card>
        </TabsContent>

        {/* News Analysis */}
        <TabsContent value="news">
          <Card>
            <CardHeader>
              <CardTitle className="flex items-center space-x-2">
                <Newspaper className="h-5 w-5" />
                <span>Phân Tích Tin Tức</span>
              </CardTitle>
            </CardHeader>
            <CardContent>
              {key_signals ? (
                <div className="space-y-4">
                  <div>
                    <h4 className="font-semibold mb-2">Tình cảm tin tức:</h4>
                    <div className="flex items-center space-x-2">
                      <Badge className={
                        key_signals.sentiment === "POSITIVE" ? "bg-green-100 text-green-800" :
                        key_signals.sentiment === "NEGATIVE" ? "bg-red-100 text-red-800" :
                        "bg-gray-100 text-gray-800"
                      }>
                        {key_signals.sentiment === "POSITIVE" ? "Tích cực" :
                         key_signals.sentiment === "NEGATIVE" ? "Tiêu cực" : "Trung lập"}
                      </Badge>
                      {key_signals.sentiment_score && (
                        <span className="text-sm text-gray-600">
                          (Score: {key_signals.sentiment_score})
                        </span>
                      )}
                    </div>
                  </div>
                </div>
              ) : (
                <p className="text-gray-500">Chưa có dữ liệu phân tích tin tức</p>
              )}
            </CardContent>
          </Card>
        </TabsContent>

        {/* Risk Analysis */}
        <TabsContent value="risk">
          <Card>
            <CardHeader>
              <CardTitle className="flex items-center space-x-2">
                <Shield className="h-5 w-5" />
                <span>Phân Tích Rủi Ro</span>
              </CardTitle>
            </CardHeader>
            <CardContent>
              {key_signals ? (
                <div className="space-y-4">
                  <div>
                    <h4 className="font-semibold mb-2">Các chỉ báo rủi ro:</h4>
                    <div className="space-y-2">
                      <div className="text-sm text-gray-700">• RSI: {key_signals.rsi} {key_signals.rsi > 70 ? '(Quá mua)' : key_signals.rsi < 30 ? '(Quá bán)' : '(Bình thường)'}</div>
                      <div className="text-sm text-gray-700">• Volume Ratio: {key_signals.volume_ratio} {key_signals.volume_ratio < 1 ? '(Thấp)' : '(Cao)'}</div>
                      <div className="text-sm text-gray-700">• P/E Ratio: {key_signals.pe_ratio} {key_signals.pe_ratio > 20 ? '(Cao)' : '(Hợp lý)'}</div>
                    </div>
                  </div>
                </div>
              ) : (
                <p className="text-gray-500">Chưa có dữ liệu phân tích rủi ro</p>
              )}
            </CardContent>
          </Card>
        </TabsContent>
      </Tabs>
    </div>
  );
}
