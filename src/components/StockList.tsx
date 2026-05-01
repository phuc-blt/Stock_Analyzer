'use client';

import { useState, useEffect } from 'react';
import { apiClient, Stock } from '@/lib/api';
import { Card, CardContent, CardHeader, CardTitle } from '@/components/ui/card';
import { Button } from '@/components/ui/button';
import { Input } from '@/components/ui/input';
import { formatCurrency, formatNumber } from '@/lib/utils';
import { Search, TrendingUp, TrendingDown } from 'lucide-react';

interface StockListProps {
  onStockSelect: (ticker: string) => void;
}

export function StockList({ onStockSelect }: StockListProps) {
  const [stocks, setStocks] = useState<Stock[]>([]);
  const [filteredStocks, setFilteredStocks] = useState<Stock[]>([]);
  const [loading, setLoading] = useState(true);
  const [searchTerm, setSearchTerm] = useState('');

  useEffect(() => {
    loadStocks();
  }, []);

  useEffect(() => {
    const filtered = stocks.filter(stock =>
      stock.ticker.toLowerCase().includes(searchTerm.toLowerCase()) ||
      stock.name.toLowerCase().includes(searchTerm.toLowerCase())
    );
    setFilteredStocks(filtered);
  }, [searchTerm, stocks]);

  const loadStocks = async () => {
    try {
      setLoading(true);
      const response = await apiClient.getStocks();
      if (response.success) {
        setStocks(response.stocks);
        setFilteredStocks(response.stocks);
      }
    } catch (error) {
      console.error('Failed to load stocks:', error);
    } finally {
      setLoading(false);
    }
  };

  if (loading) {
    return (
      <Card>
        <CardHeader>
          <CardTitle>Stocks</CardTitle>
        </CardHeader>
        <CardContent>
          <div className="space-y-2">
            {[...Array(5)].map((_, i) => (
              <div key={i} className="h-16 bg-gray-100 rounded animate-pulse" />
            ))}
          </div>
        </CardContent>
      </Card>
    );
  }

  return (
    <Card>
      <CardHeader>
        <CardTitle>Vietnam Stocks</CardTitle>
        <div className="relative">
          <Search className="absolute left-3 top-1/2 transform -translate-y-1/2 text-gray-400 h-4 w-4" />
          <Input
            placeholder="Search stocks..."
            value={searchTerm}
            onChange={(e) => setSearchTerm(e.target.value)}
            className="pl-10"
          />
        </div>
      </CardHeader>
      <CardContent>
        <div className="space-y-2 max-h-96 overflow-y-auto">
          {filteredStocks.map((stock) => (
            <div
              key={stock.ticker}
              className="flex items-center justify-between p-3 border rounded-lg hover:bg-gray-50 cursor-pointer transition-colors"
              onClick={() => onStockSelect(stock.ticker)}
            >
              <div className="flex-1">
                <div className="flex items-center gap-2">
                  <span className="font-semibold">{stock.ticker}</span>
                  <span className="text-sm text-gray-500">{stock.name}</span>
                </div>
                <div className="text-sm text-gray-500">{stock.sector}</div>
              </div>
              <div className="text-right">
                <div className="font-semibold">
                  {formatCurrency(stock.current_price)}
                </div>
                <div className="text-sm text-gray-500">
                  P/E: {stock.pe_ratio.toFixed(1)}
                </div>
              </div>
            </div>
          ))}
        </div>
      </CardContent>
    </Card>
  );
}
