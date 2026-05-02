"use client";

import { useState, useEffect, useRef } from "react";
import { Card, CardContent, CardHeader, CardTitle } from "@/components/ui/card";
import { Button } from "@/components/ui/button";
import { Input } from "@/components/ui/input";
import { ScrollArea } from "@/components/ui/scroll-area";
import { Avatar, AvatarFallback } from "@/components/ui/avatar";
import { Badge } from "@/components/ui/badge";
import { Send, Bot, User, TrendingUp, TrendingDown, Minus } from "lucide-react";
import { ChatMessage, StockAnalysis } from "@/types/stock";

interface ChatInterfaceProps {
  selectedStock?: string;
}

export function ChatInterface({ selectedStock }: ChatInterfaceProps) {
  const [messages, setMessages] = useState<ChatMessage[]>([]);
  const [input, setInput] = useState("");
  const [isLoading, setIsLoading] = useState(false);
  const scrollAreaRef = useRef<HTMLDivElement>(null);

  useEffect(() => {
    if (selectedStock && messages.length === 0) {
      // Auto-send welcome message when stock is selected
      const welcomeMessage: ChatMessage = {
        id: "welcome",
        role: "assistant",
        content: `Xin chào! Tôi là trợ lý phân tích chứng khoán. Tôi có thể giúp bạn phân tích cổ phiếu ${selectedStock} bằng hệ thống multi-agent thông minh. Bạn muốn biết điều gì về cổ phiếu này?`,
        timestamp: new Date().toISOString(),
        ticker: selectedStock,
      };
      setMessages([welcomeMessage]);
    }
  }, [selectedStock]);

  useEffect(() => {
    // Auto-scroll to bottom when new messages arrive
    if (scrollAreaRef.current) {
      scrollAreaRef.current.scrollTop = scrollAreaRef.current.scrollHeight;
    }
  }, [messages]);

  const handleSendMessage = async () => {
    if (!input.trim() || !selectedStock || isLoading) return;

    const userMessage = input.trim();
    setInput("");
    setIsLoading(true);

    // Add user message
    const userMsg: ChatMessage = {
      id: Date.now().toString(),
      role: "user",
      content: userMessage,
      timestamp: new Date().toISOString(),
      ticker: selectedStock,
    };

    setMessages((prev) => [...prev, userMsg]);

    try {
      // Use new chat API for dynamic analysis
      const response = await fetch("/api/v1/chat", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({
          ticker: selectedStock,
          message: userMessage,
        }),
      });

      const data = await response.json();
      
      // Add assistant response
      const assistantMsg: ChatMessage = {
        id: (Date.now() + 1).toString(),
        role: "assistant",
        content: data.response || "Xin lỗi, không thể phân tích câu hỏi của bạn.",
        timestamp: new Date().toISOString(),
        ticker: selectedStock,
        analysis: data,
      };

      setMessages((prev) => [...prev, assistantMsg]);
    } catch (error) {
      console.error("Failed to fetch chat analysis:", error);
      
      // Add error message
      const errorMsg: ChatMessage = {
        id: (Date.now() + 1).toString(),
        role: "assistant",
        content: "Xin lỗi, không thể kết nối đến server. Vui lòng thử lại sau.",
        timestamp: new Date().toISOString(),
        ticker: selectedStock,
      };
      
      setMessages((prev) => [...prev, errorMsg]);
    } finally {
      setIsLoading(false);
    }
  };

  const generateAnalysisResponse = (analysis: any): string => {
    if (!analysis.success) {
      return `Xin lỗi, không thể phân tích cổ phiếu ${analysis.ticker}. Lỗi: ${analysis.error}`;
    }

    let response = `## Phân Tích Nhanh Cổ Phiếu ${analysis.ticker?.toUpperCase() || 'N/A'}\n\n`;
    
    // Quick analysis data structure
    response += `**Khuyến nghị:** ${analysis.recommendation?.toUpperCase() || 'N/A'}\n`;
    response += `**Độ tin cậy:** ${analysis.confidence || "N/A"}%\n`;
    response += `**Giá hiện tại:** ${analysis.current_price ? analysis.current_price.toLocaleString() : 'N/A'}đ\n`;
    response += `**Công ty:** ${analysis.company_name || 'N/A'}\n\n`;
    
    if (analysis.key_signals) {
      response += `### Các Chỉ Báo Kỹ Thuật\n`;
      response += `**RSI:** ${analysis.key_signals.rsi || 'N/A'}\n`;
      response += `**MACD:** ${analysis.key_signals.macd || 'N/A'}\n`;
      response += `**MA20:** ${analysis.key_signals.ma20 ? analysis.key_signals.ma20.toLocaleString() : 'N/A'}đ\n`;
      response += `**MA50:** ${analysis.key_signals.ma50 ? analysis.key_signals.ma50.toLocaleString() : 'N/A'}đ\n`;
      response += `**Volume Ratio:** ${analysis.key_signals.volume_ratio || 'N/A'}\n`;
      response += `**P/E Ratio:** ${analysis.key_signals.pe_ratio || 'N/A'}\n\n`;
    }

    if (analysis.key_signals?.sentiment) {
      response += `### Tình Cảm Thị Trường\n`;
      response += `**Sentiment:** ${analysis.key_signals.sentiment}\n`;
      if (analysis.key_signals.sentiment_score !== undefined) {
        response += `**Sentiment Score:** ${analysis.key_signals.sentiment_score}\n`;
      }
      response += `\n`;
    }

    response += `---\n`;
    response += `*Phân tích nhanh được thực hiện bởi hệ thống multi-agent thông minh vào lúc ${new Date(analysis.timestamp).toLocaleString("vi-VN")}*`;

    return response;
  };

  const getRecommendationIcon = (recommendation?: string) => {
    switch (recommendation?.toLowerCase()) {
      case "buy":
        return <TrendingUp className="h-4 w-4 text-green-600" />;
      case "sell":
        return <TrendingDown className="h-4 w-4 text-red-600" />;
      default:
        return <Minus className="h-4 w-4 text-gray-600" />;
    }
  };

  const getRecommendationBadge = (recommendation?: string) => {
    switch (recommendation?.toLowerCase()) {
      case "buy":
        return <Badge className="bg-green-100 text-green-800">MUA</Badge>;
      case "sell":
        return <Badge className="bg-red-100 text-red-800">BÁN</Badge>;
      default:
        return <Badge className="bg-gray-100 text-gray-800">GIỮ</Badge>;
    }
  };

  return (
    <Card className="h-[500px] sm:h-[600px] lg:h-[650px] xl:h-[700px] flex flex-col max-w-full">
      <CardHeader className="pb-3 sm:pb-4">
        <CardTitle className="flex items-center space-x-2">
          <Bot className="h-4 w-4 sm:h-5 sm:w-5" />
          <span className="font-semibold text-sm sm:text-base">Chat Phân Tích Chứng Khoán</span>
          {selectedStock && (
            <Badge variant="outline" className="text-xs">{selectedStock.toUpperCase()}</Badge>
          )}
        </CardTitle>
      </CardHeader>
      <CardContent className="flex-1 flex flex-col p-0 overflow-hidden">
        <ScrollArea ref={scrollAreaRef} className="flex-1 p-4">
          <div className="space-y-4 max-w-full">
            {messages.map((message) => (
              <div
                key={message.id}
                className={`flex space-x-3 max-w-full ${
                  message.role === "user" ? "justify-end" : "justify-start"
                }`}
              >
                {message.role === "assistant" && (
                  <Avatar className="h-8 w-8 flex-shrink-0">
                    <AvatarFallback>
                      <Bot className="h-4 w-4" />
                    </AvatarFallback>
                  </Avatar>
                )}
                <div
                  className={`max-w-[70%] lg:max-w-[60%] rounded-lg p-3 overflow-hidden break-words ${
                    message.role === "user"
                      ? "bg-primary text-primary-foreground"
                      : "bg-muted text-foreground"
                  }`}
                >
                  {message.analysis?.recommendation && (
                    <div className="flex items-center space-x-2 mb-2 flex-wrap">
                      {getRecommendationIcon(message.analysis.recommendation)}
                      {getRecommendationBadge(message.analysis.recommendation)}
                    </div>
                  )}
                  <div className="whitespace-pre-wrap text-sm break-words overflow-hidden max-w-full">
                    {message.content}
                  </div>
                  <div className="text-xs opacity-70 mt-1">
                    {new Date(message.timestamp).toLocaleTimeString("vi-VN")}
                  </div>
                </div>
                {message.role === "user" && (
                  <Avatar className="h-8 w-8 flex-shrink-0">
                    <AvatarFallback>
                      <User className="h-4 w-4" />
                    </AvatarFallback>
                  </Avatar>
                )}
              </div>
            ))}
            {isLoading && (
              <div className="flex space-x-3 justify-start">
                <Avatar className="h-8 w-8 flex-shrink-0">
                  <AvatarFallback>
                    <Bot className="h-4 w-4" />
                  </AvatarFallback>
                </Avatar>
                <div className="bg-muted rounded-lg p-3">
                  <div className="flex space-x-1">
                    <div className="w-2 h-2 bg-muted-foreground rounded-full animate-bounce"></div>
                    <div className="w-2 h-2 bg-muted-foreground rounded-full animate-bounce delay-100"></div>
                    <div className="w-2 h-2 bg-muted-foreground rounded-full animate-bounce delay-200"></div>
                  </div>
                </div>
              </div>
            )}
          </div>
        </ScrollArea>
        <div className="p-4 border-t">
          <div className="flex space-x-2">
            <Input
              placeholder={
                selectedStock
                  ? `Nhập câu hỏi về ${selectedStock}...`
                  : "Vui lòng chọn cổ phiếu để bắt đầu..."
              }
              value={input}
              onChange={(e) => setInput(e.target.value)}
              onKeyPress={(e) => e.key === "Enter" && handleSendMessage()}
              disabled={!selectedStock || isLoading}
              className="placeholder:text-muted-foreground"
            />
            <Button
              onClick={handleSendMessage}
              disabled={!selectedStock || !input.trim() || isLoading}
            >
              <Send className="h-4 w-4" />
            </Button>
          </div>
        </div>
      </CardContent>
    </Card>
  );
}
