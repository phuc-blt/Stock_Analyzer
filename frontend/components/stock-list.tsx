"use client";

import { useState, useEffect } from "react";
import { Card, CardContent, CardHeader, CardTitle } from "@/components/ui/card";
import { Button } from "@/components/ui/button";
import { Input } from "@/components/ui/input";
import { Badge } from "@/components/ui/badge";
import { TrendingUp, TrendingDown, Search, Eye } from "lucide-react";
import { Stock, QuickAnalysis } from "@/types/stock";

interface StockListProps {
  onSelectStock: (ticker: string) => void;
  selectedStock?: string;
}

export function StockList({ onSelectStock, selectedStock }: StockListProps) {
  const [stocks, setStocks] = useState<Stock[]>([]);
  const [searchTerm, setSearchTerm] = useState("");
  const [loading, setLoading] = useState(true);
  const [analyses, setAnalyses] = useState<Record<string, QuickAnalysis>>({});

  useEffect(() => {
    fetchStocks();
  }, []);

  const fetchStocks = async () => {
    try {
      const response = await fetch("/api/v1/stocks", {
        method: "GET",
        headers: {
          "Content-Type": "application/json",
          "Accept": "application/json",
        },
      });
      
      if (!response.ok) {
        throw new Error(`HTTP error! status: ${response.status}`);
      }
      
      const data = await response.json();
      if (data.success) {
        setStocks(data.stocks);
      } else {
        console.error("API returned error:", data);
      }
    } catch (error) {
      console.error("Failed to fetch stocks:", error);
      console.error("Error details:", error instanceof Error ? error.message : String(error));
    } finally {
      setLoading(false);
    }
  };

  const getQuickAnalysis = async (ticker: string) => {
    if (analyses[ticker]) return;

    try {
      const response = await fetch("/api/v1/quick-analyze", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ ticker }),
      });
      const data = await response.json();
      if (data.success) {
        setAnalyses(prev => ({ ...prev, [ticker]: data }));
      }
    } catch (error) {
      console.error(`Failed to get analysis for ${ticker}:`, error);
    }
  };

  const filteredStocks = stocks.filter(stock =>
    stock.ticker.toLowerCase().includes(searchTerm.toLowerCase()) ||
    stock.name.toLowerCase().includes(searchTerm.toLowerCase())
  );

  const getRecommendationColor = (recommendation: string) => {
    switch (recommendation) {
      case "BUY": return "bg-green-100 text-green-800";
      case "SELL": return "bg-red-100 text-red-800";
      default: return "bg-gray-100 text-gray-800";
    }
  };

  if (loading) {
    return (
      <div className="space-y-4">
        <div className="animate-pulse">
          <div className="h-10 bg-gray-200 rounded mb-4"></div>
          {[...Array(5)].map((_, i) => (
            <div key={i} className="h-20 bg-gray-200 rounded mb-2"></div>
          ))}
        </div>
      </div>
    );
  }

  return (
    <div className="h-full flex flex-col">
      <div className="p-2 sm:p-3 lg:p-4 border-b">
        <div className="flex items-center space-x-2">
          <div className="relative flex-1">
            <Search className="absolute left-2 sm:left-3 top-1/2 transform -translate-y-1/2 text-muted-foreground h-3 w-3 sm:h-4 sm:w-4" />
            <Input
              placeholder="Tìm kiếm cổ phiếu..."
              value={searchTerm}
              onChange={(e) => setSearchTerm(e.target.value)}
              className="pl-8 sm:pl-10 text-sm sm:text-base"
            />
          </div>
        </div>
      </div>

      <div className="flex-1 overflow-y-auto">
        <div className="p-2 sm:p-3 lg:p-4 space-y-2 sm:space-y-3">
        {filteredStocks.map((stock) => {
          const analysis = analyses[stock.ticker];
          const isPositive = (stock.change || 0) >= 0;

          return (
            <Card
              key={stock.ticker}
              className={`cursor-pointer transition-all hover:shadow-md ${
                selectedStock === stock.ticker ? "ring-2 ring-blue-500" : ""
              }`}
              onClick={() => {
                onSelectStock(stock.ticker);
                getQuickAnalysis(stock.ticker);
              }}
            >
              <CardContent className="p-2 sm:p-3 lg:p-4">
                <div className="flex items-center justify-between">
                  <div className="flex-1 min-w-0">
                    <div className="flex items-center space-x-1 sm:space-x-2">
                      <h3 className="font-semibold text-sm sm:text-base lg:text-lg text-foreground truncate">{stock.ticker}</h3>
                      <span className="text-xs sm:text-sm text-muted-foreground hidden sm:block truncate">{stock.name}</span>
                    </div>
                    <div className="flex flex-col sm:flex-row sm:items-center sm:space-x-2 sm:space-y-0 space-y-1 mt-1">
                      <div className="text-lg sm:text-xl lg:text-2xl font-bold text-foreground">
                        {stock.current_price ? stock.current_price.toLocaleString() : 'N/A'}đ
                      </div>
                      <div className={`flex items-center space-x-1 ${
                        isPositive ? "text-green-600 dark:text-green-400" : "text-red-600 dark:text-red-400"
                      }`}>
                        {isPositive ? (
                          <TrendingUp className="h-3 w-3 sm:h-4 sm:w-4" />
                        ) : (
                          <TrendingDown className="h-3 w-3 sm:h-4 sm:w-4" />
                        )}
                        <span className="font-medium text-xs sm:text-sm">
                          {stock.change ? (isPositive ? "+" : "") + stock.change.toLocaleString() : 'N/A'}đ
                        </span>
                        <span className="text-xs hidden sm:inline">
                          ({stock.change_percent ? (isPositive ? "+" : "") + stock.change_percent.toFixed(2) : 'N/A'}%)
                        </span>
                      </div>
                    </div>
                    <div className="text-xs sm:text-sm text-muted-foreground mt-1">
                      KL: {stock.volume ? stock.volume.toLocaleString() : 'N/A'}
                    </div>
                  </div>

                  <div className="flex flex-col items-end space-y-2">
                    {analysis && (
                      <Badge className={getRecommendationColor(analysis.recommendation)}>
                        {analysis.recommendation}
                      </Badge>
                    )}
                    <Button variant="ghost" size="sm">
                      <Eye className="h-4 w-4" />
                    </Button>
                  </div>
                </div>
              </CardContent>
            </Card>
          );
        })}
        </div>
      </div>
    </div>
  );
}
