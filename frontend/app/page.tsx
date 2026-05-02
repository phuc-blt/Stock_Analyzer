"use client";

import { useState } from "react";
import { StockList } from "@/components/stock-list";
import { ChatInterface } from "@/components/chat-interface";
import { AnalysisDashboard } from "@/components/analysis-dashboard";
import { ThemeToggle } from "@/components/theme-toggle";
import { Tabs, TabsContent, TabsList, TabsTrigger } from "@/components/ui/tabs";
import { Card, CardContent, CardHeader, CardTitle } from "@/components/ui/card";
import { TrendingUp, MessageCircle, BarChart3 } from "lucide-react";

export default function Home() {
  const [selectedStock, setSelectedStock] = useState<string>();
  const [analysis, setAnalysis] = useState<any>();
  const [isAnalyzing, setIsAnalyzing] = useState(false);

  const handleStockSelect = async (ticker: string) => {
    setSelectedStock(ticker);
    setIsAnalyzing(true);
    
    try {
      const response = await fetch("/api/v1/quick-analyze", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({
          ticker,
        }),
      });
      
      const data = await response.json();
      setAnalysis(data);
    } catch (error) {
      console.error("Failed to fetch analysis:", error);
    } finally {
      setIsAnalyzing(false);
    }
  };

  return (
    <div className="min-h-screen bg-background">
      <header className="bg-card border-b">
        <div className="max-w-full mx-auto px-2 sm:px-4 lg:px-6 xl:px-8">
          <div className="flex items-center justify-between h-12 sm:h-14 lg:h-16">
            <div className="flex items-center space-x-2 sm:space-x-3">
              <TrendingUp className="h-6 w-6 sm:h-7 sm:w-7 lg:h-8 lg:w-8 text-primary" />
              <div>
                <h1 className="text-lg sm:text-xl font-bold text-foreground">
                  Vietnam Stock Analyzer
                </h1>
                <p className="text-xs sm:text-sm text-muted-foreground hidden sm:block">
                  Multi-Agent AI Analysis System
                </p>
              </div>
            </div>
            <div className="flex items-center space-x-2 sm:space-x-4">
              <ThemeToggle />
              {selectedStock && (
                <div className="flex items-center space-x-2 hidden sm:flex">
                  <span className="text-xs sm:text-sm text-muted-foreground">Đang phân tích:</span>
                  <span className="px-2 sm:px-3 py-1 bg-primary text-primary-foreground rounded-full font-semibold text-xs sm:text-sm">
                    {selectedStock.toUpperCase()}
                  </span>
                </div>
              )}
            </div>
          </div>
        </div>
      </header>

      <main className="max-w-full mx-auto px-2 sm:px-4 lg:px-6 xl:px-8 py-4 sm:py-6">
        <div className="grid grid-cols-1 md:grid-cols-12 gap-3 sm:gap-4 lg:gap-6">
          {/* Stock List - Left Sidebar */}
          <div className="md:col-span-4 lg:col-span-4 xl:col-span-4">
            <Card className="h-full min-h-[400px] sm:min-h-[500px] lg:min-h-[600px]">
              <CardHeader className="pb-3 sm:pb-4">
                <CardTitle className="text-base sm:text-lg font-semibold">Danh Sách Cổ Phiếu</CardTitle>
              </CardHeader>
              <CardContent className="p-0">
                <StockList 
                  onSelectStock={handleStockSelect}
                  selectedStock={selectedStock}
                />
              </CardContent>
            </Card>
          </div>

          {/* Main Content Area */}
          <div className="md:col-span-8 lg:col-span-8 xl:col-span-8 space-y-3 sm:space-y-4 lg:space-y-6">
            {selectedStock ? (
              <Tabs defaultValue="dashboard" className="space-y-4">
                <TabsList className="grid w-full grid-cols-2">
                  <TabsTrigger value="dashboard" className="flex items-center space-x-2">
                    <BarChart3 className="h-4 w-4" />
                    <span>Bảng Điều Khiển</span>
                  </TabsTrigger>
                  <TabsTrigger value="chat" className="flex items-center space-x-2">
                    <MessageCircle className="h-4 w-4" />
                    <span>Chat Phân Tích</span>
                  </TabsTrigger>
                </TabsList>

                <TabsContent value="dashboard">
                  <AnalysisDashboard
                    ticker={selectedStock}
                    analysis={analysis}
                    isLoading={isAnalyzing}
                  />
                </TabsContent>

                <TabsContent value="chat">
                  <ChatInterface selectedStock={selectedStock} />
                </TabsContent>
              </Tabs>
            ) : (
              <Card className="h-[600px] flex items-center justify-center">
                <CardContent className="text-center">
                  <TrendingUp className="h-16 w-16 text-gray-400 mx-auto mb-4" />
                  <h2 className="text-2xl font-semibold text-gray-700 mb-2">
                    Chào mừng đến với Vietnam Stock Analyzer
                  </h2>
                  <p className="text-gray-500 max-w-md mx-auto">
                    Hệ thống phân tích chứng khoán sử dụng công nghệ Multi-Agent AI. 
                    Vui lòng chọn một cổ phiếu từ danh sách bên trái để bắt đầu phân tích.
                  </p>
                </CardContent>
              </Card>
            )}
          </div>
        </div>
      </main>
    </div>
  );
}
