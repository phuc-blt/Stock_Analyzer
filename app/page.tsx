'use client';

import { useState } from 'react';
import { StockList } from '@/components/StockList';
import { StockAnalysis } from '@/components/StockAnalysis';
import { MarketSentiment } from '@/components/MarketSentiment';
import { DarkModeToggle } from '@/components/ui/dark-mode-toggle';
import { TrendingUp, BarChart3 } from 'lucide-react';

export default function Home() {
  const [selectedTicker, setSelectedTicker] = useState<string>('');

  return (
    <div className="min-h-screen bg-background">
      {/* Header */}
      <header className="bg-card border-b">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
          <div className="flex items-center justify-between h-16">
            <div className="flex items-center gap-2">
              <TrendingUp className="h-8 w-8 text-primary" />
              <h1 className="text-2xl font-bold text-foreground">
                Vietnam Stock Analyzer
              </h1>
            </div>
            <div className="flex items-center gap-4">
              <div className="flex items-center gap-2 text-sm text-muted-foreground">
                <BarChart3 className="h-4 w-4" />
                <span>AI-Powered Analysis</span>
              </div>
              <DarkModeToggle />
            </div>
          </div>
        </div>
      </header>

      {/* Main Content */}
      <main className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-8">
        <div className="grid grid-cols-1 lg:grid-cols-3 gap-8">
          {/* Left Sidebar - Stock List */}
          <div className="lg:col-span-1">
            <StockList onStockSelect={setSelectedTicker} />
            
            {/* Market Sentiment */}
            <div className="mt-6">
              <MarketSentiment />
            </div>
          </div>

          {/* Main Content Area */}
          <div className="lg:col-span-2">
            {selectedTicker ? (
              <StockAnalysis ticker={selectedTicker} />
            ) : (
              <div className="bg-card rounded-lg border p-8 text-center">
                <TrendingUp className="h-16 w-16 text-muted-foreground mx-auto mb-4" />
                <h2 className="text-xl font-semibold text-foreground mb-2">
                  Welcome to Vietnam Stock Analyzer
                </h2>
                <p className="text-muted-foreground mb-4">
                  Select a stock from the list to view detailed analysis and recommendations.
                </p>
                <div className="text-sm text-muted-foreground max-w-md mx-auto">
                  <p className="mb-2">Features:</p>
                  <ul className="text-left space-y-1">
                    <li>• Real-time stock analysis</li>
                    <li>• Technical indicators</li>
                    <li>• Market sentiment analysis</li>
                    <li>• AI-powered recommendations</li>
                  </ul>
                </div>
              </div>
            )}
          </div>
        </div>
      </main>

      {/* Footer */}
      <footer className="bg-card border-t mt-12">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-6">
          <div className="text-center text-sm text-muted-foreground">
            <p>Vietnam Stock Multi-Agent Analyzer - Real-time AI-powered market insights</p>
          </div>
        </div>
      </footer>
    </div>
  );
}
